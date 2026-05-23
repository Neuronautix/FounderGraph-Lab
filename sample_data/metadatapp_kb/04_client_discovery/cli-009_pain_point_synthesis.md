---
doc_id: CLI-009
title: "Pain point synthesis"
doc_type: client_discovery
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Pain Points, ICP]
tags: [synthesis, pain-points]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Repeated pains include scattered metadata, manual report preparation, weak traceability, and difficulty comparing studies.
- CRO and pharma show stronger willingness to pay than academic users.
- Academic platforms provide credibility and rich scientific pilots.
- HCM vendors can become partners if integration is lightweight.
- The strongest universal message is not FAIR compliance but operational traceability and reuse readiness.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Client discovery | identifies | metadata fragmentation | high |
| CRO | has | strong willingness to pay | medium |
| Operational traceability | is | strong sales message | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
