"""GraphRAG Pipeline — no-code indexing with OpenAI.

Phase 1: run graphrag index via subprocess, then ingest entities + relations.
Phase 2: ingest community reports directly into the community layer.

Requires EXTRACTION_BACKEND=graphrag and OPENAI_API_KEY in environment.
"""

from __future__ import annotations

import os
import subprocess

import streamlit as st


def main() -> None:
    from app.config import GRAPHRAG_ROOT, EXTRACTED_TEXT_DIR, EMBEDDING_DIMS, EXTRACTION_BACKEND
    from app.services.backend_factory import BackendFactory
    from app.services.graphrag_ingestor import GraphRAGIngestor
    from app.services.neo4j_migration import drop_vector_indexes, recreate_vector_indexes

    st.set_page_config(page_title="GraphRAG Pipeline", page_icon="FG", layout="wide")
    st.title("GraphRAG Pipeline")
    st.caption(
        "No-code startup knowledge graph extraction using OpenAI. "
        "Set EXTRACTION_BACKEND=graphrag and OPENAI_API_KEY."
    )

    # ------------------------------------------------------------------
    # Section 1 — Prerequisites check
    # ------------------------------------------------------------------
    st.subheader("Prerequisites")

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    txt_files = list(EXTRACTED_TEXT_DIR.glob("*.txt")) if EXTRACTED_TEXT_DIR.exists() else []

    backend_color = "green" if EXTRACTION_BACKEND == "graphrag" else "orange"
    prereqs = [
        {
            "Check": "EXTRACTION_BACKEND",
            "Value": EXTRACTION_BACKEND,
            "Status": "OK" if EXTRACTION_BACKEND == "graphrag" else "Warning",
        },
        {
            "Check": "OPENAI_API_KEY",
            "Value": "Set ✓" if openai_key else "Missing ✗",
            "Status": "OK" if openai_key else "Missing",
        },
        {
            "Check": "GRAPHRAG_ROOT",
            "Value": str(GRAPHRAG_ROOT),
            "Status": "Exists" if GRAPHRAG_ROOT.exists() else "Not found",
        },
        {
            "Check": "EXTRACTED_TEXT_DIR (.txt files)",
            "Value": str(EXTRACTED_TEXT_DIR),
            "Status": f"{len(txt_files)} file(s) found",
        },
    ]
    st.dataframe(prereqs, use_container_width=True)

    if EXTRACTION_BACKEND != "graphrag":
        st.warning("Set EXTRACTION_BACKEND=graphrag in your .env file to use this page.")

    st.divider()

    # ------------------------------------------------------------------
    # Section 2 — Workspace preparation
    # ------------------------------------------------------------------
    st.subheader("Step 1 — Prepare workspace")
    st.write(
        "Copies extracted .txt files into GRAPHRAG_ROOT/input/ ready for graphrag index."
    )

    if st.button("Prepare workspace"):
        try:
            ingestor = GraphRAGIngestor()
            n_copied = ingestor.prepare_graphrag_workspace(EXTRACTED_TEXT_DIR)
            st.success(f"Copied {n_copied} file(s) into {GRAPHRAG_ROOT}/input/")
            settings_path = GRAPHRAG_ROOT / "settings.yaml"
            st.info(
                f"settings.yaml expected at: `{settings_path}`. "
                "If it does not exist, copy it from `graphrag_settings/settings.yaml` "
                "in the project root before running graphrag index."
            )
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))

    st.divider()

    # ------------------------------------------------------------------
    # Section 3 — Run graphrag index
    # ------------------------------------------------------------------
    st.subheader("Step 2 — Run graphrag index")
    st.warning(
        "⚠ This calls the OpenAI API and may take 5-20 minutes per document batch. "
        "Estimated cost: ~$0.01-0.05 per document with gpt-4o-mini."
    )

    if st.button("Run graphrag index"):
        cmd = ["graphrag", "index", "--root", str(GRAPHRAG_ROOT)]
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=str(GRAPHRAG_ROOT),
            )
            log_area = st.empty()
            log_lines: list[str] = []
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None:
                    break
                if line:
                    log_lines.append(line.rstrip())
                    log_area.code("\n".join(log_lines[-40:]))  # rolling last 40 lines
            proc.wait()
            if proc.returncode == 0:
                st.success("graphrag index completed.")
            else:
                st.error(f"graphrag index failed (exit code {proc.returncode}).")
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))

    st.divider()

    # ------------------------------------------------------------------
    # Section 4 — Ingest into staging
    # ------------------------------------------------------------------
    st.subheader("Step 3 — Ingest entities & relations into validation queue")
    st.write(
        "Reads GraphRAG output parquets and appends candidate entities/relations to the "
        "staging JSON files. The human validation page (03) picks them up from there."
    )

    col_ent, col_rel = st.columns(2)
    with col_ent:
        if st.button("Ingest entities"):
            try:
                n = GraphRAGIngestor().ingest_entities()
                st.success(f"Added {n} candidate entities to the validation queue.")
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))
    with col_rel:
        if st.button("Ingest relations"):
            try:
                n = GraphRAGIngestor().ingest_relations()
                st.success(f"Added {n} candidate relations to the validation queue.")
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))

    st.divider()

    # ------------------------------------------------------------------
    # Section 5 — Phase 2: Community ingestion
    # ------------------------------------------------------------------
    st.subheader("Step 4 — Ingest community reports (Phase 2)")
    st.write(
        "Materialises GraphRAG community reports directly into the Neo4j community layer, "
        "bypassing LLM re-summarisation."
    )

    if st.button("Ingest communities from GraphRAG"):
        try:
            from app.services.neo4j_service import Neo4jService
            from app.services.community_service import CommunityService
            from app.services.llm_service import OllamaLLMService

            neo4j = Neo4jService()
            embed_fn = BackendFactory.create_embed_fn()
            llm = BackendFactory.create_llm()
            svc = CommunityService(neo4j_service=neo4j, llm_service=llm, embed_fn=embed_fn)
            n = GraphRAGIngestor().ingest_communities(svc)
            st.success(f"Ingested {n} communities from GraphRAG reports.")
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))

    st.divider()

    # ------------------------------------------------------------------
    # Section 6 — Vector index migration (Phase 2)
    # ------------------------------------------------------------------
    st.subheader("Vector index migration")
    st.write(
        f"Current EMBEDDING_DIMS: {EMBEDDING_DIMS}. "
        "If you are switching backends (Ollama 768-d ↔ OpenAI 1536-d), you must drop and "
        "recreate the Neo4j vector indexes. **This deletes all existing vector embeddings from Neo4j.**"
    )

    col_drop, col_recreate = st.columns(2)
    with col_drop:
        if st.button("Drop vector indexes"):
            try:
                from app.services.neo4j_service import Neo4jService

                neo4j = Neo4jService()
                dropped = drop_vector_indexes(neo4j)
                st.success(f"Dropped indexes: {', '.join(dropped) if dropped else '(none found)'}")
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))
    with col_recreate:
        if st.button("Recreate vector indexes"):
            try:
                from app.services.neo4j_service import Neo4jService

                neo4j = Neo4jService()
                recreate_vector_indexes(neo4j, EMBEDDING_DIMS)
                st.success(f"Vector indexes recreated with dims={EMBEDDING_DIMS}.")
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))


if __name__ == "__main__":
    main()
