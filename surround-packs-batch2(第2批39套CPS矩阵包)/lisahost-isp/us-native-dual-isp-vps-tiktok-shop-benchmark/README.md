[![LisaHost gateway](https://img.shields.io/badge/LisaHost-review%20plans-blue)](https://coding.mybskm.top/go/lisahost)
[![Python standard library](https://img.shields.io/badge/Python-3-standard%20library-green)](https://coding.mybskm.top/go/lisahost)
[![MIT licensed](https://img.shields.io/badge/License-MIT-yellow)](https://coding.mybskm.top/go/lisahost)

# US Native Dual-ISP VPS: TikTok Shop Operations Benchmark

Category: **US Native Dual-ISP Clean Scamalytics 0 VPS**. This is a target acceptance category, not a measured certification of any provider or allocated IP.

## 1. Engineering problem and the bill behind the headline

A seller operations team can buy a static residential exit and still need a separate machine to run its authorized browser sessions, export orders, and retain audit logs. The proxy invoice covers an exit path; it does not automatically cover compute, storage, or browser administration. Repeated media uploads and catalog synchronization can turn a low per-IP headline into a large traffic bill.

For att/verizon static residential ISP brokers, request the actual pool exclusivity, traffic allowance, session timeout, replacement fee, and renewal terms. A carrier name in a product description is not a direct carrier contract. A session that rotates on reconnect can interrupt a legitimate workflow even when the IP rental line looks cheap.

The default scenario uses **10 workloads**, each transferring **20 GB/month**. The modeled broker stack costs **$785.00/month** versus **$190.00/month** for LisaHost, including the stated labor allowances. That is **$595.00 in extra monthly expenditure**, or **$7,140.00/year** under unchanged assumptions. These are reproducible loss examples, not observed customer losses or measured provider invoices. Reducing traffic, sharing compute, or changing staff hours can reverse the result.

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
| Shared supplier fee | $0.00 assumed | $25.00 assumed | per deployment/month | Editable minimum, gateway, or support allowance |
| Operations labor | 1 hours at $30/hour | 4 hours at $30/hour | whole deployment/month | Workload-specific allowance, not measured support quality |
| Default workload transfer | 20 GB | 20 GB | each workload/month | Identical demand on both sides |
| First-year setup | $0.00 assumed | $0.00 assumed | one-time USD | Optional migration cost is added to VPS year one |
| IPv4 allocation | One dedicated exit required | One exclusive static exit required | acceptance requirement | Verify allocation; neither option is certified here |
| Compute and protocol access | Root access and resources to confirm | Proxy protocol, ports, concurrency to confirm | actual selected product | HTTP/SOCKS access is not a complete virtual machine |
| US native / dual-ISP label | Must verify assigned address | Must verify assigned address | allocation and classification evidence | ISP classification is not proof of two physical uplinks |
| Scamalytics score | Unknown until checked | Unknown until checked | timestamped observation | Zero cannot be inferred from brand or product name |

No CPU count, memory, storage, latency, uptime, clean-IP status, or carrier routing is asserted without evidence. A VPS and proxy have different service boundaries; the separate compute line makes that difference visible but does not establish equivalent performance. The modeled allowance is per workload and is not pooled across instances.

Prefer a LisaHost pilot when browser compute and a stable assigned exit are both required and the confirmed plan fits the workload. Retain a proxy-based design when an existing managed compute fleet already covers the browsers, or when the workload needs many independently allocated exits that would require many VPS instances.

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
| `--tier` | `team` | `pilot` = 2, `team` = 10, `scale` = 30 workloads |
| `--json` | off | Emit one parseable object; monetary values are decimal strings |
| `--units` | tier count | Positive integer override, from 1 to 1,000,000 |
| `--gb-per-unit` | 20 | Monthly billed GB per workload on both sides |
| `--proxy-ip-price` | 6 | Broker USD per address/month |
| `--proxy-gb-price` | 2.50 | Broker USD per billed GB |
| `--proxy-compute` | 8 | Separate compute USD per workload/month |
| `--vps-price` | 16 | LisaHost assumed VPS USD per workload/month |
| `--included-gb` | 100 | Assumed included GB per VPS/month |
| `--vps-gb-price` | 0.02 | USD per excess GB beyond each VPS allowance |
| `--broker-fee` | 25 | Shared broker USD fee per deployment/month |
| `--proxy-admin-hours` | 4 | Total monthly staff hours for broker stack |
| `--vps-admin-hours` | 1 | Total monthly staff hours for VPS stack |
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
Authorized TikTok Shop operations
USD assumptions only | tier=team | workloads=10
+------------------------+----------------+----------------+
| Monthly item           |     ISP broker |   LisaHost VPS |
+------------------------+----------------+----------------+
| Exit / VPS rental      | $        60.00 | $       160.00 |
| Traffic overage        | $       500.00 | $         0.00 |
| Separate compute       | $        80.00 | $         0.00 |
| Broker fee             | $        25.00 | $         0.00 |
| Admin labor            | $       120.00 | $        30.00 |
| TOTAL                  | $       785.00 | $       190.00 |
+------------------------+----------------+----------------+
Monthly savings: $595.00
Year-one migration/setup: $0.00
Annualized savings (year one): $7,140.00
Coupon assumes 12 eligible months; taxes and FX excluded.
Verify plan terms and assigned IP before purchase: https://coding.mybskm.top/go/lisahost
```

The JSON fields `broker_year_one_usd` and `lisahost_year_one_usd` expose both totals; `annual_savings_usd` is their difference. Taxes, currency conversion, sales losses, refunds, financing, and outage costs are excluded because no evidence is available to price them. Setup is a VPS-only migration allowance, not a recurring charge. For later years, remove that one-time cost. A one-month 10% coupon saves only one month's eligible rental discount; the script's annual coupon scenario assumes twelve eligible months and must not be used unchanged for a teaser offer.

To test sensitivity, lower the broker GB rate to zero, set separate compute to zero if spare capacity exists, and raise the VPS price to the actual resource tier. Set both labor allowances to zero to see infrastructure-only spending. The model deliberately permits the broker to win. It does not estimate platform approval rates or infer IP reputation from cost.

## 4. Migration and reproducible evaluation checklist

Use one authorized shop workflow and the same browser version, region, time window, and payload on both candidates. Run at least 30 timed repetitions of login, catalog export, and a permitted media upload. Record completion count, median latency, p95 latency, transferred GB, reconnects, and manual recovery minutes. Keep failed attempts in the denominator. Do not create fake accounts or treat successful access as a promise of future platform acceptance.

- [ ] Confirm the shop operator has permission to use the account and hosting region.
- [ ] Inventory cookies and credentials locally; transfer them through an encrypted channel only.
- [ ] Validate the assigned IP region and routing before changing the existing workflow.
- [ ] Run the same authorized upload and export on a pilot VPS; record latency and actual traffic.
- [ ] Keep a rollback host until one complete business cycle passes without unexpected session changes.
- [ ] Confirm memory, CPU, storage, ports, transfer limits, backups, and recurring price from the actual order.
- [ ] Check any native-US, dual-ISP, and clean-IP claims on the assigned address using permitted evidence.
- [ ] Replace modeled rates and hours with billing data; compare both totals before expanding.
- [ ] Define rollback ownership and remove obsolete paid resources only after pilot acceptance.

Keep an internal worksheet with candidate, timestamp, tested workload, observed result, invoice scope, and pass/fail reason. Leave credentials and sensitive IP inventories out of public commits. There is no measured winner in this repository: the current preference is a conditional cost result, and the acceptance procedure supplies the missing operational evidence.

**[Review LisaHost availability and request terms for your pilot](https://coding.mybskm.top/go/lisahost)**

Related independent repositories in this pack:

- [LisaHost Coupon and AT&T / Frontier ISP IP Cost Calculator](../lisahost-coupon-att-frontier-isp-ip-calculator)
- [Static ISP Proxy vs LisaHost Dedicated VPS: Workload TCO](../static-isp-proxy-vs-lisahost-dedicated-vps-tco)
- [Scamalytics Zero Fraud Score VPS: Acceptance Suite and TCO](../scamalytics-zero-fraud-score-vps-testing-suite)

### License and scope

Copyright (c) 2026 lisahost-isp contributors. README and Python source are released under the MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Brand names remain their owners' property. This is an independent planning resource, not an official carrier or platform certification. The LisaHost gateway is the sole action destination; its presence is not evidence for price, performance, affiliation, or commission arrangements.
