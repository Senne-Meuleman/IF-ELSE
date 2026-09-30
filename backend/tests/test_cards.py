from __future__ import annotations

import datetime as dt

from app.engine.cards import generate_cards, stage_for
from app.engine.features import compute_features
from app.schemas import CARD_KEY_PATTERN, Card
import re

from tests.test_features import END, TxBuilder, baseline, customer

D = dt.date


def cards_for(c, txs, balance, as_of, types=None) -> list[Card]:
    f = compute_features(c, txs, balance, as_of)
    cards = generate_cards(f, c, txs, as_of)
    return [k for k in cards if types is None or k.card_type in types]


def sara_like():
    b = TxBuilder()
    baseline(b, D(2024, 1, 1), END)
    b.yearly(D(2024, 10, 12), D(2025, 10, 12), -612, "insurance_car", "AG Insurance")
    b.monthly(D(2024, 1, 1), D(2026, 8, 31), -13.99, "subscription", "Netflix", day=14)
    b.add(D(2026, 9, 14), -17.99, "subscription", "Netflix")
    b.monthly(D(2024, 1, 1), END, 2400, "salary", "Acme NV", day=25)
    return customer(products=["current", "savings"]), b.txs


def test_insurance_card_lifecycle_and_honesty():
    c, txs = sara_like()
    # 45+ days before: no card yet
    assert cards_for(c, txs, 3000, D(2026, 8, 1), {"insurance_renewal"}) == []
    early = cards_for(c, txs, 3000, D(2026, 9, 10), {"insurance_renewal"})[0]
    assert early.stage == "early" and early.due_date == D(2026, 10, 12)
    soon = cards_for(c, txs, 3000, END, {"insurance_renewal"})[0]
    assert soon.stage == "soon" and "12 days" in soon.title
    urgent = cards_for(c, txs, 3000, D(2026, 10, 10), {"insurance_renewal"})[0]
    assert urgent.stage == "urgent"
    assert cards_for(c, txs, 3000, D(2026, 10, 13), {"insurance_renewal"}) == []  # expired
    assert soon.commercial and soon.card_key == "insurance_renewal:ag-insurance-car"
    rows = soon.details["comparison"]
    assert any("illustrative" in r["kbc"] for r in rows)
    assert any(r["current"] == "check your policy" for r in rows)   # never claims competitor terms
    assert "compared to what you pay now" in soon.body


def test_insurance_card_suppressed_when_kbc_customer_or_kbc_insurer():
    c, txs = sara_like()
    c2 = customer(products=["current", "car_insurance"])
    assert cards_for(c2, txs, 3000, END, {"insurance_renewal"}) == []
    b = TxBuilder()
    baseline(b, D(2024, 1, 1), END)
    b.yearly(D(2024, 10, 12), D(2025, 10, 12), -612, "insurance_car", "KBC Verzekeringen")
    assert cards_for(customer(), b.txs, 3000, END, {"insurance_renewal"}) == []


def test_price_increase_and_duplicate_charge():
    c, txs = sara_like()
    pi = cards_for(c, txs, 3000, END, {"price_increase"})[0]
    assert pi.eur_impact == 48 and "13,99" in pi.title and "17,99" in pi.title
    assert cards_for(c, txs, 3000, D(2026, 12, 1), {"price_increase"}) == []  # older than 60 days
    b = TxBuilder()
    baseline(b, D(2026, 1, 1), END)
    b.add(D(2026, 9, 27), -64.20, "groceries", "Colruyt")
    b.add(D(2026, 9, 27), -64.20, "groceries", "Colruyt")
    dup = cards_for(customer(), b.txs, 3000, END, {"duplicate_charge"})
    assert len(dup) == 1 and dup[0].eur_impact == 64.2 and "Colruyt" in dup[0].title
    assert cards_for(customer(), b.txs, 3000, D(2026, 10, 20), {"duplicate_charge"}) == []  # >14 days


def test_vat_reserve():
    b = TxBuilder()
    baseline(b, D(2025, 1, 1), END)
    for m, amt in [(7, 3000), (8, 2760), (9, 3000)]:
        b.add(D(2026, m, 10), amt, "invoice_income", f"Client {m}")
    b.add(D(2026, 7, 18), -1610, "vat_payment", "FOD Financiën")
    card = cards_for(customer(), b.txs, 3000, END, {"vat_reserve"})[0]
    assert card.due_date == D(2026, 10, 20) and card.stage == "early"
    assert card.eur_impact == round(8760 * 0.21) and card.card_key == "vat_reserve:2026q3"
    assert any("1.610" in e for e in card.evidence)
    # Q3 return stays the relevant period until its due date, escalating soon → urgent
    soon = cards_for(customer(), b.txs, 3000, D(2026, 10, 10), {"vat_reserve"})[0]
    assert soon.stage == "soon" and soon.card_key == "vat_reserve:2026q3" and soon.eur_impact == card.eur_impact
    urgent = cards_for(customer(), b.txs, 3000, D(2026, 10, 19), {"vat_reserve"})[0]
    assert urgent.stage == "urgent" and urgent.card_key == "vat_reserve:2026q3"
    # after the due date the running quarter (Q4) has no invoices yet → no card
    assert cards_for(customer(), b.txs, 3000, D(2026, 10, 21), {"vat_reserve"}) == []
    # a Q4 invoice makes a Q4 card appear, due 20 Jan
    b.add(D(2026, 11, 5), 2000, "invoice_income", "Client 11")
    q4 = cards_for(customer(), b.txs, 3000, D(2026, 11, 10), {"vat_reserve"})[0]
    assert q4.card_key == "vat_reserve:2026q4" and q4.due_date == D(2027, 1, 20) and q4.eur_impact == 420


def test_runway_cashflow_idle_and_scam():
    b = TxBuilder()
    baseline(b, D(2025, 6, 1), END)
    for day in range(1, 29):
        b.add(D(2026, 9, day), -60, "leisure", "Bar")
    c = customer(products=["current"], birth_year=1955)
    cards = cards_for(c, b.txs, 400, END)
    types = {k.card_type for k in cards}
    assert {"runway", "cashflow_squeeze", "scam_awareness"} <= types
    scam = next(k for k in cards if k.card_type == "scam_awareness")
    assert scam.confidence >= 0.7  # senior
    rich = cards_for(c, b.txs, 30000, END, {"idle_cash"})[0]
    assert rich.commercial and rich.eur_impact > 0


def test_life_event_cards_only_recent():
    b = TxBuilder()
    baseline(b, D(2026, 1, 1), END)
    b.add(D(2026, 9, 25), 2400, "salary", "Acme NV")
    cards = cards_for(customer(), b.txs, 3000, END, {"life_event"})
    assert len(cards) == 1 and "First salary" in cards[0].title
    assert cards_for(customer(), b.txs, 3000, D(2026, 12, 15), {"life_event"}) == []


def test_card_keys_are_valid_and_unique():
    c, txs = sara_like()
    cards = cards_for(c, txs, 3000, END)
    keys = [k.card_key for k in cards]
    assert len(keys) == len(set(keys))
    assert all(re.match(CARD_KEY_PATTERN, k) for k in keys)


def test_stage_for():
    d = D(2026, 10, 10)
    assert stage_for(None, d) == "info"
    assert stage_for(d, d) == "urgent"
    assert stage_for(d + dt.timedelta(days=3), d) == "urgent"
    assert stage_for(d + dt.timedelta(days=4), d) == "soon"
    assert stage_for(d + dt.timedelta(days=14), d) == "soon"
    assert stage_for(d + dt.timedelta(days=15), d) == "early"
    assert stage_for(d - dt.timedelta(days=1), d) is None


def test_scam_awareness_only_for_60_plus():
    b = TxBuilder()
    baseline(b, D(2026, 1, 1), END)
    assert cards_for(customer(birth_year=2005), b.txs, 500, END, {"scam_awareness"}) == []
    assert cards_for(customer(birth_year=1965), b.txs, 500, END, {"scam_awareness"}) != []


def test_one_off_payment_does_not_trigger_squeeze_or_runway():
    b = TxBuilder()
    baseline(b, D(2025, 1, 1), END)
    b.monthly(D(2025, 1, 1), END, 2400, "salary", "Acme NV", day=25)
    b.add(D(2026, 9, 20), -12500, "notary", "Notaris Claes")
    b.add(D(2026, 9, 22), -1800, "furniture", "IKEA")
    cards = cards_for(customer(), b.txs, 1500, END, {"cashflow_squeeze", "runway"})
    assert cards == []


def test_runway_impact_is_shortfall_until_next_income():
    b = TxBuilder()
    baseline(b, D(2025, 6, 1), END)               # ~850/month, no income → daily burn ≈ 28
    b.monthly(D(2026, 6, 1), END, 300, "student_income", "Randstad", day=20)
    card = cards_for(customer(birth_year=2004), b.txs, 200, END, {"runway"})[0]
    assert card.stage in ("urgent", "soon") and 0 < card.eur_impact < 900


def test_insurance_card_from_a_single_payment_and_no_utility_price_cards():
    b = TxBuilder()
    baseline(b, D(2025, 9, 1), END)
    b.add(D(2025, 10, 14), -735.62, "insurance_car", "Baloise")
    b.monthly(D(2025, 9, 1), D(2026, 8, 31), -110, "utilities", "Engie", day=8)
    b.add(D(2026, 9, 8), -160, "utilities", "Engie")
    cards = cards_for(customer(), b.txs, 1000, END, {"insurance_renewal", "price_increase"})
    assert [k.card_type for k in cards] == ["insurance_renewal"]
    assert cards[0].stage == "soon" and any("€735,62 to Baloise on 14 Oct 2025" in e for e in cards[0].evidence)
