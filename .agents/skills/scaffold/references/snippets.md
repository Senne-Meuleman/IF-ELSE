# Starter snippets (Python + Streamlit)

Tested patterns from the team's earlier kit, condensed. Copy what the plan
needs, delete the rest. Every function is short on purpose; adapt freely.

## llm.py: one client, any backend, with replay cache

```python
"""ask / extract / run_agent over any OpenAI-compatible chat API. Backend from LLM_BACKEND in .env."""
from __future__ import annotations
import hashlib, inspect, json, os, re
from pathlib import Path
from typing import Any, Callable, TypeVar, get_type_hints
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()
BACKENDS = {
    "gemini": {"url": "https://generativelanguage.googleapis.com/v1beta/openai",
               "key": os.getenv("GEMINI_API_KEY", ""), "model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
               "embed": "gemini-embedding-001", "extra": {}},
    "ollama": {"url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"), "key": "ollama",
               "model": os.getenv("OLLAMA_MODEL", "qwen3.5:4b"), "embed": "bge-m3",
               "extra": {"reasoning_effort": "none"}},   # otherwise qwen3.5 thinks until the context is full
    "openai": {"url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"), "key": os.getenv("OPENAI_API_KEY", ""),
               "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), "embed": "text-embedding-3-small", "extra": {}},
}
T = TypeVar("T", bound=BaseModel)


def backend() -> str:
    return os.getenv("LLM_BACKEND", "gemini")


def _cached(url: str, payload: dict, live: Callable[[], Any]) -> Any:
    """DEMO_CACHE = off | record | replay | strict. Key = exact request, so use seeded inputs."""
    mode = os.getenv("DEMO_CACHE", "off").lower()
    if mode == "off":
        return live()
    k = hashlib.sha256(json.dumps([url.rsplit("/", 1)[-1], payload], sort_keys=True, default=str).encode()).hexdigest()[:24]
    p = Path(os.getenv("DEMO_CACHE_DIR", "data/demo_cache")) / f"{k}.json"
    if mode in ("replay", "strict") and p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    if mode == "strict":
        raise RuntimeError(f"strict replay: no cached answer for this request ({k})")
    try:
        out = live()
    except Exception:
        if p.exists():                       # network died: serve the last good answer
            return json.loads(p.read_text(encoding="utf-8"))
        raise
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def _post(path: str, payload: dict, be: str | None = None) -> dict:
    cfg = BACKENDS[be or backend()]
    def live() -> dict:
        r = httpx.post(f"{cfg['url']}{path}", json=payload, headers={"Authorization": f"Bearer {cfg['key']}"}, timeout=120)
        if r.status_code >= 400:
            raise RuntimeError(f"{path} -> HTTP {r.status_code}: {r.text[:300]}")
        return r.json()
    return _cached(f"{cfg['url']}{path}", payload, live)


def chat(messages: list[dict], *, be: str | None = None, temperature: float = 0.3, **kw) -> dict:
    cfg = BACKENDS[be or backend()]
    payload = {"model": cfg["model"], "messages": messages, "temperature": temperature, **cfg["extra"], **kw}
    return _post("/chat/completions", payload, be)["choices"][0]["message"]


def ask(prompt: str, *, system: str | None = None, **kw) -> str:
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    return chat(msgs, **kw).get("content") or ""


def _parse_json(text: str) -> Any:
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}|\[.*\]", text, re.S)
        if not m:
            raise
        return json.loads(m.group(0))


def extract(text: str, schema: type[T], *, instructions: str = "", retries: int = 2, **kw) -> T:
    """Unstructured text -> validated pydantic object. Feeds validation errors back and retries."""
    system = ("Extract the requested information from the user's text. Reply with JSON only, matching this schema:\n"
              f"{json.dumps(schema.model_json_schema())}\nUse null for anything not present. Never invent values. " + instructions)
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": text}]
    fmt = {"type": "json_schema", "json_schema": {"name": schema.__name__, "schema": schema.model_json_schema()}}
    err: Exception | None = None
    for _ in range(retries + 1):
        out = chat(msgs, temperature=0, response_format=fmt, **kw).get("content") or ""
        try:
            return schema.model_validate(_parse_json(out))
        except (ValidationError, json.JSONDecodeError) as e:
            err = e
            msgs += [{"role": "assistant", "content": out}, {"role": "user", "content": f"That was invalid: {e}. Reply with corrected JSON only."}]
    raise ValueError(f"extract failed: {err}")


_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}


def tool_schema(fn: Callable) -> dict:
    """OpenAI tool definition from a type-hinted function. The docstring IS the tool description: make it precise."""
    hints, params = get_type_hints(fn), inspect.signature(fn).parameters
    return {"type": "function", "function": {"name": fn.__name__, "description": (fn.__doc__ or "").strip(),
            "parameters": {"type": "object", "properties": {n: {"type": _JSON.get(hints.get(n, str), "string")} for n in params},
                           "required": [n for n, p in params.items() if p.default is inspect.Parameter.empty]}}}


def run_agent(task: str, tools: list[Callable], *, system: str = "You are a helpful assistant. Use tools when needed.",
              max_steps: int = 8, on_step: Callable[[str, dict, Any], None] | None = None, **kw) -> str:
    """Minimal tool loop. Tools are plain functions with primitive params. on_step(name, args, result) feeds the UI."""
    by_name = {f.__name__: f for f in tools}
    msgs: list[dict] = [{"role": "system", "content": system}, {"role": "user", "content": task}]
    for _ in range(max_steps):
        msg = chat(msgs, tools=[tool_schema(f) for f in tools], **kw)
        calls = msg.get("tool_calls") or []
        msgs.append({"role": "assistant", "content": msg.get("content") or "", **({"tool_calls": calls} if calls else {})})
        if not calls:
            return msg.get("content") or ""
        for c in calls:
            name, args = c["function"]["name"], json.loads(c["function"]["arguments"] or "{}")
            try:
                result = by_name[name](**args)
            except Exception as e:
                result = f"ERROR: {e}"
            if on_step:
                on_step(name, args, result)
            msgs.append({"role": "tool", "tool_call_id": c.get("id", name), "name": name, "content": json.dumps(result, default=str)})
    return "Stopped: too many steps."


def embed(texts: list[str], *, be: str | None = None) -> list[list[float]]:
    cfg = BACKENDS[be or backend()]
    data = _post("/embeddings", {"model": cfg["embed"], "input": texts}, be)["data"]
    return [d["embedding"] for d in sorted(data, key=lambda d: d["index"])]
```

Mutating tools (send, pay, update) must **not** execute inside `run_agent`.
Have them return a proposal dict (`{"action": "update_iban", "employee_id": ..., "iban": ...}`)
and let the UI's approval card execute it (below).

## pii.py: reversible masking before any cloud call

```python
"""masked, vault = mask(text); reply = ask(masked); unmask(reply, vault). Pitch line: 'PII never leaves in the clear'."""
import re

PATTERNS = {
    "IBAN": r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){2,7}(?:[ ]?[A-Z0-9]{1,3})?\b",
    "NATIONAL_ID": r"\b\d{2}\.?\d{2}\.?\d{2}[- ]?\d{3}\.?\d{2}\b",       # rijksregisternummer YY.MM.DD-XXX.CC
    "EMAIL": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
    "CARD": r"\b(?:\d{4}[ -]?){3}\d{4}\b",
    "PHONE": r"(?<!\w)(?:\+32|0032|0)\s?4?\d{2,3}(?:[ /.]?\d{2}){3}\b",
    "VAT": r"\bBE\s?0?\d{3}\.?\d{3}\.?\d{3}\b",
}


def mask(text: str, names: list[str] | None = None) -> tuple[str, dict[str, str]]:
    vault: dict[str, str] = {}
    seen: dict[str, str] = {}
    def token(kind: str, value: str) -> str:
        if value not in seen:
            seen[value] = f"<{kind}_{sum(k.startswith(f'<{kind}_') for k in vault) + 1}>"
            vault[seen[value]] = value
        return seen[value]
    for kind, pat in PATTERNS.items():
        text = re.sub(pat, lambda m, k=kind: token(k, m.group(0)), text)
    for name in sorted(names or [], key=len, reverse=True):      # known names from your data, longest first
        text = re.sub(re.escape(name), lambda m: token("PERSON", m.group(0)), text)
    return text, vault


def unmask(text: str, vault: dict[str, str]) -> str:
    for tok, value in vault.items():
        text = text.replace(tok, value)
    return text
```

Regex masking is a demo-grade privacy proof, not anonymization. Say "masked",
not "anonymized", on stage. Show the masked text in a caption: judges love it.

## app.py: shell + approval card + safe call

```python
"""Run: uv run streamlit run app.py"""
import streamlit as st
import llm
from pii import mask, unmask

st.set_page_config(page_title="<Product name>", page_icon="⚡", layout="wide")

with st.sidebar:
    st.title("⚡ <Product name>")
    private = st.toggle("Mask personal data before cloud calls", value=True)
    if st.button("🔄 Reset demo"):
        for k in list(st.session_state):
            del st.session_state[k]
        st.rerun()


def safe_ask(prompt: str, system: str | None = None, fallback: str = "…") -> str:
    """Masking round-trip + never a stack trace on stage."""
    vault = {}
    if private:
        prompt, vault = mask(prompt)
        st.caption(f"Sent to the model: {prompt[:200]}")
    try:
        return unmask(llm.ask(prompt, system=system), vault)
    except Exception as e:                       # log, then degrade gracefully
        print("LLM error:", e)
        st.warning("The AI is taking a breather, showing the last good result.")
        return fallback


def approval_card(key: str, proposal: dict, execute):
    """Human in the loop, enforced in code: execute() runs once, only after Approve; Reject and reruns never execute."""
    st.markdown("**Proposed action**")
    st.json(proposal)
    state = st.session_state.get(f"{key}_state")
    c1, c2 = st.columns(2)
    if c1.button("✅ Approve", key=f"{key}_ok", disabled=state is not None, type="primary"):
        st.session_state[f"{key}_state"] = execute(proposal)   # bound to this exact proposal
        st.rerun()
    if c2.button("❌ Reject", key=f"{key}_no", disabled=state is not None):
        st.session_state[f"{key}_state"] = "Rejected, nothing changed."
        st.rerun()
    if state is not None:
        st.success(state)


tab1, tab2 = st.tabs(["📥 Step one", "🤖 Step two"])
with tab1:
    text = st.text_area("Message", "Beste, ik ben ziek vandaag en morgen. Doktersbriefje volgt. Groeten, An Peeters")
    if st.button("▶ Run", type="primary"):
        with st.spinner("Reading the message in Dutch…"):
            st.session_state["step1"] = safe_ask(text, system="Summarise the HR request in one English sentence.")
    if "step1" in st.session_state:
        st.info(st.session_state["step1"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Time", "20 s", "-11 min")          # headline number from /impact-calc
```

Use `key=` on every widget and prefix state keys with the step name, so two
teammates' tabs never collide. Store results in `st.session_state` so a rerun
(any click) does not repeat the AI call.

## Structured extraction with pydantic

```python
from pydantic import BaseModel

class Triage(BaseModel):
    intent: str                   # leave_request | sick_notice | address_change | fraud_report | other
    urgency: str                  # low | medium | high
    language: str                 # nl | fr | en
    summary_en: str
    fields: dict[str, str]        # e.g. {"start": "2026-11-03", "end": "2026-11-07"}
    draft_reply: str              # in the sender's language

t = llm.extract(text, Triage, instructions="draft_reply must be in the same language as the message.")
```

Comments on the fields become part of the schema description only if you put
them in `Field(description=...)`; do that for anything the model gets wrong.

## Tools for the agent

```python
import pandas as pd

@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_csv(f"data/synthetic/{name}.csv")

def get_employee(employee_id: str) -> dict:
    """Look up an employee's contract, department, salary and leave balance by id like E1003."""
    row = table("employees").query("employee_id == @employee_id")
    return row.iloc[0].to_dict() if not row.empty else {"error": "not found"}

def propose_iban_change(employee_id: str, new_iban: str) -> dict:
    """Propose changing an employee's bank account. Does NOT change anything; a human approves it."""
    return {"action": "update_iban", "employee_id": employee_id, "iban": new_iban}

log = st.container(border=True)
answer = llm.run_agent(task, [get_employee, propose_iban_change],
                       on_step=lambda n, a, r: log.markdown(f"🔧 `{n}({a})` → {str(r)[:160]}"))
```

## Synthetic data (seeded, Belgian)

```python
"""uv run python data/synth.py -> data/synthetic/*.csv. Money figures are ILLUSTRATIVE."""
import csv, random
from pathlib import Path
from faker import Faker

SEED = 42
fake = Faker(["nl_BE", "fr_BE"]); Faker.seed(SEED)
rng = random.Random(SEED)

def employees(n: int = 60) -> list[dict]:
    return [{"employee_id": f"E{1000 + i}", "name": fake.name(), "email": fake.email(),
             "language": rng.choice(["nl", "fr"]), "department": rng.choice(["Finance", "Sales", "IT", "HR", "Operations"]),
             "joint_committee": rng.choices(["PC 200", "PC 124", "PC 302"], [80, 10, 10])[0],
             "gross_monthly_eur": round(rng.uniform(2300, 6200), 2), "annual_leave_days": 20 + rng.choice([0, 0, 2, 4]),
             "iban": fake["nl_BE"].iban()} for i in range(n)]

def write(name: str, rows: list[dict], out: Path = Path("data/synthetic")) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with open(out / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    write("employees", employees())
```

Plant 3–5 rows that make the story work (the anomaly, the missing field, the
angry FR email) and mark them with a `flag` column. See `/challenge-data`.

## Voice (ElevenLabs, a tech partner)

```python
import os, httpx

def speak(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", model: str = "eleven_multilingual_v2") -> bytes:
    r = httpx.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}", timeout=60,
                   headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}, json={"text": text, "model_id": model})
    r.raise_for_status()
    return r.content                      # mp3 bytes -> st.audio(mp3, format="audio/mpeg")
```

## Tiny RAG (only if the brief comes with documents)

```python
import numpy as np

def chunks(text: str, size: int = 800, overlap: int = 150) -> list[str]:
    return [text[i:i + size] for i in range(0, max(len(text), 1), size - overlap)]

docs = {p.name: p.read_text(encoding="utf-8", errors="ignore") for p in Path("data/docs").glob("*.md")}
items = [(src, c) for src, t in docs.items() for c in chunks(t)]
V = np.array(llm.embed([c for _, c in items]), dtype=np.float32); V /= np.linalg.norm(V, axis=1, keepdims=True)

def answer(q: str, k: int = 4) -> tuple[str, list]:
    qv = np.array(llm.embed([q])[0], dtype=np.float32); qv /= np.linalg.norm(qv)
    top = np.argsort(-(V @ qv))[:k]
    ctx = "\n\n".join(f"[{i + 1}] ({items[j][0]})\n{items[j][1]}" for i, j in enumerate(top))
    system = ("Answer using ONLY the numbered sources. Cite them like [1]. If the answer is not there, say you don't know. "
              "Answer in the language of the question.\n\n" + ctx)
    return llm.ask(q, system=system), [items[j] for j in top]
```

PDFs: `from pypdf import PdfReader; "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)`.
Embed once at startup (or cache to `data/index.npz`), never per question.
