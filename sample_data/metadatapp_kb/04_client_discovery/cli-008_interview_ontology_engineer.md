---
doc_id: CLI-008
title: "Interview - ontology engineer"
doc_type: client_discussion
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Ontology Engineer, SHACL, JSON-LD]
tags: [client-discovery, ontology]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Fictionalized technical discovery call: ontology engineer warns against superficial linked-data claims.
- JSON-LD export alone does not guarantee interoperability.
- Mappings must be versioned, justified, and tested.
- SHACL shapes should reflect real competency questions.
- Users need labels and definitions; machines need identifiers and constraints.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| JSON-LD | does_not_guarantee | interoperability | high |
| SHACL shapes | reflect | competency questions | high |
| Ontology mapping | requires | versioning | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
