---
doc_id: CLI-007
title: "Interview - biostatistician"
doc_type: client_discussion
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Biostatistician, VCG, Comparability]
tags: [client-discovery, statistics]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Fictionalized interview: biostatistician supports historical control reuse but insists on rigor.
- Metadata completeness is necessary but not sufficient for VCG reuse.
- Comparability requires endpoint alignment, time-window alignment, protocol alignment, and batch-effect analysis.
- The system should expose why a study is not comparable.
- A readiness score must not be interpreted as statistical approval.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Metadata completeness | is_necessary_not_sufficient_for | VCG reuse | high |
| Comparability matrix | supports | expert review | high |
| Readiness score | is_not | statistical approval | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
