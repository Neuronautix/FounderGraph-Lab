---
doc_id: FIN-004
title: "Grant budget notes"
doc_type: finance
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Grant Budget]
tags: [grant, budget]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Mock grant budget includes backend audit, semantic support, UX design, cloud credits, legal review, pilot training, and conference demo material.
- Budget should map each item to a deliverable.
- Funding narrative should emphasize reusable research infrastructure rather than generic software development.
- Grant spending should reduce technical, semantic, and commercial uncertainty.
- The budget should avoid vague consulting lines without measurable outputs.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Grant budget | contains | technical audit semantic support UX cloud legal | medium |
| Budget item | maps_to | deliverable | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
