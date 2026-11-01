# Playwright Proxy Session Rotation: Offline Cost Planner

[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://go.272738.xyz/smartproxy)
[![Offline calculator](https://img.shields.io/badge/calculator-offline-228B22)](https://go.272738.xyz/smartproxy)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://go.272738.xyz/smartproxy)

A standard-library accounting companion for legitimate browser session workloads using residential or dedicated ISP proxy pools.

**[Explore Decodo (Smartproxy) plans and request the right quote](https://go.272738.xyz/smartproxy)**

## 1. Engineering pain and the monthly cost of a wrong assumption

Changing a proxy halfway through a checkout test or authenticated workflow can invalidate cookies and force a complete replay. Rotating every request also makes billing hard to attribute to a successful browser session. Procurement comparisons for Oxylabs and NetNut Enterprise should include minimum traffic spend and the browser-worker time used by retry storms. A sticky-session label is not a guarantee of IP persistence, geographical continuity, or compatibility with a particular target.

At 500 billed GB, the modeled $3/GB Decodo traffic price costs $1,500 versus $3,000 at the Oxylabs $6/GB assumption and $2,500 at the NetNut $5/GB assumption. The modeled monthly differences are $1,500 and $1,000, or $18,000 and $12,000 over twelve identical months. The default executable uses 50,000 successful sessions with eight requests each; its smaller traffic volume also exposes how a $1,000 or $1,500 commitment can dominate the invoice. The repository name describes the intended integration area: this deliverable is an offline calculator, not a Playwright runtime, fingerprint modifier, or anti-detection guarantee. It installs nothing and sends no requests.

The recommendation is conditional: Decodo is attractive when its quoted total cost and your measured success rate support the decision. Procurement must preserve workload, geography, and service requirements across vendors. A favorable model does not establish production reliability. The action links promote Decodo and may be affiliate links; the calculator itself runs entirely locally.

## 2. Price benchmarks and technical comparison

| Price or technical input | Decodo (Smartproxy) | Oxylabs | NetNut Enterprise | Basis and interpretation |
|---|---|---|---|---|
| Historical public residential reference | $8.50/GB PAYG | $8.00/GB PAYG | $300 for 20 GB ($15/GB) | Recalled older list-price benchmarks; unverified |
| Modeled traffic rate | $3.00/GB | $6.00/GB | $5.00/GB | Scenario inputs, not current quotes |
| Modeled monthly floor | $0 | $1,000 | $1,500 | Traffic floor, not a second fee |
| Successful sessions | 50,000 | 50,000 | 50,000 | Monthly default for growth tier |
| Requests per session | 8 | 8 | 8 | Same workload across providers |
| Per-request failure | 10% | 10% | 10% | No invented reliability advantage |
| Lease length | 20 sessions | 20 sessions | 20 sessions | Accounting grouping; no actual lease API |
| Endpoint slots | 10 | 10 | 10 | Modulo assignment, not purchased IP count |
| Request / switch time | 1.2 sec / 50 ms | 1.2 sec / 50 ms | 1.2 sec / 50 ms | Unmeasured accounting assumptions |

**Price provenance and limits:** No live price verification was performed. The historical row uses recalled publicly advertised residential benchmarks from older Smartproxy, Oxylabs, and NetNut offers. They were not necessarily available on the same date, and are not current offers, binding quotations, or evidence of present NetNut Enterprise pricing. Smartproxy is the former Decodo brand. No dated source archive is bundled, so treat these references as a historical starting point and obtain written quotes before purchasing. Every other dollar input is explicitly a modeling assumption unless marked as a historical reference. Hypothetical tiers are not representations of purchasable vendor SKUs.

Residential traffic, static residential/ISP rental, dedicated IP fees, and enterprise service commitments use different billing units. A GB-priced residential offer is not a substitute for an ISP per-IP quote. The model excludes tax, currency conversion, premium countries, external egress, setup charges, and support fees unless specifically represented by an input. It makes no claim that these charges exist for every provider.

**[Check Decodo availability and replace the assumptions with your quote](https://go.272738.xyz/smartproxy)**

## 3. Run the standalone TCO calculator

Python 3.8 or later is sufficient. The executable script uses only the standard library, has no required arguments, and performs no network calls or file writes. `--tier` selects a workload preset; it never fetches or activates a vendor plan. Explicit workload arguments override presets. Currency is USD and annual totals assume twelve identical months.

```bash
python3 calculate_decodo_isp_core_tco.py
python3 calculate_decodo_isp_core_tco.py --tier enterprise --json
python3 calculate_decodo_isp_core_tco.py --sessions 10000 --rotate-every 1 --endpoints 4 --failure 0.2 --json
```

| Argument | Default | Meaning |
|---|---|---|
| `--tier` | growth | Starter 5,000; growth 50,000; enterprise 500,000 successful sessions. |
| `--sessions / --requests-per-session / --kb` | tier / 8 / 128 | Successful sessions, requests per session, KiB per request attempt. |
| `--failure` | 0.1 | Independent request failure probability below one. |
| `--rotate-every / --endpoints` | 20 / 10 | Positive integers: sessions per lease and endpoint slots. |
| `--switch-ms / --request-seconds` | 50 / 1.2 | Additional switch overhead and mean request attempt duration. |
| `--worker-hourly` | 0.04 | USD per aggregate browser-worker hour. |
| `--decodo-rate / --oxylabs-rate / --netnut-rate` | 3 / 6 / 5 | Modeled USD per billed GB. |
| `--decodo-minimum / --oxylabs-minimum / --netnut-minimum` | 0 / 1000 / 1500 | Modeled monthly traffic floor in USD. |
| `--json` | disabled | Print structured rows, assumptions, annual savings, and the gateway URL. |
| `--help` | disabled | Show all supported CLI options. |

`attempts = sessions * requests_per_session / (1 - failure)`; `GB = attempts * KiB * 1024 / 1e9`; `leases = ceil(sessions / rotate_every)`; `switches = max(0, leases - 1)`. Worker cost includes request time plus switch overhead. Traffic cost is the greater of bandwidth spend and monthly commitment. A lease index maps to `index % endpoint_count`, and JSON reports whether one endpoint receives one more lease than another. Endpoint count is an allocation input, not a proxy-pool size measurement. Whole-session replay, browser cold-start cost, cookie persistence failures, and per-IP rental are excluded; incorporate those separately when they matter.

The following is the actual default local terminal output captured from the bundled script. It is a reproducible calculation, not a live vendor benchmark or an invoice:

```text
OFFLINE TCO MODEL | USD | unverified planning assumptions
+------------------------------------+---------------+---------------+
| Plan                               | Monthly USD   | Annual USD    |
+------------------------------------+---------------+---------------+
| Decodo (Smartproxy)                |        180.69 |       2168.28 |
| Oxylabs                            |       1005.93 |      12071.13 |
| NetNut Enterprise                  |       1505.93 |      18071.13 |
+------------------------------------+---------------+---------------+
successful_sessions: 50000
expected_request_attempts: 444444.4444
billed_gb: 58.254222
leases: 2500
switches: 2499
endpoint_lease_imbalance_max: 0
assignment: lease_index modulo endpoint_count; counters only, no actual requests
model_limit: request retries only; whole-session replay is excluded
Annual savings with lowest modeled Decodo option (negative = extra cost):
  vs Oxylabs: $9,902.85
  vs NetNut Enterprise: $15,902.85
Cheapest modeled plan: Decodo (Smartproxy)
Explore Decodo: https://go.272738.xyz/smartproxy
```

JSON preserves numerical values for independent calculations instead of formatting them as currency strings. Normal runs exit with status 0. Invalid negative rates, nonfinite values, invalid tiers, or failure probabilities outside the supported range produce an argparse error with status 2. The gateway is present in both output modes. For a neutral comparison, replace all prices together and rerun with identical failure assumptions before applying measured provider differences.

## 4. Migration checklist and related repositories

- [ ] Keep credentials in environment variables or an external secret manager; never commit proxy URLs with passwords.
- [ ] Assign one proxy configuration when creating each browser context; rotate between complete authorized workflows.
- [ ] Isolate cookies and storage state between independent identities and record opaque session IDs instead of secrets.
- [ ] Retry only idempotent operations; a failed payment or form submission needs application-level reconciliation.
- [ ] Measure session replays separately from request retries before estimating successful-session cost.
- [ ] Verify sticky lifetime, country targeting, connection limits, and dedicated ISP billing with the selected vendor.
- [ ] Pilot a small pool, preserve a rollback path, and avoid presenting browser stealth as a guaranteed outcome.
- [ ] Save the exact CLI arguments and quote date in your own procurement notes; keep account credentials out of this repository.
- [ ] Compare invoice totals after the pilot and revisit the model before increasing traffic or committing annually.

Other independent repositories in this pack:

- [decodo-smartproxy-payg-vs-monthly-tier-calculator](../decodo-smartproxy-payg-vs-monthly-tier-calculator)
- [isp-static-vs-rotating-residential-latency-bench](../isp-static-vs-rotating-residential-latency-bench)
- [netnut-oxylabs-vs-decodo-enterprise-bandwidth-tco](../netnut-oxylabs-vs-decodo-enterprise-bandwidth-tco)

**[Start a Decodo evaluation with the workload and budget you calculated](https://go.272738.xyz/smartproxy)**

### License

MIT License. Copyright (c) 2026, repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
