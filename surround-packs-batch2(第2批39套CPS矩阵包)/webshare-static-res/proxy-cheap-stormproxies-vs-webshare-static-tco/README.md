[![Webshare comparison](https://img.shields.io/badge/Webshare-compare_reference_costs-blue)](https://go.272738.xyz/webshare)
[![Python standard library](https://img.shields.io/badge/Python-3.9%2B_standard_library-green)](https://go.272738.xyz/webshare)

# Static Residential TCO: Webshare vs Proxy-Cheap and StormProxies

Offline, reproducible engineering comparison for **Verified Static Residential & High-Concurrency Datacenter Proxies**. Pack: `webshare-static-res`. This repository is independently runnable and contains its own calculator. Replace reference inputs with procurement and pilot evidence before selecting inventory.

**[Compare Webshare allocation options](https://go.272738.xyz/webshare)**

## 1. The engineering loss this repository makes visible

A nightly catalog monitor can complete its HTTP calls and still miss its delivery window. Replacing unstable sessions, restarting stalled workers, and reconciling invoices consume hours that never appear in a per-IP headline. At 500 endpoints, the Webshare static-residential reference allocation costs $150/month, versus $745/month using the Proxy-Cheap reference input. That acquisition difference is $595/month or $7,140/year. If a migration also avoids three troubleshooting hours at $60/hour, the hypothetical difference becomes $775/month or $9,300/year. Those extra hours are a staffing assumption, not a measured vendor defect.

When evaluating Proxy-Cheap and StormProxies, investigate product mismatch, minimum purchase increments, renewal terms, paid idle capacity, and replacement eligibility. These are possible budget traps to check, not allegations of undisclosed fees. StormProxies' historical $10-for-five private datacenter reference package is a different inventory class from ISP-hosted static residential addresses. Scaling that reference to 500 addresses gives $1,000/month, but does not establish residential equivalence or availability at that scale. Buying the wrong network class can erase an apparent discount.

Keep identity requirements separate from transport performance. For each quote, record the purchased network class, observed ASN, region, allocation lifetime, exclusivity, and replacement policy. An ASN lookup alone cannot prove a residential subscriber connection or ethical sourcing. Require supplier evidence before labeling an allocation verified static residential.

The calculator rounds Webshare static inventory to blocks of 20 and StormProxies private datacenter inventory to blocks of five. Proxy-Cheap is normalized per address. Begin with equal delivered-job demand and equal retry assumptions. Change failure rates only after a matched workload supplies evidence. The acquisition gap does not predict success on any particular destination.

## 2. Price and technical comparison

**Offline price provenance.** No vendor pages were fetched for this pack. These are remembered historical entry-price reference points, not independently verified current quotes: Webshare shared datacenter at $2.99 per 100 addresses/month and static residential at $6 per 20 addresses/month; Proxy-Cheap reference inputs of $0.30 per datacenter address/month and $1.49 per static-residential address/month; StormProxies private datacenter at $10 per five addresses/month. The Proxy-Cheap inputs particularly need confirmation against an actual quote. Dates, regions, stock, tax, bandwidth entitlement, and contract eligibility have not been verified. Linear scaling assumes no volume discount. Replace the inputs with written quotes before purchasing. No supplier invoice or live measurement is claimed.

"Verified" names an acceptance requirement, not a certification of any provider. Static residential/ISP hosting, shared datacenter, private datacenter, and rotating residential are separate inventory classes. No like-for-like StormProxies static-residential price has been established here. Unknown technical parameters are marked for verification rather than invented. This independent comparison may use a referral gateway; it does not verify the gateway's commercial terms.

| Metric | Webshare | Proxy-Cheap | StormProxies | Interpretation and verification |
|---|---|---|---|---|
| Historical static residential reference | $6 / 20 IPs / month | $1.49 / IP / month reference | No equivalent price established | Verify ISP hosting and current quote |
| Historical datacenter reference | $2.99 / 100 IPs / month, shared | $0.30 / IP / month reference | $10 / 5 IPs / month, private | Shared and private differ |
| Modeled product in this CLI | Static residential | Static residential reference | Private datacenter comparator | StormProxies is not a residential substitute |
| Default 500-IP acquisition / month | $150.00 | $745.00 | $1,000.00 | Linear reference model, not a volume quote |
| Allocation block assumed | 20 IPs | 1 IP | 5 IPs | Verify actual minimum and stock |
| Protocol acceptance | Verify purchased HTTP/SOCKS support | Verify purchased HTTP/SOCKS support | Verify purchased protocol support | No cross-product guarantee |
| Concurrency and bandwidth | Verify selected plan | Verify selected plan | Verify selected plan | No invented unlimited entitlement |
| Address persistence and replacement | Verify contract and pilot | Verify contract and pilot | Verify contract and pilot | Static does not imply permanent ownership |
| Measured ban rate and p95 | Not measured | Not measured | Not measured | Default 2% failure is a neutral assumption |
| Promotion assumed by default | 0%; explicit opt-in | None modeled | None modeled | No guaranteed 25% offer |


Use all three suppliers' actual quotes for a procurement decision. Successful-job cost, workload suitability, and replacement terms can outweigh unit price. No refund, throughput, geographic coverage, or destination acceptance guarantee is inferred from the historical prices.

**[Check Webshare pricing and eligibility before budgeting](https://go.272738.xyz/webshare)**

## 3. Run the TCO calculator

Requires Python 3.9 or later. There are no dependencies to install, no credentials to supply, and no network calls. `calculate_webshare_static_res_tco.py` uses only the Python standard library and is executable.

```sh
python3 calculate_webshare_static_res_tco.py
python3 calculate_webshare_static_res_tco.py --tier starter
python3 calculate_webshare_static_res_tco.py --tier scale --json
./calculate_webshare_static_res_tco.py --help
```

| Argument | Default | Meaning |
|---|---|---|
| `--tier starter\|growth\|scale` | `growth` | 100 / 500 / 2,000 requested IPs; local presets, not vendor tiers |
| `--ips N` | Tier count | Positive count override; allocation blocks still round up |
| `--json` | Off | One JSON document, including annual savings and gateway |
| `--webshare-price USD` | `0.30` | Monthly price per billed Webshare address |
| `--proxy-cheap-price USD` | `1.49` | Monthly price per billed Proxy-Cheap address |
| `--storm-price USD` | `2.00` | Monthly price per billed StormProxies address |
| `--discount-percent P` | `0` | Conditional Webshare acquisition discount, 0 through 100 |
| `--discount-months M` | `1` | Eligible invoices in year one, 0 through 12; 0 disables discount |
| `--jobs N` | `1000000` | Desired successful jobs per month, nonnegative |
| `--retry-cost USD` | `0.002` | Marginal cost of one extra attempt |
| `--hours H` | `2` | Monthly operator hours, equal across providers |
| `--hourly-rate USD` | `60` | Cost per operator hour |
| `--webshare-failure P` | `0.02` | Attempt-failure probability, 0 inclusive to 1 exclusive |
| `--proxy-cheap-failure P` | `0.02` | Proxy-Cheap attempt-failure probability |
| `--storm-failure P` | `0.02` | StormProxies attempt-failure probability |
| `--samples PATH` | None | Local latency JSON; supplied providers override failure inputs |


Monetary arithmetic uses Decimal, with final values rounded to cents. JSON money fields are decimal strings to preserve cents. Invalid tiers, negative or nonfinite numbers, invalid sample files, and failure probabilities of 1 or greater produce argparse exit code 2. A valid default invocation exits 0. Output labels distinguish requested endpoints from rounded billed inventory.

The monthly model is `rounded_allocation * unit_price + jobs * p / (1 - p) * retry_cost + hours * hourly_rate`. Month 1 subtracts the selected discount only when at least one invoice is eligible. Year 1 is twelve baseline months minus `base_proxy_bill * discount_percent / 100 * discount_months`. Savings equal comparator year-one TCO minus Webshare year-one TCO. A negative number means Webshare costs more under those inputs. Discounted year-one savings are not necessarily twelve times the first-month gap.

Intermediate values are not rounded, so the displayed annual total can differ from twelve displayed rounded monthly totals by a few cents. Retry expense represents marginal compute, queueing, or incremental traffic; do not count traffic already included in a base plan twice. Taxes, additional base traffic charges, contract credits, and one-time migration fees are excluded. Operator hours start equal across suppliers. This is a scenario calculator, not a measurement of supplier quality or a profitability guarantee.

### Actual default terminal output

This output was captured by executing this repository's script locally:

```console
$ python3 calculate_webshare_static_res_tco.py
Scenario: static-residential procurement | tier=growth | requested_ips=500
OFFLINE MODEL: unverified reference prices; mixed network classes; no measured ban rates.
+---------------+----------+----------+----------+----------+------------+-------------+
| Provider      | Base/mo  | Retry/mo | Labor/mo | Month 1  | Year 1     | Billed IPs  |
+---------------+----------+----------+----------+----------+------------+-------------+
| Webshare      |   150.00 |    40.82 |   120.00 |   310.82 |    3729.80 |         500 |
| Proxy-Cheap   |   745.00 |    40.82 |   120.00 |   905.82 |   10869.80 |         500 |
| StormProxies  |  1000.00 |    40.82 |   120.00 |  1160.82 |   13929.80 |         500 |
+---------------+----------+----------+----------+----------+------------+-------------+
USD; Month 1 applies the discount only if eligible months > 0.
Year-one savings choosing Webshare vs Proxy-Cheap: $7140.00
Year-one savings choosing Webshare vs StormProxies: $10200.00
Compare the actual allocation and renewal quote: https://go.272738.xyz/webshare
```

### Replace prices with a written quote

```sh
python3 calculate_webshare_static_res_tco.py --ips 501 --webshare-price 0.35 --proxy-cheap-price 1.20 --storm-price 1.80 --hours 4 --hourly-rate 60 --json
```

These command-line rates are hypothetical negotiated inputs. Under the documented allocation assumptions, 501 requested endpoints produce billed quantities of 520, 501, and 505 respectively. Change the script's `BLOCKS` tuple if the written contract uses different package increments. Changing per-address prices alone does not change quantity rounding. A static residential offer should be compared with the same network class before using any calculated difference as a purchase justification.


## 4. Migration checklist and related repositories

- [ ] Export endpoint counts, allocation lifetimes, countries, and current invoices.
- [ ] Confirm that static means the same allocation duration in every quote.
- [ ] Obtain evidence of ISP hosting, exclusivity, and replacement eligibility.
- [ ] Run an authorized canary with identical destinations, payload sizes, and concurrency.
- [ ] Compare successful deliveries, p95 latency, invoices, and operator hours.
- [ ] Move a small traffic slice first and preserve a working rollback allocation.
- [ ] Recalculate at the renewal price after the first billing cycle.

Acceptance requires the purchased inventory class, intended region, allocation lifetime, and an authorized workload at planned concurrency. Keep credentials in the existing secret store; redact usernames, passwords, and credential-bearing URLs from traces and issue reports. Local calculation does not verify network provenance. A migration should retain a working rollback pool until its agreed acceptance criteria pass.

**[Review Webshare and begin with a sized pilot](https://go.272738.xyz/webshare)**

### Continue the comparison series

- [Webshare Referral: Conditional 25 Percent Off Tier Calculator](../webshare-referral-25-percent-off-tier-calculator)
- [Dedicated vs Shared Datacenter Proxies: Ban-Rate Break-Even](../dedicated-vs-shared-datacenter-proxy-ban-rate)
- [High-Speed Go and Python Proxy Checker: Offline Cost and Latency CLI](../high-speed-golang-python-proxy-checker-cli)

### License

MIT License - Copyright (c) 2026 repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
