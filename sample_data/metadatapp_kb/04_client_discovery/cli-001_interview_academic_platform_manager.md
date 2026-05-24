---
doc_id: CLI-001
title: "Interview - academic platform manager"
doc_type: client_discussion
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Academic Platform, Platform Manager]
tags: [client-discovery, academic]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Fictionalized interview: university preclinical behavior platform receives heterogeneous study requests.
- Current metadata arrive through email, Word documents, and spreadsheets.
- The platform manager wants standardized intake before experiments start.
- Incomplete strain, housing, and timeline details create delays.
- ARRIVE export is attractive if it reduces publication-support workload.
- Budget is limited, but templates and training are valued.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Academic Platform | needs | standardized intake | high |
| Incomplete metadata | causes | delays | medium |
| ARRIVE export | adds_value_for | platform manager | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
