---
doc_id: TECH-001
title: "System architecture"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Symfony, API Platform, React Admin, PostgreSQL, Kubernetes]
tags: [architecture]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Backend uses Symfony and API Platform for REST, GraphQL, JSON-LD/Hydra resources, validation, and API documentation.
- Frontend uses React Admin and Material UI for structured CRUD and scientific workflows.
- Database uses PostgreSQL for transactional metadata storage.
- Semantic layer generates JSON-LD, RDF-compatible exports, and SHACL validation reports.
- Workers handle imports, exports, validation jobs, and connector synchronization.
- Deployment can use Docker and Kubernetes on Google Cloud for beta and enterprise paths.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Backend | uses | Symfony API Platform | high |
| Frontend | uses | React Admin and MUI | high |
| Deployment | can_use | GCP Kubernetes | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
