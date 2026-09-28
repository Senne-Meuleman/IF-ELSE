# Animation recipes

Drop-in effects that plug into the template's engine. Every recipe uses the same hooks:

- CSS: style the resting state under `.slide:not(.active) …` and the final state under `.slide.active …`, so it replays each time the slide is entered.
- JS: listen for `document.addEventListener('slidechange', e => { e.detail.slide, e.detail.index })` to start or stop scripted effects when a slide becomes active.
- Respect `STATIC` (the `?static` flag): show the final state immediately, which keeps screenshots and PDF export correct.

## Contents
1. Engine attribute cheat-sheet
2. Timing and easing guide
3. Signature moments: kinetic word swap, scramble text, typewriter, particle burst, clip-path reveal, 3D device mockup, logo marquee, spotlight cursor, timeline build, glowing border card, comparison slider
4. Pitfalls

---

## 1. Engine attribute cheat-sheet

| Attribute | Values | Notes |
|---|---|---|
| `data-transition` (slide) | `zoom` (default), `slide`, `rise`, `flip`, `fade` | Change per act, not per slide |
| `data-hue` (slide) | 0–360 | Ambient background + `--accent` hue; tweens smoothly |
| `data-anim` | `up down left right zoom pop blur flip fade` | Entrance on slide enter |
| `data-delay` | ms | Adds to the 250ms base delay |
| `data-stagger` (parent) | ms | Sets children's delay to `i * ms` (+ the child's own `data-delay`) |
| `data-step` | 1, 2, 3… | Hidden until the Nth "next" press; `data-anim` sets its entrance direction |
| `data-split` | — | Per-letter cascade. Plain text only |
| `data-count` | number | + `data-prefix`, `data-suffix`, `data-decimals` |
| `data-tilt` | — | 3D hover tilt + radial highlight (`.card` has the highlight built in) |
| `svg.draw` | — | Children with `pathLength="1"` draw themselves in |

Custom entrance: define a new `[data-anim="name"] { --from: <transform>; --blur: blur(…) }`.

## 2. Timing and easing guide

- Entrances: 600–1200ms, `--ease` (expo-out). Exits: faster than entrances (the engine does this).
- Stagger siblings by 80–150ms. Stagger headline → body by 150–300ms.
- The first element should move within ~300ms of the slide change. Longer feels laggy.
- Overshoot (`cubic-bezier(.34,1.56,.64,1)`) only for small playful things: icons, badges, avatars.
- Ambient loops (float, shine, drift) should be slow (5–30s) so they never compete with content.

## 3. Signature moments

### Kinetic word swap ("Shopping made **faster / simpler / magical**")
```html
<h1>Shopping made <span class="swap grad" data-words="faster,simpler,magical">faster</span></h1>
```
```css
.swap { display: inline-block; transition: opacity .35s, transform .35s var(--ease), filter .35s; }
.swap.out { opacity: 0; transform: translateY(-.4em); filter: blur(8px); }
```
```js
document.querySelectorAll('.swap').forEach(el => {
  const words = el.dataset.words.split(','); let i = 0;
  setInterval(() => {
    if (!el.closest('.slide').classList.contains('active') || STATIC) return;
    el.classList.add('out');
    setTimeout(() => { el.textContent = words[i = (i + 1) % words.length]; el.classList.remove('out'); }, 350);
  }, 1800);
});
```
Note: `.grad` on an inline-block works; `.grad` on `data-split` characters does not.

### Scramble / decode text (techy reveal)
```js
function scramble(el, dur = 1200) {
  const final = el.dataset.text ||= el.textContent, chars = '!<>-_\\/[]{}=+*^?#ABCDEF0123456789';
  if (STATIC) return el.textContent = final;
  const t0 = performance.now();
  (function f(now) {
    const p = Math.min(1, (now - t0) / dur), n = Math.floor(p * final.length);
    el.textContent = final.slice(0, n) + [...final.slice(n)].map(c => c === ' ' ? ' ' : chars[Math.random() * chars.length | 0]).join('');
    if (p < 1) requestAnimationFrame(f);
  })(t0);
}
document.addEventListener('slidechange', e => e.detail.slide.querySelectorAll('[data-scramble]').forEach(el => setTimeout(() => scramble(el), 300)));
```

### Typewriter with caret
```css
.type::after { content: '▍'; animation: blink 1s steps(1) infinite; color: var(--accent); }
@keyframes blink { 50% { opacity: 0; } }
```
```js
async function typewrite(el, speed = 45) {
  const text = el.dataset.text ||= el.textContent; el.textContent = '';
  if (STATIC) return el.textContent = text;
  for (const ch of text) { el.textContent += ch; await new Promise(r => setTimeout(r, speed + Math.random() * 40)); }
}
document.addEventListener('slidechange', e => e.detail.slide.querySelectorAll('.type').forEach(el => typewrite(el)));
```

### Particle burst behind a number (the hook slide)
```js
function burst(slide, x = 960, y = 540, n = 80) {
  if (STATIC) return;
  for (let i = 0; i < n; i++) {
    const p = document.createElement('i'), a = Math.random() * Math.PI * 2, d = 200 + Math.random() * 600, s = 4 + Math.random() * 10;
    Object.assign(p.style, { position: 'absolute', left: x + 'px', top: y + 'px', width: s + 'px', height: s + 'px', borderRadius: '50%', background: 'var(--accent)', boxShadow: '0 0 12px var(--accent)', pointerEvents: 'none' });
    slide.appendChild(p);
    p.animate([{ transform: 'translate(0,0) scale(1)', opacity: 1 }, { transform: `translate(${Math.cos(a) * d}px,${Math.sin(a) * d}px) scale(0)`, opacity: 0 }],
      { duration: 1200 + Math.random() * 800, easing: 'cubic-bezier(.1,.8,.3,1)', delay: 1900 }).finished.then(() => p.remove());
  }
}
document.addEventListener('slidechange', e => { if (e.detail.slide.dataset.title === 'Hook') burst(e.detail.slide); });
```
The 1900ms delay lines the burst up with the counter's landing (400ms start + 1800ms count).

### Clip-path reveal (image or screenshot wipes in)
```css
.reveal { clip-path: inset(0 100% 0 0 round 24px); transition: clip-path 1.4s var(--ease-io) calc(var(--d, 0ms) + 300ms); }
.slide.active .reveal { clip-path: inset(0 0 0 0 round 24px); }
```
Variants: `circle(0% at 50% 50%)` → `circle(75% at 50% 50%)` for an iris, or `polygon()` for diagonal wipes.

### 3D device mockup (demo screenshot or mini-shop on a floating phone)
```html
<div class="phone float" data-anim="zoom"><div class="screen"><!-- content or an <img> --></div></div>
```
```css
.phone { width: 420px; height: 860px; border-radius: 64px; padding: 18px; background: linear-gradient(145deg, #2a2838, #0d0c14);
  box-shadow: 0 0 0 2px #3a3850, 0 80px 120px -40px hsl(var(--hue) 80% 40% / .6); transform: perspective(1600px) rotateY(-18deg) rotateX(6deg); }
.phone .screen { width: 100%; height: 100%; border-radius: 48px; overflow: hidden; background: #fff; }
```
Combining with `.float`: the float keyframe overrides `transform`. Wrap the phone in a `.float` div instead of putting both on one element.

### Logo / testimonial marquee
```html
<div class="marquee"><div class="track">…items…</div></div>
```
```css
.marquee { overflow: hidden; mask-image: linear-gradient(90deg, transparent, #000 15%, #000 85%, transparent); }
.marquee .track { display: flex; gap: 80px; width: max-content; animation: marq 30s linear infinite; }
@keyframes marq { to { transform: translateX(-50%); } }
```
Duplicate the items once inside `.track` so the loop is seamless.

### Spotlight cursor (dark slide lit by the mouse)
```css
.spot::before { content: ''; position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(500px circle at var(--sx, 50%) var(--sy, 50%), transparent, rgba(0,0,0,.85)); }
```
```js
addEventListener('pointermove', e => document.querySelectorAll('.spot').forEach(s => {
  const r = s.getBoundingClientRect(); s.style.setProperty('--sx', (e.clientX - r.left) / r.width * 100 + '%'); s.style.setProperty('--sy', (e.clientY - r.top) / r.height * 100 + '%'); }));
```
Only use this if the presenter will actually move the mouse. On a clicker-driven pitch it just looks dark.

### Timeline / roadmap build
Horizontal `svg.draw` line + milestone dots as `data-step` elements with `data-anim="pop"`. Each press reveals the next milestone. Put the line in its own `data-step="1"` wrapper if it should draw on the first press rather than on enter.

### Glowing animated border card
```css
@property --ang { syntax: '<angle>'; inherits: false; initial-value: 0deg; }
.glow { border: 2px solid transparent; background: linear-gradient(var(--bg), var(--bg)) padding-box, conic-gradient(from var(--ang), var(--accent), transparent 30%, var(--accent-2), transparent 70%, var(--accent)) border-box; animation: spinb 4s linear infinite; }
@keyframes spinb { to { --ang: 360deg; } }
```
Use it on the one card that matters (the pricing tier, the key feature) and nowhere else.

### Before/after comparison slider
Two stacked panels. The top one uses `clip-path: inset(0 calc(100% - var(--x)) 0 0)`. Drive `--x` from `pointermove`, or animate it 0→100% on slide enter for clicker use.

## 4. Pitfalls

- **`background-clip: text` + transformed children** (e.g. `.grad` on `data-split`): the characters turn invisible. Put the gradient on a wrapper that doesn't split, or give each `.char` its own gradient.
- **SVG gradients on horizontal/vertical lines** need `gradientUnits="userSpaceOnUse"` with explicit x1/x2. The default bounding box of a zero-height line is empty, so the stroke disappears.
- **Emoji without a variation selector** (🛍, ⌨, ✈) may render as flat text glyphs. Prefer emoji with default emoji presentation, or inline SVG icons.
- **`filter: blur()` on huge elements** is expensive. Keep blurs ≤ 24px and avoid animating blur on full-slide backgrounds.
- **Don't combine `data-anim` with an element's own `transform` animation** (`.float`, tilt). Both write `transform`, so nest them instead.
- **Text in the stage is at 1920 scale.** A 16px font is unreadable when projected, so nothing below ~22px.
