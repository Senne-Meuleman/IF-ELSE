---
name: scaffold
description: Bootstrap the hackathon demo app from nothing in about 15 minutes, right after /kickoff. Sets up the project (default Python 3.12 + uv + Streamlit + Gemini through the OpenAI-compatible API, with Ollama as offline fallback), the .env, a one-file app shell with one tab per demo step, and the small helpers the demo needs (LLM ask/extract/tool loop, replay cache, PII masking, seeded data) from tested snippets. Use when the team says "set up the project", "start the app", "scaffold", "create the repo structure", "first commit", or when a skill needs an app that does not exist yet.
---

# Scaffold: from empty repo to first working AI call

There is no starter kit in this repo by design. This skill builds the smallest
app the plan in `PLAN.md` needs, and nothing more. Target: **15 minutes** to a
Streamlit page that makes one real Gemini call with a seeded input.

## 1. Decide the stack (1 minute, don't debate)
- **Default: Python 3.12 + uv + Streamlit + Gemini.** Fastest path to a
  clickable multi-screen demo; pandas and pydantic are free; Google Cloud is a
  partner. Use this unless the team is clearly stronger in JavaScript.
- **Alternative: Next.js + Vercel AI SDK** when the demo must look like a
  consumer app (mobile-like banking UI) and two teammates are JS-native. Same
  patterns apply; port the snippets.
- Never: a database, auth, Docker, a queue, a microservice. Files and
  `st.session_state` are the database.

## 2. Create the project
```powershell
uv init --python 3.12 --no-workspace .        # if pyproject.toml does not exist yet
uv add streamlit httpx pydantic python-dotenv pandas faker
uv add pypdf            # only if the brief comes with PDFs
```
Files to create (copy from `references/snippets.md`, then trim to what the plan needs):
```
app.py            entry point: sidebar (backend, privacy toggle, reset), one tab per demo step
llm.py            ask / extract / run_agent + replay cache, Gemini or Ollama via one env var
pii.py            mask / unmask (only if the pitch claims privacy)
data/synth.py     seeded fake Belgian data (see /challenge-data)
.env.example      LLM_BACKEND, GEMINI_API_KEY, GEMINI_MODEL, ELEVENLABS_API_KEY, DEMO_CACHE
.gitignore        .env  .venv/  __pycache__/  data/index.npz
DEMO_SCRIPT.md    3–4 clicks; filled in by /demo-hardening
```
Copy `.env.example` to `.env`, paste the Gemini key (from the team's private
note, never from chat history), keep `DEMO_CACHE=record` from the first run so
every good answer is already cached for the offline replay later.

## 3. Wire the first demo step
Add one tab with a seeded input and one AI call following `/demo-step`. Run:
```powershell
uv run streamlit run app.py
```
Click the seeded example. If the answer appears, commit: `git commit -am "scaffold: first AI call works"`.
That commit is the team's safety net for the rest of the evening.

## 4. Split the files between teammates
Following `AGENTS.md` "Working in parallel": the demo owner keeps `app.py`;
every other step lives in its own file (`steps/triage.py` exposing
`render()`), imported by `app.py`. Data and prompts in their own files too.
Tell the team which file is whose in `PLAN.md`.

## Rules
- Gemini via the OpenAI-compatible endpoint (`/v1beta/openai`), so switching to
  Ollama, OpenAI or a Vertex model is one env var, not a rewrite.
- For Ollama keep `reasoning_effort: none` (qwen3.5 otherwise thinks until the
  context is full and returns nothing) and expect weak structured extraction.
- `DEMO_CACHE` modes: `off` (live), `record` (live + save), `replay` (cache,
  else live + save), `strict` (cache only, raise on miss). The key is the exact
  request, so seeded inputs and unchanged prompts are what make replay work.
- Don't build voice, RAG or a second persona in the scaffold. Add them as
  steps when the plan calls for them.

## Output
The running app, the file list with owners, and the exact command each
teammate runs to start it. Confirm the first AI call was live, not cached.
