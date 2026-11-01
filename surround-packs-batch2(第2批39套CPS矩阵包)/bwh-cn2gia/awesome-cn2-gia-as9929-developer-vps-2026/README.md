[![BWH gateway](https://img.shields.io/badge/BWH-compare_plans-blue)](https://coding.mybskm.top/go/bwh)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-green)](https://coding.mybskm.top/go/bwh)
[![License MIT](https://img.shields.io/badge/license-MIT-lightgrey)](https://coding.mybskm.top/go/bwh)

# Awesome CN2 GIA and AS9929 Developer VPS: 2026 Evaluation Guide

Pack: `bwh-cn2gia`. An open-source, offline comparison workbook for CN2 GIA enterprise low-latency developer VPS decisions.

**[Compare BandwagonHost plans and confirm your quote](https://coding.mybskm.top/go/bwh)**

## 1. Engineering pain and the bill behind the sticker price

Route lists age faster than procurement documents. A developer can choose a server labeled optimized, discover that only one direction takes the expected carrier, and then spend a week tuning an application around an unrelated bottleneck. This guide organizes a decision process for CN2 GIA enterprise low-latency developer VPS workloads rather than inventing a universal speed ranking.

DMIT has multiple route families and CloudCone offers budget compute; neither brand alone specifies the path your users receive. Their potential hidden project costs are qualification, incident handling and a second migration when the selected route does not meet requirements. BWH also needs qualification and can lose on infrastructure cost. An annual commitment without measured fit is a procurement risk for every provider.

Concrete scenario: four extra monthly support hours at $75/hour cost $300, and a hypothetical 1.25 additional impact hours at $200/hour cost $250. The combined difference is $550/month or $6,600/year before hosting. A one-time four-hour BWH migration costs $300 and reduces first-year savings by that amount. The default script amortizes it as $25/month. The impact inputs describe a planning scenario, not outage records or provider SLA statistics; avoid counting engineering wages inside both support labor and business impact.

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
python3 calculate_bwh_cn2gia_tco.py --tier enterprise --migration-hours 0 --cloudcone-outage-hours 0.25
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
| --bwh-ops-hours / --dmit-ops-hours / --cloudcone-ops-hours | 2 / 2 / 6 | Fleet engineering hours per month. |
| --bwh-outage-hours / --dmit-outage-hours / --cloudcone-outage-hours | 0.25 / 0.25 / 1.5 | Illustrative monthly business-impact hours; not historical uptime. |
| --impact-hourly | 200 | Contribution margin at risk per impact hour, excluding separately counted labor. |
| --migration-hours | 4 | One-time BWH switching labor included in first-year TCO. |

Numeric inputs must be finite and nonnegative. Invalid tiers and out-of-range bounded inputs fail with an argparse error. Help lists the complete accepted arguments. The default tier is three hosting nodes, while developer activity, incident hours and operational labor remain fleet-wide. Do not treat tier names as vendor SKU names or redundancy guarantees.

The first-year model is hosting plus monthly operational labor plus outage-impact hours times contribution margin at risk per hour. It adds one-time migration labor to BWH only, spread over twelve months. That makes the switching cost visible. For a greenfield comparison use `--migration-hours 0`; for steady-state recurring cost also remove that first-year term.

CN2 is associated with AS4809; AS9929 is China Unicom premium backbone infrastructure, not another name for CN2 GIA. An ASN visible in a trace does not alone prove a retail service class, a bidirectional routing commitment or an end-to-end latency target. CN2 GIA and CN2 GT should not be collapsed into one premium bucket. Classify candidates by geography, direction, retail route commitment and actual client ISP. This repository does not assert that a listed BWH, DMIT or CloudCone plan includes AS9929.

Actual local stdout from the default command, generated while preparing this README:

```text
2026 route portfolio: first-year TCO | tier=team | nodes=3
USD; historical price references + illustrative assumptions (not measurements)
+----------------------+------------+------------+------------+-------------+
| Provider             | Infra/mo   | Model/mo   | TCO/mo     | TCO/year    |
+----------------------+------------+------------+------------+-------------+
| BandwagonHost (BWH)  |      42.50 |     225.00 |     267.50 |     3209.97 |
| DMIT                 |      29.97 |     200.00 |     229.97 |     2759.64 |
| CloudCone            |      10.50 |     750.00 |     760.50 |     9126.00 |
+----------------------+------------+------------+------------+-------------+
Annual savings with BWH vs DMIT: $-450.33
Annual savings with BWH vs CloudCone: $5,916.03
one_time_bwh_migration_usd: 300
scope: Ops, outage impact and migration are fleet-wide; no SLA probability inferred.
https://coding.mybskm.top/go/bwh
```

`Infra/mo` is annualized hosting divided by twelve, not necessarily the cash invoice paid each month. `Model/mo` is the scenario's labor, retry or impact cost. `TCO/year` is calculated from unrounded values, so multiplying a displayed two-decimal monthly value can differ by a few cents. Annual savings subtract BWH's annual TCO from each competitor's annual TCO. JSON preserves assumptions, bill components, scenario details and the same action URL; no default model is evidence that a provider is slower or less reliable.

For a fair sensitivity check, first equalize operational assumptions and run infrastructure-only mode. Then introduce only differences supported by your own measurements. The scripts intentionally allow DMIT or CloudCone to win; a cost comparison that cannot show a negative saving is not useful for engineering procurement.

## 4. Migration checklist and companion repositories

- [ ] Inventory interactive shells, CI, databases and public services; assign latency and recovery targets separately.
- [ ] Classify each candidate as premium-route or budget-transit using its actual product terms.
- [ ] Measure both directions when possible and each relevant client ISP during peak hours.
- [ ] Confirm backups, restore time, memory headroom and upgrade paths; a premium route cannot fix swapping.
- [ ] Lower DNS TTL before cutover, validate restore on a canary, then keep a rollback window before cancellation.
- [ ] Confirm SSH keys, firewall rules, service users, secrets delivery and dependency versions before cutover.
- [ ] Restore a backup into the new environment and verify data consistency before redirecting writes.
- [ ] Check actual transfer accounting and preserve prepaid-service overlap in the migration budget.
- [ ] Keep a rollback endpoint and a recent backup until application metrics meet the acceptance target.

Continue with the other three independently runnable repositories:

- [DMIT vs BandwagonHost: CN2 GIA Latency and Developer TCO](../dmit-vs-bandwagonhost-cn2-gia-latency-tco)
- [BWH Promo Code and DC6/DC9 Plan Calculator](../bwh-promo-code-dc6-dc9-plan-calculator)
- [PacificRack and CloudCone vs BWH: Packet-Loss Audit Economics](../pacific-rack-cloudcone-vs-bwh-packet-loss-audit)

**[Use the BWH gateway to confirm the final plan before migrating](https://coding.mybskm.top/go/bwh)**

### Contributing and evidence

Contributions should identify the exact plan, billing period, location, observation date, client ISP and method. Remove account identifiers and credentials from shared evidence. Separate an invoice-backed price correction from a measured latency result and a hypothetical cost input. Improve this directory independently; sibling repositories are reading links, not runtime dependencies. The gateway is a commercial action destination, not evidence for the price table or network results, and may involve referral tracking.

### MIT License

Copyright (c) 2026 Repository contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
