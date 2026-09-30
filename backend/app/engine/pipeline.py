"""build_home(customer, txs, balance_today, prefs, as_of) → HomeResponse.

The only place in the engine that may touch the wall clock (for `generated_at`), and only as a default.
"""
from __future__ import annotations

import datetime as dt

from ..schemas import (Customer, CustomerPublic, HomeResponse, Layout, Milestone, Prefs, Section, Theme,
                       TimelineResponse, Transaction)
from . import cards as cards_mod
from . import persona as persona_mod
from . import ranker
from .features import compute_features

try:  # layout.py is owned by another track; degrade gracefully until it lands
    from .layout import plan_layout as _plan_layout
except ImportError:  # pragma: no cover
    _plan_layout = None


def _fallback_layout(features, persona_mix) -> Layout:
    return Layout(
        version=1,
        theme=Theme(density="comfortable", tone="neutral", contrast="normal"),
        sections=[
            Section(component="BalanceHero", size="hero", props={
                "balance_eur": features.balance_eur, "monthly_income_eur": features.monthly_income_avg_90d,
                "monthly_spend_eur": features.monthly_spend_avg_90d, "trend_30d_eur": 0.0, "sparkline": []}),
            Section(component="ForYouFeed", size="full", props={}),
        ],
        explanations={"BalanceHero": "Default layout (layout planner not available)."},
    )


def customer_public(customer: Customer) -> CustomerPublic:
    return CustomerPublic(first_name=customer.first_name, language=customer.language,
                          consent_personalization=customer.consent_personalization)


def build_home(customer: Customer, txs: list[Transaction], balance_today: float, prefs: Prefs,
               as_of: dt.date, generated_at: dt.datetime | None = None) -> HomeResponse:
    features = compute_features(customer, txs, balance_today, as_of)
    persona_mix = persona_mod.infer_persona_mix(features)
    candidates = cards_mod.generate_cards(features, customer, txs, as_of)
    feed = ranker.rank(candidates, persona_mix, prefs, customer, as_of)
    if _plan_layout is not None:
        layout = _plan_layout(features, persona_mix, prefs, customer, txs, as_of, feed.cards)
    else:
        layout = _fallback_layout(features, persona_mix)
    return HomeResponse(
        as_of=as_of,
        customer=customer_public(customer),
        persona_mix=persona_mix,
        layout=layout,
        feed=feed,
        generated_at=generated_at or dt.datetime.now(dt.timezone.utc),
        llm_copy=False,
    )


_MILESTONE_LABELS = {
    "first_salary": "First salary",
    "first_invoice": "Went freelance",
    "baby": "Baby",
    "pension_start": "Pension",
    "moved_house": "Mortgage",
}


def build_timeline(customer: Customer, txs: list[Transaction], balance_today: float) -> TimelineResponse:
    if not txs:
        today = dt.date(1970, 1, 1)
        return TimelineResponse(min_date=today, max_date=today, milestones=[])
    dates = [t.date for t in txs]
    lo, hi = min(dates), max(dates)
    features = compute_features(customer, txs, balance_today, hi)
    milestones = [Milestone(date=e.date, label=_MILESTONE_LABELS.get(e.type, e.type.replace("_", " ").title()))
                  for e in features.life_events]
    milestones.sort(key=lambda m: m.date)
    return TimelineResponse(min_date=lo, max_date=hi, milestones=milestones)
