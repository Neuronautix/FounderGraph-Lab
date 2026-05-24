---
doc_id: RES-003
title: "VCG scientific rationale"
doc_type: research
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [VCG, Historical Controls]
tags: [vcg, statistics]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- VCGs require historical or external control data that are sufficiently comparable to a new study.
- Metadata completeness is prerequisite because unknown protocol differences cannot be modeled reliably.
- Comparability must include animal characteristics, facility context, cage system, endpoint definitions, timing, interventions, and preprocessing.
- A readiness workflow can triage which datasets are worth statistical assessment.
- High completeness does not eliminate bias.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| VCG | requires | metadata completeness | high |
| Completeness score | does_not_eliminate | bias | high |
| Readiness workflow | triages | candidate datasets | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
