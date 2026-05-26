"""Communities — graph-level summarisation (Phase 7).

This page exercises :class:`app.services.community_service.CommunityService`
against the live Neo4j graph.  The workflow is:

1. Click "Detect & summarize communities" to run Louvain (or the pure-Python
   fallback when GDS is missing), have the LLM produce a per-community
   summary, embed each summary, and write everything back to Neo4j.
2. Browse the materialised :class:`Community` nodes ranked by
   ``risk_exposure`` desc, then ``size`` desc.
3. Use the "Global question" box to vector-search community summaries
   directly -- this is the entry point exercised by the hybrid retriever's
   "global vs. local" routing.
"""

from __future__ import annotations

try:
    import streamlit as st
except ImportError:  # pragma: no cover -- streamlit only needed at runtime
    st = None  # type: ignore[assignment]

from app.services.community_service import Community, CommunityService, MacroCommunity
from app.services.neo4j_service import Neo4jService
from app.services.qdrant_service import QdrantService


def _short(text: str, limit: int = 240) -> str:
    """Truncate a summary string to ``limit`` characters with an ellipsis."""
    if not text:
        return ""
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _build_service() -> tuple[CommunityService | None, Neo4jService | None, str | None]:
    """Wire the community service to its live dependencies.

    Returns ``(service, neo4j, error)``.  When any dependency cannot be
    constructed we return a friendly error string so the page can render a
    banner instead of crashing.
    """
    try:
        neo4j = Neo4jService()
    except Exception as exc:  # noqa: BLE001
        return None, None, f"Neo4j: {exc}"
    try:
        qdrant = QdrantService()
        from app.services.backend_factory import BackendFactory as _BF
        llm = _BF.create_llm()
        embed_fn = _BF.create_embed_fn()
    except Exception as exc:  # noqa: BLE001
        return None, neo4j, f"LLM/embedding service: {exc}"
    service = CommunityService(neo4j_service=neo4j, llm_service=llm, embed_fn=embed_fn)
    return service, neo4j, None


def _fetch_materialised_communities(neo4j: Neo4jService) -> list[dict]:
    """Read every materialised :class:`Community` node for the table view."""
    query = """
    MATCH (c:Community)
    OPTIONAL MATCH (e:Entity)-[:IN_COMMUNITY]->(c)
    WITH c, collect({id: e.id, type: e.type, name: e.name})[0..6] AS sample,
         count(e) AS member_count
    RETURN c.id AS id, c.summary AS summary, c.size AS size,
           c.risk_exposure AS risk_exposure, member_count, sample
    ORDER BY c.risk_exposure DESC, c.size DESC
    """
    try:
        return neo4j._rows(query, {})  # type: ignore[attr-defined]
    except Exception as exc:  # noqa: BLE001
        if st is not None:
            st.warning(f"Could not list communities: {exc}")
        return []


def _fetch_materialised_macro_communities(neo4j: Neo4jService) -> list[dict]:
    """Read every materialised :class:`MacroCommunity` node for the table view."""
    query = """
    MATCH (m:MacroCommunity)
    OPTIONAL MATCH (c:Community)-[:IN_MACRO_COMMUNITY]->(m)
    WITH m, collect(c.id)[0..6] AS sample_communities, count(c) AS member_count
    RETURN m.id AS id, m.summary AS summary,
           m.total_entity_count AS total_entity_count,
           m.max_risk_exposure AS max_risk_exposure,
           m.member_count AS member_count, sample_communities
    ORDER BY m.max_risk_exposure DESC, m.total_entity_count DESC
    """
    try:
        return neo4j._rows(query, {})  # type: ignore[attr-defined]
    except Exception as exc:  # noqa: BLE001
        if st is not None:
            st.warning(f"Could not list macro-communities: {exc}")
        return []


def _fetch_community_members(neo4j: Neo4jService, community_id: str) -> list[dict]:
    """Expand a single community into its member entity rows."""
    query = """
    MATCH (e:Entity)-[:IN_COMMUNITY]->(c:Community {id: $cid})
    RETURN e.id AS id, e.name AS name, e.type AS type
    ORDER BY e.type, e.name
    """
    try:
        return neo4j._rows(query, {"cid": community_id})  # type: ignore[attr-defined]
    except Exception as exc:  # noqa: BLE001
        if st is not None:
            st.warning(f"Could not load members for {community_id}: {exc}")
        return []


def _run_pipeline(service: CommunityService) -> tuple[list[Community], str | None]:
    """Detect -> summarise -> materialise.  Returns the final community list."""
    if st is None:
        return [], "Streamlit is not installed."
    try:
        with st.spinner("Detecting communities…"):
            detected = service.detect()
    except Exception as exc:  # noqa: BLE001
        return [], f"Detection failed: {exc}"
    if not detected:
        return [], "No communities of size >=2 were found in the validated graph."
    progress = st.progress(0.0, text="Summarising communities…")
    summarised: list[Community] = []
    for idx, community in enumerate(detected, start=1):
        try:
            summarised.append(service.summarize(community))
        except Exception as exc:  # noqa: BLE001
            st.warning(f"Skipping {community.id}: {exc}")
            continue
        progress.progress(idx / len(detected), text=f"Summarising ({idx}/{len(detected)})")
    progress.empty()
    if not summarised:
        return [], "Summarisation pass produced no usable communities."
    try:
        with st.spinner("Writing communities to Neo4j…"):
            service.materialize(summarised)
    except Exception as exc:  # noqa: BLE001
        return summarised, f"Materialisation failed: {exc}"
    return summarised, None


def _run_macro_pipeline(
    service: CommunityService, communities: list[Community]
) -> tuple[list[MacroCommunity], str | None]:
    """Aggregate -> summarise -> materialise macro-communities."""
    if st is None:
        return [], "Streamlit is not installed."
    if not communities:
        return [], "No Level-1 communities to aggregate.  Run detection first."
    try:
        with st.spinner("Aggregating communities into macro-clusters…"):
            macros = service.aggregate(communities)
    except Exception as exc:  # noqa: BLE001
        return [], f"Aggregation failed: {exc}"
    if not macros:
        return [], "Aggregation produced no macro-communities."
    progress = st.progress(0.0, text="Summarising macro-communities…")
    summarised: list[MacroCommunity] = []
    for idx, macro in enumerate(macros, start=1):
        try:
            summarised.append(service.summarize_macro(macro, communities))
        except Exception as exc:  # noqa: BLE001
            st.warning(f"Skipping {macro.id}: {exc}")
            continue
        progress.progress(idx / len(macros), text=f"Summarising ({idx}/{len(macros)})")
    progress.empty()
    if not summarised:
        return [], "Macro summarisation produced no usable results."
    try:
        with st.spinner("Writing macro-communities to Neo4j…"):
            service.materialize_macro(summarised)
    except Exception as exc:  # noqa: BLE001
        return summarised, f"Macro materialisation failed: {exc}"
    return summarised, None


def main() -> None:
    if st is None:
        print("Streamlit is not installed.")
        return

    st.set_page_config(page_title="Communities — graph-level summarisation", layout="wide")
    st.title("Communities — graph-level summarization.")
    st.caption(
        "Microsoft GraphRAG-style clustering: detect communities (Louvain or "
        "label-propagation), summarise each one with an LLM, embed the summary, "
        "then vector-search for global questions."
    )
    from app.config import EXTRACTION_BACKEND as _backend
    if _backend == "graphrag":
        st.info("GraphRAG backend active — embeddings use OpenAI text-embedding-3-small (1536-d).")

    service, neo4j, error = _build_service()
    if error:
        st.error(
            f"Unable to initialise the community service: {error}. "
            "Configure NEO4J / OLLAMA / QDRANT env vars and reload."
        )

    # ------------------------------------------------------------------
    # Global-question search bar (sits above the table so it is reachable
    # even when no detection run has been triggered this session).
    # ------------------------------------------------------------------
    st.subheader("Global question")
    st.write(
        "Vector-search materialised community summaries by cosine similarity. "
        "Use this to ask broad, landscape-level questions (\"what are the "
        "overall themes across the portfolio?\")."
    )
    question = st.text_input("Global question", key="community-global-question")
    if st.button("Search communities", key="community-search", disabled=service is None):
        if not question.strip():
            st.warning("Enter a question to search community summaries.")
        elif service is None:
            st.warning("Community service is unavailable; cannot search.")
        else:
            try:
                vec = list(service.embed(question))
                matches = service.search(vec, k=5)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Search failed: {exc}")
                matches = []
            if not matches:
                st.info("No matching communities found.  Have you run detection?")
            else:
                st.write(f"Top {len(matches)} community matches:")
                rows = [
                    {
                        "id": m.id,
                        "size": m.size,
                        "risk_exposure": round(m.risk_exposure, 3),
                        "summary": _short(m.summary, 200),
                    }
                    for m in matches
                ]
                st.dataframe(rows, use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------
    # Detection / summarisation / materialisation pipeline.
    # ------------------------------------------------------------------
    st.subheader("Detect & summarise communities")
    st.write(
        "Runs Louvain (if the GDS plugin is installed) or a label-propagation "
        "fallback over the validated entity subgraph, then writes "
        ":Community nodes with embeddings via the community_embedding vector index."
    )
    if "last_communities" not in st.session_state:
        st.session_state["last_communities"] = []
    if st.button("Detect & summarize communities", disabled=service is None):
        if service is None:
            st.warning("Community service is unavailable.")
        else:
            communities, run_error = _run_pipeline(service)
            if run_error:
                st.error(run_error)
            else:
                st.session_state["last_communities"] = communities
                st.success(
                    f"Materialised {len(communities)} communities into Neo4j."
                )

    st.divider()

    # ------------------------------------------------------------------
    # Level-2 macro-community pipeline.
    # ------------------------------------------------------------------
    st.subheader("Macro-communities (Level-2 aggregation)")
    st.write(
        "Clusters related Level-1 communities into macro-clusters using embedding "
        "cosine similarity (threshold 0.65) or entity-edge connectivity when "
        "embeddings are absent.  Each macro-cluster gets an LLM summary and is "
        "written to Neo4j as a :MacroCommunity node linked via IN_MACRO_COMMUNITY."
    )
    macro_disabled = service is None
    if st.button("Aggregate & summarize macro-communities", disabled=macro_disabled):
        if service is None:
            st.warning("Community service is unavailable.")
        else:
            lvl1 = list(st.session_state.get("last_communities", []))
            if not lvl1 and neo4j is not None:
                # Re-detect if we have no in-memory communities from this run.
                try:
                    with st.spinner("Re-detecting communities for aggregation…"):
                        lvl1 = service.detect()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Detection failed: {exc}")
                    lvl1 = []
            macros, macro_error = _run_macro_pipeline(service, lvl1)
            if macro_error:
                st.error(macro_error)
            else:
                st.success(f"Materialised {len(macros)} macro-communities into Neo4j.")

    # Macro global-question search
    st.write(
        "Use the box below to vector-search macro-community summaries "
        "for the highest-level cross-domain questions "
        "(\"strategic overview\", \"overall themes across all domains\")."
    )
    macro_q = st.text_input("Very-global question", key="macro-global-question")
    if st.button("Search macro-communities", key="macro-search", disabled=service is None):
        if not macro_q.strip():
            st.warning("Enter a question to search macro-community summaries.")
        elif service is None:
            st.warning("Community service is unavailable; cannot search.")
        else:
            try:
                vec = list(service.embed(macro_q))
                matches = service.search_macro(vec, k=5)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Macro search failed: {exc}")
                matches = []
            if not matches:
                st.info("No matching macro-communities found.  Run aggregation first.")
            else:
                st.write(f"Top {len(matches)} macro-community matches:")
                rows = [
                    {
                        "id": m.id,
                        "total_entities": m.total_entity_count,
                        "max_risk_exposure": round(m.max_risk_exposure, 3),
                        "summary": _short(m.summary, 200),
                    }
                    for m in matches
                ]
                st.dataframe(rows, use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------
    # Materialised macro-communities table.
    # ------------------------------------------------------------------
    st.subheader("Materialised macro-communities")
    if neo4j is not None:
        macro_rows = _fetch_materialised_macro_communities(neo4j)
        if not macro_rows:
            st.info(
                "No :MacroCommunity nodes found.  Click 'Aggregate & summarize macro-communities' above."
            )
        else:
            st.metric("Macro-communities", len(macro_rows))
            macro_table = []
            for row in macro_rows:
                sample_cids = row.get("sample_communities") or []
                macro_table.append(
                    {
                        "id": row.get("id"),
                        "total_entities": int(row.get("total_entity_count") or 0),
                        "member_communities": int(row.get("member_count") or len(sample_cids)),
                        "max_risk_exposure": round(float(row.get("max_risk_exposure") or 0.0), 3),
                        "summary": _short(row.get("summary") or "", 200),
                        "community sample": ", ".join(str(c) for c in sample_cids[:4]),
                    }
                )
            st.dataframe(macro_table, use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------
    # Materialised communities table.
    # ------------------------------------------------------------------
    st.subheader("Materialised communities")
    if neo4j is None:
        st.info("No Neo4j connection — community list unavailable.")
        return

    rows = _fetch_materialised_communities(neo4j)
    if not rows:
        st.info(
            "No :Community nodes found.  Click 'Detect & summarize communities' "
            "above to populate them."
        )
    else:
        st.metric("Communities", len(rows))
        table_rows = []
        for row in rows:
            sample = row.get("sample") or []
            sample_text = ", ".join(
                f"{(s.get('type') or '?')}:{(s.get('name') or s.get('id') or '?')}"
                for s in sample
                if s and (s.get("id") or s.get("name"))
            )
            table_rows.append(
                {
                    "id": row.get("id"),
                    "size": int(row.get("size") or row.get("member_count") or 0),
                    "risk_exposure": round(float(row.get("risk_exposure") or 0.0), 3),
                    "summary": _short(row.get("summary") or "", 200),
                    "member sample": sample_text,
                }
            )
        st.dataframe(table_rows, use_container_width=True)

        for row in rows:
            cid = row.get("id")
            if not cid:
                continue
            with st.expander(f"View members of {cid}", expanded=False):
                members = _fetch_community_members(neo4j, cid)
                if not members:
                    st.write("(no member entities)")
                else:
                    st.dataframe(members, use_container_width=True)

    if neo4j is not None:
        try:
            neo4j.close()
        except Exception:  # noqa: BLE001 -- best-effort
            pass


if __name__ == "__main__":
    main()
