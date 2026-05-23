---
doc_id: CLI-003
title: "Interview - pharma translational group"
doc_type: client_discussion
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Pharma, Historical Controls, VCG]
tags: [client-discovery, pharma]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Fictionalized discussion: translational group has archived studies but inconsistent metadata.
- Historical control reuse is valuable only if comparability is defensible.
- The group wants dashboards showing metadata completeness across old studies.
- They are skeptical of unsupported AI automation claims.
- First pilot should use non-sensitive archived or synthetic data.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Pharma Group | values | historical data reuse | medium |
| VCG use | requires | defensible comparability | high |
| Pilot | uses | non-sensitive data | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
