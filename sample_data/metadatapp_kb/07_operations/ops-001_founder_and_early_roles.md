---
doc_id: OPS-001
title: "Founder and early roles"
doc_type: operations
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Founder, CTO, Advisor]
tags: [team, roles]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Scientific founder owns domain vision, client discovery, product positioning, and HCM use-case credibility.
- Technical lead or CTO owns architecture, security, deployment, code quality, and engineering process.
- Product/data engineer owns import/export workflows, validation reports, and frontend flows.
- Semantic-web contributor owns JSON-LD contexts, ontology mappings, SHACL shapes, and RO-Crate exports.
- Commercial advisor tests pricing, buyer journey, procurement, and CRO/pharma access.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Scientific Founder | owns | domain vision | high |
| CTO | owns | technical execution | high |
| Semantic Web Contributor | supports | JSON-LD and SHACL | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
