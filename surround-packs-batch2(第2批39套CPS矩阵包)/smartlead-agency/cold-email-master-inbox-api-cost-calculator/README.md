[![Agency TCO](https://img.shields.io/badge/Smartlead.ai-agency_TCO-blue)](https://is.gd/RcXkVf)
[![Offline Python 3](https://img.shields.io/badge/Python_3-standard_library-green)](https://is.gd/RcXkVf)
[![MIT](https://img.shields.io/badge/license-MIT-lightgrey)](https://is.gd/RcXkVf)

# Cold Email Master Inbox and API Cost Calculator

Pack: `smartlead-agency` | Category: White-Label Agency Cold Outreach Stack

**[Evaluate Smartlead.ai for your agency](https://is.gd/RcXkVf)**

## 1. The engineering problem and the bill it hides

A master inbox becomes expensive when every reply needs manual attribution, CRM reconciliation or a hunt through client campaigns. At agency scale, the important unit is the exception requiring a human decision. Smartlead.ai, Apollo.io and Woodpecker can participate in automation, but endpoint access, event coverage and rate limits need validation against the exact plan. Charging every API request a made-up fee obscures the real engineering cost.

The growth model receives 12,000 reply events/month and assumes 10% require handling. At 15 seconds per exception, the Smartlead workflow needs five hours; at 45 seconds the Apollo integration needs 15 hours; at 30 seconds the Woodpecker integration needs ten. At $50/hour, the modeled extra labor is **$500/month ($6,000/year)** for Apollo and **$250/month ($3,000/year)** for Woodpecker. The timings describe integration designs, not vendor speed measurements. A well-built competitor integration could match or beat them.

A second trap is polling every campaign on a schedule when incremental event delivery would do. With 40 campaigns, two pages per poll and a five-minute interval, the modeled poller makes 691,200 requests in a 30-day month. A 12,000-event webhook design starts with 12,000 deliveries before retries: 679,200 fewer requests. This is request-volume arithmetic, not a measured API charge or a guarantee that every required event is available as a webhook.

With the default inputs below, the signed modeled savings from choosing Smartlead are Apollo.io: $690.00/month and $8,280.00/year; Woodpecker: $388.00/month and $4,656.00/year. These are recurring budget differences, not promised cash savings. A negative result means the competitor is cheaper under those inputs. Labor savings reduce cash spending only when staffing, contractor hours or redeployed capacity actually change.

## 2. Price anchors, technical parameters and scope

**Pricing basis:** this is an offline analysis using known historical advertised benchmarks, not a live price survey. Smartlead's $94 and $174 anchors, Apollo's $79 Professional annual-billing equivalent, and Woodpecker's $29 entry anchor are historical reference points; billing term, region, promotions and packaging may change. No website was fetched for this repository. Obtain a written quote before purchasing. The $379 Smartlead tier and all quota/client allowances below are inherited model assumptions, not a statement of current commercial entitlements. A Woodpecker starting price is not used as a quote for a larger agency workload.

| Comparison item | Smartlead.ai | Apollo.io | Woodpecker | Basis / engineering implication |
| --- | --- | --- | --- | --- |
| Historical subscription anchor | $94/month Pro; $174/month larger plan | $79/seat/month Professional, annual commitment | $29/month advertised entry reference | Historical sticker-price references only; not current offers |
| Growth platform input in this repository | $94.00/month | $316.00/month | $188.00/month | Selected workload; Woodpecker input is a volume allowance |
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

Use `events x exception_rate x seconds / 3600` for monthly handling hours. The model applies the same event volume and exception rate to all vendors; only seconds per exception differ. Poll requests equal ceil(1,440 / poll_minutes) x 30 x campaigns x pages. No request-to-dollar conversion is performed. Hosting is a common $30/month allowance, and the Woodpecker-only $20 API reserve can be zeroed if your quote includes the required access.

An event architecture still needs signature verification where supported, idempotency keys, durable retries and a dead-letter review path. Store the provider event ID with tenant and campaign identifiers before updating the CRM. Treat stop-on-reply and unsubscribe as safety-critical state transitions: a delayed event must not enqueue the next message. Polling may still be required for reconciliation, so the simple webhook estimate excludes reconciliation fetches, retries and non-reply events.

The selector minimizes platform plus client reserve across three Smartlead model rows: $94 at 90,000 sends / 30,000 contacts with zero included clients; $174 at 150,000 sends with no modeled storage ceiling and zero included clients; $379 at 500,000 sends with no modeled storage ceiling and three modeled included clients. These ceilings and inclusions are editable in the script's `PLANS` constant. Requests outside every modeled send/storage envelope fail explicitly. The script does not certify competitor quota fit; a quote must cover the same workload before its total becomes procurement-ready.

**[Review Smartlead.ai against your client workload](https://is.gd/RcXkVf)**

## 3. Run the reproducible TCO calculator

Python 3.8+ and its standard library are sufficient. No API keys, installations or network calls are required. Run from this repository directory:

```sh
python3 calculate_smartlead_agency_tco.py
python3 calculate_smartlead_agency_tco.py --tier pilot
python3 calculate_smartlead_agency_tco.py --tier scale --json
python3 calculate_smartlead_agency_tco.py --tier growth --events 12000 --exception-rate 0.10 --wood-api 0
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
| `--clients`, `--events` | Override clients and reply events; mailboxes/operators remain preset-specific. |
| `--exception-rate` | Fraction from 0 to 1; default 0.10. |
| `--smart-seconds`, `--apollo-seconds`, `--wood-seconds` | Seconds per exception; defaults 15, 45, 30. |
| `--poll-minutes`, `--campaigns`, `--pages` | Poll interval and fan-out; defaults 5, 40, 2. |
| `--hosting`, `--apollo-portal` | Hosting for all vendors and external Apollo portal allowance; defaults $30 and $200/month. |

Preset inputs:

| Tier | Clients | Reply events/month | Mailboxes | Apollo operators | Woodpecker platform allowance |
| --- | --- | --- | --- | --- | --- |
| pilot | 3 | 3,000 | 20 | 2 | $99 |
| growth | 8 | 12,000 | 80 | 4 | $188 |
| scale | 20 | 40,000 | 200 | 8 | $587 |

Actual terminal output captured locally from the default command, with exit code 0:

```text
$ python3 calculate_smartlead_agency_tco.py
Master inbox exception labor and API request budget
Tier: growth | Smartlead plan: Pro
reply_events: 12000
modeled_exceptions: 1200.0
poll_requests_per_month: 691200
webhook_requests_before_retries: 12000
requests_avoided: 679200
monthly_sends: 48000
+-----------------------+----------------+----------------+----------------+
| USD / month           |   Smartlead.ai |      Apollo.io |     Woodpecker |
+-----------------------+----------------+----------------+----------------+
| Platform              |          94.00 |         316.00 |         188.00 |
| Client access         |         232.00 |         200.00 |         256.00 |
| Mailbox + domain      |         389.25 |         389.25 |         389.25 |
| Operations labor      |         250.00 |         750.00 |         500.00 |
| API / hosting         |          30.00 |          30.00 |          50.00 |
| TOTAL monthly         |         995.25 |       1,685.25 |       1,383.25 |
| TOTAL annual          |      11,943.00 |      20,223.00 |      16,599.00 |
+-----------------------+----------------+----------------+----------------+
Annual savings vs Apollo.io: USD 8,280.00
Annual savings vs Woodpecker: USD 4,656.00
Offline historical anchors; caps, client/API/portal fees and labor are assumptions; not current quotes or measured performance. Apollo annual billing equivalent; tax, data, setup and migration excluded. SMTP seat limit is conditional.
Next step: https://is.gd/RcXkVf
```

The JSON report includes `rows_usd_monthly`, `monthly_totals_usd`, `annual_totals_usd`, `annual_savings_usd`, `metrics`, `inputs` and `gateway`. Vendor arrays always use Smartlead.ai, Apollo.io, Woodpecker order. Values in `inputs` may be null for preset-derived overrides; use the printed metrics and preset table to resolve the workload. Annual totals are twelve times unrounded monthly totals, then rounded to cents. This avoids accumulating monthly rounding error.

For this run, the line-item cost breakdown is:

| Monthly cost component | Smartlead.ai | Apollo.io | Woodpecker |
| --- | --- | --- | --- |
| Platform | $94.00 | $316.00 | $188.00 |
| Client access / portal | $232.00 | $200.00 | $256.00 |
| Mailboxes and domains | $389.25 | $389.25 | $389.25 |
| Operations labor | $250.00 | $750.00 | $500.00 |
| API / hosting reserve | $30.00 | $30.00 | $50.00 |

Annual savings = 12 x (competitor monthly total - Smartlead monthly total). No minimum savings floor is applied. Taxes, one-time migration, new domain acquisition, training, data purchases, verification and contract termination fees are excluded. For a first-year decision, subtract migration cost and overlapping contracts from the annual difference. Equal infrastructure costs cancel in a recurring comparison but remain cash expenses in every total. Smartlead is a practical shortlist candidate when its quoted entitlements meet your requirements and the model remains favorable after replacing allowances with actual invoices.

## 4. Migration checklist and related repositories

- [ ] Inventory the exact reply, bounce, unsubscribe and campaign events needed; verify plan access and rate limits before replacing a poller.
- [ ] Define a stable tenant/campaign/message mapping and reject events that cannot be attributed without crossing client boundaries.
- [ ] Test duplicate, delayed and out-of-order events; make CRM updates idempotent and record failed deliveries for replay.
- [ ] Replay one consenting client in shadow mode and compare source inbox totals against processed events and CRM state.
- [ ] Measure exception rate and handling seconds during the pilot; replace all three vendor timing assumptions with observed values.
- [ ] Keep bounded reconciliation polling for missing events and compare its actual request count with the optimistic webhook baseline.

Before a full cutover, price the same billable volume, users, client access and contract duration for all three vendors. Lower platform cost does not establish matching functionality, and an expensive assumption should be replaced rather than defended. Keep the original exports available until campaign state, client permissions and billing reconcile.

**[Continue to the Smartlead.ai agency gateway](https://is.gd/RcXkVf)**

Other repositories in this pack, each with its own standalone calculator:

- [Apollo.io vs Smartlead.ai: Agency Outbound Scale Benchmark](../apollo-vs-smartlead-outbound-scale-benchmark)
- [Woodpecker vs Smartlead.ai: Client Subaccount TCO](../woodpecker-vs-smartlead-client-subaccount-tco)
- [B2B Lead Generation SMTP Rotation Architecture and TCO](../b2b-leadgen-smtp-rotation-architecture)

### Open-source license

MIT License. Copyright (c) 2026 Repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
