---
doc_id: RES-001
title: "HCM use case rationale"
doc_type: research
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [HCM, DVC-like Data, Behavior]
tags: [hcm, research]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- HCM is a strong wedge because it generates dense longitudinal data that are expensive and biologically rich.
- The value of HCM outputs depends on cage type, animal identity, group composition, light cycle, enrichment, facility events, and protocol timeline.
- HCM can support welfare monitoring, circadian phenotyping, activity endpoints, recovery trajectories, and digital biomarker exploration.
- Without standardized metadata, cross-study comparison is fragile.
- Metadatapp can link HCM sessions, cage metadata, animal metadata, endpoints, events, and export packages.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| HCM | requires | cage and protocol context | high |
| Metadatapp | links | HCM endpoints to metadata | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
