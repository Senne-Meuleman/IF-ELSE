# Tectonic Hackathon: team IF-ELSE prep kit

This repo holds the team's **agent instructions, skills and checklists**. There is
no starter app on purpose: we build the demo from scratch on the day with the
`/scaffold` skill, in whatever stack fits the challenge. See
[SKILLS.md](SKILLS.md) for the 15 skills shared by Claude Code, Codex and Cursor.

## What we know (researched 27–28 Sept 2026)

| | |
|---|---|
| **Round 1 (preselection)** | **Wed 30 Sept 2026, 18:00–23:00** at Sassevaartstraat 46, Gent. Same time in 7 cities, 700+ builders. Expect about 4 h of actual building, then pitches. |
| **Final** | Tue 20 Oct 2026, De Vooruit, Gent. Top 32 teams (16 per track). You must be able to attend. |
| **Teams** | 3–4 people. **Registration closes 29 Sept.** |
| **Tracks** | **KBC** (bank/insurer) and **SD Worx** (HR & payroll). Each brings "a real business case from their own organisation". |
| **Tech partners** | Google Cloud (Gemini), ElevenLabs (voice), Cursor, Aikido (security scanning). Using them visibly earns goodwill. |
| **Prize** | EUR 10,000 in the final. Note: *"solutions may be used by the sponsoring companies"*. |
| **Vibe** | Conference theme is **Agentic AI**. "No coding experience required", so judging weighs business value and pitch more than code. |

The briefs and judging criteria are not public. The `be-domain` skill's
`references/facts.md` has 140 lines of sourced Belgian HR, payroll, banking,
fraud, Peppol and AI Act facts for the pitch.

## Likely challenge shapes (speculation)

**SD Worx**: their own internal hackathon winners were (1) *an agent that turns legal documents into payroll validation rules* and (2) *an agent that turns unstructured customer emails into system actions*. In June 2026 they launched multi-agent payroll operations where humans supervise AI agents. Likely:
- Email/ticket → structured HR action (leave, sickness, address or bank change), with a human approving the action
- Regulation / collective agreement (CAO/CCT, joint committees) → rules, or "what changed and who is affected" (RAG + extraction)
- Employee self-service assistant in NL/FR/EN ("why is my net pay lower?", "can I go 4/5?")
- **EU Pay Transparency Directive** (Belgium missed the June 2026 deadline): pay-gap reporting, explaining salary bands
- Absence and wellbeing signals, planning and scheduling

**KBC**: Kate (5.8M users) already answers 7 out of 10 questions and is exploring agentic AI, but only *"with explicit customer approval"*. Put a human-in-the-loop confirm step in any agent demo. Likely:
- Scam and fraud detection, and *explaining* alerts to customers (phishing losses EUR 93M in 2025)
- Financial coaching and budgeting from transactions; SME / self-employed cash-flow forecasting
- Belgian B2B **e-invoicing (Peppol)**, mandatory since 2026: invoice extraction and reconciliation
- Customer message triage, KYC/AML document checks, insurance claims (KBC is also an insurer)

**For both**: privacy and GDPR matter. "PII is masked before any cloud call" is a strong pitch line, and cheap to make true.

## Game plan for the evening

| Time | Do | Skill |
|---|---|---|
| T+0:00 | Read the brief twice. Ask the KBC / SD Worx mentors what "success" means. 15-minute interactive brainstorm, converge on **one** user and **one** painful moment. | `/brainstorm`, `researcher` in the background |
| T+0:15 | Pitch skeleton first (problem → demo → impact in EUR or hours → why us). Build only what the demo needs. | `/kickoff` → `PLAN.md` |
| T+0:30 | Scaffold the app, first AI call working, first commit. | `/scaffold` |
| T+0:45 → T+3:00 | Build. One person keeps the demo path working at all times. Fake anything that isn't on screen. | `/demo-step`, `/challenge-data`, `/rag-grounding`, `/prompt-eval`, `/be-domain`, `/impact-calc` |
| T+3:00 | **Feature freeze.** Replay cache, approvals, reset, fallbacks. Record a backup video. | `/demo-hardening`, `/demo-check`, `/privacy-check` |
| T+3:20 | Deck and rehearsal, twice, timed. | `/epic-pitch-deck`, `/pitch-rehearsal`, `judge` |
| T+3:45 | Submit: README, one-liner, video, links. | `/submission-pack` |
| Pitch | Lead with the customer's pain and a number. End with the ask. | |

## Stack (decided on the day, defaults below)

- **Default**: Python 3.12 + `uv` + Streamlit + Gemini (`gemini-3.8-flash` through
  the OpenAI-compatible endpoint, so any model is one env var away). Fastest path
  from nothing to a clickable demo, and Google Cloud is a partner.
- **Offline fallback** on Henri's laptop: Ollama with `qwen3.5:4b` (chat, weak at
  extraction) and `bge-m3` (multilingual embeddings). Set
  `OLLAMA_CONTEXT_LENGTH=8192` if RAG prompts get truncated.
- **Voice**: ElevenLabs REST (`eleven_multilingual_v2` handles NL/FR). One `speak()`
  call makes a pitch memorable; do it last.
- Snippets for all of this (LLM client, extraction, tool loop, PII mask, replay
  cache, approval gate, synthetic data) are in the `scaffold` skill's
  `references/snippets.md`.

## Agent helpers

Claude Code uses `.claude/skills/`; Codex and Cursor use the synchronized
`.agents/skills/`. In Codex type `$skill-name`; in Claude Code and Cursor
`/skill-name`. Subagents (Claude Code only): `researcher`, `judge`,
`demo-tester`, `security-check`.

| When | Use |
|---|---|
| Brief arrives | `/brainstorm` with the whole team · `researcher` in the background · `/kickoff` on the pick · `judge` on the plan |
| First 30 min | `/scaffold` |
| Building | `/demo-step` for every screen · `/challenge-data` · `/be-domain` before any law or number · `/impact-calc` for the headline number · `/rag-grounding` if documents are involved · `/prompt-eval` when extraction misbehaves |
| After each merge | `demo-tester` (or `/demo-check`) |
| Feature freeze (T−60) | `/demo-hardening` → `/demo-check` → `security-check` → `/epic-pitch-deck` → `judge` on the pitch |
| Last 20 min | `/submission-pack` |

## Checklist before Wednesday

- [ ] Registered and in a team (deadline **29 Sept**). Agree on who pitches and who owns the demo path.
- [ ] Everyone: `git clone` this repo, install `uv`, open it once in Claude Code / Codex / Cursor and check the skills are listed.
- [ ] Keys ready in a private note (never in the repo): **Gemini** (aistudio.google.com/apikey) and **ElevenLabs** (free tier). Test both with a 5-line script.
- [ ] Henri: `ollama pull qwen3.5:4b bge-m3` done; test the deck pipeline once (`node scripts/smoke_test.mjs` in the `epic-pitch-deck` skill; Edge is enough).
- [ ] Laptop chargers, extension lead, phone hotspot, HDMI/USB-C adapter. Venue Wi-Fi will be slow.
- [ ] Read 10 min: `be-domain/references/facts.md` "Most useful for a pitch" block; SD Worx agentic payroll press release; KBC Kate; EU Pay Transparency; Peppol.
- [ ] Decide the team name shown on screen and the presenter's opening line.
- [ ] Run at least one drill from [`practice/`](practice/README.md) end to end (the 90-min sprint on challenge 01 is the warm-up), and fix the skills that hurt.
