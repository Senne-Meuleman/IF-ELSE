# Skills for Claude Code, Codex and Cursor

The same fifteen workflows are available to all three agents. They contain no
required model IDs, agent-specific tool calls or absolute machine paths. The
coding agent's model is separate from the demo application's LLM backend.

## Use

- **Claude Code:** project skills live in `.claude/skills/`. Invoke `/kickoff`,
  `/scaffold`, etc., or ask naturally. `CLAUDE.md` imports `AGENTS.md`.
- **Codex with GPT models:** project skills live in `.agents/skills/`. Invoke
  `$kickoff`, `$scaffold`, etc., or select a skill in the client.
- **Cursor agents:** use the same `.agents/skills/` directory. Invoke `/kickoff`,
  `/scaffold`, etc., or ask naturally. No separate `.cursor/skills/` copy is
  necessary.

Restart or reload the agent session if newly added skills are not listed. For a
client without skill discovery, ask it to read the relevant `SKILL.md`.

Discovery locations follow the official [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills),
[Cursor skill documentation](https://cursor.com/docs/skills) and
[Claude Code skill documentation](https://code.claude.com/docs/en/skills).

## Catalog (in the order you'll need them)

| Skill | Moment | What it does |
|---|---|---|
| **brainstorm** | brief arrives | interactive 15-minute team brainstorm in rounds: reframe, diverge through lenses, deepen, steelman and kill, converge → `BRAINSTORM.md` |
| **kickoff** | after the pick | pitch skeleton, demo map, cut list, team split by file → `PLAN.md` |
| **scaffold** | T+30 | bootstrap the demo app (default Python + Streamlit + Gemini) with snippets for LLM calls, extraction, tools, PII masking, replay cache |
| **demo-step** | every screen | the pattern for one demo step: seeded input → AI → proposal → Approve/Reject → metric → fallback |
| **challenge-data** | building | seeded synthetic Belgian data with planted demo moments |
| **be-domain** | before any law or number | sourced Belgian HR/payroll/banking/regulation facts (`references/facts.md`) |
| **impact-calc** | building | the headline EUR / hours number with explicit assumptions |
| **rag-grounding** | if documents are involved | small index, grounded answers with citations, honest "not found" |
| **prompt-eval** | extraction misbehaves | 6–12 NL/FR/EN cases, measure, fix the smallest thing |
| **demo-hardening** | feature freeze | replay cache, approvals, reset, fallbacks, `DEMO_SCRIPT.md`, backup video |
| **demo-check** | after merges, before rehearsal | click the path, reject/approve/rerun, reset, offline; verdict |
| **privacy-check** | before sharing or presenting | secrets, PII at cloud boundaries, unsafe tools, unsupported claims |
| **epic-pitch-deck** | T−40 | animated single-file HTML deck with a labeled mock demo |
| **pitch-rehearsal** | T−30 | timed 3-minute script, rubric score, five hardest questions |
| **submission-pack** | T−20 | README for judges, one-liner, blurb, video, links, repo hygiene |

## Maintain

`.claude/skills/` is the source. `.agents/skills/` is a committed copy including
references, templates and scripts (text files normalized to LF, so Windows
editors cannot cause drift). Plain files, no symlinks.

```powershell
py scripts/sync_skills.py            # Windows (python3 on macOS/Linux)
py scripts/sync_skills.py --check    # what CI runs
py -m unittest discover -s scripts
```

The script uses only the standard library. It validates frontmatter, folder
names and resource references, then copies changed files. `--check` writes
nothing and fails on drift; GitHub Actions runs it on every push. Unexpected
target files are reported, never deleted. When removing a source skill, remove
its copy too. In Claude Code a PostToolUse hook runs the sync automatically
after any edit under `.claude/skills/`.

Skill authoring rules: frontmatter `name` equals the folder name; the
`description` is what the agent matches on, so it names the trigger phrases
and the moment; resources referenced as `references/x.md` must exist; no
machine paths, no secrets, no generated output in skill folders.
