---
doc_id: FIN-001
title: "Financial assumptions"
doc_type: finance
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Revenue, Costs]
tags: [finance, assumptions]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Early revenue is expected to come from pilots, consulting, and implementation support.
- Recurring revenue grows only after templates and connectors become repeatable.
- Cloud costs are modest during MVP but rise with storage, validation jobs, backups, and private deployments.
- The most important early cost is senior technical execution.
- Academic sales cycles may be easier to access but lower in contract value.
- CRO and pharma contracts may be higher value but slower due to procurement and security review.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Early revenue | comes_from | pilots and services | medium |
| Recurring revenue | depends_on | repeatable templates and connectors | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
