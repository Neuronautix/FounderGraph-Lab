---
doc_id: RES-004
title: "HCM metadata schema sketch"
doc_type: research
status: synthetic_mock
created_at: 2026-05-20
project: Metadatapp
entities: [HCM Schema, Animal, Cage, Endpoint]
tags: [schema, hcm]
kg_focus: "entity extraction, relationship extraction, decision extraction, risk extraction"
---

## Purpose

- This file is part of a synthetic but realistic Metadatapp knowledge base for a mock knowledge-graph experiment.
- It is point-ended by design: short claims, explicit entities, explicit relations, and open questions are easier to extract into a graph.
- Client and partner situations are fictionalized unless described as standards, technologies, or general market concepts.

## Key points

- Study metadata: objective, design, site, start/end dates, protocol version.
- Animal metadata: species, strain, sex, age, genotype, source, health status.
- Cage metadata: cage ID, system type, density, bedding, enrichment, location, sensor hardware.
- Environment metadata: light cycle, temperature, humidity, noise, alarm, and room events.
- HCM session metadata: acquisition window, sampling frequency, endpoint definitions, preprocessing rules.
- Dataset metadata: file name, source system, export date, checksum, unit, and time zone.
- Provenance metadata: source, editor, validation status, mapping version.

## KG relationships

| subject | predicate | object | confidence |
|---|---|---|---|
| HCM metadata schema | includes | animal cage environment protocol endpoint provenance | high |
| Dataset | requires | source system and checksum | medium |

## Open questions

- Which claims require external validation before investor or client use?
- Which entities should become canonical nodes in the knowledge graph?
- Which relationships are factual, inferred, fictional, or strategic assumptions?
