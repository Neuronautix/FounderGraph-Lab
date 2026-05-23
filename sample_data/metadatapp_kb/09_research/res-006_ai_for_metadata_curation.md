---
doc_id: RES-006
title: "AI for metadata curation"
doc_type: research
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [LLM, Metadata Curation]
tags: [ai, curation]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- AI can extract candidate metadata from protocol documents.
- AI can suggest controlled vocabulary mappings.
- AI can detect inconsistencies between protocol text and structured fields.
- AI can summarize missing metadata in plain language.
- AI can generate draft report text from validated metadata.
- AI is an accelerator for curation, not an authority.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| AI | accelerates | metadata curation | medium |
| AI-derived field | requires | provenance and review | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
