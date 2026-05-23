---
doc_id: MTG-002
title: "Meeting - semantic architecture"
doc_type: meeting
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [JSON-LD, SHACL, Ontology]
tags: [meeting, semantics]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Decision: use JSON-LD export generated from canonical internal entities.
- Decision: build SHACL shapes around competency questions.
- Decision: version ontology mappings.
- Decision: hide raw RDF complexity from primary UI.
- Risk: ontology work can slow MVP delivery if not scoped.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| JSON-LD export | derived_from | canonical internal entities | high |
| SHACL shapes | based_on | competency questions | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
