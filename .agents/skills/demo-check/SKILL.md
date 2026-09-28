---
name: demo-check
description: Verify the hackathon demo after a merge or before rehearsal with smoke tests, seeded UI clicks, approval checks, reset and offline replay. Reports evidence without changing application code unless asked to fix it.
---

# Demo check

Read AGENTS.md and DEMO_SCRIPT.md from the repository root. Confirm app.py,
blocks/ and smoke_test.py exist before running kit commands. If absent, report
that this is an instructions-only checkout; do not invent a passing app test.

1. Identify the presenting backend and the exact seeded inputs. Use the existing
   smoke test for that backend. Never print .env values to check configuration.
2. Start Streamlit on an available local port and exercise the happy path with
   the browser tools available in this agent. Use stable labels/keys. Verify the
   actual output, language, impact metric and absence of exceptions at each step.
   If browser control is unavailable, use Streamlit AppTest when installed and
   explicitly distinguish headless checks from visual verification.
3. Test Reject (no mutation), Approve (one mutation), and a rerun (no duplicate
   mutation). Reset and repeat the seeded path to catch stale session state.
4. Inspect blocks/cache.py before testing replay. Block external calls in a
   process-scoped test or use an existing strict offline mode. Merely breaking
   Ollama's URL does not prove Gemini, OpenAI, embeddings or voice are offline.
   Test a recorded request and an unseen request; a cache miss should be visible
   and must not silently claim a live AI result.
5. Measure the slow steps; flag waits over eight seconds. Stop only processes
   started for this check and restore any process-scoped configuration.

Report DEMO-READY, RISKY or BROKEN; exact path and backend tested; observed
results and timings; offline status; and blockers with file/line references.
Missing prerequisites or skipped checks must remain visible in the verdict.
