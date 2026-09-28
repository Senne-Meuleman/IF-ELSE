---
name: challenge-data
description: Generate realistic fake Belgian data for the actual hackathon challenge - seeded, deterministic, with deliberately planted edge cases the demo can "discover". Tables (employees, payslips, invoices, claims, transactions, tickets, salary bands, CAO clauses…), multilingual inbox messages, and documents for RAG. Use when the brief needs data the app doesn't have, or the user says "we need data for X", "generate fake …", "make test data", "add a table", "the demo needs an example where …".
---

# Challenge data

Real data never arrives at a hackathon, so good synthetic data is what makes
the demo look real. One seeded generator (`data/synth.py`, pattern in the
`scaffold` skill's snippets: Faker `nl_BE` + `fr_BE`, `random.Random(SEED)`)
writes CSV/JSON into `data/synthetic/`. Extend it; don't start a second one.

## Rules
1. **Keep existing rows stable.** Teammates, prompts, `DEMO_SCRIPT.md` and the replay cache reference IDs like `E1004`, `C5007`, `MSG003`. Give every new generator its own `random.Random(SEED + n)` and its own `Faker` instance with `seed_instance()`, registered **after** existing generators. Regenerate twice and diff: identical output or it's a bug.
2. **Link to existing entities** by ID (`employee_id`, `customer_id`) so agent tools can join across tables.
3. **Plant the demo moments.** 3–5 rows that make the story work: the anomaly, the missing field, the rule violation, the angry FR email, the two-requests-in-one mail. Mark them in a `flag` column and list them in the output so the presenter knows which ones to click.
4. **Belgian realism**: NL/FR names and text (and some EN), IBANs from `fake["nl_BE"].iban()`, VAT numbers `BE0xxx.xxx.xxx`, joint committees (PC 200, 124, 302), regions Flanders/Wallonia/Brussels, euro amounts in plausible ranges, dates around today. Regulatory figures come from `/be-domain` or are labeled *illustrative* in a comment.
5. **Small**: tens to a few thousand rows, regenerates in under 5 s, readable in a data tab.
6. **Documents for RAG** (policies, CAO excerpts, product terms, an internal procedure) go in `data/docs/` as `.md`, visibly marked *synthetic, not actual sponsor policy or law*, with the evidence in specific paragraphs. Mix NL/FR/EN if the challenge is multilingual.

## Common shapes
| Challenge | Table ideas | Planted cases |
|---|---|---|
| Peppol / invoices | `invoices.csv` (supplier VAT, PO number, lines, amount, due date, status) + `purchase_orders.csv` | amount mismatch with PO, duplicate invoice, wrong VAT number |
| Pay transparency | `salary_bands.csv`; gender and job level added to employees | unexplained gap above 5% in one job category |
| Payroll validation | `payroll_rules.csv` (derived from CAO text), `payroll_run.csv` | employee below the sector minimum, missing indexation |
| Insurance claims | `claims.csv` (policy, type, amount, description NL/FR) | claim just after policy start, repeat claimant |
| Fraud / scams | `transactions.csv` with `flag`, `alerts.csv` with reason codes | new-payee large transfer at night, "bank helpdesk" scam text, itsme phishing |
| Tickets / email | `inbox.json` templates per intent, NL/FR/EN | ambiguous intent, two requests in one mail, an instruction hidden in the mail |
| Employee self-service | `employees.csv`, `absences.csv`, `payslips.csv` | leave balance exhausted, 4/5 request, "net pay lower" after indexation |

## Output
- The generator code (own function, own rng, registered at the end of `write_all`).
- Run it and show the row counts.
- If the table should be visible, add it to the data tab. If an agent should use it, write a docstringed tool function (see `/demo-step`).
- The planted cases with their IDs and what the demo should reveal about each one.
