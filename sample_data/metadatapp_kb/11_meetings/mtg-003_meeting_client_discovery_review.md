---
doc_id: MTG-003
title: "Meeting - client discovery review"
doc_type: meeting
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [ICP, Pilot]
tags: [meeting, client-discovery]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Finding: academic users validate the scientific problem but have limited budgets.
- Finding: CRO users respond to time saving and traceability more than FAIR terminology.
- Finding: pharma users are interested in historical reuse but cautious about governance.
- Decision: lead sales messaging with operational pain.
- Decision: use FAIR and ontology as proof of durability after pain is established.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Sales messaging | leads_with | operational pain | high |
| FAIR terminology | supports | credibility | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
