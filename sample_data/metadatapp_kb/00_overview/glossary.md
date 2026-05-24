---
doc_id: KB-001
title: "Glossary"
doc_type: glossary
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [FAIR, FAIRRR, ARRIVE, JSON-LD, SHACL, RO-Crate, HCM]
tags: [glossary, semantics]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- FAIR means Findable, Accessible, Interoperable, and Reusable.
- FAIRRR means FAIR for the Animals, and for Innovative, Reproducible, and Responsible Research.
- HCM means Home Cage Monitoring: automated measurement of animal activity and welfare-related signals in the home cage.
- ARRIVE refers to reporting guidelines for animal research.
- JSON-LD is a JSON serialization for linked data.
- SHACL validates RDF graphs against explicit shapes and constraints.
- RO-Crate packages research data, metadata, provenance, and contextual files.
- VCG means Virtual Control Group and should be treated as a statistical reuse concept requiring comparability evidence.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| FAIRRR | extends | FAIR toward animal welfare and responsible research | high |
| SHACL | validates | RDF graphs | high |
| RO-Crate | packages | research objects | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
