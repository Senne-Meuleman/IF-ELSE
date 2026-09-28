@AGENTS.md

## Claude Code helpers in `.claude/`
Skills (invoke with `/name`):
- `/kickoff`: paste the challenge brief and get the user, pain, pitch skeleton, scope, which tabs to keep, and a team task split
- `/be-domain`: verified Belgian HR/payroll/banking/regulation facts. Load it before stating any law, rate or date.
- `/impact-calc`: € / hours-saved business case with explicit assumptions
- `/demo-hardening`: offline replay cache, approve buttons, reset, seeded inputs. Run it at feature freeze.
- `/challenge-data`: extend `blocks/synth.py` with the tables the brief needs
- `/epic-pitch-deck`: the animated HTML pitch with a mock demo

Subagents: `researcher` (web facts with sources), `demo-tester` (smoke test + clicks through the app), `judge` (scores the idea and pitch, asks hard questions), `security-check` (keys, PII, OWASP basics).

During the build, when several teammates or tasks run in parallel, give each feature its own git worktree or branch and merge often. Run `demo-tester` after every merge.
