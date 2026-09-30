"""API tests: auth, IDOR isolation, validation, feedback loop, as_of clamping."""
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from app import db as dbmod


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("db") / "kbc_test.db")
    os.environ["KBC_DB_PATH"] = path
    os.environ["DEMO_PASSWORD"] = "demo"
    dbmod.DB_PATH = path
    from synth.generate import build

    build(path, n=20, seed=7)
    from app.main import app

    with TestClient(app) as c:
        yield c


def _login(client: TestClient, username: str, password: str = "demo"):
    return client.post("/api/login", json={"username": username, "password": password})


def test_home_requires_login(client):
    client.cookies.clear()
    assert client.get("/api/me/home").status_code == 401


def test_bad_password_rejected(client):
    client.cookies.clear()
    assert _login(client, "sara", "wrong").status_code == 401


def test_login_validation(client):
    client.cookies.clear()
    r = client.post("/api/login", json={"username": "Sara; DROP TABLE users", "password": "demo"})
    assert r.status_code == 422


def test_home_is_session_bound(client):
    client.cookies.clear()
    assert _login(client, "sara").status_code == 200
    sara = client.get("/api/me/home").json()
    assert sara["customer"]["first_name"] == "Sara"
    assert "ground_truth" not in str(sara)
    # No way to ask for another customer: there is no customer id parameter at all
    assert client.get("/api/me/home?customer_id=9003").json()["customer"]["first_name"] == "Sara"

    client.cookies.clear()
    assert _login(client, "jan").status_code == 200
    jan = client.get("/api/me/home").json()
    assert jan["customer"]["first_name"] == "Jan"


def test_home_response_shape(client):
    client.cookies.clear()
    _login(client, "sara")
    home = client.get("/api/me/home").json()
    assert home["layout"]["sections"][0]["size"] == "hero"
    assert home["layout"]["sections"][1]["component"] == "ForYouFeed"
    assert abs(sum(p["weight"] for p in home["persona_mix"]) - 1) < 1e-6
    assert len(home["feed"]["cards"]) <= 7


def test_as_of_is_clamped(client):
    client.cookies.clear()
    _login(client, "sara")
    r = client.get("/api/me/home?as_of=2099-01-01")
    assert r.status_code == 200
    assert r.json()["as_of"] <= "2026-09-30"
    assert client.get("/api/me/home?as_of=not-a-date").status_code == 422


def test_timeline(client):
    client.cookies.clear()
    _login(client, "lotte")
    tl = client.get("/api/me/timeline").json()
    assert tl["min_date"] < tl["max_date"]
    assert len(tl["milestones"]) >= 3


def test_feedback_changes_feed(client):
    client.cookies.clear()
    _login(client, "sara")
    home = client.get("/api/me/home").json()
    assert home["feed"]["cards"], "sara should have cards"
    first = home["feed"]["cards"][0]
    after = client.post("/api/me/feedback",
                        json={"card_key": first["card_key"], "card_type": first["card_type"],
                              "decision": "dismiss"}).json()
    assert all(c["card_key"] != first["card_key"] for c in after["feed"]["cards"])
    reset = client.post("/api/me/feedback",
                        json={"card_key": "reset", "card_type": first["card_type"], "decision": "reset"}).json()
    assert any(c["card_key"] == first["card_key"] for c in reset["feed"]["cards"])


def test_feedback_validation(client):
    client.cookies.clear()
    _login(client, "sara")
    r = client.post("/api/me/feedback", json={"card_key": "<script>", "card_type": "runway", "decision": "dismiss"})
    assert r.status_code == 422
    r = client.post("/api/me/feedback", json={"card_key": "x", "card_type": "runway", "decision": "delete_all"})
    assert r.status_code == 422


def test_layout_pref_hides_component(client):
    client.cookies.clear()
    _login(client, "sara")
    home = client.get("/api/me/home").json()
    halves = [s["component"] for s in home["layout"]["sections"] if s["size"] == "half"]
    if not halves:
        pytest.skip("no half-size components to hide")
    target = halves[0]
    after = client.post("/api/me/layout-prefs", json={"component": target, "state": "hidden"}).json()
    assert target not in [s["component"] for s in after["layout"]["sections"]]
    client.post("/api/me/layout-prefs", json={"component": target, "state": "reset"})
    r = client.post("/api/me/layout-prefs", json={"component": "EvilComponent", "state": "pinned"})
    assert r.status_code == 422


def test_consent_gates_commercial(client):
    client.cookies.clear()
    _login(client, "sara")
    off = client.post("/api/me/consent", json={"consent_personalization": False}).json()
    assert not any(c["commercial"] for c in off["feed"]["cards"])
    on = client.post("/api/me/consent", json={"consent_personalization": True}).json()
    assert on["customer"]["consent_personalization"] is True


def test_advisor_role_enforced(client):
    client.cookies.clear()
    _login(client, "sara")
    assert client.get("/api/advisor/overview").status_code == 403
    client.cookies.clear()
    _login(client, "advisor")
    assert client.get("/api/me/home").status_code == 403
    r = client.get("/api/advisor/overview")
    assert r.status_code == 200
    body = r.json()
    assert body["customers_scored"] >= 20
    assert body["projected_2_3m_seconds"] > 0


def test_security_headers(client):
    client.cookies.clear()
    r = client.post("/api/logout")
    assert "Content-Security-Policy" in r.headers
    assert r.headers["X-Frame-Options"] == "DENY"
