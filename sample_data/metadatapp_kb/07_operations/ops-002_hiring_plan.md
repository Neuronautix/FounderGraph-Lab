---
doc_id: OPS-002
title: "Hiring plan"
doc_type: operations
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [CTO, Developer, Intern]
tags: [hiring]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Priority one: part-time senior engineer or CTO with API Platform, React, deployment, testing, and product judgment.
- Priority two: full-stack developer for frontend polish, import/export, and admin workflows.
- Priority three: semantic web intern or consultant for ontology mapping and validation shapes.
- Candidate test: build a small JSON-LD export with tests.
- Candidate test: implement CSV import with validation report.
- Candidate test: explain how to avoid ontology-driven technical debt.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Hiring priority | is | technical execution | high |
| Candidate test | includes | JSON-LD export with tests | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
