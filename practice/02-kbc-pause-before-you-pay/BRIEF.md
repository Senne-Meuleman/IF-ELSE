> Practice brief written by team IF-ELSE. Fictional: not an actual KBC or Tectonic brief.

# KBC challenge: Pause before you pay

## Context

Scammers no longer break into banks. They talk our customers into sending the money
themselves. In Belgium, phishing losses reached **EUR 93 million in 2025**, almost double
the year before, across more than 11,000 cases. The messages are good: a "new device was
added to your account" SMS, a WhatsApp from a "child" with a new number, an itsme
"reactivation" link. By the time the customer realises, the money is gone.

The sector is moving. Since 9 October 2025, SEPA credit transfers in the euro area get a **Verification of
Payee** check (does the name match the IBAN?). On 8 July 2026, Febelfin and Minister
Beenders announced an action plan: a default transfer limit of at most EUR 5,000 by early
2027, a 4-hour wait when a customer raises a limit, and temporary holds on suspicious
payments.

But a limit or a hold is only half the answer. The decisive moment is the ten seconds before
the customer presses "confirm", and the hour after a scam, when they feel ashamed and do
not know who to call. At the same time, almost every transfer we see is perfectly normal.
Our customers buy cars, pay plumbers and split restaurant bills. They do not want a bank
that treats them as suspects.

Kate, our digital assistant, already helps 5.8 million users. One rule is not negotiable:
Kate never acts without explicit customer approval.

## The challenge

**How might we help a customer who is about to send a risky transfer, or who has just been
scammed, to pause and decide, in plain language and in their own language, without adding
friction to the many legitimate payments?**

## Who you're building for

- **Retail customers** of KBC in Flanders, CBC in Wallonia and KBC Brussels. Some live in
  the app. Others are over 75, use a PC twice a month and would rather phone someone.
  They speak Dutch, French or English.
- **Fraud analysts**, who review the payments our rules put on hold. Today they see a
  queue of alerts with little context, and many of them turn out to be false alarms.

Pick one of them, or show how both meet.

## What we give you

All data is synthetic. See `materials/README.md`.

- `customers.csv`: 10 customers, their brand, language, digital profile and limits
- `transactions.csv`: 30 days of outgoing transfers, some currently held for review
- `vop_results.csv`: Verification of Payee results for the held transfers
- `events.csv`: logins, devices, limit changes
- `messages.json`: messages customers received around their transfers
- `scam_patterns.md`: our fraud team's cheat sheet

Tech partners available to you, optional: **Gemini** (Google Cloud) and **ElevenLabs**
(voice).

## What success looks like for us

- A real person, a real moment. Show us the exact screen, message or call where your
  solution changes the outcome.
- The customer understands *why* in one sentence, in their language, and stays in control.
- Normal payments stay fast. Tell us how you avoid crying wolf.
- A believable idea of impact: money kept, alerts avoided, analyst time saved. Show your
  assumptions.
- Something we could imagine inside KBC Mobile or next to Kate.

## Constraints

- The customer or an analyst decides. Your solution may advise, pause or explain, but it
  does not silently block or move money.
- Use only the synthetic data. No real customer data, no real national register numbers.
- Be careful with claims about law and about KBC. If a rule is not in force yet, say so.
  If you need a number we did not give you, label it as an assumption.
- Explain how you would keep personal data safe if you use a cloud model.

## Practical

- The whole event runs in **English**. Your product may speak Dutch, French and English.
- **3-minute pitch**, live demo preferred, followed by questions from the jury.
- Hand in a repo link, a short README and a backup video or screenshots.
- Mentors from our fraud and digital teams walk around. Ask them what a normal day looks
  like.
