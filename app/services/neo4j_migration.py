"""Neo4j vector index migration helpers for backend switching.

When changing EXTRACTION_BACKEND from 'ollama' (768-d) to 'graphrag' (1536-d)
or vice versa, the Neo4j vector indexes must be dropped and recreated.
These helpers are called from the GraphRAG pipeline UI page (09_graphrag_pipeline).
"""
from __future__ import annotations

from typing import Any

from app.config import EMBEDDING_DIMS


# Map from Neo4j index name to the node label it covers.
# Update this dict if new vector indexes are added to cypher_constraints.cypher.
_VECTOR_INDEXES: dict[str, str] = {
    "entity_embedding": "Entity",
    "community_embedding": "Community",
    "macro_community_embedding": "MacroCommunity",
}


def drop_vector_indexes(neo4j: Any) -> list[str]:
    """Drop all known vector indexes.

    Iterates over :data:`_VECTOR_INDEXES` and issues ``DROP INDEX … IF EXISTS``
    for each one.  Failures for individual indexes are silently swallowed so
    that a missing index (e.g. ``macro_community_embedding`` on a fresh
    install) does not abort the migration.

    Parameters
    ----------
    neo4j:
        A :class:`~app.services.neo4j_service.Neo4jService`-shaped object
        that exposes ``_rows(query, params) -> list[dict]``.

    Returns
    -------
    list[str]
        Names of indexes that were successfully dropped.
    """
    dropped: list[str] = []
    for index_name in _VECTOR_INDEXES:
        try:
            neo4j._rows(f"DROP INDEX {index_name} IF EXISTS", {})
            dropped.append(index_name)
        except Exception:  # noqa: BLE001 — missing index is not an error
            pass
    return dropped


def recreate_vector_indexes(neo4j: Any, dims: int | None = None) -> None:
    """Recreate all vector indexes with the given embedding dimension.

    Reads :data:`~app.config.EMBEDDING_DIMS` from config if *dims* is not
    provided.  Uses ``IF NOT EXISTS`` guards so the function is idempotent;
    call :func:`drop_vector_indexes` first if you need to change the dimension
    of an existing index.

    Parameters
    ----------
    neo4j:
        A :class:`~app.services.neo4j_service.Neo4jService`-shaped object.
    dims:
        Embedding dimensionality.  Defaults to ``EMBEDDING_DIMS`` from config
        (768 for Ollama ``nomic-embed-text``, 1536 for OpenAI
        ``text-embedding-3-small``).

    Raises
    ------
    RuntimeError
        If any ``CREATE VECTOR INDEX`` statement fails.  Earlier statements
        that succeeded are not rolled back — Neo4j DDL is not transactional.
    """
    dims = dims or EMBEDDING_DIMS

    statements: list[str] = [
        (
            f"CREATE VECTOR INDEX entity_embedding IF NOT EXISTS "
            f"FOR (e:Entity) ON e.embedding "
            f"OPTIONS {{indexConfig: {{`vector.dimensions`: {dims}, "
            f"`vector.similarity_function`: 'cosine'}}}}"
        ),
        (
            f"CREATE VECTOR INDEX community_embedding IF NOT EXISTS "
            f"FOR (c:Community) ON c.embedding "
            f"OPTIONS {{indexConfig: {{`vector.dimensions`: {dims}, "
            f"`vector.similarity_function`: 'cosine'}}}}"
        ),
        (
            f"CREATE VECTOR INDEX macro_community_embedding IF NOT EXISTS "
            f"FOR (m:MacroCommunity) ON m.embedding "
            f"OPTIONS {{indexConfig: {{`vector.dimensions`: {dims}, "
            f"`vector.similarity_function`: 'cosine'}}}}"
        ),
    ]

    for stmt in statements:
        try:
            neo4j._rows(stmt, {})
        except Exception as exc:
            raise RuntimeError(
                f"Failed to recreate vector index: {exc}"
            ) from exc
