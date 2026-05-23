---
doc_id: TECH-002
title: "Domain model"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Project, Study, Experiment, Animal, Cage, Endpoint, Dataset]
tags: [data-model]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Organization owns projects, users, templates, permissions, and deployment settings.
- Project groups related studies or client work.
- Study defines scientific objectives and design.
- Experiment captures operational execution: animals, cages, procedures, events, endpoints, and datasets.
- Animal has species, strain, sex, age, genotype, source, identifier, and health status.
- Cage has system type, cage ID, density, enrichment, bedding, room, rack, and HCM hardware.
- Endpoint has label, unit, method, sampling frequency, and semantic mapping.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Experiment | has_part | Animal | high |
| Cage | houses | Animal | high |
| Dataset | measures | Endpoint | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
