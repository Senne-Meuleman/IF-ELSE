> Practice brief written by team IF-ELSE. Fictional: not an actual SD Worx or Tectonic brief.

# SD Worx challenge: Inbox to action

*90-minute sprint*

## Context

Every month SD Worx pays more than 6 million employees for over 100,000
organisations. In Belgium, a large part of that work happens in our SME payroll
teams. A payroll consultant looks after dozens of small and mid-sized clients:
a software company in Gent, a construction firm in Roeselare, a hotel in Namur.

Those clients do not fill in forms. They send email. "Can you change her
address?" "He's sick since Monday." "New guy starts soon, can you sort it out?"
The emails come in Dutch, French and English, often forwarded, sometimes typed
on a phone between two meetings. Our consultants read every one of them, look
up the employee, work out what has to change and type it into the payroll
system. It is careful work, and a lot of it is copy-paste.

On 24 June 2026 we launched a multi-agent payroll model: payroll professionals
manage a team of AI agents for customer interactions, knowledge retrieval and
payroll execution, and humans validate the results. About 500 payroll
consultants in our Belgian SME teams were onboarded by the end of the summer.
This challenge sits right in that model.

## The challenge

**How might we turn a payroll consultant's inbox into a queue of proposed,
structured payroll actions that the consultant can check and approve in
seconds, without ever losing control of what gets executed?**

## Who you're building for

Lien is a payroll consultant in our Belgian SME team. She has around forty
client companies. On a normal Monday she opens her inbox to 60 new emails, and
the monthly payroll run closes on the 25th. She knows her clients well, she
speaks Dutch and French and gets by in English, and she is personally
accountable for every change that reaches a payslip. She does not want an AI
that does her job. She wants one that does the typing, shows its work and
lets her decide. *(Lien and her numbers are a practice persona, not SD Worx data.)*

## What we give you

All in `materials/`. The data is synthetic.

- `inbox.json`: 15 real-looking emails from one week of Lien's inbox, 21–25 September 2026.
- `employees.csv`: the 30 employees of four client companies, with joint committee, contract type, IBAN and address.
- `clients.csv`: the four clients and their authorised HR contacts.
- `actions.md`: the actions of our payroll sandbox API, with required fields. Your agent proposes calls to these actions.

You may add data if your demo needs it. Tell us what you added.

## What success looks like for us

- Lien opens one screen and sees each email turned into a proposed action with the fields filled in, the matching employee, and why the agent thinks so.
- Nothing reaches payroll until a human says yes. Rejecting is as easy as approving.
- The agent knows when it does not know. A good "I need to ask the client" is worth more than a confident wrong change.
- It works in Dutch, French and English, and replies in the client's language.
- You can tell us, with a number you can defend, what this changes for a consultant's week.
- We would trust it with real employee data. Tell us how you handle that.

## Constraints

- Use only the synthetic data. Do not put real personal data into any tool.
- Our payroll data includes sensitive personal information. Treat it like we have to.
- Do not state Belgian labour or social security rules unless you can back them up. If you are unsure, say so.
- Keep the scope to proposing and validating actions. Calculating payslips is out of scope.

## Practical

- Language of the pitch: English.
- Pitch: 3 minutes, including a live demo, followed by 2 minutes of questions.
- Format: any stack. A working, clickable demo beats slides. Show the real flow on at least a few of the emails we gave you.
- A mentor from our payroll team is available during the sprint. Ask them anything about how consultants work today.
