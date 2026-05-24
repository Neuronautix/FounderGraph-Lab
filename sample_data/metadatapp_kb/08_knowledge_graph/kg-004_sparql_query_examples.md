---
doc_id: KG-004
title: "SPARQL query examples"
doc_type: knowledge_graph
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [SPARQL, Query]
tags: [kg, sparql]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Find documents mentioning both VCG and HCM.
- List high-confidence edges with predicate requires.
- Find client discovery documents linked to procurement risk.
- Find product modules linked to export formats.
- Find technical risks linked to mitigation strategies.
- Find all documents where AI is proposal-only.
- Find all dependencies of the MVP.
- Find all pilot success metrics connected to commercial documents.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| SPARQL | queries | mock KG relationships | medium |
| KG schema | determines | exact syntax | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
