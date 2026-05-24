---
doc_id: TECH-007
title: "Connector architecture"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [CSV Connector, ELN, LIMS, HCM]
tags: [connectors]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- CSV connector is the first practical integration path.
- REST connectors synchronize resources from systems exposing APIs.
- File-drop connectors monitor SFTP or object storage exports.
- Vendor-specific connectors handle idiosyncratic export formats and authentication.
- All connectors map source fields to canonical internal entities before export.
- Each connector import creates a mapping version and validation report.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Connector | maps | source fields to canonical entities | high |
| CSV Connector | is | first connector | high |
| Connector import | creates | validation report | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
