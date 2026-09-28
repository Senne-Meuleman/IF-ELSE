---
name: demo-hardening
description: Make a hackathon Streamlit demo safe to run on stage. It records an offline replay cache of every LLM call on the happy path, adds human-in-the-loop Approve/Reject steps, a reset button, seeded one-click demo inputs, spinners, friendly error fallbacks and a visible impact metric, then verifies the whole path with Wi-Fi "off". Use at feature freeze, before rehearsal, before recording the backup video, or whenever the user says "make the demo bulletproof", "what if the Wi-Fi dies", "demo keeps breaking", "polish the app", or "we present in N minutes".
---

# Demo hardening

A live demo dies from four things: the network, an unlucky LLM output, leftover state from the last run, and the presenter typing under pressure. Fix all four without adding features. **No new functionality at this stage.** If something is broken and can't be fixed in 10 minutes, hide it.

Work through this checklist in `app.py` (or whatever the demo entry point is). After each step, run the app and click the path.

## 1. Seeded inputs: no typing on stage
- Every input the demo needs gets a pre-filled default or a "▶ Demo example" button that fills it. Pick inputs that produce the best-looking output (for example the NL email that shows translation plus extraction).
- Keep the demo path to 3–4 clicks and write it down as `DEMO_SCRIPT.md` (click → what the audience sees → what the presenter says).

## 2. Offline replay cache (`blocks/cache.py`)
Every `llm.*` call already goes through the cache when `DEMO_CACHE` is not `off`:
1. Set `DEMO_CACHE=record` in `.env`, restart Streamlit, and click the full demo path with the good backend (Gemini) until the outputs look great.
2. Set `DEMO_CACHE=replay`. Identical requests are now served from `data/demo_cache/` instantly, and live calls happen only for unseen inputs. If a live call fails, it falls back to the cache when possible.
3. Test it: disconnect Wi-Fi (or set the backend base URL to `http://localhost:1/v1`) and click the path. Everything seeded must still work.
4. Commit `data/demo_cache/` so every teammate's laptop can run the demo.

Caveats: the key is the exact request, so any prompt, model, schema or temperature change invalidates it. **Record last, after the code freeze.** RAG embeddings are cached too, so the question text must match exactly.

## 3. Human in the loop, visibly
Any agent action that changes data, pays, sends a message or makes a decision about a person must show a proposal card with **✅ Approve** / **✏️ Edit** / **❌ Reject** (`st.button` in `st.columns`) and only "execute" after the click, with a `st.toast` confirmation. It is a pitch point for both sponsors (KBC: explicit customer approval; SD Worx: humans supervise payroll agents) and for the EU AI Act.

## 4. State and reset
- A sidebar **🔄 Reset demo** button that clears `st.session_state` and `st.cache_data`, then calls `st.rerun()`.
- No state that makes the second run differ from the first (appended lists, counters that don't reset).

## 5. Failure never shows a stack trace
- Wrap each LLM call site in `try/except Exception as e:` → `st.warning("The AI is taking a breather, showing the last good result")` plus a cached or hardcoded fallback. Log `e` to the console only.
- Spinners with human text on every call (`st.spinner("Reading the email in Dutch…")`).
- For `extract` on Ollama, check for null-heavy results and fall back to Gemini or the cache.

## 6. Make the value visible
- One `st.metric` row with the headline impact (from `/impact-calc`), for example "Time: 11 min → 20 s".
- Show the "agent thinking" (`run_agent(..., on_step=...)`) in a bordered container, because judges love seeing the tools fire.
- If PII masking is on, show a small "sent to the model" caption with the `<IBAN_1>` tokens. It is a privacy proof in one glance.
- Clean up: set the page title and icon to the product name, remove unused tabs, debug prints and "Team Demo" labels, and make it look good at the projector's resolution (wide layout, zoom 125%).

## 7. Verify
- Run `uv run python smoke_test.py` for the backend you'll present with.
- Spawn the `demo-tester` agent to click the path end to end and report.
- Record a 60–90 s screen recording of the happy path as a backup (Win+Alt+R with Xbox Game Bar, or OBS). Put it on the desktop and on a phone.

## Output
A short report: what was changed, the final demo path (3–4 clicks), the cache status (N responses recorded, offline test passed or failed), and anything still risky with a suggestion to hide it or accept the risk.
