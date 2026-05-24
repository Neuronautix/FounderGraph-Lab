---
doc_id: KG-001
title: "Competency questions"
doc_type: knowledge_graph
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Knowledge Graph, SPARQL]
tags: [kg, competency-questions]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Which experiments used a given strain, cage system, endpoint, and light cycle?
- Which studies are missing metadata required for ARRIVE reporting?
- Which datasets are linked to procedures performed within a specific time window?
- Which HCM sessions are comparable across facility sites?
- Which metadata fields were proposed by AI and later accepted by a human reviewer?
- Which studies are candidates for VCG-readiness review?
- Which connectors contributed metadata to a given experiment?
- Which ontology mappings changed between two export versions?

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Knowledge Graph | answers | comparability and provenance questions | high |
| Competency Question | guides | ontology and SHACL design | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
