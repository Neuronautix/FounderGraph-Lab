---
doc_id: MTG-005
title: "Meeting - pricing review"
doc_type: meeting
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Pricing, Pilot]
tags: [meeting, pricing]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Discussion: academic pilot price should be accessible and grant-supported where possible.
- Discussion: CRO pilot can be priced higher if linked to report time saved.
- Discussion: enterprise pricing requires security, private deployment, and support commitments.
- Decision: use paid diagnostic or small paid pilot as qualification step.
- Decision: discount only in exchange for strong reference, reusable template, or case study.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Paid pilot | qualifies | serious prospect | medium |
| Discount | requires | reference or reusable asset | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
