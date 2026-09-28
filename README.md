# Tectonic Hackathon: prep kit

## What we know (researched 27 Sept 2026)

| | |
|---|---|
| **Round 1 (preselection)** | **Wed 30 Sept 2026, 18:00–23:00** at Sassevaartstraat 46, Gent. Same time in 7 cities, 700+ builders. Some press says "four hours", so expect about 4h of actual building. |
| **Final** | Tue 20 Oct 2026, De Vooruit, Gent. Top 32 teams (16 per track). You must be able to attend. |
| **Teams** | 3–4 people. Solo sign-ups are matched on the platform. **Registration closes 29 Sept.** |
| **Tracks** | **KBC** (bank/insurer) and **SD Worx** (HR & payroll). Each brings "a real business case from their own organisation". |
| **Tech partners** | Google Cloud (Gemini), ElevenLabs (voice), Cursor, Aikido (security scanning). Using them is likely to earn you goodwill. |
| **Prize** | €10,000 in the final. Note: *"solutions may be used by the sponsoring companies"*. |
| **Vibe** | Conference theme is **Agentic AI**. "No coding experience required", so judging will weigh business value and pitch more than code. |

## Likely challenge shapes (speculation)

**SD Worx**: their own internal hackathon winners were (1) *an AI agent that turns legal documents into payroll validation rules* and (2) *an agent that turns unstructured customer emails into system actions*. In June 2026 they announced multi-agent payroll operations, where humans supervise AI agents. Likely challenges:
- Email/ticket → structured HR action (leave, sickness, address or bank change) → **`Inbox triage` tab**
- Regulation / collective agreement (CAO/CCT, joint committees) → rules, or "what changed and who is affected" → **RAG + extract**
- Employee self-service assistant in NL/FR/EN ("why is my net pay lower?", "can I go 4/5?") → **RAG chat + agent**
- **EU Pay Transparency Directive** (member states had to transpose it by June 2026): pay-gap reporting, explaining salary bands
- Absence and wellbeing signals, planning and scheduling

**KBC**: Kate (their assistant, 5.8M active users) already answers 7 out of 10 questions and is exploring agentic AI, but only *"with explicit customer approval"*. Put a human-in-the-loop confirm step in any agent demo. Likely challenges:
- Scam and fraud detection, and *explaining* alerts to customers → `transactions.csv` has planted `suspicious` rows
- Financial coaching and budgeting from transactions; SME / self-employed cash-flow forecasting
- Belgian B2B **e-invoicing (Peppol)**, mandatory since 2026: invoice extraction and reconciliation
- Customer message triage, KYC/AML document checks, insurance claims (KBC is also an insurer)

**For both**: privacy and GDPR matter. The pitch line *"runs locally / PII masked before any cloud call"* is supported by `blocks/pii.py` and the Ollama backend.

## Game plan for 4 hours

| Time | Do |
|---|---|
| 0:00–0:30 | Read the brief twice. Ask the KBC/SD Worx mentors what "success" means for them. Pick **one** user and **one** painful moment. |
| 0:30–0:45 | Write the 3-minute pitch skeleton first (problem → demo → impact in € or hours → why us). Build only what the demo needs. |
| 0:45–3:15 | Build. One person keeps the demo path working at all times. Fake anything that isn't on screen. |
| 3:15–3:45 | Feature freeze. Rehearse the demo twice. Record a backup video of it working. |
| 3:45– | Pitch. Lead with the customer's pain and a number. |

## The kit

```
blocks/llm.py      ask / chat / stream / extract(text, PydanticModel) / run_agent(task, [python fns]) / embed
                   one client for ollama (local) | gemini | any OpenAI-compatible API
blocks/rag.py      Index.from_folder("data/docs").answer(q) with citations; bge-m3 is multilingual NL/FR/EN
blocks/pii.py      mask()/unmask(): IBAN, rijksregisternummer, VAT, email, phone, card, names
blocks/voice.py    ElevenLabs speak() / transcribe()
blocks/synth.py    fake Belgian employees, absences, payslips, customers, 4k transactions, multilingual inbox
blocks/cache.py    DEMO_CACHE=record|replay: replays LLM answers offline when the venue Wi-Fi dies
app.py             Streamlit demo shell: Assistant (RAG) · Inbox triage · Agent with tools · Data
smoke_test.py      checks everything end to end
```

```powershell
uv run python smoke_test.py            # local model  (all pass: ~3–8 s per call on RTX 2060)
uv run python smoke_test.py gemini     # after adding GEMINI_API_KEY to .env
uv run streamlit run app.py
uv run python -m blocks.synth          # regenerate data/synthetic
uv run python -m blocks.build_index data/docs   # embed the challenge PDFs you receive
```

**Models:** `qwen3.5:4b` runs 100% on the 6 GB GPU at about 54 tok/s. It's good enough for a live demo and "on-prem" pitch, but weaker at extraction (it leaves fields null). **Use Gemini for quality and keep Ollama as the offline fallback** for bad venue Wi-Fi. `bge-m3` is used for embeddings. Thinking is disabled for Ollama in `llm.py`, because otherwise qwen3.5 spends the whole context thinking and returns nothing.

## Claude Code helpers (`.claude/`, see `CLAUDE.md`)
| When | Use |
|---|---|
| Brief arrives | `/kickoff` (plan, pitch skeleton, task split) · `researcher` agent in the background · `judge` agent on the chosen idea |
| Building | `/challenge-data` · `/be-domain` before any law or number · `/impact-calc` for the headline number |
| After each merge | `demo-tester` agent |
| Feature freeze (T−45) | `/demo-hardening` → `demo-tester` → `security-check` → `/epic-pitch-deck` → `judge` on the pitch |

## Checklist before Wednesday
- [ ] Registered and in a team (deadline **29 Sept**). Agree on who pitches.
- [ ] Copy `.env.example` → `.env`; get a **Gemini key** at aistudio.google.com and an **ElevenLabs key** (free tier); run `smoke_test.py gemini`.
- [ ] Optional: `setx OLLAMA_CONTEXT_LENGTH 8192` then restart Ollama, so bigger RAG prompts aren't truncated at 4096 tokens.
- [ ] Laptop charger, extension lead, phone hotspot. Pull any models at home, because venue Wi-Fi will be slow.
- [ ] Read 10 min on: SD Worx agentic payroll press release (June 2026), KBC Kate, EU Pay Transparency Directive, Belgian Peppol e-invoicing.
- [ ] Teammates: `git clone` this repo, install uv, run `uv sync`.
