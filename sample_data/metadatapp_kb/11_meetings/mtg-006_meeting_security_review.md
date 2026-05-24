---
doc_id: MTG-006
title: "Meeting - security review"
doc_type: meeting
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Security, RBAC]
tags: [meeting, security]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Decision: document data categories before pilots.
- Decision: implement audit log for critical metadata changes.
- Decision: separate edit permission and export permission.
- Decision: prepare private deployment story for sensitive clients.
- Open issue: timing of SSO for enterprise pilots.
- Open issue: formal vulnerability disclosure process.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Export permission | separate_from | edit permission | medium |
| Audit log | required_for | critical metadata changes | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
