---
doc_id: TECH-009
title: "GCP Kubernetes deployment"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [GCP, Kubernetes, Docker]
tags: [deployment, gcp, kubernetes]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Containerized services include backend, frontend, worker, database, and validation service.
- Kubernetes manages deployment, ingress, services, secrets, scaling, and rollout.
- Object storage holds uploads, exports, validation artifacts, and RO-Crate bundles.
- Backups and restore drills are mandatory before real pilots.
- Validation workers should scale independently from the API.
- Secrets must not be embedded in configuration files.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Metadatapp | deploys_on | GCP Kubernetes | medium |
| Validation worker | scales_independently_from | API | medium |
| Backup | required_for | pilot readiness | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
