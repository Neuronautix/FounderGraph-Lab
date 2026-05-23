---
doc_id: TECH-005
title: "SHACL validation strategy"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [SHACL, Validation Report, RDF]
tags: [shacl, validation]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Application validation checks types, required fields, permissions, and relational integrity.
- Schema validation checks file structure, expected columns, and allowed values.
- Semantic validation checks RDF shapes, class-property consistency, and identifier requirements.
- Business validation checks pilot-specific completeness rules.
- Example shape: Animal must have species, strain, sex, and identifier.
- Example shape: Endpoint must have label, unit, method, and biological interpretation note.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| SHACL | validates | semantic metadata graph | high |
| Animal | requires | species strain sex identifier | high |
| Endpoint | requires | unit and method | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
