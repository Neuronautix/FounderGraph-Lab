"""Tests for the GraphRAG / OpenAI backend layer.

Covers OpenAILLMService, OpenAIEmbedService, BackendFactory,
GraphRAGIngestor, and neo4j_migration without any live API calls,
real parquet files, or external services.

The openai package is mocked via sys.modules injection; pandas DataFrames
are constructed inline for the ingestor tests so pyarrow is not required.
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def _make_openai_mock(text_response: str = "ok", embed_vector: list[float] | None = None) -> MagicMock:
    """Return a fake openai module wired with configurable responses."""
    fake = MagicMock()
    # chat.completions.create
    msg = MagicMock()
    msg.content = text_response
    choice = MagicMock()
    choice.message = msg
    chat_resp = MagicMock()
    chat_resp.choices = [choice]
    fake.OpenAI.return_value.chat.completions.create.return_value = chat_resp
    # embeddings.create
    emb_data = MagicMock()
    emb_data.embedding = embed_vector or [0.1, 0.2, 0.3]
    emb_resp = MagicMock()
    emb_resp.data = [emb_data]
    fake.OpenAI.return_value.embeddings.create.return_value = emb_resp
    return fake


@pytest.fixture()
def mock_openai():
    """Inject a fake openai module for the duration of the test."""
    fake = _make_openai_mock()
    sys.modules["openai"] = fake
    yield fake
    sys.modules.pop("openai", None)


# ---------------------------------------------------------------------------
# OpenAILLMService
# ---------------------------------------------------------------------------


class TestOpenAILLMService:
    def test_generate_text_returns_stripped_content(self, mock_openai):
        mock_openai.OpenAI.return_value.chat.completions.create.return_value.choices[
            0
        ].message.content = "  hello world  "
        from app.services.openai_llm_service import OpenAILLMService

        svc = OpenAILLMService(api_key="test-key", model="gpt-test")
        result = svc.generate_text("say hi")
        assert result == "hello world"

    def test_generate_json_parses_valid_json(self, mock_openai):
        payload = {"entities": [{"name": "FAIR", "type": "ProductFeature"}]}
        mock_openai.OpenAI.return_value.chat.completions.create.return_value.choices[
            0
        ].message.content = json.dumps(payload)
        from app.services.openai_llm_service import OpenAILLMService

        svc = OpenAILLMService(api_key="k", model="m")
        assert svc.generate_json("extract") == payload

    def test_generate_json_raises_on_invalid_json(self, mock_openai):
        mock_openai.OpenAI.return_value.chat.completions.create.return_value.choices[
            0
        ].message.content = "not json at all"
        from app.services.openai_llm_service import OpenAILLMService
        from app.services.llm_service import LLMInvalidJSONError

        svc = OpenAILLMService(api_key="k", model="m")
        with pytest.raises(LLMInvalidJSONError):
            svc.generate_json("extract")

    def test_raises_when_openai_not_installed(self):
        sys.modules.pop("openai", None)
        # Make sure import fails by removing the module entirely.
        import builtins
        real_import = builtins.__import__

        def _block_openai(name, *args, **kwargs):
            if name == "openai":
                raise ImportError("No module named 'openai'")
            return real_import(name, *args, **kwargs)

        from app.services.openai_llm_service import OpenAILLMService
        from app.services.llm_service import LLMServiceError

        svc = OpenAILLMService(api_key="k", model="m")
        with patch("builtins.__import__", side_effect=_block_openai):
            with pytest.raises(LLMServiceError, match="pip install"):
                svc.generate_text("hi")


# ---------------------------------------------------------------------------
# OpenAIEmbedService
# ---------------------------------------------------------------------------


class TestOpenAIEmbedService:
    def test_embed_returns_vector(self, mock_openai):
        mock_openai.OpenAI.return_value.embeddings.create.return_value.data[
            0
        ].embedding = [0.5, 0.6, 0.7]
        from app.services.openai_embed_service import OpenAIEmbedService

        svc = OpenAIEmbedService(api_key="k", model="text-embedding-3-small")
        result = svc.embed("hello")
        assert result == [0.5, 0.6, 0.7]

    def test_call_delegates_to_embed(self, mock_openai):
        mock_openai.OpenAI.return_value.embeddings.create.return_value.data[
            0
        ].embedding = [1.0, 2.0]
        from app.services.openai_embed_service import OpenAIEmbedService

        svc = OpenAIEmbedService(api_key="k", model="m")
        assert svc("text") == svc.embed("text")

    def test_raises_when_openai_not_installed(self):
        import builtins
        real_import = builtins.__import__

        def _block_openai(name, *args, **kwargs):
            if name == "openai":
                raise ImportError("No module named 'openai'")
            return real_import(name, *args, **kwargs)

        sys.modules.pop("openai", None)
        from app.services.openai_embed_service import OpenAIEmbedService
        from app.services.llm_service import LLMServiceError

        svc = OpenAIEmbedService(api_key="k", model="m")
        with patch("builtins.__import__", side_effect=_block_openai):
            with pytest.raises(LLMServiceError, match="pip install"):
                svc.embed("text")


# ---------------------------------------------------------------------------
# BackendFactory
# ---------------------------------------------------------------------------


class TestBackendFactory:
    def test_backend_name_default_is_ollama(self):
        import app.services.backend_factory as bf

        with patch.object(bf, "EXTRACTION_BACKEND", "ollama"):
            assert bf.BackendFactory.backend_name() == "ollama"

    def test_is_graphrag_true_when_set(self):
        import app.services.backend_factory as bf

        with patch.object(bf, "EXTRACTION_BACKEND", "graphrag"):
            assert bf.BackendFactory.is_graphrag() is True

    def test_is_graphrag_false_for_ollama(self):
        import app.services.backend_factory as bf

        with patch.object(bf, "EXTRACTION_BACKEND", "ollama"):
            assert bf.BackendFactory.is_graphrag() is False

    def test_create_llm_returns_ollama_service_by_default(self):
        import app.services.backend_factory as bf
        from app.services.llm_service import OllamaLLMService

        with patch.object(bf, "EXTRACTION_BACKEND", "ollama"):
            llm = bf.BackendFactory.create_llm()
        assert isinstance(llm, OllamaLLMService)

    def test_create_llm_returns_openai_service_when_graphrag(self, mock_openai):
        import app.services.backend_factory as bf
        from app.services.openai_llm_service import OpenAILLMService

        with patch.object(bf, "EXTRACTION_BACKEND", "graphrag"):
            llm = bf.BackendFactory.create_llm()
        assert isinstance(llm, OpenAILLMService)

    def test_create_qdrant_service_passes_embed_fn_when_graphrag(self, mock_openai):
        import app.services.backend_factory as bf
        from app.services.qdrant_service import QdrantService

        with patch.object(bf, "EXTRACTION_BACKEND", "graphrag"):
            qdrant = bf.BackendFactory.create_qdrant_service()
        assert isinstance(qdrant, QdrantService)
        assert qdrant._embed_fn is not None


# ---------------------------------------------------------------------------
# GraphRAGIngestor — static helpers
# ---------------------------------------------------------------------------


class TestGraphRAGIngestorHelpers:
    def setup_method(self):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        self.cls = GraphRAGIngestor

    def test_stable_id_is_deterministic(self):
        a = self.cls._stable_id("Home Cage Monitoring", "ProductFeature")
        b = self.cls._stable_id("Home Cage Monitoring", "ProductFeature")
        assert a == b
        assert uuid.UUID(a)  # valid UUID

    def test_stable_id_differs_by_name(self):
        a = self.cls._stable_id("Alpha", "Risk")
        b = self.cls._stable_id("Beta", "Risk")
        assert a != b

    def test_stable_id_differs_by_type(self):
        a = self.cls._stable_id("Same", "Risk")
        b = self.cls._stable_id("Same", "Assumption")
        assert a != b

    def test_map_entity_type_direct_match(self):
        assert self.cls._map_entity_type("Risk") == "Risk"
        assert self.cls._map_entity_type("risk") == "Risk"
        assert self.cls._map_entity_type("ASSUMPTION") == "Assumption"

    def test_map_entity_type_keyword_fallback(self):
        assert self.cls._map_entity_type("organization") == "Partner"
        assert self.cls._map_entity_type("company") == "Competitor"
        assert self.cls._map_entity_type("investor") == "Investor"

    def test_map_entity_type_unknown_falls_back_to_evidence(self):
        assert self.cls._map_entity_type("unknown_xyz_type") == "Evidence"

    def test_infer_predicate_fund(self):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        assert GraphRAGIngestor._infer_predicate("This entity funds the project") == "FUNDS"

    def test_infer_predicate_default_related_to(self):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        assert GraphRAGIngestor._infer_predicate("some generic relationship") == "RELATED_TO"

    def test_infer_predicate_compete(self):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        assert GraphRAGIngestor._infer_predicate("they compete in the same market") == "COMPETES_ON"

    def test_infer_predicate_depend(self):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        assert GraphRAGIngestor._infer_predicate("the product depends on this technology") == "DEPENDS_ON"


# ---------------------------------------------------------------------------
# GraphRAGIngestor — workspace preparation
# ---------------------------------------------------------------------------


class TestGraphRAGIngestorWorkspace:
    def test_prepare_copies_txt_files(self, tmp_path):
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        (docs_dir / "doc1.txt").write_text("content 1", encoding="utf-8")
        (docs_dir / "doc2.txt").write_text("content 2", encoding="utf-8")
        (docs_dir / "ignore.md").write_text("markdown", encoding="utf-8")

        root = tmp_path / "graphrag"
        from app.services.graphrag_ingestor import GraphRAGIngestor

        ingestor = GraphRAGIngestor(graphrag_output_dir=root / "output")
        with patch("app.services.graphrag_ingestor.GRAPHRAG_ROOT", root):
            ingestor.prepare_graphrag_workspace(docs_dir)

        input_dir = root / "input"
        copied = {f.name for f in input_dir.iterdir()}
        assert "doc1.txt" in copied
        assert "doc2.txt" in copied
        assert "ignore.md" not in copied

    def test_prepare_raises_when_no_txt_files(self, tmp_path):
        docs_dir = tmp_path / "empty"
        docs_dir.mkdir()
        root = tmp_path / "graphrag"
        from app.services.graphrag_ingestor import GraphRAGIngestor

        ingestor = GraphRAGIngestor(graphrag_output_dir=root / "output")
        with patch("app.services.graphrag_ingestor.GRAPHRAG_ROOT", root):
            with pytest.raises(FileNotFoundError):
                ingestor.prepare_graphrag_workspace(docs_dir)


# ---------------------------------------------------------------------------
# GraphRAGIngestor — _merge_staging
# ---------------------------------------------------------------------------


class TestGraphRAGIngestorMergeStaging:
    def _make_ingestor(self, tmp_path):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        return GraphRAGIngestor(
            graphrag_output_dir=tmp_path / "output",
            staging_entities_path=tmp_path / "entities.json",
            staging_relations_path=tmp_path / "relations.json",
        )

    def test_merge_creates_file_when_absent(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        path = tmp_path / "entities.json"
        n = ingestor._merge_staging(path, [{"id": "abc", "name": "X"}])
        assert n == 1
        data = json.loads(path.read_text())
        assert len(data) == 1

    def test_merge_skips_existing_ids(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        path = tmp_path / "entities.json"
        path.write_text(json.dumps([{"id": "abc", "name": "Old"}]), encoding="utf-8")

        n = ingestor._merge_staging(path, [{"id": "abc", "name": "New"}, {"id": "xyz", "name": "Y"}])
        assert n == 1  # only xyz is new
        data = json.loads(path.read_text())
        existing = next(d for d in data if d["id"] == "abc")
        assert existing["name"] == "Old"  # original preserved

    def test_merge_appends_new_items(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        path = tmp_path / "entities.json"
        path.write_text(json.dumps([{"id": "a"}]), encoding="utf-8")
        n = ingestor._merge_staging(path, [{"id": "b"}, {"id": "c"}])
        assert n == 2
        assert len(json.loads(path.read_text())) == 3


# ---------------------------------------------------------------------------
# GraphRAGIngestor — ingest_entities
# ---------------------------------------------------------------------------


class TestGraphRAGIngestorIngestEntities:
    def _make_ingestor(self, tmp_path):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        return GraphRAGIngestor(
            graphrag_output_dir=tmp_path / "output",
            staging_entities_path=tmp_path / "entities.json",
            staging_relations_path=tmp_path / "relations.json",
        )

    def _make_entities_df(self):
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")
        return pd.DataFrame(
            [
                {"id": 1, "title": "Home Cage Monitoring", "type": "ProductFeature", "description": "HCM system"},
                {"id": 2, "title": "FAIR Compliance Risk", "type": "Risk", "description": "Risk of non-compliance"},
                {"id": 3, "title": "", "type": "Unknown", "description": "blank name — should be skipped"},
            ]
        )

    def test_ingest_entities_adds_candidates(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        df = self._make_entities_df()
        with patch.object(ingestor, "_load_parquet", return_value=df):
            n = ingestor.ingest_entities()
        assert n == 2  # blank-name row skipped
        data = json.loads((tmp_path / "entities.json").read_text())
        names = {d["name"] for d in data}
        assert "Home Cage Monitoring" in names
        assert "FAIR Compliance Risk" in names

    def test_ingest_entities_handles_name_column(self, tmp_path):
        """v0.x parquets use 'name' not 'title' — should be normalised."""
        ingestor = self._make_ingestor(tmp_path)
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")
        df = pd.DataFrame([{"id": 1, "name": "Old Style", "type": "Risk", "description": "desc"}])
        with patch.object(ingestor, "_load_parquet", return_value=df):
            n = ingestor.ingest_entities()
        assert n == 1
        data = json.loads((tmp_path / "entities.json").read_text())
        assert data[0]["name"] == "Old Style"

    def test_ingest_entities_raises_on_missing_columns(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")
        df = pd.DataFrame([{"id": 1, "title": "X"}])  # missing type, description
        with patch.object(ingestor, "_load_parquet", return_value=df):
            with pytest.raises(KeyError, match="missing required columns"):
                ingestor.ingest_entities()

    def test_ingest_entities_stable_id_matches_map_type(self, tmp_path):
        """Entity ID should match _stable_id(title, mapped_type)."""
        ingestor = self._make_ingestor(tmp_path)
        df = self._make_entities_df()
        with patch.object(ingestor, "_load_parquet", return_value=df):
            ingestor.ingest_entities()
        data = json.loads((tmp_path / "entities.json").read_text())
        hcm = next(d for d in data if d["name"] == "Home Cage Monitoring")
        expected_id = ingestor._stable_id("Home Cage Monitoring", "ProductFeature")
        assert hcm["id"] == expected_id


# ---------------------------------------------------------------------------
# GraphRAGIngestor — ingest_relations
# ---------------------------------------------------------------------------


class TestGraphRAGIngestorIngestRelations:
    def _make_ingestor(self, tmp_path):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        return GraphRAGIngestor(
            graphrag_output_dir=tmp_path / "output",
            staging_entities_path=tmp_path / "entities.json",
            staging_relations_path=tmp_path / "relations.json",
        )

    def _make_dfs(self):
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")
        entities = pd.DataFrame([
            {"id": 1, "title": "HCM Module", "type": "ProductFeature", "description": ""},
            {"id": 2, "title": "FAIR Risk", "type": "Risk", "description": ""},
        ])
        relations = pd.DataFrame([
            {"source": "HCM Module", "target": "FAIR Risk", "description": "mitigates the risk"},
            {"source": "HCM Module", "target": "Unknown Entity", "description": "unknown endpoint"},
        ])
        return entities, relations

    def test_ingest_relations_maps_predicates(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        entities_df, relations_df = self._make_dfs()

        def _load(filename):
            return entities_df if "entities" in filename else relations_df

        with patch.object(ingestor, "_load_parquet", side_effect=_load):
            n = ingestor.ingest_relations()

        assert n == 1  # unknown-endpoint row skipped
        data = json.loads((tmp_path / "relations.json").read_text())
        assert data[0]["predicate"] == "MITIGATES"

    def test_ingest_relations_skips_unknown_endpoints(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        entities_df, relations_df = self._make_dfs()

        def _load(filename):
            return entities_df if "entities" in filename else relations_df

        with patch.object(ingestor, "_load_parquet", side_effect=_load):
            n = ingestor.ingest_relations()
        assert n == 1  # second row has unknown target

    def test_ingest_relations_raises_on_missing_columns(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")
        entities_df = pd.DataFrame([{"id": 1, "title": "X", "type": "Risk", "description": ""}])
        bad_rel = pd.DataFrame([{"source": "X"}])  # missing target, description

        def _load(filename):
            return entities_df if "entities" in filename else bad_rel

        with patch.object(ingestor, "_load_parquet", side_effect=_load):
            with pytest.raises(KeyError, match="missing required columns"):
                ingestor.ingest_relations()


# ---------------------------------------------------------------------------
# GraphRAGIngestor — ingest_communities
# ---------------------------------------------------------------------------


class TestGraphRAGIngestorIngestCommunities:
    def _make_ingestor(self, tmp_path):
        from app.services.graphrag_ingestor import GraphRAGIngestor

        return GraphRAGIngestor(
            graphrag_output_dir=tmp_path / "output",
            staging_entities_path=tmp_path / "entities.json",
            staging_relations_path=tmp_path / "relations.json",
        )

    def _make_dfs(self):
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")
        entities = pd.DataFrame([
            {"id": 1, "title": "Entity A", "type": "Risk", "description": ""},
            {"id": 2, "title": "Entity B", "type": "Assumption", "description": ""},
        ])
        communities = pd.DataFrame([
            {"id": 0, "level": 0, "title": "Cluster 0", "entity_ids": [1, 2]},
            {"id": 1, "level": 1, "title": "Cluster 1 (deeper)", "entity_ids": [1]},  # filtered out
        ])
        reports = pd.DataFrame([
            {"community_id": "0", "summary": "Risk and assumption cluster."},
        ])
        return entities, communities, reports

    def test_ingest_communities_filters_level_0(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        entities_df, communities_df, reports_df = self._make_dfs()

        def _load(filename):
            if "entities" in filename:
                return entities_df
            if "community_reports" in filename:
                return reports_df
            return communities_df

        fake_svc = MagicMock()
        with patch.object(ingestor, "_load_parquet", side_effect=_load):
            n = ingestor.ingest_communities(fake_svc)

        assert n == 1  # only level-0 community
        fake_svc.materialize.assert_called_once()
        communities_passed = fake_svc.materialize.call_args[0][0]
        assert len(communities_passed) == 1

    def test_ingest_communities_attaches_summary(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        entities_df, communities_df, reports_df = self._make_dfs()

        def _load(filename):
            if "entities" in filename:
                return entities_df
            if "community_reports" in filename:
                return reports_df
            return communities_df

        fake_svc = MagicMock()
        with patch.object(ingestor, "_load_parquet", side_effect=_load):
            ingestor.ingest_communities(fake_svc)

        community = fake_svc.materialize.call_args[0][0][0]
        assert community.summary == "Risk and assumption cluster."

    def test_ingest_communities_raises_on_missing_columns(self, tmp_path):
        ingestor = self._make_ingestor(tmp_path)
        try:
            import pandas as pd
        except ImportError:
            pytest.skip("pandas not installed")
        entities_df = pd.DataFrame([{"id": 1, "title": "X", "type": "Risk", "description": ""}])
        bad_communities = pd.DataFrame([{"id": 0}])  # missing level, entity_ids
        reports_df = pd.DataFrame([{"community_id": "0", "summary": "s"}])

        def _load(filename):
            if "entities" in filename:
                return entities_df
            if "community_reports" in filename:
                return reports_df
            return bad_communities

        fake_svc = MagicMock()
        with patch.object(ingestor, "_load_parquet", side_effect=_load):
            with pytest.raises(KeyError, match="missing required columns"):
                ingestor.ingest_communities(fake_svc)


# ---------------------------------------------------------------------------
# neo4j_migration
# ---------------------------------------------------------------------------


class _FakeNeo4j:
    """Minimal Neo4j stub that records DDL calls and optionally raises."""

    def __init__(self, fail_on: set[str] | None = None) -> None:
        self.calls: list[str] = []
        self._fail_on = fail_on or set()

    def _rows(self, query: str, params: dict) -> list:
        self.calls.append(query)
        for fragment in self._fail_on:
            if fragment in query:
                raise RuntimeError(f"Simulated failure for: {fragment}")
        return []


class TestNeo4jMigration:
    def test_drop_returns_all_index_names(self):
        from app.services.neo4j_migration import drop_vector_indexes

        neo = _FakeNeo4j()
        dropped = drop_vector_indexes(neo)
        assert set(dropped) == {"entity_embedding", "community_embedding", "macro_community_embedding"}

    def test_drop_swallows_individual_failures(self):
        from app.services.neo4j_migration import drop_vector_indexes

        neo = _FakeNeo4j(fail_on={"DROP INDEX community_embedding IF EXISTS"})
        dropped = drop_vector_indexes(neo)
        # community_embedding failed silently; others should succeed
        assert "entity_embedding" in dropped
        assert "macro_community_embedding" in dropped
        assert "community_embedding" not in dropped

    def test_recreate_emits_three_statements(self):
        from app.services.neo4j_migration import recreate_vector_indexes

        neo = _FakeNeo4j()
        recreate_vector_indexes(neo, dims=1536)
        assert len(neo.calls) == 3
        assert all("CREATE VECTOR INDEX" in q for q in neo.calls)

    def test_recreate_uses_correct_dims(self):
        from app.services.neo4j_migration import recreate_vector_indexes

        neo = _FakeNeo4j()
        recreate_vector_indexes(neo, dims=1536)
        for query in neo.calls:
            assert "1536" in query

    def test_recreate_raises_on_failure(self):
        from app.services.neo4j_migration import recreate_vector_indexes

        neo = _FakeNeo4j(fail_on={"entity_embedding"})
        with pytest.raises(RuntimeError, match="Failed to recreate"):
            recreate_vector_indexes(neo, dims=768)

    def test_recreate_uses_config_dims_when_not_specified(self):
        from app.services.neo4j_migration import recreate_vector_indexes
        import app.services.neo4j_migration as mig_module

        neo = _FakeNeo4j()
        with patch.object(mig_module, "EMBEDDING_DIMS", 512):
            recreate_vector_indexes(neo)
        assert all("512" in q for q in neo.calls)
