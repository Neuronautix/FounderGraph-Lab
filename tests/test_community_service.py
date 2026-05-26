"""Tests for the Phase 7 :class:`CommunityService`.

The service is exercised against captured-query FakeDriver fakes (matching
the patterns used in ``tests/test_vector_index.py``) plus a tiny LLM stub.
We never touch a live Neo4j / Ollama instance here -- every assertion is on
the query text the service emits or on the Python-side dataclass output.
"""

from __future__ import annotations

import hashlib
from typing import Any

import pytest

from app.services.community_service import Community, CommunityService, MacroCommunity
from app.services.hybrid_retriever import (
    HybridRetriever,
    RetrievalWeights,
    RetrievedItem,
)


# ---------------------------------------------------------------------------
# Stubs
# ---------------------------------------------------------------------------


def _deterministic_embed(text: str) -> list[float]:
    """Hash-based 768-d vector so tests are byte-stable across runs."""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return [(digest[i % 32] / 255.0) for i in range(768)]


class _StubLLM:
    """LLM stub: returns a fixed string (or raises a queued exception)."""

    def __init__(self, response: str | Exception = "summary text"):
        self.response = response
        self.calls: list[str] = []

    def generate_text(self, prompt: str) -> str:
        self.calls.append(prompt)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class FakeNeo4j:
    """In-memory Neo4j-like peer.

    The clustering path calls ``_rows`` repeatedly; we route by recognising
    a substring of the Cypher.  Writes are pushed onto ``writes`` so tests
    can assert on the exact query / parameter pair.
    """

    def __init__(
        self,
        members: list[dict[str, Any]] | None = None,
        edges: list[dict[str, Any]] | None = None,
        gds_rows: list[dict[str, Any]] | None = None,
        search_rows: list[dict[str, Any]] | None = None,
    ) -> None:
        self.members = members or []
        self.edges = edges or []
        self.gds_rows = gds_rows  # None -> simulate "no GDS plugin"
        self.search_rows = search_rows or []
        self.writes: list[tuple[str, dict[str, Any]]] = []

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def _rows(self, query: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        if "gds.list()" in query:
            if self.gds_rows is None:
                raise RuntimeError("gds plugin not installed")
            return list(self.gds_rows)
        if "MATCH (e:Entity)" in query and "validation_status" in query and "labels(e)" in query:
            return list(self.members)
        if "MATCH (a:Entity)-[r]-(b:Entity)" in query:
            return list(self.edges)
        if "gds.louvain.stream" in query:
            # Each row is {entity_id, cluster} computed by the test harness.
            return list(getattr(self, "louvain_rows", []) or [])
        return []

    # ------------------------------------------------------------------
    # Writes (CommunityService.materialize)
    # ------------------------------------------------------------------

    def write_community_node(self, community: dict[str, Any]) -> None:
        # Capture the Cypher-shape we would otherwise emit so the test can
        # assert on it; the CommunityService never reaches into this private
        # detail.
        self.writes.append(
            (
                "MERGE (c:Community {id: $id}) "
                "SET c.summary = $summary, c.embedding = $embedding, "
                "c.size = $size, c.risk_exposure = $risk_exposure",
                dict(community),
            )
        )

    def set_node_community(
        self, entity_ids: list[str], community_id: str
    ) -> None:
        self.writes.append(
            (
                "UNWIND $ids AS id MATCH (e:Entity {id:id}) "
                "MERGE (e)-[r:IN_COMMUNITY]->(c:Community {id:$community_id})",
                {"ids": list(entity_ids), "community_id": community_id},
            )
        )

    def community_summary_search(
        self, query_embedding: list[float], k: int = 5
    ) -> list[dict[str, Any]]:
        self.writes.append(
            (
                "CALL db.index.vector.queryNodes('community_embedding', $k, $vec)",
                {"k": k, "vec": list(query_embedding)},
            )
        )
        return list(self.search_rows)[:k]

    def write_macro_community_node(self, macro: dict[str, Any]) -> None:
        self.writes.append(
            (
                "MERGE (m:MacroCommunity {id: $id}) SET ...",
                dict(macro),
            )
        )

    def set_community_macro(
        self, community_ids: list[str], macro_id: str
    ) -> None:
        self.writes.append(
            (
                "UNWIND $ids AS cid MATCH (c:Community {id:cid}) "
                "MERGE (c)-[r:IN_MACRO_COMMUNITY]->(m:MacroCommunity {id:$macro_id})",
                {"ids": list(community_ids), "macro_id": macro_id},
            )
        )

    def macro_community_summary_search(
        self, query_embedding: list[float], k: int = 5
    ) -> list[dict[str, Any]]:
        self.writes.append(
            (
                "CALL db.index.vector.queryNodes('macro_community_embedding', $k, $vec)",
                {"k": k, "vec": list(query_embedding)},
            )
        )
        return list(getattr(self, "macro_search_rows", []))[:k]


def _make_service(**fake_kwargs) -> tuple[CommunityService, FakeNeo4j, _StubLLM]:
    """Build a CommunityService wired against in-memory fakes."""
    neo = FakeNeo4j(**fake_kwargs)
    llm = _StubLLM("summary text")
    svc = CommunityService(neo4j_service=neo, llm_service=llm, embed_fn=_deterministic_embed)
    return svc, neo, llm


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_detect_falls_back_to_label_propagation_when_no_gds():
    """No GDS plugin -> pure-Python clustering still produces a community."""
    members = [
        {"id": "a", "name": "A", "type": "Assumption", "criticality": "", "labels": ["Entity", "Assumption"]},
        {"id": "b", "name": "B", "type": "Evidence", "criticality": "", "labels": ["Entity", "Evidence"]},
    ]
    edges = [{"source_id": "a", "target_id": "b", "type": "SUPPORTED_BY"}]
    svc, _, _ = _make_service(members=members, edges=edges, gds_rows=None)
    communities = svc.detect()
    assert svc._has_gds() is False
    assert len(communities) >= 1
    assert set(communities[0].member_ids) == {"a", "b"}


def test_detect_groups_connected_components():
    """A chain becomes one community; an isolated node is dropped below min_size."""
    members = [
        {"id": "a", "name": "A", "type": "Assumption", "criticality": "", "labels": []},
        {"id": "b", "name": "B", "type": "Assumption", "criticality": "", "labels": []},
        {"id": "c", "name": "C", "type": "Assumption", "criticality": "", "labels": []},
        # ``solo`` is not in any edge -> its connected component is {solo} only.
        {"id": "solo", "name": "Solo", "type": "Risk", "criticality": "", "labels": []},
    ]
    edges = [
        {"source_id": "a", "target_id": "b", "type": "RELATED_TO"},
        {"source_id": "b", "target_id": "c", "type": "RELATED_TO"},
    ]
    svc, _, _ = _make_service(members=members, edges=edges, gds_rows=None)
    communities = svc.detect(min_size=2)
    # Exactly one community (a-b-c).  Solo is below min_size, so it's dropped.
    assert len(communities) == 1
    assert set(communities[0].member_ids) == {"a", "b", "c"}
    assert all("solo" not in c.member_ids for c in communities)


def test_summarize_populates_summary_and_embedding():
    """The LLM stub returns a fixed summary; the embed_fn returns a 768-d vec."""
    svc, _, llm = _make_service()
    base = Community(
        id="community-test",
        member_ids=("a", "b"),
        size=2,
        risk_exposure=0.0,
    )
    enriched = svc.summarize(base)
    assert enriched.summary == "summary text"
    assert len(enriched.embedding) == 768
    # The LLM was invoked exactly once with the prompt builder's text.
    assert len(llm.calls) == 1
    # The default prompt frames the cluster as a "cluster of related ...
    # entities"; we assert on both nouns so a prompt-text rewrite need only
    # keep one of them.
    assert any(kw in llm.calls[0].lower() for kw in ("cluster", "community"))


def test_materialize_writes_community_and_in_community_edges():
    """The two write helpers emit MERGE Community / MERGE IN_COMMUNITY shapes."""
    svc, neo, _ = _make_service()
    community = Community(
        id="community-xyz",
        member_ids=("a", "b"),
        size=2,
        summary="brief summary",
        embedding=tuple([0.1] * 8),
        risk_exposure=0.5,
    )
    svc.materialize([community])
    captured = [q for q, _ in neo.writes]
    assert any(
        "MERGE (c:Community {id: $id}" in q for q in captured
    ), f"Expected community MERGE in {captured}"
    assert any(
        "MERGE (e)-[r:IN_COMMUNITY]->" in q for q in captured
    ), f"Expected IN_COMMUNITY MERGE in {captured}"
    # And the params should round-trip cleanly.
    community_call = next(
        params for q, params in neo.writes if "MERGE (c:Community" in q
    )
    assert community_call["id"] == "community-xyz"
    assert community_call["size"] == 2
    assert community_call["risk_exposure"] == 0.5


def test_search_uses_vector_index_call():
    """``search`` delegates to the community_embedding vector index."""
    search_rows = [
        {"id": "community-a", "summary": "Cluster A", "size": 5, "risk_exposure": 0.4, "score": 0.91},
        {"id": "community-b", "summary": "Cluster B", "size": 3, "risk_exposure": 0.1, "score": 0.80},
    ]
    svc, neo, _ = _make_service(search_rows=search_rows)
    results = svc.search([0.1] * 8, k=2)
    captured = [q for q, _ in neo.writes]
    assert any(
        "db.index.vector.queryNodes('community_embedding'" in q for q in captured
    ), f"Expected community_embedding index call in {captured}"
    assert [c.id for c in results] == ["community-a", "community-b"]
    assert results[0].risk_exposure == pytest.approx(0.4)


def test_risk_exposure_share_of_high_criticality_members():
    """4 members; 2 Risk + 1 Assumption(high) -> exposure = 3/4 = 0.75."""
    members = [
        {"id": "r1", "name": "Risk1", "type": "Risk", "criticality": "", "labels": []},
        {"id": "r2", "name": "Risk2", "type": "Risk", "criticality": "", "labels": []},
        {"id": "a1", "name": "AssumeHigh", "type": "Assumption", "criticality": "high", "labels": []},
        {"id": "a2", "name": "AssumeLow", "type": "Assumption", "criticality": "low", "labels": []},
    ]
    # Make all four reachable via a chain so they cluster together.
    edges = [
        {"source_id": "r1", "target_id": "r2", "type": "RELATED_TO"},
        {"source_id": "r2", "target_id": "a1", "type": "RELATED_TO"},
        {"source_id": "a1", "target_id": "a2", "type": "RELATED_TO"},
    ]
    svc, _, _ = _make_service(members=members, edges=edges, gds_rows=None)
    communities = svc.detect(min_size=2)
    assert len(communities) == 1
    assert communities[0].size == 4
    assert communities[0].risk_exposure == pytest.approx(0.75)


# ---------------------------------------------------------------------------
# Hybrid retriever integration test
# ---------------------------------------------------------------------------


class _CommunityServiceStub:
    """Minimal community-service stand-in used by the retriever-side test."""

    def __init__(self, communities: list[Community]):
        self.communities = communities
        self.calls: list[tuple[list[float], int]] = []

    def search(self, question_embedding: list[float], k: int = 5) -> list[Community]:
        self.calls.append((list(question_embedding), int(k)))
        return list(self.communities)[:k]


class _FakeNeoForRetriever:
    """Just enough Neo4j surface for HybridRetriever (no community helpers)."""

    def vector_search_entities(self, query_embedding, k=10, label_filter=None):
        return []

    def get_neighborhood(self, entity_ids, hops=1, allowed_relationships=None):
        return []


class _FakeQdrantForRetriever:
    def semantic_search(self, query, collection, limit):
        return {"available": True, "results": []}

    def embed(self, text):  # pragma: no cover -- not used
        return _deterministic_embed(text)


def test_hybrid_retriever_global_question_prepends_communities():
    """A global question with a community service attached yields a community item."""
    communities = [
        Community(
            id="community-1",
            member_ids=("a", "b"),
            size=2,
            summary="A high-level theme summary.",
            embedding=(),
            risk_exposure=0.5,
        )
    ]
    community_service = _CommunityServiceStub(communities=communities)
    retriever = HybridRetriever(
        neo4j_service=_FakeNeoForRetriever(),
        qdrant_service=_FakeQdrantForRetriever(),
        embed_fn=_deterministic_embed,
        weights=RetrievalWeights(alpha_cosine=0.6, beta_proximity=0.25, gamma_evidence=0.15),
        seed_k=4,
        community_service=community_service,
    )

    # A clearly "global" question -- contains "overall" + "summary".
    result = retriever.retrieve("What are the overall themes across the portfolio?")
    kinds = {item.kind for item in result.items}
    assert "community" in kinds
    community_items = [item for item in result.items if item.kind == "community"]
    assert community_items and community_items[0].id == "community-1"

    # Sanity check: a local-style question should NOT pull community items.
    local_result = retriever.retrieve("Tell me about assumption a")
    local_kinds = {item.kind for item in local_result.items}
    assert "community" not in local_kinds


def test_hybrid_retriever_without_community_service_unchanged():
    """No community service -> behaviour is identical to pre-Phase-7."""
    retriever = HybridRetriever(
        neo4j_service=_FakeNeoForRetriever(),
        qdrant_service=_FakeQdrantForRetriever(),
        embed_fn=_deterministic_embed,
        weights=RetrievalWeights(alpha_cosine=0.6, beta_proximity=0.25, gamma_evidence=0.15),
        seed_k=4,
    )
    result = retriever.retrieve("What are the overall themes across the portfolio?")
    assert all(item.kind != "community" for item in result.items)


# ---------------------------------------------------------------------------
# Level-2 macro-community tests
# ---------------------------------------------------------------------------


def _make_communities_with_embeddings() -> list[Community]:
    """Three communities: A&B are similar, C is orthogonal."""
    base_vec = _deterministic_embed("product module risk")
    ortho_vec = _deterministic_embed("finance runway cash")
    return [
        Community(id="c-a", member_ids=("e1", "e2"), size=2, risk_exposure=0.3, embedding=tuple(base_vec)),
        Community(id="c-b", member_ids=("e3", "e4"), size=2, risk_exposure=0.5, embedding=tuple(base_vec)),
        Community(id="c-c", member_ids=("e5",), size=1, risk_exposure=0.1, embedding=tuple(ortho_vec)),
    ]


def test_aggregate_groups_similar_communities():
    """Communities with identical embeddings should collapse into one macro."""
    svc, _, _ = _make_service()
    communities = _make_communities_with_embeddings()
    # c-a and c-b share the same vector -> cosine sim = 1.0 > 0.65 threshold.
    macros = svc.aggregate(communities, threshold=0.65)
    assert len(macros) >= 1
    # The two similar ones (c-a, c-b) must end up in the same macro.
    for macro in macros:
        if "c-a" in macro.member_community_ids:
            assert "c-b" in macro.member_community_ids, (
                "c-a and c-b share identical embeddings so must be co-clustered"
            )


def test_aggregate_fallback_connectivity_when_no_embeddings():
    """When no embeddings are present, fallback groups by entity-edge connectivity.

    The _aggregate_by_connectivity path reads edges from Neo4j.  We supply an
    edge between e2 (in c-x) and e3 (in c-y) so the two communities get
    union-found together.  c-z has no inter-community edge so it stays alone.
    """
    # Edge e2->e3 connects c-x and c-y through the entity graph.
    svc, _, _ = _make_service(edges=[{"source_id": "e2", "target_id": "e3", "type": "RELATED_TO"}])
    communities = [
        Community(id="c-x", member_ids=("e1", "e2"), size=2, risk_exposure=0.2),
        Community(id="c-y", member_ids=("e3", "e4"), size=2, risk_exposure=0.4),
        Community(id="c-z", member_ids=("e9",), size=1, risk_exposure=0.0),
    ]
    macros = svc.aggregate(communities)
    grouped_ids: list[tuple[str, ...]] = [m.member_community_ids for m in macros]
    shared_macro = next(
        (m for m in macros if "c-x" in m.member_community_ids and "c-y" in m.member_community_ids),
        None,
    )
    assert shared_macro is not None, f"c-x and c-y should be co-grouped via edge e2->e3; got {grouped_ids}"


def test_aggregate_empty_returns_empty():
    svc, _, _ = _make_service()
    assert svc.aggregate([]) == []


def test_aggregate_singleton_returns_one_macro():
    svc, _, _ = _make_service()
    c = Community(id="c-solo", member_ids=("e1",), size=1, risk_exposure=0.0, embedding=tuple(_deterministic_embed("x")))
    macros = svc.aggregate([c])
    assert len(macros) == 1
    assert "c-solo" in macros[0].member_community_ids


def test_summarize_macro_populates_summary_and_embedding():
    """summarize_macro calls the LLM and embeds the result."""
    svc, _, llm = _make_service()
    communities = [
        Community(id="c-1", member_ids=("e1",), size=1, summary="Product risk cluster."),
        Community(id="c-2", member_ids=("e2",), size=1, summary="Finance risk cluster."),
    ]
    bare_macro = MacroCommunity(
        id="macro-test",
        member_community_ids=("c-1", "c-2"),
        total_entity_count=2,
        max_risk_exposure=0.5,
    )
    enriched = svc.summarize_macro(bare_macro, communities)
    assert enriched.summary == "summary text"
    assert len(enriched.embedding) == 768
    assert len(llm.calls) == 1
    assert any(kw in llm.calls[0].lower() for kw in ("cluster", "theme", "strategic"))


def test_materialize_macro_writes_node_and_edges():
    """materialize_macro emits MacroCommunity MERGE + IN_MACRO_COMMUNITY MERGE."""
    svc, neo, _ = _make_service()
    macro = MacroCommunity(
        id="macro-xyz",
        member_community_ids=("c-a", "c-b"),
        total_entity_count=4,
        summary="Combined macro summary",
        embedding=tuple([0.1] * 8),
        max_risk_exposure=0.5,
    )
    svc.materialize_macro([macro])
    queries = [q for q, _ in neo.writes]
    assert any("MacroCommunity" in q for q in queries), f"Expected MacroCommunity MERGE in {queries}"
    assert any("IN_MACRO_COMMUNITY" in q for q in queries), f"Expected IN_MACRO_COMMUNITY MERGE in {queries}"
    node_call = next(params for q, params in neo.writes if "MacroCommunity" in q)
    assert node_call["id"] == "macro-xyz"
    assert node_call["total_entity_count"] == 4


def test_search_macro_delegates_to_vector_index():
    """search_macro delegates to macro_community_embedding vector index."""
    svc, neo, _ = _make_service()
    neo.macro_search_rows = [  # type: ignore[attr-defined]
        {"id": "macro-1", "summary": "Strategic theme A", "total_entity_count": 10, "max_risk_exposure": 0.6, "score": 0.92},
    ]
    results = svc.search_macro([0.1] * 8, k=3)
    queries = [q for q, _ in neo.writes]
    assert any("macro_community_embedding" in q for q in queries)
    assert len(results) == 1
    assert results[0].id == "macro-1"
    assert results[0].max_risk_exposure == pytest.approx(0.6)


# ---------------------------------------------------------------------------
# Hybrid retriever macro-community routing tests
# ---------------------------------------------------------------------------


class _CommunityServiceWithMacro(_CommunityServiceStub):
    """Extends the retriever-side stub with search_macro."""

    def __init__(self, communities: list[Community], macros: list[MacroCommunity]):
        super().__init__(communities)
        self.macros = macros
        self.macro_calls: list[tuple[list[float], int]] = []

    def search_macro(self, question_embedding: list[float], k: int = 5) -> list[MacroCommunity]:
        self.macro_calls.append((list(question_embedding), int(k)))
        return list(self.macros)[:k]


def test_hybrid_retriever_very_global_question_prepends_macro_items():
    """A very-global question yields macro_community items from search_macro."""
    macro = MacroCommunity(
        id="macro-1",
        member_community_ids=("c-a",),
        total_entity_count=5,
        summary="Top-level strategic overview.",
        max_risk_exposure=0.7,
    )
    community = Community(id="c-a", member_ids=("e1",), size=1, summary="Cluster A.")
    svc = _CommunityServiceWithMacro(communities=[community], macros=[macro])
    retriever = HybridRetriever(
        neo4j_service=_FakeNeoForRetriever(),
        qdrant_service=_FakeQdrantForRetriever(),
        embed_fn=_deterministic_embed,
        weights=RetrievalWeights(alpha_cosine=0.6, beta_proximity=0.25, gamma_evidence=0.15),
        seed_k=4,
        community_service=svc,
    )
    # "strategic overview" triggers _is_very_global_question.
    result = retriever.retrieve("Give me a strategic overview of all domains.")
    kinds = {item.kind for item in result.items}
    assert "macro_community" in kinds, f"Expected macro_community kind in {kinds}"
    macro_items = [item for item in result.items if item.kind == "macro_community"]
    assert macro_items[0].id == "macro-1"
    # Macro items should appear before non-macro items (prepended).
    first_non_macro = next((i for i, item in enumerate(result.items) if item.kind != "macro_community"), len(result.items))
    last_macro = max(i for i, item in enumerate(result.items) if item.kind == "macro_community")
    assert last_macro < first_non_macro or first_non_macro == len(result.items)


def test_hybrid_retriever_global_but_not_very_global_skips_macro():
    """A question that is global but not very-global should not yield macro items."""
    macro = MacroCommunity(
        id="macro-1",
        member_community_ids=("c-a",),
        total_entity_count=5,
        summary="Top-level strategic overview.",
        max_risk_exposure=0.7,
    )
    community = Community(id="c-a", member_ids=("e1",), size=1, summary="Cluster A.")
    svc = _CommunityServiceWithMacro(communities=[community], macros=[macro])
    retriever = HybridRetriever(
        neo4j_service=_FakeNeoForRetriever(),
        qdrant_service=_FakeQdrantForRetriever(),
        embed_fn=_deterministic_embed,
        weights=RetrievalWeights(alpha_cosine=0.6, beta_proximity=0.25, gamma_evidence=0.15),
        seed_k=4,
        community_service=svc,
    )
    # "overall" + "summary" trigger global but "overall themes" would trigger very-global;
    # "What is the overall summary?" does NOT contain "overall themes" verbatim.
    result = retriever.retrieve("What is the overall summary?")
    kinds = {item.kind for item in result.items}
    assert "macro_community" not in kinds, f"macro_community should not appear for non-very-global query; got {kinds}"
    # Community items may appear (it is a global question).
    assert svc.macro_calls == [], "search_macro should not have been called"
