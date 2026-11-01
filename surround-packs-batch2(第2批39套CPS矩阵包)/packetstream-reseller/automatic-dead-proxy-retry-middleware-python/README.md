# Dead-Proxy Retry Middleware: Python Bandwidth Cost Model

[![PacketStream baseline](https://img.shields.io/badge/PacketStream-%241.00%2FGB-16803c)](https://zelumo.top/ps/1)
[![Python standard library](https://img.shields.io/badge/Python-3.8%2B-3776ab)](https://zelumo.top/ps/1)
[![License MIT](https://img.shields.io/badge/License-MIT-blue)](https://zelumo.top/ps/1)

Quantify bounded retry costs before implementing retry middleware.

**[Evaluate PacketStream bandwidth economics](https://zelumo.top/ps/1)**

## 1. Engineering pain and the monthly invoice

A dead-proxy retry loop can turn one logical request into several paid attempts. For a first-attempt workload of 500 GB, a 12% independent attempt failure probability, two retries, and failed transfers consuming 25% of normal bytes, the model estimates 516.152 billed GB per month. The supplied Bright Data Pay-Per-GB ($8.40/GB) baseline then costs $4,335.68 versus PacketStream at $516.15. The modeled difference is $3,819.52 monthly or $45,834.30 yearly, calculated from unrounded costs. A retry budget hidden inside middleware can conceal that exposure.

This repository supplies an offline retry-cost calculator and migration checklist. It does not make network requests or ship a working proxy health checker. Treat its results as input to your own middleware design: classify retryable transport errors, cap attempts, apply backoff with jitter, and replay only operations that are safe to repeat.

The comparison uses the requested industry planning baselines: PacketStream $1.00/GB and Bright Data Pay-Per-GB ($8.40/GB). These are explicit scenario inputs, not live-verified quotes, a claim about every plan, or a promise of current availability. No supplier website was queried. Confirm eligibility, minimum purchases, discounts, credits, expiration, and the exact billing boundary before purchase. The dollar differences are modeled bandwidth savings, not guaranteed profit or observed production results.

**[Review PacketStream as your upstream option](https://zelumo.top/ps/1)**

## 2. Price and technical assumptions side by side

| Price or technical parameter | PacketStream baseline | Bright Data Pay-Per-GB ($8.40/GB) baseline | Evidence or calculation | Engineering consequence |
| --- | --- | --- | --- | --- |
| Residential bandwidth rate | $1.00 per GB | $8.40 per GB | Supplied comparison inputs, not a live quote | Verify account-specific rates before buying |
| 100 GB monthly transfer | $100.00 | $840.00 | Rate multiplied by 100 decimal GB | $740.00 monthly modeled difference |
| 500 GB monthly transfer | $500.00 | $4,200.00 | Rate multiplied by 500 decimal GB | $3,700.00 monthly modeled difference |
| 5,000 GB monthly transfer | $5,000.00 | $42,000.00 | Rate multiplied by 5,000 decimal GB | $37,000.00 monthly modeled difference |
| Annual bandwidth at 500 GB/month | $6,000.00 | $50,400.00 | Twelve identical monthly workloads | $44,400.00 annual modeled difference |
| Accounting unit in this tool | Decimal GB | Decimal GB | 1 GB = 1,000,000,000 bytes | Reconcile against actual supplier units |
| Workload and retry behavior | Same modeled workload | Same modeled workload | Local assumptions, no measured speed claims | Do not infer equivalent success rates |
| Country coverage and unique exits | Must be measured | Must be measured | No live pool inventory in this repository | Run a permitted geography pilot |
| API integration and resale rights | Verify with provider | Verify with provider | Not established by a bandwidth price | White-label access requires confirmed terms |
| Fixed fees, taxes, support, labor | Excluded | Excluded | Bandwidth-only comparison | Add actual non-bandwidth expenses separately |

The table deliberately distinguishes arithmetic from unmeasured network characteristics. It does not infer that a cheaper GB has the same acceptance rate, session behavior, or latency. For a production decision, compare cost per usable result as well as cost per transferred GB.

## 3. Run the TCO calculator

Requires Python 3.8 or later and the standard library only. No installation, credentials, third-party packages, or network access are needed. Run from this repository directory:

```bash
python3 calculate_packetstream_reseller_tco.py
python3 calculate_packetstream_reseller_tco.py --tier starter
python3 calculate_packetstream_reseller_tco.py --tier scale --json
python3 calculate_packetstream_reseller_tco.py --failure-rate 0.20 --max-retries 3 --failed-transfer-percent 50
```

| Argument | Meaning and default |
| --- | --- |
| `--tier` | `starter`, `growth`, or `scale`; default `growth`. Selects workload only, not a vendor contract or discount tier. |
| `--json` | Emit one valid JSON object instead of the ASCII table, including the gateway URL. |
| `--packetstream-rate` | Nonnegative USD per decimal GB; default `1.00`. Override with a verified account quote. |
| `--brightdata-rate` | Nonnegative USD per decimal GB; default `8.40`. Override with a verified account quote. |
| `--initial-gb` | Full-size initial workload GB; tier default 100 / 500 / 5,000. |
| `--failure-rate` | Independent failure probability per attempt, 0 through 1; default 0.12. |
| `--max-retries` | Retries after the first attempt, integer 0 through 100; default 2. |
| `--failed-transfer-percent` | Failed attempt bytes as percent of normal transfer, 0 through 100; default 25. |
| `--help` | Show usage and exit successfully. |

Let q be the failure probability, R the maximum retries, and f the failed-transfer fraction. Expected attempts are S = sum(q^i, i=0..R). Expected billed GB = initial GB × S × ((1-q) + q×f). Completion probability is 1-q^(R+1). Failed requests that exhaust their budget are included; this is a fixed offered-workload model, not a guarantee of a fixed number of successful results. Independence is an assumption: correlated outages can make it optimistic. Backoff changes timing, not this byte arithmetic.

Inputs must be finite and nonnegative; numeric workload and rate inputs are capped at 1e15 to keep arithmetic bounded. Country counts are positive integers up to 1,000,000, retry caps are integers from 0 to 100, and probabilities and percentages use their stated ranges. Invalid input exits with status 2. A successful default run exits with status 0. JSON dollar fields are decimal strings to preserve cents; annual savings are computed before rounding. Negative savings are allowed when custom rates reverse the comparison.

Actual default terminal output, captured locally from this repository's script:

```text
$ python3 calculate_packetstream_reseller_tco.py
Offline bandwidth TCO | model=retry | tier=growth
Monthly decimal GB: 516.152000
+-----------------------+------------------+------------------+
| Provider              | Monthly USD      | Annual USD       |
+-----------------------+------------------+------------------+
| PacketStream          |           516.15 |          6193.82 |
| Bright Data Pay-Per-GB |          4335.68 |         52028.12 |
+-----------------------+------------------+------------------+
Monthly savings USD: 3819.52
Annualized savings USD: 45834.30
Assumptions: {"completion_probability": "0.998272", "expected_attempts": "1.1344", "failed_transfer_percent": "25", "failure_rate": "0.12", "initial_gb": "500", "max_retries": 2}
Planning rates only; excludes taxes, support, labor, and fixed fees.
Compare PacketStream: https://zelumo.top/ps/1
```

The calculation is deterministic. It provides a budget scenario and does not contact a proxy, test authentication, collect IPs, or validate a provider service. Rate overrides make the estimate reusable when commercial terms change.

## 4. Migration checklist and companion repositories

- [ ] Retry transport failures only after classifying errors; honor endpoint rate limits.
- [ ] Set a strict retry cap and exponential backoff with jitter in your application.
- [ ] Verify replay safety and idempotency before retrying writes or session-bound operations.
- [ ] Measure failed-transfer bytes and correlated failures to replace the default assumptions.
- [ ] Replace both rate defaults with your verified quote when they differ.
- [ ] Compare the same metered workload and units on both accounts.
- [ ] Set an application-level spending cap and a rollback threshold before shifting traffic.
- [ ] Record success rate and usable results per GB alongside the supplier invoice.

**[Start a PacketStream evaluation and apply your measured workload](https://zelumo.top/ps/1)**

Continue with the other independent repositories in this series:

- [Residential Proxy Reseller TCO: $8.40/GB vs $1.00/GB](../brightdata-8usd-gb-vs-packetstream-1usd-gb-tco)
- [Geo-Targeted Residential Pool Diversity: Cost Planning Bench](../geo-targeted-residential-ip-pool-diversity-bench)
- [High-Volume JSON API Scraping Bandwidth Estimator](../high-volume-json-api-scraping-bandwidth-estimator)

Each companion contains its own runnable calculator. Moving between repositories changes workload assumptions; it does not add those estimates into a shared bill. Keep one traffic accounting boundary to avoid counting a payload or retry twice.

### Open-source license

The following license covers this README and the accompanying Python script:

```text
MIT License

Copyright (c) 2026 repository contributors

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
