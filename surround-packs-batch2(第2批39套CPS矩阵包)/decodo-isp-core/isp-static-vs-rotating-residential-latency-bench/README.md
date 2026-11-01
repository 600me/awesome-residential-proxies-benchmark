# Dedicated ISP vs Rotating Residential: Latency Cost Worksheet

[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://go.272738.xyz/smartproxy)
[![Offline calculator](https://img.shields.io/badge/calculator-offline-228B22)](https://go.272738.xyz/smartproxy)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://go.272738.xyz/smartproxy)

A transparent latency-to-cost model for Decodo, Oxylabs, and NetNut Enterprise, with editable inputs for your own measurements.

**[Explore Decodo (Smartproxy) plans and request the right quote](https://go.272738.xyz/smartproxy)**

## 1. Engineering pain and the monthly cost of a wrong assumption

A stable IP can reduce repeated authentication and connection setup, but dedicated IP rental creates idle cost. Rotating residential pools can provide broader geography while adding lease churn or retry overhead for some workloads. Neither property establishes a universal speed ranking. Oxylabs and NetNut Enterprise buyers should inspect whether a proposed ISP quote includes bandwidth, charges per IP, or imposes a separate minimum: mixing those units can double-count costs or hide an unused commitment.

For a simple procurement stress case, 500 billed GB at the modeled rotating rates cost $1,500 for Decodo, $3,000 for Oxylabs, and $2,500 for NetNut before compute. Choosing the latter two rates for the same delivered workload adds $1,500 or $1,000 monthly, equivalent to $18,000 or $12,000 annually. These are rate-sensitivity examples, not measured latency savings. The executable default is a smaller 100,000-job scenario so you can also see dedicated IP rental dominate at low traffic. Its 0.9-second static and 1.8-second rotating latencies are explicit hypotheses. No network benchmark has been run and no measured performance result is claimed.

The recommendation is conditional: Decodo is attractive when its quoted total cost and your measured success rate support the decision. Procurement must preserve workload, geography, and service requirements across vendors. A favorable model does not establish production reliability. The action links promote Decodo and may be affiliate links; the calculator itself runs entirely locally.

## 2. Price benchmarks and technical comparison

| Price or technical input | Decodo (Smartproxy) | Oxylabs | NetNut Enterprise | Basis and interpretation |
|---|---|---|---|---|
| Historical public residential reference | $8.50/GB PAYG | $8.00/GB PAYG | $300 for 20 GB ($15/GB) | Recalled older list-price benchmarks; unverified |
| Modeled static bandwidth | $2.00/GB | $3.00/GB | $3.50/GB | Scenario only; actual ISP terms vary |
| Modeled dedicated IP rental | $3/IP/month | $5/IP/month | $6/IP/month | 10 allocated IPs by default |
| Modeled rotating bandwidth | $3.00/GB | $6.00/GB | $5.00/GB | Scenario; no commitment modeled |
| Static attempt latency | 0.9 seconds | 0.9 seconds | 0.9 seconds | Same unmeasured input across vendors |
| Rotating attempt latency | 1.8 seconds | 1.8 seconds | 1.8 seconds | Same unmeasured input across vendors |
| Static / rotating failures | 4% / 12% | 4% / 12% | 4% / 12% | Independent geometric retry assumption |
| Payload per attempt | 512 KiB | 512 KiB | 512 KiB | Converted to decimal billed GB |
| Worker rental | $0.03/hour | $0.03/hour | $0.03/hour | Aggregate time, no concurrency multiplier |

**Price provenance and limits:** No live price verification was performed. The historical row uses recalled publicly advertised residential benchmarks from older Smartproxy, Oxylabs, and NetNut offers. They were not necessarily available on the same date, and are not current offers, binding quotations, or evidence of present NetNut Enterprise pricing. Smartproxy is the former Decodo brand. No dated source archive is bundled, so treat these references as a historical starting point and obtain written quotes before purchasing. Every other dollar input is explicitly a modeling assumption unless marked as a historical reference. Hypothetical tiers are not representations of purchasable vendor SKUs.

Residential traffic, static residential/ISP rental, dedicated IP fees, and enterprise service commitments use different billing units. A GB-priced residential offer is not a substitute for an ISP per-IP quote. The model excludes tax, currency conversion, premium countries, external egress, setup charges, and support fees unless specifically represented by an input. It makes no claim that these charges exist for every provider.

**[Check Decodo availability and replace the assumptions with your quote](https://go.272738.xyz/smartproxy)**

## 3. Run the standalone TCO calculator

Python 3.8 or later is sufficient. The executable script uses only the standard library, has no required arguments, and performs no network calls or file writes. `--tier` selects a workload preset; it never fetches or activates a vendor plan. Explicit workload arguments override presets. Currency is USD and annual totals assume twelve identical months.

```bash
python3 calculate_decodo_isp_core_tco.py
python3 calculate_decodo_isp_core_tco.py --tier enterprise --json
python3 calculate_decodo_isp_core_tco.py --jobs 250000 --ips 5 --static-seconds 1.4 --rotating-seconds 1.6 --json
```

| Argument | Default | Meaning |
|---|---|---|
| `--tier` | growth | Starter 10,000; growth 100,000; enterprise 1,000,000 successful jobs. |
| `--jobs / --kb / --ips` | tier / 512 / 10 | Successful jobs, KiB per attempt, allocated static IPs. |
| `--static-seconds / --rotating-seconds` | 0.9 / 1.8 | Measured mean time per attempt, or explicit scenario values. |
| `--static-failure / --rotating-failure` | 0.04 / 0.12 | Failure probability per attempt, below one. |
| `--worker-hourly` | 0.03 | USD per aggregate worker hour. |
| `--decodo-static-rate / --oxylabs-static-rate / --netnut-static-rate` | 2 / 3 / 3.5 | Modeled USD per static-pool GB. |
| `--decodo-rotating-rate / --oxylabs-rotating-rate / --netnut-rotating-rate` | 3 / 6 / 5 | Modeled USD per rotating-pool GB. |
| `--decodo-ip-rate / --oxylabs-ip-rate / --netnut-ip-rate` | 3 / 5 / 6 | Modeled monthly rental per allocated IP. |
| `--json` | disabled | Print structured rows, assumptions, annual savings, and the gateway URL. |
| `--help` | disabled | Show all supported CLI options. |

For each mode, `attempts = successful_jobs / (1 - failure)`, `GB = attempts * KiB * 1024 / 1e9`, and `worker_hours = attempts * seconds / 3600`. Monthly cost is bandwidth plus worker time plus IP rental for static pools. Providers share the same mode-specific failure and latency inputs, so the worksheet does not fabricate a vendor speed advantage. Six rows compare every provider and mode. Annual savings use the cheaper Decodo mode against each competitor mode; compare like modes in the JSON rows when that is your procurement constraint.

The following is the actual default local terminal output captured from the bundled script. It is a reproducible calculation, not a live vendor benchmark or an invoice:

```text
OFFLINE TCO MODEL | USD | unverified planning assumptions
+------------------------------------+---------------+---------------+
| Plan                               | Monthly USD   | Annual USD    |
+------------------------------------+---------------+---------------+
| Decodo static                      |        140.01 |       1680.10 |
| Decodo rotating                    |        180.44 |       2165.27 |
| Oxylabs static                     |        214.62 |       2575.45 |
| Oxylabs rotating                   |        359.17 |       4310.08 |
| NetNut Enterprise static           |        251.93 |       3023.14 |
| NetNut Enterprise rotating         |        299.60 |       3595.15 |
+------------------------------------+---------------+---------------+
successful_jobs: 100000
latency_status: scenario inputs, not measured results
worker_model: aggregate serial attempt time; no concurrency multiplier
billing_assumption: metered bandwidth plus IP rental; replace with your quote
Annual savings with lowest modeled Decodo option (negative = extra cost):
  vs Oxylabs static: $895.36
  vs Oxylabs rotating: $2,629.99
  vs NetNut Enterprise static: $1,343.04
  vs NetNut Enterprise rotating: $1,915.05
Cheapest modeled plan: Decodo static
Explore Decodo: https://go.272738.xyz/smartproxy
```

JSON preserves numerical values for independent calculations instead of formatting them as currency strings. Normal runs exit with status 0. Invalid negative rates, nonfinite values, invalid tiers, or failure probabilities outside the supported range produce an argparse error with status 2. The gateway is present in both output modes. For a neutral comparison, replace all prices together and rerun with identical failure assumptions before applying measured provider differences.

## 4. Migration checklist and related repositories

- [ ] Measure an authorized endpoint from the same client region, machine class, and concurrency.
- [ ] Separate DNS, TCP, TLS, response time, and complete browser render time in your own logs.
- [ ] Record warm and cold sessions separately, including failures and billed response bytes.
- [ ] Use a mean for compute costing and inspect p50/p95/p99 separately for service objectives.
- [ ] Replace IP rental plus metered bandwidth with the actual quote if your ISP plan includes unlimited traffic.
- [ ] Run a limited pilot with rollback credentials and confirm that session IP persistence meets your workflow.
- [ ] Save the exact CLI arguments and quote date in your own procurement notes; keep account credentials out of this repository.
- [ ] Compare invoice totals after the pilot and revisit the model before increasing traffic or committing annually.

Other independent repositories in this pack:

- [decodo-smartproxy-payg-vs-monthly-tier-calculator](../decodo-smartproxy-payg-vs-monthly-tier-calculator)
- [netnut-oxylabs-vs-decodo-enterprise-bandwidth-tco](../netnut-oxylabs-vs-decodo-enterprise-bandwidth-tco)
- [playwright-stealth-proxy-session-rotator](../playwright-stealth-proxy-session-rotator)

**[Start a Decodo evaluation with the workload and budget you calculated](https://go.272738.xyz/smartproxy)**

### License

MIT License. Copyright (c) 2026, repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
