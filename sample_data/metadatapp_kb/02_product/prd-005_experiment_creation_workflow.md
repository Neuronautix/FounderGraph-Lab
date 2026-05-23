---
doc_id: PRD-005
title: "Experiment creation workflow"
doc_type: product
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [Experiment, Animal, Cage, Endpoint]
tags: [workflow, ux]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Step 1: create project and choose study type.
- Step 2: select metadata template such as generic preclinical, HCM, pharmacology, or behavioral battery.
- Step 3: enter animal cohort metadata including species, strain, sex, age, genotype, source, and housing.
- Step 4: define protocol timeline with baseline, intervention, procedures, endpoint windows, and follow-up.
- Step 5: attach facility events such as cage change, transfer, surgery, alarm, dosing, or light-cycle deviation.
- Step 6: map endpoint names to controlled vocabulary terms and units.
- Step 7: run validation and export metadata package.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| Experiment workflow | creates | validated metadata package | high |
| Facility event | contextualizes | HCM data | high |
| Endpoint mapping | links_to | controlled vocabulary | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
