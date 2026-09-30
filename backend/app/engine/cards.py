"""Card generators. Each proposes cards; none of them rank.

Every card carries plain-English evidence. Comparison cards list coverage differences honestly and
never claim the competitor's policy terms. KBC prices are illustrative placeholders.
"""
from __future__ import annotations

import datetime as dt
import re
import statistics
from collections import defaultdict

from ..schemas import Card, Cta, Customer, Features, Stage, Transaction
from .features import fmt_date, fmt_eur

# ---- tuning knobs -----------------------------------------------------------------
from .features import FIXED_PRICE_CATEGORIES, VAT_DUE_DAY  # noqa: E402  (20th of the month after quarter end)
VAT_RESERVE_RATE = 0.21
SOON_DAYS = 14
URGENT_DAYS = 3
RUNWAY_MAX_DAYS = 21
SQUEEZE_MIN_CHANGE = 0.5
DUPLICATE_WINDOW_HOURS = 48
DUPLICATE_LOOKBACK_DAYS = 14
PRICE_INCREASE_LOOKBACK_DAYS = 60
LIFE_EVENT_LOOKBACK_DAYS = 45
IDLE_CASH_MIN_EUR = 2000
IDLE_CASH_MONTHS_LOOKBACK = 4
INSURANCE_KBC_DISCOUNT = 0.27          # illustrative: "same coverage at KBC" ≈ 27 % cheaper
INSURANCE_WINDOW_DAYS = 45             # show the renewal card from 45 days before renewal
SCAM_MIN_AGE = 60                      # below this the card is noise, not protection
SCAM_CONFIDENCE_BASE = 0.5
SCAM_CONFIDENCE_SENIOR = 0.75
SCAM_SENIOR_AGE = 65
KBC_NAMES = ("kbc", "cbc")


def _slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:40] or "x"


def stage_for(due_date: dt.date | None, as_of: dt.date) -> Stage | None:
    """Lifecycle stage; None means expired (don't show)."""
    if due_date is None:
        return "info"
    days = (due_date - as_of).days
    if days < 0:
        return None
    if days <= URGENT_DAYS:
        return "urgent"
    if days <= SOON_DAYS:
        return "soon"
    return "early"


def _days_phrase(due: dt.date, as_of: dt.date) -> str:
    d = (due - as_of).days
    return "today" if d == 0 else ("tomorrow" if d == 1 else f"in {d} days")


def _past(txs: list[Transaction], as_of: dt.date, days: int | None = None) -> list[Transaction]:
    lo = as_of - dt.timedelta(days=days) if days else None
    return [t for t in txs if t.date <= as_of and (lo is None or t.date > lo)]


# ---- generators -------------------------------------------------------------------


def gen_insurance_renewal(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    if "car_insurance" in c.products:
        return []
    out = []
    for r in f.recurring_payments:
        if r.category != "insurance_car" or r.period_days != 365:
            continue
        if any(k in r.counterparty.lower() for k in KBC_NAMES):
            continue
        due = r.next_date
        if (due - as_of).days > INSURANCE_WINDOW_DAYS:
            continue
        stage = stage_for(due, as_of)
        if stage is None:
            continue
        kbc_yearly = round(r.amount_eur * (1 - INSURANCE_KBC_DISCOUNT))
        saving = round(r.amount_eur - kbc_yearly)
        out.append(Card(
            card_key=f"insurance_renewal:{_slug(r.counterparty)}-car",
            card_type="insurance_renewal", family="deadline", stage=stage,
            title=f"Your car insurance renews {_days_phrase(due, as_of)}",
            body=(f"You paid {fmt_eur(r.amount_eur)} to {r.counterparty} last year. Comparable coverage at KBC is "
                  f"estimated at about {fmt_eur(saving / 12)}/month less (illustrative). Here's what differs, "
                  f"compared to what you pay now."),
            eur_impact=saving, due_date=due, confidence=0.85, commercial=True,
            evidence=[f"Yearly payment of {fmt_eur(r.amount_eur)} to {r.counterparty} on {fmt_date(r.last_date)}",
                      f"Renewal expected on {fmt_date(due)} (one year after the last payment)",
                      "No car insurance with KBC"],
            cta=Cta(label="Compare coverage", action="open_compare"),
            details={"comparison": [
                {"item": "Yearly premium", "current": fmt_eur(r.amount_eur), "kbc": f"{fmt_eur(kbc_yearly)} (illustrative)"},
                {"item": "Civil liability (mandatory)", "current": "included", "kbc": "included"},
                {"item": "Legal assistance", "current": "check your policy", "kbc": "included"},
                {"item": "Roadside assistance abroad", "current": "check your policy", "kbc": "optional, +€48/yr"},
                {"item": "Own damage (omnium)", "current": "check your policy", "kbc": "optional"},
            ], "note": "We only know what you pay, not your current policy's terms. Check them before switching."},
        ))
    return out


def gen_vat_reserve(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    if f.vat_due_date is None or f.vat_period_invoice_income_eur <= 0:
        return []
    due = f.vat_due_date
    stage = stage_for(due, as_of)
    if stage is None:
        return []
    reserve = round(f.vat_period_invoice_income_eur * VAT_RESERVE_RATE)
    q_label = f.vat_period_label  # "Q3 2026"
    q_num, q_year = int(q_label[1]), int(q_label.split()[1])
    period_start = dt.date(q_year, (q_num - 1) * 3 + 1, 1)
    invoices = [t for t in _past(txs, as_of) if t.category == "invoice_income" and t.date >= period_start]
    last_vat = [t for t in _past(txs, as_of) if t.category == "vat_payment"]
    ev = [f"{len(invoices)} invoices received since {fmt_date(period_start)}"]
    if last_vat:
        lv = last_vat[-1]
        ev.append(f"Previous VAT payment {fmt_eur(lv.amount)} on {fmt_date(lv.date)}")
    return [Card(
        card_key=f"vat_reserve:{q_year}q{q_num}", card_type="vat_reserve", family="deadline", stage=stage,
        title=f"VAT return due {fmt_date(due)}",
        body=f"Based on {fmt_eur(f.vat_period_invoice_income_eur)} invoiced in {q_label}, set aside about {fmt_eur(reserve)}.",
        eur_impact=reserve, due_date=due, confidence=0.9, commercial=False, evidence=ev,
        cta=Cta(label="Set aside now", action="vat_transfer"),
        details={"quarter": q_label, "rate": VAT_RESERVE_RATE},
    )]


def gen_price_increase(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    out = []
    for r in f.recurring_payments:
        if r.previous_amount_eur is None or r.amount_eur <= r.previous_amount_eur:
            continue
        if r.category not in FIXED_PRICE_CATEGORIES:
            continue
        if (as_of - r.last_date).days > PRICE_INCREASE_LOOKBACK_DAYS:
            continue
        per_year = (r.amount_eur - r.previous_amount_eur) * (12 if r.period_days == 30 else 1)
        out.append(Card(
            card_key=f"price_increase:{_slug(r.counterparty)}", card_type="price_increase", family="anomaly",
            stage="info",
            title=f"{r.counterparty} went from {fmt_eur(r.previous_amount_eur)} to {fmt_eur(r.amount_eur)}",
            body=f"That's {fmt_eur(per_year)} more per year. Still worth it?",
            eur_impact=round(per_year, 2), due_date=None, confidence=0.95, commercial=False,
            evidence=[f"Payment to {r.counterparty} was {fmt_eur(r.previous_amount_eur)} before",
                      f"{fmt_eur(r.amount_eur)} charged on {fmt_date(r.last_date)}"],
            cta=Cta(label="Review subscriptions", action="open_subscriptions"),
        ))
    return out


def gen_duplicate_charge(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    recent = [t for t in _past(txs, as_of, DUPLICATE_LOOKBACK_DAYS) if t.amount < 0]
    groups: dict[tuple[str, float], list[Transaction]] = defaultdict(list)
    for t in recent:
        groups[(t.counterparty, round(t.amount, 2))].append(t)
    out = []
    for (cp, amt), items in groups.items():
        items.sort(key=lambda t: (t.date, t.id))
        for a, b in zip(items, items[1:]):
            if (b.date - a.date).days * 24 <= DUPLICATE_WINDOW_HOURS:
                out.append(Card(
                    card_key=f"duplicate_charge:{_slug(cp)}-{b.date.isoformat()}", card_type="duplicate_charge",
                    family="anomaly", stage="info",
                    title=f"Two identical charges of {fmt_eur(amt)} at {cp}",
                    body=(f"Both on {fmt_date(a.date)}" if a.date == b.date else
                          f"On {fmt_date(a.date)} and {fmt_date(b.date)}") + ". If you only bought once, we can help you get it back.",
                    eur_impact=abs(amt), due_date=None, confidence=0.8, commercial=False,
                    evidence=[f"{fmt_eur(amt)} to {cp} on {fmt_date(a.date)}", f"{fmt_eur(amt)} to {cp} on {fmt_date(b.date)}"],
                    cta=Cta(label="Dispute charge", action="dispute_charge"),
                ))
                break
    return out


def gen_runway(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    if f.runway_days is None or f.runway_days > RUNWAY_MAX_DAYS:
        return []
    zero_day = as_of + dt.timedelta(days=f.runway_days)
    due = zero_day
    stage = stage_for(due, as_of) or "urgent"
    if f.next_income_date and f.next_income_date <= zero_day:
        body = (f"At this pace you'd hit €0 on {fmt_date(zero_day)}, but your next income "
                f"({fmt_eur(f.next_income_eur or 0)}) is expected {fmt_date(f.next_income_date)}. Tight, but OK.")
        conf = 0.6
    else:
        body = f"At this pace you'll be at €0 on {fmt_date(zero_day)}. Let's look at what can wait."
        conf = 0.8
    # projected shortfall by the next income (or over 30 days if unknown), at the current daily burn
    daily_burn = f.balance_eur / f.runway_days if f.runway_days > 0 else 0.0
    horizon = (f.next_income_date - as_of).days if f.next_income_date else 30
    shortfall = max(0.0, daily_burn * max(horizon, 0) - f.balance_eur)
    return [Card(
        card_key=f"runway:{zero_day.isoformat()}", card_type="runway", family="forecast", stage=stage,
        title=f"{fmt_eur(f.balance_eur)} left, about {f.runway_days} days of runway",
        body=body, eur_impact=round(shortfall, 2), due_date=due, confidence=conf, commercial=False,
        evidence=[f"Balance {fmt_eur(f.balance_eur)} on {fmt_date(as_of)}",
                  f"Spending about {fmt_eur(f.monthly_spend_avg_90d)}/month vs income {fmt_eur(f.monthly_income_avg_90d)}/month"],
        cta=Cta(label="Plan the month", action="open_budget"),
    )]


def gen_cashflow_squeeze(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    if f.variable_spend_change_30d < SQUEEZE_MIN_CHANGE:
        return []
    pct = round(f.variable_spend_change_30d * 100)
    top = sorted(f.spend_by_category_30d.items(), key=lambda kv: -kv[1])[:2]
    top_txt = " and ".join(k.replace("_", " ") for k, _ in top) if top else "everyday spending"
    extra = sum(v for _, v in top)
    return [Card(
        card_key=f"cashflow_squeeze:{as_of.strftime('%Y-%m')}", card_type="cashflow_squeeze", family="forecast",
        stage="info",
        title=f"Spending is up {pct}% this month",
        body=f"Mostly {top_txt}. Want a quick plan to end the month comfortably?",
        eur_impact=round(extra, 2), due_date=None, confidence=0.7, commercial=False,
        evidence=[f"Variable spending in the last 30 days is {pct}% above your 3-month average"]
                 + [f"{fmt_eur(v)} on {k.replace('_', ' ')} this month" for k, v in top],
        cta=Cta(label="Talk to an advisor", action="call_advisor"),
    )]


def gen_idle_cash(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    if f.idle_cash_eur < IDLE_CASH_MIN_EUR:
        return []
    idle = round(f.idle_cash_eur / 100) * 100
    return [Card(
        card_key="idle_cash:savings", card_type="idle_cash", family="opportunity", stage="info",
        title=f"About {fmt_eur(idle)} has been sitting idle",
        body=f"That's more than {IDLE_CASH_MONTHS_LOOKBACK} months of spending on your current account. A savings account would earn interest without locking it up.",
        eur_impact=round(idle * 0.02), due_date=None, confidence=0.7, commercial=True,
        evidence=[f"Balance {fmt_eur(f.balance_eur)} vs about {fmt_eur(f.monthly_spend_avg_90d)}/month of spending",
                  "No savings account with KBC"],
        cta=Cta(label="See savings options", action="open_savings"),
        details={"estimated_interest_eur": round(idle * 0.02), "note": "2% p.a. illustrative"},
    )]


_LIFE_EVENT_COPY = {
    "first_salary": ("First salary! 🎉", "Welcome to payday. A 3-step starter plan: a buffer, a budget, and a first savings goal.",
                     "Start the 3-step plan", "open_starter_plan", "milestone"),
    "first_invoice": ("Your first invoice got paid", "Nice. As a freelancer, set aside about 21% for VAT and plan for social contributions.",
                      "Set up a tax reserve", "vat_transfer", "milestone"),
    "baby": ("Congratulations on the new arrival", "Groeipakket is coming in. Want a family budget and a child savings goal?",
             "Set up family budget", "open_family_budget", "milestone"),
    "pension_start": ("Your first pension has arrived", "A calmer rhythm. We can help you keep an eye on bills and stay safe from scams.",
                      "See my monthly overview", "open_pension_overview", "milestone"),
    "moved_house": ("New home, new bills", "Time to check home insurance and update recurring payments.",
                    "Review home setup", "open_home_checklist", "milestone"),
}


def gen_life_event(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    out = []
    for e in f.life_events:
        if 0 <= (as_of - e.date).days <= LIFE_EVENT_LOOKBACK_DAYS and e.type in _LIFE_EVENT_COPY:
            title, body, cta_label, action, _ = _LIFE_EVENT_COPY[e.type]
            out.append(Card(
                card_key=f"life_event:{e.type}-{e.date.isoformat()}", card_type="life_event", family="milestone",
                stage="info", title=title, body=body, eur_impact=0.0, due_date=None, confidence=0.85,
                commercial=False, evidence=[e.evidence], cta=Cta(label=cta_label, action=action),
            ))
    return out


def gen_scam_awareness(f: Features, c: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    if f.age < SCAM_MIN_AGE:
        return []
    senior = f.age >= SCAM_SENIOR_AGE
    return [Card(
        card_key=f"scam_awareness:{as_of.strftime('%Y-%W')}", card_type="scam_awareness", family="protection",
        stage="info",
        title="Scam SMS wave this week",
        body="KBC never asks for your card code, PIN or a payment 'to verify'. When in doubt, hang up and call us.",
        eur_impact=0.0, due_date=None, confidence=SCAM_CONFIDENCE_SENIOR if senior else SCAM_CONFIDENCE_BASE,
        commercial=False,
        evidence=["Phishing reports are up this week (synthetic)"] + (["Customers over 65 are targeted most often"] if senior else []),
        cta=Cta(label="How to spot a scam", action="open_scam_tips"),
    )]


GENERATORS = [
    gen_insurance_renewal, gen_vat_reserve, gen_price_increase, gen_duplicate_charge,
    gen_runway, gen_cashflow_squeeze, gen_idle_cash, gen_life_event, gen_scam_awareness,
]


def generate_cards(features: Features, customer: Customer, txs: list[Transaction], as_of: dt.date) -> list[Card]:
    cards: list[Card] = []
    seen: set[str] = set()
    for g in GENERATORS:
        for card in g(features, customer, txs, as_of):
            if card.card_key in seen:
                continue
            seen.add(card.card_key)
            cards.append(card)
    return cards
