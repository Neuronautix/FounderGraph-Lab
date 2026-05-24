---
doc_id: TECH-006
title: "Ontology layer"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Ontology Registry, MBO, HCM Ontology]
tags: [ontology, semantics]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- The ontology layer links local metadata labels to stable concepts.
- The first ontology priority is HCM behavior, cage-system metadata, endpoint definitions, and facility events.
- Ontology mappings should record IRI, label, synonym, source, version, status, and review notes.
- AI-suggested mappings require human review.
- Local aliases are acceptable if canonical export mappings are defined.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Ontology layer | links | local labels to stable concepts | high |
| AI mapping | requires | human review | high |
| HCM ontology | supports | behavior metadata | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
