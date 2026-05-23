---
doc_id: PRD-009
title: "ARRIVE export"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [ARRIVE, Report Export]
tags: [ARRIVE, reporting]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- ARRIVE export should generate a draft reporting checklist from structured metadata.
- It should expose missing fields before manuscript or client report preparation.
- Mapped dimensions include study design, sample size, animal details, housing, procedures, outcome measures, and statistical methods.
- The export should distinguish captured, missing, not applicable, and requires review.
- The output should be human-readable but traceable back to structured metadata fields.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| ARRIVE export | uses | structured metadata | high |
| ARRIVE export | flags | missing reporting fields | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
