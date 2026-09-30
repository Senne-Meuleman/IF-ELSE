---
name: theme-kbc
description: KBC-track visual theme for the hackathon demo app (Streamlit) and the HTML pitch deck - white and blue, calm, secure, with built-in transparency components ("Why am I seeing this?", Approve/Reject card, discreet lock badge), subtle motion and a ?lite=1 no-animation fallback. Use when the team is on the KBC track and says "make it look like KBC", "theme the app", "style the deck", "brand colours", or before /demo-hardening and /epic-pitch-deck on the KBC track.
---

# Theme: KBC track (white, blue, calm, secure)

Inspired by the KBC look, **not** the KBC brand. No logo or brand mark: write the
product name as plain text (e.g. "Kate-style assistant · prototype"). Sources,
verified vs estimated values: `research.md`.

## Files
| File | Where it goes |
|---|---|
| `assets/theme.css` | Streamlit (injected) and any HTML page. All classes start with `th-`. |
| `assets/.streamlit/config.toml` | Copy to `<app>/.streamlit/config.toml`. |
| `assets/deck.css` | Paste into the deck `<style>` **after** the template's CSS (see `/epic-pitch-deck`). |

## Palette (CSS variables)
```css
--th-brand:        #00AEEF; /* verified on kbc.be CSS. Decoration only: fails AA as text on white */
--th-primary:      #006A9E; /* estimated darker cerulean: buttons, links (~5.9:1 on white) */
--th-ink:          #0D2A50; /* seen on kbc.be homepage: headings, body text (14:1) */
--th-muted:        #4A5B70; /* estimated: secondary text (6.9:1) */
--th-bg:           #FFFFFF;
--th-surface:      #F2F8FC; /* estimated pale blue cards */
--th-line:         #D3E3EE; /* estimated borders */
--th-success:      #80C342; /* verified on kbc.be CSS. Fill only; text uses --th-success-ink */
--th-success-ink:  #2E6B12; /* estimated */
--th-danger:       #B3261E; /* estimated */
```
Rule: blue text is always `--th-primary` or `--th-ink`, never `--th-brand`.

## Typography
`"Museo Sans", "MuseoSans", "Segoe UI", system-ui, sans-serif`. KBC's site uses
MuseoSans (licensed; not bundled). Offline the stack falls back to Segoe UI /
system fonts, so nothing is downloaded. Projector sizes: body 18px min, table
16px min, headline metric 44px+, weights 400/600/700 only.

## Shape, depth, icons
- Radius: `5px` controls and cards (seen in KBC CSS), `30px` pills for buttons and badges.
- Shadows: one soft level, `0 4px 16px rgb(13 42 80 / .08)`. No glow, no neon.
- Icons: inline SVG line icons, 1.75px stroke, `currentColor`. One lock icon
  only, next to the security badge. No emoji in the UI chrome.

## Components (in `theme.css`)
- `.th-card`: white card, 1px line, soft shadow. `.th-card--surface` for pale blue.
- `.th-metric`: headline number (`.th-metric__value` + `.th-metric__label`).
- `.th-btn`, `.th-btn--primary`, `.th-btn--ghost`, `.th-btn--danger`: pill buttons, 44px min height.
- `.th-table`: 16px, zebra rows in `--th-surface`, right-aligned `.num` columns.
- `.th-secure`: discreet badge "🔒 Data stays masked · you approve every action" (SVG lock, see snippet).
- `.th-why`: `<details>` "Why am I seeing this?" with the reason, the data used and the source.
- `.th-approval`: Approve/Reject card with what will happen, the amount and the account (masked).

## When and how to use
- KBC track only. Apply once in the entry point, before any tab renders:
```python
from pathlib import Path
import streamlit as st
css = Path("theme/theme.css").read_text(encoding="utf-8")   # copied from assets/
if st.query_params.get("lite") == "1":
    css += "*,*::before,*::after{animation:none!important;transition:none!important}"
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
```
- Transparency on every AI result: a `.th-why` block right under it, e.g.
```python
st.markdown("""<details class="th-why"><summary>Why am I seeing this?</summary>
<p>The payee name differs from the IBAN holder (Verification of Payee). Data used: last 3 transfers. Nothing was sent.</p></details>""", unsafe_allow_html=True)
```
- Approval: `.th-approval` is the look; the rule stays in code (`/demo-step`):
  the action runs only in the Approve button's branch. Kate "never acts without
  explicit customer approval" (see `/be-domain`).
- Lock badge, once per screen, top right:
```html
<span class="th-secure"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.75"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="1.75"/></svg>Data masked · you approve every action</span>
```
  Only claim what the code does (`/privacy-check`).
- Deck: paste `deck.css` after the template CSS. It turns the dark template into
  white and blue and adds `?lite=1`.

## Motion rules
- Only `opacity` and `transform`, 160-280 ms, `ease-out`. Allowed: `.th-fade-in`,
  `.th-slide-up` (8px), hover lift of 1px. No particles, video, big images or libraries.
- `prefers-reduced-motion: reduce` makes all motion instant (in `theme.css`).
- Fallback: `?lite=1` (Streamlit snippet above; deck: `deck.css` script) or class
  `th-lite` on `<html>`/`<body>` disables every animation.
- Final state is the default state: if an animation never runs, content is
  still visible. Nothing waits on an animation.
