# THEMIS — Scope

Step 0 of the implementation plan (PLAN.md §9). This is the anchor: every later
module must serve the decisions below. Change them deliberately, not by accident.

Decided: 2026-09-23
Status: locked for MVP 1

## Case study

Audit a mortgage-lending (HMDA-style) approval model for racial disparity that is
mediated by geography, and connect it to historical HOLC redlining.

## Decisions

| Dimension | Decision |
| --- | --- |
| Domain | Mortgage lending (HMDA schema) |
| Prediction target | Binary loan approval (`1` = approved, `0` = denied) |
| Sensitive attribute | Race / ethnicity |
| Geographic proxy | HOLC grade A–D → 2020 census tract (`redlining_score` 0–3), via `themis.holc` |
| MVP data | Small, documented synthetic loan dataset |
| Model under audit | Black box, accessed only through a `predict_proba` adapter |
| First output | Markdown technical report |

## What success looks like (MVP 1)

1. Audit a model without access to its weights or training code.
2. Join modern loan rows to HOLC grades by census `GEOID`.
3. Quantify disparity (approval rate by race; demographic parity difference) and
   proxy association (predictions ↔ `redlining_score`).
4. Produce a traceable Markdown report.

## Non-goals for MVP 1

- Training models from scratch.
- Causal claims about redlining causing individual outcomes.
- Real HMDA data (later milestone).
- XAI, agents, and mitigation (later MVPs per the plan).
