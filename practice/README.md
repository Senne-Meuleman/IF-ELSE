# Practice drills

Five mock challenges in the style we expect from KBC and SD Worx. They let us
test the skills, practise the team split and time-box, and find what breaks
**before** Wednesday. They are fictional: the briefs, sponsor quotes and data
are made up by us, not published by KBC, SD Worx or Tectonic.

| # | Track | Challenge | Format | What it trains |
|---|---|---|---|---|
| 01 | SD Worx | [Inbox to action](01-sdworx-inbox-to-action/BRIEF.md) | 90-min sprint (warm-up) | `/scaffold`, `/demo-step`, extraction + `/prompt-eval`, approval gate, prompt injection, `/privacy-check` |
| 02 | KBC | [Pause before you pay](02-kbc-pause-before-you-pay/BRIEF.md) | 2 h or full 4 h | agent with Approve/Reject, NL/FR, voice (ElevenLabs), `/be-domain` on fraud rules, `/impact-calc` |
| 03 | SD Worx | [From CAO to payroll check](03-sdworx-cao-to-payroll-check/BRIEF.pdf) | full 4 h | PDF brief, `/rag-grounding` with citations, rule extraction, a late new document |
| 04 | KBC | [The SME cash-flow moment](04-kbc-sme-cashflow/BRIEF.md) | 2 h | vague brief → `/brainstorm`, no data given → `/challenge-data`, Peppol facts, business model question |
| 05 | SD Worx | [Pay transparency, before the law lands](05-sdworx-pay-transparency/BRIEF.md) | 2 h, then **cut to 1 h 15** | uncertain law (`/be-domain` ⚠️), charts, the re-scope in `/kickoff`, careful claims |

Each folder has:
- `BRIEF.md` (or `.pdf`): what the team gets at T+0. Read it only when the drill starts.
- `materials/`: whatever the "sponsor" hands over (sometimes nothing, on purpose).
- `ORGANIZER.md`: **sealed**. The curveball and when to drop it, the traps, what a strong
  answer looks like, and the jury questions. Only the organizer opens it before the pitch.
  Agents must not read it while building (see `AGENTS.md`).

## Running a drill

1. **Pick an organizer** (rotate). They read `ORGANIZER.md`, keep time, play the
   sponsor mentor for questions and drop the curveball on time. The organizer can
   also build; they just don't share the file.
2. **Branch off** so the demo code never lands on `main`:
   `git switch -c drill/01` → build in the repo root as on the real day → at the end,
   `git switch main` and delete the branch. Keep only lessons, not code.
3. **Start the clock** and follow the README game plan, compressed to the drill
   format (see below). Use the skills exactly as we would on Wednesday:
   `/brainstorm` → `/kickoff` → `/scaffold` → build → `/demo-hardening` → `/pitch-rehearsal` → `/submission-pack`.
4. **Pitch** for 3 minutes, live, to the organizer. Then run the `judge` subagent,
   and let the organizer ask the ORGANIZER.md questions.
5. **Debrief (15 min)**, fill in the template below and turn every "the skill
   got this wrong" into a fix in `.claude/skills/` the same evening.

### Time-box per format

| Phase | Full 4 h | 2 h | 90-min sprint | 30-min paper drill (no code) |
|---|---|---|---|---|
| Brief, brainstorm, pick | 0:00–0:15 | 0:00–0:10 | 0:00–0:08 | 0:00–0:10 |
| Kickoff → `PLAN.md` | 0:15–0:30 | 0:10–0:18 | 0:08–0:15 | 0:10–0:18 |
| Scaffold, first AI call | 0:30–0:45 | 0:18–0:30 | 0:15–0:25 | – |
| Build | 0:45–3:00 | 0:30–1:25 | 0:25–1:05 | – |
| Freeze, harden, check | 3:00–3:20 | 1:25–1:35 | 1:05–1:12 | – |
| Deck + rehearsal | 3:20–3:45 | 1:35–1:50 | 1:12–1:22 | 0:18–0:27 (pitch outline + `judge`) |
| Submission pack | 3:45–4:00 | 1:50–2:00 | 1:22–1:30 | – |
| Pitch + questions | 5 min | 5 min | 5 min | 3 min |

The **paper drill** uses any brief with no code: brainstorm, kickoff, pitch
skeleton, `judge`. Do it for the challenges we don't have time to build; it
trains the part of the evening that decides the most.

### Suggested plan before Wednesday
- **Mon evening:** 01 as a 90-min sprint (tests the whole pipeline end to end).
- **Tue:** 02 or 03 as a 2 h build, plus 04 and 05 as 30-min paper drills.
- **Tue late:** fix the skills that hurt, run `py scripts/sync_skills.py`, commit, pull on every laptop.

## Score sheet (organizer)

| | 1–5 | Evidence |
|---|---|---|
| Business value (persona, moment, traceable number) | | |
| Sponsor fit (their words, their reality) | | |
| Demo (live, 3–4 clicks, nothing typed) | | |
| Trust (approval in code, privacy claim true, limits named) | | |
| Clarity (problem in 20 s, ends with an ask) | | |
| **Process**: first AI call working by the target time? | yes / no | time: |
| **Process**: feature freeze respected? | yes / no | |
| **Process**: happy path broken for > 10 min at any point? | yes / no | |
| **Traps** from ORGANIZER.md caught | _ / _ | |

## Debrief template

Copy into `practice/DEBRIEF.md` (one section per drill, newest on top):

```markdown
## Drill NN – <name> – <date> – format <4h/2h/90m/paper>
Organizer: … · Roles: demo owner …, AI builder …, story …, wow …
Scores: value _/5 · fit _/5 · demo _/5 · trust _/5 · clarity _/5 · traps caught _/_
Milestones: plan at …, first AI call at …, freeze at …, pitch at …
Went well: …
Hurt us (and the fix):
- [skill /name] <what it did wrong> → <edit to make in SKILL.md>
- [teamwork] <merge conflict, idle person, unclear owner> → <new rule>
- [setup] <missing key, slow install> → <checklist item>
Would we pass round 1 with this? yes / no, because …
```
