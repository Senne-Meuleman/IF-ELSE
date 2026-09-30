# KBC Adaptive Home

*Persona sets the stage, moments fill it.*

One banking app that **looks and behaves differently depending on the customer's life situation**. Nobody designed
the home screen you see: the system composed it from signals in the customer's own transactions.

- **Adaptive layout** (who you are): a persona mix (student, young professional, young family, freelancer, retiree)
  decides which modules appear, which is the hero, density, contrast and tone.
- **For You feed** (what is happening now): time-bound cards (insurance renewal, VAT reserve, price increase,
  duplicate charge, runway, idle cash, life events, scam awareness) ranked by value to the customer, with a
  lifecycle (early → soon → urgent → expired) and a feed that **ends**.
- **Explainable and controllable**: "Why am I seeing this?" on every card and every section; dismiss, snooze,
  less like this, pin, hide, consent switch.
- **Time travel**: the same customer, recomputed "as of" any date over 8 years. Watch the layout morph.

Built for the Tectonic Hackathon (KBC challenge). **All data is synthetic.** See `docs/DESIGN.md` for the design and
`docs/KBC-QUESTIONS.md` for how this answers KBC's five questions.

## Run it

Backend (Python 3.12):

```bash
cd backend
py -3.12 -m pip install -r requirements.txt        # or: python -m pip install ...
py -3.12 -m synth.generate --n 1000 --seed 42       # builds backend/kbc.db (also runs automatically on first start)
py -3.12 -m uvicorn app.main:app --reload --port 8000
```

Frontend (Node 22):

```bash
cd frontend
npm install
npm run dev            # http://localhost:5173 (proxies /api to :8000)
```

Or build once and let the backend serve it: `npm run build`, then open http://localhost:8000.

Standalone UI without a backend: http://localhost:5173/?mock=1

## Demo logins

Password for all: `demo` (override with `DEMO_PASSWORD` in `.env`).

| Username | Story | What it shows |
|---|---|---|
| `lotte` | 2018 student in Leuven → 2021 first job → 2022 mortgage → 2024 baby → 2026 freelance | **Time travel**: drag the slider and watch the same person pass through every persona |
| `sara` | Freelancer **and** young mother; car insurance renews in 12 days; Netflix price increase | A **blend** nobody designed, the honest insurance comparison |
| `jan` | 71, retiree; pension; a duplicate charge; idle cash | Retiree layout: large, calm, high contrast, scam shield |
| `advisor` | Portfolio view | Persona distribution, card volume, scoring time projected to 2.3M customers |

Regular synthetic customers: `c1` … `c1000`.

## How it works

```
transactions ─► features ─► persona mix ─┬─► layout planner ─► layout spec (JSON) ─┐
                    │                    │                                         ├─► phone renderer
                    └─► card generators ─┴─► ranker (+ feedback, constraints) ─► feed ┘
```

| Module | What it does |
|---|---|
| `backend/synth/` | ~1,000 synthetic customers with injected scenarios + 3 hand-crafted demo customers (8-year histories) |
| `backend/app/engine/features.py` | transactions → features (income pattern, recurring payments, runway, idle cash, life events) |
| `backend/app/engine/persona.py` | features → weighted persona mix with plain-language evidence |
| `backend/app/engine/cards.py` | 9 card generators, each with evidence, impact, lifecycle stage |
| `backend/app/engine/ranker.py` | `persona_fit × (urgency, impact, confidence, novelty) × fatigue`, then hard constraints |
| `backend/app/engine/layout.py` | component registry + deterministic planner → validated layout spec |
| `backend/app/main.py` | FastAPI: session auth, `/api/me/*` from session only, feedback, prefs, consent, advisor overview |
| `frontend/` | React + Vite + Framer Motion: control panel, phone frame, registry renderer, animated morphs |

Tests: `cd backend && py -3.12 -m pytest` (90 tests: synth, features, persona, cards, ranker, layout, pipeline, API incl. IDOR).

Offline evaluation against the injected ground truth: `cd backend && py -3.12 -m scripts.evaluate`

| Metric (1,000 synthetic customers, seed 42) | Value |
|---|---|
| persona recall / dominant-persona precision | 0.94 / 1.00 |
| feed precision@5 / recall vs injected events | 0.66 / 0.86 |
| scoring time per customer (laptop, single core) | ≈ 3 ms |

Remaining misses are mostly by design: renewals more than 45 days out are not shown yet, and a price increase that
has not been charged yet cannot be detected.

## Security (Aikido)

- HMAC-signed `HttpOnly` `SameSite=Lax` session cookie (8h); PBKDF2-SHA256 200k-iteration password hashes;
  login rate limit per username and per IP.
- Customer endpoints take the customer from the session only: no customer ids in customer URLs (no IDOR).
- Every input is a Pydantic model with patterns, enums and length limits. SQL uses bound parameters only.
- Security headers + CSP; the frontend renders text nodes only, never HTML.
- Advisor endpoints check the role server-side and write to `audit_log`.
- Secrets only via `.env` (see `.env.example`); `ground_truth` is never returned to customers.

## Scale story

The engine is pure functions per customer, so it is embarrassingly parallel. In production: nightly batch +
event triggers (salary received, due date entering a new stage) recompute and cache each `HomeResponse`; the app
open is a cache read. The advisor overview times scoring the whole synthetic portfolio and extrapolates to 2.3M.

## Demo script (< 3 min)

1. Log in as `lotte`, turn on **Explain mode**, drag the time slider from 2018 to 2026: runway hero as a student
   (with a Spotify price bump and a duplicate Alma charge), "First salary!" milestone, "New home, new bills",
   family budget with Groeipakket, first invoice → VAT reserve, and finally the tax-reserve hero as a freelancer.
2. Switch to `sara`: a 59 % freelancer / 41 % young family blend nobody designed. Open the car-insurance card,
   tap ⓘ for the evidence and the honest comparison. Move the slider to 10 Oct: the card turns urgent.
3. Swipe a card away or choose "less like this": the feed re-ranks. Scroll to "✓ You're all caught up".
4. Switch to `jan`: large text, high contrast, pension hero, scam shield, duplicate charge, idle cash.
5. Log in as `advisor` and call `GET /api/advisor/overview` for the scale numbers.

## Not done / honest limitations

- Rules, not ML: persona scoring and ranking are transparent rule-based models by design; the contracts allow
  swapping in trained models.
- LLM copywriting (Gemini) and voice (ElevenLabs) are designed (see `docs/DESIGN.md` §6.7) but not wired in;
  everything works with deterministic templates.
- Offers and prices in comparison cards are illustrative placeholders, not KBC products.
- English only. Synthetic data only.
