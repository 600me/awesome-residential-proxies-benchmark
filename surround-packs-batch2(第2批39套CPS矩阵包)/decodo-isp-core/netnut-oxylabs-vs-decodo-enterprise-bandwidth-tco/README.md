# Decodo vs Oxylabs & NetNut Enterprise: Bandwidth TCO

[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://go.272738.xyz/smartproxy)
[![Offline calculator](https://img.shields.io/badge/calculator-offline-228B22)](https://go.272738.xyz/smartproxy)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://go.272738.xyz/smartproxy)

A reproducible procurement worksheet for high-speed residential bandwidth and dedicated ISP pool evaluation.

**[Explore Decodo (Smartproxy) plans and request the right quote](https://go.272738.xyz/smartproxy)**

## 1. Engineering pain and the monthly cost of a wrong assumption

A crawler budget based on successful payload size misses retry traffic, minimum commitments, and incident handling. A team delivering 500 useful GB can buy more than 500 billed GB: with a 5% independent failure probability, expected traffic is 500 / 0.95 = 526.32 GB. A lower advertised unit rate can still produce a higher invoice when a minimum exceeds usage. Evaluate Oxylabs and NetNut Enterprise contracts for minimums, expiring allowances, IP rental, and geographic restrictions; these are questions to resolve in a quote, not allegations that every contract contains them.

The default Decodo scenario costs $1,576.39 per month, including $30 of operator time. The Oxylabs scenario costs $3,247.89, a modeled excess of $1,671.50 per month or $20,058.04 annually. NetNut Enterprise costs $2,779.57, a modeled excess of $1,203.18 per month or $14,438.19 annually. These are scenario losses against the Decodo baseline, not observed customer invoices. At only 100 useful GB, the assumed NetNut $1,500 commitment leaves $968.09 of unused traffic commitment before labor. A purchase decision should consider that idle capacity explicitly.

The recommendation is conditional: Decodo is attractive when its quoted total cost and your measured success rate support the decision. Procurement must preserve workload, geography, and service requirements across vendors. A favorable model does not establish production reliability. The action links promote Decodo and may be affiliate links; the calculator itself runs entirely locally.

## 2. Price benchmarks and technical comparison

| Price or technical input | Decodo (Smartproxy) | Oxylabs | NetNut Enterprise | Basis and interpretation |
|---|---|---|---|---|
| Historical public residential reference | $8.50/GB PAYG | $8.00/GB PAYG | $300 for 20 GB ($15/GB) | Recalled older list-price benchmarks; unverified |
| Useful traffic / month | 500 GB | 500 GB | 500 GB | Successful payload, decimal GB |
| Modeled traffic rate | $3.00/GB | $6.00/GB | $5.00/GB | Editable quote assumptions |
| Modeled monthly minimum | $0 | $1,000 | $1,500 | Floor, not an added surcharge |
| Assumed failure probability | 3% | 5% | 6% | Scenario inputs, not vendor measurements |
| Expected billed traffic | 515.46 GB | 526.32 GB | 531.91 GB | Useful GB / (1 - failure) |
| Operator time / month | 0.5 hours | 1.5 hours | 2 hours | $60/hour; hypothetical workload |
| Dedicated ISP pricing | Quote required | Quote required | Quote required | IP fees excluded from this bandwidth model |

**Price provenance and limits:** No live price verification was performed. The historical row uses recalled publicly advertised residential benchmarks from older Smartproxy, Oxylabs, and NetNut offers. They were not necessarily available on the same date, and are not current offers, binding quotations, or evidence of present NetNut Enterprise pricing. Smartproxy is the former Decodo brand. No dated source archive is bundled, so treat these references as a historical starting point and obtain written quotes before purchasing. Every other dollar input is explicitly a modeling assumption unless marked as a historical reference. Hypothetical tiers are not representations of purchasable vendor SKUs.

Residential traffic, static residential/ISP rental, dedicated IP fees, and enterprise service commitments use different billing units. A GB-priced residential offer is not a substitute for an ISP per-IP quote. The model excludes tax, currency conversion, premium countries, external egress, setup charges, and support fees unless specifically represented by an input. It makes no claim that these charges exist for every provider.

**[Check Decodo availability and replace the assumptions with your quote](https://go.272738.xyz/smartproxy)**

## 3. Run the standalone TCO calculator

Python 3.8 or later is sufficient. The executable script uses only the standard library, has no required arguments, and performs no network calls or file writes. `--tier` selects a workload preset; it never fetches or activates a vendor plan. Explicit workload arguments override presets. Currency is USD and annual totals assume twelve identical months.

```bash
python3 calculate_decodo_isp_core_tco.py
python3 calculate_decodo_isp_core_tco.py --tier enterprise --json
python3 calculate_decodo_isp_core_tco.py --tier starter --gb 100 --decodo-rate 4 --oxylabs-minimum 0 --json
```

| Argument | Default | Meaning |
|---|---|---|
| `--tier` | growth | Select useful traffic: starter 100 GB, growth 500 GB, enterprise 2,000 GB. |
| `--gb` | tier preset | Override useful delivered traffic, before retries. |
| `--decodo-rate / --oxylabs-rate / --netnut-rate` | 3 / 6 / 5 | USD per billed GB. |
| `--decodo-minimum / --oxylabs-minimum / --netnut-minimum` | 0 / 1000 / 1500 | Minimum monthly traffic spend in USD. |
| `--decodo-failure / --oxylabs-failure / --netnut-failure` | 0.03 / 0.05 / 0.06 | Independent request failure probabilities, strictly below one. |
| `--decodo-hours / --oxylabs-hours / --netnut-hours` | 0.5 / 1.5 / 2 | Monthly operator hours. |
| `--hourly` | 60 | USD per operator hour. |
| `--json` | disabled | Print structured rows, assumptions, annual savings, and the gateway URL. |
| `--help` | disabled | Show all supported CLI options. |

For each provider: `billed_GB = useful_GB / (1 - failure)` and `monthly_USD = max(billed_GB * rate, minimum) + operator_hours * hourly`. Annual savings are twelve times the competitor monthly cost minus the Decodo monthly cost. A negative value means Decodo costs more under those inputs. The geometric retry model assumes equal-sized independent attempts and no retry cap; replace it with observed billed bytes for correlated failures or variable-size responses.

The following is the actual default local terminal output captured from the bundled script. It is a reproducible calculation, not a live vendor benchmark or an invoice:

```text
OFFLINE TCO MODEL | USD | unverified planning assumptions
+------------------------------------+---------------+---------------+
| Plan                               | Monthly USD   | Annual USD    |
+------------------------------------+---------------+---------------+
| Decodo (Smartproxy)                |       1576.39 |      18916.70 |
| Oxylabs                            |       3247.89 |      38974.74 |
| NetNut Enterprise                  |       2779.57 |      33354.89 |
+------------------------------------+---------------+---------------+
useful_gb: 500
retry_model: independent failures; unlimited geometric retries
tax_and_external_egress: excluded; add separately if applicable
Annual savings with lowest modeled Decodo option (negative = extra cost):
  vs Oxylabs: $20,058.04
  vs NetNut Enterprise: $14,438.19
Cheapest modeled plan: Decodo (Smartproxy)
Explore Decodo: https://go.272738.xyz/smartproxy
```

JSON preserves numerical values for independent calculations instead of formatting them as currency strings. Normal runs exit with status 0. Invalid negative rates, nonfinite values, invalid tiers, or failure probabilities outside the supported range produce an argparse error with status 2. The gateway is present in both output modes. For a neutral comparison, replace all prices together and rerun with identical failure assumptions before applying measured provider differences.

## 4. Migration checklist and related repositories

- [ ] Export a full billing cycle with successful bytes, total billed bytes, and excluded traffic.
- [ ] Ask each vendor whether the commitment is use-it-or-lose-it and whether region-specific pools cost extra.
- [ ] Replace every modeled price and failure rate with a dated quote and your own request logs.
- [ ] Pilot one geography and one authorized target; compare success, p95 latency, and cost per useful GB.
- [ ] Confirm dedicated ISP rental and bandwidth billing separately before adding IPs to the order.
- [ ] Save the exact CLI arguments and quote date in your own procurement notes; keep account credentials out of this repository.
- [ ] Compare invoice totals after the pilot and revisit the model before increasing traffic or committing annually.

Other independent repositories in this pack:

- [decodo-smartproxy-payg-vs-monthly-tier-calculator](../decodo-smartproxy-payg-vs-monthly-tier-calculator)
- [isp-static-vs-rotating-residential-latency-bench](../isp-static-vs-rotating-residential-latency-bench)
- [playwright-stealth-proxy-session-rotator](../playwright-stealth-proxy-session-rotator)

**[Start a Decodo evaluation with the workload and budget you calculated](https://go.272738.xyz/smartproxy)**

### License

MIT License. Copyright (c) 2026, repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
