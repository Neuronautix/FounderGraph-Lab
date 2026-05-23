---
doc_id: PRD-010
title: "UX principles"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [React Admin, MUI, Scientist UX]
tags: [ux, frontend]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Use progressive disclosure: simple workflow first, semantic detail second.
- Do not expose raw IRI paths as primary labels.
- Validation errors should include missing item, why it matters, severity, and suggested fix.
- Ontology suggestions should look like assisted autocomplete, not a semantic-web lesson.
- Export previews should show exactly what will be included in the package.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| UI | hides | semantic complexity | high |
| Validation UI | provides | actionable guidance | high |
| IRI paths | should_not_be | primary labels | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
