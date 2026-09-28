---
name: kickoff
description: Turn a hackathon challenge brief into a winning plan in minutes. Picks one user and one painful moment, writes the 3-minute pitch skeleton, scopes the demo to what fits in the remaining time, maps it onto the Blocks kit (which app.py tabs to keep, rename or delete) and splits the work across 3–4 teammates. Use at the start of the hackathon or whenever the user pastes or points to a challenge brief, case description, or PDF from KBC / SD Worx, or says "we got the challenge", "what should we build", "plan this", "re-scope", or "we're behind".
argument-hint: "[path to brief PDF, or paste the brief] [minutes left]"
---

# Kickoff: brief → plan

The clock is the enemy. Produce a plan the team can start on **within 15 minutes** of reading the brief. Be decisive: recommend one direction and don't list options for the team to discuss.

## 1. Read the brief
- If it's a PDF or in `data/docs/`, read all of it (use the pdf skill for PDFs). If it's pasted, use that.
- Also read `README.md` (event facts, game plan) and `AGENTS.md` (the kit).
- Note the **sponsor's own words** for success, the users they name, any data they provide, and any required tech. Quote them back later in the pitch.
- Default time left is 240 minutes if the user doesn't say.

## 2. Pick ONE user and ONE painful moment
Brainstorm 3–5 candidate angles silently, then score each 1–5 on:
| Criterion | Question |
|---|---|
| Sponsor fit | Does it solve *their* stated case, in their words? |
| Visible pain | Can we show the "before" misery in 15 seconds? |
| Number | Is there an obvious € / hours / % we can claim? (see `/impact-calc`) |
| Demo-ability | Can the full happy path run in under 60 seconds on screen? |
| Buildable | Does it fit in (time left − 60 min) with the kit? |
| Wow | Agentic behaviour, voice (ElevenLabs), multilingual NL/FR, or privacy (PII masking / local model)? |

Pick the top one. Show the table briefly so the team sees why.

KBC: always include a **human-in-the-loop approval** step. SD Worx: think "humans supervise payroll agents" (their June 2026 direction).

## 3. Write the pitch skeleton first (3 minutes)
```
0:00  Hook: persona + painful moment + one number        (20s)
0:20  Why now / why it's hard (regulation, volume, languages) (20s)
0:40  LIVE DEMO: the happy path, 3–4 clicks               (80s)
2:00  Impact: € / hours / risk reduced, with assumptions  (25s)
2:25  Why it's credible: privacy, human in the loop, uses their stack, next steps (25s)
2:50  Ask / closing line                                  (10s)
```
Fill it with concrete text: persona name, the demo input (for example `inbox.json` MSG003 or customer C5007), what appears on screen, and the closing line.

## 4. Scope the demo against the kit
Map every demo step to a building block, and mark what gets faked:
| Demo step | Block | Real / faked | Owner |
|---|---|---|---|
- Tabs in `app.py`: 💬 Assistant (RAG chat), 📥 Inbox triage (`extract`), 🤖 Agent (`run_agent` with tools), 📊 Data. Say which to **keep, rename or delete**.
- New data needed? → `/challenge-data`. Challenge PDFs → `data/docs/` + `build_index`.
- Cut list: what we explicitly will **not** build.

## 5. Team split and timeline
Roles for 3–4 people (adjust to team size):
- **Demo owner**: owns `app.py`, keeps the happy path working at every moment, merges.
- **AI builder**: prompts, schemas, agent tools, data.
- **Story and numbers**: impact calc, domain facts (`/be-domain`), pitch deck (`/epic-pitch-deck`), asks the sponsor mentors questions.
- **(4th) Wow feature**: voice, a second persona, or a polish tab. Cut it first if time runs short.

Timeline relative to now, based on the README plan: build until T−45 min → **feature freeze** → `/demo-hardening` + `demo-tester` agent → record a backup video → rehearse twice.

## 6. Questions for the mentors
List 3–5 short questions to ask KBC / SD Worx mentors in the first 30 minutes (what success means, volumes, current process time, what they'd pilot).

## Output
One compact markdown plan with these sections: **Pick** (with the score table) · **Pitch skeleton** · **Demo map** · **Cut list** · **Who does what until when** · **Mentor questions**. Offer to save it as `PLAN.md`. Then offer to start the first build task immediately.

If the user says "re-scope" or "we're behind", redo only steps 4–5 with the minutes left, and cut aggressively.
