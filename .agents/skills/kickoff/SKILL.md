---
name: kickoff
description: Turn the chosen idea (from /brainstorm, or a pasted brief) into a concrete plan in minutes - persona and painful moment confirmed, the 3-minute pitch skeleton, the demo scoped to the remaining time, every demo step mapped to what gets built or faked, and the work split across 3–4 teammates by file, saved as PLAN.md. Use after the brainstorm, or when the user says "plan this", "make the plan", "who does what", "re-scope", or "we're behind". For open-ended "what could we build" questions, use /brainstorm first.
---

# Kickoff: brief → plan

The clock is the enemy. Produce a plan the team can start on **within 15 minutes**.
The divergent thinking belongs in `/brainstorm`; this skill converges. Be
decisive: one direction, concrete owners, a cut list.

## 1. Read the brief
- If it's a PDF, read all of it (use the available PDF reader). If it's pasted, use that.
- Also read `README.md` (event facts, likely challenge shapes) and `AGENTS.md` (priorities, conventions).
- Note the **sponsor's own words** for success, the users they name, any data they provide, and any required tech. Quote them back in the pitch.
- Default time left is 240 minutes if the user doesn't say. Ask the mentors when pitches start if unknown.

## 2. Pick ONE user and ONE painful moment
If `BRAINSTORM.md` exists or the team has already chosen, take that pick and its
reasons; skip the scoring unless the team asks. If nothing has been chosen yet,
offer `/brainstorm` (15 interactive minutes) and, if the team prefers a fast
plan, brainstorm 3–5 candidate angles silently and score each 1–5 on:
| Criterion | Question |
|---|---|
| Sponsor fit | Does it solve *their* stated case, in their words? |
| Visible pain | Can we show the "before" misery in 15 seconds? |
| Number | Is there an obvious EUR / hours / % we can claim? (see `/impact-calc`) |
| Demo-ability | Can the full happy path run in under 60 seconds on screen, in 3–4 clicks? |
| Buildable | Does it fit in (time left − 60 min) with `/scaffold` + `/demo-step` patterns? |
| Wow | Agentic behaviour with visible approval, voice (ElevenLabs), NL/FR, privacy (PII masking)? |

Pick the top one. Show the table briefly so the team sees why.

KBC: always include a **human-in-the-loop approval** step ("Kate never acts without explicit customer approval"). SD Worx: think "humans supervise payroll agents" (their June 2026 launch). Both: an AI Act / GDPR-aware line earns trust with the experts in the room.

## 3. Write the pitch skeleton first (3 minutes)
```
0:00  Hook: persona + painful moment + one number        (20s)
0:20  Why now / why it's hard (regulation, volume, languages) (20s)
0:40  LIVE DEMO: the happy path, 3–4 clicks               (80s)
2:00  Impact: EUR / hours / risk reduced, with assumptions (25s)
2:25  Why it's credible: privacy, human in the loop, uses their stack, next step (25s)
2:50  Ask / closing line                                  (10s)
```
Fill it with concrete text: persona name, the exact demo input (the NL email, customer C5007), what appears on screen, the closing line.

## 4. Scope the demo
Map every demo step to what gets built and what gets faked:
| Demo step | Screen | AI call (ask / extract / agent / RAG / voice) | Data needed | Real / faked | Owner |
|---|---|---|---|---|---|
- Stack: default from `/scaffold` (Python + Streamlit + Gemini) unless the brief or team says otherwise.
- Data: what synthetic tables and planted cases → `/challenge-data`. Documents from the brief → `/rag-grounding`.
- **Cut list**: what we explicitly will **not** build (login, real integrations, a second persona, mobile layout…).

## 5. Team split and timeline
Roles for 3–4 people, **each owning files, not features** (see `AGENTS.md`):
- **Demo owner**: `app.py`, scaffold, merges, keeps the happy path working at every moment, `DEMO_SCRIPT.md`.
- **AI builder**: prompts, pydantic schemas, agent tools, the hardest step.
- **Story and numbers**: `/impact-calc`, `/be-domain` facts, `/epic-pitch-deck`, mentor questions, pitch.
- **(4th) Wow feature**: voice, a chart, a second language, polish. First thing cut if late.

Timeline relative to now: `/scaffold` by T+30 → build until **T−60 feature freeze** → `/demo-hardening`, `/demo-check`, `/privacy-check` → backup video → `/pitch-rehearsal` twice → `/submission-pack` at T−20. With under 60 minutes left: one working path and rehearsal, nothing else.

## 6. Questions for the mentors
3–5 short questions for the KBC / SD Worx mentors in the first 30 minutes: what does success look like, volumes, minutes per case today, who does the work now, what would they pilot, what data or documents can they share.

## Output
One compact plan with sections **Pick** (with scores) · **Pitch skeleton** · **Demo map** · **Cut list** · **Who does what until when** · **Mentor questions**. Save it as `PLAN.md`. Then start `/scaffold` if the user asked to build.

If the user says "re-scope" or "we're behind", redo only steps 4–5 with the minutes left, and cut aggressively: the demo path first, everything else after.
