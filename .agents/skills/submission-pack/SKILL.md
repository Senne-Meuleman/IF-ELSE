---
name: submission-pack
description: Produce everything the hackathon submission needs in the last 20 minutes - a judge-facing README, the one-liner and 100-word blurb, screenshots, the backup video and deck links, team and track info, and a repo hygiene pass (no secrets, only synthetic data, the app starts from a fresh clone). Use when the team says "submit", "submission form", "deadline in 20 minutes", "write the README for the judges", "what do we hand in".
---

# Submission pack

Judges who didn't see the pitch, or who re-read entries when ranking the top
16, meet the project through the submission. A sloppy README loses a place
that a great demo earned. Do this at **T−20**, in this order, and stop at T−5.

## 1. Find out what the form asks (2 minutes)
Read the submission form or the organizer's message first. Typical fields:
project name, one-liner, description, track (KBC / SD Worx), team members,
repo URL, demo video URL, slides URL, tech used. Produce exactly those, in
that order, ready to paste. If the form isn't known, produce the full set below.

## 2. Texts (paste-ready)
- **One-liner** (≤ 15 words): persona + pain + outcome. *"Payroll consultants approve AI-triaged employee requests in 20 seconds instead of 11 minutes."*
- **Blurb** (≤ 100 words): the problem with a number, what the demo does in 3 sentences, human in the loop, the impact number with its assumption, what's next (pilot). No adjectives, no "revolutionary".
- **Tech line**: name the partners you actually used (Gemini, ElevenLabs, Cursor) and the honest privacy claim from `/privacy-check`.
- **Team**: names, roles, who to contact.
Check every number against `PLAN.md` / `/impact-calc`; check every legal or sponsor claim against `/be-domain`.

## 3. README.md for judges (replace the prep README's top section)
```
# <Product name>: <one-liner>
Track: KBC | SD Worx · Team IF-ELSE: <names>
## The problem            2–3 lines with the number
## What it does           the 3–4 demo steps, one line each; screenshot per step
## Human in the loop      one paragraph: what is proposed, who approves, what never happens automatically
## Impact                 the headline number + the assumptions table
## Run it                 uv sync · copy .env.example to .env · uv run streamlit run app.py · DEMO_CACHE=replay works offline
## What's real / mocked   honest list
## Next steps             pilot idea for the sponsor
Links: video · slides
```
Screenshots: 3–4 PNGs of the happy path in `docs/`, taken from the app at
projector zoom. Reference them in the README.

## 4. Repo hygiene (5 minutes)
- `git status` clean; `git ls-files | findstr /i "\.env"` (or grep) shows only `.env.example`.
- No real personal data: only files from the synthetic generator. Spot-check names and IBANs.
- The app starts from a fresh clone: `.env.example` complete, dependency file committed, `data/` committed (including `data/demo_cache/` so replay works for judges).
- Remove dead tabs, debug prints, "TODO" text visible in the UI, "Team Demo" placeholders.
- Tag the submitted commit: `git tag submission-r1` and push tags.

## 5. Links
- Backup video (60–90 s, recorded by `/demo-hardening`) uploaded somewhere that needs no login (unlisted YouTube or Drive with link sharing). Test the link on a phone.
- Deck: `presentation/index.html` in the repo plus a PDF export (`?static` + Ctrl+P) for the form.

## Output
The paste-ready texts, the README diff, the screenshot list, the tag and the
two links, followed by a 6-line checklist with what is done and what the human
still has to click.
