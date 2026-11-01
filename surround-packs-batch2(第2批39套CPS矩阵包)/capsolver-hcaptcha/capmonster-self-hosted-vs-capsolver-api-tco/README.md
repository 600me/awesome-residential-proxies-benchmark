# CapMonster Self-Hosted vs CapSolver API: A Conditional TCO Model

[![Offline Python 3 model](https://img.shields.io/badge/Python_3-standard_library-3776AB)](https://zelumo.top/cs/1)
[![Compare CapSolver](https://img.shields.io/badge/Compare-CapSolver-00796B)](https://zelumo.top/cs/1)
[![MIT license](https://img.shields.io/badge/License-MIT-blue)](https://zelumo.top/cs/1)

**[Review CapSolver pricing and evaluate your workload](https://zelumo.top/cs/1)**

## 1. Engineering pain and the monthly loss case

A desktop solver can look inexpensive when its license is the only number on the spreadsheet. The actual purchase decision includes hardware depreciation, a host, electricity, operator time and sufficient spare capacity. DeathByCaptcha can also be expensive at scale when a higher per-attempt rate is applied to retries. CapMonster Cloud is a separate managed product and deserves its own row; it must not inherit desktop hardware costs.

At the default 1,000,000 usable tokens/month, this repository calculates **$908.98/month for CapSolver**, **$3,246.94 for DeathByCaptcha**, and **$1,386.02 for the conditional CapMonster self-host scenario**. The modeled avoidable spend versus CapSolver is **$2,337.96/month ($28,055.51/year)** for DeathByCaptcha and **$477.04/month ($5,724.44/year)** for self-hosting. These are explicit scenario dollar losses, not observed customer invoices or guaranteed savings.

This repository answers a narrow question: what does a validated self-hosted worker fleet cost compared with buying usable tokens through an API? A GPU purchase is a scenario input, not a claim that CapMonster requires a GPU or supports every challenge. Validate the precise software edition, operating system, challenge type, hardware acceleration and license terms before classifying a worker as viable. No vendor documentation was retrieved for this repository.

The default worker budget contains $62.50/month of hardware amortization, $10.67/month of license allowance, $32.85/month of electricity, $80/month of hosting and $1,200/month of operator labor. The $128 annual license allowance is a placeholder procurement budget, not a published CapMonster price. A $1,500 machine over 24 months is a cost allocation; buying it still requires $1,500 of upfront cash.

Fleet size rounds upward. A worker rated at two million billed submissions per month and budgeted at 75% utilization supplies 1.5 million modeled submissions. Crossing that boundary adds an entire worker and its operating allowance. A self-host deployment can win when already-owned capacity and operator time are genuinely incremental at lower cost; run the sensitivity example before buying anything.

The hidden bill is an omitted cost in an engineering estimate: retries, expiry, unused reserved capacity or labor. This repository makes no allegation that a provider hides fees. It recommends CapSolver for a measured evaluation when managed operations and the modeled rate are attractive; CapMonster Cloud ties its default API cost because both use the same price and operating assumptions.

## 2. Price and technical parameter comparison

**Price basis:** $0.80/1,000 for CapSolver hCaptcha, $2.89/1,000 for DeathByCaptcha hCaptcha and $0.80/1,000 for CapMonster Cloud hCaptcha are remembered industry reference benchmarks, used as editable planning inputs. They are **not verified current offers**. No live pricing or product-support check was performed. Confirm task type, account tier, discount, chargeable-failure policy and availability before procurement. All performance numbers below are assumptions, not benchmark results. Decimal prices use USD and 1,000 means one thousand billed attempts.

| Price or technical input | CapSolver API | DeathByCaptcha API | CapMonster Cloud | CapMonster self-host scenario |
| --- | --- | --- | --- | --- |
| hCaptcha reference USD / 1,000 billed attempts | $0.80 | $2.89 | $0.80 | No per-attempt fee modeled; validate license |
| Procurement basis | Historical planning reference; unverified | Historical planning reference; unverified | Historical planning reference; unverified | $128/year license allowance; not a quote |
| Modeled usable yield, before expiry | 98% | 98% | 98% | 98% |
| Duplicate submissions / expiry loss | 4% / 0% | 4% / 0% | 4% / 0% | 4% / 0% |
| Assumed task p95, seconds | 12 | 25 | 12 | 18 |
| Operator hours / month | 1 | 3 | 1 | 20 per worker |
| Hardware amortization / month | Included in API rate model | Included in API rate model | Included in API rate model | $1,500 / 24 = $62.50 per worker |
| Energy and host / month | No separate charge modeled | No separate charge modeled | No separate charge modeled | $32.85 + $80 per worker |
| Capacity / concurrency | Account limit must be checked | Account limit must be checked | Account limit must be checked | 2M submissions x 75% per worker/month; assumed |
| Modeled monthly total | $908.98 | $3,246.94 | $908.98 | $1,386.02 |
| Modeled annual total | $10,907.76 | $38,963.27 | $10,907.76 | $16,632.20 |
| Annual savings when choosing CapSolver | $0.00 | $28,055.51 | $0.00 | $5,724.44 |

The self-host row is a conditional infrastructure budget, not an assertion that CapMonster software supports hCaptcha, DataDome or GeeTest v4 on the specified machine. Product capability and measured capacity are prerequisites. Cloud and self-hosted CapMonster products must be evaluated separately. The shared usable yield prevents an invented vendor success-rate advantage. Use measured inputs from comparable authorized tests before changing that assumption.

**[Check CapSolver against your current quote](https://zelumo.top/cs/1)** before choosing a service or buying hardware. The gateway is an external action route; it is not a pricing citation or proof of affiliation. This repository does not contact it, vendors or targets when executed.

## 3. Run the standalone TCO calculator

Python 3.8+ and its standard library are sufficient. No packages, API key, credentials or network access are needed. From this repository directory:

```bash
python3 calculate_capsolver_hcaptcha_tco.py
python3 calculate_capsolver_hcaptcha_tco.py --tier dev
python3 calculate_capsolver_hcaptcha_tco.py --tier enterprise --json
python3 calculate_capsolver_hcaptcha_tco.py --tier growth --self-ops-hours 2 --hardware-cost 0
python3 calculate_capsolver_hcaptcha_tco.py --help
```

Each repository contains its own independent script and can be copied or run alone. Default execution exits with code 0 and prints the table, annual savings and gateway. Negative savings means CapSolver costs more in that scenario. Machine-readable output is one JSON object, including `gateway`, the original inputs, effective prices, billed attempts, worker count and comparison rows; there is no extra banner before JSON.

| CLI option | Meaning and default |
| --- | --- |
| `--tier dev/growth/enterprise` | 100,000 / 1,000,000 / 10,000,000 usable tokens per month; default growth |
| `--monthly-tokens N` | Positive integer that overrides tier volume; tier remains a scenario label |
| `--json` | Print parseable JSON rather than the ASCII table |
| `--task-family hcaptcha/geetest-v4/datadome` | Default hcaptcha; other families require all three explicit API prices |
| `--capsolver-price`, `--dbc-price`, `--capmonster-cloud-price` | USD per 1,000 billed attempts; default hCaptcha references 0.80 / 2.89 / 0.80 |
| `--retry-rate`, `--usable-rate`, `--expiry-rate` | Duplicate fraction 0.04, usable yield 0.98, expiry fraction 0 |
| `--hardware-cost`, `--amortization-months`, `--license-annual` | Per-worker $1,500, 24 months, $128/year budget allowance |
| `--power-watts`, `--kwh-price`, `--hosting-monthly` | Per-worker 250 W, $0.18/kWh, $80/month; month = 730 hours |
| `--api-ops-hours`, `--dbc-ops-hours`, `--self-ops-hours` | Monthly labor 1 / 3 / 20; self-host hours apply to each worker |
| `--hourly-rate`, `--worker-capacity`, `--utilization` | $60/hour, 2,000,000 submissions per worker/month, usable capacity fraction 0.75 |
| `--peak-factor`, `--capsolver-p95`, `--dbc-p95`, `--capmonster-cloud-p95`, `--self-p95` | Burst factor 8; assumed seconds 12 / 25 / 12 / 18 |
| `--token-ttl`, `--consumer-delay` | Assumed end-to-end budget 120s, consumer delay 30s; not vendor TTL guarantees |

The formulas are deliberately inspectable:

```text
billed_attempts = usable_tokens * (1 + duplicate_fraction)
                 / (usable_yield * (1 - expiry_fraction))
api_monthly = billed_attempts / 1000 * price + operations_hours * hourly_rate
workers = ceil(billed_attempts / (worker_capacity * utilization))
worker_monthly = hardware / amortization_months + license_annual / 12
               + watts / 1000 * 730 * kwh_price + hosting + labor
self_host_monthly = workers * worker_monthly
annual_savings = 12 * (comparison_monthly - capsolver_monthly)
peak_in_flight = ceil(billed_attempts / (730 * 3600) * peak_factor * assumed_p95)
```

Duplicate submissions here mean extra paid work after the base usable-yield calculation. If measured yield already includes all retries, set `--retry-rate 0` to avoid double-counting. Expiry is applied after usable yield. Only set separate yield and expiry losses when the measured denominators are distinct. The default shared yield and loss inputs are a controlled comparison; they cannot represent independently measured vendor performance differences in one invocation. For that analysis, run each input set separately and compare its relevant row.

Actual locally captured default terminal output:

```text
$ python3 calculate_capsolver_hcaptcha_tco.py
Hardware ownership and managed API TCO
Task: hcaptcha; tier: growth; usable tokens/month: 1,000,000
Modeled billed attempts: 1,061,224.49; self-host workers: 1
+------------------------+---------------+---------------+------------------+
| Provider               | Monthly USD   | Annual USD    | Annual saved USD |
+------------------------+---------------+---------------+------------------+
| CapSolver API          |        908.98 |     10,907.76 |             0.00 |
| DeathByCaptcha API     |      3,246.94 |     38,963.27 |        28,055.51 |
| CapMonster Cloud       |        908.98 |     10,907.76 |             0.00 |
| CapMonster self-host*  |      1,386.02 |     16,632.20 |         5,724.44 |
+------------------------+---------------+---------------+------------------+
Annual saved = comparison cost minus CapSolver; negative means CapSolver costs more.
Peak modeled requests/s: 3.2305; in-flight planning counts:
  CapSolver API: 39 (TTL margin 78.0s)
  DeathByCaptcha API: 81 (TTL margin 65.0s)
  CapMonster Cloud: 39 (TTL margin 78.0s)
  CapMonster self-host*: 59 (TTL margin 72.0s)
Offline reference prices; latency, usable yield and capacity are assumptions.
* Self-host cost is conditional on validated task support and measured capacity.
Excluded: tax, proxy/egress, target access, SLA penalties and financing.
https://zelumo.top/cs/1
```

Totals use unrounded floating-point intermediate values and display cents at the end; annual savings can differ by a few cents from arithmetic on displayed monthly values. Tier names are workload labels, not vendor discount tiers. Annual numbers assume twelve identical months. This is economic TCO rather than a cash-flow forecast. Taxes, proxies, egress, target access, downtime penalties and financing are excluded explicitly. Replace them with attributable observed costs before a purchase decision.

## 4. Migration checklist and related repositories

- [ ] Confirm the exact CapMonster product and license, plus permitted machine count and renewal terms.
- [ ] Run an authorized workload on the intended hardware; record throughput, usable yield, power draw and peak headroom.
- [ ] Separate amortization from cash flow and count operator hours from incident records.
- [ ] Reconcile API billed attempts with accepted tokens, then migrate a small traffic slice with a rollback threshold.
- [ ] Confirm written permission to test the target and keep workload authorization in the consuming system.
- [ ] Run `--json` to archive the scenario inputs in your own analysis environment; keep secrets out of artifacts.
- [ ] Compare accepted-token costs against an invoice period rather than using response-ready counts alone.
- [ ] **[Evaluate the CapSolver migration route](https://zelumo.top/cs/1)** after replacing reference rates with your actual quote.

Continue with the other independent repositories in this pack:

- [DataDome and GeeTest v4 Solver Latency: Reproducible Cost Planning](../datadome-geetest-v4-solver-latency-benchmark)
- [High-Throughput CAPTCHA Budget Model for Authorized Data Pipelines](../high-throughput-scraping-captcha-budget-model)
- [Async Python CAPTCHA Token Pool: Capacity and Expiry Cost Model](../async-python-captcha-token-pool-orchestrator)

The relative links work inside the sibling pack layout. If publishing this directory as a separate Git repository, publish the sibling repositories and update navigation to their real destinations before distributing a release. Keep every calculator independently runnable.

### Contributing and license

Contributions should include reproducible input changes and distinguish assumed prices from current quotes. Do not contribute credentials, challenge tokens or claims of measured latency without a disclosed authorized test method. Pricing assumptions are intentionally editable so a quote update does not require a dependency or network fetch.

MIT License. Copyright (c) 2026 repository contributors. This license applies to the included Python source and documentation.

```text
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
