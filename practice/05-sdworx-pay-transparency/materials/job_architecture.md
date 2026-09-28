> SYNTHETIC: fictional company, fictional job architecture and pay ranges, written by team IF-ELSE for a practice drill. Not real SD Worx or client data. All amounts are illustrative.

# Vlaskaai Logistics NV: job architecture and pay ranges

Vlaskaai Logistics NV is a fictional contract-logistics company in Willebroek with
180 employees (warehouse, transport planning, customer service and support
functions). Payroll is run by SD Worx. Joint committee labels used internally:
PC 226 and PC 200. These are labels only for this drill: no sectoral pay scales
are supplied, and none should be assumed.

Snapshot date of `employees.csv`: **1 September 2026**.

## 1. How pay is set (internal policy, version 2019, last reviewed 2023)

- Every job belongs to one **job category**. A category groups jobs of the same
  work or work of equal value, based on four criteria: **skills**, **effort**,
  **responsibility** and **working conditions**.
- Every category has one or two **levels**. Each level has a monthly gross
  **pay range for a full-time job (1.0 FTE)**.
- New hires start near the bottom of the range. Pay then progresses with
  relevant experience at that level, reviewed once a year by the line manager
  and HR.
- Part-time employees are paid pro rata: a 0.8 FTE contract earns 80% of the
  full-time amount.
- Variable pay is annual and only exists for some categories (see table).
  It depends on team and company targets.
- Managers can propose a starting salary "within or near the range" when the
  labour market is tight. There is no written rule for "near".

## 2. Levels (generic)

| Level | Meaning |
|---|---|
| 1 | Executes defined tasks under close supervision. Short on-the-job training. |
| 2 | Executes tasks autonomously, handles standard exceptions. Vocational training or 1–2 years' experience. |
| 3 | Coordinates or plans the work of others, or owns a technical domain. 3–5 years' experience. |
| 4 | Specialist or account owner, works with external parties, bachelor or equivalent experience. |
| 5 | Leads a department, owns budget and people decisions. |

## 3. Job categories

Scores are 1 (low) to 5 (high) per criterion.

| Job category | Skills | Effort | Responsibility | Working conditions | Levels | Full-time monthly gross range (EUR) | Variable pay |
|---|---|---|---|---|---|---|---|
| Warehouse operator | 2 | 4 | 2 | 4 (cold store, shifts) | L1 / L2 | L1: 2,450–2,900 · L2: 2,750–3,250 | none |
| Forklift and reach-truck driver | 3 (certificate) | 3 | 2 | 4 (shifts) | L2 | 2,800–3,350 | none |
| Maintenance technician | 4 | 3 | 3 | 4 (on call) | L3 | 3,200–3,900 | none |
| Warehouse team lead | 3 | 3 | 4 (team of 8–12) | 4 (shifts) | L3 | 3,400–4,200 | team bonus, ~4% |
| Customer service agent | 3 (NL/FR/EN) | 2 | 2 | 2 | L2 | 2,700–3,300 | none |
| Administrative assistant | 3 | 2 | 2 | 1 | L2 | 2,650–3,200 | none |
| Transport planner | 4 | 3 | L2: 3 · L3: 4 | 3 (early shifts) | L2 / L3 | L2: 3,000–3,650 · L3: 3,500–4,300 | none |
| Finance and payroll officer | 4 | 2 | 3 | 1 | L3 | 3,300–4,200 | none |
| Account manager | 4 | 3 | 4 | 2 (travel) | L4 | 3,900–5,000 | commission, ~12% |
| Quality and safety coordinator | 4 (prevention advisor course) | 3 | 4 | 3 | L4 | 3,800–4,800 | target bonus, ~5% |
| IT and data specialist | 5 | 2 | 3 | 1 | L4 | 4,000–5,200 | target bonus, ~5% |
| Department manager | 4 | 3 | 5 | 2 | L5 | 5,000–6,500 | target bonus, ~15% |

### Level rules inside a category

- **Warehouse operator L1 → L2**: can work every zone (ambient, cold, returns)
  and trains new operators.
- **Transport planner L2 → L3**: at least 5 years of planning experience and
  independent ownership of a customer portfolio (planning, customer contact,
  escalation). Pay in L3 starts at the L3 minimum and progresses with years in L3.

### Job titles in use

Job titles are free text in the payroll system and were entered by different
managers over the years. The `job_category` column is the reference for
comparisons; the `job_title` column is what appears on the contract and payslip.

## 4. Data dictionary: `employees.csv`

| Column | Meaning |
|---|---|
| employee_id | Synthetic ID (SYN-xxxx) |
| first_name, last_name | Fictional names |
| gender | F, M or X (as registered by the employee) |
| job_title | Title on the contract and payslip (free text) |
| job_category | Category from the table above |
| level | 1 to 5 |
| department | Organisational unit |
| hire_date | Start date with Vlaskaai (ISO) |
| fte | Contract fraction, 1.0 = full-time |
| base_monthly_gross | Actual contractual monthly gross base pay in EUR on 1 Sept 2026, for the contract's FTE (part-time is already pro rata) |
| variable_pay_annual | Variable pay in EUR paid over the last 12 months |
| language | Preferred language for HR communication: NL, FR or EN |

Not included: pay history, benefits in kind, meal vouchers, overtime, holiday
pay, performance ratings.
