# Materials – "From CAO to payroll check" (practice drill 03)

> ⚠️ **SYNTHETIC.** Everything here was made up by team IF-ELSE for a practice drill.
> The joint committee "PC 399.07", its agreements, the client "Brabo Cold Logistics NV"
> and all employees are fictional. No real person, CAO or company data.

## Files

| File | What it is |
|---|---|
| `docs/cao_01_loonschalen_nl.md` | Agreement (NL): minimum wage scales per category A–D and seniority step, effective 1 July 2026. |
| `docs/cct_02_prime_cheques_repas_fr.md` | Agreement (FR): end-of-year bonus and meal vouchers. |
| `docs/cao_03_nachtarbeid_flexi_nl-fr.md` | Agreement (NL/FR bilingual): night-work premium and the sector's flexi-job opt-out. |
| `payroll_run_2026-10.csv` | The October 2026 payroll run of one client under PC 399.07: 40 employees. |

Each agreement has numbered articles (`Artikel` / `Article`) and paragraphs (`§`),
so a rule can cite e.g. "CAO 399.07/2026/014, art. 3 §1".

## `payroll_run_2026-10.csv` columns

| Column | Meaning |
|---|---|
| `employee_id` | Client payroll ID |
| `name` | Employee name (fictional) |
| `category` | Function category A–D |
| `hire_date` | Date of entry with this employer (ISO) |
| `seniority_years` | Full years of service on 1 Oct 2026 |
| `regime` | `FT` full-time or `PT` part-time |
| `weekly_hours` | Contractual hours per week (full-time = 38) |
| `gross_monthly` | Basic gross monthly wage paid in October 2026 (EUR) |
| `legacy_allowance` | Personal transitional allowance (EUR/month), if any |
| `meal_voucher_days` | Meal vouchers granted this month |
| `meal_voucher_employer_share` | Employer share per voucher (EUR) |
| `night_hours` | Night hours worked in October 2026 |
| `night_premium_paid` | Night premium paid this month (EUR) |
| `contract_type` | `permanent`, `fixed_term` or `flexi` |

Amounts use a dot as decimal separator. The payroll month is October 2026.
