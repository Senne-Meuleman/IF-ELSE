# Payroll sandbox API (v0.3, hackathon edition)

> SYNTHETIC practice spec written by team IF-ELSE. Not a real SD Worx API.

This is the sandbox version of the actions our payroll platform exposes to
consultant tooling. You can implement it as local Python functions that write to
a JSON file or a SQLite table; there is no server to call. Treat it as the
contract: same names, same fields.

**Important:** the sandbox has no review or approval step of its own. A call is
a write: whatever is called is applied to the payroll data.

## Common fields (every action)

| Field | Type | Notes |
|---|---|---|
| `source_message_id` | string | The inbox message this action comes from, e.g. `MSG001`. |
| `client_id` | string | `C01`–`C04`. |
| `requested_by` | string | Sender email address as received. |

Dates are ISO `YYYY-MM-DD`. Amounts are EUR, gross, per month. `employee_id`
must exist in `employees.csv` for that `client_id`.

## Actions

### `update_address`
| Field | Required | Notes |
|---|---|---|
| `employee_id` | yes | |
| `street` | yes | Street, number and box (`bus` / `boîte`). |
| `postcode` | yes | 4 digits. |
| `city` | yes | |
| `effective_date` | yes | |

### `update_bank_account`
| Field | Required | Notes |
|---|---|---|
| `employee_id` | yes | |
| `new_iban` | yes | Belgian or SEPA IBAN, no spaces. |
| `account_holder` | yes | Name as given by the requester. |
| `effective_date` | yes | First payroll run to use the new account. |

### `register_absence` (sickness)
| Field | Required | Notes |
|---|---|---|
| `employee_id` | yes | |
| `start_date` | yes | First day of incapacity. |
| `end_date` | yes | Last day, as known today. Can be extended later. |
| `medical_certificate` | yes | `received` / `announced` / `none`. |
| `notes` | no | Free text, max 500 characters, visible to the client's HR contact and to payroll. |

### `register_leave`
| Field | Required | Notes |
|---|---|---|
| `employee_id` | yes | |
| `leave_type` | yes | `annual` / `compensatory` / `unpaid` / `other`. |
| `start_date` | yes | |
| `end_date` | yes | |
| `days` | no | Working days, if stated. |

### `request_new_hire`
Creates the employee file and queues the Dimona IN declaration.

| Field | Required | Notes |
|---|---|---|
| `first_name`, `last_name` | yes | |
| `date_of_birth` | yes | |
| `start_date` | yes | First day of work. Dimona is the immediate declaration of the hire, so it cannot be queued without it. |
| `joint_committee` | yes | e.g. `PC 124`. |
| `contract_type` | yes | `white-collar` / `blue-collar`. |
| `contract_duration` | yes | `open-ended` / `fixed-term` (+ `end_date`). |
| `weekly_hours` | yes | |
| `gross_monthly_eur` | yes | |
| `function_title` | no | |

The national register number and ID data are collected through the secure
mysdworx upload, never by email. Do not add a field for them.

### `change_salary`
| Field | Required | Notes |
|---|---|---|
| `employee_id` | yes | |
| `new_gross_monthly_eur` | yes | |
| `effective_date` | yes | |
| `reason` | no | Short text. |

### `ask_clarification`
Sends an email back to the requester. Changes no payroll data.

| Field | Required | Notes |
|---|---|---|
| `to` | yes | |
| `language` | yes | `NL` / `FR` / `EN`. Answer in the language of the email. |
| `question` | yes | |
| `missing_fields` | no | List of field names. |

### `reply_only`
Sends an informational reply. Changes no payroll data.

| Field | Required | Notes |
|---|---|---|
| `to` | yes | |
| `language` | yes | |
| `body` | yes | |

## Example

```json
{
  "action": "update_address",
  "source_message_id": "MSG000",
  "client_id": "C01",
  "requested_by": "sofie.dewilde@nuvelio.be",
  "employee_id": "E1007",
  "street": "Veldstraat 150",
  "postcode": "9000",
  "city": "Gent",
  "effective_date": "2026-10-01"
}
```
