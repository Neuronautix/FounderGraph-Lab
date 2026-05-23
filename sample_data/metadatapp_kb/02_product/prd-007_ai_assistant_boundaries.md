---
doc_id: PRD-007
title: "AI assistant boundaries"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [LLM, Human Review, Validation]
tags: [ai, validation]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- AI can suggest mappings from free text to controlled vocabulary terms.
- AI can summarize validation errors in plain language.
- AI can generate draft ARRIVE-style text from validated metadata.
- AI must not silently fill missing metadata as fact.
- AI output is proposal-only until deterministic validation, provenance, and human review accept it.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| AI output | is | proposal-only | high |
| Human review | accepts_or_rejects | AI suggestion | high |
| Validation | precedes | FAIR claims | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
