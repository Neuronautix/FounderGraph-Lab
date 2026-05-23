---
doc_id: DEC-003
title: "Decision log - VCG language"
doc_type: decision
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [VCG, Marketing]
tags: [decision, vcg]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Decision: use VCG readiness rather than VCG generation in early commercial language.
- Decision: state that metadata quality is necessary but not sufficient.
- Decision: require biostatistical review before historical-control validity claims.
- Rationale: overclaiming could damage credibility.
- Rationale: readiness is more defensible than automatic generation.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| VCG language | uses | readiness not automatic generation | high |
| Biostatistical review | required_for | validity claims | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
