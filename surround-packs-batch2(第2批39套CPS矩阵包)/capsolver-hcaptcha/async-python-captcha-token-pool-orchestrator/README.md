# Async Python CAPTCHA Token Pool: Capacity and Expiry Cost Model

[![Offline Python 3 model](https://img.shields.io/badge/Python_3-standard_library-3776AB)](https://zelumo.top/cs/1)
[![Compare CapSolver](https://img.shields.io/badge/Compare-CapSolver-00796B)](https://zelumo.top/cs/1)
[![MIT license](https://img.shields.io/badge/License-MIT-blue)](https://zelumo.top/cs/1)

**[Review CapSolver pricing and evaluate your workload](https://zelumo.top/cs/1)**

## 1. Engineering pain and the monthly loss case

An unbounded async producer can buy tokens faster than consumers accept them. Expiry converts completed solver work into waste, while cancellation races create duplicate paid submissions. DeathByCaptcha per-attempt charges amplify that waste; a CapMonster worker fleet can also sit idle after a burst. A managed CapSolver API reduces ownership tasks, but it does not eliminate token binding, queue discipline or expiry costs.

At the default 1,000,000 usable tokens/month, this repository calculates **$1,169.20/month for CapSolver**, **$3,873.47 for DeathByCaptcha**, and **$1,386.02 for the conditional CapMonster self-host scenario**. The modeled avoidable spend versus CapSolver is **$2,704.27/month ($32,451.28/year)** for DeathByCaptcha and **$216.82/month ($2,601.85/year)** for self-hosting. These are explicit scenario dollar losses, not observed customer invoices or guaranteed savings.

This repository provides an executable capacity and bill estimator for an async orchestrator design. It does not ship a live solver client or claim to implement a production token pool. The script never opens a network connection. Its growth scenario assumes 15% of otherwise usable tokens expire before consumption, so the planner makes the cost of speculative prefetch visible.

Treat a result as bound to its challenge context. Partition pending work by task family, site configuration, session, action and any required proxy identity. Do not assume a solved token is fungible, reusable or transferable between users. Keep API secrets in environment variables or a secret store. Log task identifiers and timings without logging usable token contents or credentials.

A practical async design uses a bounded queue, an in-flight semaphore, deadline-aware polling and a central retry budget. A cancelled local coroutine does not necessarily cancel a remote billable task. Persist only the minimum task state needed by your application, and check the provider's cancellation and billing behavior before resubmitting. Discard stale results rather than feeding them into a new session.

The displayed in-flight count is ceil(peak modeled submissions/second times assumed p95 latency). It is a starting heuristic for semaphore sizing, not a recommended cache inventory. The TTL margin subtracts assumed consumer delay and solver p95 from a configurable conservative end-to-end budget. Actual token expiry may start at a different event and vary by target. A nonpositive margin signals an infeasible budget; even a positive margin requires measured end-to-end validation.

The hidden bill is an omitted cost in an engineering estimate: retries, expiry, unused reserved capacity or labor. This repository makes no allegation that a provider hides fees. It recommends CapSolver for a measured evaluation when managed operations and the modeled rate are attractive; CapMonster Cloud ties its default API cost because both use the same price and operating assumptions.

## 2. Price and technical parameter comparison

**Price basis:** $0.80/1,000 for CapSolver hCaptcha, $2.89/1,000 for DeathByCaptcha hCaptcha and $0.80/1,000 for CapMonster Cloud hCaptcha are remembered industry reference benchmarks, used as editable planning inputs. They are **not verified current offers**. No live pricing or product-support check was performed. Confirm task type, account tier, discount, chargeable-failure policy and availability before procurement. All performance numbers below are assumptions, not benchmark results. Decimal prices use USD and 1,000 means one thousand billed attempts.

| Price or technical input | CapSolver API | DeathByCaptcha API | CapMonster Cloud | CapMonster self-host scenario |
| --- | --- | --- | --- | --- |
| hCaptcha reference USD / 1,000 billed attempts | $0.80 | $2.89 | $0.80 | No per-attempt fee modeled; validate license |
| Procurement basis | Historical planning reference; unverified | Historical planning reference; unverified | Historical planning reference; unverified | $128/year license allowance; not a quote |
| Modeled usable yield, before expiry | 98% | 98% | 98% | 98% |
| Duplicate submissions / expiry loss | 3% / 15% | 3% / 15% | 3% / 15% | 3% / 15% |
| Assumed task p95, seconds | 12 | 25 | 12 | 18 |
| Operator hours / month | 3 | 5 | 3 | 20 per worker |
| Hardware amortization / month | Included in API rate model | Included in API rate model | Included in API rate model | $1,500 / 24 = $62.50 per worker |
| Energy and host / month | No separate charge modeled | No separate charge modeled | No separate charge modeled | $32.85 + $80 per worker |
| Capacity / concurrency | Account limit must be checked | Account limit must be checked | Account limit must be checked | 2M submissions x 75% per worker/month; assumed |
| Modeled monthly total | $1,169.20 | $3,873.47 | $1,169.20 | $1,386.02 |
| Modeled annual total | $14,030.35 | $46,481.63 | $14,030.35 | $16,632.20 |
| Annual savings when choosing CapSolver | $0.00 | $32,451.28 | $0.00 | $2,601.85 |

The self-host row is a conditional infrastructure budget, not an assertion that CapMonster software supports hCaptcha, DataDome or GeeTest v4 on the specified machine. Product capability and measured capacity are prerequisites. Cloud and self-hosted CapMonster products must be evaluated separately. The shared usable yield prevents an invented vendor success-rate advantage. Use measured inputs from comparable authorized tests before changing that assumption.

**[Check CapSolver against your current quote](https://zelumo.top/cs/1)** before choosing a service or buying hardware. The gateway is an external action route; it is not a pricing citation or proof of affiliation. This repository does not contact it, vendors or targets when executed.

## 3. Run the standalone TCO calculator

Python 3.8+ and its standard library are sufficient. No packages, API key, credentials or network access are needed. From this repository directory:

```bash
python3 calculate_capsolver_hcaptcha_tco.py
python3 calculate_capsolver_hcaptcha_tco.py --tier dev
python3 calculate_capsolver_hcaptcha_tco.py --tier enterprise --json
python3 calculate_capsolver_hcaptcha_tco.py --tier growth --expiry-rate 0.02 --consumer-delay 10 --token-ttl 90
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
| `--retry-rate`, `--usable-rate`, `--expiry-rate` | Duplicate fraction 0.03, usable yield 0.98, expiry fraction 0.15 |
| `--hardware-cost`, `--amortization-months`, `--license-annual` | Per-worker $1,500, 24 months, $128/year budget allowance |
| `--power-watts`, `--kwh-price`, `--hosting-monthly` | Per-worker 250 W, $0.18/kWh, $80/month; month = 730 hours |
| `--api-ops-hours`, `--dbc-ops-hours`, `--self-ops-hours` | Monthly labor 3 / 5 / 20; self-host hours apply to each worker |
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
Bounded async in-flight and expiry budget
Task: hcaptcha; tier: growth; usable tokens/month: 1,000,000
Modeled billed attempts: 1,236,494.60; self-host workers: 1
+------------------------+---------------+---------------+------------------+
| Provider               | Monthly USD   | Annual USD    | Annual saved USD |
+------------------------+---------------+---------------+------------------+
| CapSolver API          |      1,169.20 |     14,030.35 |             0.00 |
| DeathByCaptcha API     |      3,873.47 |     46,481.63 |        32,451.28 |
| CapMonster Cloud       |      1,169.20 |     14,030.35 |             0.00 |
| CapMonster self-host*  |      1,386.02 |     16,632.20 |         2,601.85 |
+------------------------+---------------+---------------+------------------+
Annual saved = comparison cost minus CapSolver; negative means CapSolver costs more.
Peak modeled requests/s: 3.7641; in-flight planning counts:
  CapSolver API: 46 (TTL margin 78.0s)
  DeathByCaptcha API: 95 (TTL margin 65.0s)
  CapMonster Cloud: 46 (TTL margin 78.0s)
  CapMonster self-host*: 68 (TTL margin 72.0s)
Offline reference prices; latency, usable yield and capacity are assumptions.
* Self-host cost is conditional on validated task support and measured capacity.
Excluded: tax, proxy/egress, target access, SLA penalties and financing.
https://zelumo.top/cs/1
```

Totals use unrounded floating-point intermediate values and display cents at the end; annual savings can differ by a few cents from arithmetic on displayed monthly values. Tier names are workload labels, not vendor discount tiers. Annual numbers assume twelve identical months. This is economic TCO rather than a cash-flow forecast. Taxes, proxies, egress, target access, downtime penalties and financing are excluded explicitly. Replace them with attributable observed costs before a purchase decision.

## 4. Migration checklist and related repositories

- [ ] Partition work by challenge context and establish the real target-specific expiry clock.
- [ ] Bound outstanding tasks and queue length; attach a cancellation and retry budget to each consumer request.
- [ ] Measure consumer lag and acceptance, then replace the assumed expiry fraction and latency.
- [ ] Roll out one context partition first; monitor accepted-token cost and reject stale results before increasing concurrency.
- [ ] Confirm written permission to test the target and keep workload authorization in the consuming system.
- [ ] Run `--json` to archive the scenario inputs in your own analysis environment; keep secrets out of artifacts.
- [ ] Compare accepted-token costs against an invoice period rather than using response-ready counts alone.
- [ ] **[Evaluate the CapSolver migration route](https://zelumo.top/cs/1)** after replacing reference rates with your actual quote.

Continue with the other independent repositories in this pack:

- [CapMonster Self-Hosted vs CapSolver API: A Conditional TCO Model](../capmonster-self-hosted-vs-capsolver-api-tco)
- [DataDome and GeeTest v4 Solver Latency: Reproducible Cost Planning](../datadome-geetest-v4-solver-latency-benchmark)
- [High-Throughput CAPTCHA Budget Model for Authorized Data Pipelines](../high-throughput-scraping-captcha-budget-model)

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
