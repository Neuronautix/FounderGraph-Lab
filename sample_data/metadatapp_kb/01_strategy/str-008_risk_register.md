---
doc_id: STR-008
title: "Risk register"
doc_type: strategy
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Scope Creep, Adoption Risk, Validation Risk]
tags: [risk, governance]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Scope creep is a major risk if the platform tries to cover all preclinical domains too early.
- Adoption risk is high if scientists perceive metadata capture as extra administrative work.
- Validation risk is high if VCG language overclaims what metadata can prove.
- Integration risk is high because client systems differ and procurement can delay API access.
- Mitigation requires a narrow HCM wedge, import templates, validation reports, and pilot metrics.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Scope creep | threatens | MVP delivery | high |
| VCG overclaiming | threatens | scientific credibility | high |
| Import templates | mitigate | adoption risk | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
