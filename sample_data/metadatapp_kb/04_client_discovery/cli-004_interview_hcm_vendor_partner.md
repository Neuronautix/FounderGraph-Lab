---
doc_id: CLI-004
title: "Interview - HCM vendor partner"
doc_type: client_discussion
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [HCM Vendor, Connector]
tags: [client-discovery, partner]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Fictionalized discussion: HCM vendor exports activity metrics but not all protocol context.
- Customers ask how to compare studies across sites.
- Vendor is interested in integration if support burden stays low.
- A co-marketed FAIR HCM metadata demo could be attractive after technical validation.
- The integration should be complementary: vendor keeps analytics; Metadatapp adds context.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| HCM Vendor | provides | activity metrics | high |
| Metadatapp | adds | protocol context | high |
| Vendor partnership | starts_with | lightweight connector | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
