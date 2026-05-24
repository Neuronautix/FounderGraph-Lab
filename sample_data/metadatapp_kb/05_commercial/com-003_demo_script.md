---
doc_id: COM-003
title: "Demo script"
doc_type: commercial
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Demo, HCM Study, Validation Report]
tags: [demo, sales]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Open with a messy HCM study: protocol PDF, animal spreadsheet, HCM activity export, and email notes.
- Show the problem: no trusted map between animals, cages, treatments, endpoints, and events.
- Import animal and cage metadata.
- Resolve validation errors for sex, strain, cage density, light cycle, and endpoint units.
- Generate FAIR validation report, JSON-LD export, RO-Crate, and ARRIVE draft.
- End with VCG-readiness dashboard showing remaining gaps.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Demo | uses | messy HCM study | high |
| Validation report | shows | missing metadata | high |
| Demo | ends_with | VCG readiness gaps | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
