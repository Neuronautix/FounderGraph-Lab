---
doc_id: KG-005
title: "Graph schema notes"
doc_type: knowledge_graph
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Node, Edge, Property]
tags: [kg, schema]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Suggested node labels: Document, ProductModule, Stakeholder, Technology, Standard, Risk, Decision, UseCase, Pilot, Metric, ExportFormat, Connector, OntologyTerm.
- Suggested edge labels: requires, supports, enables, integrates_with, validates, exports, measures, mitigates, competes_with, targets, produces, depends_on, has_risk, has_metric.
- Use confidence as an edge property.
- Use status to distinguish synthetic notes from standards or validated decisions.
- Document provenance should remain explicit in the graph.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Graph schema | includes | Document and ProductModule nodes | high |
| Edge labels | include | requires supports validates exports | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
