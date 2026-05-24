---
doc_id: MTG-001
title: "Meeting - product scope"
doc_type: meeting
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [MVP, Scope]
tags: [meeting, product]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Decision: keep MVP focused on HCM and behavioral experiment metadata.
- Decision: postpone general preclinical coverage until after pilots.
- Decision: prioritize validation reports and exports over advanced dashboards.
- Open question: which HCM export format should be supported first?
- Open question: should initial UI target platform managers or individual scientists?

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| MVP | focuses_on | HCM metadata | high |
| Advanced dashboard | postponed_until | after validation exports | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
