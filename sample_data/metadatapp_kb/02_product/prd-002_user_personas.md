---
doc_id: PRD-002
title: "User personas"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [PI, Platform Manager, Data Steward, CRO Scientist]
tags: [personas, ux]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- The PI wants defensible reuse and publication-quality reporting without administrative overload.
- The platform manager wants standardized study intake and fewer incomplete requests.
- The data steward wants stable identifiers, validation reports, and machine-readable exports.
- The CRO scientist wants traceable client reporting across repeated studies.
- The biostatistician wants comparability evidence before historical control reuse.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Platform Manager | needs | standardized intake | high |
| Data Steward | needs | machine-readable exports | high |
| Biostatistician | requires | comparability evidence | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
