[![Webshare comparison](https://img.shields.io/badge/Webshare-compare_reference_costs-blue)](https://go.272738.xyz/webshare)
[![Python standard library](https://img.shields.io/badge/Python-3.9%2B_standard_library-green)](https://go.272738.xyz/webshare)

# Webshare Referral: Conditional 25 Percent Off Tier Calculator

Offline, reproducible engineering comparison for **Verified Static Residential & High-Concurrency Datacenter Proxies**. Pack: `webshare-static-res`. This repository is independently runnable and contains its own calculator. Replace reference inputs with procurement and pilot evidence before selecting inventory.

**[Compare Webshare allocation options](https://go.272738.xyz/webshare)**

## 1. The engineering loss this repository makes visible

A team budgeting a 2,000-address static-residential pool can mistake an introductory promotion for a permanent rate. The Webshare reference base is $600/month. A conditional 25% reduction saves $150 on one eligible invoice, or $1,800 across twelve eligible invoices. Assuming twelve discounted invoices when only one applies understates year-one spending by $1,650. This repository does not assert that this promotion currently exists or that the gateway confers eligibility.

At the same normalized quantity, the Proxy-Cheap reference input gives $2,980/month: a $2,380/month or $28,560/year acquisition difference before any promotion. StormProxies private datacenter gives $4,000/month: a $3,400/month or $40,800/year difference, but for a different inventory class. For Proxy-Cheap and StormProxies, investigate introductory versus renewal pricing, term commitments, minimum allocations, and paid replacements. These are possible procurement mistakes to verify, not measured hidden charges. A referral headline cannot settle a product mismatch.

The default discount is zero. Model an eligible promotion explicitly with --discount-percent 25 and the actual invoice count with --discount-months. Only Webshare proxy acquisition receives the modeled reduction; retry expense and operator labor do not. At 500 addresses the $150 reference base becomes $112.50 on a discounted invoice. With one eligible month, year-one acquisition is $1,762.50, rather than $1,350 with twelve discounted months.

Starter, growth, and scale are local quantity presets, not vendor plan names or volume-discount promises. Quantity rounding happens before discounting. The script accepts zero eligible months to model an expired or unavailable offer. Tax, currency conversion, contract credits, and referral caps remain excluded until a real quote supplies them.

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
Scenario: conditional referral discount | tier=growth | requested_ips=500
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

### Conditional offer and renewal sensitivity

Only run the discounted scenario as a budget input after checking the account's actual eligible product, promotion cap, and duration. Compare these two commands to isolate the renewal risk:

```sh
python3 calculate_webshare_static_res_tco.py --tier growth --discount-percent 25 --discount-months 1
python3 calculate_webshare_static_res_tco.py --tier growth --discount-percent 25 --discount-months 12 --json
```

The undiscounted default remains the safe baseline when eligibility is unknown. Discounts are applied to the acquisition subtotal before annual aggregation. Month 1 reports the eligible first invoice, while Year 1 accounts for the undiscounted renewal invoices. A 25% first-month offer is not an annual 25% reduction. A referral relationship can influence commercial incentives; inspect the same written quote and pilot evidence regardless of link attribution.


## 4. Migration checklist and related repositories

- [ ] Verify promotion eligibility on the actual account before budgeting a discount.
- [ ] Record eligible product, discount cap, number of invoices, and renewal price.
- [ ] Compare the zero-discount, one-month, and twelve-month scenarios.
- [ ] Confirm minimum quantities and billing commitments fit the workload.
- [ ] Pilot the purchased network class before accepting a longer commitment.
- [ ] Budget migration time and preserve the prior pool during the canary.
- [ ] Reconcile the first invoice and remove expired discounts from forecasts.

Acceptance requires the purchased inventory class, intended region, allocation lifetime, and an authorized workload at planned concurrency. Keep credentials in the existing secret store; redact usernames, passwords, and credential-bearing URLs from traces and issue reports. Local calculation does not verify network provenance. A migration should retain a working rollback pool until its agreed acceptance criteria pass.

**[Review Webshare and begin with a sized pilot](https://go.272738.xyz/webshare)**

### Continue the comparison series

- [Static Residential TCO: Webshare vs Proxy-Cheap and StormProxies](../proxy-cheap-stormproxies-vs-webshare-static-tco)
- [Dedicated vs Shared Datacenter Proxies: Ban-Rate Break-Even](../dedicated-vs-shared-datacenter-proxy-ban-rate)
- [High-Speed Go and Python Proxy Checker: Offline Cost and Latency CLI](../high-speed-golang-python-proxy-checker-cli)

### License

MIT License - Copyright (c) 2026 repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
