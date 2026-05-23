---
doc_id: PRD-001
title: "Product requirements document"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Experiment Registry, Validation Report, RO-Crate]
tags: [prd, product]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- The MVP should let users create structured projects, studies, experiments, animals, cages, procedures, events, endpoints, and datasets.
- The user should be able to import CSV metadata, resolve validation errors, and export structured packages.
- The product must generate a validation report explaining missing fields, inconsistent values, provenance gaps, and export readiness.
- The MVP should support JSON, CSV, JSON-LD, ARRIVE-style reporting, and RO-Crate package generation.
- The MVP excludes raw video tracking, full statistical modeling, and automatic VCG approval.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| MVP | includes | experiment metadata registry | high |
| MVP | exports | JSON-LD and RO-Crate | high |
| MVP | excludes | raw video tracking | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
