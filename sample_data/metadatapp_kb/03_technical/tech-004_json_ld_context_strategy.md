---
doc_id: TECH-004
title: "JSON-LD context strategy"
doc_type: technical
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [JSON-LD, Context, Ontology]
tags: [json-ld, semantics]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Start with a compact internal context for Metadatapp entities.
- Map common properties to established vocabularies where appropriate.
- Use local terms for domain-specific HCM concepts when external vocabulary coverage is weak.
- Version contexts to preserve compatibility of exported studies.
- Avoid pretending JSON-LD alone guarantees interoperability; mappings and validation matter.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| JSON-LD context | maps | application fields to semantic terms | high |
| Context versioning | preserves | export compatibility | medium |
| JSON-LD | does_not_guarantee | interoperability | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
