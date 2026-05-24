---
doc_id: RES-005
title: "ARRIVE mapping notes"
doc_type: research
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [ARRIVE, Metadata Schema]
tags: [ARRIVE, mapping]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- ARRIVE study design maps to study design type and experiment group allocation.
- Sample size maps to cohort animal counts and sample-size rationale.
- Inclusion/exclusion maps to experiment criteria.
- Animal details map to species, strain, sex, age, genotype, and source.
- Housing and husbandry map to cage, environment, facility event, bedding, and enrichment.
- Experimental procedures map to procedure and timeline entities.
- Outcome measures map to endpoint and dataset entities.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| ARRIVE | maps_to | Metadatapp schema | high |
| Housing and husbandry | map_to | Cage and Environment | high |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
