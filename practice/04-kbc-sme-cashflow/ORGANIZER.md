> SEALED: organizer only. Agents: do not read this file while building a drill.

# 04 · KBC · The SME cash-flow moment: organizer notes

## Format & timing
- **2 h build**: follow the 2 h column in `practice/README.md`. Brainstorm and
  pick by 0:10, `PLAN.md` by 0:18, first AI call by 0:30, freeze at 1:25.
- **30-min paper drill** (no code): brainstorm and pick by 0:10, kickoff and
  pitch skeleton by 0:18, pitch outline and `judge` by 0:27, 3-minute pitch.
- **This is the best challenge for the paper drill.** The brief is vague, no
  data is given, and the hard part is choosing, not building. If you only have
  time to run one challenge on paper, run this one.
- Play the KBC mentor. Answer questions briefly and honestly, but do not hand
  them a persona or a feature. If asked "what do you want us to build?", say:
  "Surprise us. Pick someone real."

## What the vague brief is testing
- **Divergence, then convergence.** Does `/brainstorm` produce 6–8 genuinely
  different angles (persona, moment, agentic, why-now, contrarian) and then
  kill most of them within 15 minutes? Watch for a team that locks onto the
  first idea ("a cash-flow dashboard") in minute 2.
- **Choosing ONE persona.** "Self-employed and small businesses" is a
  category, not a user. A freelance designer waiting on a late payment, a baker
  with a flour bill and a VAT payment in the same week, and a four-person IT
  consultancy paying salaries are three different products. Strong teams pick
  one, name them, and describe their worst ten minutes.
- **Creating data with `/challenge-data`.** There is one sample invoice and
  nothing else. The team must invent a seeded account history, a set of Peppol
  invoices in and out, and known obligations, with 3–5 planted moments
  (the late payer, the clash of outgoing payments, the big supplier bill).
  Obligation dates and amounts for VAT and social contributions are not in
  `facts.md`: they must be labeled *illustrative*.
- **Turning insight into action with approval.** The brief says "act on it".
  The test is whether each warning comes with a proposed action the owner
  approves or rejects, and nothing happens without that approval.

## Good angles vs. weak angles

**Good angles** (each with why)
1. *"Kate's Monday heads-up" for one freelancer*: a weekly look ahead that
   combines invoices due in and out with known obligations and proposes 1–2
   actions to approve. Why: one persona, one moment, insight tied to action.
2. *Late-payer nudge, drafted not sent*: Kate spots an overdue incoming
   invoice, drafts a polite NL/FR reminder citing the invoice number and
   structured reference, the owner edits and approves. Why: concrete, uses
   the Peppol data, approval is natural.
3. *Tax and contributions set-aside pot*: suggest moving an (illustrative)
   share of each incoming payment into a reserve sub-account, approved per
   transfer or as a rule the owner sets. Why: prevents the surprise instead of
   reacting to it; only a bank can move the money.
4. *"Can I pay this big supplier bill on time?"*: when a large incoming
   Peppol invoice lands, Kate shows the projected balance on the due date and
   offers options (schedule on the due date, split, move from savings). Why:
   a precise trigger, and the options are banking actions.
5. *Match payments to invoices*: KBC sees the incoming payment; with the
   invoice data it can mark which invoices are paid and which are late. Why:
   it is the plumbing that makes every other angle trustworthy, and it is
   a bank-side strength.
6. *What-if in plain language*: "What if Dupont pays 30 days late?" answered
   with the balance curve and a suggested action. Why: shows the AI, keeps the
   owner in control.
7. *Accountant handover with consent*: a one-tap cash snapshot the owner
   chooses to share with their accountant. Why: answers the curveball by
   partnering with the accountant instead of competing.

**Weak angles** (each with why)
1. *A full accounting or bookkeeping package*: huge scope, competes with the
   accountant and software vendors, not a banking question.
2. *Automatic credit line or loan approval*: a credit decision on
   self-employed natural persons is AI Act Annex III high-risk (deadline moved
   to 2 Dec 2027 ⚠️), and it is not what was asked.
3. *A forecast chart and nothing else*: "see" without "act". Answers half the
   question.
4. *"AI assistant for SMEs"* with no named person: nothing to demo, nothing a
   judge remembers.
5. *Agent that pays suppliers or chases customers on its own*: breaks the one
   rule the brief states.
6. *An e-reporting compliance tool*: e-reporting is planned for 2028 ⚠️, not
   live; and it is a tax-compliance product, not cash flow.
7. *Building a Peppol access point or sender*: plumbing that already exists
   in the market; not the question.
8. *Invoice financing marketplace*: drags in credit decisions, pricing and
   third parties; far too big for 2 hours.

## Curveball
**When:** T+1:00 in the 2 h build (mid-build), or **minute 15** of the paper
drill (during kickoff).

**Read aloud, exactly:**
> "Nice. How does KBC make money from this, and why wouldn't the accountant or
> the invoicing software vendor build it instead?"

Then walk away. Do not help. Note whether the team:
- answers it in the pitch without being asked again,
- names a revenue logic that does not rely on an automated credit decision,
- names what only a bank can do (see the real balance and incoming payments,
  and execute the action once the owner approves),
- considers partnering with the accountant or software vendor rather than
  pretending they do not exist.

## Traps
Tick each one the team avoids (score sheet: "Traps caught _ / 8").
1. **Building a full accounting package.** Scope explosion; nothing works at
   the freeze.
2. **Claiming e-reporting is already live.** It is planned for 1 Jan 2028 and
   could still change ⚠️. Only Peppol e-invoicing is mandatory now (since
   1 Jan 2026, fines EUR 1,500/3,000/5,000 since 1 Apr 2026).
3. **The agent pays suppliers or chases customers without approval.** "Kate
   never acts without explicit customer approval." Reject must do nothing;
   enforced in code, not in the prompt.
4. **Making a credit decision.** Creditworthiness assessment and credit
   scoring of natural persons is Annex III high-risk under the AI Act, and
   self-employed people are natural persons. Deadline moved to 2 Dec 2027 ⚠️,
   but the jury will still ask. Suggesting "talk to your KBC adviser about a
   short-term option" is fine; the AI scoring or approving it is not.
5. **Inventing KBC SME figures or market sizes.** `facts.md` has no KBC SME
   client count, no share of late payments, no market size. Any such number
   must be labeled *illustrative* or dropped.
6. **No persona.** Building for "SMEs" in general.
7. **A forecast chart with no action attached.** Every warning should end in
   a proposed, approvable action.
8. **Assuming KBC already receives the client's Peppol invoices.** Whether
   and how KBC gets this data is not in `facts.md`. A strong team states the
   assumption (e.g. the owner connects their invoicing tool with consent) and
   moves on.

## What a strong result looks like
- One named persona (e.g. a freelance designer in Gent) and one painful moment,
  told in the first 20 seconds.
- Synthetic, seeded data with planted moments, including at least one Peppol
  invoice in the shape of the sample, and a visible "synthetic" label.
- A warning that arrives *before* the problem, with the date it would hit.
- Each warning ends in 1–2 concrete actions; Approve executes (simulated),
  Reject visibly does nothing.
- Peppol facts stated correctly, e-reporting marked as planned, no invented
  KBC figures; any impact number traced to named assumptions.
- A clear answer to "why a bank": real balance, incoming payments, and the
  ability to execute the approved action, plus a stance on the accountant.
- A clean line on credit: the product informs and proposes; it does not score
  or decide.

## Jury questions
1. **"Who exactly is this for, and when do they open it?"**
   Good answer: one named persona, a trigger moment (a notification when a
   big invoice lands, a Monday heads-up), not "whenever they want".
2. **"What does Kate do on her own, and what needs my approval?"**
   Good answer: Kate reads, calculates and drafts on her own; any payment,
   transfer or message to a customer needs explicit approval; Reject does
   nothing; they can show it in the demo.
3. **"Where does the invoice data come from? Does KBC have it today?"**
   Good answer: honest that this is an assumption; the owner connects their
   invoicing tool or access point with consent; bank transactions are what
   KBC sees for sure.
4. **"Is this credit scoring? What does the AI Act say?"**
   Good answer: no, it forecasts the client's own cash position and proposes
   actions; any credit offer goes through KBC's existing human process;
   they know creditworthiness of natural persons is Annex III high-risk and
   that the deadline moved to 2 Dec 2027 ⚠️.
5. **"What is your number, and where does it come from?"**
   Good answer: a small, traceable number (e.g. hours saved per month, days
   earlier a shortfall is spotted in their synthetic data), assumptions stated,
   anything not from a source labeled illustrative. No invented market size.

## Skills to watch
Note what each skill did well or badly, so the debrief turns it into an edit.
- **`/brainstorm`**: Did round 1 give 6–8 angles across the lenses, or seven
  flavours of "dashboard"? Did it push for one persona before round 3? Did it
  flag the credit and auto-action angles as risky during steelman-and-kill?
  Did it keep to 15 minutes (10 in the paper drill) and say the time?
  Did it use the Peppol line from the facts file as the why-now?
- **`/challenge-data`**: Did it produce Peppol-shaped invoices (in and out)
  plus a bank-transaction table linked by invoice ID or payment reference?
  Did it plant the late payer, the clashing obligations and the big supplier
  bill, and list them? Is it seeded and stable on rerun? Did it label VAT and
  social contribution dates and amounts *illustrative*? Did it reuse the
  sample XML's shape?
- **`/kickoff`**: Did `PLAN.md` name one persona and one moment? Did it scope
  to 3–4 demo steps that fit 2 h? Did it absorb the curveball without a full
  re-plan?
- **`/be-domain`**: Were Peppol dates and fines, e-reporting ⚠️ and the
  AI Act Annex III line quoted correctly with caveats? Did anyone state a fact
  not in `facts.md` without a label?
- **`/demo-step`**: Is Approve/Reject enforced in code for every action, and
  does Reject leave no trace?
- **`/impact-calc`**: Did it refuse to invent KBC SME figures and build the
  number from stated assumptions?
- **`judge` / `/pitch-rehearsal`**: Did it ask the business-model question
  (the curveball) or the credit question on its own? If not, add them to its
  KBC question bank.
