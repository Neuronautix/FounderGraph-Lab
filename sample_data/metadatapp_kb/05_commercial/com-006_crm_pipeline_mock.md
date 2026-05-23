---
doc_id: COM-006
title: "CRM pipeline mock"
doc_type: commercial
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [CRM, Prospect]
tags: [crm, sales]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Pipeline stages: lead identified, discovery scheduled, problem confirmed, sample received, diagnostic delivered, pilot proposed, procurement review, pilot active, expansion, closed.
- Mock academic prospect is interested in intake standardization and ARRIVE export.
- Mock CRO prospect is interested in traceability and client reporting.
- Mock pharma prospect is interested in historical-control readiness.
- Mock vendor prospect is interested in connector partnership.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| CRM pipeline | tracks | pilot conversion | high |
| Diagnostic delivered | precedes | pilot proposal | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
