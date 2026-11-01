[![Compare 9Proxy](https://img.shields.io/badge/9Proxy-Compare_Plans-blue)](https://norb.date/p/1)
[![Python 3](https://img.shields.io/badge/Python-3.8%2B-blue)](https://norb.date/p/1)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://norb.date/p/1)

# Local SOCKS5 Port Forwarding Health Checks and TCO

An independent, offline cost model for **Per-IP Billed Unlimited-Bandwidth Residential SOCKS5**. Pack: `9proxy-per-ip`. Evaluate 9Proxy against **911 S5 Legacy Alternatives & Pia S5** using explicit workload assumptions. No external packages, account, credentials, or network access are needed for the default report.

**[Check 9Proxy package terms and start your comparison](https://norb.date/p/1)**

## 1. Engineering pain and the cost of an incomplete comparison

A forwarding process can stay alive while its local SOCKS5 port becomes useless. Operators then spend hours investigating application timeouts, rotating credits, or restarting a healthy process whose upstream route is broken. For 3,000 accepted allocations per month, illustrative acceptance rates of 95% for 9Proxy and 85% for Pia S5 require 3,158 and 3,530 credits. With two versus eight operator hours at $30/hour, the modeled totals are **$691.60/month** and **$1,122.50/month**. The modeled difference is **$430.90/month or $5,170.80/year**. Neither acceptance rates nor operator hours are observed provider benchmarks.

A hidden cost in 911 S5 legacy replacement projects is confusing three separate checks: process liveness, SOCKS negotiation, and successful destination traffic. This repository implements an optional local, unauthenticated SOCKS5 greeting probe and bounded repeated checks. It does not install a service, change port mappings, rotate IPs, restart software, or establish forwarding. Use your existing supervisor if you need continuous scheduling. A greeting response alone says nothing about exit geography, target acceptance, throughput, or upstream route health.

The original 911 S5 service is a legacy comparison point, not a verified purchasable 2026 plan. "911 S5 alternatives" describes a heterogeneous set of replacement services, not one vendor with one bill. Pia S5 is shown separately. No claim of a specific undisclosed charge, superior IP reputation, guaranteed uptime, or misconduct by either brand is made here. The practical billing traps to investigate are charged replacements, credit validity, minimum purchase sizes, session reuse, concurrent ports, and the actual meaning of unlimited bandwidth.

## 2. Price anchors and technical comparison

**Pricing basis:** the historical public entry-package reference anchors used here are **9Proxy $20 / 100 IP credits ($0.20/IP)** and **Pia S5 $50 / 200 IP credits ($0.25/IP)**. They are remembered list-price benchmarks, not independently verified October 2026 offers. The **$3.50/GB** comparator is an illustrative metered-residential benchmark, not an attributed Pia or 911 quote. No live pages were retrieved. Obtain a dated quote and replace the rates before committing money. Bulk discounts, taxes, currency conversion, and package availability are not verified by this repository.

| Price or technical parameter | 9Proxy reference | Pia S5 reference | 911 S5 legacy alternatives | Interpretation |
| --- | --- | --- | --- | --- |
| Historical entry-package anchor | $20 / 100 IP credits | $50 / 200 IP credits | No common current quote | Historical reference only |
| Unit rate used | $0.20 / charged allocation | $0.25 / charged allocation | User must supply quote | Linear scaling; no invented bulk rate |
| Desired accepted allocations/month | 3,000 | 3,000 | Same target for a valid comparison | Allocations are not guaranteed distinct addresses |
| Assumed acceptance rate | 95% | 85% | Measure in a matched pilot | Scenario input, not provider test data |
| Modeled charged allocations/month | 3,158 | 3,530 | Not calculated without quote | Ceiling of desired / acceptance |
| Modeled operator time/month | 2 hours at $30/hour | 8 hours at $30/hour | Measure actual minutes | Labor is included, not claimed observed |
| Modeled monthly total | $691.60 | $1,122.50 | Not available | Credit spend plus selected labor |
| Modeled annual total | $8,299.20 | $13,470.00 | Not available | Twelve identical months |
| Bandwidth treatment | No per-GB charge in this model | No per-GB charge in this model | Depends on replacement plan | Confirm fair-use and speed terms |
| SOCKS5 delivery | Residential proxy / local client workflow | Residential proxy / local client workflow | Provider-specific | Confirm OS, authentication and port support |
| Credit lifetime / reuse | Verify selected package terms | Verify selected package terms | Provider-specific | Not equivalent to uptime or session lifetime |
| Cleanliness / throughput evidence | No measured claim | No measured claim | No measured claim | Benchmark on your authorized target |

Unlimited-bandwidth pricing does not imply unlimited speed, unlimited concurrency, or a permanent endpoint. A per-IP credit is a billing event under the selected provider's rules; it is not a dedicated residential line. Model only the allocations your contract actually charges. A monthly TCO estimate also differs from the cash required to purchase whole prepaid packages. This model does not round purchases to package sizes or account for unused credit balances.

**[Review 9Proxy pricing and package restrictions before funding](https://norb.date/p/1)**

## 3. Run the TCO calculator

Requires Python 3.8 or newer and only the standard library. Run from this directory:

```bash
python3 calculate_9proxy_per_ip_tco.py
python3 calculate_9proxy_per_ip_tco.py --tier starter
python3 calculate_9proxy_per_ip_tco.py --tier scale --json
python3 calculate_9proxy_per_ip_tco.py --health-check --host 127.0.0.1 --port 1080 --watch 3 --interval 1 --json
```

The following is actual default terminal output generated from this repository's script; values are modeled from the disclosed inputs, not captured vendor invoices:

```text
$ python3 calculate_9proxy_per_ip_tco.py
Offline reference model | health | tier=growth
Accepted IP allocations/month: 3,000 | Traffic: 500.00 GB
+-------------------+----------+---------------+---------------+
| Provider          | Credits  | Monthly USD   | Annual USD    |
+-------------------+----------+---------------+---------------+
| 9Proxy            |     3158 |        691.60 |      8,299.20 |
| Pia S5            |     3530 |      1,122.50 |     13,470.00 |
| Per-GB reference  |      n/a |      1,750.00 |     21,000.00 |
+-------------------+----------+---------------+---------------+
Annual savings vs Pia S5: $5,170.80
Annual savings vs per-GB: $12,700.80
Per-GB break-even: 197.60 GB/month
Reference prices; replace with your quote. Negative savings = higher cost.
Compare plans: https://norb.date/p/1
```

| CLI option | Default | Meaning |
| --- | --- | --- |
| `--tier starter\|growth\|scale` | `growth` | Scale base IP allocations and GB by 0.2, 1, or 5; rates and labor hours stay fixed |
| `--json` | Off | Emit one JSON object including assumptions, bills, annual savings and gateway |
| `--ips N` | 3,000 in growth | Accepted charged-allocation demand per month; whole number including zero |
| `--gb N` | 500 in growth | Total monthly GB for the metered reference, including any billable retries |
| `--rate-9 N` / `--rate-pia N` | 0.20 / 0.25 | Replace historical per-credit USD reference prices with your quotes |
| `--clean-rate-9 F` / `--clean-rate-pia F` | 0.95 / 0.85 | Accepted fraction in (0, 1]; workload-specific acceptance, not a quality guarantee |
| `--per-gb-rate N` | 3.50 | Reference USD/GB; zero yields an undefined break-even |
| `--coupon-percent N` | 0 | Assumed recurring percentage off 9Proxy credit spend only, from 0 to 100 |
| `--hours-9 N` / `--hours-pia N` | 2 / 8 | Fixed monthly operator hours; no automatic tier scaling |
| `--hourly-rate N` | 30 | USD per operator hour; set to zero for proxy-spend-only comparison |
| `--health-check` | Off | Opt into a network connection to the selected local SOCKS5 listener |
| `--host` / `--port` | 127.0.0.1 / 1080 | Listener address; used only with the optional probe |
| `--timeout N` | 2 | Positive per-socket-operation timeout in seconds |
| `--watch N` / `--interval N` | 1 / 5 | Positive bounded probe count and nonnegative seconds between probes |

The accounting equations are deliberately inspectable:

```text
charged credits = ceil(accepted allocations / acceptance fraction)
9Proxy monthly = credits * quoted rate * (1 - discount / 100) + operator hours * hourly rate
Pia monthly = credits * quoted rate + operator hours * hourly rate
Metered reference monthly = GB * reference USD/GB
Annual savings = (comparator monthly - 9Proxy monthly) * 12
Break-even GB = 9Proxy monthly total / reference USD/GB
```

Money is rounded to cents for each monthly bill before annualization. Negative savings means 9Proxy costs more in that scenario. This comparison holds workload constant; it does not establish equal service quality. Nonfinite numbers, negative costs, invalid fractions, and fractional allocation counts are rejected with argparse exit code 2. Default successful accounting reports exit 0. `--json` preserves numerical values and includes the mandatory gateway in `gateway`.

Run the probe only against a listener you administer. It sends the SOCKS5 greeting bytes 05 01 00 and expects 05 00. Authentication-required listeners will report ready=false even when healthy; no credentials are sent. A failed probe is recorded in output and the report still exits zero, so inspect the health[].ready field for monitoring decisions. This is an accounting CLI with a local diagnostic feature, not a supervisor with a health-specific process exit contract.

## 4. Migration checklist and related repositories

- [ ] Export the current plan's price, credit balance, validity rules, concurrency cap, and refund conditions without copying credentials into the repository.
- [ ] Separate required accepted allocations from total retries, traffic volume, and simultaneous sessions.
- [ ] Obtain dated quotes for both vendors; enter actual unit prices and test both favorable and unfavorable acceptance scenarios.
- [ ] Pilot a small package using the same authorized destinations, request rate, geography and acceptance rules.
- [ ] Confirm SOCKS5 authentication and local port mappings in the existing client; keep application secrets in your normal secret store.
- [ ] Test local negotiation separately from destination reachability; a successful greeting cannot validate exit reputation or useful traffic.
- [ ] Compare invoice cash requirements with consumed-credit economics and include unused prepaid inventory in the purchasing decision.
- [ ] Keep the previous route available until the pilot meets your acceptance threshold; switch only the intended application configuration.

Related repositories in this pack:

- [Clean Residential IP TCO: Pia S5 vs 9Proxy](../pia-s5-vs-9proxy-clean-residential-ip-tco-2026/)
- [Per-GB vs Per-IP Proxy Billing: Break-Even Calculator](../per-gb-vs-per-ip-proxy-billing-breakeven-calculator/)
- [9Proxy Coupon and Bulk SOCKS5 Pricing Breakdown](../9proxy-coupon-code-bulk-socks5-pricing-breakdown/)

**[Continue to 9Proxy plan comparison and purchase options](https://norb.date/p/1)**

The gateway is a commercial action link, not a source for independently measured benchmark results. This repository is an independent comparison and is not endorsed by 9Proxy, Pia S5, or a legacy provider. It does not provide a currently verified coupon code. The default calculator is entirely offline; only an explicitly requested health probe opens a socket.

### MIT License

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
