---
doc_id: TECH-012
title: "Performance considerations"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Asynchronous Job, Cache, Index]
tags: [performance]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Large CSV imports should not block API requests.
- Graph exports can become slow for studies with many animals and time windows.
- Ontology autocomplete should use cached term registries rather than live external calls when possible.
- Incremental validation can run during editing; full validation can run at export.
- Indexes are needed on organization, project, identifier, label, IRI, and foreign keys.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Large import | uses | asynchronous job | high |
| Ontology lookup | uses | cache | medium |
| Full validation | runs_at | export time | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
