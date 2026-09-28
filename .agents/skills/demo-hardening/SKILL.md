---
name: demo-hardening
description: Make a hackathon Streamlit demo safe to run on stage. It records an offline replay cache of every LLM call on the happy path, adds human-in-the-loop Approve/Reject steps, a reset button, seeded one-click demo inputs, spinners, friendly error fallbacks and a visible impact metric, then verifies the whole path with Wi-Fi "off". Use at feature freeze, before rehearsal, before recording the backup video, or whenever the user says "make the demo bulletproof", "what if the Wi-Fi dies", "demo keeps breaking", "polish the app", or "we present in N minutes".
---

# Demo hardening

A live demo dies from four things: the network, an unlucky LLM output, leftover state from the last run, and the presenter typing under pressure. Fix all four without adding features. **No new functionality at this stage.** If something is broken and can't be fixed in 10 minutes, hide it.

Read AGENTS.md and inspect the actual app, blocks/llm.py and blocks/cache.py first. This checkout may contain only skills; report missing prerequisites rather than inventing cache support. Work through applicable steps in the demo entry point, then run the app and click the path after changes.

## 1. Seeded inputs: no typing on stage
- Every input the demo needs gets a pre-filled default or a "▶ Demo example" button that fills it. Pick inputs that produce the best-looking output (for example the NL email that shows translation plus extraction).
- Keep the demo path to 3–4 clicks and write it down as `DEMO_SCRIPT.md` (click → what the audience sees → what the presenter says).

## 2. Offline replay cache (`blocks/cache.py`)
Verify the implemented modes and coverage rather than assuming every call is cached:
1. If record mode exists, set DEMO_CACHE=record for the demo process and record the seeded path with the selected backend. Mask customer/employee text before cloud calls. Do not expose or overwrite credentials.
2. Inspect replay behavior on a hit and a miss. If replay can make live calls, it is not strict offline operation. Add or use a bounded, explicit fallback for missing seeded responses and label replay/fallback output in the UI.
3. Test without external calls using a process-scoped network stub or an implemented strict replay mode; include embeddings and voice. Changing Ollama's URL alone cannot prove cloud calls are blocked. Do not disconnect the user's machine from Wi-Fi.
4. Share only reviewed synthetic cache records; exclude real PII, secrets and unmasking vaults. Commit them only when repository publication is in scope.

Caveats: the key is the exact request, so any prompt, model, schema or temperature change invalidates it. **Record last, after the code freeze.** RAG embeddings are cached too, so the question text must match exactly.

## 3. Human in the loop, visibly
Any agent action that changes data, pays, sends a message or makes a decision about a person must show a proposal card with **✅ Approve** / **✏️ Edit** / **❌ Reject** and execute only after approval. Enforce this in application code, not just the prompt. Bind approval to exact arguments; edits invalidate approval. Reject performs no mutation, and reruns/double-clicks cannot duplicate execution. This control alone does not establish legal compliance.

## 4. State and reset
- A sidebar **🔄 Reset demo** button that clears this demo session's state and calls `st.rerun()`. Avoid globally clearing caches shared with other sessions or deleting the recorded replay data.
- No state that makes the second run differ from the first (appended lists, counters that don't reset).

## 5. Failure never shows a stack trace
- Wrap each LLM call site in `try/except Exception as e:` → `st.warning("The AI is taking a breather, showing the last good result")` plus a cached or hardcoded fallback. Log `e` to the console only.
- Spinners with human text on every call (`st.spinner("Reading the email in Dutch…")`).
- For `extract` on Ollama, validate required fields and use a labeled synthetic fallback or cache. Do not silently route local/private data to Gemini; cloud fallback must respect the selected mode and masking boundary.

## 6. Make the value visible
- One `st.metric` row with the headline impact (from `/impact-calc`), for example "Time: 11 min → 20 s".
- Show concise tool names, status and sanitized results using `run_agent(..., on_step=...)`; do not expose hidden reasoning, secrets or unmasked tool output.
- If PII masking is on, show a small "sent to the model" caption with the `<IBAN_1>` tokens. It is a privacy proof in one glance.
- Clean up: set the page title and icon to the product name, remove unused tabs, debug prints and "Team Demo" labels, and make it look good at the projector's resolution (wide layout, zoom 125%).

## 7. Verify
- Run `uv run python smoke_test.py` for the backend you'll present with.
- Use the demo-check skill to click the path end to end and report; a Claude-only demo-tester agent is optional. Report skipped browser or offline checks explicitly.
- Record a 60–90 s screen recording of the happy path as a backup (Win+Alt+R with Xbox Game Bar, or OBS). Put it on the desktop and on a phone.

## Output
A short report: what was changed, the final demo path (3–4 clicks), the cache status (N responses recorded, offline test passed or failed), and anything still risky with a suggestion to hide it or accept the risk.
