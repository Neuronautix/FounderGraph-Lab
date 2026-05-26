"""GraphRAG parquet → FounderGraph-Lab staging JSON bridge.

Reads the output of ``graphrag index`` (parquet files in GRAPHRAG_ROOT/output/)
and appends candidate entities and relations into the same staging JSON files
that EntityExtractor writes to.  The human validation page (03_validate_knowledge)
then picks them up unchanged.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import uuid
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

from app.config import (
    CANDIDATE_ENTITIES_JSON,
    CANDIDATE_RELATIONS_JSON,
    GRAPHRAG_ROOT,
)

# ---------------------------------------------------------------------------
# Ontology constants
# ---------------------------------------------------------------------------

_VALID_TYPES = {
    t.lower(): t
    for t in [
        "CustomerSegment",
        "Problem",
        "ValueProposition",
        "ProductFeature",
        "Assumption",
        "Evidence",
        "Risk",
        "Experiment",
        "Decision",
        "Milestone",
        "GrantCall",
        "Investor",
        "Partner",
        "Competitor",
        "IPAsset",
        "RegulatoryConstraint",
        "TechnicalDependency",
        "FinancialHypothesis",
    ]
}

_TYPE_MAP: dict[str, str] = {
    "organization": "Partner",
    "company": "Competitor",
    "person": "Decision",
    "product": "ProductFeature",
    "technology": "TechnicalDependency",
    "market": "CustomerSegment",
    "problem": "Problem",
    "risk": "Risk",
    "assumption": "Assumption",
    "milestone": "Milestone",
    "investor": "Investor",
    "grant": "GrantCall",
    "event": "Decision",
    "location": "CustomerSegment",
    "geo": "CustomerSegment",
}

# Namespace UUID used by _stable_id.  Never change this — it would invalidate
# all existing GraphRAG entity IDs stored in the staging files or Neo4j.
_GRAPHRAG_NAMESPACE = uuid.UUID("7a1f9f1e-3c2b-4d0e-9b5a-0123456789ab")

# Keyword → predicate mapping for relation inference (checked in order).
_PREDICATE_KEYWORDS: list[tuple[str, str]] = [
    ("fund", "FUNDS"),
    ("invest", "FUNDS"),
    ("compete", "COMPETES_ON"),
    ("risk", "THREATENS"),
    ("threaten", "THREATENS"),
    ("support", "SUPPORTED_BY"),
    ("depend", "DEPENDS_ON"),
    ("require", "DEPENDS_ON"),
    ("target", "TARGETS"),
    ("provide", "PROVIDES"),
    ("address", "ADDRESSES"),
    ("mitigat", "MITIGATES"),
    ("protect", "PROTECTS"),
    ("test", "TESTS"),
    ("based on", "BASED_ON"),
    ("mention", "MENTIONS"),
]


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------


class GraphRAGIngestor:
    """Bridge between Microsoft GraphRAG parquet output and FounderGraph staging.

    Typical usage::

        ingestor = GraphRAGIngestor()
        ingestor.prepare_graphrag_workspace(Path("data/extracted_text"))
        # … run `graphrag index` externally …
        n_entities = ingestor.ingest_entities()
        n_relations = ingestor.ingest_relations()

    The staging files written here are identical in schema to those produced by
    :class:`EntityExtractor`, so the human validation UI at
    *03_validate_knowledge* picks them up without modification.
    """

    def __init__(
        self,
        graphrag_output_dir: Path | str | None = None,
        staging_entities_path: Path | str | None = None,
        staging_relations_path: Path | str | None = None,
    ) -> None:
        self.graphrag_output_dir = Path(
            graphrag_output_dir if graphrag_output_dir is not None else GRAPHRAG_ROOT / "output"
        )
        self.staging_entities_path = Path(
            staging_entities_path if staging_entities_path is not None else CANDIDATE_ENTITIES_JSON
        )
        self.staging_relations_path = Path(
            staging_relations_path if staging_relations_path is not None else CANDIDATE_RELATIONS_JSON
        )

    # ------------------------------------------------------------------
    # Static helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _stable_id(name: str, type_: str) -> str:
        """Return a deterministic UUIDv5 for a given (name, type) pair.

        The key is namespaced under a fixed UUID so GraphRAG-sourced entity IDs
        never collide with LLM-extracted entity IDs (which use a different
        namespace in :func:`entity_extractor.stable_entity_id`).
        """
        key = f"graphrag::{name.strip().lower()}::{type_.lower()}"
        return str(uuid.uuid5(_GRAPHRAG_NAMESPACE, key))

    @staticmethod
    def _map_entity_type(raw_type: str) -> str:
        """Map a GraphRAG free-form entity type string to an ontology type.

        Resolution order:
        1. Direct case-insensitive match against the 18 valid ontology types.
        2. Keyword lookup in ``_TYPE_MAP``.
        3. Fallback to ``"Evidence"``.
        """
        lowered = raw_type.lower().strip()
        if lowered in _VALID_TYPES:
            return _VALID_TYPES[lowered]
        return _TYPE_MAP.get(lowered, "Evidence")

    # ------------------------------------------------------------------
    # Workspace preparation
    # ------------------------------------------------------------------

    def prepare_graphrag_workspace(self, docs_dir: Path | str) -> None:
        """Populate ``GRAPHRAG_ROOT/input/`` with text files for indexing.

        Copies all ``.txt`` files from *docs_dir* into the GraphRAG input
        directory and writes a ``.env`` placeholder so the CLI can pick up the
        OpenAI API key.

        Parameters
        ----------
        docs_dir:
            Directory containing ``.txt`` documents to index.  Typically
            ``EXTRACTED_TEXT_DIR`` after the extraction pipeline has run.

        Raises
        ------
        FileNotFoundError
            If *docs_dir* contains no ``.txt`` files.
        """
        docs_dir = Path(docs_dir)
        txt_files = list(docs_dir.glob("*.txt"))
        if not txt_files:
            raise FileNotFoundError(
                f"No .txt files found in {docs_dir}. "
                "Run the document extraction pipeline first."
            )

        input_dir = GRAPHRAG_ROOT / "input"
        input_dir.mkdir(parents=True, exist_ok=True)

        for src in txt_files:
            shutil.copy2(src, input_dir / src.name)

        # Write a .env stub so `graphrag index` can resolve the API key.
        env_path = GRAPHRAG_ROOT / ".env"
        if not env_path.exists():
            env_path.write_text("GRAPHRAG_API_KEY=${OPENAI_API_KEY}\n", encoding="utf-8")

    # ------------------------------------------------------------------
    # Parquet loading
    # ------------------------------------------------------------------

    def _load_parquet(self, filename: str) -> "pd.DataFrame":
        """Load a GraphRAG output parquet file into a DataFrame.

        Parameters
        ----------
        filename:
            Bare filename relative to ``self.graphrag_output_dir``,
            e.g. ``"entities.parquet"``.

        Raises
        ------
        ImportError
            If ``pandas`` or ``pyarrow`` are not installed.
        FileNotFoundError
            If the parquet file does not exist (i.e. ``graphrag index`` has
            not been run yet).
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for GraphRAG ingestion. "
                "Install it with: pip install 'foundergraph-lab[graphrag]'"
            ) from exc

        path = self.graphrag_output_dir / filename
        if not path.exists():
            raise FileNotFoundError(
                f"GraphRAG output not found: {path}. "
                "Run 'graphrag index' first."
            )
        return pd.read_parquet(path)

    # ------------------------------------------------------------------
    # Entity ingestion
    # ------------------------------------------------------------------

    def ingest_entities(self) -> int:
        """Read ``entities.parquet`` and write candidates to the staging file.

        Returns
        -------
        int
            Number of *newly added* entities (entities already present in the
            staging file by ID are skipped).

        Raises
        ------
        KeyError
            If the parquet file is missing required columns.
        """
        df = self._load_parquet("entities.parquet")

        # Normalise column names: GraphRAG v0.x used "name", v2.x uses "title".
        if "title" not in df.columns and "name" in df.columns:
            df = df.rename(columns={"name": "title"})

        required = {"title", "type", "description"}
        missing = required - set(df.columns)
        if missing:
            raise KeyError(
                f"entities.parquet is missing required columns: {sorted(missing)}. "
                f"Available columns: {sorted(df.columns.tolist())}"
            )

        # Build parquet int-id → stable UUID map for use by ingest_relations.
        entity_id_map: dict[Any, str] = {}

        new_items: list[dict[str, Any]] = []
        for _, row in df.iterrows():
            title = str(row.get("title") or "").strip()
            if not title:
                continue
            raw_type = str(row.get("type") or "").strip()
            mapped_type = self._map_entity_type(raw_type)
            description = str(row.get("description") or "")
            row_id = row.get("id")

            stable = self._stable_id(title, mapped_type)
            if row_id is not None:
                entity_id_map[row_id] = stable

            new_items.append(
                {
                    "id": stable,
                    "name": title,
                    "type": mapped_type,
                    "description": description,
                    "source_document_id": "graphrag",
                    "evidence": description,
                    "evidence_grade": "paraphrase",
                    "validation_status": "candidate",
                    "tags": ["graphrag"],
                    "properties": {
                        "graphrag_id": str(row_id) if row_id is not None else "",
                        "raw_type": raw_type,
                    },
                }
            )

        return self._merge_staging(self.staging_entities_path, new_items)

    # ------------------------------------------------------------------
    # Relation ingestion
    # ------------------------------------------------------------------

    def ingest_relations(self) -> int:
        """Read ``relationships.parquet`` and write candidates to the staging file.

        Entity name → stable UUID mapping is rebuilt from ``entities.parquet``
        so the subject/object IDs in the relations match those written by
        :meth:`ingest_entities`.

        Returns
        -------
        int
            Number of newly added relations.

        Raises
        ------
        KeyError
            If required columns are absent from the parquet files.
        """
        # Build entity name → stable UUID lookup from entities parquet.
        entities_df = self._load_parquet("entities.parquet")
        if "title" not in entities_df.columns and "name" in entities_df.columns:
            entities_df = entities_df.rename(columns={"name": "title"})

        entity_name_map: dict[str, str] = {}
        for _, row in entities_df.iterrows():
            title = str(row.get("title") or "").strip()
            if not title:
                continue
            raw_type = str(row.get("type") or "").strip()
            mapped_type = self._map_entity_type(raw_type)
            entity_name_map[title] = self._stable_id(title, mapped_type)

        # Load relationships.
        rel_df = self._load_parquet("relationships.parquet")

        required = {"source", "target", "description"}
        missing = required - set(rel_df.columns)
        if missing:
            raise KeyError(
                f"relationships.parquet is missing required columns: {sorted(missing)}. "
                f"Available columns: {sorted(rel_df.columns.tolist())}"
            )

        new_items: list[dict[str, Any]] = []
        for _, row in rel_df.iterrows():
            source = str(row.get("source") or "").strip()
            target = str(row.get("target") or "").strip()
            description = str(row.get("description") or "")

            subject_id = entity_name_map.get(source, "")
            object_id = entity_name_map.get(target, "")

            # Skip if either endpoint is unknown.
            if not subject_id or not object_id:
                continue

            predicate = self._infer_predicate(description)

            new_items.append(
                {
                    "id": str(uuid.uuid4()),
                    "subject_id": subject_id,
                    "predicate": predicate,
                    "object_id": object_id,
                    "source_document_id": "graphrag",
                    "evidence": description,
                }
            )

        return self._merge_staging(self.staging_relations_path, new_items)

    # ------------------------------------------------------------------
    # Community ingestion
    # ------------------------------------------------------------------

    def ingest_communities(self, community_service: Any) -> int:
        """Read community parquets and materialise Community nodes via Neo4j.

        Phase 2 community ingestion: reads ``communities.parquet`` and
        ``community_reports.parquet``, filters to level-0 (Leiden top-level
        partition), maps parquet integer entity IDs to stable UUIDs, and
        calls ``community_service.materialize(communities)`` to write
        ``(:Community)`` nodes and ``IN_COMMUNITY`` edges.

        Parameters
        ----------
        community_service:
            A fully initialised :class:`~app.services.community_service.CommunityService`
            instance (or compatible duck-type).

        Returns
        -------
        int
            Number of communities materialised.

        Raises
        ------
        KeyError
            If required columns are missing from either parquet file.
        """
        from app.services.community_service import Community

        # ---- Load entities for ID mapping ----------------------------------------
        entities_df = self._load_parquet("entities.parquet")
        if "title" not in entities_df.columns and "name" in entities_df.columns:
            entities_df = entities_df.rename(columns={"name": "title"})

        # parquet int id → stable UUID
        parquet_id_to_uuid: dict[Any, str] = {}
        for _, row in entities_df.iterrows():
            title = str(row.get("title") or "").strip()
            if not title:
                continue
            raw_type = str(row.get("type") or "").strip()
            mapped_type = self._map_entity_type(raw_type)
            row_id = row.get("id")
            if row_id is not None:
                parquet_id_to_uuid[row_id] = self._stable_id(title, mapped_type)

        # ---- Load communities -------------------------------------------------------
        comm_df = self._load_parquet("communities.parquet")

        required_comm = {"id", "level", "entity_ids"}
        missing_comm = required_comm - set(comm_df.columns)
        if missing_comm:
            raise KeyError(
                f"communities.parquet is missing required columns: {sorted(missing_comm)}. "
                f"Available columns: {sorted(comm_df.columns.tolist())}"
            )

        # ---- Load community reports -------------------------------------------------
        reports_df = self._load_parquet("community_reports.parquet")

        required_reports = {"community_id", "summary"}
        missing_reports = required_reports - set(reports_df.columns)
        if missing_reports:
            raise KeyError(
                f"community_reports.parquet is missing required columns: {sorted(missing_reports)}. "
                f"Available columns: {sorted(reports_df.columns.tolist())}"
            )

        # Build community_id → summary lookup.
        report_map: dict[str, str] = {}
        for _, row in reports_df.iterrows():
            cid = str(row.get("community_id") or "").strip()
            summary = str(row.get("summary") or "").strip()
            if cid:
                report_map[cid] = summary

        # ---- Filter to level-0 communities -----------------------------------------
        level_0 = comm_df[comm_df["level"] == 0]

        communities: list[Community] = []
        for _, row in level_0.iterrows():
            parquet_community_id = row.get("id")
            raw_entity_ids = row.get("entity_ids") or []

            # Map parquet int entity IDs to stable UUIDs.
            member_uuids = tuple(
                sorted(
                    parquet_id_to_uuid[eid]
                    for eid in raw_entity_ids
                    if eid in parquet_id_to_uuid
                )
            )
            if not member_uuids:
                continue

            # Derive stable community ID from member set.
            digest = hashlib.sha256("|".join(member_uuids).encode("utf-8")).hexdigest()
            community_id = f"community-{digest[:12]}"

            summary = report_map.get(str(parquet_community_id), "")

            communities.append(
                Community(
                    id=community_id,
                    member_ids=member_uuids,
                    size=len(member_uuids),
                    summary=summary,
                    embedding=(),
                    risk_exposure=0.0,
                )
            )

        community_service.materialize(communities)
        return len(communities)

    # ------------------------------------------------------------------
    # Staging merge helper
    # ------------------------------------------------------------------

    def _merge_staging(self, path: Path, new_items: list[dict[str, Any]]) -> int:
        """Read existing JSON array, deduplicate by ``id``, append, write back.

        Parameters
        ----------
        path:
            Absolute path to the staging JSON file.
        new_items:
            Dicts to merge in.  Items whose ``id`` already exists in the file
            are skipped (existing data wins to preserve human edits).

        Returns
        -------
        int
            Number of items actually added (excludes pre-existing duplicates).
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        existing: list[dict[str, Any]] = []
        if path.exists():
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                existing = raw if isinstance(raw, list) else []
            except (json.JSONDecodeError, OSError):
                existing = []

        existing_ids: set[str] = {str(item["id"]) for item in existing if item.get("id")}

        added = 0
        for item in new_items:
            item_id = str(item.get("id") or "")
            if item_id and item_id not in existing_ids:
                existing.append(item)
                existing_ids.add(item_id)
                added += 1

        text = json.dumps(existing, ensure_ascii=True, indent=2, sort_keys=True)
        tmp_path = path.with_suffix(f"{path.suffix}.tmp")
        tmp_path.write_text(f"{text}\n", encoding="utf-8")
        tmp_path.replace(path)

        return added

    # ------------------------------------------------------------------
    # Predicate inference
    # ------------------------------------------------------------------

    @staticmethod
    def _infer_predicate(description: str) -> str:
        """Infer a valid ontology predicate from a relationship description.

        Checks each keyword in :data:`_PREDICATE_KEYWORDS` (in order) against
        the lower-cased description.  Falls back to ``"RELATED_TO"``.
        """
        lower = description.lower()
        for keyword, predicate in _PREDICATE_KEYWORDS:
            if keyword in lower:
                return predicate
        return "RELATED_TO"
