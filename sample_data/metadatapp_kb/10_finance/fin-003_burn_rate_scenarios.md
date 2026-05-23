---
doc_id: FIN-003
title: "Burn-rate scenarios"
doc_type: finance
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Burn Rate, Runway]
tags: [burn, runway]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Lean scenario: founder-led commercial work, part-time technical lead, semantic intern, minimal cloud, service-led pilots.
- Growth scenario: full-time technical lead, full-stack developer, UX support, staging/production infrastructure, paid pilots or funding.
- Hiring before product-market evidence can consume runway.
- Underinvesting in technical quality can block enterprise adoption.
- The correct path depends on pilot conversion speed and available non-dilutive funding.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Lean scenario | uses | part-time technical lead | medium |
| Growth scenario | requires | paid pilots or funding | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
