---
doc_id: KB-003
title: "Knowledge graph extraction guide"
doc_type: guide
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Document, Entity, Relationship]
tags: [knowledge-graph, extraction]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Each file should become a Document node with doc_id, title, doc_type, tags, status, and created_at properties.
- Each front-matter entity should become or link to an Entity node.
- Each row in the KG relationships table should become a directed edge with confidence as an edge property.
- Tags should become Topic nodes linked by has_topic.
- Folders should become DocumentCategory nodes.
- Do not treat fictionalized client notes as real contracts or real client evidence.
- Distinguish standards such as JSON-LD, SHACL, and RO-Crate from internal Metadatapp modules.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Markdown file | becomes | Document node | high |
| Relationship row | becomes | KG edge | high |
| Tag | becomes | Topic node | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
