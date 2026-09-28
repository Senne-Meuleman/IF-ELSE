---
name: demo-check
description: Verify the hackathon demo after a merge or before rehearsal - start the app, click the seeded happy path, test Reject/Approve/rerun, Reset, offline replay and timings, and report DEMO-READY / RISKY / BROKEN with evidence. Reports without changing application code unless asked to fix. Use after every merge, before recording the video, before the pitch, or when someone says "does the demo still work", "check the app", "test the happy path".
---

# Demo check

Read `AGENTS.md` and `DEMO_SCRIPT.md` (if it doesn't exist yet, derive the
path from `PLAN.md` and say so). This is a test, not a build: report; fix only
when the user asks.

1. **Start the app** on a free local port with the team's command (typically
   `uv run streamlit run app.py --server.port 8502 --server.headless true`).
   Confirm the backend and `DEMO_CACHE` mode it runs with without printing
   `.env` values.
2. **Click the happy path** exactly as `DEMO_SCRIPT.md` describes, with the
   browser tools if available (Claude-in-Chrome), otherwise with Streamlit's
   `AppTest` (`from streamlit.testing.v1 import AppTest`) and say clearly which
   one was used: a headless check does not prove the layout looks right. At
   each step verify the actual output text, the language, the metric and the
   absence of exceptions or red boxes.
3. **Approval semantics**: Reject → no mutation. Approve → exactly one
   mutation. Rerun / double-click → still one. Approve disabled afterwards.
4. **Reset and repeat** the whole path: the second run must match the first
   (no leftover lists, counters, or "already done" states).
5. **Offline**: set `DEMO_CACHE=strict` (cache only) in the app's environment
   and run the path again. Every step served from cache = offline-ready. A miss
   must show a visible warning, not a silent live call. Breaking one backend's
   URL proves nothing about the others, embeddings or voice.
6. **Timings**: measure each step; flag anything over 8 seconds and suggest
   the cache or a smaller prompt.
7. Stop only the processes you started; restore any env var you changed.

## Report
`DEMO-READY`, `RISKY` or `BROKEN`, then: path and backend tested, per-step
observed result and timing, approval results, reset result, offline status
(N/N steps from cache), and blockers with file and line. Skipped checks stay
visible in the verdict; never report a check you didn't run.
