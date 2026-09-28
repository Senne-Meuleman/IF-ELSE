---
name: challenge-data
description: Quickly generate realistic fake Belgian data for the actual hackathon challenge by extending blocks/synth.py. Adds new tables (invoices, claims, contracts, CAO clauses, tickets, loan applications, job postings, salary bands…), new inbox message templates, or new documents for RAG, with deliberately planted edge cases the demo can "discover". Use when the brief needs data the kit doesn't have, when the user says "we need data for X", "generate fake …", "make test data", "add a table", or "the demo needs an example where …".
---

# Challenge data

Real data never arrives at a hackathon, so good synthetic data is what makes the demo look real. `blocks/synth.py` already generates employees, absences, payslips, customers, transactions and a multilingual inbox with Faker (`nl_BE`, `fr_BE`) and a seeded `rng`. Extend it and don't start a new generator.

First confirm that `blocks/synth.py` exists and inspect its current schema and seeding. This checkout may contain instructions only; if the kit is missing, report the prerequisite and prepare a data specification instead of assuming those APIs exist. Read AGENTS.md. Skill resources are relative to this SKILL.md; kit commands run from the repository root.

## Rules
1. **Keep existing rows stable.** Teammates, prompts, the demo script and the replay cache already reference IDs like `E1004`, `C5007` and `MSG003`. Use an independent `random.Random(SEED + n)` AND an independently seeded Faker instance (`seed_instance`); do not reseed shared Faker state. Register additions after existing generators. Compare old file hashes before/after (including untracked fixtures), generate twice to verify determinism, and validate unique IDs and foreign-key joins.
2. **Link to existing entities** by ID (`employee_id`, `customer_id`) so agents can join across tables.
3. **Plant the demo moments.** Deliberately include 3–5 rows that make the story work: the anomaly, the missing field, the rule violation, the angry NL/FR email. Mark them with a column like `flag` or `planted_case` and list them in the output so the presenter knows which ones to click.
4. **Belgian realism**: NL/FR names and text (and some EN), Belgian IBANs (`fake['nl_BE'].iban()`), VAT numbers `BE0xxx.xxx.xxx`, joint committees (PC 200…), regions Flanders/Wallonia/Brussels, and euro amounts in plausible ranges. For regulatory figures, use `/be-domain` facts or label them *illustrative* in a comment, as `payslip()` does.
5. **Small**: tens to a few thousand rows. It must regenerate in under 5 s and be readable in the 📊 Data tab.
6. Documents for RAG (policies, CAO excerpts, product terms, a fake internal procedure) go in `data/docs/` as `.md`. Mark fictional documents visibly as synthetic and not actual sponsor policy or law. Mix NL/FR/EN if the challenge is multilingual and put the evidence in specific paragraphs. Inspect the embedding backend and privacy boundary before running `uv run python -m blocks.build_index data/docs`.

## Common shapes
| Challenge | Table ideas | Planted cases |
|---|---|---|
| Peppol / invoices | `invoices.csv` (supplier VAT, PO number, lines, amount, due date, status) + `purchase_orders.csv` | amount mismatch with PO, duplicate invoice, wrong VAT number |
| Pay transparency | `salary_bands.csv`, gender and job level added to employees | unexplained gap above 5% in one job category |
| Payroll validation | `payroll_rules.csv` (derived from CAO text), `payroll_run.csv` | employee below the sector minimum, missing indexation |
| Insurance claims | `claims.csv` (policy, type, amount, description NL/FR, photos: none) | claim just after policy start, repeat claimant |
| Fraud / scams | more `SUSPICIOUS` patterns, `alerts.csv` with reason codes | new-payee large transfer at night, "helpdesk" scam text |
| Tickets / email | extend `inbox()` templates with the challenge's intents | ambiguous intent, two requests in one mail |

## Output
- The code added to `blocks/synth.py` (its own generator function and its own rng, registered at the end of `write_all`).
- Run `uv run python -m blocks.synth` and show the row counts.
- If the new table should be visible, add it to the table list in the 📊 Data tab of `app.py`. If agents should use it, write a docstringed tool function (see `get_employee` in `app.py`).
- List the planted cases with their IDs, and what the demo should reveal about each one.
