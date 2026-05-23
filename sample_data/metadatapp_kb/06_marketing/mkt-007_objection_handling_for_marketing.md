---
doc_id: MKT-007
title: "Objection handling for marketing"
doc_type: marketing
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Objection, Marketing]
tags: [objections]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- If a prospect says the topic is too technical, respond with workflow examples and concrete outputs.
- If a prospect says they already document protocols, ask whether the documentation is machine-readable, validated, exportable, and reusable.
- If a prospect says FAIR is only for publication, explain internal reuse, audit, client reporting, and AI-readiness.
- If a prospect says ontologies are too heavy, explain that users see labels while the system manages identifiers.
- If a prospect says virtual controls are risky, agree and position Metadatapp as readiness and comparability infrastructure.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Objection handling | emphasizes | practical workflow outputs | high |
| Protocol documentation | may_lack | machine-readable structure | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
