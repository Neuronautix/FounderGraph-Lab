---
doc_id: DEC-002
title: "Decision log - AI boundaries"
doc_type: decision
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [AI Assistant, Validation]
tags: [decision, ai]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Decision: AI features remain proposal-only.
- Decision: no AI-suggested field becomes validated without source evidence or human review.
- Decision: validation reports separate deterministic errors from AI suggestions.
- Rationale: scientific metadata must be auditable.
- Rationale: trust is a stronger differentiator than automation claims.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| AI feature | is | proposal-only | high |
| Validated metadata | requires | source evidence or human review | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
