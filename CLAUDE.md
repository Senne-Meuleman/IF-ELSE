@AGENTS.md

## Claude Code specifics
- Skills: `/brainstorm`, `/kickoff`, `/scaffold`, `/demo-step`, `/challenge-data`, `/be-domain`,
  `/impact-calc`, `/rag-grounding`, `/prompt-eval`, `/demo-hardening`,
  `/demo-check`, `/privacy-check`, `/epic-pitch-deck`, `/pitch-rehearsal`,
  `/submission-pack`. Catalog and maintenance in `SKILLS.md`.
- Subagents: `researcher` (sourced web facts, run it in the background),
  `judge` (scores the idea or the pitch, asks the hard questions),
  `demo-tester` (clicks through the demo and reports), `security-check`
  (secrets, PII, unsafe agent actions).
- `.claude/skills/` is the source. A PostToolUse hook re-syncs
  `.agents/skills/` on every skill edit and syntax-checks any edited `.py`
  file, so a broken entry point is reported immediately.
- On this machine `python` is not on PATH: use `py` or `uv run python`.
- When several tasks run in parallel, give each its own file (see "Working in
  parallel" above) or its own worktree, and run `demo-tester` after each merge.
