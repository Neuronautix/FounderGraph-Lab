---
doc_id: STR-002
title: "Problem statement"
doc_type: strategy
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Preclinical Research, Metadata, Data Silos]
tags: [problem, market]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Preclinical experiments generate expensive data whose interpretation depends on protocol context.
- Protocol context is often fragmented across PDFs, spreadsheets, ELNs, LIMS, emails, animal facility systems, and instrument exports.
- HCM data are especially sensitive to missing context because continuous activity traces depend on cage, animal, environment, and event metadata.
- Poor metadata blocks reproducibility, reporting, AI readiness, historical reuse, and cross-study comparability.
- The core problem is not lack of data; it is lack of structured context attached to data.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Data silos | cause | metadata fragmentation | high |
| HCM data | requires | protocol context | high |
| Missing metadata | blocks | reproducibility and reuse | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
