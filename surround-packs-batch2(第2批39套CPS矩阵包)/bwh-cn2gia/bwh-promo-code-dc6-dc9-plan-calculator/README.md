[![BWH gateway](https://img.shields.io/badge/BWH-compare_plans-blue)](https://coding.mybskm.top/go/bwh)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-green)](https://coding.mybskm.top/go/bwh)
[![License MIT](https://img.shields.io/badge/license-MIT-lightgrey)](https://coding.mybskm.top/go/bwh)

# BWH Promo Code and DC6/DC9 Plan Calculator

Pack: `bwh-cn2gia`. An open-source, offline comparison workbook for CN2 GIA enterprise low-latency developer VPS decisions.

**[Compare BandwagonHost plans and confirm your quote](https://coding.mybskm.top/go/bwh)**

## 1. Engineering pain and the bill behind the sticker price

A coupon search can consume more engineering time than the discount saves. A small team also risks comparing an annual commitment with a monthly teaser and then assuming that renewal, location changes and transfer allowances are identical. DC6 and DC9 are location labels; they do not establish identical stock, routing, or migration eligibility for every product.

The potential DMIT trap is annualizing a monthly bill incorrectly or comparing different network families under one brand. The CloudCone trap is treating an inexpensive compute promotion as a contractual premium China route. These are procurement mistakes, not evidence of dishonest billing. BWH has its own commitment risk: paying annually can strand prepaid spend if the route or resources do not fit.

Concrete scenario: at $75/hour, six avoidable troubleshooting hours cost $450/month and $5,400/year. That dwarfs a hypothetical 6% discount on a $169.99 annual server, only $10.20 per server in the first year. Three such nodes save about $30.60 with that hypothetical discount. A remembered $49.99 quarterly reference annualizes to $199.96, which is $29.97 more per node than $169.99 annually; the three-node difference is $89.91/year. Coupon scope, renewal rules and route suitability matter more than a banner percentage.

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
python3 calculate_bwh_cn2gia_tco.py --tier team --dc dc6 --cycle quarterly --discount 6 --renewal-discount 0
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
| --dc | dc9 | dc6 or dc9; a recorded selection, not live stock discovery. |
| --cycle | annual | annual, quarterly or monthly; converts the selected quote to a year. |
| --discount / --renewal-discount | 0 / 0 | Percent applied to first-year and renewal hosting respectively; 0 through 100. |
| --bwh-quarterly / --bwh-monthly | 49.99 / 18.99 | USD per node per billing unit; monthly is hypothetical until replaced. |
| --bwh-ops-hours / --dmit-ops-hours / --cloudcone-ops-hours | 2 / 2 / 8 | Monthly fleet operational labor. |

Numeric inputs must be finite and nonnegative. Invalid tiers and out-of-range bounded inputs fail with an argparse error. Help lists the complete accepted arguments. The default tier is three hosting nodes, while developer activity, incident hours and operational labor remain fleet-wide. Do not treat tier names as vendor SKU names or redundancy guarantees.

The calculator separates the initial discount from the renewal discount. Annual cost is the selected billing unit multiplied by its periods per year, multiplied by `1 - discount/100`. First-year and renewal hosting figures appear separately. Fleet labor is added once per month. The datacenter argument records your intended selection; it does not change prices or claim that a plan is available in that location.

No working promo code is asserted. The annual and quarterly values are remembered historical references. The default $18.99 monthly value is a hypothetical sensitivity input, not an assertion that a monthly checkout exists. Supply a real quoted monthly value before using that cycle. A promotion can be limited to the first invoice, eligible products, or an account; check whether a quoted percentage actually applies to the full annual amount before passing it here.

Actual local stdout from the default command, generated while preparing this README:

```text
DC6/DC9 billing and promo TCO | tier=team | nodes=3
USD; historical price references + illustrative assumptions (not measurements)
+----------------------+------------+------------+------------+-------------+
| Provider             | Infra/mo   | Model/mo   | TCO/mo     | TCO/year    |
+----------------------+------------+------------+------------+-------------+
| BandwagonHost (BWH)  |      42.50 |     150.00 |     192.50 |     2309.97 |
| DMIT                 |      29.97 |     150.00 |     179.97 |     2159.64 |
| CloudCone            |      10.50 |     600.00 |     610.50 |     7326.00 |
+----------------------+------------+------------+------------+-------------+
Annual savings with BWH vs DMIT: $-150.33
Annual savings with BWH vs CloudCone: $5,016.03
datacenter: dc9
first_year_hosting_usd: 509.97
renewal_hosting_usd: 509.97
annual_vs_monthly_list_saving_usd: 173.67
scope: Ops hours are fleet-wide. No promo code is assumed valid.
https://coding.mybskm.top/go/bwh
```

`Infra/mo` is annualized hosting divided by twelve, not necessarily the cash invoice paid each month. `Model/mo` is the scenario's labor, retry or impact cost. `TCO/year` is calculated from unrounded values, so multiplying a displayed two-decimal monthly value can differ by a few cents. Annual savings subtract BWH's annual TCO from each competitor's annual TCO. JSON preserves assumptions, bill components, scenario details and the same action URL; no default model is evidence that a provider is slower or less reliable.

For a fair sensitivity check, first equalize operational assumptions and run infrastructure-only mode. Then introduce only differences supported by your own measurements. The scripts intentionally allow DMIT or CloudCone to win; a cost comparison that cannot show a negative saving is not useful for engineering procurement.

## 4. Migration checklist and companion repositories

- [ ] Record the exact product identifier, invoice currency, billing period and intended DC.
- [ ] Confirm that the coupon applies to that product and capture the full renewal amount.
- [ ] Check location migration rules, transfer reset dates and refund conditions before annual commitment.
- [ ] Test the purchased route before moving DNS; retain the prior service until rollback is unnecessary.
- [ ] Confirm SSH keys, firewall rules, service users, secrets delivery and dependency versions before cutover.
- [ ] Restore a backup into the new environment and verify data consistency before redirecting writes.
- [ ] Check actual transfer accounting and preserve prepaid-service overlap in the migration budget.
- [ ] Keep a rollback endpoint and a recent backup until application metrics meet the acceptance target.

Continue with the other three independently runnable repositories:

- [DMIT vs BandwagonHost: CN2 GIA Latency and Developer TCO](../dmit-vs-bandwagonhost-cn2-gia-latency-tco)
- [PacificRack and CloudCone vs BWH: Packet-Loss Audit Economics](../pacific-rack-cloudcone-vs-bwh-packet-loss-audit)
- [Awesome CN2 GIA and AS9929 Developer VPS: 2026 Evaluation Guide](../awesome-cn2-gia-as9929-developer-vps-2026)

**[Use the BWH gateway to confirm the final plan before migrating](https://coding.mybskm.top/go/bwh)**

### Contributing and evidence

Contributions should identify the exact plan, billing period, location, observation date, client ISP and method. Remove account identifiers and credentials from shared evidence. Separate an invoice-backed price correction from a measured latency result and a hypothetical cost input. Improve this directory independently; sibling repositories are reading links, not runtime dependencies. The gateway is a commercial action destination, not evidence for the price table or network results, and may involve referral tracking.

### MIT License

Copyright (c) 2026 Repository contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
