# Fraud team cheat sheet (SYNTHETIC)

> Synthetic practice document written by team IF-ELSE for a drill. It is not a KBC,
> CBC or Febelfin document. Public facts are sourced from Safeonweb, Febelfin and VRT;
> everything else is illustrative.

## What we see most

| Pattern | How it starts | What the customer is pushed to do | Tell-tale signs |
|---|---|---|---|
| **Fake bank helpdesk** | Email or SMS: "a new device was added to your account", with a phone number to call | Call the "helpdesk", read out banking codes, or move money "to safety" | Urgency, a phone number that is not the one on the back of the card, a request for codes |
| **"Hi Mum / Hi Dad"** | WhatsApp from an unknown number: "my phone broke, this is my new number" | Pay an "urgent invoice" for the child, to an account that is not the child's | New number, refuses to call ("my mic is broken"), unusual account, same-day pressure |
| **itsme "update / reactivate"** | SMS or email: "your itsme expires, reactivate now" with a link, or an itsme approval the customer did not start | Enter details on a fake page, or approve an itsme request | **itsme never sends links by SMS.** An approval request you did not start |

## Useful signals in our own data
- Verification of Payee (IBAN–name check, mandatory since 9 Oct 2025). Four results:
  **Match**, **Close match** (we suggest the registered name), **No match**, **Not possible**.
  The customer decides whether to go ahead. A Match only says the name fits the account;
  it does not say the payee is honest.
- New payee, new device, unusual hour, amount far above the customer's usual pattern,
  a known payee's name on a new (or foreign) account.
- A message the customer received shortly before the transfer.

## What we tell customers
- The bank will never ask you for codes by phone, SMS or email.
- Lost card or codes shared? Call **Card Stop: 078 170 170**.
- Forward suspicious messages to **suspect@safeonweb.be**.
- When in doubt: stop, hang up, call someone you trust using a number you already have.

## Context for the team
- Phishing losses in Belgium reached **EUR 93M in 2025** (about EUR 49M in 2024), with 11,000+
  cases. Source: VRT, 8 July 2026.
- Febelfin / Minister Beenders action plan (8 July 2026): a default transfer limit of at most
  EUR 5,000 by early 2027, at least a 4-hour wait before a raised limit takes effect,
  temporary holds on suspicious payments, and a "slow banking" option. These are plans being
  rolled out, not all live today.
