---
doc_id: PRD-008
title: "VCG readiness module"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [VCG Readiness, Comparability Matrix, Biostatistician]
tags: [vcg, product]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- The VCG module should assess readiness for expert review, not automatically approve virtual controls.
- The module should score metadata completeness by animal, cage, environment, procedure, endpoint, dataset, and provenance dimensions.
- The module should generate a comparability matrix across candidate studies.
- Risk flags should identify non-overlapping protocols, endpoint definitions, time windows, or facility conditions.
- Recommendation labels should include not ready, curation needed, expert review needed, and candidate for statistical validation.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| VCG Readiness | requires | metadata completeness | high |
| VCG Readiness | requires | comparability matrix | high |
| Readiness score | is_not | statistical approval | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
