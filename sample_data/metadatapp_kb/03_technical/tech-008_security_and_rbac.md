---
doc_id: TECH-008
title: "Security and RBAC"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [RBAC, Audit Log, Private Deployment]
tags: [security, rbac]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Roles include owner, admin, scientist, data steward, viewer, and external client.
- Export permission should be separated from edit permission.
- Audit log should record critical metadata changes.
- Private deployment should be available for sensitive enterprise clients.
- Data retention and deletion policies should be explicit.
- Security documentation is required before CRO or pharma procurement.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| RBAC | controls | metadata editing and export | high |
| Audit log | records | critical changes | high |
| Private deployment | supports | enterprise clients | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
