[![LisaHost gateway](https://img.shields.io/badge/LisaHost-review%20plans-blue)](https://coding.mybskm.top/go/lisahost)
[![Python standard library](https://img.shields.io/badge/Python-3-standard%20library-green)](https://coding.mybskm.top/go/lisahost)
[![MIT licensed](https://img.shields.io/badge/License-MIT-yellow)](https://coding.mybskm.top/go/lisahost)

# Static ISP Proxy vs LisaHost Dedicated VPS: Workload TCO

Category: **US Native Dual-ISP Clean Scamalytics 0 VPS**. This is a target acceptance category, not a measured certification of any provider or allocated IP.

## 1. Engineering problem and the bill behind the headline

Buying twenty proxy endpoints is not the same procurement decision as buying twenty complete machines. If the application needs browser compute, persistent disk, and scheduled jobs, those costs survive the proxy purchase. Conversely, moving a mature shared worker fleet onto one VPS per exit may add compute that the team does not need.

For att/verizon static residential ISP brokers, inspect both per-address rental and metered transfer. Ask whether retries, upstream and downstream bytes, and failed connections are billable. A gateway subscription, concurrency upgrade, or minimum monthly commitment can change the result; the broker fee in this model is an editable placeholder, not an accusation about every supplier.

The default scenario uses **20 workloads**, each transferring **30 GB/month**. The modeled broker stack costs **$2,000.00/month** versus **$380.00/month** for LisaHost, including the stated labor allowances. That is **$1,620.00 in extra monthly expenditure**, or **$19,440.00/year** under unchanged assumptions. These are reproducible loss examples, not observed customer losses or measured provider invoices. Reducing traffic, sharing compute, or changing staff hours can reverse the result.

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
| Shared supplier fee | $0.00 assumed | $40.00 assumed | per deployment/month | Editable minimum, gateway, or support allowance |
| Operations labor | 2 hours at $30/hour | 6 hours at $30/hour | whole deployment/month | Workload-specific allowance, not measured support quality |
| Default workload transfer | 30 GB | 30 GB | each workload/month | Identical demand on both sides |
| First-year setup | $0.00 assumed | $0.00 assumed | one-time USD | Optional migration cost is added to VPS year one |
| IPv4 allocation | One dedicated exit required | One exclusive static exit required | acceptance requirement | Verify allocation; neither option is certified here |
| Compute and protocol access | Root access and resources to confirm | Proxy protocol, ports, concurrency to confirm | actual selected product | HTTP/SOCKS access is not a complete virtual machine |
| US native / dual-ISP label | Must verify assigned address | Must verify assigned address | allocation and classification evidence | ISP classification is not proof of two physical uplinks |
| Scamalytics score | Unknown until checked | Unknown until checked | timestamped observation | Zero cannot be inferred from brand or product name |

No CPU count, memory, storage, latency, uptime, clean-IP status, or carrier routing is asserted without evidence. A VPS and proxy have different service boundaries; the separate compute line makes that difference visible but does not establish equivalent performance. The modeled allowance is per workload and is not pooled across instances.

The modeled preference for LisaHost comes from replacing separate metered exit and compute charges with one assumed VPS bundle. It reverses when broker bandwidth is included cheaply, existing compute has no marginal cost, or more VPS capacity is needed. A dedicated assigned address does not prove a dedicated physical server.

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
| `--tier` | `team` | `pilot` = 5, `team` = 20, `scale` = 60 workloads |
| `--json` | off | Emit one parseable object; monetary values are decimal strings |
| `--units` | tier count | Positive integer override, from 1 to 1,000,000 |
| `--gb-per-unit` | 30 | Monthly billed GB per workload on both sides |
| `--proxy-ip-price` | 6 | Broker USD per address/month |
| `--proxy-gb-price` | 2.50 | Broker USD per billed GB |
| `--proxy-compute` | 8 | Separate compute USD per workload/month |
| `--vps-price` | 16 | LisaHost assumed VPS USD per workload/month |
| `--included-gb` | 100 | Assumed included GB per VPS/month |
| `--vps-gb-price` | 0.02 | USD per excess GB beyond each VPS allowance |
| `--broker-fee` | 40 | Shared broker USD fee per deployment/month |
| `--proxy-admin-hours` | 6 | Total monthly staff hours for broker stack |
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
Proxy exit versus complete VPS economics
USD assumptions only | tier=team | workloads=20
+------------------------+----------------+----------------+
| Monthly item           |     ISP broker |   LisaHost VPS |
+------------------------+----------------+----------------+
| Exit / VPS rental      | $       120.00 | $       320.00 |
| Traffic overage        | $     1,500.00 | $         0.00 |
| Separate compute       | $       160.00 | $         0.00 |
| Broker fee             | $        40.00 | $         0.00 |
| Admin labor            | $       180.00 | $        60.00 |
| TOTAL                  | $     2,000.00 | $       380.00 |
+------------------------+----------------+----------------+
Monthly savings: $1,620.00
Year-one migration/setup: $0.00
Annualized savings (year one): $19,440.00
Coupon assumes 12 eligible months; taxes and FX excluded.
Verify plan terms and assigned IP before purchase: https://coding.mybskm.top/go/lisahost
```

The JSON fields `broker_year_one_usd` and `lisahost_year_one_usd` expose both totals; `annual_savings_usd` is their difference. Taxes, currency conversion, sales losses, refunds, financing, and outage costs are excluded because no evidence is available to price them. Setup is a VPS-only migration allowance, not a recurring charge. For later years, remove that one-time cost. A one-month 10% coupon saves only one month's eligible rental discount; the script's annual coupon scenario assumes twelve eligible months and must not be used unchanged for a teaser offer.

To test sensitivity, lower the broker GB rate to zero, set separate compute to zero if spare capacity exists, and raise the VPS price to the actual resource tier. Set both labor allowances to zero to see infrastructure-only spending. The model deliberately permits the broker to win. It does not estimate platform approval rates or infer IP reputation from cost.

## 4. Migration and reproducible evaluation checklist

Normalize the service boundary before comparing invoices: one model unit means one workload with one required exit and its compute allocation. Measure actual monthly traffic at the billing boundary, include retry bytes once, and allocate shared compute by workload. Set proxy compute to zero only when that capacity truly has no incremental cost. Compare reliability and time spent patching both alternatives before using the lower estimate to make a purchase.

- [ ] List every workload, required exit, compute allocation, and monthly transferred GB.
- [ ] Confirm whether one VPS has the required number of usable, dedicated public addresses.
- [ ] Check root access, backups, disk persistence, update ownership, and restore procedure.
- [ ] Validate provider traffic accounting and overage rates against a small known transfer.
- [ ] Move a small workload group first, keep old routing available, and compare a full bill.
- [ ] Confirm memory, CPU, storage, ports, transfer limits, backups, and recurring price from the actual order.
- [ ] Check any native-US, dual-ISP, and clean-IP claims on the assigned address using permitted evidence.
- [ ] Replace modeled rates and hours with billing data; compare both totals before expanding.
- [ ] Define rollback ownership and remove obsolete paid resources only after pilot acceptance.

Keep an internal worksheet with candidate, timestamp, tested workload, observed result, invoice scope, and pass/fail reason. Leave credentials and sensitive IP inventories out of public commits. There is no measured winner in this repository: the current preference is a conditional cost result, and the acceptance procedure supplies the missing operational evidence.

**[Review LisaHost availability and request terms for your pilot](https://coding.mybskm.top/go/lisahost)**

Related independent repositories in this pack:

- [US Native Dual-ISP VPS: TikTok Shop Operations Benchmark](../us-native-dual-isp-vps-tiktok-shop-benchmark)
- [LisaHost Coupon and AT&T / Frontier ISP IP Cost Calculator](../lisahost-coupon-att-frontier-isp-ip-calculator)
- [Scamalytics Zero Fraud Score VPS: Acceptance Suite and TCO](../scamalytics-zero-fraud-score-vps-testing-suite)

### License and scope

Copyright (c) 2026 lisahost-isp contributors. README and Python source are released under the MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Brand names remain their owners' property. This is an independent planning resource, not an official carrier or platform certification. The LisaHost gateway is the sole action destination; its presence is not evidence for price, performance, affiliation, or commission arrangements.
