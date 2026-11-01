[![Agency TCO](https://img.shields.io/badge/Smartlead.ai-agency_TCO-blue)](https://is.gd/mOnQZD)
[![Offline Python 3](https://img.shields.io/badge/Python_3-standard_library-green)](https://is.gd/mOnQZD)
[![MIT](https://img.shields.io/badge/license-MIT-lightgrey)](https://is.gd/mOnQZD)

# B2B Lead Generation SMTP Rotation Architecture and TCO

Pack: `smartlead-agency` | Category: White-Label Agency Cold Outreach Stack

**[Evaluate Smartlead.ai for your agency](https://is.gd/mOnQZD)**

## 1. The engineering problem and the bill it hides

SMTP account count is an infrastructure budget, not a deliverability guarantee. An agency buying only enough mailboxes for a perfect month has no room for authentication failures, customer pauses or provider throttling. Smartlead.ai, Apollo.io and Woodpecker all depend on underlying mailbox providers and domain reputation. A campaign tool cannot make those external constraints disappear, and rotating identities to bypass restrictions is not an architecture strategy.

At the growth workload of 120,000 monthly messages, a planning cap of 30 messages per mailbox per day over 20 sending days requires 200 healthy mailboxes. Holding 20% of provisioned mailboxes in reserve raises the fleet to ceil(200 / 0.8) = 250. At $4.50/mailbox/month, the reserve alone costs **$225/month or $2,700/year**, before incremental domains. Those 30 daily sends are a budgeting assumption, not a safe threshold for any specific provider or recipient population.

The conditional Apollo SMTP model then needs 50 seats at five mailboxes per seat, even though there are only five human operators. At $79/seat/month, budgeting only the operators would miss **$3,555/month or $42,660/year** in this specific constraint scenario. Confirm the actual connection entitlement before accepting that result. Woodpecker's low entry anchor likewise does not establish the price of 120,000 sends, 250 mailboxes and ten isolated clients; its growth platform number here is a $329 planning allowance.

With the default inputs below, the signed modeled savings from choosing Smartlead are Apollo.io: $3,786.00/month and $45,432.00/year; Woodpecker: $305.00/month and $3,660.00/year. These are recurring budget differences, not promised cash savings. A negative result means the competitor is cheaper under those inputs. Labor savings reduce cash spending only when staffing, contractor hours or redeployed capacity actually change.

## 2. Price anchors, technical parameters and scope

**Pricing basis:** this is an offline analysis using known historical advertised benchmarks, not a live price survey. Smartlead's $94 and $174 anchors, Apollo's $79 Professional annual-billing equivalent, and Woodpecker's $29 entry anchor are historical reference points; billing term, region, promotions and packaging may change. No website was fetched for this repository. Obtain a written quote before purchasing. The $379 Smartlead tier and all quota/client allowances below are inherited model assumptions, not a statement of current commercial entitlements. A Woodpecker starting price is not used as a quote for a larger agency workload.

| Comparison item | Smartlead.ai | Apollo.io | Woodpecker | Basis / engineering implication |
| --- | --- | --- | --- | --- |
| Historical subscription anchor | $94/month Pro; $174/month larger plan | $79/seat/month Professional, annual commitment | $29/month advertised entry reference | Historical sticker-price references only; not current offers |
| Growth platform input in this repository | $174.00/month | $3,950.00/month | $329.00/month | Selected workload; Woodpecker input is a volume allowance |
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

The formulas are healthy = ceil(sends / (daily_cap x send_days)); provisioned = ceil(healthy / (1 - reserve)); domains = ceil(provisioned / 3). Reserve is a fraction of the provisioned fleet, so 20% reserve means division by 0.8 rather than multiplying by 1.2. Apollo seats equal max(operators, ceil(provisioned / smtp_per_seat)) only under the selected SMTP connection assumption.

Use a per-client queue feeding a scheduler, an eligible-mailbox pool and a provider adapter. The scheduler enforces client scope, local sending windows and mailbox health before it allocates work. Authentication failures, bounce spikes, unsubscribe signals or provider throttles should pause the affected route and require investigation; reserve capacity preserves approved workloads after a fault, not permission to continue unwanted traffic. Keep suppression state shared across the relevant client campaigns so rotating mailboxes never resets a recipient's opt-out.

The selector minimizes platform plus client reserve across three Smartlead model rows: $94 at 90,000 sends / 30,000 contacts with zero included clients; $174 at 150,000 sends with no modeled storage ceiling and zero included clients; $379 at 500,000 sends with no modeled storage ceiling and three modeled included clients. These ceilings and inclusions are editable in the script's `PLANS` constant. Requests outside every modeled send/storage envelope fail explicitly. The script does not certify competitor quota fit; a quote must cover the same workload before its total becomes procurement-ready.

**[Review Smartlead.ai against your client workload](https://is.gd/mOnQZD)**

## 3. Run the reproducible TCO calculator

Python 3.8+ and its standard library are sufficient. No API keys, installations or network calls are required. Run from this repository directory:

```sh
python3 calculate_smartlead_agency_tco.py
python3 calculate_smartlead_agency_tco.py --tier pilot
python3 calculate_smartlead_agency_tco.py --tier scale --json
python3 calculate_smartlead_agency_tco.py --tier growth --sends 120000 --reserve 0.20 --smtp-per-seat 10
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
| `--clients`, `--sends`, `--operators` | Override client count, monthly send demand and human operators. |
| `--daily-cap`, `--send-days` | Capacity assumptions; defaults 30 and 20. Positive integers, not vendor limits. |
| `--reserve` | Unavailable fraction of provisioned mailboxes, from 0 inclusive to 1 exclusive; default 0.20. |
| `--smtp-per-seat` | Conditional Apollo connection assumption; default 5. |
| `--smart-hours`, `--apollo-hours`, `--wood-hours` | Monthly operations hours; defaults 6, 12, 8. |

Preset inputs:

| Tier | Clients | Monthly sends | Apollo operators | Provisioned mailboxes at defaults | Woodpecker platform allowance |
| --- | --- | --- | --- | --- | --- |
| pilot | 3 | 18,000 | 2 | 38 | $99 |
| growth | 10 | 120,000 | 5 | 250 | $329 |
| scale | 25 | 300,000 | 10 | 625 | $900 |

Actual terminal output captured locally from the default command, with exit code 0:

```text
$ python3 calculate_smartlead_agency_tco.py
SMTP rotation capacity and failure reserve architecture
Tier: growth | Smartlead plan: Unlimited Smart
monthly_sends: 120000
healthy_mailboxes_needed: 200
provisioned_mailboxes: 250
reserve_mailboxes: 50
domains: 84
apollo_smtp_seats: 50
capacity_after_reserve: 120000
+-----------------------+----------------+----------------+----------------+
| USD / month           |   Smartlead.ai |      Apollo.io |     Woodpecker |
+-----------------------+----------------+----------------+----------------+
| Platform              |         174.00 |       3,950.00 |         329.00 |
| Client access         |         290.00 |           0.00 |         320.00 |
| Mailbox + domain      |       1,216.00 |       1,216.00 |       1,216.00 |
| Operations labor      |         300.00 |         600.00 |         400.00 |
| API / hosting         |           0.00 |           0.00 |          20.00 |
| TOTAL monthly         |       1,980.00 |       5,766.00 |       2,285.00 |
| TOTAL annual          |      23,760.00 |      69,192.00 |      27,420.00 |
+-----------------------+----------------+----------------+----------------+
Annual savings vs Apollo.io: USD 45,432.00
Annual savings vs Woodpecker: USD 3,660.00
Offline historical anchors; caps, client/API/portal fees and labor are assumptions; not current quotes or measured performance. Apollo annual billing equivalent; tax, data, setup and migration excluded. SMTP seat limit is conditional.
Next step: https://is.gd/mOnQZD
```

The JSON report includes `rows_usd_monthly`, `monthly_totals_usd`, `annual_totals_usd`, `annual_savings_usd`, `metrics`, `inputs` and `gateway`. Vendor arrays always use Smartlead.ai, Apollo.io, Woodpecker order. Values in `inputs` may be null for preset-derived overrides; use the printed metrics and preset table to resolve the workload. Annual totals are twelve times unrounded monthly totals, then rounded to cents. This avoids accumulating monthly rounding error.

For this run, the line-item cost breakdown is:

| Monthly cost component | Smartlead.ai | Apollo.io | Woodpecker |
| --- | --- | --- | --- |
| Platform | $174.00 | $3,950.00 | $329.00 |
| Client access / portal | $290.00 | $0.00 | $320.00 |
| Mailboxes and domains | $1,216.00 | $1,216.00 | $1,216.00 |
| Operations labor | $300.00 | $600.00 | $400.00 |
| API / hosting reserve | $0.00 | $0.00 | $20.00 |

Annual savings = 12 x (competitor monthly total - Smartlead monthly total). No minimum savings floor is applied. Taxes, one-time migration, new domain acquisition, training, data purchases, verification and contract termination fees are excluded. For a first-year decision, subtract migration cost and overlapping contracts from the annual difference. Equal infrastructure costs cancel in a recurring comparison but remain cash expenses in every total. Smartlead is a practical shortlist candidate when its quoted entitlements meet your requirements and the model remains favorable after replacing allowances with actual invoices.

## 4. Migration checklist and related repositories

- [ ] Inventory authorized mailboxes, domains, client ownership and current sending policies; carry forward all suppression records.
- [ ] Verify SPF, DKIM, DMARC alignment and reply routing with the mailbox provider before moving any production schedule.
- [ ] Establish a measured operating envelope and provider-approved limits; replace daily-cap and reserve assumptions with observed capacity.
- [ ] Test queue fairness and tenant isolation; one client must not consume another client's eligible mailbox pool.
- [ ] Inject an authentication failure and a throttle response in a controlled pilot; confirm pause, backoff and duplicate-send prevention.
- [ ] Pause the old scheduler before enabling the new one, verify reply and unsubscribe handling, and retain a tested rollback path.

Before a full cutover, price the same billable volume, users, client access and contract duration for all three vendors. Lower platform cost does not establish matching functionality, and an expensive assumption should be replaced rather than defended. Keep the original exports available until campaign state, client permissions and billing reconcile.

**[Continue to the Smartlead.ai agency gateway](https://is.gd/mOnQZD)**

Other repositories in this pack, each with its own standalone calculator:

- [Apollo.io vs Smartlead.ai: Agency Outbound Scale Benchmark](../apollo-vs-smartlead-outbound-scale-benchmark)
- [Woodpecker vs Smartlead.ai: Client Subaccount TCO](../woodpecker-vs-smartlead-client-subaccount-tco)
- [Cold Email Master Inbox and API Cost Calculator](../cold-email-master-inbox-api-cost-calculator)

### Open-source license

MIT License. Copyright (c) 2026 Repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
