---
doc_id: KB-000
title: "README - Metadatapp synthetic knowledge base"
doc_type: readme
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Metadatapp, Knowledge Graph]
tags: [overview, mock-knowledge-base]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- This archive contains a synthetic knowledge base inspired by Metadatapp: a FAIR-by-design metadata platform for preclinical animal research.
- The corpus is designed for graph construction, RAG evaluation, ontology extraction, strategic mapping, and mock startup due diligence.
- All client discussions, CRM notes, pricing notes, meeting notes, and financial assumptions are fictionalized mock material.
- The corpus separates established standards from plausible strategy and fictional operational notes.
- Files are deliberately small and structured so that each document can become a Document node connected to entities, topics, decisions, and risks.
- Recommended extraction order: manifest, entity registry, node registry, edge registry, Markdown front matter, relationship tables, then free-text bullets.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Metadatapp | is_a | FAIR metadata platform concept | high |
| Corpus | supports | mock knowledge graph generation | high |
| Client discussions | are | fictionalized synthetic notes | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
