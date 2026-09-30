"""KBC Adaptive Home API.

- Customer endpoints derive the customer from the session cookie. No customer IDs in URLs (no IDOR).
- Every body/query is a Pydantic model (schemas.py). `as_of` is clamped to the customer's data range.
- Advisor endpoints check the role server-side and write to audit_log.
- Security headers + CSP on every response.
"""
from __future__ import annotations

import datetime as dt
import os
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import auth, db
from .auth import Principal
from .engine import pipeline
from .engine.persona import dominant
from .schemas import (
    AdvisorOverview, ConsentRequest, FeedbackRequest, HomeResponse, LayoutPrefRequest,
    LoginRequest, LoginResponse, TimelineResponse,
)

HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.abspath(os.path.join(HERE, "..", "..", "frontend", "dist"))
SYNTH_N = int(os.environ.get("SYNTH_N", "1000"))
SYNTH_SEED = int(os.environ.get("SYNTH_SEED", "42"))
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "0") == "1"
PORTFOLIO_SIZE = 2_300_000
# The synthetic dataset's reference "today". Time travel is clamped to [first transaction, DEMO_TODAY].
DEMO_TODAY = dt.date.fromisoformat(os.environ.get("DEMO_TODAY", "2026-09-30"))


def ensure_db() -> None:
    if os.path.exists(db.DB_PATH):
        return
    from synth.generate import build  # lazy: heavy import, only on first start

    build(db.DB_PATH, n=SYNTH_N, seed=SYNTH_SEED)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_db()
    yield


app = FastAPI(title="KBC Adaptive Home", lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; "
        "base-uri 'self'; form-action 'self'"
    )
    return response


# ----------------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------------


def _effective_as_of(conn, customer_id: int, as_of: dt.date | None) -> dt.date:
    """Clamp the requested date to [first transaction, DEMO_TODAY]. Never the future."""
    rng = db.date_range(conn, customer_id)
    if not rng:
        raise HTTPException(status_code=404, detail="No data for customer")
    lo, hi = rng
    hi = max(hi, DEMO_TODAY)
    return hi if as_of is None else min(max(as_of, lo), hi)


def _load_and_build(customer_id: int, as_of: dt.date | None) -> HomeResponse:
    with db.tx() as conn:
        customer = db.get_customer(conn, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        effective = _effective_as_of(conn, customer_id, as_of)
        txs = db.get_transactions(conn, customer_id)
        balance_today = db.get_balance_today(conn, customer_id)
        prefs = db.get_prefs(conn, customer_id)
        home = pipeline.build_home(customer, txs, balance_today, prefs, effective)
        db.touch_visit(conn, customer_id, effective)
    return home


def _as_of_param(as_of: dt.date | None = Query(default=None)) -> dt.date | None:
    return as_of


# ----------------------------------------------------------------------------------
# Auth
# ----------------------------------------------------------------------------------


@app.post("/api/login", response_model=LoginResponse)
def login(body: LoginRequest, request: Request, response: Response) -> LoginResponse:
    ip = request.client.host if request.client else "unknown"
    auth.check_rate_limit(f"u:{body.username}")
    auth.check_rate_limit(f"ip:{ip}")
    with db.tx() as conn:
        row = db.get_user(conn, body.username)
    if not row or not auth.verify_password(body.password, row["password_hash"]):
        auth.record_attempt(f"u:{body.username}")
        auth.record_attempt(f"ip:{ip}")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    auth.set_session_cookie(response, auth.make_session(row["id"], row["role"]), secure=COOKIE_SECURE)
    return LoginResponse(role=row["role"], username=row["username"])


@app.post("/api/logout")
def logout(response: Response) -> dict:
    auth.clear_session_cookie(response)
    return {"ok": True}


@app.get("/api/me/session", response_model=LoginResponse)
def session(user: Principal = Depends(auth.current_user)) -> LoginResponse:
    return LoginResponse(role=user.role, username=user.username)


# ----------------------------------------------------------------------------------
# Customer
# ----------------------------------------------------------------------------------


@app.get("/api/me/home", response_model=HomeResponse)
def me_home(as_of: dt.date | None = Depends(_as_of_param),
            user: Principal = Depends(auth.require_customer)) -> HomeResponse:
    return _load_and_build(user.customer_id, as_of)


@app.get("/api/me/timeline", response_model=TimelineResponse)
def me_timeline(user: Principal = Depends(auth.require_customer)) -> TimelineResponse:
    with db.tx() as conn:
        customer = db.get_customer(conn, user.customer_id)
        txs = db.get_transactions(conn, user.customer_id)
        balance_today = db.get_balance_today(conn, user.customer_id)
    if not customer or not txs:
        raise HTTPException(status_code=404, detail="No data for customer")
    tl = pipeline.build_timeline(customer, txs, balance_today)
    tl.max_date = max(tl.max_date, DEMO_TODAY)
    return tl


@app.post("/api/me/feedback", response_model=HomeResponse)
def me_feedback(body: FeedbackRequest, as_of: dt.date | None = Depends(_as_of_param),
                user: Principal = Depends(auth.require_customer)) -> HomeResponse:
    with db.tx() as conn:
        at = _effective_as_of(conn, user.customer_id, as_of)
        db.add_feedback(conn, user.customer_id, body.card_key, body.card_type, body.decision, at)
    return _load_and_build(user.customer_id, as_of)


@app.post("/api/me/layout-prefs", response_model=HomeResponse)
def me_layout_prefs(body: LayoutPrefRequest, as_of: dt.date | None = Depends(_as_of_param),
                    user: Principal = Depends(auth.require_customer)) -> HomeResponse:
    with db.tx() as conn:
        at = _effective_as_of(conn, user.customer_id, as_of)
        db.set_layout_pref(conn, user.customer_id, body.component, body.state, at)
    return _load_and_build(user.customer_id, as_of)


@app.post("/api/me/consent", response_model=HomeResponse)
def me_consent(body: ConsentRequest, as_of: dt.date | None = Depends(_as_of_param),
               user: Principal = Depends(auth.require_customer)) -> HomeResponse:
    with db.tx() as conn:
        db.set_consent(conn, user.customer_id, body.consent_personalization)
    return _load_and_build(user.customer_id, as_of)


# ----------------------------------------------------------------------------------
# Advisor (stretch): portfolio overview + scale projection
# ----------------------------------------------------------------------------------

_overview_cache: AdvisorOverview | None = None


@app.get("/api/advisor/overview", response_model=AdvisorOverview)
def advisor_overview(user: Principal = Depends(auth.require_advisor)) -> AdvisorOverview:
    global _overview_cache
    with db.tx() as conn:
        db.audit(conn, user.user_id, "advisor.overview", "portfolio")
    if _overview_cache:
        return _overview_cache

    persona_dist: dict[str, int] = {}
    card_volume: dict[str, int] = {}
    eur_total = 0.0
    with db.tx() as conn:
        ids = db.all_customer_ids(conn)
        started = time.perf_counter()
        for cid in ids:
            customer = db.get_customer(conn, cid)
            txs = db.get_transactions(conn, cid)
            if not customer or not txs:
                continue
            balance_today = db.get_balance_today(conn, cid)
            prefs = db.get_prefs(conn, cid)
            home = pipeline.build_home(customer, txs, balance_today, prefs, max(txs[-1].date, DEMO_TODAY))
            dom = dominant(home.persona_mix)
            persona_dist[dom] = persona_dist.get(dom, 0) + 1
            for card in home.feed.cards:
                card_volume[card.card_type] = card_volume.get(card.card_type, 0) + 1
                eur_total += abs(card.eur_impact)
        elapsed_ms = (time.perf_counter() - started) * 1000
    n = max(1, len(ids))
    _overview_cache = AdvisorOverview(
        customers_scored=len(ids),
        scoring_ms=round(elapsed_ms, 1),
        projected_2_3m_seconds=round(elapsed_ms / 1000 / n * PORTFOLIO_SIZE, 1),
        persona_distribution=persona_dist,
        card_volume=card_volume,
        eur_impact_total=round(eur_total, 2),
    )
    return _overview_cache


# ----------------------------------------------------------------------------------
# Static frontend (production build), if present
# ----------------------------------------------------------------------------------

if os.path.isdir(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str):
        candidate = os.path.abspath(os.path.join(FRONTEND_DIST, path))
        if path and candidate.startswith(FRONTEND_DIST) and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
