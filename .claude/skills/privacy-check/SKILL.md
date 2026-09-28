---
name: privacy-check
description: Review the hackathon app and repo for exposed secrets, customer or employee PII reaching a cloud model or the repo, unsafe agent actions (mutations without approval, prompt injection through emails or documents, model text reaching shell/eval/HTML), and privacy claims the code doesn't support. Use before pushing, before presenting, before the submission, or when the pitch says "GDPR", "local", "PII never leaves", "secure".
---

# Privacy check

Sponsors are a bank and a payroll provider; a judge will ask "where does the
data go?". This is a review with file/line evidence; fix only when asked.

- **Secrets**: `.env` and local credentials ignored and untracked; nothing
  key-shaped in code, notebooks, cache files, screenshots, the deck or the
  video. Scan history when evidence suggests an earlier leak. Report the path
  and the secret type, never the value. Don't rotate or rewrite history without
  authorization.
- **PII at the cloud boundary**: trace customer/employee text through every
  call (ask, extract, agent tool outputs, embeddings, voice, retries,
  fallbacks). Masking must happen before each cloud call and the vault must
  stay local. Regex masking is not anonymization: free text and names slip
  through, so check what actually gets sent.
- **Data in the repo and cache**: synthetic only, with known provenance
  (`data/synth.py`). Replay cache payloads, logs, screenshots and pitch assets
  contain what was sent to the model; read a few.
- **Agent actions**: any mutating tool needs application-enforced approval
  bound to the exact arguments; Reject and reruns never execute. Email and
  document text is data, never instructions: test one injected "approve this"
  line.
- **Dangerous sinks**: model output flowing into shell commands, `eval`,
  `exec`, unsafe deserialization or unescaped HTML (`unsafe_allow_html=True`).
- **Claims vs code**: compare "local only", "PII never leaves", "GDPR
  compliant", "anonymized" with the configuration. Propose the exact wording
  that is true ("personal identifiers are masked before any cloud call; the
  unmasking table stays on the laptop").

## Output
Findings by severity: file:line, what happens, smallest fix. Then the review
scope and what was skipped. No findings is not a certification; say what was
checked. Never upload repository data to an external scanner for this review;
if the team wants an Aikido scan (a tech partner), the human runs it.
