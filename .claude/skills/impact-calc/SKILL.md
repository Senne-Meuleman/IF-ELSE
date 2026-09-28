---
name: impact-calc
description: Build a credible, defensible business-impact number (euros saved, hours freed, errors or fraud avoided, payback) for a hackathon idea, with every assumption explicit and sourced or flagged. Use whenever the team needs "the number" for the pitch, an ROI or business case, a "why this matters" slide, an impact metric to show in the Streamlit app, or when a judge might ask "how much does this save?". Also trigger on "business value", "impact", "ROI", "how big is this problem".
argument-hint: "[short description of the solution]"
---

# Impact calc

Judges at a sponsor hackathon (KBC, SD Worx) score **business value**, so a pitch needs one headline number the room remembers and that holds up to a finance person asking "where does that come from?".

## Method
1. **Name the unit of work** the solution touches: one email triaged, one payslip question answered, one invoice reconciled, one fraud alert explained, one leave request processed.
2. **Volume**: how many per year? Prefer the sponsor's own public figures (for example SD Worx payslips per month, KBC Kate conversations). Get them from `/be-domain` facts or the `researcher` agent. Otherwise estimate from first principles and label it an estimate.
3. **Before**: minutes per unit today × fully loaded cost per hour. Belgian defaults, all labelled *assumption*:
   - back-office / HR admin / customer-service FTE: **€45–55 per hour** fully loaded
   - specialist (payroll expert, fraud analyst, legal): **€65–90 per hour**
   - 1 FTE ≈ **1,600 productive hours per year**
4. **After**: automation rate (the share handled end to end) and the minutes left for human review. Be conservative: 50–70% automation with a human in the loop is more credible than 95%.
5. **Second-order value**, stated qualitatively or with a clearly marked range: errors avoided (payroll corrections, fines), fraud losses prevented, faster answers (NPS), compliance (Pay Transparency, Peppol, AI Act).
6. **Sanity check**: if the number is larger than the plausible budget of the department, halve your assumptions. Round hard: "≈ €2.4M / year", never "€2,413,907".

## Output
1. A small assumptions table: `Assumption | Value | Source or "estimate"`.
2. The calculation in 3–5 lines.
3. **One headline sentence for the pitch**, for example: *"For a 1,000-person client that's 3,100 HR hours a year, about 2 FTE freed for real people-work."* Offer a conservative and an optimistic version, and recommend using the conservative one.
4. Optionally, a Python snippet or `st.metric` row for `app.py` so the number appears in the demo, computed from the demo's own counters (for example "12 emails triaged in 40 s ≈ 36 min saved").
5. The 2 hardest questions a judge could ask about the number, with one-line answers.

Never present an estimate as a sponsor figure. If a fact about Belgian regulation or the sponsor is used, it must come from `/be-domain` or a cited source.
