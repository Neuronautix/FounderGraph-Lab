---
doc_id: KG-003
title: "Example triples"
doc_type: knowledge_graph
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [RDF, Triple]
tags: [kg, triples]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Metadatapp -- has_initial_wedge --> Home Cage Monitoring.
- Home Cage Monitoring -- requires --> Protocol Context.
- Validation Report -- identifies --> Missing Metadata.
- RO-Crate Export -- packages --> Research Object.
- AI Suggestion -- requires --> Human Review.
- VCG Readiness -- requires --> Comparability Matrix.
- CRO Pilot -- measures --> Report Assembly Time.
- Ontology Mapping -- has_property --> Version.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Metadatapp | has_initial_wedge | Home Cage Monitoring | high |
| AI Suggestion | requires | Human Review | high |
| VCG Readiness | requires | Comparability Matrix | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
