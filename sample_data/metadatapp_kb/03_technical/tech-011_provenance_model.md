---
doc_id: TECH-011
title: "Provenance model"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Provenance, Source Document, Review Status]
tags: [provenance, audit]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Every metadata field should record source type, source identifier, creator, timestamp, confidence, review status, and validation report ID.
- Source types include manual, CSV import, API connector, AI proposal, protocol document, and system-generated.
- Imported values should preserve raw value and normalized value.
- AI-proposed values should not be treated as validated facts before review.
- Critical deleted values should remain in audit history.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Metadata value | has | provenance fields | high |
| AI proposal | requires | review before validation | high |
| Imported value | retains | raw and normalized value | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
