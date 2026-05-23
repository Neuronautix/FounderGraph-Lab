---
doc_id: CLI-010
title: "Client objections"
doc_type: client_discovery
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Client, Sales]
tags: [objections, sales]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Objection: we already have an ELN. Response: Metadatapp is a structured metadata and interoperability layer, not an ELN replacement.
- Objection: scientists will not fill more forms. Response: use templates, imports, autocomplete, and downstream time saved.
- Objection: FAIR is too abstract. Response: show validation reports, ARRIVE drafts, and curation time metrics.
- Objection: AI can do this automatically. Response: AI can propose; validation and provenance make it trustworthy.
- Objection: cloud is impossible. Response: provide private deployment or de-identified pilot options.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| ELN objection | answered_by | complementary metadata layer | high |
| AI objection | answered_by | validation-first architecture | high |
| Cloud objection | answered_by | private deployment option | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
