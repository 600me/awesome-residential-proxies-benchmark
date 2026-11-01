[![BWH gateway](https://img.shields.io/badge/BWH-compare_plans-blue)](https://coding.mybskm.top/go/bwh)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-green)](https://coding.mybskm.top/go/bwh)
[![License MIT](https://img.shields.io/badge/license-MIT-lightgrey)](https://coding.mybskm.top/go/bwh)

# PacificRack and CloudCone vs BWH: Packet-Loss Audit Economics

Pack: `bwh-cn2gia`. An open-source, offline comparison workbook for CN2 GIA enterprise low-latency developer VPS decisions.

**[Compare BandwagonHost plans and confirm your quote](https://coding.mybskm.top/go/bwh)**

## 1. Engineering pain and the bill behind the sticker price

A cheap runner is expensive when builds fail after downloading most dependencies, operators rerun deployments, and every investigation blames a different hop. Intermediate-hop ICMP loss is not proof that application packets are lost. Routers can rate-limit diagnostic traffic while forwarding payload normally. The useful audit correlates endpoint loss, TCP retransmissions, completed jobs and queue delay.

CloudCone and PacificRack should be evaluated on the exact server and route rather than an assumed common upstream. DMIT premium networking also needs application evidence. The hidden project bill can be failed-job handling, wasted runner minutes and manual reruns; these are internal workload costs, not documented vendor surcharges. PacificRack is included in the audit procedure but excluded from the priced model because this offline repository has no reliable remembered comparable quote.

Concrete scenario: 10,000 monthly logical jobs with four-minute attempts require approximately 20.04 extra attempts at a 0.2% whole-job failure rate, versus 309.28 at 3%. At $0.20 per worker-hour, their extra compute bills are about $0.27 and $4.12. The larger risk is response labor: two engineer hours per percentage point of failure at $75/hour yields $30 versus $450/month, a $420/month or $5,040/year labor difference. At a hypothetical 12% failure rate that response rule alone costs $1,800/month or $21,600/year. None of these rates is a measured result for any brand.

Read the savings as a conditional budget estimate. A negative saving means BWH costs more under the supplied inputs. Keep competitors in consideration when their measured service fits your workload. No synthetic number in this repository is represented as an independent network benchmark.

## 2. Historical prices and technical comparison

| Provider / historical reference | USD per billing unit | Annual hosting equivalent | Memory reference | Network / comparison limit |
| --- | ---: | ---: | --- | --- |
| BandwagonHost (BWH), CN2 GIA ECOMMERCE entry | $169.99/year | $169.99 | 2 GB | Premium China route family; verify exact DC and direction |
| BandwagonHost (BWH), entry quarterly reference | $49.99/quarter | $199.96 | 2 GB | Same resource target; quarterly commitment differs |
| BandwagonHost (BWH), larger reference | $299.99/year | $299.99 | 4 GB | Capacity upgrade; not the calculator default |
| BandwagonHost (BWH), larger reference | $549.99/year | $549.99 | 8 GB | Capacity upgrade; not the calculator default |
| DMIT, LAX Pro TINY reference | $9.99/month | $119.88 | 2 GB | Premium route family; exact retail terms control |
| DMIT, LAX Pro GIG reference | $79.90/month | $958.80 | 8 GB | Larger capacity; not the calculator default |
| CloudCone, basic compute reference | $3.50/month | $42.00 | 1 GB | Budget transit; no CN2 GIA guarantee assumed |

These are remembered historical public-price benchmarks, compiled offline, not verified 2026 checkout quotes or guaranteed inventory. Prices, product names and configurations can change. The 2026 label identifies this evaluation edition, not a claim of fresh testing. Confirm the exact offer before spending. No tax, currency conversion, paid backup, extra IPv4, transfer overage or support add-on is included. Those items depend on the actual order and must be added consistently to all quotes.

The calculator uses the entry references: BWH $169.99/year, DMIT $9.99/month and CloudCone $42/year annualized from $3.50/month. CloudCone's listed entry has less memory; this is an entry-budget comparison, not an equal-resource performance test. If the application needs 2 GB or more, replace the CloudCone price with a suitable quote before drawing a procurement conclusion. Likewise, storage size, vCPU count, transfer allowance, port rate and fair-use restrictions must be matched from the chosen order. They are not silently inferred from brand or price.

At three nodes, annual hosting alone is $509.97 for BWH, $359.64 for DMIT and $126.00 for CloudCone. BWH therefore needs to recover a $150.33/year premium over DMIT or $383.97/year over CloudCone through a benefit your team can actually observe. Higher bandwidth port rates do not guarantee lower RTT, and an advertised route does not guarantee loss-free service.

**[Check BWH product, location and renewal terms](https://coding.mybskm.top/go/bwh)**

## 3. Reproducible TCO calculator

`calculate_bwh_cn2gia_tco.py` is an executable Python 3 standard-library script. It makes no network requests, installs no packages and writes no output files. Run from this directory:

```sh
python3 calculate_bwh_cn2gia_tco.py
python3 calculate_bwh_cn2gia_tco.py --tier small --json
python3 calculate_bwh_cn2gia_tco.py --tier enterprise --infrastructure-only
python3 calculate_bwh_cn2gia_tco.py --tier small --jobs 20000 --worker-hourly 0 --cloudcone-failure-percent 0.2
python3 calculate_bwh_cn2gia_tco.py --help
```

| Argument | Default | Meaning |
| --- | --- | --- |
| --tier | team | small=1, team=3, enterprise=10 nodes; scales hosting only. |
| --json | off | Emit one valid JSON document, including gateway and assumptions. |
| --hourly | 75 | USD per engineering hour. |
| --bwh-annual | 169.99 | Annual hosting USD per BWH node. |
| --dmit-monthly | 9.99 | Monthly hosting USD per DMIT node. |
| --cloudcone-annual | 42 | Annualized hosting USD per CloudCone node. |
| --infrastructure-only | off | Exclude modeled labor, impact and migration costs. |
| --jobs / --job-minutes | 10000 / 4 | Monthly logical jobs across the fleet and full attempt duration. |
| --worker-hourly | 0.20 | USD per incremental worker-hour; use zero for included idle capacity. |
| --incident-hours | 2 | Monthly engineering hours per percentage point of failed attempts. |
| --bwh-failure-percent / --dmit-failure-percent / --cloudcone-failure-percent | 0.2 / 0.2 / 3 | Whole-job failure percentages; each must be less than 100. |

Numeric inputs must be finite and nonnegative. Invalid tiers and out-of-range bounded inputs fail with an argparse error. Help lists the complete accepted arguments. The default tier is three hosting nodes, while developer activity, incident hours and operational labor remain fleet-wide. Do not treat tier names as vendor SKU names or redundancy guarantees.

Independent attempts with constant failure probability `p` require `jobs * p / (1-p)` expected extra attempts. Multiply by attempt minutes divided by sixty and worker price to obtain wasted runner cost. Add `failure_percent * incident_hours * hourly` as an explicit operational response assumption. The percentage argument uses percentage points: 3 means 3%, not 0.03%.

Packet loss is not interchangeable with job failure probability. TCP recovery, retries inside clients, partial resume and burst correlation all change the mapping. The default model assumes failed attempts consume the full attempt duration and retry until successful; caps, cancellation and correlated outages require a different model. Use completed-job telemetry to estimate the input. Avoid billing the same worker capacity twice if it is already included in the VPS invoice: set worker price to zero when there is no incremental runner charge.

Actual local stdout from the default command, generated while preparing this README:

```text
Packet-loss audit: job retry TCO | tier=team | nodes=3
USD; historical price references + illustrative assumptions (not measurements)
+----------------------+------------+------------+------------+-------------+
| Provider             | Infra/mo   | Model/mo   | TCO/mo     | TCO/year    |
+----------------------+------------+------------+------------+-------------+
| BandwagonHost (BWH)  |      42.50 |      30.27 |      72.76 |      873.18 |
| DMIT                 |      29.97 |      30.27 |      60.24 |      722.85 |
| CloudCone            |      10.50 |     454.12 |     464.62 |     5575.48 |
+----------------------+------------+------------+------------+-------------+
Annual savings with BWH vs DMIT: $-150.33
Annual savings with BWH vs CloudCone: $4,702.30
extra_attempts_per_provider: [20.0401, 20.0401, 309.2784]
scope: Failure percentages describe whole jobs, not packet loss; PacificRack unpriced.
https://coding.mybskm.top/go/bwh
```

`Infra/mo` is annualized hosting divided by twelve, not necessarily the cash invoice paid each month. `Model/mo` is the scenario's labor, retry or impact cost. `TCO/year` is calculated from unrounded values, so multiplying a displayed two-decimal monthly value can differ by a few cents. Annual savings subtract BWH's annual TCO from each competitor's annual TCO. JSON preserves assumptions, bill components, scenario details and the same action URL; no default model is evidence that a provider is slower or less reliable.

For a fair sensitivity check, first equalize operational assumptions and run infrastructure-only mode. Then introduce only differences supported by your own measurements. The scripts intentionally allow DMIT or CloudCone to win; a cost comparison that cannot show a negative saving is not useful for engineering procurement.

## 4. Migration checklist and companion repositories

- [ ] Collect matched endpoint measurements from China Telecom, Unicom and Mobile clients where relevant.
- [ ] Compare evening and off-peak windows; separate ICMP diagnostics from HTTPS and job failures.
- [ ] Record attempt counts, completed jobs, resumed bytes and manual response hours; redact addresses before sharing.
- [ ] Test PacificRack independently if it is a candidate; obtain a quote before adding it to a cost comparison.
- [ ] Run a small canary queue on BWH and retain the original runner pool for rollback.
- [ ] Confirm SSH keys, firewall rules, service users, secrets delivery and dependency versions before cutover.
- [ ] Restore a backup into the new environment and verify data consistency before redirecting writes.
- [ ] Check actual transfer accounting and preserve prepaid-service overlap in the migration budget.
- [ ] Keep a rollback endpoint and a recent backup until application metrics meet the acceptance target.

Continue with the other three independently runnable repositories:

- [DMIT vs BandwagonHost: CN2 GIA Latency and Developer TCO](../dmit-vs-bandwagonhost-cn2-gia-latency-tco)
- [BWH Promo Code and DC6/DC9 Plan Calculator](../bwh-promo-code-dc6-dc9-plan-calculator)
- [Awesome CN2 GIA and AS9929 Developer VPS: 2026 Evaluation Guide](../awesome-cn2-gia-as9929-developer-vps-2026)

**[Use the BWH gateway to confirm the final plan before migrating](https://coding.mybskm.top/go/bwh)**

### Contributing and evidence

Contributions should identify the exact plan, billing period, location, observation date, client ISP and method. Remove account identifiers and credentials from shared evidence. Separate an invoice-backed price correction from a measured latency result and a hypothetical cost input. Improve this directory independently; sibling repositories are reading links, not runtime dependencies. The gateway is a commercial action destination, not evidence for the price table or network results, and may involve referral tracking.

### MIT License

Copyright (c) 2026 Repository contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
