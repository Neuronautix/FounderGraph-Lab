---
doc_id: COM-010
title: "Statement of work template"
doc_type: commercial
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [SOW, Pilot]
tags: [sow, pilot]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Scope includes discovery workshop, metadata inventory, template configuration, import mapping, validation report, export package, training, and pilot evaluation.
- Out of scope includes raw statistical analysis, regulated GxP validation, full historical migration, custom connector beyond agreement, and automatic VCG approval.
- Deliverables include configured template, import mapping table, validation report, JSON-LD export, RO-Crate export, and pilot recommendation.
- SOW should protect against unpaid bespoke integrations.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| SOW | defines | pilot deliverables | high |
| SOW | excludes | automatic VCG approval | high |
| SOW | protects_against | unpaid bespoke integration | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
