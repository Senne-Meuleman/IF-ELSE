# The demo mock

The demo slide (`<section class="slide" data-demo>`) hosts a fake but fully clickable app inside a browser frame, plus an autopilot that performs the happy path with a fake cursor while caption steps light up on the left.

## Philosophy

- **Demo the promise, not the codebase.** The audience needs to *feel* the core value in 15–20 seconds. Cut login, settings, loading states and edge cases. Keep the one or two moments that make someone say "oh, nice" (instant search, the fly-to-cart, the one-tap pay, the confetti).
- **Look like the real app.** Reuse the real app's name, colors, fonts, product names, prices and copy when they exist (read the project's code, seed data or design files). A mock that matches the real screenshots builds trust. A generic one looks like vaporware.
- **Never depend on the network.** Product "photos" are gradients + emoji or inline SVG. If the user has real product images in the repo, you may reference them with relative paths, but keep them small and check they load from `file://`.
- **Both modes must work.** Autopilot (`A`) for the smooth narrated version. Manual clicking for a judge who says "can I try?". `R` resets to a clean state at any time.

## Anatomy (in the template)

```
PRODUCTS            array of { id, name, price, emoji, a, b }  (a/b = gradient colors)
Shop IIFE
  shell()           renders header (logo, search, cart button) + main + drawer
  home()/renderGrid() banner + product grid, filtered by search query q
  add(id, btn)      cart update + fly(img) ghost animation + badge bump
  openCart()/renderDrawer()   slide-in cart drawer with lines + total
  checkout()        prefilled checkout form + summary + Pay button
  pay(btn)          spinner 1.3s → success view + confetti()
  click delegation  data-add | data-open-cart | data-close-cart | data-checkout | data-pay | data-continue | data-clear
Autopilot helpers
  moveTo(sel, ms)   glide fake cursor to element center (handles stage scaling)
  click(sel)        move + press animation + ripple + real .click()
  type(sel, text)   focus input, type char by char firing 'input' events, blur
  setCap(i)         highlight caption i in #demoSteps, mark earlier ones done
  wait(ms)          abortable sleep; reset() cancels a running tour
  tour()            ← THE SCRIPT: edit this
```

## Adapting it

**Same webshop, different products/brand**: edit `PRODUCTS`, the logo text, banner copy, the URL in `.browser-bar .url`, currency in `money()` (`Intl.NumberFormat` locale + currency), and the checkout's fake customer details (use obviously fake ones: no real people or addresses).

**Webshop with a special feature** (AI stylist, AR try-on, group buying, subscriptions…): add one view function for the feature (for example `stylist()` rendering a chat bubble that "types" a recommendation and then a product card), a `data-` action for it in the click delegation, and a caption step. The feature *is* the pitch, so give it the most screen time in `tour()`.

**Not a webshop at all**: keep the `.browser` frame (or swap it for the `.phone` mockup from `animation-recipes.md`), the autopilot helpers, captions, reset and confetti. Replace `shell/home/renderGrid/...` with the app's own 3–4 views. The pattern stays: `render view → user action via data-attribute → state change → animated feedback`.

## Writing the tour

```js
async function tour() {
  setCap(0); await wait(500);
  await type('[data-search]', 'sneak'); await wait(600);   // show instant search
  setCap(1); await click('[data-add="p1"]'); await wait(900);
  ...
  setCap(N); caps[N].classList.add('done');                  // final step ticked
}
```

- One caption per beat, 3–5 beats. The caption text is what the presenter says, so write it as a benefit ("Find it instantly"), not an action ("Type in search box").
- Pause after every visible payoff (700–1500ms) so the audience registers it. The fly-to-cart needs ~900ms, and the success screen needs ≥ 1.2s before anything else happens.
- Only target elements that exist at that moment. After a re-render, wait for the new view before clicking into it.
- Keep total runtime ≤ 20s. Test it with `node scripts/smoke_test.mjs`, whose log shows each caption step and state change per second.
- `?tour` in the URL auto-starts the tour when the demo slide opens, which is handy for kiosk loops and for the smoke test.

## Feedback animations worth keeping

| Moment | Effect | Why |
|---|---|---|
| Add to cart | product image arcs into the cart icon, badge bounces | makes an abstract state change physical |
| Open cart | drawer slides with expo-out, lines cascade in | spatial continuity |
| Pay | button morphs into a spinner | builds a beat of suspense |
| Success | tick draws itself + confetti | the emotional payoff, so let it breathe |
| Search | cards re-cascade as results filter | shows speed |
