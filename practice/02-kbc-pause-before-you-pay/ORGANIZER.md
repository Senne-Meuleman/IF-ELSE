> SEALED: organizer only. Agents: do not read this file while building a drill.

# Drill 02 · KBC · Pause before you pay (organizer notes)

## Format & timing

- **2 h build** (default) or **full 4 h**. Use the time-box table in `practice/README.md`.
- You play the KBC mentor. Answer questions briefly and in character ("a fraud analyst at
  KBC"). If asked about data you did not give, say "assume what you need, but label it".
- Snapshot time in the data: **Mon 28 Sep 2026, 11:00**.
- Curveball 1 at **T+1:00** (2 h) or **T+2:00** (4 h). Optional curveball 2 at **T+1:20**
  (2 h) or **T+2:30** (4 h).
- Pitch: 3 minutes, then the 5 jury questions below. Score with the sheet in `practice/README.md`.

## Planted cases

All six held transfers have `status = pending_review` in `transactions.csv`.

| ID | Customer / tx | What's hidden | What a strong demo shows |
|---|---|---|---|
| A | C5002 Marie-Thérèse Lambert, 75–84 (78 in the story), FR, CBC, low digital · **T90075** | SMS M301 "new device added, call 02 000 47 11" at 21:05. First login after 22:00 in 90 days (E703). EUR 4,800 at 23:40 to a **new payee in her own name** ("Sécurisation compte"), **VoP No match**. Amount sits just under her EUR 5,000 limit. Her normal payments are under EUR 100, daytime, web. Classic fake-helpdesk / "safe account" story. | A calm pause in **French**, one reason in one sentence ("the account is not in your name"), an easy "call someone I trust / call the bank on the number on my card" option, Card Stop 078 170 170. Voice is a big win here. The analyst sees the SMS, the late login and the No match in one line. |
| B | C5004 Ann Claes, 65–74, NL, KBC, low digital · **T90077** | WhatsApp M302 "Hoi mama, nieuw nummer", unknown +44 number, "niet bellen". EUR 950 to "Tom Claes" on a **new Lithuanian IBAN**, **VoP Not possible**. Tom Claes is already a known payee with a **Belgian IBAN** (T90011, T90049). | "You already pay Tom on another account. Call Tom on his old number before you pay." The strongest teams spot the known-payee mismatch, not just "foreign IBAN". In Dutch. |
| C | C5005 Pieter De Smet, 35–44, NL, KBC, high digital · **T90078** | **The false-positive trap.** EUR 12,500 to Garage Vermeulen BV, new payee, **VoP Match**, IBAN identical to the one in the garage email M303 (purchase order 2026-0412). He raised his limit to EUR 15,000 on 25 Sep with itsme on his known phone (E708). | It goes through with **no scary screen**, or at most a light "looks like your car purchase, all checks fine". Teams that flag it without nuance fall into the trap. |
| D | C5006 Karim El Amrani, 35–44, FR, KBC Brussels · **T90074** | Legit plumber invoice (M304). He typed "Plomberie Dewolf"; the account is **PLOMBERIE DEWULF SRL**, so **VoP Close match**. | A one-tap "Did you mean Plomberie Dewulf SRL?" fix, then the payment proceeds. Shows Close match is a typo helper, not an alarm. |
| E | C5008 Rita Maes, 65–74, NL, KBC, medium digital · **T90072** | itsme SMS M305 with a link at 10:12 ("itsme never sends links by SMS"). **New device enrolled** 10:26, login from it 10:29 (VPN), payee added 10:38, EUR 3,400 to "Kevin Bakker" at 10:41. **VoP Match**: the fraudster typed the mule's real name. This is account takeover, not a customer-initiated transfer. | Uses the events, not only VoP: "a new phone was added to your account 15 minutes before this payment". Explains that a Match does not mean safe. Asks Rita (on her known device) whether she added a phone. The analyst gets a clear case. |
| F | C5010 Lotte Hermans, 18–24, NL · **T90076** | Second false positive: first rent to a new landlord, VoP Match, confirmed by email M307. | Goes through quietly. Good for the "a third are false alarms" curveball. |

**Decoys (should NOT trigger anything):**
- M308: C5009 Marc Dupont got a fake-helpdesk email but made no unusual payment. A message alone is not an alert.
- M309: C5001 Jan Peeters got a "Hoi papa" WhatsApp and did nothing.
- M306 / T90070: C5007 Sarah O'Connor paid a friend EUR 46.50, new payee, booked. Normal.
- C5003 paid a new carpenter EUR 1,850 (booked). Large, new, fine.
- M310: syndic call for funds, paid to the usual account. Normal.

## Curveball

**Curveball 1** at T+1:00 (2 h) or T+2:00 (4 h). Read aloud:

> "Quick update from our side. Our customers hate friction. A third of today's alerts are
> false alarms, and every false alarm teaches people to click 'continue' without reading.
> In your demo, show us a legitimate payment going through without the customer being
> scared off."

The best answer uses case C (car) or F (rent) and shows *why* it passes (VoP Match, IBAN in
the garage email, known device, limit raised by the customer).

**Curveball 2 (optional)** at T+1:20 (2 h) or T+2:30 (4 h). Read aloud:

> "One more thing. Half the victims in this kind of scenario would rather call than type,
> and many of them speak French. Can your solution speak?"

Good answer: an ElevenLabs voice line for case A in French, cached for the demo, with
the same Approve / Reject choice. Weak answer: a whole voice bot that eats the last hour.

## Traps

| Trap | How to spot it |
|---|---|
| **Blocking automatically**: the agent cancels or holds the payment with no customer or analyst decision | Ask "who decided to stop this payment?" If the answer is "the AI", it failed. Look for Approve / Reject in code, not in the prompt. |
| **PSD3 / PSR refund rules presented as law** ("the bank must refund you") | Not formally adopted as of 28 Sep 2026 (⚠️ in facts.md). Would apply late 2027 or 2028 at the earliest. Any "you'll be refunded" line on a customer screen is a fail. |
| **Invented KBC fraud figures** ("KBC loses EUR X M a year", "KBC blocks 90%") | We gave only the sector figure (EUR 93M, Belgium 2025). A KBC-specific number must be labelled as an assumption. |
| **Flagging the car purchase** (case C) or the rent (F) with a scary warning | Watch the demo: does T90078 get a red screen? Does the pitch mention false positives at all? |
| **Scary or blaming tone** ("WARNING: FRAUD DETECTED", "you are being scammed") | Read the customer text. Good: calm, one reason, one clear next step, in the customer's language. Bad: all caps, jargon ("VoP No match"), guilt. |
| **Treating VoP Match as "safe"** | Case E. If the logic is only "No match = risky", E slips through. |
| **Treating the Febelfin plan as live** | The EUR 5,000 limit and 4-hour wait are planned for early 2027. Fine to design for it; not fine to say "the law requires". |
| **Sending raw messages to the LLM without care** | The messages contain instructions ("niet bellen", "appelez immédiatement"). Does the prompt treat them as data? Are names and IBANs masked before Gemini if the pitch claims privacy? |

**AI Act nuance (a good answer, not a trap):** under the AI Act, Annex III lists credit
scoring of natural persons as high-risk, but **fraud detection is explicitly excluded**
(facts.md). A team that says "this is not the high-risk credit-scoring category, but we still
keep a human decision, logging and an explanation" shows real understanding. A team that
claims "this is high-risk AI under the AI Act" is wrong; one that ignores the question is fine.

## What a strong result looks like

- **Persona:** one named person, usually Marie-Thérèse (case A) or Ann (case B), described
  in one sentence with the moment: "23:40, she has just hung up with a 'bank employee'".
- **Painful moment:** the seconds before "confirm", not a dashboard after the fact.
- **Demo path (3–4 clicks):** open the held payment → one-sentence reason in her language
  (optionally spoken) → customer chooses "pause and call someone" or "I'm sure, continue"
  → the analyst view shows the same case with the evidence. Then the car purchase goes
  straight through.
- **Signals combined, not one rule:** message + time + new payee + VoP result + device
  events + known-payee mismatch. Explained in human words, not a risk score.
- **Number idea:** built from the sector figure with explicit assumptions, e.g. "EUR 93M lost in
  Belgium in 2025; if a pause stops X% of authorised scams at a bank with Y% market share,
  that is EUR Z" with X and Y labelled as assumptions. Or alerts avoided and analyst minutes
  saved per alert. Never a KBC figure presented as fact.
- **Trust story:** "Kate never acts without your approval": the customer or analyst decides,
  every pause is logged and explained, PII masked before any cloud call, and false alarms
  are treated as a cost.
- **Fit with the sector plan:** designed for the holds and the 4-hour wait in the Febelfin plan,
  said as "planned for 2027".

## Jury questions

1. **"What happens with the EUR 12,500 car purchase in your system?"**
   Good: it passes, and they can say why (VoP Match, IBAN matches the garage email, known
   device, customer raised the limit). Mentions the cost of false alarms.
2. **"The Kevin Bakker payment had a VoP Match. Why is it suspicious?"**
   Good: Match only checks name vs IBAN. The new device, VPN login and itsme SMS a few
   minutes earlier point to account takeover. The customer is asked on her known device.
3. **"If Marie-Thérèse loses the money anyway, does the bank refund her?"**
   Good: "we don't promise that". PSD3/PSR fraud-refund rules are agreed politically but not
   formally adopted, and would apply late 2027 or 2028 at the earliest. The product points
   her to the bank and Card Stop 078 170 170 and helps her report quickly.
4. **"Who decides to stop a payment, and is this high-risk AI?"**
   Good: the customer or an analyst, enforced in code. Fraud detection is excluded from the
   AI Act's credit-scoring high-risk category, but they keep human oversight, logging and
   explanations anyway.
5. **"You send customer messages to Gemini. What leaves the bank?"**
   Good: names, IBANs and phone numbers masked before the call, only the text needed,
   messages treated as data (not instructions), the claim matches the code. Bonus: an
   offline or cached fallback.

## Skills to watch

| Skill | What this drill tests | What to observe for the debrief |
|---|---|---|
| `/brainstorm` | Choosing one persona and one moment among customer, post-scam victim and analyst | Did they converge in time, or try to build for all three? Did the skill push "one moment"? |
| `/kickoff` | Scoping a 2 h demo with the curveball arriving mid-build | Did `PLAN.md` leave room for a false-positive path? How long did the re-scope take? |
| `/be-domain` | VoP results, Febelfin plan (planned, not law), PSD3 ⚠️, AI Act fraud exclusion, Card Stop | Did every fact on screen and in the pitch come from facts.md with the ⚠️ said aloud? Any invented KBC figures? |
| `/demo-step` | Approve / Reject before any payment action, seeded one-click cases | Is the gate in code? Does Reject really do nothing? Is there a "▶ Demo example" per planted case? |
| `/prompt-eval` | Answers in FR / NL / EN, calm tone, messages treated as data | Did the reason come out in the customer's language every time? Any caps or jargon? Did they test case E (Match but risky)? |
| `/privacy-check` | Names, IBANs, phone numbers and message text sent to a cloud model | Masking present and true to the pitch claim? Prompt injection from message text? |
| `/impact-calc` | A number from the EUR 93M sector figure with explicit assumptions | Were assumptions labelled? Any KBC figure presented as fact? |
| `/demo-hardening` | Voice (ElevenLabs) and Gemini calls cached for the stage | Does the voice line work offline from the replay cache? |
| `/pitch-rehearsal` | The 5 questions above | Did the rehearsal predict the car and VoP-Match questions? |
| `/challenge-data` | Data is given, so the skill should mostly stay idle | Did anyone regenerate data instead of using the planted cases? That is a skill-trigger problem to fix. |
