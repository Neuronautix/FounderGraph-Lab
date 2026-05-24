---
doc_id: RES-008
title: "Mock HCM study protocol summary"
doc_type: research
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Mock Study, HCM]
tags: [mock-study, protocol]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Title: Baseline circadian activity in C57BL/6J mice using home cage monitoring.
- Objective: quantify night/day activity ratio and recovery after cage-change event.
- Animals: 24 C57BL/6J mice, balanced sex, 10-12 weeks old.
- Housing: group-housed, four mice per cage, enriched environment.
- Recording: continuous HCM activity index, seven baseline days, three post-cage-change days.
- Endpoints: total activity, night/day ratio, fragmentation index, and post-event recovery slope.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Mock HCM Study | measures | night/day activity ratio | high |
| Cage-change event | affects | post-event recovery endpoint | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
