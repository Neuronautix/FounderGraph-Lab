---
doc_id: COM-001
title: "Ideal customer profile"
doc_type: commercial
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [ICP, CRO, Academic Platform, Pharma]
tags: [icp, sales]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Best-fit customers run repeated preclinical animal studies with heterogeneous data sources.
- They use HCM, behavioral testing, physiology, or multi-modal endpoints.
- They experience reporting, traceability, reuse, or AI-readiness pressure.
- They have a scientific lead, data steward, platform manager, or innovation champion.
- Poor-fit customers expect magic AI cleanup without governance or staff involvement.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Best-fit ICP | runs | repeated heterogeneous preclinical studies | high |
| Poor-fit customer | expects | magic AI cleanup | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
