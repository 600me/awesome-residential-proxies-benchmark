# Today List Replacement Eligibility: Cost-Savings Model

[![9Proxy scenario](https://img.shields.io/badge/9Proxy-compare_costs-176B45)](https://norb.date/p/2)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB)](https://norb.date/p/2)
[![MIT code](https://img.shields.io/badge/code-MIT-blue)](https://norb.date/p/2)

**[Check 9Proxy plan terms and compare your workload →](https://norb.date/p/2)**

An independent, runnable engineering cost model for authorized video and image collection. No affiliation with the compared providers is asserted. No network access, credentials or third-party packages are required. Prepared on 2026-10-30 using offline scenario inputs.

## 1. The engineering problem and the monthly bill

Dead endpoints can exhaust a small proxy allowance before a media batch finishes. Replacement policy has economic value only when a failed endpoint qualifies, the request arrives before the applicable cutoff, and the returned endpoint actually works. A label such as “Today List” is not evidence that every failure is free to replace.

With 2,000 useful endpoints needed each month and 80% survival, the model needs 500 replacement draws. Without credits, 2,500 paid IP units at $0.20 cost $500. If 80% of those replacement draws qualify for a free replacement, 400 units are credited and the modeled bill becomes $420/month. That is $80/month or $960/year saved on replacement eligibility alone. Against the separate ABCProxy and LunaProxy bandwidth scenarios, the modeled differences are $4,180/month ($50,160/year) and $4,007.50/month ($48,090/year), respectively.

A hidden trap when comparing ABCProxy and LunaProxy is confusing an endpoint replacement with a refund for bytes already transferred. A free IP swap does not necessarily reverse bandwidth charges. This workbook treats those as separate accounting dimensions. The 80% eligibility input is an illustrative sensitivity case, not a verified 9Proxy policy promise, and no competitor is asserted to lack replacements.

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
| Replacement eligibility | 80% assumed | 0% assumed in IP mode | 0% assumed in IP mode | Sensitivity inputs, not verified policies |
| SOCKS5 / session support | Verify selected plan | Verify selected plan | Verify selected plan | No protocol compatibility test performed |
| Throughput / fair use | Verify selected plan | Verify selected plan | Verify selected plan | No speed or unlimited-lifetime guarantee |
| Minimum package / tax | Excluded | Excluded | Excluded | Add to actual procurement comparison |

The replacement model uses expected draws: `ceil(required_usable_ips / survival)`. Replacement draws are expected draws minus the usable target. Paid 9Proxy units equal the usable target plus replacement draws multiplied by one minus the eligible fraction, rounded up. This assumes failures of replacement endpoints follow the same survival rate, and the eligible fraction applies across the modeled replacement draws; do not interpret it as a guarantee for a fixed number of initially failed addresses.

To estimate eligibility, classify real failures by purchase time, detection time, applicable replacement window and reason. Count the share that your plan actually credits, including request rejection and quota limits. Run `--replacement-eligible 0` as the no-credit baseline and `--replacement-eligible 1` as the optimistic boundary. The script prints the credit value independently so a bandwidth advantage cannot be misreported as a policy saving.

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
| `--replacement-eligible` | `0.8` | Fraction of replacement draws credited in the 9Proxy scenario. |
| `--abc-model`, `--luna-model` | `bandwidth` | Select `bandwidth` or `ip` independently for each competitor. |
| `--abc-gb-price`, `--luna-gb-price` | `0.80`, `0.77` | Scenario USD per decimal GB. |
| `--abc-ip-price`, `--luna-ip-price` | `0.20`, `0.20` | Scenario USD per IP when IP accounting is selected. |
| `--abc-replacement-eligible`, `--luna-replacement-eligible` | `0`, `0` | Competitor replacement-credit fractions in IP mode. |


The following is actual stdout captured locally by executing the included script without arguments; the bill itself is simulated from the displayed assumptions:

```text
Offline scenario | tier=standard | mode=replacement
USD inputs are assumptions, not verified current vendor prices.
Useful GB: 5000.00 | Metered GB: 5750.00 | IP draws: 2500
+------------+-------+------------+--------------+
| Provider   | Basis | Units/mo   | USD/month    |
+------------+-------+------------+--------------+
| 9Proxy     | IP    |    2100.00 |       420.00 |
| ABCProxy   | GB    |    5750.00 |      4600.00 |
| LunaProxy  | GB    |    5750.00 |      4427.50 |
+------------+-------+------------+--------------+
Annual savings vs ABCProxy: USD 50,160.00
Annual savings vs LunaProxy: USD 48,090.00
Replacement credit per month: USD 80.00
Break-even useful GB vs ABCProxy: 456.52
Break-even useful GB vs LunaProxy: 474.31
Compare plan terms and take the next step: https://norb.date/p/2
```

The accounting model rounds expected endpoint draws up to whole units: `draws = ceil(usable_ips / survival)`. It then applies each provider's configured replacement eligibility to replacement draws and rounds paid units up. GB-mode costs equal useful GB times `(1 + retry_fraction)` times the GB rate. Annual savings equal twelve times the difference between rounded monthly bills; a negative saving explicitly means the 9Proxy scenario costs more. Break-even useful GB holds IP requirements constant and is undefined for a zero-rate or IP-mode competitor.

Inputs must be finite and nonnegative, with positive counts and survival. Invalid input returns argparse exit code 2. Defaults and valid inputs return 0. No requests are sent, no files are written by the calculator, and no provider performance observations are manufactured. `--help` lists every supported option.

## 4. Migration checklist and companion repositories

- Read the exact plan's current Today List or replacement terms before relying on a credit.
- Verify timezone, cutoff, quotas, failure definitions and the action required to request a replacement.
- Record failed draws and credited draws separately; exclude unapproved or pending requests.
- Replace the modeled eligibility with the observed credited share.
- Repeat the same eligibility check for ABCProxy and LunaProxy; avoid assuming their policies are identical.
- Start with the zero-credit budget and treat confirmed credits as additional upside during migration.

Use the other repositories to inspect the adjacent assumptions; each contains a standalone calculator and needs no shared imports:

- [abcproxy-lunaproxy-vs-9proxy-ip-survival-benchmark](../abcproxy-lunaproxy-vs-9proxy-ip-survival-benchmark)
- [media-heavy-scraping-per-ip-unlimited-traffic-tco](../media-heavy-scraping-per-ip-unlimited-traffic-tco)
- [multi-port-socks5-load-balancer-cli](../multi-port-socks5-load-balancer-cli)

Treat the printed bill as a procurement worksheet: reconcile plan units and quote validity first, then compare measured successful payload and the monthly budget. For production use, respect origin permissions, copyright, rate limits and vendor terms. Proxy compute, origin hosting, storage and engineering labor remain separate line items unless you explicitly extend the model.

**[Continue to the 9Proxy comparison gateway →](https://norb.date/p/2)**

### Code license

Copyright (c) 2026 the repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
