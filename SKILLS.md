# Skills for Claude Code, Codex and Cursor

The same eleven workflows are available to all three agents. They contain no
required model IDs, agent-specific tool calls or absolute machine paths.
The coding agent's model is separate from the demo application's LLM backend.

## Use

- **Claude Code:** project skills live in `.claude/skills/`. Invoke `/kickoff`,
  `/demo-check`, etc., or ask naturally. `CLAUDE.md` imports `AGENTS.md`.
- **Codex with GPT models:** project skills live in `.agents/skills/`. Invoke
  `$kickoff`, `$demo-check`, etc., or select a skill in the client.
- **Cursor agents:** use the same `.agents/skills/` directory. Invoke `/kickoff`,
  `/demo-check`, etc., or ask naturally. No separate `.cursor/skills/` copy is
  necessary. Agent/model selection stays in your client settings.

Restart or reload the agent session if newly added skills are not listed. For a
client without skill discovery, explicitly ask it to read the relevant SKILL.md.
These are repository skills, not an installation into plain ChatGPT or a raw GPT
API call. They work in coding-agent environments that load local skills.

Discovery locations follow the official [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills),
[Cursor skill documentation](https://cursor.com/docs/skills) and
[Claude Code skill documentation](https://code.claude.com/docs/en/skills).

## Catalog

- **kickoff:** turn the challenge into one persona, demo path, timed plan and team split.
- **be-domain:** verify Belgian legal and sponsor claims from dated source material.
- **impact-calc:** calculate capacity freed and net value with explicit assumptions.
- **challenge-data:** extend seeded synthetic fixtures without changing existing IDs.
- **demo-hardening:** improve replay, approvals, resets and stage-friendly recovery.
- **epic-pitch-deck:** create an animated HTML pitch with a clearly identified mock.
- **demo-check** (new): test seeded clicks, reject/approve, repeat runs and offline behavior.
- **privacy-check** (new): review secrets, cloud boundaries, tool permissions and claims.
- **prompt-eval** (new): compare prompt/extraction behavior on synthetic NL/FR/EN cases.
- **rag-grounding** (new): inspect retrieval evidence, citations and missing answers.
- **pitch-rehearsal** (new): time the pitch and prepare evidence-based jury answers.

Start with kickoff; use challenge-data, rag-grounding and prompt-eval while
building; finish with demo-hardening, demo-check, privacy-check and pitch-rehearsal.
The original Claude subagents remain optional wrappers/helpers. Other agents can
perform the workflows directly; no subagent installation is required.

## Maintain

`.claude/skills/` remains the canonical source to preserve the existing Claude
setup. `.agents/skills/` is a committed, byte-for-byte copy including references,
templates and scripts. Ordinary files work on Windows without symlink privileges.

```powershell
python scripts/sync_skills.py
python scripts/sync_skills.py --check
```

The script uses only Python's standard library. It validates required metadata,
folder names and resource references, then copies changed files. `--check` writes
nothing and fails on drift; GitHub Actions runs it on pushes and pull requests.
Unexpected target files are reported, never deleted automatically. When removing
a source resource or skill, review and remove its generated counterpart too.
Do not copy caches, credentials or output artifacts into skill folders.

Validate behavior as well as synchronization: run changed helper scripts and
try a realistic request with the relevant agent when available. Syntax and file
parity do not prove all three clients have loaded the skills.

This checkout contains no app.py, blocks/, pyproject.toml or smoke_test.py. App
workflows require the actual kit; a skill-only update cannot verify its happy path.
