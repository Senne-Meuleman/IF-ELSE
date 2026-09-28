# Materials (SYNTHETIC)

Everything in this folder is synthetic practice data made by team IF-ELSE. The people,
accounts, companies, phone numbers and links are fictional. IBANs have a valid format
and checksum but were generated at random. Links use the reserved `.example` domain.
There are no national register numbers anywhere. Snapshot time: **28 Sep 2026, 11:00**.

| File | What it is |
|---|---|
| `customers.csv` | 10 retail customers: language, brand (KBC / CBC / KBC Brussels), digital profile, known payees, current daily transfer limit |
| `transactions.csv` | 78 outgoing transfers over the last 30 days. `status` is `booked` or `pending_review` (held by today's rules engine) |
| `vop_results.csv` | Verification of Payee result for each pending transfer |
| `events.csv` | Digital banking events: logins, new devices, limit changes, payees added |
| `messages.json` | 10 messages customers received around their transfers (SMS, email, WhatsApp; NL / FR / EN) |
| `scam_patterns.md` | A short fraud team cheat sheet |

Note on `messages.json`: for this exercise, assume customers shared these messages with
the bank (forwarded to Kate, or read out to the fraud line). In reality the bank does not
see a customer's SMS, email or WhatsApp.

CSV files start with one `#` comment line. In pandas: `pd.read_csv(path, comment="#")`.
