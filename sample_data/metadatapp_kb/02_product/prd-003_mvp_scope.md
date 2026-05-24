---
doc_id: PRD-003
title: "MVP scope"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [MVP, HCM, ARRIVE]
tags: [mvp, scope]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- The MVP is focused on HCM and behavioral experiment metadata.
- Core modules: project workspace, experiment form, animal registry, cohort registry, cage metadata, procedure timeline, endpoint dictionary, validation report, and export builder.
- Acceptance criteria include completing a mock HCM study, generating validation output, and exporting JSON-LD.
- The first import path should be CSV because most clients can provide spreadsheets faster than API access.
- The MVP should avoid deep enterprise features until pilot needs are validated.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| MVP | targets | HCM metadata | high |
| CSV import | is | first import path | high |
| Enterprise features | come_after | pilot validation | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
