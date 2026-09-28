---
name: pitch-rehearsal
description: Rehearse and critique the 3-minute KBC or SD Worx hackathon pitch against the actual challenge, the demo that exists, and defensible impact assumptions - timed script, rubric score, the five hardest jury questions with grounded answers, and the backup-demo transition. Use before presenting, when someone says "rehearse", "score our pitch", "play the judge", "what will they ask", or to stress-test an idea right after /kickoff.
---

# Pitch rehearsal

Read the challenge brief, `PLAN.md`, `DEMO_SCRIPT.md` and the deck if they
exist. Judge what is there, not what was planned. No code changes unless asked.

## 1. Time it
Write the script as a table: `time | slide or click | what the presenter says (verbatim) | what the audience sees`.
Budget 180 s with 15 s reserve for a UI wait and one recovery line ("while
that loads: this is what the payroll consultant sees every Monday"). If it
runs over, cut a feature before speeding up an explanation the judges need.

## 2. Score with the rubric (1–5 each, with the evidence)
| Criterion | 5 looks like |
|---|---|
| Business value | one persona, one painful moment, a number a finance person can trace |
| Sponsor fit | solves the case in the sponsor's own words; mentions their reality (Kate, multi-agent payroll, PC, Peppol…) |
| Demo | live, 3–4 clicks, visible before/after, nothing typed, nothing explained that isn't on screen |
| Trust | human approval shown, privacy claim true, limitations named, AI Act / GDPR awareness in one line |
| Clarity | a 12-year-old gets the problem in 20 s; one idea per slide; ends with an ask |
Scores are rehearsal judgments, not a prediction of the jury's ranking.

## 3. The five hardest questions
Pick the five this specific demo invites, from: model errors and how the
human catches them, where the data goes (privacy), what happens if the
approver is wrong, the impact arithmetic ("where does 11 minutes come
from?"), why the sponsor couldn't do this with Kate / their platform already,
what it costs to run, what happens for the 30% the AI doesn't handle,
multilingual quality, the legal basis for a rule shown on screen. Give a
two-sentence answer grounded in what exists; where evidence is missing, say
what to admit rather than bluff.

## 4. Honesty check
Which demo actions are live, replayed, or mocked? The narration must not
present a mock as a working integration. Suggest wording ("the approval goes
to a simulated HR system today").

## Output
1. The three highest-value edits feasible in the time left.
2. The timed script.
3. Rubric scores with evidence.
4. The five questions with answers.
5. The backup-demo transition sentence (video or deck mock) if the live app dies.
Use `/impact-calc` for arithmetic and `/be-domain` for any claim that needs a
source. Don't add features or rebuild the deck because the user asked for critique.
