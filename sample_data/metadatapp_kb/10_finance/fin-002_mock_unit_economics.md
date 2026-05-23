---
doc_id: FIN-002
title: "Mock unit economics"
doc_type: finance
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [CAC, Gross Margin, Pilot]
tags: [unit-economics]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Customer acquisition cost includes founder time, conference outreach, discovery calls, and pilot preparation.
- Pilot delivery cost includes configuration, data mapping, training, support, and report generation.
- Cloud cost includes hosting, storage, validation jobs, and backups.
- Support cost includes onboarding, bug fixes, template adjustments, and connector maintenance.
- Bespoke connector work must be priced carefully because it can destroy margin.
- Low-price pilots are acceptable only if they create reusable assets or reference evidence.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Pilot | can_produce | reusable assets | medium |
| Bespoke connector work | threatens | gross margin | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
