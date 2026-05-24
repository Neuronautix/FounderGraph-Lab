---
doc_id: COM-005
title: "Pricing tiers"
doc_type: commercial
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Academic Tier, CRO Tier, Enterprise Tier]
tags: [pricing]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Academic Starter: lower annual fee, limited users, standard templates, community-oriented support.
- Professional CRO: higher annual subscription, more users, client-report exports, connector support, onboarding package.
- Enterprise Pharma: private deployment, SSO, custom connectors, support SLA, governance workshops.
- Services: ontology mapping, FAIR audit, historical data curation, custom templates, and training.
- Pricing values should remain assumptions until tested through pilots and procurement conversations.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Academic Tier | targets | platform credibility | medium |
| Enterprise Tier | requires | private deployment and SLA | medium |
| Service add-on | provides | early revenue | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
