---
doc_id: COM-008
title: "Procurement and security questions"
doc_type: commercial
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Procurement, Security]
tags: [procurement, security]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Likely questions: where are data hosted, what data types are stored, how are permissions managed, and can the product run privately?
- Clients will ask about audit logs, backups, vulnerability handling, export rights, deletion policy, and contract termination.
- Prepared documents should include architecture diagram, RBAC policy, audit-log spec, backup procedure, and export/deletion policy.
- Security answers must be concrete before CRO or pharma pilots.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Procurement | asks_about | hosting and data ownership | high |
| Security questionnaire | requires | RBAC and backup documentation | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
