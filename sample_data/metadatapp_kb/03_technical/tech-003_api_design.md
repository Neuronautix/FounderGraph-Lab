---
doc_id: TECH-003
title: "API design"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [REST, GraphQL, JSON-LD]
tags: [api]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Core endpoints include projects, studies, experiments, animals, cohorts, cages, procedures, events, endpoints, datasets, validation reports, exports, ontology terms, and connectors.
- Each resource should have a stable internal UUID.
- Each semantic resource should expose an optional IRI and human-readable label.
- REST should support integration and CRUD workflows.
- GraphQL should support dashboards and flexible query views.
- Bulk imports should create asynchronous jobs and validation reports.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| API resource | has | stable UUID | high |
| Bulk import | creates | asynchronous validation job | high |
| GraphQL | supports | dashboard queries | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
