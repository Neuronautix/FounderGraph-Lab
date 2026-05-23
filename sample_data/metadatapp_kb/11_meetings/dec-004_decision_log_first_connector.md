---
doc_id: DEC-004
title: "Decision log - first connector"
doc_type: decision
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [CSV Connector, Vendor API]
tags: [decision, connector]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Decision: build CSV import and mapping workflow before vendor-specific API connectors.
- Rationale: most clients can export spreadsheets faster than API access can be approved.
- Rationale: CSV validates the core mapping and validation logic.
- Consequence: connector abstractions should still support future vendor APIs.
- Consequence: user mapping interface becomes strategically important.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| First connector | is | CSV import mapping workflow | high |
| Vendor API connector | comes_after | pilot validation | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
