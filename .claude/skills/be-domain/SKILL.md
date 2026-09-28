---
name: be-domain
description: Verified, sourced facts on Belgian HR & payroll (joint committees, leave, holiday pay, social security, sickness, time credit, meal vouchers, indexation), EU Pay Transparency, Belgian banking and fraud (KBC, Kate, Verification of Payee, PSD2, DORA), Peppol e-invoicing, the EU AI Act and GDPR in Belgium, plus SD Worx and KBC company facts. Load BEFORE stating any Belgian law, rate, threshold, deadline or sponsor figure in code, UI text, prompts, the pitch or an answer, and whenever someone asks "is that true", "what's the rule for …", "how does … work in Belgium", or wants a number for the pitch. Prevents confidently wrong regulation in front of KBC / SD Worx experts.
---

# Belgian domain facts

The audience at the final includes payroll experts from SD Worx and bankers from KBC. One invented rule ("employees get 25 legal leave days") costs more credibility than the whole demo earns. So:

1. **Read `references/facts.md`** as a dated research starting point, not proof that a claim is still correct. Before stating a legal rule, rate, deadline or sponsor figure, open the supporting source and check its date, scope and current status. Distinguish proposals, enacted rules and effective dates; EU directives do not by themselves establish Belgian transposition.
2. If a needed fact is missing or stale, research it with the available web tools (in Claude Code the `researcher` subagent does this in the background) and cite an official source (belgium.be, socialsecurity.be, FOD/SPF Financiën, FOD WASO/SPF Emploi, eur-lex.europa.eu, nbb.be, febelfin.be, kbc.com, sdworx.com). Record verified updates in `.claude/skills/be-domain/references/facts.md` with source, scope and date checked, then run `py scripts/sync_skills.py` (`python3` on macOS/Linux) from the repository root.
3. If it still can't be verified, **say so** and label it *illustrative* in the UI or pitch. Never present a guess as a legal fact.
4. In any prompt that touches rules (chat, extraction, agent system prompts), paste the relevant facts into the system prompt instead of trusting the model's memory. Small local models especially invent Belgian law.
5. Use the local terms the experts use, with a translation: *paritair comité / commission paritaire (PC)*, *CAO / CCT*, *bedrijfsvoorheffing / précompte professionnel*, *RSZ / ONSS*, *rijksregisternummer / numéro de registre national*, *tijdskrediet / crédit-temps*, *vakantiegeld / pécule de vacances*.

For the pitch, the "Most useful for a pitch" block at the top of `facts.md` gives quick "why now" hooks (deadlines, regulation, fraud figures, sponsor scale).
