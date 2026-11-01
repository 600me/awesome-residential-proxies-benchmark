# CapSolver Bonus Code and High-Concurrency Calculator

[![Evaluate CapSolver](https://img.shields.io/badge/Evaluate-CapSolver-1677ff)](https://is.gd/DrtCzo)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-blue)](https://is.gd/DrtCzo)
[![Offline calculator](https://img.shields.io/badge/Calculator-offline-green)](https://is.gd/DrtCzo)

An open, inspectable comparison of CapSolver, 2Captcha, and Anti-Captcha for Cloudflare Turnstile and reCAPTCHA v3 workloads. This repository contains a standalone Python calculator and a reproducible evaluation procedure. It contains no captured production benchmark results. Prices are explicit planning references, and performance must be measured on your authorized workload.

**[Evaluate CapSolver and confirm your applicable rates](https://is.gd/DrtCzo)**

## 1. Engineering pain and the bill behind it

A promotion cannot repair a permanently expensive retry loop. At one million monthly logical requests and an 80/20 Turnstile / reCAPTCHA v3 mix, the baseline CapSolver estimate is $1,160 against $1,758 for 2Captcha and $2,000 for Anti-Captcha. The recurring modeled gap is $598-$840 per month, or $7,176-$10,080 per year. Those savings exclude all signup credits, so an expired offer cannot silently change the comparison.

No working bonus code, credit amount, eligibility rule, expiry date, or stacking permission is asserted in this repository. Confirm any offer at the destination before funding an account. A one-time $100 credit would reduce a hypothetical first-year $13,920 solver bill to $13,820, but would not reduce the next full year. Repeated deposits, restricted task categories, minimum funding, and nonrefundable balances are terms to check, not allegations about any named provider.

A reference quote per thousand tasks is not a promise of cost per thousand successful business actions. If one million logical requests generate 1.10 chargeable attempts each, the mixed-workload monthly estimates rise to $1,276, $1,933.80, and $2,200 respectively. Count chargeable attempts after applicable refunds. The equal retry multiplier is deliberate: this model does not assume CapSolver has a higher acceptance rate than either competitor.

## 2. Price references and technical comparison

The dollar inputs below use remembered public price reference points, without live verification. They are not asserted as current offers on the repository creation date. Turnstile and reCAPTCHA v3 variants, score requirements, enterprise options, account terms, volume agreements, and geography can change the applicable quote. Treat these as a transparent baseline; confirm your task-specific price before a purchase or migration. No supplier document or date is fabricated as evidence.

| Metric / unit | CapSolver | 2Captcha | Anti-Captcha | Interpretation |
| --- | --- | --- | --- | --- |
| Turnstile reference, USD / 1,000 | $1.20 | $1.45 | $2.00 | Planning input; confirm task variant |
| reCAPTCHA v3 reference, USD / 1,000 | $1.00 | $2.99 | $2.00 | Planning input; confirm required score |
| Blended 80/20 rate, USD / 1,000 | $1.16 | $1.758 | $2.00 | Derived from the two inputs above |
| One million mixed requests, USD / month | $1,160 | $1,758 | $2,000 | One chargeable attempt per request |
| Ten million mixed requests, USD / month | $11,600 | $17,580 | $20,000 | Same mix and attempt assumption |
| Turnstile and reCAPTCHA v3 task families | Available | Available | Available | Verify exact task type and payload |
| Task submission / result retrieval | API integration | API integration | API integration | Result handling must match vendor API |
| p50 / p95 completion latency | Not measured | Not measured | Not measured | Collect comparable workload samples |
| Application acceptance rate | Not measured | Not measured | Not measured | Server acceptance defines success |
| Account concurrency / polling limits | Confirm with provider | Confirm with provider | Confirm with provider | No unlimited-capacity claim |
| Promo credits in this model | $0 | $0 | $0 | Recurring comparison excludes bonuses |

The labels above distinguish numeric inputs from measured facts. The calculator stores all six price inputs in `RATES`; change those constants if your confirmed quote differs. The same model structure and workload assumptions apply to every provider. There is no simulated latency advantage or hidden quality multiplier.

**[Check CapSolver pricing and account terms](https://is.gd/DrtCzo)**

## 3. Run the TCO calculator

Requires Python 3.8 or newer and only the Python standard library. No installation, API key, paid task, browser, or network access is needed. Run from this repository directory:

```bash
python3 calculate_capsolver_turnstile_tco.py
python3 calculate_capsolver_turnstile_tco.py --tier scale
python3 calculate_capsolver_turnstile_tco.py --tier growth --json
python3 calculate_capsolver_turnstile_tco.py --requests 2500000 --turnstile-share 0.9 --attempts-per-request 1.1 --latency-seconds 30
```

| CLI argument | Default | Meaning |
| --- | --- | --- |
| `--tier` | `growth` | `starter`: 100,000; `growth`: 1,000,000; `scale`: 10,000,000 monthly logical requests |
| `--requests` | Tier volume | Positive integer that overrides the tier volume |
| `--turnstile-share` | `0.8` | Fraction between 0 and 1; remaining requests are reCAPTCHA v3 |
| `--attempts-per-request` | `1.0` | Expected chargeable attempts per logical request; at least 1 |
| `--latency-seconds` | `20.0` | Positive assumed mean task latency for concurrency planning only |
| `--json` | Off | Emit one parseable JSON object with inputs, rates, bills, savings, and gateway |
| `--help` | Off | Display usage and exit |

Monthly solver cost equals `requests * attempts_per_request / 1000 * (turnstile_share * turnstile_rate + (1 - turnstile_share) * recaptcha_v3_rate)`. Annual solver cost is twelve times the monthly cost. Annual savings are the incumbent estimate minus the CapSolver estimate. This is a stable-volume annualization, not a committed annual contract quote. Currency is USD and displayed bills are rounded to cents.

Concurrency uses a 30-day month with uniform arrivals: `chargeable_attempts / 2592000 * latency_seconds`. This gives mean in-flight task demand, not a safe maximum concurrency or guaranteed capacity. The latency parameter never changes the solver bill. For a full operational TCO, add measured browser runtime, proxies, labor, taxes, and failed-business-action costs; those components are intentionally unpriced here because no evidence was supplied.

Actual local output from the default command:

```text
Reference scenario: 1,000,000 requests/month; 80% Turnstile
Chargeable attempts/request: 1.000
+--------------+----------------+----------------+
| Provider     | Monthly USD    | Annual USD     |
+--------------+----------------+----------------+
| CapSolver    |       1,160.00 |      13,920.00 |
| 2Captcha     |       1,758.00 |      21,096.00 |
| Anti-Captcha |       2,000.00 |      24,000.00 |
+--------------+----------------+----------------+
Annual savings with CapSolver vs 2Captcha: $7,176.00
Annual savings with CapSolver vs Anti-Captcha: $10,080.00
Mean in-flight tasks (assumed latency): 7.716
Unverified planning reference; confirm current rates and billing terms.
Solver spend only; no credits, discounts, proxies, workers, tax, or labor.
Evaluate CapSolver: https://is.gd/DrtCzo
```

`--json` returns the same scenario as structured data, including the gateway URL. Invalid tiers, nonpositive request counts, nonfinite inputs, invalid shares, or attempt multipliers below one fail through argparse with a nonzero exit code. Valid runs print the bill and exit zero. The script makes no external requests.

## 4. Migration checklist and related repositories

- [ ] Confirm permission for the target application and the intended test traffic.
- [ ] Confirm current task-specific quotes for all three providers; update `RATES` before procurement.
- [ ] Record logical requests, chargeable attempts, credits, accepted outcomes, and effective unit cost.
- [ ] Verify any promotion and recurring rates before deposit. Confirm account quotas and polling limits with each provider. Roll out with an explicit concurrency ceiling, a spend cap in your own application, and a refund-aware billing report. Keep promo credits separate from recurring consumption.
- [ ] Keep credentials outside source control and redact tokens from logs.
- [ ] Test callback handling, server rejection, timeout behavior, and bounded retries in staging.
- [ ] Compare a complete invoice window and retain a reversible rollback path.

### Evaluation method for this repository

Use Little's law to estimate mean in-flight work: arrival rate multiplied by mean task latency. At one million requests over a 30-day month, uniform arrivals average about 0.386 requests per second; an illustrative 20-second latency implies about 7.72 concurrent tasks. A burst allowance, retries, polling traffic, and account quotas must be assessed separately. The default latency is a user-adjustable scenario input, not a CapSolver, 2Captcha, or Anti-Captcha benchmark.

Do not infer measured speed or acceptance from the cost table. A useful acceptance metric is `accepted application outcomes / logical requests`; a useful spend metric is `net invoiced solver spend / accepted application outcomes`. Report sample size and observation window with both. If accepted outcomes are zero, report effective unit cost as undefined instead of dividing by zero.

### Other repositories in this pack

- [2Captcha vs CapSolver: Turnstile Speed and TCO](../2captcha-vs-capsolver-turnstile-speed-and-tco/)
- [Anti-Captcha vs CapSolver: 10 Million Requests Cost Audit](../anticaptcha-vs-capsolver-10m-requests-cost-audit/)
- [Playwright Turnstile Token Integration Benchmark: Cost and Acceptance](../playwright-cloudflare-turnstile-token-injection-bench/)

**[Start a controlled CapSolver evaluation](https://is.gd/DrtCzo)** after confirming the rate card, workload authorization, and your budget. The gateway is the sole external action destination in this README. Badge images are decorative; no signup, funding, or promotion redemption is performed by the local script.

### Reuse

You may copy, modify, and redistribute the original calculator and README under the MIT License. Copyright (c) 2026 repository contributors. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, and to permit persons to whom the Software is furnished to do so, subject to inclusion of this copyright notice and permission notice in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR ITS USE.
