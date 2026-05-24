---
doc_id: CLI-006
title: "Interview - animal facility manager"
doc_type: client_discussion
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Animal Facility, Facility Event]
tags: [client-discovery, facility]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Fictionalized discussion: facility events often explain variation in behavioral data.
- Cage changes, room moves, alarms, water interruptions, and light-cycle deviations matter.
- Researchers usually ask for context after analysis problems appear.
- Event categories are preferred over free text only.
- Reports should phrase facility events neutrally and avoid staff blame.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Facility Event | affects | behavioral data interpretation | high |
| Event categories | reduce | ambiguous free text | medium |
| HCM analysis | requires | facility context | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
