[![Webshare comparison](https://img.shields.io/badge/Webshare-compare_reference_costs-blue)](https://go.272738.xyz/webshare)
[![Python standard library](https://img.shields.io/badge/Python-3.9%2B_standard_library-green)](https://go.272738.xyz/webshare)

# Dedicated vs Shared Datacenter Proxies: Ban-Rate Break-Even

Offline, reproducible engineering comparison for **Verified Static Residential & High-Concurrency Datacenter Proxies**. Pack: `webshare-static-res`. This repository is independently runnable and contains its own calculator. Replace reference inputs with procurement and pilot evidence before selecting inventory.

**[Compare Webshare allocation options](https://go.272738.xyz/webshare)**

## 1. The engineering loss this repository makes visible

A shared pool can have a low per-address price while dedicated inventory buys isolation that a particular destination may reward. Neither label determines a ban rate. For 500 addresses, the Webshare shared-datacenter reference base is $14.95/month, the Proxy-Cheap datacenter input is $150/month, and the StormProxies private-datacenter reference is $1,000/month. The last package carries a $985.05/month or $11,820.60/year acquisition premium over the Webshare shared reference. That premium needs measured operational value.

The budget trap when comparing Proxy-Cheap and StormProxies is mixing shared and private inventory, or calling every failure an IP ban. At one million desired successful jobs and $0.002 per extra attempt, a 20% failure assumption generates $500/month in retries. At 2%, that falls to about $40.82/month. The difference is $459.18/month, or approximately $5,510.20/year using unrounded values. This is a sensitivity calculation, not a vendor benchmark. Authentication errors, destination rate limits, application bugs, and timeouts require separate diagnosis.

Use a matched canary with the same destinations, countries, request mix, time windows, connection reuse, and concurrency. Randomize assignments, count attempts and successes, and preserve HTTP error categories. Confirm allocation exclusivity from the purchased contract. No provider-specific ban rate is supplied here.

The model estimates extra attempts as delivered_jobs * p / (1 - p), where p is a stationary attempt-failure probability. Correlated outages, limited retry budgets, and backoff can materially change the result. With the reference acquisition premium of $985.05/month, one million delivered jobs, $0.002 per retry, and a 2% dedicated failure input, break-even occurs at about 33.90% shared failures. This is algebra on hypothetical inputs, not evidence that any named provider exhibits those rates.

## 2. Price and technical comparison

**Offline price provenance.** No vendor pages were fetched for this pack. These are remembered historical entry-price reference points, not independently verified current quotes: Webshare shared datacenter at $2.99 per 100 addresses/month and static residential at $6 per 20 addresses/month; Proxy-Cheap reference inputs of $0.30 per datacenter address/month and $1.49 per static-residential address/month; StormProxies private datacenter at $10 per five addresses/month. The Proxy-Cheap inputs particularly need confirmation against an actual quote. Dates, regions, stock, tax, bandwidth entitlement, and contract eligibility have not been verified. Linear scaling assumes no volume discount. Replace the inputs with written quotes before purchasing. No supplier invoice or live measurement is claimed.

"Verified" names an acceptance requirement, not a certification of any provider. Static residential/ISP hosting, shared datacenter, private datacenter, and rotating residential are separate inventory classes. No like-for-like StormProxies static-residential price has been established here. Unknown technical parameters are marked for verification rather than invented. This independent comparison may use a referral gateway; it does not verify the gateway's commercial terms.

| Metric | Webshare | Proxy-Cheap | StormProxies | Interpretation and verification |
|---|---|---|---|---|
| Historical static residential reference | $6 / 20 IPs / month | $1.49 / IP / month reference | No equivalent price established | Verify ISP hosting and current quote |
| Historical datacenter reference | $2.99 / 100 IPs / month, shared | $0.30 / IP / month reference | $10 / 5 IPs / month, private | Shared and private differ |
| Modeled product in this CLI | Shared datacenter | Datacenter reference | Private datacenter | StormProxies is not a residential substitute |
| Default 500-IP acquisition / month | $14.95 | $150.00 | $1,000.00 | Linear reference model, not a volume quote |
| Allocation block assumed | 100 IPs | 1 IP | 5 IPs | Verify actual minimum and stock |
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
| `--webshare-price USD` | `0.0299` | Monthly price per billed Webshare address |
| `--proxy-cheap-price USD` | `0.30` | Monthly price per billed Proxy-Cheap address |
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
Scenario: datacenter failure-cost sensitivity | tier=growth | requested_ips=500
OFFLINE MODEL: unverified reference prices; mixed network classes; no measured ban rates.
+---------------+----------+----------+----------+----------+------------+-------------+
| Provider      | Base/mo  | Retry/mo | Labor/mo | Month 1  | Year 1     | Billed IPs  |
+---------------+----------+----------+----------+----------+------------+-------------+
| Webshare      |    14.95 |    40.82 |   120.00 |   175.77 |    2109.20 |         500 |
| Proxy-Cheap   |   150.00 |    40.82 |   120.00 |   310.82 |    3729.80 |         500 |
| StormProxies  |  1000.00 |    40.82 |   120.00 |  1160.82 |   13929.80 |         500 |
+---------------+----------+----------+----------+----------+------------+-------------+
USD; Month 1 applies the discount only if eligible months > 0.
Year-one savings choosing Webshare vs Proxy-Cheap: $1620.60
Year-one savings choosing Webshare vs StormProxies: $11820.60
Compare the actual allocation and renewal quote: https://go.272738.xyz/webshare
```

### Explore a failure-cost crossover

```sh
python3 calculate_webshare_static_res_tco.py --jobs 1000000 --webshare-failure 0.20 --proxy-cheap-failure 0.10 --storm-failure 0.02 --retry-cost 0.002 --json
```

The deliberately different failure probabilities are sensitivity inputs, not observations about the brands. Solve `premium = jobs * retry_cost * (p_shared / (1 - p_shared) - p_dedicated / (1 - p_dedicated))` to estimate a crossover. Choose a dedicated pool only when a matched pilot justifies the premium for your workload. Report sample size and uncertainty; a few blocked requests do not establish a population ban rate. Retry transient failures only within authorized service limits.


## 4. Migration checklist and related repositories

- [ ] Obtain written shared-versus-exclusive allocation terms for every quote.
- [ ] Define application success independently of HTTP 200.
- [ ] Separate 407, 403, 429, 5xx, timeout, and content-validation failures.
- [ ] Use authorized destinations with per-host limits and bounded retries.
- [ ] Compare matched samples and report sample size and confidence intervals.
- [ ] Move traffic only when successful-job cost and latency meet the SLO.
- [ ] Preserve rollback credentials and verify the next actual invoice.

Acceptance requires the purchased inventory class, intended region, allocation lifetime, and an authorized workload at planned concurrency. Keep credentials in the existing secret store; redact usernames, passwords, and credential-bearing URLs from traces and issue reports. Local calculation does not verify network provenance. A migration should retain a working rollback pool until its agreed acceptance criteria pass.

**[Review Webshare and begin with a sized pilot](https://go.272738.xyz/webshare)**

### Continue the comparison series

- [Static Residential TCO: Webshare vs Proxy-Cheap and StormProxies](../proxy-cheap-stormproxies-vs-webshare-static-tco)
- [Webshare Referral: Conditional 25 Percent Off Tier Calculator](../webshare-referral-25-percent-off-tier-calculator)
- [High-Speed Go and Python Proxy Checker: Offline Cost and Latency CLI](../high-speed-golang-python-proxy-checker-cli)

### License

MIT License - Copyright (c) 2026 repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
