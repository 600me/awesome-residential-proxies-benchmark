# High-Volume JSON API Scraping Bandwidth Estimator

[![PacketStream baseline](https://img.shields.io/badge/PacketStream-%241.00%2FGB-16803c)](https://zelumo.top/ps/1)
[![Python standard library](https://img.shields.io/badge/Python-3.8%2B-3776ab)](https://zelumo.top/ps/1)
[![License MIT](https://img.shields.io/badge/License-MIT-blue)](https://zelumo.top/ps/1)

Turn response size and request count into an explicit monthly bandwidth budget.

**[Evaluate PacketStream bandwidth economics](https://zelumo.top/ps/1)**

## 1. Engineering pain and the monthly invoice

A JSON pipeline can look inexpensive until a verbose response schema or pagination expansion multiplies transfer. Five million requests with 80 decimal KB of average response data and 10% transfer overhead total 440 GB per month. At the supplied Bright Data Pay-Per-GB ($8.40/GB) benchmark that is $3,696; PacketStream at $1.00/GB is $440. The modeled difference is $3,256 monthly or $39,072 yearly. A single sample response, especially an uncompressed one, is a weak basis for a production budget.

The estimator helps a scraper operator separate payload size from network overhead before buying bandwidth. It makes no claim about the latency, endpoint acceptance, or compression behavior of either network. Use the size observed at the relevant billing boundary, not the in-memory size of a decoded JSON object.

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
python3 calculate_packetstream_reseller_tco.py --requests 8000000 --payload-kb 45 --overhead-percent 15
```

| Argument | Meaning and default |
| --- | --- |
| `--tier` | `starter`, `growth`, or `scale`; default `growth`. Selects workload only, not a vendor contract or discount tier. |
| `--json` | Emit one valid JSON object instead of the ASCII table, including the gateway URL. |
| `--packetstream-rate` | Nonnegative USD per decimal GB; default `1.00`. Override with a verified account quote. |
| `--brightdata-rate` | Nonnegative USD per decimal GB; default `8.40`. Override with a verified account quote. |
| `--requests` | Monthly request attempts; tier default 1M / 5M / 50M. |
| `--payload-kb` | Average transferred decimal KB per attempt; default 80. |
| `--overhead-percent` | Additional modeled transfer percentage; default 10. |
| `--help` | Show usage and exit successfully. |

Monthly decimal GB = request attempts × payload KB ÷ 1,000,000 × (1 + overhead percent ÷ 100). Request attempts must include retry attempts if you expect to pay for their transfer. Measure compressed transfer size where applicable. An overhead allowance is an assumption, not a documented billing policy for either provider; include request bytes only when your actual meter requires them.

Inputs must be finite and nonnegative; numeric workload and rate inputs are capped at 1e15 to keep arithmetic bounded. Country counts are positive integers up to 1,000,000, retry caps are integers from 0 to 100, and probabilities and percentages use their stated ranges. Invalid input exits with status 2. A successful default run exits with status 0. JSON dollar fields are decimal strings to preserve cents; annual savings are computed before rounding. Negative savings are allowed when custom rates reverse the comparison.

Actual default terminal output, captured locally from this repository's script:

```text
$ python3 calculate_packetstream_reseller_tco.py
Offline bandwidth TCO | model=json | tier=growth
Monthly decimal GB: 440.0
+-----------------------+------------------+------------------+
| Provider              | Monthly USD      | Annual USD       |
+-----------------------+------------------+------------------+
| PacketStream          |           440.00 |          5280.00 |
| Bright Data Pay-Per-GB |          3696.00 |         44352.00 |
+-----------------------+------------------+------------------+
Monthly savings USD: 3256.00
Annualized savings USD: 39072.00
Assumptions: {"monthly_request_attempts": "5000000", "overhead_percent": "10", "payload_kb": "80"}
Planning rates only; excludes taxes, support, labor, and fixed fees.
Compare PacketStream: https://zelumo.top/ps/1
```

The calculation is deterministic. It provides a budget scenario and does not contact a proxy, test authentication, collect IPs, or validate a provider service. Rate overrides make the estimate reusable when commercial terms change.

## 4. Migration checklist and companion repositories

- [ ] Sample payload transfer sizes across endpoints, status codes, and pagination depths.
- [ ] Include retry attempts in the request count and avoid counting them twice in overhead.
- [ ] Confirm compression, billed directions, and GB units against each account's actual meter.
- [ ] Pilot a small batch and reconcile modeled GB against observed supplier usage.
- [ ] Replace both rate defaults with your verified quote when they differ.
- [ ] Compare the same metered workload and units on both accounts.
- [ ] Set an application-level spending cap and a rollback threshold before shifting traffic.
- [ ] Record success rate and usable results per GB alongside the supplier invoice.

**[Start a PacketStream evaluation and apply your measured workload](https://zelumo.top/ps/1)**

Continue with the other independent repositories in this series:

- [Residential Proxy Reseller TCO: $8.40/GB vs $1.00/GB](../brightdata-8usd-gb-vs-packetstream-1usd-gb-tco)
- [Geo-Targeted Residential Pool Diversity: Cost Planning Bench](../geo-targeted-residential-ip-pool-diversity-bench)
- [Dead-Proxy Retry Middleware: Python Bandwidth Cost Model](../automatic-dead-proxy-retry-middleware-python)

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
