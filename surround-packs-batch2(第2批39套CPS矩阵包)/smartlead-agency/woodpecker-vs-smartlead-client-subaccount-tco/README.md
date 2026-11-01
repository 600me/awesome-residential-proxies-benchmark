[![Agency TCO](https://img.shields.io/badge/Smartlead.ai-agency_TCO-blue)](https://is.gd/3awPq2)
[![Offline Python 3](https://img.shields.io/badge/Python_3-standard_library-green)](https://is.gd/3awPq2)
[![MIT](https://img.shields.io/badge/license-MIT-lightgrey)](https://is.gd/3awPq2)

# Woodpecker vs Smartlead.ai: Client Subaccount TCO

Pack: `smartlead-agency` | Category: White-Label Agency Cold Outreach Stack

**[Evaluate Smartlead.ai for your agency](https://is.gd/3awPq2)**

## 1. The engineering problem and the bill it hides

A white-label agency does not sell just email delivery. It sells client separation, controlled approvals and reporting that a customer can inspect without seeing another customer's prospects. A low entry subscription from Woodpecker or Apollo.io does not by itself establish the price of that operating model. Conversely, unlimited mailbox connections in a Smartlead.ai subscription do not mean free mailboxes, free domains, or free branded client access.

The growth scenario has 20 active clients. The modeled Woodpecker client-access reserve is 20 x $32 = **$640/month or $7,680/year**, in addition to a $188 volume subscription allowance. Both numbers are planning inputs rather than a verified Woodpecker agency quote. They expose a common hidden-bill trap: approving a base subscription while leaving per-client access outside the budget. Smartlead receives its own client reserve, 20 x $29 = $580/month, so the comparison does not make white-label access disappear.

Apollo's growth alternative budgets five $79 operator seats, $200/month for an external portal and 20 operating hours at $50/hour. That portal amount is a build/hosting allowance, not a native Apollo product or promise of tenant isolation. The Smartlead workflow assumes eight operating hours. The 12-hour labor difference alone represents **$600/month or $7,200/year** of avoidable work if your own timed trial reproduces it. These are labor scenarios, not measured vendor performance.

With the default inputs below, the signed modeled savings from choosing Smartlead are Apollo.io: $521.00/month and $6,252.00/year; Woodpecker: $274.00/month and $3,288.00/year. These are recurring budget differences, not promised cash savings. A negative result means the competitor is cheaper under those inputs. Labor savings reduce cash spending only when staffing, contractor hours or redeployed capacity actually change.

## 2. Price anchors, technical parameters and scope

**Pricing basis:** this is an offline analysis using known historical advertised benchmarks, not a live price survey. Smartlead's $94 and $174 anchors, Apollo's $79 Professional annual-billing equivalent, and Woodpecker's $29 entry anchor are historical reference points; billing term, region, promotions and packaging may change. No website was fetched for this repository. Obtain a written quote before purchasing. The $379 Smartlead tier and all quota/client allowances below are inherited model assumptions, not a statement of current commercial entitlements. A Woodpecker starting price is not used as a quote for a larger agency workload.

| Comparison item | Smartlead.ai | Apollo.io | Woodpecker | Basis / engineering implication |
| --- | --- | --- | --- | --- |
| Historical subscription anchor | $94/month Pro; $174/month larger plan | $79/seat/month Professional, annual commitment | $29/month advertised entry reference | Historical sticker-price references only; not current offers |
| Growth platform input in this repository | $94.00/month | $395.00/month | $188.00/month | Selected workload; Woodpecker input is a volume allowance |
| Billing unit modeled | One platform plus active-client reserve | Paid seats; capacity constraint where stated | Volume platform plus active-client reserve | These are different purchasing units |
| Client access reserve | $29/active client/month | External portal allowance, or excluded where stated | $32/active client/month | Scenario reserves; verify branding and permissions separately |
| Sending/storage ceilings in local selector | 90k/30k; 150k/unbounded; 500k/unbounded | No quota validation implemented | No quota validation implemented | Model ceilings only; unbounded storage is not a vendor promise |
| Custom SMTP capacity | Mailboxes have external provider costs | Seat formula conditional on `--smtp-per-seat` where exposed | Mailboxes have external provider costs | Confirm actual connection and volume entitlements |
| Inbox/API design | Centralized inbox-oriented candidate | Engagement plus data workflow | Campaign and agency workflow | Test exact endpoints, event scope and rate limits |
| Extra API-access allowance | $0 | $0 | $20/month | Unknown charges can exist for all; Woodpecker reserve is editable |
| Mailbox infrastructure | $4.50/mailbox/month | $4.50/mailbox/month | $4.50/mailbox/month | Common assumption, not a bundled platform entitlement |
| Domain infrastructure | $13/domain/year | $13/domain/year | $13/domain/year | Shared cost; three mailboxes per domain in this model |
| Prospect enrichment and verification | Excluded | Excluded, despite possible bundled value | Excluded | Add a comparable data budget for a full acquisition-stack TCO |
| Measured deliverability or throughput | Not measured | Not measured | Not measured | Local financial model, not a production send test |

The central distinction is contracted versus active clients. `--inactive` removes paused clients from modeled platform client fees and forecast sends, while retaining all preset mailboxes and domains. No mailbox savings occur until you actually deprovision those resources. Default growth sends are 20 x 1,800 = 36,000/month, with 20 x 600 stored contacts. The plan selector considers those two quantities and the model's client allowance.

For example, `--clients 20 --inactive 5` bills 15 active clients in this model. It assumes paused clients stop generating all incremental access charges; a vendor contract may behave differently. Change the fee inputs or use the full contracted count if paused tenants remain billable. Branding, scoped API access and customer-facing reports must be checked individually; an agency add-on does not automatically prove all three.

The selector minimizes platform plus client reserve across three Smartlead model rows: $94 at 90,000 sends / 30,000 contacts with zero included clients; $174 at 150,000 sends with no modeled storage ceiling and zero included clients; $379 at 500,000 sends with no modeled storage ceiling and three modeled included clients. These ceilings and inclusions are editable in the script's `PLANS` constant. Requests outside every modeled send/storage envelope fail explicitly. The script does not certify competitor quota fit; a quote must cover the same workload before its total becomes procurement-ready.

**[Review Smartlead.ai against your client workload](https://is.gd/3awPq2)**

## 3. Run the reproducible TCO calculator

Python 3.8+ and its standard library are sufficient. No API keys, installations or network calls are required. Run from this repository directory:

```sh
python3 calculate_smartlead_agency_tco.py
python3 calculate_smartlead_agency_tco.py --tier pilot
python3 calculate_smartlead_agency_tco.py --tier scale --json
python3 calculate_smartlead_agency_tco.py --tier growth --clients 20 --inactive 5 --wood-client-fee 0
python3 calculate_smartlead_agency_tco.py --help
```

The executable bit also permits `./calculate_smartlead_agency_tco.py`. `--tier` changes the workload; numeric flags override only the named input, so changing client count does not automatically resize every mailbox fleet or Woodpecker allowance. Money/rate inputs must be finite and nonnegative. Positive-count flags reject zero. JSON is printed to stdout and can be piped directly to another local tool.

| Option | Meaning and default |
| --- | --- |
| `--tier {pilot,growth,scale}` | Workload preset; default `growth`. These are local scenarios, not vendor subscription names. |
| `--json` | Emit exactly one JSON document instead of the ASCII bill; includes the gateway and signed annual savings. |
| `--hourly-rate` | Cost of operations labor, $50/hour. |
| `--mailbox-price`, `--domain-year` | Common provider costs, $4.50/mailbox/month and $13/domain/year; three mailboxes per domain. |
| `--apollo-seat-price` | $79/month equivalent of historical annually billed Professional; no annual discount is invented for other vendors. |
| `--smart-pro-price`, `--smart-scale-price`, `--smart-prime-price` | Smartlead platform price inputs: $94, $174, $379/month. |
| `--smart-client-fee`, `--wood-client-fee` | Modeled per-active-client reserves: $29 and $32/month. Set either to 0 if covered by your quote. |
| `--wood-base` | Replace the tier-specific Woodpecker volume allowance; this is not an inferred official volume tier. |
| `--wood-api` | Extra API-access reserve, $20/month; set to 0 when access is included. |
| `--clients` | Total contracted clients; default is preset-specific. |
| `--inactive` | Nonnegative integer below contracted clients; default 0. Mailboxes stay provisioned. |
| `--mailboxes`, `--operators` | Override retained mailboxes and Apollo human seats. |
| `--apollo-portal` | External portal allowance, $200/month; not a quoted Apollo feature. |
| `--smart-hours`, `--apollo-hours`, `--wood-hours` | Monthly operating hours; defaults 8, 20, 10. |

Preset inputs:

| Tier | Contracted clients | Retained mailboxes | Apollo operators | Sends per active client | Woodpecker platform allowance |
| --- | --- | --- | --- | --- | --- |
| pilot | 5 | 15 | 2 | 1,800/month | $99 |
| growth | 20 | 60 | 5 | 1,800/month | $188 |
| scale | 50 | 150 | 10 | 1,800/month | $587 |

Actual terminal output captured locally from the default command, with exit code 0:

```text
$ python3 calculate_smartlead_agency_tco.py
Active client and white-label subaccount TCO
Tier: growth | Smartlead plan: Pro
contracted_clients: 20
active_clients: 20
paused_clients: 0
monthly_sends: 36000
mailboxes_retained: 60
apollo_operator_seats: 5
+-----------------------+----------------+----------------+----------------+
| USD / month           |   Smartlead.ai |      Apollo.io |     Woodpecker |
+-----------------------+----------------+----------------+----------------+
| Platform              |          94.00 |         395.00 |         188.00 |
| Client access         |         580.00 |         200.00 |         640.00 |
| Mailbox + domain      |         291.67 |         291.67 |         291.67 |
| Operations labor      |         400.00 |       1,000.00 |         500.00 |
| API / hosting         |           0.00 |           0.00 |          20.00 |
| TOTAL monthly         |       1,365.67 |       1,886.67 |       1,639.67 |
| TOTAL annual          |      16,388.00 |      22,640.00 |      19,676.00 |
+-----------------------+----------------+----------------+----------------+
Annual savings vs Apollo.io: USD 6,252.00
Annual savings vs Woodpecker: USD 3,288.00
Offline historical anchors; caps, client/API/portal fees and labor are assumptions; not current quotes or measured performance. Apollo annual billing equivalent; tax, data, setup and migration excluded. SMTP seat limit is conditional.
Next step: https://is.gd/3awPq2
```

The JSON report includes `rows_usd_monthly`, `monthly_totals_usd`, `annual_totals_usd`, `annual_savings_usd`, `metrics`, `inputs` and `gateway`. Vendor arrays always use Smartlead.ai, Apollo.io, Woodpecker order. Values in `inputs` may be null for preset-derived overrides; use the printed metrics and preset table to resolve the workload. Annual totals are twelve times unrounded monthly totals, then rounded to cents. This avoids accumulating monthly rounding error.

For this run, the line-item cost breakdown is:

| Monthly cost component | Smartlead.ai | Apollo.io | Woodpecker |
| --- | --- | --- | --- |
| Platform | $94.00 | $395.00 | $188.00 |
| Client access / portal | $580.00 | $200.00 | $640.00 |
| Mailboxes and domains | $291.67 | $291.67 | $291.67 |
| Operations labor | $400.00 | $1,000.00 | $500.00 |
| API / hosting reserve | $0.00 | $0.00 | $20.00 |

Annual savings = 12 x (competitor monthly total - Smartlead monthly total). No minimum savings floor is applied. Taxes, one-time migration, new domain acquisition, training, data purchases, verification and contract termination fees are excluded. For a first-year decision, subtract migration cost and overlapping contracts from the annual difference. Equal infrastructure costs cancel in a recurring comparison but remain cash expenses in every total. Smartlead is a practical shortlist candidate when its quoted entitlements meet your requirements and the model remains favorable after replacing allowances with actual invoices.

## 4. Migration checklist and related repositories

- [ ] Export a per-client inventory: contacts, campaigns, suppression lists, billing state, credentials owner and authorized viewers.
- [ ] Verify tenant isolation using two test clients: client A must not read client B's contacts, replies, exports or API results.
- [ ] Confirm whether brand removal, custom domains, client seats and reporting each require a separate paid entitlement.
- [ ] Obtain written cancellation rules for paused clients and test them against a first-month invoice before relying on the inactive-client model.
- [ ] Map each mailbox to exactly one intended client boundary; transfer ownership without copying credentials into this repository.
- [ ] Test approvals, stop-on-reply and reporting with a pilot client; retain exports until invoice and client acceptance checks pass.

Before a full cutover, price the same billable volume, users, client access and contract duration for all three vendors. Lower platform cost does not establish matching functionality, and an expensive assumption should be replaced rather than defended. Keep the original exports available until campaign state, client permissions and billing reconcile.

**[Continue to the Smartlead.ai agency gateway](https://is.gd/3awPq2)**

Other repositories in this pack, each with its own standalone calculator:

- [Apollo.io vs Smartlead.ai: Agency Outbound Scale Benchmark](../apollo-vs-smartlead-outbound-scale-benchmark)
- [Cold Email Master Inbox and API Cost Calculator](../cold-email-master-inbox-api-cost-calculator)
- [B2B Lead Generation SMTP Rotation Architecture and TCO](../b2b-leadgen-smtp-rotation-architecture)

### Open-source license

MIT License. Copyright (c) 2026 Repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
