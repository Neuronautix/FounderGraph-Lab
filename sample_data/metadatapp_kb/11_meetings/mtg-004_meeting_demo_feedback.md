---
doc_id: MTG-004
title: "Meeting - demo feedback"
doc_type: meeting
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Demo, Feedback]
tags: [meeting, demo]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Positive: users understood missing-context map quickly.
- Positive: validation report was clearer than raw FAIR terminology.
- Positive: ARRIVE export was perceived as practical.
- Negative: too many ontology labels were visible.
- Action: hide ontology identifiers by default.
- Action: create HCM import template and endpoint tooltips.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Demo feedback | supports | validation report value | high |
| Ontology identifier | should_be | hidden by default | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
