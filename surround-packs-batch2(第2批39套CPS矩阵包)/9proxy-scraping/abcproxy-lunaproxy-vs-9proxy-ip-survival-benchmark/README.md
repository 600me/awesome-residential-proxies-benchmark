# IP Survival Benchmark: 9Proxy vs ABCProxy and LunaProxy

[![9Proxy scenario](https://img.shields.io/badge/9Proxy-compare_costs-176B45)](https://norb.date/p/2)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB)](https://norb.date/p/2)
[![MIT code](https://img.shields.io/badge/code-MIT-blue)](https://norb.date/p/2)

**[Check 9Proxy plan terms and compare your workload →](https://norb.date/p/2)**

An independent, runnable engineering cost model for authorized video and image collection. No affiliation with the compared providers is asserted. No network access, credentials or third-party packages are required. Prepared on 2026-10-30 using offline scenario inputs.

## 1. The engineering problem and the monthly bill

A media crawler that loses residential endpoints during a long video download pays twice: once for an IP that no longer works and again for bytes that must be fetched again. A successful HTTP handshake is not a survival measurement. Count an endpoint as usable only after it finishes the same authorized image or video transfer, within the same deadline, from the same region. Otherwise a low acquisition price can hide an expensive stream of replacements.

In this repository's standard **modeled** workload, 5,000 GB of useful payload becomes 5,750 GB of billable traffic after retries. With 2,000 required usable IPs and 80% endpoint survival, the model purchases 2,500 IP units. At the explicit input of $0.20 per IP, the 9Proxy scenario costs $500/month. The ABCProxy bandwidth scenario costs $4,600 and the LunaProxy bandwidth scenario costs $4,427.50. The modeled excess is $4,100/month ($49,200/year) or $3,927.50/month ($47,130/year), respectively. These are reproducible budget differences, not measured vendor losses.

The billing trap to investigate in ABCProxy and LunaProxy plans is whether failed and retried transfers consume paid bandwidth, and whether the chosen product charges for IP acquisition as well. The script can switch either competitor to per-IP accounting; it does not assume every product from either company is sold by the GB.

**Evidence boundary:** current vendor prices, product limits and replacement policies were not fetched or verified. All dollar rates below are explicit illustrative planning assumptions, not real-time quotes, historical price evidence or measured invoices. This repository cannot substantiate a claim about the cheapest current provider. Replace the rates with your actual selected product's dated quote, including minimum purchase, geography, tax and discounts, before making a purchase decision. Price examples are not a claim that all three providers offer interchangeable products.

## 2. Price inputs and technical comparison

The comparison has five columns and separates a numerical assumption from a product capability that still needs verification. The bandwidth scenarios for ABCProxy and LunaProxy are selectable accounting modes, not assertions that those providers only sell bandwidth plans.

| Parameter | 9Proxy scenario | ABCProxy scenario | LunaProxy scenario | Interpretation / evidence |
| --- | --- | --- | --- | --- |
| Default billing basis | Per acquired IP | Per decimal GB | Per decimal GB | Selected scenario, not universal vendor billing |
| Input price in USD | $0.20/IP | $0.80/GB | $0.77/GB | Unverified planning rates; replace with dated quotes |
| Alternative per-IP input | $0.20/IP | $0.20/IP | $0.20/IP | Equal-rate sensitivity, not a vendor tariff |
| Useful payload per month | 5,000 GB | 5,000 GB | 5,000 GB | Same standard workload in every scenario |
| Extra bytes from retries | 15% | 15% | 15% | Byte overhead, not request-failure probability |
| Metered payload per month | No byte fee in model | 5,750 GB | 5,750 GB | Useful GB multiplied by 1.15 |
| Required usable endpoints | 2,000 | 2,000 workload target | 2,000 workload target | GB model does not separately charge these IPs |
| Endpoint survival input | 80% | 80% if per-IP mode | 80% if per-IP mode | Synthetic input; no vendor test performed |
| Replacement eligibility | 0% assumed | 0% assumed in IP mode | 0% assumed in IP mode | Sensitivity inputs, not verified policies |
| SOCKS5 / session support | Verify selected plan | Verify selected plan | Verify selected plan | No protocol compatibility test performed |
| Throughput / fair use | Verify selected plan | Verify selected plan | Verify selected plan | No speed or unlimited-lifetime guarantee |
| Minimum package / tax | Excluded | Excluded | Excluded | Add to actual procurement comparison |

For a real survival experiment, use a permitted static media fixture with known size and checksum. Run equal-size regional cohorts during the same time window. Record assigned endpoint ID, timestamp, bytes received, completion deadline, status code and checksum result locally. Compute survival as completed usable endpoints divided by purchased endpoints. A 403 or 429 from the origin is not automatically a dead proxy; tag failures before attributing them to the provider. Repeat across multiple windows and report sample counts. No live cohort was collected for this repository; its default survival value is an input, not a finding.

**[Review the 9Proxy offer, then enter your quoted rates →](https://norb.date/p/2)**

## 3. Reproducible Python CLI and actual local output

Run from this repository directory with Python 3.8 or newer:

```bash
python3 calculate_9proxy_scraping_tco.py
python3 calculate_9proxy_scraping_tco.py --tier small
python3 calculate_9proxy_scraping_tco.py --tier scale --json
python3 calculate_9proxy_scraping_tco.py --gb 5000 --usable-ips 2000 --survival 0.8 --retry-fraction 0.15
python3 calculate_9proxy_scraping_tco.py --abc-model ip --abc-ip-price 0.20 --luna-model ip --luna-ip-price 0.20
```

| Argument | Default | Meaning |
| --- | --- | --- |
| `--tier` | `standard` | `small`: 1,000 GB / 500 usable IPs; `standard`: 5,000 / 2,000; `scale`: 20,000 / 8,000. All values are monthly. |
| `--json` | Off | Emit one JSON object with assumptions, bills, annual savings and the action URL. |
| `--gb` | From tier | Override useful monthly decimal GB; zero is allowed. |
| `--usable-ips` | From tier | Override usable monthly endpoint target; positive integer. |
| `--survival` | `0.8` | Usable fraction per acquired endpoint; must be greater than zero and at most one. |
| `--retry-fraction` | `0.15` | Additional metered bytes as a fraction of useful payload. |
| `--nine-ip-price` | `0.20` | Scenario price per acquired 9Proxy IP, USD. |
| `--replacement-eligible` | `0.0` | Fraction of replacement draws credited in the 9Proxy scenario. |
| `--abc-model`, `--luna-model` | `bandwidth` | Select `bandwidth` or `ip` independently for each competitor. |
| `--abc-gb-price`, `--luna-gb-price` | `0.80`, `0.77` | Scenario USD per decimal GB. |
| `--abc-ip-price`, `--luna-ip-price` | `0.20`, `0.20` | Scenario USD per IP when IP accounting is selected. |
| `--abc-replacement-eligible`, `--luna-replacement-eligible` | `0`, `0` | Competitor replacement-credit fractions in IP mode. |


The following is actual stdout captured locally by executing the included script without arguments; the bill itself is simulated from the displayed assumptions:

```text
Offline scenario | tier=standard | mode=survival
USD inputs are assumptions, not verified current vendor prices.
Useful GB: 5000.00 | Metered GB: 5750.00 | IP draws: 2500
+------------+-------+------------+--------------+
| Provider   | Basis | Units/mo   | USD/month    |
+------------+-------+------------+--------------+
| 9Proxy     | IP    |    2500.00 |       500.00 |
| ABCProxy   | GB    |    5750.00 |      4600.00 |
| LunaProxy  | GB    |    5750.00 |      4427.50 |
+------------+-------+------------+--------------+
Annual savings vs ABCProxy: USD 49,200.00
Annual savings vs LunaProxy: USD 47,130.00
Replacement credit per month: USD 0.00
Break-even useful GB vs ABCProxy: 543.48
Break-even useful GB vs LunaProxy: 564.65
Compare plan terms and take the next step: https://norb.date/p/2
```

The accounting model rounds expected endpoint draws up to whole units: `draws = ceil(usable_ips / survival)`. It then applies each provider's configured replacement eligibility to replacement draws and rounds paid units up. GB-mode costs equal useful GB times `(1 + retry_fraction)` times the GB rate. Annual savings equal twelve times the difference between rounded monthly bills; a negative saving explicitly means the 9Proxy scenario costs more. Break-even useful GB holds IP requirements constant and is undefined for a zero-rate or IP-mode competitor.

Inputs must be finite and nonnegative, with positive counts and survival. Invalid input returns argparse exit code 2. Defaults and valid inputs return 0. No requests are sent, no files are written by the calculator, and no provider performance observations are manufactured. `--help` lists every supported option.

## 4. Migration checklist and companion repositories

- Define a successful complete transfer, a deadline and a fixed sample size before testing.
- Hold target, region, concurrency and retry budget constant across vendors.
- Replace `--survival 0.8` with the observed usable-endpoint fraction; retain failure reasons.
- Confirm whether a replacement consumes a new paid IP unit on the actual plan.
- Compare p50/p95 completion time and checksum success separately from the cost table.
- Pilot on a permitted dataset, keep the existing route available, and expand after the measured crossover supports migration.

Use the other repositories to inspect the adjacent assumptions; each contains a standalone calculator and needs no shared imports:

- [media-heavy-scraping-per-ip-unlimited-traffic-tco](../media-heavy-scraping-per-ip-unlimited-traffic-tco)
- [today-list-free-replacement-policy-cost-savings](../today-list-free-replacement-policy-cost-savings)
- [multi-port-socks5-load-balancer-cli](../multi-port-socks5-load-balancer-cli)

Treat the printed bill as a procurement worksheet: reconcile plan units and quote validity first, then compare measured successful payload and the monthly budget. For production use, respect origin permissions, copyright, rate limits and vendor terms. Proxy compute, origin hosting, storage and engineering labor remain separate line items unless you explicitly extend the model.

**[Continue to the 9Proxy comparison gateway →](https://norb.date/p/2)**

### Code license

Copyright (c) 2026 the repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
