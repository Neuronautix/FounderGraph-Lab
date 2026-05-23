---
doc_id: TECH-010
title: "Testing strategy"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Unit Test, Integration Test, Golden File, SHACL Test]
tags: [testing, quality]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Unit tests cover validators, parsers, mapping functions, and export builders.
- API integration tests cover permissions, CRUD, imports, exports, and validation jobs.
- Golden-file tests protect JSON-LD and RO-Crate export stability.
- SHACL tests require known valid and invalid metadata graphs.
- Connector tests require fixture files and expected validation reports.
- End-to-end tests cover study creation, validation, export, and re-import.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| JSON-LD export | requires | golden-file tests | high |
| SHACL shapes | require | valid and invalid fixtures | high |
| Connector | requires | contract tests | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
