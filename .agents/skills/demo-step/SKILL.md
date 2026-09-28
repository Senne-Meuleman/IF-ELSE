---
name: demo-step
description: Build one screen of the hackathon demo the right way, fast. Every step follows the same pattern - seeded input, masked AI call, visible result, Approve/Reject before any action, headline metric, graceful fallback - so four teammates produce a consistent product that survives the stage. Use whenever someone adds a feature, tab, screen or agent action, or says "add a step", "build the triage screen", "make the agent do X", "add voice", "add a chart".
---

# Demo step: the one pattern for every screen

A judge sees a screen for 20 seconds. In that time it must show **the pain**,
**the AI doing the work**, **a human staying in control**, and **the number**.
Build every step in this order and stop when the happy path works.

## The pattern
```
1. Seeded input      a selectbox / "▶ Demo example" button, never an empty box
2. Privacy proof     mask() if the pitch claims it, show "sent to the model: …" in a caption
3. The AI call       with st.spinner("Reading the email in Dutch…"); result stored in session_state
4. Visible result    3 st.metric columns + the key text; the audience must read it from the back row
5. Human in the loop proposal card → ✅ Approve / ❌ Reject, executed only after Approve
6. The number        st.metric("Time per case", "20 s", "-11 min") from /impact-calc
7. Fallback          try/except around the call → st.warning + a cached or hardcoded answer
```
Skip 5 only if the step never changes data or contacts a person. Skip 2 only if
the app is local-only or the pitch doesn't mention privacy.

## Which AI call
| Need | Call | Notes |
|---|---|---|
| free-text answer, chat | `ask` / streaming | system prompt states language + persona + the facts it may use |
| messy text → fields | `extract(text, Model)` | pydantic model with `Field(description=…)` on tricky fields; null when absent |
| look things up, then propose an action | `run_agent(task, tools)` | tools read data or **return proposals**; nothing mutates inside the loop |
| answer from the brief's documents | RAG `answer(q)` | citations visible; "not in the documents" is a valid answer |
| wow moment | ElevenLabs `speak()` | last, and only on the closing screen |
Snippets for all of these: the `scaffold` skill's snippets reference file.

## Rules that keep it on the rails
- **One file per step**: `steps/<name>.py` with `def render():`; `app.py` only
  imports it. Widget `key=` and session_state keys prefixed with the step name.
- Store every AI result in `st.session_state` so any click (a rerun) does not
  call the model again. The second run must look exactly like the first.
- Facts in prompts, not in the model's memory: paste the relevant `/be-domain`
  facts or the seeded policy text into the system prompt. Small models invent
  Belgian law.
- Prompt in English, answer in the user's language ("Answer in the language of
  the message"). Show the detected language as a metric: judges notice NL/FR.
- Approval is bound to the exact proposal (key includes its hash). Reject
  performs no mutation. Approve is disabled after use. This is a KBC / SD Worx
  talking point: say it out loud in the pitch.
- Never print a stack trace. Log to the console, show a friendly warning.
- Belgian realism in what appears on screen: euro amounts, IBANs `BE..`, PC 200,
  NL/FR names. Label illustrative figures.

## Done means
1. The happy path runs twice in a row from a fresh "Reset demo" with no typing.
2. `DEMO_CACHE=record` was on, so the answers are cached for offline replay.
3. The step's line in `DEMO_SCRIPT.md` is written: click → what appears → what the presenter says.
4. Committed and pulled by the demo owner, who clicked it once.
