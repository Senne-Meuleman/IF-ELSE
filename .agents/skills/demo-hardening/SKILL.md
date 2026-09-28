---
name: demo-hardening
description: Make a hackathon demo safe to run on stage. Records an offline replay cache of every AI call on the happy path, adds human-in-the-loop Approve/Reject steps, a reset button, seeded one-click inputs, spinners, friendly error fallbacks and a visible impact metric, writes DEMO_SCRIPT.md, then verifies the whole path with the network "off". Use at feature freeze, before rehearsal, before recording the backup video, or whenever the user says "make the demo bulletproof", "what if the Wi-Fi dies", "demo keeps breaking", "polish the app", "we present in N minutes".
---

# Demo hardening

A live demo dies from four things: the network, an unlucky model output,
leftover state from the last run, and the presenter typing under pressure.
Fix all four **without adding features**. If something is broken and can't be
fixed in 10 minutes, hide it.

Read `AGENTS.md`, `PLAN.md` and the app's entry point first, then work through
the steps in the demo path order.

## 1. Seeded inputs: no typing on stage
- Every input gets a pre-filled default or a "▶ Demo example" button. Pick the inputs that produce the best-looking output (the NL email that shows translation plus extraction).
- Keep the demo path to 3–4 clicks and write it down as `DEMO_SCRIPT.md`: click → what the audience sees → what the presenter says → recovery line if it fails.

## 2. Offline replay cache
The cache pattern (see the `scaffold` skill's snippets) keys on the exact request payload: `DEMO_CACHE=off | record | replay | strict`.
1. Set `DEMO_CACHE=record`, click the seeded path once per backend you'll present with. Include embeddings and voice if used.
2. Set `DEMO_CACHE=strict` and click the path again: every step must come from the cache, and a miss must show a visible warning, never a silent live call. Fix misses (usually a prompt or input that changed) and re-record.
3. **Record last, after the code freeze.** Any prompt, model, schema or temperature change invalidates the entries.
4. Commit `data/demo_cache/` (synthetic data only; check for real PII or a secret in the payloads first).
Do not disconnect the user's machine to test; `strict` mode is the proof.

## 3. Human in the loop, visibly
Any agent action that changes data, pays, sends a message or decides about a person shows a proposal card with **✅ Approve / ❌ Reject** and executes only after approval. Enforced in code: approval bound to the exact proposal, Reject performs no mutation, reruns and double-clicks cannot execute twice, Approve disabled after use. This is a pitch point, not just a safety: say it.

## 4. State and reset
- A sidebar **🔄 Reset demo** button that clears session state and reruns.
- No state that makes the second run differ from the first (appended lists, counters, "already processed" flags). Run the path twice from Reset.

## 5. Failure never shows a stack trace
- Wrap every AI call site: `try/except Exception` → `st.warning("The AI is taking a breather, showing the last good result")` plus a cached or hardcoded fallback. Log the error to the console only.
- Spinners with human text on every call.
- For extraction, validate required fields and fall back to a labeled example when the model returns nulls.
- Don't silently route "local only" data to a cloud backend as a fallback.

## 6. Make the value visible
- One `st.metric` row with the headline impact from `/impact-calc` ("Time per case: 11 min → 20 s").
- Agent steps shown as concise tool names and sanitized results; never hidden reasoning or raw dumps.
- If PII masking is on, a small "sent to the model" caption with the `<IBAN_1>` tokens: a privacy proof in one glance.
- Page title and icon = the product name. Remove unused tabs, debug prints, "TODO" text. Check at projector resolution: wide layout, browser zoom 125%, nothing cut off.

## 7. Verify and record
- Run `/demo-check` (or the `demo-tester` agent): the path twice, Reject/Approve/rerun, Reset, `strict` replay, timings.
- Record a 60–90 s screen recording of the happy path as the backup (Win+Alt+R with Xbox Game Bar, or OBS). Put it on the desktop and on a phone. Upload it unlisted for `/submission-pack`.

## Output
A short report: what changed, the final demo path (3–4 clicks, in `DEMO_SCRIPT.md`), cache status (N responses recorded, strict replay passed or failed), and anything still risky with the recommendation to hide it or accept it.
