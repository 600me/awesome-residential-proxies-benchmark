[![LisaHost gateway](https://img.shields.io/badge/LisaHost-review%20plans-blue)](https://coding.mybskm.top/go/lisahost)
[![Python standard library](https://img.shields.io/badge/Python-3-standard%20library-green)](https://coding.mybskm.top/go/lisahost)
[![MIT licensed](https://img.shields.io/badge/License-MIT-yellow)](https://coding.mybskm.top/go/lisahost)

# Scamalytics Zero Fraud Score VPS: Acceptance Suite and TCO

Category: **US Native Dual-ISP Clean Scamalytics 0 VPS**. This is a target acceptance category, not a measured certification of any provider or allocated IP.

## 1. Engineering problem and the bill behind the headline

A screenshot showing a zero fraud score is a point-in-time observation. Teams can still spend hours investigating mismatched geolocation, address reassignment, or application access failures. Treating a reputation score as a permanent property creates repeated retest work and can make a cheap exit expensive to operate.

For att/verizon static residential ISP brokers, establish whether a replacement address is free, whether it resets the rental period, and whether exclusivity is contractual. LisaHost also requires verification: neither the product category nor this repository proves that an assigned IP is US native, dual-ISP classified, or scored zero by Scamalytics.

The default scenario uses **8 workloads**, each transferring **10 GB/month**. The modeled broker stack costs **$482.00/month** versus **$188.00/month** for LisaHost, including the stated labor allowances. That is **$294.00 in extra monthly expenditure**, or **$3,528.00/year** under unchanged assumptions. These are reproducible loss examples, not observed customer losses or measured provider invoices. Reducing traffic, sharing compute, or changing staff hours can reverse the result.

**[Review LisaHost plan terms and start a small pilot](https://coding.mybskm.top/go/lisahost)**

## 2. Numeric price baseline and technical comparison

**Evidence boundary:** no live pages, checkout quotes, invoices, network benchmarks, or reputation lookups were retrieved for this repository. Dollar figures below are editable industry-style budgeting assumptions, not verified current prices, published tariffs, or guaranteed product specifications. The LisaHost $16 assumption is a planning input, not a claim that such a plan is available. There is no invented coupon, exchange rate, bandwidth entitlement, or test result. Replace each input with an actual written quote before spending money.

The competitor column describes **att/verizon static residential ISP brokers**, meaning independent resellers using those carrier labels, not AT&T or Verizon retail service. Individual brokers differ; verify every contract. One workload is modeled as one allocated exit and one compute allocation on each side. This does not assert that multiple workloads or IPs can share any particular plan.

| Cost or capability | LisaHost modeled candidate | att/verizon static residential ISP brokers | Unit / boundary | Evidence and decision check |
| --- | --- | --- | --- | --- |
| Exit or VPS rental | $16.00 | $6.00 | per workload/month | Unverified budget inputs; replace with quote |
| Separate application compute | $0.00 incremental | $8.00 | per workload/month | VPS compute assumed in bundle; broker compute separately budgeted |
| Traffic charging | $0.02 above assumed allowance | $2.50 per GB | per workload/month | Model only; contracts may include or meter traffic differently |
| Included transfer | 100 GB assumed | 0 GB assumed | per workload/month | Not a verified LisaHost or broker entitlement |
| Shared supplier fee | $0.00 assumed | $20.00 assumed | per deployment/month | Editable minimum, gateway, or support allowance |
| Operations labor | 2 hours at $30/hour | 5 hours at $30/hour | whole deployment/month | Workload-specific allowance, not measured support quality |
| Default workload transfer | 10 GB | 10 GB | each workload/month | Identical demand on both sides |
| First-year setup | $0.00 assumed | $0.00 assumed | one-time USD | Optional migration cost is added to VPS year one |
| IPv4 allocation | One dedicated exit required | One exclusive static exit required | acceptance requirement | Verify allocation; neither option is certified here |
| Compute and protocol access | Root access and resources to confirm | Proxy protocol, ports, concurrency to confirm | actual selected product | HTTP/SOCKS access is not a complete virtual machine |
| US native / dual-ISP label | Must verify assigned address | Must verify assigned address | allocation and classification evidence | ISP classification is not proof of two physical uplinks |
| Scamalytics score | Unknown until checked | Unknown until checked | timestamped observation | Zero cannot be inferred from brand or product name |

No CPU count, memory, storage, latency, uptime, clean-IP status, or carrier routing is asserted without evidence. A VPS and proxy have different service boundaries; the separate compute line makes that difference visible but does not establish equivalent performance. The modeled allowance is per workload and is not pooled across instances.

Use a LisaHost pilot if a confirmed plan meets the acceptance criteria and reduces the combined workload bill. Reject any candidate whose allocation or operating characteristics cannot be confirmed. A score of zero is not a guarantee against fraud, an application ban, or future reputation changes.

**[Compare a confirmed LisaHost quote against these assumptions](https://coding.mybskm.top/go/lisahost)**

## 3. Run the offline TCO calculator

Python 3 with its standard library is sufficient. Each repository contains its own executable script and needs no sibling files, third-party packages, API keys, or network access.

```bash
python3 calculate_lisahost_isp_tco.py
python3 calculate_lisahost_isp_tco.py --tier pilot
python3 calculate_lisahost_isp_tco.py --tier scale --json
python3 calculate_lisahost_isp_tco.py --units 5 --proxy-gb-price 0 --proxy-compute 0
python3 calculate_lisahost_isp_tco.py --coupon-percent 10 --setup-fee 75 --json
```

| CLI option | Default here | Meaning |
| --- | --- | --- |
| `--tier` | `team` | `pilot` = 2, `team` = 8, `scale` = 24 workloads |
| `--json` | off | Emit one parseable object; monetary values are decimal strings |
| `--units` | tier count | Positive integer override, from 1 to 1,000,000 |
| `--gb-per-unit` | 10 | Monthly billed GB per workload on both sides |
| `--proxy-ip-price` | 6 | Broker USD per address/month |
| `--proxy-gb-price` | 2.50 | Broker USD per billed GB |
| `--proxy-compute` | 8 | Separate compute USD per workload/month |
| `--vps-price` | 16 | LisaHost assumed VPS USD per workload/month |
| `--included-gb` | 100 | Assumed included GB per VPS/month |
| `--vps-gb-price` | 0.02 | USD per excess GB beyond each VPS allowance |
| `--broker-fee` | 20 | Shared broker USD fee per deployment/month |
| `--proxy-admin-hours` | 5 | Total monthly staff hours for broker stack |
| `--vps-admin-hours` | 2 | Total monthly staff hours for VPS stack |
| `--hourly-rate` | 30 | USD per staff hour on both sides |
| `--coupon-percent` | 0 | 0 to 100, applied only to VPS rental for all modeled months |
| `--setup-fee` | 0 | One-time migration/setup USD added to VPS year one |

Nonnegative numeric inputs must be finite and at most 1e12. Invalid arguments exit with code 2. A valid scenario exits with code 0 even if savings are negative: a negative number is useful cost evidence. Dollar rows are rounded to cents using decimal arithmetic, and displayed monthly rows are summed before annualization.

The calculation is explicit:

```text
Broker/month = units * (IP rental + GB * broker GB rate + separate compute)
               + shared broker fee + broker staff hours * hourly rate
LisaHost/month = units * VPS rental * (1 - coupon percent / 100)
                 + units * max(0, GB - included GB) * VPS excess GB rate
                 + VPS staff hours * hourly rate
Year-one savings = 12 * (Broker/month - LisaHost/month) - setup fee
```

The following output was captured by actually running this repository's script with no arguments:

```text
IP reputation acceptance and retest cost
USD assumptions only | tier=team | workloads=8
+------------------------+----------------+----------------+
| Monthly item           |     ISP broker |   LisaHost VPS |
+------------------------+----------------+----------------+
| Exit / VPS rental      | $        48.00 | $       128.00 |
| Traffic overage        | $       200.00 | $         0.00 |
| Separate compute       | $        64.00 | $         0.00 |
| Broker fee             | $        20.00 | $         0.00 |
| Admin labor            | $       150.00 | $        60.00 |
| TOTAL                  | $       482.00 | $       188.00 |
+------------------------+----------------+----------------+
Monthly savings: $294.00
Year-one migration/setup: $0.00
Annualized savings (year one): $3,528.00
Coupon assumes 12 eligible months; taxes and FX excluded.
Verify plan terms and assigned IP before purchase: https://coding.mybskm.top/go/lisahost
```

The JSON fields `broker_year_one_usd` and `lisahost_year_one_usd` expose both totals; `annual_savings_usd` is their difference. Taxes, currency conversion, sales losses, refunds, financing, and outage costs are excluded because no evidence is available to price them. Setup is a VPS-only migration allowance, not a recurring charge. For later years, remove that one-time cost. A one-month 10% coupon saves only one month's eligible rental discount; the script's annual coupon scenario assumes twelve eligible months and must not be used unchanged for a teaser offer.

To test sensitivity, lower the broker GB rate to zero, set separate compute to zero if spare capacity exists, and raise the VPS price to the actual resource tier. Set both labor allowances to zero to see infrastructure-only spending. The model deliberately permits the broker to win. It does not estimate platform approval rates or infer IP reputation from cost.

## 4. Migration and reproducible evaluation checklist

This is an offline acceptance checklist plus a cost calculator, not an automated Scamalytics client. For each assigned address, manually record UTC observation time, region, ASN, organization, provider allocation evidence, and the exact score and lookup source available under its usage terms. Repeat after a reassignment and at a planned interval. Record unavailable data as unknown, not zero. The script makes no network requests and never fabricates a reputation result.

- [ ] Obtain provider confirmation of allocation, intended region, and address replacement terms.
- [ ] Record a permitted lookup result with timestamp and distinguish ASN from marketing labels.
- [ ] Define whether an unknown or nonzero score triggers hold, review, or replacement.
- [ ] Test the real authorized application separately from the reputation lookup.
- [ ] Budget retest labor and retain rollback routing until both application and IP checks pass.
- [ ] Confirm memory, CPU, storage, ports, transfer limits, backups, and recurring price from the actual order.
- [ ] Check any native-US, dual-ISP, and clean-IP claims on the assigned address using permitted evidence.
- [ ] Replace modeled rates and hours with billing data; compare both totals before expanding.
- [ ] Define rollback ownership and remove obsolete paid resources only after pilot acceptance.

Keep an internal worksheet with candidate, timestamp, tested workload, observed result, invoice scope, and pass/fail reason. Leave credentials and sensitive IP inventories out of public commits. There is no measured winner in this repository: the current preference is a conditional cost result, and the acceptance procedure supplies the missing operational evidence.

**[Review LisaHost availability and request terms for your pilot](https://coding.mybskm.top/go/lisahost)**

Related independent repositories in this pack:

- [US Native Dual-ISP VPS: TikTok Shop Operations Benchmark](../us-native-dual-isp-vps-tiktok-shop-benchmark)
- [LisaHost Coupon and AT&T / Frontier ISP IP Cost Calculator](../lisahost-coupon-att-frontier-isp-ip-calculator)
- [Static ISP Proxy vs LisaHost Dedicated VPS: Workload TCO](../static-isp-proxy-vs-lisahost-dedicated-vps-tco)

### License and scope

Copyright (c) 2026 lisahost-isp contributors. README and Python source are released under the MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Brand names remain their owners' property. This is an independent planning resource, not an official carrier or platform certification. The LisaHost gateway is the sole action destination; its presence is not evidence for price, performance, affiliation, or commission arrangements.
