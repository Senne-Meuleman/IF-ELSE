# Setup notes (30 Sept 2026)

Only the **tooling** was prepared before the event. No demo code: the app is built
from scratch on the day with `/scaffold`.

## What to do (each teammate, once)
1. Install uv: `winget install astral-sh.uv`, then **restart your terminal**.
2. `git pull`
3. `uv sync` (downloads Python 3.12 and all packages into `.venv`, automatic).
4. `copy .env.example .env`, then paste the shared Gemini key after `GEMINI_API_KEY=`.
   Get the key from the team's private note. **Never commit `.env`** (it is gitignored).

## What was added
| File | What / why |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | The project's package list (streamlit, httpx, pydantic, python-dotenv, pandas, faker). Everyone gets identical versions. Change with `uv add <package>`, not by hand. |
| `.env.example` | Template for `.env` (which holds the secret key). Safe to commit, contains no secret. |
| `.gitignore` | Added `data/index.npz`. |

## Changes worth knowing
- **Gemini model is now `gemini-3.8-flash`** (was `gemini-2.5-flash`). Google retired 2.5 for new accounts and it returned a 404. Changed in `.env.example`, `README.md` and the scaffold skill snippets. If 3.8 is overloaded (503), set `GEMINI_MODEL=gemini-flash-lite-latest` in `.env`.
- `uv init` wanted to create a `src/` package folder. Removed: we keep a flat app.

## Not a problem
- "No interpreter" in VS Code: Python is inside `.venv`. Pick it via Ctrl+Shift+P → "Python: Select Interpreter" → `.venv`.
- `uv` is not found: restart the terminal so the new PATH loads.
