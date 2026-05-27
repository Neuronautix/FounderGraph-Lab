"""Community summarisation service (Phase 7).

Microsoft GraphRAG-style graph-level summarisation:

1. **Detect** -- project the validated entity subgraph and run a clustering
   algorithm.  When the Neo4j GDS plugin is installed we use Louvain; if not,
   we degrade to a pure-Python label-propagation / union-find implementation
   so the feature still works in vanilla / community Neo4j installs.
2. **Summarise** -- per cluster, the LLM produces a 2-3 sentence description
   from member names + key edges.  The summary is embedded with the same
   model used elsewhere so a single vector index covers entity + community
   summaries.
3. **Materialise** -- write ``(:Community {id, summary, embedding, size,
   risk_exposure})`` nodes and reversible ``(:Entity)-[:IN_COMMUNITY]->
   (:Community)`` edges via :class:`Neo4jService` helpers.

``risk_exposure`` is the share of a community's members that are ``Risk``
entities OR ``Assumption`` entities flagged ``criticality='high'``.  It lets
the UI sort by *strategic* risk concentration rather than raw cluster size --
small communities that are entirely composed of high-criticality assumptions
tell a much louder story than a sprawling cluster of supporting evidence.

The service is intentionally driver-agnostic: the LLM is any object exposing
``generate_text(prompt) -> str``, the embed function is any callable
``str -> Sequence[float]``, and the Neo4j peer is duck-typed against the
helpers added in Phase 7 (``write_community_node`` / ``set_node_community``
/ ``community_summary_search``).  Tests inject minimal fakes for all three.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Protocol, Sequence


# ---------------------------------------------------------------------------
# Public dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Community:
    """A detected cluster of entity ids plus its LLM summary + embedding.

    ``id`` is deterministic across runs for a given member set so re-running
    ``detect()`` on an unchanged graph produces stable community ids (which
    in turn keeps IN_COMMUNITY edges from churning).  ``risk_exposure`` is
    the share of members carrying a high-criticality risk marker (see the
    module docstring); 0.0 for empty / risk-free clusters.
    """

    id: str
    member_ids: tuple[str, ...]
    size: int
    summary: str = ""
    embedding: tuple[float, ...] = ()
    risk_exposure: float = 0.0


@dataclass(frozen=True)
class MacroCommunity:
    """A Level-2 macro-cluster grouping related Level-1 communities.

    Produced by :meth:`CommunityService.aggregate`.  The id is deterministic
    from the sorted member community ids.  ``max_risk_exposure`` is the
    maximum ``risk_exposure`` across member communities so the UI can
    highlight macro-clusters with concentrated risk even when the macro
    summary is broad.
    """

    id: str
    member_community_ids: tuple[str, ...]
    total_entity_count: int
    summary: str = ""
    embedding: tuple[float, ...] = ()
    max_risk_exposure: float = 0.0


# ---------------------------------------------------------------------------
# Protocols (kept narrow so tests inject minimal fakes)
# ---------------------------------------------------------------------------


class _LLMLike(Protocol):
    def generate_text(self, prompt: str) -> str: ...


class _Neo4jLike(Protocol):
    def write_community_node(self, community: dict[str, Any]) -> None: ...

    def set_node_community(
        self, entity_ids: list[str], community_id: str
    ) -> None: ...

    def community_summary_search(
        self, query_embedding: list[float], k: int = ...
    ) -> list[dict[str, Any]]: ...

    def write_macro_community_node(self, macro: dict[str, Any]) -> None: ...

    def set_community_macro(
        self, community_ids: list[str], macro_id: str
    ) -> None: ...

    def macro_community_summary_search(
        self, query_embedding: list[float], k: int = ...
    ) -> list[dict[str, Any]]: ...


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


class _UnionFind:
    """Tiny union-find used by the GDS-less fallback clustering."""

    def __init__(self, members: Iterable[str]) -> None:
        self.parent: dict[str, str] = {m: m for m in members}

    def find(self, x: str) -> str:
        # Path compression so repeated lookups stay near-O(1).
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        # Deterministic ordering: smaller id becomes the root, which makes the
        # community id reproducible across runs.
        if ra < rb:
            self.parent[rb] = ra
        else:
            self.parent[ra] = rb


def _stable_community_id(member_ids: Sequence[str]) -> str:
    """Deterministic id derived from the sorted member list."""
    sorted_members = sorted(str(m) for m in member_ids if m)
    digest = hashlib.sha256("|".join(sorted_members).encode("utf-8")).hexdigest()
    return f"community-{digest[:12]}"


def _cosine_sim(a: Sequence[float], b: Sequence[float]) -> float:
    """Cosine similarity between two equal-length float sequences."""
    al, bl = list(a), list(b)
    if not al or not bl or len(al) != len(bl):
        return 0.0
    num = sum(x * y for x, y in zip(al, bl))
    da = sum(x * x for x in al) ** 0.5
    db = sum(y * y for y in bl) ** 0.5
    if da == 0.0 or db == 0.0:
        return 0.0
    return float(num / (da * db))


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class CommunityService:
    """Detect, summarise and materialise GraphRAG-style communities.

    Parameters
    ----------
    neo4j_service:
        A :class:`Neo4jService`-shaped peer.  The service uses the Phase 7
        helpers (``write_community_node`` / ``set_node_community`` /
        ``community_summary_search``) plus a generic ``_rows`` / ``driver``
        pair to read the validated subgraph for clustering.
    llm_service:
        Object exposing ``generate_text(prompt) -> str``.  Used for the
        per-community summary; failures degrade to a fallback summary built
        from member names so materialisation can still proceed.
    embed_fn:
        Callable ``str -> Sequence[float]``.  Reusing the same embed model
        as entity / chunk vectors keeps cosine scores comparable across the
        retrieval pipeline.
    """

    def __init__(
        self,
        neo4j_service: _Neo4jLike,
        llm_service: _LLMLike,
        embed_fn: Callable[[str], Sequence[float]],
    ) -> None:
        self.neo4j = neo4j_service
        self.llm = llm_service
        self.embed = embed_fn
        # GDS availability is cached on first probe; ``None`` means "not yet
        # probed", a bool means "we know".  Tests can preset this to bypass
        # the live probe.
        self._gds_available: bool | None = None

    # ------------------------------------------------------------------
    # GDS detection
    # ------------------------------------------------------------------

    def _has_gds(self) -> bool:
        """Return True if the Neo4j GDS plugin is callable.

        We probe via ``CALL gds.list() YIELD name`` which is the cheapest
        round-trip that exercises the procedure namespace.  The result is
        cached so we never pay the cost twice per service instance.
        """
        if self._gds_available is not None:
            return self._gds_available
        rows: list[dict[str, Any]] | None
        try:
            rows = self.neo4j._rows("CALL gds.list() YIELD name RETURN name LIMIT 1", {})  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001 -- any failure means "no GDS"
            rows = None
        self._gds_available = bool(rows)
        return self._gds_available

    # ------------------------------------------------------------------
    # Phase 7 public API
    # ------------------------------------------------------------------

    def detect(self, min_size: int = 2) -> list[Community]:
        """Cluster the validated entity subgraph into communities.

        Tries GDS Louvain first; falls back to a pure-Python connected-
        components (label-propagation flavoured) implementation if GDS is
        not installed.  Returns communities sorted by ``size`` descending;
        clusters smaller than ``min_size`` are dropped.
        """
        if self._has_gds():
            try:
                clusters = self._detect_gds()
            except Exception:  # noqa: BLE001 -- fall back on any GDS hiccup
                clusters = self._detect_fallback()
        else:
            clusters = self._detect_fallback()

        # Each cluster carries the member entity dicts (id + type + maybe
        # criticality) so we can compute risk_exposure deterministically here.
        communities: list[Community] = []
        for members in clusters:
            if len(members) < max(2, int(min_size)):
                continue
            member_ids = tuple(sorted(str(m["id"]) for m in members if m.get("id")))
            if not member_ids:
                continue
            cid = _stable_community_id(member_ids)
            risk = self._risk_exposure(members)
            communities.append(
                Community(
                    id=cid,
                    member_ids=member_ids,
                    size=len(member_ids),
                    risk_exposure=risk,
                )
            )

        communities.sort(key=lambda c: (-c.size, c.id))
        return communities

    def summarize(self, community: Community) -> Community:
        """Run an LLM summarisation + embedding pass over a community."""
        prompt = self._build_summary_prompt(community)
        summary_text = ""
        try:
            raw = self.llm.generate_text(prompt)
            summary_text = str(raw or "").strip()
        except Exception as exc:  # noqa: BLE001 -- never crash the batch
            summary_text = (
                f"Community of {community.size} entities "
                f"(LLM summary unavailable: {exc})."
            )
        if not summary_text:
            summary_text = (
                f"Community of {community.size} entities; "
                "members: " + ", ".join(community.member_ids[:6])
            )

        # Embedding -- the embed_fn may be expensive or off-line; surround it
        # with the same defensive handler so a single bad call doesn't poison
        # the whole materialisation pass.
        try:
            vec = tuple(float(v) for v in (self.embed(summary_text) or []))
        except Exception:  # noqa: BLE001
            vec = ()

        return Community(
            id=community.id,
            member_ids=community.member_ids,
            size=community.size,
            summary=summary_text,
            embedding=vec,
            risk_exposure=community.risk_exposure,
        )

    def materialize(self, communities: list[Community]) -> None:
        """Write ``(:Community)`` nodes and IN_COMMUNITY edges to Neo4j."""
        for c in communities or []:
            self.neo4j.write_community_node(
                {
                    "id": c.id,
                    "summary": c.summary,
                    "embedding": list(c.embedding),
                    "size": c.size,
                    "risk_exposure": c.risk_exposure,
                }
            )
            self.neo4j.set_node_community(list(c.member_ids), c.id)

    def search(
        self,
        question_embedding: list[float],
        k: int = 5,
    ) -> list[Community]:
        """Vector-search materialised community summaries by cosine similarity.

        Returns reconstructed :class:`Community` objects with score-bearing
        fields populated.  Embeddings are NOT round-tripped from the index
        because callers only need the summary + similarity score; member
        listings can be hydrated on demand by an explicit second query.
        """
        if not question_embedding:
            return []
        rows = self.neo4j.community_summary_search(question_embedding, k=int(k))
        results: list[Community] = []
        for row in rows or []:
            cid = str(row.get("id") or "")
            if not cid:
                continue
            results.append(
                Community(
                    id=cid,
                    member_ids=(),
                    size=int(row.get("size") or 0),
                    summary=str(row.get("summary") or ""),
                    embedding=(),
                    risk_exposure=float(row.get("risk_exposure") or 0.0),
                )
            )
        return results

    # ------------------------------------------------------------------
    # Level-2 macro-community API
    # ------------------------------------------------------------------

    def aggregate(
        self,
        communities: list[Community],
        threshold: float = 0.65,
    ) -> list[MacroCommunity]:
        """Cluster Level-1 communities into Level-2 macro-communities.

        When communities carry embeddings, pairs whose cosine similarity
        exceeds ``threshold`` are merged (Union-Find).  When embeddings are
        absent, the fallback groups communities that share entity-level edges
        between their member sets (connectivity-based).  A single community
        is returned as a singleton macro; an empty list returns an empty list.
        """
        if not communities:
            return []
        if len(communities) == 1:
            return [self._build_macro(communities)]
        has_embeddings = any(len(c.embedding) > 0 for c in communities)
        groups = (
            self._aggregate_by_similarity(communities, threshold)
            if has_embeddings
            else self._aggregate_by_connectivity(communities)
        )
        return [self._build_macro(g) for g in groups]

    def summarize_macro(
        self,
        macro: MacroCommunity,
        communities: list[Community],
    ) -> MacroCommunity:
        """LLM-summarise a macro-community from its member Level-1 summaries."""
        by_id = {c.id: c for c in communities}
        bullets = [
            f"- {by_id[cid].summary}"
            for cid in macro.member_community_ids
            if cid in by_id and by_id[cid].summary
        ]
        prompt = (
            "You are analysing a portfolio of startup entities organised into "
            "thematic clusters.  Summarise the following group of related "
            "clusters in 2-3 sentences.  Identify the overarching strategic "
            "theme and any shared risk concentration.\n\n"
            "Cluster summaries:\n"
            + ("\n".join(bullets) if bullets else "(no summaries available)")
            + "\n\nReply in plain prose, no JSON."
        )
        summary_text = ""
        try:
            summary_text = str(self.llm.generate_text(prompt) or "").strip()
        except Exception as exc:  # noqa: BLE001
            summary_text = (
                f"Macro-community of {len(macro.member_community_ids)} clusters "
                f"(LLM unavailable: {exc})."
            )
        if not summary_text:
            summary_text = (
                f"Macro-community of {len(macro.member_community_ids)} clusters: "
                + ", ".join(macro.member_community_ids[:3])
            )
        try:
            vec = tuple(float(v) for v in (self.embed(summary_text) or []))
        except Exception:  # noqa: BLE001
            vec = ()
        return MacroCommunity(
            id=macro.id,
            member_community_ids=macro.member_community_ids,
            total_entity_count=macro.total_entity_count,
            summary=summary_text,
            embedding=vec,
            max_risk_exposure=macro.max_risk_exposure,
        )

    def materialize_macro(self, macros: list[MacroCommunity]) -> None:
        """Write ``(:MacroCommunity)`` nodes and IN_MACRO_COMMUNITY edges."""
        for m in macros or []:
            self.neo4j.write_macro_community_node(
                {
                    "id": m.id,
                    "summary": m.summary,
                    "embedding": list(m.embedding),
                    "total_entity_count": m.total_entity_count,
                    "max_risk_exposure": m.max_risk_exposure,
                    "member_count": len(m.member_community_ids),
                }
            )
            self.neo4j.set_community_macro(list(m.member_community_ids), m.id)

    def search_macro(
        self,
        question_embedding: list[float],
        k: int = 5,
    ) -> list[MacroCommunity]:
        """Vector-search materialised macro-community summaries."""
        if not question_embedding:
            return []
        rows = self.neo4j.macro_community_summary_search(
            question_embedding, k=int(k)
        )
        results: list[MacroCommunity] = []
        for row in rows or []:
            mid = str(row.get("id") or "")
            if not mid:
                continue
            results.append(
                MacroCommunity(
                    id=mid,
                    member_community_ids=(),
                    total_entity_count=int(row.get("total_entity_count") or 0),
                    summary=str(row.get("summary") or ""),
                    embedding=(),
                    max_risk_exposure=float(row.get("max_risk_exposure") or 0.0),
                )
            )
        return results

    # ------------------------------------------------------------------
    # Detection strategies
    # ------------------------------------------------------------------

    def _detect_gds(self) -> list[list[dict[str, Any]]]:
        """Run GDS Louvain over the validated entity projection.

        We use the anonymous projection variant (``gds.graph.project.cypher``
        is not strictly required for Louvain, but a projection keeps the
        algorithm scoped to validated entities only).  The output rows are
        ``{nodeId, communityId}`` pairs which we group back into membership
        lists.  Any failure here bubbles up so :meth:`detect` can fall back.
        """
        # Probe for member nodes + their type/criticality so the fallback and
        # GDS paths share the downstream risk-exposure calculation.
        members = self._load_validated_members()
        edges = self._load_validated_edges()
        if not members or not edges:
            return []
        # GDS Louvain via direct Cypher.  Using anonymous projection keeps us
        # from leaving a stale projection behind in the graph catalog.
        query = """
        CALL gds.louvain.stream({
          nodeQuery: 'MATCH (e:Entity) WHERE coalesce(e.validation_status, e.status) = "validated" RETURN id(e) AS id',
          relationshipQuery: 'MATCH (a:Entity)-[r]-(b:Entity) WHERE coalesce(a.validation_status, a.status) = "validated" AND coalesce(b.validation_status, b.status) = "validated" RETURN id(a) AS source, id(b) AS target'
        })
        YIELD nodeId, communityId
        RETURN gds.util.asNode(nodeId).id AS entity_id, communityId AS cluster
        """
        rows = self.neo4j._rows(query, {})  # type: ignore[attr-defined]
        by_id = {str(m["id"]): m for m in members}
        clusters: dict[Any, list[dict[str, Any]]] = {}
        for row in rows or []:
            entity_id = str(row.get("entity_id") or "")
            if entity_id not in by_id:
                continue
            cluster = row.get("cluster")
            clusters.setdefault(cluster, []).append(by_id[entity_id])
        return list(clusters.values())

    def _detect_fallback(self) -> list[list[dict[str, Any]]]:
        """Pure-Python connected-components clustering.

        Reads the validated entity slice plus all undirected edges between
        validated entities, then unions endpoints into groups.  Equivalent to
        a single-iteration label-propagation -- it picks up everything that's
        path-reachable inside the validated subgraph and stops there.
        """
        members = self._load_validated_members()
        edges = self._load_validated_edges()
        if not members:
            return []
        ids = [str(m["id"]) for m in members if m.get("id")]
        uf = _UnionFind(ids)
        valid = set(ids)
        for edge in edges:
            a = str(edge.get("source_id") or edge.get("source") or "")
            b = str(edge.get("target_id") or edge.get("target") or "")
            if a in valid and b in valid:
                uf.union(a, b)

        clusters: dict[str, list[dict[str, Any]]] = {}
        by_id = {str(m["id"]): m for m in members}
        for eid in ids:
            root = uf.find(eid)
            clusters.setdefault(root, []).append(by_id[eid])
        return list(clusters.values())

    # ------------------------------------------------------------------
    # Graph readers
    # ------------------------------------------------------------------

    def _load_validated_members(self) -> list[dict[str, Any]]:
        """Pull validated entities with the type + criticality fields we need."""
        query = """
        MATCH (e:Entity)
        WHERE coalesce(e.validation_status, e.status) = 'validated'
        RETURN e.id AS id, e.name AS name, e.type AS type,
               e.criticality AS criticality,
               labels(e) AS labels
        """
        try:
            rows = self.neo4j._rows(query, {})  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001 -- empty graph / fake driver / etc.
            return []
        out: list[dict[str, Any]] = []
        for row in rows or []:
            if not row.get("id"):
                continue
            out.append(
                {
                    "id": str(row["id"]),
                    "name": str(row.get("name") or row["id"]),
                    "type": str(row.get("type") or ""),
                    "criticality": str(row.get("criticality") or ""),
                    "labels": list(row.get("labels") or []),
                }
            )
        return out

    def _load_validated_edges(self) -> list[dict[str, Any]]:
        """Pull undirected edges between two validated entities."""
        query = """
        MATCH (a:Entity)-[r]-(b:Entity)
        WHERE coalesce(a.validation_status, a.status) = 'validated'
          AND coalesce(b.validation_status, b.status) = 'validated'
          AND a.id < b.id
        RETURN a.id AS source_id, b.id AS target_id, type(r) AS type
        """
        try:
            rows = self.neo4j._rows(query, {})  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001
            return []
        return list(rows or [])

    # ------------------------------------------------------------------
    # Risk exposure
    # ------------------------------------------------------------------

    @staticmethod
    def _is_risky(member: dict[str, Any]) -> bool:
        """A member is risk-bearing if it is a Risk OR a high-crit Assumption.

        We accept both the ``type`` field and the ``labels`` list so members
        loaded from a fake driver (which may only return one or the other)
        score consistently.
        """
        type_ = str(member.get("type") or "").strip()
        labels = [str(l) for l in (member.get("labels") or [])]
        if type_ == "Risk" or "Risk" in labels:
            return True
        if type_ == "Assumption" or "Assumption" in labels:
            crit = str(member.get("criticality") or "").strip().lower()
            if crit == "high":
                return True
        return False

    def _risk_exposure(self, members: list[dict[str, Any]]) -> float:
        if not members:
            return 0.0
        risky = sum(1 for m in members if self._is_risky(m))
        return risky / float(len(members))

    # ------------------------------------------------------------------
    # Level-2 aggregation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_macro(communities: list[Community]) -> MacroCommunity:
        sorted_ids = tuple(sorted(c.id for c in communities))
        digest = hashlib.sha256("|".join(sorted_ids).encode("utf-8")).hexdigest()
        macro_id = f"macro-{digest[:12]}"
        total = sum(c.size for c in communities)
        max_risk = max((c.risk_exposure for c in communities), default=0.0)
        return MacroCommunity(
            id=macro_id,
            member_community_ids=sorted_ids,
            total_entity_count=total,
            max_risk_exposure=max_risk,
        )

    def _aggregate_by_similarity(
        self,
        communities: list[Community],
        threshold: float,
    ) -> list[list[Community]]:
        """Union communities whose embedding cosine >= threshold."""
        uf = _UnionFind(c.id for c in communities)
        for i, ci in enumerate(communities):
            if not ci.embedding:
                continue
            for cj in communities[i + 1 :]:
                if not cj.embedding:
                    continue
                if _cosine_sim(ci.embedding, cj.embedding) >= threshold:
                    uf.union(ci.id, cj.id)
        groups: dict[str, list[Community]] = {}
        for c in communities:
            root = uf.find(c.id)
            groups.setdefault(root, []).append(c)
        return list(groups.values())

    def _aggregate_by_connectivity(
        self, communities: list[Community]
    ) -> list[list[Community]]:
        """Union communities that share entity-level edges between their members."""
        edges = self._load_validated_edges()
        edge_pairs: set[tuple[str, str]] = set()
        for e in edges:
            src = str(e.get("source_id") or e.get("source") or "")
            tgt = str(e.get("target_id") or e.get("target") or "")
            if src and tgt:
                edge_pairs.add((src, tgt))
                edge_pairs.add((tgt, src))
        entity_to_community: dict[str, str] = {
            eid: c.id for c in communities for eid in c.member_ids
        }
        uf = _UnionFind(c.id for c in communities)
        for src, tgt in edge_pairs:
            sc = entity_to_community.get(src)
            tc = entity_to_community.get(tgt)
            if sc and tc and sc != tc:
                uf.union(sc, tc)
        groups: dict[str, list[Community]] = {}
        for c in communities:
            root = uf.find(c.id)
            groups.setdefault(root, []).append(c)
        return list(groups.values())

    # ------------------------------------------------------------------
    # Prompting
    # ------------------------------------------------------------------

    @staticmethod
    def _build_summary_prompt(community: Community) -> str:
        """Build a short summarisation prompt from a community's member ids.

        The caller may attach richer context (member names + edge types) via
        a subclass override; the default prompt is intentionally minimal and
        deterministic so the JSON-mode Ollama path works with no extra
        context fetches.
        """
        sample = ", ".join(community.member_ids[:8])
        more = "" if community.size <= 8 else f" (+{community.size - 8} more)"
        return (
            "Summarise the following cluster of related startup-graph entities "
            "in 2-3 sentences.  Focus on the shared theme and any visible "
            "risk concentration.  Cluster member ids: "
            f"{sample}{more}.  Reply in plain prose, no JSON."
        )


__all__ = [
    "Community",
    "MacroCommunity",
    "CommunityService",
]
