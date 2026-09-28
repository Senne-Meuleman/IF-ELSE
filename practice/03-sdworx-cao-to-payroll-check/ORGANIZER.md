> SEALED: organizer only. Agents: do not read this file while building a drill.

# Drill 03 – SD Worx – "From CAO to payroll check" – organizer notes

All content is synthetic. PC 399.07, Brabo Cold Logistics NV, the agreements and
every employee are fictional. Scale amounts, the 20% night premium and the 2%
addendum are illustrative. The meal-voucher amounts (EUR 10 face value, EUR 8.91
employer, EUR 1.09 employee, max since 1 Jan 2026, needs a CAO) and the flexi-job
opening on 1 Jul 2026 with sector opt-out by CAO come from `be-domain/references/facts.md`.

## Format & timing

- **Full 4 h**, time-box as in `practice/README.md`.
- T+0:00: hand out `BRIEF.pdf` only (not this file). The team must work from the
  PDF: that is the point. Watch whether their agents actually read it.
- T+0:00 to T+2:00: you are the SD Worx mentor. Answer questions briefly, in
  character. Do not confirm or deny any planted case. Allowed answers:
  - "Is PC 399.07 real?" → "No, treat it as a stand-in for any sector."
  - "What reference date for seniority?" → "Look at the README and art. 5."
  - "Should we check the end-of-year bonus?" → "Is it due in October?"
  - "Can we send the CSV to Gemini?" → "What does the consultant need to send?"
- **T+2:00: drop the curveball** (below).
- T+3:00 feature freeze. T+3:45 submission. Pitch 3 min + 2 min questions.
- After the pitch: run `judge`, ask the jury questions, fill the score sheet.

## Planted cases

Payroll month: October 2026. Seniority = full years on 1 Oct 2026 (the CSV
already has it). Full-time = 38 h. Part-time minimum = scale × hours / 38.
Night premium = 20% × gross_monthly / (weekly_hours × 52/12) × night_hours.

| ID | Employee | What's hidden | What a strong demo shows |
|---|---|---|---|
| P1 UNDER-1 | BCL-1224 (B, 3 y, FT) | Paid 2,410.00, minimum B step 2 = 2,450.00. Gap EUR 40/month. | Flag with citation CAO 399.07/2026/014 art. 3 §1, the expected amount and the gap. |
| P2 UNDER-2 | BCL-1273 (A, hired 2021-06-14, 5 y) | Paid 2,210.00 = exactly the step-2 amount. Should be step 5 = 2,290.00 since 1 Jul 2026. Missed seniority step. | Explanation says "seniority step not applied" (art. 3 §1 + art. 5 §1), not just "below minimum". |
| P3 UNDER-3 | BCL-1119 (C, hired 2014, 12 y) | Pre-2020 with legacy allowance 90.00. Base 2,950 + 90 = 3,040 < 3,090. Clause applies but does not save them. Gap EUR 50. | Shows the transitional rule was evaluated (art. 6 §2) and still fails. |
| P4 PROTECT | BCL-1147 (D, hired 2012, 14 y) | Base 3,480 < 3,610, but base + legacy allowance 260 = 3,740 ≥ 3,610. Protected by art. 6 §2. **Must NOT be flagged.** | Listed as "OK – transitional clause, art. 6 §2" or not listed; a strong team shows it as a near-miss it deliberately did not flag. |
| P5 MEAL | BCL-1084, BCL-1091, BCL-1126, BCL-1140 | Employer share still 6.91 (the pre-1 Oct amount) in the October run. Should be 8.91. EUR 2.00 × 85 vouchers = EUR 170. | One finding per employee (or one grouped finding) citing CCT 399.07/2026/015 art. 3 §3–§4, in French source, explained in English. |
| P6 NIGHT | BCL-1280 (A, FT, 32 night hours) | Night premium 0.00. Expected 20% × 2,395 / 164.67 × 32 = EUR 93.09. | Flag with the computed amount and art. 3 §1–§2 of 399.07/2026/016. The other 6 night workers are paid correctly (to the cent). |
| P7 FLEXI | BCL-1196 (A, hired 2026-08-17, 12 h, `flexi`) | Flexi-job contract after the sector opt-out (art. 4 §2, from 1 Jul 2026). Pay itself is fine pro rata. | Flag as a contract issue, not a pay issue: "reclassify the contract", with the opt-out cited. |
| P8 PART-TIME | BCL-1098 (19 h), BCL-1133 (30.4 h), BCL-1077 (22.8 h) | All correct pro rata (art. 4 §1). A naive "gross < scale" check flags all three. | Not flagged. The explanation of the rule shows "× hours / 38". |

Correct result before the curveball: **10 employees with findings** (3 scale, 4 meal,
1 night, 1 flexi, plus nothing else). Total monthly underpayment: 170 (scale) + 170
(meal) + 93.09 (night) = **EUR 433.09/month** for this one client (synthetic).

A naive checker (gross vs full-time scale, no hours, no clause) flags 8 on scale:
the 3 true ones plus 5 false positives (P4, P8 × 3, P7 on pay).

Distractors on purpose: the end-of-year bonus (CCT 015 art. 2) is paid in December,
so there is nothing to check in October. Two other pre-2020 employees
(BCL-1217, BCL-1112) have a legacy allowance but are above the scale anyway.

## Curveball

**When:** T+2:00 sharp.

**What you do:** create `materials/docs/cao_04_addendum_loonschalen_nl.md` with the
text below (copy exactly), then read this aloud:

> "Mentor update. The social partners of PC 399.07 signed an addendum on Friday.
> It raises the scales from 1 October and changes one seniority step, so tonight's
> October run is affected. The file is in materials/docs now. Your consultant needs
> the approved rules updated and the check re-run before the payslips go out. We
> would prefer not to wait for a developer."

**Expected effect** (after the team approves the new rules):

| Employee | Why it changes | New minimum | Paid | Gap |
|---|---|---|---|---|
| BCL-1007 (D, 1 y) | +2% | 3,213.00 | 3,155.00 | 58.00 |
| BCL-1063 (A, 2 y) | +2% | 2,254.20 | 2,230.00 | 24.20 |
| BCL-1070 (C, 5 y) | +2% | 2,968.20 | 2,920.00 | 48.20 |
| BCL-1154 (B, 7 y) | +2% | 2,590.80 | 2,555.00 | 35.80 |
| BCL-1014 (C, 9 y) | top step now from 9 y | 3,151.80 | 3,012.00 | 139.80 |
| BCL-1028 (B, 9 y) | top step now from 9 y | 2,743.80 | 2,629.00 | 114.80 |
| BCL-1224 (P1) | +2% | 2,499.00 | 2,410.00 | 89.00 |
| BCL-1273 (P2) | +2% | 2,335.80 | 2,210.00 | 125.80 |
| BCL-1119 (P3) | +2%, 3,040 incl. allowance | 3,151.80 | 3,040.00 | 111.80 |

Still NOT flagged: P4 BCL-1147 (3,740 ≥ 3,682.20), the three part-timers
(BCL-1133 is also 9 y: 3,151.80 × 30.4/38 = 2,521.44 ≤ 2,571), the decoys.
New result: **16 employees with findings**, monthly underpayment 747.40 + 170 +
93.09 = **EUR 1,010.49**. Night premium and meal findings do not change.

A strong team shows a rule diff ("art. 3 §1 amounts replaced, citation now
399.07/2026/021 art. 1–2"), the consultant approves the changed rules, and the
same check runs again with no code change. A weak team edits a Python dict.

**Full text of the late document** (`cao_04_addendum_loonschalen_nl.md`):

````markdown
# ⚠️ SYNTHETIC – not an actual CAO or Belgian law ⚠️

> Written by team IF-ELSE for a practice drill. The joint committee, the parties and
> every amount below are fictional and illustrative. Do not use for real payroll.

---

# Paritair Comité 399.07 (fictief, enkel voor deze oefening)
## Paritair Comité voor de koel- en vrieslogistiek

# Collectieve arbeidsovereenkomst van 25 september 2026
## Addendum bij de collectieve arbeidsovereenkomst van 16 juni 2026 betreffende de loonschalen en anciënniteitstrappen (399.07/2026/014)

Registratienummer: 399.07/2026/021 (fictief)

---

### Artikel 1 – Verhoging van de loonschaal

§1. Vanaf 1 oktober 2026 worden de bedragen van artikel 3, §1 van de
collectieve arbeidsovereenkomst 399.07/2026/014 verhoogd met 2,0%.

§2. De verhoogde bedragen worden afgerond op de eurocent en luiden als volgt
(in EUR, voltijdse arbeidsduur):

| Categorie | Trap 0 (0–1 jaar) | Trap 2 (2–4 jaar) | Trap 5 (5–8 jaar) | Hoogste trap (9 jaar en meer) |
|---|---|---|---|---|
| A | 2.193,00 | 2.254,20 | 2.335,80 | 2.458,20 |
| B | 2.427,60 | 2.499,00 | 2.590,80 | 2.743,80 |
| C | 2.774,40 | 2.856,00 | 2.968,20 | 3.151,80 |
| D | 3.213,00 | 3.315,00 | 3.457,80 | 3.682,20 |

### Artikel 2 – Wijziging van de hoogste anciënniteitstrap

§1. Vanaf 1 oktober 2026 wordt de hoogste trap ("trap 10") bereikt na
9 jaar anciënniteit in plaats van 10 jaar.

§2. Werknemers die op 1 oktober 2026 ten minste 9 jaar anciënniteit hebben,
worden op die datum in de hoogste trap ingeschaald. Artikel 5, §1 van de
overeenkomst 399.07/2026/014 blijft van toepassing voor latere overgangen.

### Artikel 3 – Overige bepalingen

§1. Artikel 4 (deeltijdse werknemers) en artikel 6 (overgangsregeling) van de
overeenkomst 399.07/2026/014 blijven onverminderd van toepassing, op basis van
de bedragen van artikel 1 van dit addendum.

§2. Alle andere bepalingen van de overeenkomst 399.07/2026/014 blijven
ongewijzigd.

### Artikel 4 – Inwerkingtreding

§1. Dit addendum treedt in werking op 1 oktober 2026 en volgt de
geldigheidsduur van de overeenkomst 399.07/2026/014.

---

*SYNTHETIC – fictional joint committee, fictional agreement, illustrative figures.*
````

## Traps

- **Rules hardcoded instead of extracted.** The scale lives in a Python dict or a
  prompt. It works until T+2:00 and then needs a code edit. Ask them to re-run
  without touching code.
- **No citations, or wrong ones.** "Minimum wage violated" with no article, or the
  French meal-voucher rule cited to the Dutch agreement, or a paragraph that says
  something else. Spot-check two citations against the docs.
- **Missing the transitional clause.** BCL-1147 flagged. Or the opposite: every
  pre-2020 employee exempted, so BCL-1119 is missed.
- **Rules executed without consultant approval.** The extracted table goes straight
  into the check. The approval must be enforced in code: an unapproved or rejected
  rule is never applied.
- **Treating the fictional PC as real law**, or "correcting" the scales with real
  PC 200 or other sector figures from the model's memory.
- **Pro-rata part-time errors.** The three part-timers flagged; or the night
  premium computed with 38 h for a part-timer.
- **Names sent to the cloud.** The check needs category, hire date, hours and
  amounts, not names. Sending the whole CSV (names included) to Gemini while the
  pitch says "privacy by design" is a trust hit. Rule extraction from the CAO text
  can use the cloud; the payroll check can be plain code on approved rules.
- **Smaller ones:** checking the end-of-year bonus in October; missing the
  seniority step (flagging BCL-1273 as "below minimum" without saying why); the
  flexi contract presented as a pay gap.

## What a strong result looks like

- **Persona and moment:** a named SD Worx payroll consultant (e.g. "An, 60 SME
  clients in 12 PCs") the day a new CAO lands, and the evening before the October
  payslips go out.
- **Painful moment on screen:** three agreements in two languages and a 40-line run;
  today that is hours of reading and a spreadsheet, and misses surface months later.
- **Demo path:** load the agreements → proposed rules table, each rule with a
  clickable citation and the source sentence → consultant approves / rejects each
  → run check → findings list with plain-language explanations → curveball
  addendum → rule diff → approve → re-run in seconds.
- **Trust story:** approval enforced in code, every finding traceable to an article,
  the protected employee shown as "not flagged because art. 6 §2", deterministic
  check on approved rules (no LLM in the loop for the verdict), names never leave
  the machine.
- **Number idea:** EUR 433/month underpaid for one 40-person client, EUR 1,010
  after the addendum (synthetic), caught before payslips instead of months later
  as back pay. Scale it with an explicit, labelled assumption (via `/impact-calc`),
  and link it to the ~500 Belgian SME consultants now working with agents
  (facts.md).
- **Honest limits:** fictional PC, illustrative amounts; real CAOs need expert
  review; indexation (e.g. the ⚠️ cent index) is out of scope.

## Jury questions

1. **"How do I know a rule is right before it touches 6 million payslips?"**
   Good answer: every rule shows its source article and sentence, a human approves
   each one, rejected rules never run, and the approval is logged. Bonus: they show
   the approval is enforced in code.
2. **"A new addendum arrives tomorrow. What changes in your system?"**
   Good answer: nothing in the code. The addendum is ingested, the agent proposes a
   diff against the approved rules, the consultant approves, the check re-runs.
   Best: they did exactly this live at T+2:00.
3. **"Why didn't you flag BCL-1147, who is paid below the scale?"**
   Good answer: art. 6 §2 transitional clause, hired before 2020, base plus legacy
   allowance is above the minimum; and BCL-1119 is still flagged because the sum
   falls short. Weak: "the model decided".
4. **"Which employee data goes to the language model?"**
   Good answer: the CAO text goes to the model for extraction; the payroll check is
   code on approved rules; names (and ideally IDs) never leave. The claim must match
   the code.
5. **"What is this worth to SD Worx?"**
   Good answer: a traceable number with labelled assumptions (hours per CAO per
   consultant, errors caught before payslips, back pay avoided), tied to the
   multi-agent payroll model. Not a made-up market size.

## Skills to watch

| Skill | What to observe (for the debrief) |
|---|---|
| (PDF brief) | Did the agents read `BRIEF.pdf` directly, or did someone paste it? If a tool (Codex, Cursor) cannot read PDFs, the skills or AGENTS.md need a line on it. |
| `/brainstorm`, `/kickoff` | Did they pick the consultant persona and the "before payslips go out" moment? Did `PLAN.md` reserve time for a re-run with a new document? |
| `/rag-grounding` | Citations at article + paragraph level, correct across NL and FR, and verified against the source text. Does the skill push for "quote the sentence"? |
| `/prompt-eval` | Rule extraction into a schema (rule type, category, step, amount, date, citation). Did they measure extraction on the 3 docs, or trust one run? Did the table come out with thresholds right (e.g. step 5 = 5–9 years)? |
| `/demo-step` | Approve / Reject per rule, enforced in code. Findings screen with explanations. |
| `/be-domain` | Used for meal vouchers (EUR 10 / 8.91 / 1.09, needs a CAO) and flexi-jobs (1 Jul 2026, opt-out). No invented real-PC figures. ⚠️ caveats kept. |
| `/challenge-data` | Should NOT be needed: data is given. Note if an agent regenerated or "fixed" the CSV. |
| `/privacy-check` | Names in the cloud call; privacy claim vs code. |
| `/demo-hardening` | Does the replay cache survive a new document, or does it replay stale rules after the curveball? |
| `/impact-calc`, `/pitch-rehearsal` | Number grounded in the run (EUR 433 → 1,010) with labelled assumptions; jury questions above anticipated. |

## Appendix: the brief's source text

Edit the HTML below, save it as `brief03.html`, then re-print (Git Bash):

```bash
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="D:\\Hackathon\\IF-ELSE\\practice\\03-sdworx-cao-to-payroll-check\\BRIEF.pdf" \
  "file:///C:/path/to/brief03.html"
```

Check it stays at 1–2 pages.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Brief 03 – From CAO to payroll check</title>
<style>
  @page { size: A4; margin: 18mm 18mm 16mm 18mm; }
  body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1d2330; margin: 0; }
  .disclaimer { font-size: 8.5pt; color: #7a2e0e; background: #fff4e5; border: 1px solid #f0c98a; padding: 5px 9px; margin-bottom: 12px; }
  header { border-bottom: 3px solid #0b5fa5; padding-bottom: 8px; margin-bottom: 14px; }
  .track { font-size: 9pt; letter-spacing: .08em; text-transform: uppercase; color: #0b5fa5; font-weight: 600; }
  h1 { font-size: 21pt; margin: 3px 0 2px; color: #0b2a4a; }
  .meta { font-size: 9pt; color: #5a6475; }
  h2 { font-size: 12pt; color: #0b5fa5; margin: 14px 0 4px; }
  p { margin: 4px 0 6px; }
  ul { margin: 4px 0 6px 18px; padding: 0; }
  li { margin: 2px 0; }
  .hmw { font-size: 12pt; font-weight: 600; color: #0b2a4a; border-left: 4px solid #0b5fa5; padding: 4px 10px; background: #eef5fc; margin: 6px 0; }
  code { font-family: Consolas, monospace; font-size: 9.5pt; background: #f1f3f6; padding: 0 3px; }
  footer { margin-top: 14px; font-size: 8.5pt; color: #7a8394; border-top: 1px solid #d8dde5; padding-top: 5px; }
</style>
</head>
<body>
<div class="disclaimer">Practice brief written by team IF-ELSE. Fictional: not an actual SD Worx or Tectonic brief.</div>
<header>
  <div class="track">SD Worx track · Challenge 03</div>
  <h1>From CAO to payroll check</h1>
  <div class="meta">Hackathon challenge brief · 4 hours · Pitch in English</div>
</header>

<h2>Context</h2>
<p>Every Belgian employer falls under a joint committee (paritair comité / commission paritaire). Its collective agreements (CAO / CCT) set minimum wage scales, seniority steps, bonuses, premiums, meal vouchers and, since flexi-jobs opened to all sectors on 1 July 2026, sometimes a sector opt-out. Payroll has to be PC-aware: the same gross pay can be right in one sector and wrong in another.</p>
<p>Today a payroll consultant reads each new agreement, often in Dutch or French, and translates it into payroll parameters by hand. It is careful work, but it is manual, and when something is missed the error tends to surface months later: an employee notices, a union delegate calls, or an inspection finds it. By then, correcting it means back pay and a difficult conversation with the client.</p>
<p>In June 2026 we launched a multi-agent payroll model in which our consultants supervise a team of AI agents and validate what they produce. We have seen promising internal prototypes of agents that turn legal text into rules. Now we want to see how far you can take the idea.</p>

<h2>The challenge</h2>
<div class="hmw">How might we help a payroll consultant turn a new collective agreement into payroll rules they trust, and then catch every payroll line that breaks them, before the payslips go out?</div>
<p>We imagine an agent that reads the agreement, proposes structured rules, lets the consultant approve them, and then checks a client's payroll run and explains what it finds. How you shape that is up to you.</p>

<h2>Who you're building for</h2>
<p>A payroll consultant in our Belgian SME team. They handle a portfolio of client companies across several joint committees, read Dutch and French, and are accountable for every payslip. They do not want a black box: they need to see where a rule comes from and decide whether it is right.</p>

<h2>What we give you</h2>
<p>All data is synthetic, for a fictional joint committee (<b>PC 399.07</b>) and a fictional client.</p>
<ul>
  <li><code>materials/docs/cao_01_loonschalen_nl.md</code>: wage scales and seniority steps (Dutch)</li>
  <li><code>materials/docs/cct_02_prime_cheques_repas_fr.md</code>: end-of-year bonus and meal vouchers (French)</li>
  <li><code>materials/docs/cao_03_nachtarbeid_flexi_nl-fr.md</code>: night-work premium and flexi-jobs (bilingual)</li>
  <li><code>materials/payroll_run_2026-10.csv</code>: the client's October 2026 payroll run, 40 employees</li>
  <li><code>materials/README.md</code>: what each file and column means</li>
</ul>

<h2>What success looks like for us</h2>
<ul>
  <li>Every rule points back to the exact article and paragraph it came from.</li>
  <li>The consultant stays in control: nothing is applied until a human has approved it.</li>
  <li>Every finding on the payroll run is explained in plain language a consultant could forward to the client.</li>
  <li>Agreements change all the time. Your solution should cope with that.</li>
  <li>A credible view of the value: time saved, errors caught earlier, or risk avoided.</li>
</ul>

<h2>Constraints</h2>
<ul>
  <li>Treat PC 399.07 as fictional. Do not present its figures as real Belgian law.</li>
  <li>Employee data is personal data. Show us how you handle it responsibly.</li>
  <li>The consultant decides, the agent assists.</li>
</ul>

<h2>Practical</h2>
<ul>
  <li>Working language and pitch: English. The documents are in Dutch and French.</li>
  <li>Pitch: 3 minutes, live demo preferred, followed by questions from the jury.</li>
  <li>Any stack. A working prototype beats slides. Mentors are available during the build.</li>
</ul>

<footer>Fictional practice material for team IF-ELSE drills. SD Worx facts used: joint committees and CAOs, flexi-jobs opening on 1 July 2026, the June 2026 multi-agent payroll model.</footer>
</body>
</html>
```
