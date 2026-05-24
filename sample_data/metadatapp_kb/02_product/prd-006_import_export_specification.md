---
doc_id: PRD-006
title: "Import export specification"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [CSV, JSON, JSON-LD, RO-Crate]
tags: [import-export, interoperability]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- CSV import supports legacy spreadsheets and platform curation templates.
- JSON import supports application exchange and connector payloads.
- JSON-LD export supports linked-data interoperability.
- RO-Crate export packages metadata, files, provenance, and manifest.
- ARRIVE export produces a human-readable reporting checklist draft.
- Unknown imported fields should be quarantined rather than silently discarded.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| CSV import | supports | legacy metadata migration | high |
| JSON-LD export | supports | linked data interoperability | high |
| Unknown fields | should_be | quarantined | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
