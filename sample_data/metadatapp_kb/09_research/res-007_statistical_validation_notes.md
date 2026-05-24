---
doc_id: RES-007
title: "Statistical validation notes"
doc_type: research
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [VCG, Batch Effects, Comparability]
tags: [statistics, validation]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Define the target estimand before selecting historical controls.
- Assess endpoint alignment and preprocessing consistency.
- Model site, batch, cage, strain, sex, age, and time-window effects where relevant.
- Use sensitivity analyses to test robustness to control selection.
- Compare prospective controls and virtual controls before claiming replacement potential.
- Prespecify exclusion criteria and comparability thresholds.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Statistical validation | requires | target estimand and comparability criteria | high |
| Missing metadata | limits | credible statistical adjustment | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
