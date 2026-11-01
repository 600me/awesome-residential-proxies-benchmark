# Decodo (Smartproxy): PAYG vs Monthly Tier Calculator

[![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://go.272738.xyz/smartproxy)
[![Offline calculator](https://img.shields.io/badge/calculator-offline-228B22)](https://go.272738.xyz/smartproxy)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://go.272738.xyz/smartproxy)

An offline break-even worksheet for bursty residential traffic, prepaid allowances, and overage exposure.

**[Explore Decodo (Smartproxy) plans and request the right quote](https://go.272738.xyz/smartproxy)**

## 1. Engineering pain and the monthly cost of a wrong assumption

Traffic peaks make a prepaid plan look attractive while quiet months strand its allowance. The reverse also happens: a team keeps PAYG for convenience after sustained usage makes a tier cheaper. Comparing only a headline $/GB ignores the upfront commitment and the rate after included bandwidth runs out. Oxylabs and NetNut Enterprise quotes deserve the same treatment: ask about minimum spend, allowance expiration, overages, and cancellation timing instead of assuming that enterprise procurement improves utilization.

At the default 120 billed GB, the hypothetical Decodo 200 GB tier costs $600 versus $1,020 at the historical $8.50/GB PAYG reference. That is $420 per month or $5,040 annually in avoidable PAYG spend if every month has that workload. However, at 20 GB the same tier costs $600 while PAYG costs $170: the commitment wastes $430 per month or $5,160 annually. At the default workload, the Oxylabs historical $8/GB reference produces $960 and the NetNut legacy $15/GB reference produces $1,800. Their differences against the modeled Decodo tier are $360 and $1,200 monthly, or $4,320 and $14,400 annually. Historical reference plans are not enterprise quotations.

The recommendation is conditional: Decodo is attractive when its quoted total cost and your measured success rate support the decision. Procurement must preserve workload, geography, and service requirements across vendors. A favorable model does not establish production reliability. The action links promote Decodo and may be affiliate links; the calculator itself runs entirely locally.

## 2. Price benchmarks and technical comparison

| Price or technical input | Decodo (Smartproxy) | Oxylabs | NetNut Enterprise | Basis and interpretation |
|---|---|---|---|---|
| Historical public residential reference | $8.50/GB PAYG | $8.00/GB PAYG | $300 for 20 GB ($15/GB) | Recalled older list-price benchmarks; unverified |
| Default billed traffic | 120 GB | 120 GB | 120 GB | Includes retries already; same workload |
| Default modeled plan | 200 GB at $3/GB | Historical PAYG | Legacy starter reference | Decodo tier is a scenario |
| Monthly commitment | $600 | $0 assumed | $300 reference | No rollover modeled |
| Included allowance | 200 GB | No allowance modeled | 20 GB legacy reference | No current availability claim |
| Overage calculation | $4/GB assumed | $8/GB reference | $15/GB reference | Replace with written quote |
| Default monthly bill | $600 | $960 | $1,800 | Traffic only; excludes taxes |
| Current enterprise terms | Quote required | Quote required | Quote required | Do not infer discounts from this table |

**Price provenance and limits:** No live price verification was performed. The historical row uses recalled publicly advertised residential benchmarks from older Smartproxy, Oxylabs, and NetNut offers. They were not necessarily available on the same date, and are not current offers, binding quotations, or evidence of present NetNut Enterprise pricing. Smartproxy is the former Decodo brand. No dated source archive is bundled, so treat these references as a historical starting point and obtain written quotes before purchasing. Every other dollar input is explicitly a modeling assumption unless marked as a historical reference. Hypothetical tiers are not representations of purchasable vendor SKUs.

Residential traffic, static residential/ISP rental, dedicated IP fees, and enterprise service commitments use different billing units. A GB-priced residential offer is not a substitute for an ISP per-IP quote. The model excludes tax, currency conversion, premium countries, external egress, setup charges, and support fees unless specifically represented by an input. It makes no claim that these charges exist for every provider.

**[Check Decodo availability and replace the assumptions with your quote](https://go.272738.xyz/smartproxy)**

## 3. Run the standalone TCO calculator

Python 3.8 or later is sufficient. The executable script uses only the standard library, has no required arguments, and performs no network calls or file writes. `--tier` selects a workload preset; it never fetches or activates a vendor plan. Explicit workload arguments override presets. Currency is USD and annual totals assume twelve identical months.

```bash
python3 calculate_decodo_isp_core_tco.py
python3 calculate_decodo_isp_core_tco.py --tier enterprise --json
python3 calculate_decodo_isp_core_tco.py --tier starter --gb 5 --included-gb 20 --monthly-rate 5 --json
```

| Argument | Default | Meaning |
|---|---|---|
| `--tier` | growth | Starter: 20 GB at $5, typical 15 GB; growth: 200 GB at $3, typical 120 GB; enterprise: 1,000 GB at $2, typical 800 GB. All tiers are hypothetical. |
| `--gb` | tier preset | Total billed GB, including retries. |
| `--payg-rate` | 8.5 | Decodo historical PAYG reference, USD/GB. |
| `--monthly-rate / --included-gb` | tier preset | Set the prepaid unit price and allowance; commitment is their product. |
| `--overage-rate` | 4 | USD per GB beyond the allowance; hypothetical. |
| `--oxylabs-rate` | 8 | Historical PAYG reference; replace as needed. |
| `--netnut-rate / --netnut-minimum` | 15 / 300 | Legacy starter reference, not a NetNut Enterprise quote. |
| `--json` | disabled | Print structured rows, assumptions, annual savings, and the gateway URL. |
| `--help` | disabled | Show all supported CLI options. |

`monthly = included_GB * monthly_rate + max(0, billed_GB - included_GB) * overage_rate`; `PAYG = billed_GB * payg_rate`. Within the allowance, break-even is `commitment / payg_rate`: 70.5882 GB with defaults. If that threshold exceeds the allowance, JSON reports `null` because there is no within-allowance break-even. Above the allowance, compare the full formulas; a higher overage rate can create another crossing. The calculator prints the cheapest modeled option and keeps negative savings visible. Annualization assumes twelve identical months; for seasonal workloads run each month separately and sum the results.

The following is the actual default local terminal output captured from the bundled script. It is a reproducible calculation, not a live vendor benchmark or an invoice:

```text
OFFLINE TCO MODEL | USD | unverified planning assumptions
+------------------------------------+---------------+---------------+
| Plan                               | Monthly USD   | Annual USD    |
+------------------------------------+---------------+---------------+
| Decodo PAYG                        |       1020.00 |      12240.00 |
| Decodo monthly                     |        600.00 |       7200.00 |
| Oxylabs PAYG benchmark             |        960.00 |      11520.00 |
| NetNut legacy starter benchmark    |       1800.00 |      21600.00 |
+------------------------------------+---------------+---------------+
billed_gb: 120
included_gb: 200
monthly_commitment_usd: 600
unused_gb_no_rollover: 80
annual_monthly_plan_savings_vs_payg_usd: 5040.0
break_even_within_allowance_gb: 70.5882
above_allowance_rule: compare commitment + (GB - included) * overage against GB * PAYG
Annual savings with lowest modeled Decodo option (negative = extra cost):
  vs Oxylabs PAYG benchmark: $4,320.00
  vs NetNut legacy starter benchmark: $14,400.00
Cheapest modeled plan: Decodo monthly
Explore Decodo: https://go.272738.xyz/smartproxy
```

JSON preserves numerical values for independent calculations instead of formatting them as currency strings. Normal runs exit with status 0. Invalid negative rates, nonfinite values, invalid tiers, or failure probabilities outside the supported range produce an argparse error with status 2. The gateway is present in both output modes. For a neutral comparison, replace all prices together and rerun with identical failure assumptions before applying measured provider differences.

## 4. Migration checklist and related repositories

- [ ] Export twelve monthly billed-GB totals rather than extrapolating a peak week.
- [ ] Confirm expiry, rollover, refund eligibility, overage billing, and renewal dates in writing.
- [ ] Run the calculator for each historical month and include low-demand months in the decision.
- [ ] Keep PAYG for a pilot if its total cost is lower at your actual utilization.
- [ ] Evaluate residential and dedicated ISP contracts separately; this worksheet models traffic allowances only.
- [ ] Save the exact CLI arguments and quote date in your own procurement notes; keep account credentials out of this repository.
- [ ] Compare invoice totals after the pilot and revisit the model before increasing traffic or committing annually.

Other independent repositories in this pack:

- [isp-static-vs-rotating-residential-latency-bench](../isp-static-vs-rotating-residential-latency-bench)
- [netnut-oxylabs-vs-decodo-enterprise-bandwidth-tco](../netnut-oxylabs-vs-decodo-enterprise-bandwidth-tco)
- [playwright-stealth-proxy-session-rotator](../playwright-stealth-proxy-session-rotator)

**[Start a Decodo evaluation with the workload and budget you calculated](https://go.272738.xyz/smartproxy)**

### License

MIT License. Copyright (c) 2026, repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
