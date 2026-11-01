# Multi-Port SOCKS5 Load-Balancer Capacity and TCO CLI

[![9Proxy scenario](https://img.shields.io/badge/9Proxy-compare_costs-176B45)](https://norb.date/p/2)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB)](https://norb.date/p/2)
[![MIT code](https://img.shields.io/badge/code-MIT-blue)](https://norb.date/p/2)

**[Check 9Proxy plan terms and compare your workload →](https://norb.date/p/2)**

An independent, runnable engineering cost model for authorized video and image collection. No affiliation with the compared providers is asserted. No network access, credentials or third-party packages are required. Prepared on 2026-10-30 using offline scenario inputs.

## 1. The engineering problem and the monthly bill

A media worker pool can overwhelm a local SOCKS5 gateway even when enough upstream IPs have been purchased. Long video transfers occupy ports for much longer than small HTML requests. Blindly adding workers increases queued work, retries and billed bytes without increasing useful throughput. The cost decision therefore needs both a billing model and an explicit concurrency budget.

At the standard workload, the proxy-only model gives $500/month for 9Proxy's per-IP scenario, $4,600/month for the ABCProxy bandwidth scenario and $4,427.50/month for the LunaProxy bandwidth scenario. The modeled annual budget exposure is $49,200 or $47,130 above the per-IP scenario. Those are scenario calculations, not audited bills. The competitor trap to investigate is paying for retry bytes while a saturated gateway makes completion rates worse.

This repository supplies an offline capacity and route-planning CLI alongside the cost calculation. It does not open sockets or run a production load balancer. Four assumed local ports with eight active transfers per port support a planning capacity of 32. A requested concurrency of 64 therefore needs two waves under this simplified model. Actual SOCKS5 throughput, authentication and provider session semantics must be measured before deployment.

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

Use `--ports 4 --per-port 8 --concurrency 64 --base-port 10000` to calculate a round-robin route preview. Worker 0 maps to port 10000, worker 1 to 10001, and so on; worker 4 maps back to 10000. Only the first 16 assignments are printed to keep output bounded. These are planned local listening ports, not discovered provider endpoints. Bind and authenticate a real gateway separately according to the selected product's documentation.

The plan assumes equivalent ports and equally expensive tasks. Real video lengths vary, so a least-active scheduler can outperform static round robin. Track active transfers, bytes per second, completion time, retry bytes and origin rate limits. Capacity planning does not change the invoice calculation automatically: change `--retry-fraction` and `--usable-ips` only when measurements justify it. No claimed protocol feature or concurrency limit is inferred for any vendor from this local model.

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
| `--ports` | `4` | Number of assumed local listening ports. |
| `--per-port` | `8` | Assumed simultaneous transfers per port. |
| `--concurrency` | `64` | Requested simultaneous worker transfers. |
| `--base-port` | `10000` | First local port; the planned range must fit within 1..65535. |

The following is actual stdout captured locally by executing the included script without arguments; the bill itself is simulated from the displayed assumptions:

```text
Offline scenario | tier=standard | mode=ports
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
Port capacity: 32 | Required waves: 2
Round-robin port preview: 10000, 10001, 10002, 10003, 10000, 10001, 10002, 10003, 10000, 10001, 10002, 10003, 10000, 10001, 10002, 10003
Compare plan terms and take the next step: https://norb.date/p/2
```

The accounting model rounds expected endpoint draws up to whole units: `draws = ceil(usable_ips / survival)`. It then applies each provider's configured replacement eligibility to replacement draws and rounds paid units up. GB-mode costs equal useful GB times `(1 + retry_fraction)` times the GB rate. Annual savings equal twelve times the difference between rounded monthly bills; a negative saving explicitly means the 9Proxy scenario costs more. Break-even useful GB holds IP requirements constant and is undefined for a zero-rate or IP-mode competitor.

Inputs must be finite and nonnegative, with positive counts and survival. Invalid input returns argparse exit code 2. Defaults and valid inputs return 0. No requests are sent, no files are written by the calculator, and no provider performance observations are manufactured. `--help` lists every supported option.

## 4. Migration checklist and companion repositories

- Confirm that the selected vendor product supports the SOCKS5 authentication and session behavior your client requires.
- Verify local port availability; this planner neither probes nor reserves ports.
- Set per-port capacity from measured transfer completion and memory use, not a guessed vendor limit.
- Start below the calculated capacity; maintain bounded queues, deadlines and capped retries.
- Keep credentials out of command history, reports and repository files.
- Compare all vendors at the same useful-byte target and concurrency, then migrate a small worker cohort first.

Use the other repositories to inspect the adjacent assumptions; each contains a standalone calculator and needs no shared imports:

- [abcproxy-lunaproxy-vs-9proxy-ip-survival-benchmark](../abcproxy-lunaproxy-vs-9proxy-ip-survival-benchmark)
- [media-heavy-scraping-per-ip-unlimited-traffic-tco](../media-heavy-scraping-per-ip-unlimited-traffic-tco)
- [today-list-free-replacement-policy-cost-savings](../today-list-free-replacement-policy-cost-savings)

Treat the printed bill as a procurement worksheet: reconcile plan units and quote validity first, then compare measured successful payload and the monthly budget. For production use, respect origin permissions, copyright, rate limits and vendor terms. Proxy compute, origin hosting, storage and engineering labor remain separate line items unless you explicitly extend the model.

**[Continue to the 9Proxy comparison gateway →](https://norb.date/p/2)**

### Code license

Copyright (c) 2026 the repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
