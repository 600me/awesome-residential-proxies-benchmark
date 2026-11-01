[![Compare 9Proxy](https://img.shields.io/badge/9Proxy-Compare_Plans-blue)](https://norb.date/p/1)
[![Python 3](https://img.shields.io/badge/Python-3.8%2B-blue)](https://norb.date/p/1)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://norb.date/p/1)

# Per-GB vs Per-IP Proxy Billing: Break-Even Calculator

An independent, offline cost model for **Per-IP Billed Unlimited-Bandwidth Residential SOCKS5**. Pack: `9proxy-per-ip`. Evaluate 9Proxy against **911 S5 Legacy Alternatives & Pia S5** using explicit workload assumptions. No external packages, account, credentials, or network access are needed for the default report.

**[Check 9Proxy package terms and start your comparison](https://norb.date/p/1)**

## 1. Engineering pain and the cost of an incomplete comparison

A data-intensive job can spend more on traffic than on useful IP allocations. At an illustrative $3.50/GB, 1,000 GB costs **$3,500/month**. For 1,000 accepted allocations with no replacement loss, the historical per-IP reference anchors produce **$200/month for 9Proxy** and **$250/month for Pia S5**. Relative to the per-GB reference, the modeled 9Proxy difference is **$3,300/month or $39,600/year**. Against Pia S5 it is only **$50/month or $600/year**. Those are different comparisons and must not be combined into one advertised saving.

The billing trap is estimating a crawler from page counts while forgetting response bodies, retries, assets, and failed transfers. The opposite trap is assuming per-IP pricing always wins: a rotation-heavy workload with very little traffic can favor per-GB billing. With the default $200 IP bill and $3.50/GB reference, the crossover is **57.14 GB/month**. Below that boundary, the traffic bill is lower under the stated assumptions. The script prints negative savings honestly when per-IP costs more.

The original 911 S5 service is a legacy comparison point, not a verified purchasable 2026 plan. "911 S5 alternatives" describes a heterogeneous set of replacement services, not one vendor with one bill. Pia S5 is shown separately. No claim of a specific undisclosed charge, superior IP reputation, guaranteed uptime, or misconduct by either brand is made here. The practical billing traps to investigate are charged replacements, credit validity, minimum purchase sizes, session reuse, concurrent ports, and the actual meaning of unlimited bandwidth.

## 2. Price anchors and technical comparison

**Pricing basis:** the historical public entry-package reference anchors used here are **9Proxy $20 / 100 IP credits ($0.20/IP)** and **Pia S5 $50 / 200 IP credits ($0.25/IP)**. They are remembered list-price benchmarks, not independently verified October 2026 offers. The **$3.50/GB** comparator is an illustrative metered-residential benchmark, not an attributed Pia or 911 quote. No live pages were retrieved. Obtain a dated quote and replace the rates before committing money. Bulk discounts, taxes, currency conversion, and package availability are not verified by this repository.

| Price or technical parameter | 9Proxy reference | Pia S5 reference | 911 S5 legacy alternatives | Interpretation |
| --- | --- | --- | --- | --- |
| Historical entry-package anchor | $20 / 100 IP credits | $50 / 200 IP credits | No common current quote | Historical reference only |
| Unit rate used | $0.20 / charged allocation | $0.25 / charged allocation | User must supply quote | Linear scaling; no invented bulk rate |
| Desired accepted allocations/month | 1,000 | 1,000 | Same target for a valid comparison | Allocations are not guaranteed distinct addresses |
| Assumed acceptance rate | 100% | 100% | Measure in a matched pilot | Scenario input, not provider test data |
| Modeled charged allocations/month | 1,000 | 1,000 | Not calculated without quote | Ceiling of desired / acceptance |
| Modeled operator time/month | 0 hours at $30/hour | 0 hours at $30/hour | Measure actual minutes | Labor is included, not claimed observed |
| Modeled monthly total | $200.00 | $250.00 | Not available | Credit spend plus selected labor |
| Modeled annual total | $2,400.00 | $3,000.00 | Not available | Twelve identical months |
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
python3 calculate_9proxy_per_ip_tco.py --ips 1000 --gb 20 --per-gb-rate 3.50
```

The following is actual default terminal output generated from this repository's script; values are modeled from the disclosed inputs, not captured vendor invoices:

```text
$ python3 calculate_9proxy_per_ip_tco.py
Offline reference model | bandwidth | tier=growth
Accepted IP allocations/month: 1,000 | Traffic: 1,000.00 GB
+-------------------+----------+---------------+---------------+
| Provider          | Credits  | Monthly USD   | Annual USD    |
+-------------------+----------+---------------+---------------+
| 9Proxy            |     1000 |        200.00 |      2,400.00 |
| Pia S5            |     1000 |        250.00 |      3,000.00 |
| Per-GB reference  |      n/a |      3,500.00 |     42,000.00 |
+-------------------+----------+---------------+---------------+
Annual savings vs Pia S5: $600.00
Annual savings vs per-GB: $39,600.00
Per-GB break-even: 57.14 GB/month
Reference prices; replace with your quote. Negative savings = higher cost.
Compare plans: https://norb.date/p/1
```

| CLI option | Default | Meaning |
| --- | --- | --- |
| `--tier starter\|growth\|scale` | `growth` | Scale base IP allocations and GB by 0.2, 1, or 5; rates and labor hours stay fixed |
| `--json` | Off | Emit one JSON object including assumptions, bills, annual savings and gateway |
| `--ips N` | 1,000 in growth | Accepted charged-allocation demand per month; whole number including zero |
| `--gb N` | 1,000 in growth | Total monthly GB for the metered reference, including any billable retries |
| `--rate-9 N` / `--rate-pia N` | 0.20 / 0.25 | Replace historical per-credit USD reference prices with your quotes |
| `--clean-rate-9 F` / `--clean-rate-pia F` | 1.0 / 1.0 | Accepted fraction in (0, 1]; workload-specific acceptance, not a quality guarantee |
| `--per-gb-rate N` | 3.50 | Reference USD/GB; zero yields an undefined break-even |
| `--coupon-percent N` | 0 | Assumed recurring percentage off 9Proxy credit spend only, from 0 to 100 |
| `--hours-9 N` / `--hours-pia N` | 0 / 0 | Fixed monthly operator hours; no automatic tier scaling |
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

The boundary uses the selected 9Proxy monthly total divided by the reference GB rate. The reference GB row assumes the same task can be completed with equal outcomes and zero additional labor; it has no minimum commitment or included-traffic allowance. Add those costs externally or adjust your quote before making a purchasing decision. If concurrency or connection limits prevent completion, a lower theoretical bill is not an acceptable substitute for a working service.

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
- [9Proxy Coupon and Bulk SOCKS5 Pricing Breakdown](../9proxy-coupon-code-bulk-socks5-pricing-breakdown/)
- [Local SOCKS5 Port Forwarding Health Checks and TCO](../local-port-forwarding-socks5-health-check-daemon/)

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
