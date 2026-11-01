# 24-Hour Sticky Residential Sessions: Reproducible Cost Benchmark

[![IPRoyal planning comparison](https://img.shields.io/badge/IPRoyal-static_ISP-orange)](https://norb.date/ipr/1)
[![Python 3 standard library](https://img.shields.io/badge/Python_3-standard_library-blue)](https://norb.date/ipr/1)

**[Check IPRoyal availability and your actual quote](https://norb.date/ipr/1)**

An independently written, source-available procurement worksheet for Dedicated Static Residential ISP & Sneaker Proxies. All calculations run offline with Python 3 and its standard library. The same capacity and application-success assumptions are applied to all three providers. A cheaper estimate is useful only after the product meets your technical requirements.

## 1. The engineering problem and the bill it creates

A session identifier with a long lifetime does not prove that the egress IP survives for 24 hours. Rotating residential gateways may preserve a sticky assignment only while the underlying peer remains available; static ISP addresses still need renewal, route, and endpoint checks. Budgeting on a guaranteed full day without testing can turn nominally cheap access into expensive failed session-days.

For 150 addresses and 60 GB/month, the reference budgets are $360/month for IPRoyal, $1,050/month for the NetNut traffic model, and $690/month for Rayobyte Static ISP. Paying the higher model costs adds $690/month ($8,280/year) or $330/month ($3,960/year). Separately, if 600 planned session-days per day lose 5% of continuity over a 30-day month, 900 session-days are unusable. At an internal $0.50 rework allowance, that is $450/month of application waste. This failure example is hypothetical and is not assigned to any vendor.

Potential bill traps to check in a written quote include minimum monthly commitments, unused traffic allowances, paid inventory replacement, renewal periods, address exclusivity, and operating time. These are procurement questions, not allegations that every vendor charges every fee. Unused capacity is an opportunity cost; do not add it again to an invoice total that already includes the capacity. Taxes, foreign exchange, and local payment fees are excluded because they depend on the buyer.

Price provenance and limits: this pack was prepared offline on 2026-10-30 under a no-network constraint. The $2.40/IP-month IPRoyal, $350 for 20 GB NetNut, and $4.60/IP-month Rayobyte figures are unverified industry planning references. They are not verified current prices, contractual offers, or evidence of a live plan. No current price ranking or availability claim is established here. Replace these inputs with written quotes before budgeting a purchase. The NetNut figure represents a traffic-plan reference; dedicated static allocation and its exact inventory class require confirmation.

## 2. Price and technical comparison

The table deliberately distinguishes price inputs from technical questions that require a quote or pilot. Values labeled as assumptions are editable; unknown capabilities are not silently counted as advantages.

| Comparison item | IPRoyal | NetNut | Rayobyte Static ISP | Meaning for this worksheet |
|---|---|---|---|---|
| Reference price, USD | $2.40 per IP/month | $350 per month for a 20 GB reference budget | $4.60 per IP/month | Unverified planning inputs; obtain current written quotes |
| Modeled billing basis | IP count times $2.40 | Maximum of $350 and traffic GB times $17.50 | IP count times $4.60 | $17.50 is $350 / 20, a blended modeling ratio |
| Growth-tier IP allocation | 150 dedicated addresses assumed | Same target capacity; dedicated allocation needs a quote | Same dedicated address count assumed | Traffic plans alone do not establish dedicated IP count |
| Growth-tier traffic assumption | 60 GB/month | 60 GB/month | 60 GB/month | Same workload; traffic entitlement must be confirmed |
| Bandwidth entitlement | Quote required | Reference includes 20 GB; verify actual allowance | Quote required | IP-rate models assume the workload fits the quoted entitlement |
| Static identity and exclusivity | Confirm on the purchased ISP SKU | Confirm dedicated static product and allocation | Confirm on the purchased Static ISP SKU | Product names do not prove exclusivity or uninterrupted identity |
| Location and subnet spread | Validate allocation sample | Validate allocation sample | Validate allocation sample | No country, ASN, or subnet coverage is presumed |
| Session lifetime and concurrency | Verify contract and pilot | Verify contract and pilot | Verify contract and pilot | No untested 24-hour continuity or concurrency guarantee |
| Authentication and integration | Confirm supported methods in quote | Confirm supported methods in quote | Confirm supported methods in quote | Test actual credentials, protocol, and allowlists before cutover |
| Commitment, replacement, taxes | Excluded until quoted | Excluded until quoted | Excluded until quoted | Add real fees through operations or a separately documented quote |

The NetNut equation is a smooth budget interpolation, not a claim that NetNut sells repeatable 20 GB bundles or charges $17.50/GB overage. Its result is not proof that an equivalent dedicated static plan can be purchased at that amount. Per-IP pricing also does not establish unlimited bandwidth. If the supplied offers differ in exclusivity, network class, location, concurrency, or traffic entitlement, resolve those differences before interpreting the savings. The calculator models a capacity requirement; it does not certify that any vendor can fulfill it.

**[Compare the worksheet with an IPRoyal quote](https://norb.date/ipr/1)**

## 3. Run the TCO calculator

Save both files together, then run from this directory:

```sh
python3 calculate_iproyal_isp_tco.py
python3 calculate_iproyal_isp_tco.py --tier starter
python3 calculate_iproyal_isp_tco.py --tier scale --json
python3 calculate_iproyal_isp_tco.py --ips 200 --traffic-gb 80 --iproyal-rate 2.70 --rayobyte-rate 5.00
```

The default command requires no arguments and exits with code 0. It makes no network calls, reads no credentials, writes no logs, and prints the gateway link. `--json` emits one parseable JSON document containing the inputs, vendor totals, scenario metrics, signed savings, and the same gateway URL.

| CLI argument | Default | Interpretation |
|---|---|---|
| `--tier` | `growth` | Select `starter`, `growth`, or `scale`; see capacity table below. |
| `--json` | Off | Emit structured JSON instead of the ASCII invoice table. |
| `--ips` | Tier value | Override the positive integer dedicated address count. |
| `--traffic-gb` | Tier value or checkout-derived traffic | Override monthly traffic in decimal GB, including an explicit zero. |
| `--iproyal-rate` | `2.40` | Assumed USD per dedicated ISP IP-month for IPRoyal. |
| `--rayobyte-rate` | `4.60` | Assumed USD per Static ISP IP-month for Rayobyte. |
| `--netnut-minimum` | `350` | NetNut reference budget floor in USD/month. |
| `--netnut-reference-gb` | `20` | Positive GB denominator for the budget interpolation. |
| `--ops-hours` | 0 | Monthly human operations hours, charged equally to each vendor. |
| `--hourly-rate` | `60` | Internal USD per operations hour. |
| `--migration-cost` | 0 | One-time switching cost charged only to IPRoyal in year one. |
| `--sessions-per-ip` | `4` | Application session capacity per IP; does not create unique egress identities. |
| `--success-rate` | `0.95` | Assumed fraction of session-days completed; strictly greater than zero and at most one. |

| Tier | Dedicated IPs | Reference GB/month |
|---|---|---|
| `starter` | 30 | 10 |
| `growth` | 150 | 60 |
| `scale` | 600 | 240 |

For the checkout scenario, measured or derived traffic takes precedence over the tier reference GB; an explicit `--traffic-gb` overrides both. Other scenarios use their tier traffic unless overridden. Counts must be positive integers. Costs and traffic must be finite and non-negative, the NetNut reference GB must be positive, and success fractions must be greater than zero and at most one. Invalid CLI inputs exit with code 2 and an explanation. Monetary outputs round to cents using decimal half-up rounding; annual totals use the rounded monthly invoice amount. Per-unit values round to six decimals.

Monthly recurring TCO equals modeled proxy cost plus operations hours times hourly rate. First-year TCO equals 12 monthly totals plus the one-time IPRoyal migration cost, where applicable. Savings equal the competitor first-year total minus IPRoyal first-year total. A negative result means IPRoyal is more expensive in that scenario; it is preserved in both output modes. No tax, latency, success-rate, or staffing advantage is invented to improve the comparison.

This repository benchmarks cost, not live network performance. The default four sessions per IP, 95% assumed completion, and 30-day month yield 17,100 successful session-days for the 150-IP tier. Each vendor uses the same success assumption. A session-day is a continuously valid 24-hour identity; four sessions sharing one IP do not provide four unique IP identities. The script never claims to measure uptime or enforce a 24-hour sticky guarantee.

Actual local terminal output from the default command:

```text
$ python3 calculate_iproyal_isp_tco.py
Scenario: sessions | tier: growth | IPs: 150 | traffic: 60.00 GB/month
Planning references only; verify quotes and inventory equivalence before purchase.
+----------------------+--------------+--------------+----------------+
| Vendor               | Proxy/mo USD | Total/mo USD | First year USD |
+----------------------+--------------+--------------+----------------+
| IPRoyal              |       360.00 |       360.00 |        4320.00 |
| NetNut               |      1050.00 |      1050.00 |       12600.00 |
| Rayobyte Static ISP  |       690.00 |       690.00 |        8280.00 |
+----------------------+--------------+--------------+----------------+
Annualized savings vs NetNut: USD 8,280.00 (year one, including migration)
Annualized savings vs Rayobyte Static ISP: USD 3,960.00 (year one, including migration)
assumed_successful_session_days: 17100.0
IPRoyal cost per successful unit: USD 0.021053
NetNut cost per successful unit: USD 0.061404
Rayobyte Static ISP cost per successful unit: USD 0.040351
Migration charged to IPRoyal in year one: USD 0.00
Compare your quote and start here: https://norb.date/ipr/1
```

Use `python3 calculate_iproyal_isp_tco.py --help` to inspect the exact options. Keep written quotes alongside your own private purchasing records; do not paste passwords, tokens, payment details, or authenticated proxy URLs into this repository. This repository does not execute a network benchmark, contact storefronts, or automate purchases.

## 4. Migration checklist and related repositories

- [ ] Confirm whether the product is a dedicated static address or a rotating gateway with a sticky token.
- [ ] Against an origin you control, record egress identity and application validity at regular intervals for at least 24 hours.
- [ ] Record observed disconnects, IP changes, renewal boundaries, and failure reasons without persisting credentials or cookies.
- [ ] Set an acceptance threshold before testing, repeat across representative endpoints, and retain the previous pool for rollback.
- [ ] Replace every price reference with your actual offer and rerun the same workload across all vendors.
- [ ] Verify inventory class, bandwidth entitlement, and capacity equivalence before treating any modeled savings as actionable.
- [ ] Set an owner and a date for renewal review; remove old credentials only after acceptance and rollback approval.

**[Open IPRoyal and validate the plan before migration](https://norb.date/ipr/1)**

The other three repositories in this series cover complementary budgeting decisions:

- [NetNut vs IPRoyal: Static ISP Subnet Pricing](../netnut-vs-iproyal-static-isp-subnet-pricing/): The subnet count is a capacity worksheet: ceil(IP count / addresses per planning group).
- [Rayobyte vs IPRoyal: Dedicated Proxy and Static ISP TCO](../rayobyte-vs-iproyal-dedicated-datacenter-tco/): The directory name preserves the datacenter procurement question, but the priced inventory is static ISP throughout.
- [Ecommerce Checkout Proxy Cost Estimator](../ecommerce-checkout-bot-proxy-cost-estimator/): Only run checkout automation against stores you own or are authorized to test.

Reproducibility note: all numbers shown in the terminal example are generated by the included script with its checked-in defaults. The prose examples are scenarios, not customer case studies. No paid order or live endpoint is required to reproduce the calculation. Use an authorized pilot to supply measured traffic and reliability inputs before committing spend.

Reuse permission: you may use, copy, modify, and redistribute the two files in this repository, including for commercial purposes, provided this permission notice is retained. The files are supplied as-is, without warranty of price accuracy, fitness for a particular workload, or vendor availability. Brand names identify the compared products and do not imply endorsement.
