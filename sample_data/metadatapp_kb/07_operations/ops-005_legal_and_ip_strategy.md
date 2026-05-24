---
doc_id: OPS-005
title: "Legal and IP strategy"
doc_type: operations
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [AGPL, Commercial License, Open Source]
tags: [legal, opensource]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Permissive licensing maximizes adoption but weakens commercial control.
- AGPL open-core protects server-side improvements but may deter some companies.
- Dual license can support community use under AGPL and commercial use under separate terms.
- Proprietary connectors and enterprise modules can remain commercial.
- Contracts and licensing should be reviewed legally before external contributions or client pilots.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Dual license | supports | community and commercial use | medium |
| Proprietary connectors | can_be | premium modules | medium |
| Legal review | required_for | contracts and licensing | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
