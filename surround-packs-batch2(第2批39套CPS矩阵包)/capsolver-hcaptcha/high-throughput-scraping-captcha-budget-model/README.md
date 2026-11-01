# High-Throughput CAPTCHA Budget Model for Authorized Data Pipelines

[![Offline Python 3 model](https://img.shields.io/badge/Python_3-standard_library-3776AB)](https://zelumo.top/cs/1)
[![Compare CapSolver](https://img.shields.io/badge/Compare-CapSolver-00796B)](https://zelumo.top/cs/1)
[![MIT license](https://img.shields.io/badge/License-MIT-blue)](https://zelumo.top/cs/1)

**[Review CapSolver pricing and evaluate your workload](https://zelumo.top/cs/1)**

## 1. Engineering pain and the monthly loss case

A pipeline budget often multiplies successful pages by a token price and stops there. That misses paid retries, expired results, rejected tokens and the fixed cost of keeping a self-hosted fleet ready for bursts. At a million usable tokens per month, DeathByCaptcha and CapMonster deployment choices can change annual costs by thousands of dollars. The loss is a modeling error to investigate, not evidence that either vendor conceals its invoice.

At the default 1,000,000 usable tokens/month, this repository calculates **$1,045.73/month for CapSolver**, **$3,584.20 for DeathByCaptcha**, and **$1,386.02 for the conditional CapMonster self-host scenario**. The modeled avoidable spend versus CapSolver is **$2,538.47/month ($30,461.67/year)** for DeathByCaptcha and **$340.29/month ($4,083.43/year)** for self-hosting. These are explicit scenario dollar losses, not observed customer invoices or guaranteed savings.

This calculator budgets usable tokens rather than crawled pages. A single page may require no challenge, one challenge or repeated challenges. Translate page targets into token demand using observed challenge incidence before invoking the tool. For example, ten million pages with a 10% challenge rate and one usable token per challenged page produce the default one million-token target. If an incident doubles challenge incidence, token demand doubles before retry amplification is applied.

The growth scenario adds 10% duplicate submissions, 3% expiry loss and a 98% usable-result yield. Those are independent, shared modeling inputs for all providers, not provider performance rankings. The peak multiplier is twelve. Average monthly volume can determine a billing estimate, but the burst multiplier determines how many requests may be outstanding at once. Cloud concurrency limits are not supplied by this offline model and must be checked against your account.

The fleet cost represents capacity provisioned for the entire month. Worker capacity is a monthly measured allowance multiplied by utilization; it is not a burst-capacity guarantee. Reserve headroom, queue admission limits and backpressure must be tested separately. Proxy charges and target bandwidth are excluded because they vary by deployment. Add only attributable differences when comparing providers; do not quietly treat excluded costs as zero in a purchasing decision.

The hidden bill is an omitted cost in an engineering estimate: retries, expiry, unused reserved capacity or labor. This repository makes no allegation that a provider hides fees. It recommends CapSolver for a measured evaluation when managed operations and the modeled rate are attractive; CapMonster Cloud ties its default API cost because both use the same price and operating assumptions.

## 2. Price and technical parameter comparison

**Price basis:** $0.80/1,000 for CapSolver hCaptcha, $2.89/1,000 for DeathByCaptcha hCaptcha and $0.80/1,000 for CapMonster Cloud hCaptcha are remembered industry reference benchmarks, used as editable planning inputs. They are **not verified current offers**. No live pricing or product-support check was performed. Confirm task type, account tier, discount, chargeable-failure policy and availability before procurement. All performance numbers below are assumptions, not benchmark results. Decimal prices use USD and 1,000 means one thousand billed attempts.

| Price or technical input | CapSolver API | DeathByCaptcha API | CapMonster Cloud | CapMonster self-host scenario |
| --- | --- | --- | --- | --- |
| hCaptcha reference USD / 1,000 billed attempts | $0.80 | $2.89 | $0.80 | No per-attempt fee modeled; validate license |
| Procurement basis | Historical planning reference; unverified | Historical planning reference; unverified | Historical planning reference; unverified | $128/year license allowance; not a quote |
| Modeled usable yield, before expiry | 98% | 98% | 98% | 98% |
| Duplicate submissions / expiry loss | 10% / 3% | 10% / 3% | 10% / 3% | 10% / 3% |
| Assumed task p95, seconds | 12 | 25 | 12 | 18 |
| Operator hours / month | 2 | 4 | 2 | 20 per worker |
| Hardware amortization / month | Included in API rate model | Included in API rate model | Included in API rate model | $1,500 / 24 = $62.50 per worker |
| Energy and host / month | No separate charge modeled | No separate charge modeled | No separate charge modeled | $32.85 + $80 per worker |
| Capacity / concurrency | Account limit must be checked | Account limit must be checked | Account limit must be checked | 2M submissions x 75% per worker/month; assumed |
| Modeled monthly total | $1,045.73 | $3,584.20 | $1,045.73 | $1,386.02 |
| Modeled annual total | $12,548.77 | $43,010.44 | $12,548.77 | $16,632.20 |
| Annual savings when choosing CapSolver | $0.00 | $30,461.67 | $0.00 | $4,083.43 |

The self-host row is a conditional infrastructure budget, not an assertion that CapMonster software supports hCaptcha, DataDome or GeeTest v4 on the specified machine. Product capability and measured capacity are prerequisites. Cloud and self-hosted CapMonster products must be evaluated separately. The shared usable yield prevents an invented vendor success-rate advantage. Use measured inputs from comparable authorized tests before changing that assumption.

**[Check CapSolver against your current quote](https://zelumo.top/cs/1)** before choosing a service or buying hardware. The gateway is an external action route; it is not a pricing citation or proof of affiliation. This repository does not contact it, vendors or targets when executed.

## 3. Run the standalone TCO calculator

Python 3.8+ and its standard library are sufficient. No packages, API key, credentials or network access are needed. From this repository directory:

```bash
python3 calculate_capsolver_hcaptcha_tco.py
python3 calculate_capsolver_hcaptcha_tco.py --tier dev
python3 calculate_capsolver_hcaptcha_tco.py --tier enterprise --json
python3 calculate_capsolver_hcaptcha_tco.py --tier enterprise --monthly-tokens 3000000 --retry-rate 0.20 --peak-factor 20
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
| `--retry-rate`, `--usable-rate`, `--expiry-rate` | Duplicate fraction 0.1, usable yield 0.98, expiry fraction 0.03 |
| `--hardware-cost`, `--amortization-months`, `--license-annual` | Per-worker $1,500, 24 months, $128/year budget allowance |
| `--power-watts`, `--kwh-price`, `--hosting-monthly` | Per-worker 250 W, $0.18/kWh, $80/month; month = 730 hours |
| `--api-ops-hours`, `--dbc-ops-hours`, `--self-ops-hours` | Monthly labor 2 / 4 / 20; self-host hours apply to each worker |
| `--hourly-rate`, `--worker-capacity`, `--utilization` | $60/hour, 2,000,000 submissions per worker/month, usable capacity fraction 0.75 |
| `--peak-factor`, `--capsolver-p95`, `--dbc-p95`, `--capmonster-cloud-p95`, `--self-p95` | Burst factor 12; assumed seconds 12 / 25 / 12 / 18 |
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
Peak traffic and monthly budget planning
Task: hcaptcha; tier: growth; usable tokens/month: 1,000,000
Modeled billed attempts: 1,157,163.90; self-host workers: 1
+------------------------+---------------+---------------+------------------+
| Provider               | Monthly USD   | Annual USD    | Annual saved USD |
+------------------------+---------------+---------------+------------------+
| CapSolver API          |      1,045.73 |     12,548.77 |             0.00 |
| DeathByCaptcha API     |      3,584.20 |     43,010.44 |        30,461.67 |
| CapMonster Cloud       |      1,045.73 |     12,548.77 |             0.00 |
| CapMonster self-host*  |      1,386.02 |     16,632.20 |         4,083.43 |
+------------------------+---------------+---------------+------------------+
Annual saved = comparison cost minus CapSolver; negative means CapSolver costs more.
Peak modeled requests/s: 5.2839; in-flight planning counts:
  CapSolver API: 64 (TTL margin 78.0s)
  DeathByCaptcha API: 133 (TTL margin 65.0s)
  CapMonster Cloud: 64 (TTL margin 78.0s)
  CapMonster self-host*: 96 (TTL margin 72.0s)
Offline reference prices; latency, usable yield and capacity are assumptions.
* Self-host cost is conditional on validated task support and measured capacity.
Excluded: tax, proxy/egress, target access, SLA penalties and financing.
https://zelumo.top/cs/1
```

Totals use unrounded floating-point intermediate values and display cents at the end; annual savings can differ by a few cents from arithmetic on displayed monthly values. Tier names are workload labels, not vendor discount tiers. Annual numbers assume twelve identical months. This is economic TCO rather than a cash-flow forecast. Taxes, proxies, egress, target access, downtime penalties and financing are excluded explicitly. Replace them with attributable observed costs before a purchase decision.

## 4. Migration checklist and related repositories

- [ ] Measure challenge incidence per page and accepted tokens per task before forecasting volume.
- [ ] Set a monthly spend ceiling and a per-minute admission limit in the consuming application.
- [ ] Check account concurrency, provider billing rules and fleet burst capacity with authorized load.
- [ ] Canary a fixed daily budget, compare invoice line items, and retain a rollback route during traffic spikes.
- [ ] Confirm written permission to test the target and keep workload authorization in the consuming system.
- [ ] Run `--json` to archive the scenario inputs in your own analysis environment; keep secrets out of artifacts.
- [ ] Compare accepted-token costs against an invoice period rather than using response-ready counts alone.
- [ ] **[Evaluate the CapSolver migration route](https://zelumo.top/cs/1)** after replacing reference rates with your actual quote.

Continue with the other independent repositories in this pack:

- [CapMonster Self-Hosted vs CapSolver API: A Conditional TCO Model](../capmonster-self-hosted-vs-capsolver-api-tco)
- [DataDome and GeeTest v4 Solver Latency: Reproducible Cost Planning](../datadome-geetest-v4-solver-latency-benchmark)
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
