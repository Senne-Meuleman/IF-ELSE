---
name: theme-sdworx
description: SD Worx-track visual theme for the hackathon demo app (Streamlit) and the HTML pitch deck - human, trustworthy and clear for HR and payroll (white, light grey, SD Worx blue, deep navy, one warm accent, Inter), with the same transparency components ("Why am I seeing this?", Approve/Reject card, lock badge), subtle motion and a ?lite=1 no-animation fallback. Use when the team is on the SD Worx track and says "make it look like SD Worx", "theme the app", "style the deck", "brand colours", or before /demo-hardening and /epic-pitch-deck on the SD Worx track.
---

# Theme: SD Worx track (human, trustworthy, clear)

Based on SD Worx's public "Ignite" design-system CSS, **not** its brand. No logo
and no three-stripe mark: write the product name as plain text (e.g. "Payroll
co-pilot · prototype"). Sources, verified vs estimated values: `research.md`.

Look and feel: lots of white and light grey, SD Worx blue for actions only,
deep navy headings, one warm accent used sparingly (a person, a highlight).
Plain words, short sentences, people before numbers ("Sarah's payslip", not
"record 4711"). Brand line: "from complexity to confidence".

## Files
| File | Where it goes |
|---|---|
| `assets/theme.css` | Streamlit (injected) and any HTML page. All classes start with `th-`. |
| `assets/.streamlit/config.toml` | Copy to `<app>/.streamlit/config.toml`. |
| `assets/deck.css` | Paste into the deck `<style>` **after** the template's CSS (see `/epic-pitch-deck`). |

## Palette (CSS variables)
```css
--th-primary:        #006DD8; /* verified Ignite: buttons, links (5.0:1 on white) */
--th-primary-hover:  #005BBF; /* verified Ignite text-primary (6.4:1) */
--th-heading:        #000D3A; /* verified Ignite primary-strong: headings */
--th-ink:            #212223; /* verified Ignite: body text */
--th-muted:          #444547; /* verified Ignite: secondary text (9.7:1) */
--th-bg:             #FFFFFF;
--th-surface:        #F4F5F6; /* verified Ignite: grey panels */
--th-primary-subtle: #EFFAFF; /* verified Ignite: info / "why" blocks */
--th-line:           #D9DBDD; /* verified Ignite: borders */
--th-brand:          #0087F3; /* verified Ignite (dark-mode hover): focus ring, decoration */
--th-warm:           #DA3300; /* verified Ignite accent-0: max one use per screen */
--th-success:        #1E8E3E; /* estimated */
--th-danger:         #C42600; /* Ignite accent-0 pressed, used as danger: estimated role */
```
The logo red `#F1002F` and yellow `#FFBE00` come from third-party sources only.
They are not used: the rule there is "logo only".

## Typography
`Inter, "Segoe UI", system-ui, sans-serif`. SD Worx's site uses Inter for body text
and "SD Worx Display" for headings (proprietary, not bundled). Nothing is downloaded,
so it works offline (Segoe UI if Inter isn't installed). Projector sizes: body 18px
min, table 16px min, headline metric 44px+, weights 400/600/700.

## Shape, depth, icons
- Radius: `4px` on buttons and inputs (the Ignite value), `8px` on cards (estimated).
- Shadows: one soft level, `0 4px 16px rgb(0 13 58 / .08)`.
- Icons: inline SVG line icons, 1.75px stroke, `currentColor`, people icons welcome.
  One lock icon only, in the security badge.

## Components (in `theme.css`, same classes as theme-kbc)
`.th-card`, `.th-card--surface`, `.th-metric`, `.th-btn(--primary|--ghost|--danger)`,
`.th-table` (+ `.num`), `.th-secure`, `.th-why`, `.th-approval`,
`.th-status--approved|--rejected`, `.th-fade-in`, `.th-slide-up`. The markup is
the same as in `theme-kbc/SKILL.md`, so a screen can switch tracks by swapping the CSS file.

## When and how to use
- SD Worx track only. Inject once in the entry point:
```python
from pathlib import Path
import streamlit as st
css = Path("theme/theme.css").read_text(encoding="utf-8")   # copied from assets/
if st.query_params.get("lite") == "1":
    css += "*,*::before,*::after{animation:none!important;transition:none!important}"
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
```
- Put a `.th-why` under every AI result: what the agent looked at (payslip, CAO / paritair comité),
  which rule it used (cite it, `/be-domain`) and what it did **not** do.
- `.th-approval` before any payroll change or employee message. SD Worx says
  "humans supervise payroll agents": the Approve branch in code is the only
  place the action runs (`/demo-step`). Show the payroll consultant's name on the card.
- Lock badge text: "Personal data masked · a payroll expert approves". Only
  claim what the code does (`/privacy-check`).
- Deck: paste `deck.css` after the template CSS, plus the `?lite=1` script it names.

## Motion rules
- Only `opacity` and `transform`, 160-280 ms, `ease-out`. No particles, video,
  big images or libraries.
- `prefers-reduced-motion: reduce` makes all motion instant.
- Fallback: `?lite=1` or class `th-lite` disables every animation.
- Final state is the default state: nothing is hidden if an animation fails,
  and nothing waits on an animation.
