> SEALED: organizer only. Agents: do not read this file while building a drill.

# Drill 05 – Pay transparency, before the law lands – organizer notes

All numbers below were computed from `materials/employees.csv` (180 rows, seed 11).
Gap = (mean men − mean women) / mean men, on monthly base pay normalised to
1.0 FTE, unless stated otherwise. The 2 employees registered as X are left out of
the binary F/M comparison (they stay in the data).

## Format & timing

Announced to the team as a **2-hour build** (see the 2 h column in
`practice/README.md`). The real pitch happens at **T+1:15** because of the curveball.

| Time | What happens |
|---|---|
| T+0:00 | Hand out `BRIEF.md` and `materials/`. Start the clock. Answer questions as the SD Worx mentor. |
| T+0:10 | Expect a pick from `/brainstorm`. |
| T+0:18 | Expect `PLAN.md` from `/kickoff`. |
| T+0:30 | First AI call working? Note the time. |
| **T+0:45** | **Curveball** (below). |
| T+0:55 | Expect a re-scoped `PLAN.md`. |
| T+1:00 | Expect feature freeze. |
| T+1:15 | Pitch, 3 minutes, live. Then 5 minutes of jury questions, then `judge`. |
| T+1:30 | 15-minute debrief (template in `practice/README.md`). |

## Planted cases

| ID / category | What's hidden | Actual computed numbers | What a strong demo shows |
|---|---|---|---|
| **P1 · Warehouse team lead** (14: 6 F, 8 M, all full-time, all level 3) | Unexplained gender gap. Women are paid ~9% less at equal seniority. | Mean F EUR 3,368 vs M EUR 3,741: **10.0% raw** (median 10.5%, total pay incl. variable 10.0%). Seniority: F 7.8 y, M 8.6 y. **Seniority-adjusted gap 9.2%** (OLS on log pay). 4 of the 6 women (SYN-1102, 1164, 1170, 1173) are **below the range minimum** of EUR 3,400; no man is. Cost to lift each woman to the men's pay line at her seniority: ~EUR 2,020/month, **~EUR 24,300/year base gross** (before employer contributions). | Flags this category ≥ 5% after adjustment, shows the women below the range floor, proposes a correction for a human to approve, and links it to Eva's request (REQ-2026-031). |
| **P2 · Transport planner** (16: 7 F, 9 M, levels 2/3) | Raw gap that disappears with seniority. Women were hired later, so fewer reached level 3 (rule: 5+ years). | Mean F EUR 3,318 vs M EUR 3,567: **7.0% raw**, median **11.4%**. Seniority F 4.6 y, M 7.9 y. Level 3: 3 of 7 F, 7 of 9 M. **Adjusted for seniority: −0.8%**, for seniority + level: **+0.1%**. | Shows the raw 7% and then the explanation by an objective criterion, and does NOT flag it for correction. Answers Nathalie (REQ-2026-033) with the level 3 criteria, not with a pay number alone. |
| **P3 · Quality and safety coordinator** (3: 2 F, 1 M) | Small cell. Averages by sex disclose individual pay. | Man (SYN-1055): EUR 4,065. Women: EUR 3,945 and EUR 4,200, mean EUR 4,072.50. Gap −0.2%. Publishing "men's average" = Tom Stevens' exact salary. Laetitia (EUR 4,200, REQ-2026-032) can then work out Veerle's EUR 3,945 from the women's average. | Detects the small group, does not show raw averages, explains why, and routes it to a human (for example: answer with the pay range and criteria, or a wider comparison group, decided by HR). Same issue hits Administrative assistant (1 M), Maintenance technician (1 F) and IT and data specialist (1 F). |
| **P4 · Gendered job titles** | Job-title neutrality (Art. 5). | "Magazijnier" (13 rows, all M) next to "Warehouse operator (m/f/x)" (56). "Secretaresse" (4 F) and "Secrétaire de direction" (1 F) in Administrative assistant. "Heftruckchauffeur" (6, all M) next to "Forklift driver (m/f/x)". | Lists the titles and suggests neutral ones, as a side finding. Bonus if the team uses `job_category`, not `job_title`, as the comparison unit. |
| **P5 · Part-time, Customer service agent** (14: 10 F, 4 M; 6 women part-time) | Monthly pay must be FTE-normalised. | Raw monthly: F EUR 2,396 vs M EUR 2,924, **18.0% gap**. Per FTE: F EUR 2,934 vs M EUR 2,924, **−0.4%**. Nadia (SYN-1074, 0.8 FTE, EUR 2,285) vs Wim De Smet (EUR 3,050): the "EUR 750" in REQ-2026-034 is almost all FTE. | Normalises before comparing and explains it to Nadia in plain English, and points her to the internal scale (Art. 6 criteria). |
| Org-wide | Headline trap. | Raw monthly gap **8.6%**, FTE-normalised **4.0%**, median FTE 2.4%. | Does not stop at "4%, we're fine": the org average hides P1. |
| Decoy · Maintenance technician (8: 1 F, 7 M) | Naive over-flag. | Gap **14.0%**, but the one woman has 3.0 years vs 13.6 for the men, and it is a single person. | Does not report "14% gap" as a finding. |
| Decoy · Account manager (8: 3 F, 5 M) | Borderline raw gap. | Mean 4.3%, median 5.1%, seniority-adjusted −3.8%. | Not flagged. |

All other categories are below 5% on the FTE mean (warehouse operator 2.0%,
forklift −2.6%, finance 3.2%, IT 2.9%, managers 1.8%, admin −4.6%).

## Curveball

At **T+0:45**, walk in and say exactly:

> "Quick update from the jury: they're running early. Pitches start in 30 minutes, not 75. Same 3 minutes."

Do not negotiate. If asked "is this real?", say "yes, plan for it". The pitch is at
T+1:15. This trains the "re-scope / we're behind" path of `/kickoff`.

## Traps

- **Stating the directive is already Belgian law**, or quoting Belgian implementing
  rules, fines or a Belgian law number. There is none: Belgium missed the 7 June 2026
  deadline and asked for six more months (⚠️ still being legislated). Eva's email
  ("werknemers hebben nu het recht") invites this mistake.
- **Using or asking for pay history.** Art. 5 bans asking applicants about it; the
  data has no such column on purpose. Watch for "we'll add previous salary as a
  feature".
- **Small-cell disclosure** (P3 and the three 1-person groups).
- **Sending individual salary rows to a cloud LLM** when the statistics can be
  computed locally in pandas and only aggregates (or nothing) need the model.
- **Letting the AI decide raises.** AI Act Annex III (high-risk) covers employment
  uses such as decisions on promotion and evaluating workers, which is where a
  "who gets a raise" tool lands. The deadline moved to 2 Dec 2027 ⚠️ under the
  AI Digital Omnibus, but the human still decides. Look for an Approve/Reject in code.
- **Ignoring FTE** (P5, and the org-wide 8.6% vs 4.0%).
- **Comparing raw means only**: over-flags P2 and the maintenance decoy, and the
  mean alone hides the median for planners.
- **A chart without an action**: a gap bar chart that ends at "interesting".
- Smaller ones: dropping or exposing the 2 X employees; comparing by `job_title`
  instead of `job_category`; forgetting the 2-month answer deadline.

## What a strong result looks like

- **Persona:** the HR manager of a 180-person SME, alone, with four requests in
  three languages, or the SD Worx payroll consultant who serves 40 such clients.
- **Painful moment:** Eva's email lands. HR does not know if the answer will show a
  problem, or how to explain it without breaking someone's privacy.
- **Demo path (3–4 clicks):** load data → category table with raw vs FTE vs
  adjusted gap, only P1 red → open Eva's request → drafted NL reply with the
  right averages and a suppressed small-cell case → HR approves.
- **Number idea:** "1 of 12 categories needs action; closing it costs ~EUR 24k a
  year in base pay. Fixing it now, not after the June 2027 report." Any euro
  figure must be traceable to the data or labelled illustrative.
- **Trust story:** stats computed locally, only aggregates reach the model, small
  groups suppressed, law status stated with its uncertainty, a human signs every
  reply and every raise.
- **Sponsor fit:** fits SD Worx's model where humans supervise AI agents
  (launched 24 June 2026), as a service the consultant runs for many clients.

## Jury questions

1. **"Is this legally required in Belgium today?"** Good answer: not yet transposed
   (deadline 7 June 2026 missed, 6-month extension asked), but the directive sets
   the content and the first report on 2026 data is due 7 June 2027 for 150+
   employees. The tool follows the directive and will adapt to the Belgian text.
2. **"Your tool says women earn 7% less in transport planning. Do we have to fix
   it?"** Good answer: no, it is explained by seniority and the level 3 rule
   (adjusted ~0%). The 5% trigger is for gaps not justified by objective,
   gender-neutral criteria. Bonus: check that the level rule itself is applied
   neutrally.
3. **"What happens when Laetitia asks her question?"** Good answer: one man in the
   group, so the average is his salary; the tool suppresses it and flags it for HR
   to choose a safe answer. It does not invent a legal threshold for group size.
4. **"Where does the salary data go?"** Good answer: a precise, true description of
   the code: which step runs locally, what is sent to the model (aggregates, no
   names), and what is masked. Vague "it's GDPR compliant" is a weak answer.
5. **"Who decides the raise for the team leads?"** Good answer: HR and management,
   with workers' representatives if it reaches a joint pay assessment. The tool
   proposes and explains; a human approves. Mentions AI Act Annex III (⚠️ date moved
   to Dec 2027) without over-claiming.

## Skills to watch

| Skill | What to observe | Debrief question |
|---|---|---|
| `/brainstorm` | Does it push toward one user and one moment, or a "pay transparency platform"? | Did the pick fit in 75 minutes? |
| `/kickoff` | At T+0:45: does "re-scope" redo only the demo scope and split, cut hard, and keep the demo path first? Time from curveball to new `PLAN.md`. | Did the re-scope take under 10 minutes? What did it keep that it should have cut? |
| `/be-domain` | Are the ⚠️ caveats said out loud (Belgian status, AI Act date)? Any invented Belgian rule, fine or small-cell threshold? | Which claim in the pitch was not in facts.md? |
| `/challenge-data` | Data is given: does the team waste time regenerating it? | Did anyone generate data they did not need? |
| `/demo-step` | Seeded input, visible result, Approve/Reject before a reply is "sent". | Is the approval enforced in code? |
| `/privacy-check` | Do salaries with names reach the cloud model? Is the privacy claim as true as the code? | Would the check have caught it before the pitch? |
| `/impact-calc` | Is the EUR number traceable (P1 ~EUR 24k/year) or invented? | Were the assumptions stated on the slide? |
| `/pitch-rehearsal` | Does rehearsal still happen after the cut? Were the jury questions above predicted? | How many of the 5 did it predict? |

Note which skill output was wrong or slow, and turn it into an edit in
`.claude/skills/` the same evening.
