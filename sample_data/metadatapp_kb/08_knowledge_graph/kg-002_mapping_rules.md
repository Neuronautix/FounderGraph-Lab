---
doc_id: KG-002
title: "Mapping rules"
doc_type: knowledge_graph
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Document, Node, Edge]
tags: [kg, mapping]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Each Markdown front-matter entity becomes a candidate node.
- Each relationship table row becomes a directed edge.
- Each doc_id becomes a Document node.
- Tags become Topic nodes.
- Folder name becomes document_category.
- Fictional client names become FictionalOrganization nodes.
- Do not infer real contracts from synthetic meeting notes.
- Normalize aliases but preserve technology labels exactly.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Front matter entity | becomes | candidate node | high |
| Relationship row | becomes | directed edge | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
