---
name: epic-pitch-deck
description: Build jaw-dropping, animated HTML slide presentations with a built-in interactive product demo — one self-contained file, no build step, works offline on any projector. Use this whenever the user wants a presentation, pitch, deck, slides, keynote, demo-day or hackathon pitch, product launch or "show off our app" page, especially for a webshop, e-commerce or other app with a user flow to demo. Trigger even if they don't say "HTML" or "animated", e.g. "make slides for our app", "we need to present tomorrow", "add a demo slide", "make the deck more epic".
---

# Epic Pitch Deck

Build a presentation that makes a room lean forward: a single `index.html` with cinematic motion, a strong story and a live, clickable product demo that can't crash on stage.

You start from a working engine (`assets/deck-template.html`): 1920×1080 scaled stage, slide transitions, entrance choreography, build steps, counters, split-text, a presenter-notes window, and a mock webshop with a scripted "autopilot" tour. Your job is the story, the design and the choreography. Don't rebuild the plumbing.

## Why it's built this way

- **One file, no dependencies.** Hackathon venues and conference rooms have bad wifi and random laptops. The deck must open by double-clicking, with no server, CDN or npm. Google Fonts is the only network request, and it falls back to system fonts.
- **A mock demo, not the real app.** A live demo of a half-finished app is the #1 way pitches die. The mock shows the *intended* happy path, runs identically every time, and still clicks for real if a judge wants to try it. Autopilot (`A`) means the presenter can talk while the demo runs itself.
- **A fixed 1920×1080 stage.** Design in pixels once and it scales to any screen, so the laptop preview matches the projector.

## Workflow

### 1. Gather the story (briefly)

You need: product name, one-line promise, audience (judges / investors / class), time limit, the problem, 3 key features, the demo's happy path, team, and the ask/close. **Look before asking**: if the repo contains the app, read its README, routes, product data, colors and logo, and pull real names and flows from there. Ask the user only for what you can't find, in one short batch. Fill any remaining gaps with clearly marked placeholders rather than stalling.

### 2. Outline the arc

A pitch is a story, not a feature list. The default arc for a 3–5 min pitch (≈1 slide per 20–30 s):

| # | Slide | Job | Signature move |
|---|---|---|---|
| 1 | Title | Name + promise | split-text logo reveal |
| 2 | Hook | One shocking number or question | giant counter, nothing else |
| 3 | Problem | Make it hurt, 3 pains max | stagger-flipped cards |
| 4 | Solution | The reveal | blur-in gradient headline, a build step |
| 5 | **Demo** | Prove it | autopilot tour in a browser frame |
| 6 | How it works / tech | Credibility | self-drawing flow line |
| 7 | Impact / market | Why it matters | counters |
| 8 | Business model / roadmap (optional) | | timeline build steps |
| 9 | Team (optional) | | pop-in avatars |
| 10 | Close | Ask + repeat promise | split-text "Thank you", shine text |

Show the user the outline (titles + one line each) before building if the content is uncertain. If they gave you everything, just build.

### 3. Build from the template

Copy `assets/deck-template.html` to the target (default: `presentation/index.html` in the project) and replace its content. Keep the engine `<script>` and the CSS component library intact. Edit the slides, the tokens and the demo data.

Engine vocabulary (full reference and more effects: `references/animation-recipes.md`):

- `<section class="slide" data-title="…" data-hue="265" data-transition="zoom|slide|rise|flip|fade">`: add `center` for centered layouts. `data-hue` recolors the whole ambient background per slide, which is a cheap way to give each act its own mood.
- `data-anim="up|down|left|right|zoom|pop|blur|flip|fade"` + `data-delay="ms"`: entrance animations on slide enter.
- `data-stagger="120"` on a parent: children cascade in.
- `data-step="1"`: revealed on the next key press (build steps).
- `data-split`: per-letter cascade (plain text only; don't nest markup inside it or put `.grad` on it).
- `data-count="42" data-suffix="%" data-decimals="1" data-prefix="€"`: animated counter.
- `data-tilt`: 3D hover tilt + spotlight (use on cards).
- `<svg class="draw">` with `pathLength="1"` on paths: self-drawing lines.
- `<aside class="notes">`: presenter notes, shown in the `N` window with a timer.
- Classes: `.mega/h1/h2/h3/.lead/.kicker`, `.grad` (gradient text), `.shine` (animated sheen), `.chip`, `.card`, `.row`, `.stat .num/.label`, `.float`.

### 4. Design: commit to a direction

Pick ONE visual concept that fits the product and apply it everywhere. Examples: "midnight luxury" (near-black, gold hue, serif display), "candy pop" (bright hues, rounded, bouncy `pop` easing), "brutalist tech" (mono font, hard cuts, `fade` transitions), or the template's default "aurora glass". Change the `:root` tokens (`--bg`, `--display`, `--body`, base `--hue`) and the Google Fonts link. If the app has a brand color, convert it to a hue and use that as the base.

Rules that keep it premium rather than a PowerPoint with effects:
- **One idea per slide.** A headline of ≤ 8 words. If you need a paragraph, you need two slides.
- **Huge type.** On a 1920 stage: headlines 100–230px, body ≥ 30px. The back row must read it.
- **Generous emptiness.** Keep the 120/160px slide padding. Space reads as confidence.
- **Contrast of scale.** One giant element and small supporting text beats five medium things.
- **Real content only.** No lorem ipsum. Any number you invent is a placeholder: mark it in the slide's notes (`PLACEHOLDER — verify`) and tell the user.

### 5. Choreograph the motion

Animation should direct the eye in reading order, not decorate. For each slide, decide what the audience looks at first, second and third, and stagger in that order (kicker → headline → support → details, ~100–200ms apart). Then:

- **Budget the wow.** Give 2–3 slides a signature moment (title, hook, demo, close). Keep the rest calmer, so the contrast makes the big moments land.
- **Vary transitions by act, not by slide.** Use e.g. `zoom` for the intro, `rise` for data, `flip` for the reveal and `slide` into the demo. Random variety feels cheap.
- **Match easing to personality.** Expo-out (`--ease`) feels premium. Overshoot (`pop`) feels playful. Keep entrance durations between 0.6 and 1.2s. Anything longer makes the presenter wait.
- **Use build steps for talking points.** Anything the presenter explains one by one should be `data-step`, so the audience never reads ahead.
- `prefers-reduced-motion` is handled by the engine, so don't fight it.

### 6. Build the demo

Read `references/demo-mock.md` before touching the demo. In short: model the mock on the real app's screens, use realistic product data (names, prices in the right currency, nice gradient or emoji "photos" so nothing depends on image files), and script `tour()` to show the core value in **≤ 20 seconds**, one caption step per beat. For a non-webshop app, keep the frame and the autopilot helpers (`moveTo`, `click`, `type`, `setCap`) and replace the shop views.

### 7. Verify — don't hand over an unchecked deck

Run both checks from the skill directory (the scripts need Chrome or Edge; Python may be `py` on Windows):

```bash
node scripts/smoke_test.mjs <deck.html>             # per-slide overflow + JS errors, then watches the autopilot run
python scripts/screenshot_slides.py <deck.html> <out_dir>   # PNG of each slide's final state
```

Then **look at every screenshot** yourself (Read the PNGs). Check for overflow, collisions, unreadable contrast, orphaned words in headlines, empty-looking slides and emoji that render as boxes. `smoke_test` must end with "All clear", and the autopilot log must reach its final caption step. If the Claude-in-Chrome browser tools are available, also open the deck and step through it with the keyboard to see the motion. Screenshots only show end states.

Headless Chrome throttles CSS animations under `--virtual-time-budget`, which is why the screenshots use `?static` (final state, motion disabled) and the tour check uses real time over DevTools.

### 8. Hand over

Tell the user where the file is and give them the presenter cheat-sheet:

```
→ / Space / PageDown  next (clickers work)     ← / PageUp  back
F  fullscreen      N  presenter notes + timer (separate window)
A  demo autopilot  R  reset demo               12 + Enter  jump to slide 12
?static in URL = no motion (PDF export via Ctrl+P)   ?tour = autopilot starts itself
```

List every placeholder they still need to fill in (numbers, team names, contact info). Suggest a rehearsal: run the whole deck once with `N` open and check the timer against their slot.

## Iterating on "make it more epic"

When the user wants more wow, don't just add more motion everywhere. Pick from `references/animation-recipes.md` → "Signature moments": a scroll-scrubbed product reveal, a particle burst on the hook number, a typewriter headline, a 3D device mockup of the demo, a marquee of logos or testimonials, a spotlight cursor. Add one to a slide that's currently flat, and re-verify.
