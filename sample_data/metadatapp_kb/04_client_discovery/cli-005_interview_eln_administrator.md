---
doc_id: CLI-005
title: "Interview - ELN administrator"
doc_type: client_discussion
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [ELN, Data Steward]
tags: [client-discovery, eln]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Fictionalized interview: ELN stores protocols and notes but lacks structured animal-experiment metadata.
- The administrator opposes duplicate data entry.
- Integration should pull from ELN or push structured summaries back.
- Authentication and permission mapping matter for institutional adoption.
- Protocol extraction can help but should remain proposal-only.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| ELN Admin | opposes | duplicate data entry | high |
| Metadatapp | should_integrate_with | ELN | high |
| Protocol extraction | is | proposal-only | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
