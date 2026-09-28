# IF-ELSE: Tectonic Hackathon team kit

Shared guidance for every coding agent. Claude Code loads it through `CLAUDE.md`;
Codex and Cursor read it directly. Skills are authored in `.claude/skills/` and
copied to `.agents/skills/` (see `SKILLS.md`; never edit the copy).

## The event
Tectonic Hackathon round 1: **Wed 30 Sept 2026, 18:00–23:00, Gent**. Two tracks,
**KBC** (bank/insurer) and **SD Worx** (HR & payroll), each with a real business
case. Top 16 per track go to the final on 20 Oct (EUR 10,000). "No coding
experience required", so judges weigh business value and the pitch at least as
much as code. `README.md` has the facts, the timeline and the checklist.

## What we are building
Nothing yet, on purpose. There is no starter kit in this repo: the team builds
the demo app from scratch on the day, in whatever stack is fastest for the
challenge (default: Python + Streamlit + Gemini, see `/scaffold`). Skills
describe patterns and checks, not existing files. Do not look for `blocks/`,
`app.py` or `smoke_test.py` unless the team has created them; if a skill needs
something that does not exist yet, build the smallest version of it.

## Priorities (in order)
1. **The demo path always works.** Never leave the entry point broken. After
   any change, run the app and click the happy path.
2. **Business value you can see on screen**: a real user, a painful moment, and
   a number (EUR or hours saved).
3. **Fake anything that isn't on screen.** Hardcode, seed and cache freely.
4. Working beats pretty beats clever. No unit tests, no abstractions, no
   refactors after T−90 min.

## Conventions for the demo app
- One demo step per screen or tab. Every input has a seeded default or a
  "▶ Demo example" button. A spinner with human text on every AI call. The
  headline impact number is visible in the UI.
- An explicit **Approve / Reject** step before any agent action that changes
  data, pays, or contacts a person. KBC: "Kate never acts without explicit
  customer approval". SD Worx: "humans supervise payroll agents". Enforce it in
  code, not in the prompt; Reject and reruns must never execute.
- Cloud LLM (Gemini, a tech partner) for quality. If the pitch claims privacy,
  mask personal data before the cloud call and keep the claim exactly as true as
  the code. Ollama + qwen3.5:4b is installed on Henri's laptop as an offline
  fallback.
- Every AI call site: `try/except` → friendly warning plus a cached or hardcoded
  fallback. A stack trace on stage is a lost round.
- Answer in the user's language (NL/FR/EN) with Belgian terms (paritair comité,
  rijksregisternummer, Peppol, itsme). Never invent Belgian law or sponsor
  figures: use `/be-domain` or label the number "illustrative".
- Only synthetic data in the repo. Never commit `.env`.
- Python style: 3.12+, type hints, pydantic for anything structured, short
  docstrings, one or two files until that hurts.

## Working in parallel (3–4 people, one repo)
- Own **files**, not features: one file per demo step, the entry point is owned
  by the demo owner only. This is what keeps merges trivial.
- Small commits on `main`; pull before push, every 20–30 minutes. Branches only
  for risky experiments; a git worktree when an agent runs a long task.
- After every merge: run the app, click the path. Broken for more than 10
  minutes → revert.
- Keep `PLAN.md` (from `/kickoff`) and `DEMO_SCRIPT.md` (from
  `/demo-hardening`) current. The presenter and the agents both read them.

## Practice drills
`practice/` holds five fictional mock challenges for rehearsing before the
event (see `practice/README.md`). They are not the real brief: ignore them on
the day unless someone asks for a drill. Never read a `practice/*/ORGANIZER.md`
file unless the user says they are the organizer or asks for the debrief or the
jury questions; it holds the planted answers. Drill code lives on a
`drill/NN` branch and never merges into `main`.

## Skills workflow
Brief → `/brainstorm` (interactive, the whole team) → `/kickoff` → `/scaffold` → build with `/demo-step`, `/challenge-data`,
`/rag-grounding`, `/prompt-eval`, `/be-domain`, `/impact-calc` → T−60
`/demo-hardening`, `/demo-check`, `/privacy-check` → `/epic-pitch-deck`,
`/pitch-rehearsal` → `/submission-pack`. The Claude subagents (`researcher`,
`judge`, `demo-tester`, `security-check`) are optional wrappers around those
skills; any agent can run the skill itself.
