# Redirect Delay to CPA Revenue Calculator

[![Voluum evaluation](https://img.shields.io/badge/Voluum-evaluate-1769ff)](https://norb.date/v/2)
[![Python standard library](https://img.shields.io/badge/Python-3-standard_library)](https://norb.date/v/2)
[![Offline model](https://img.shields.io/badge/Model-offline_assumptions-orange)](https://norb.date/v/2)

A reproducible, independent comparison for **High-Volume Native & Push Ad Arbitrage Attribution**. Pack: `voluum-arbitrage`. This repository contains a transparent economic model and a practical evaluation checklist. Voluum is the primary evaluation candidate; ClickMagick and Hyros are the comparison alternatives. No vendor sponsored or validated these calculations.

**[Evaluate Voluum for your campaign volume](https://norb.date/v/2)**

## 1. Engineering pain and the hidden operational bill

A redirect chain can lose visitors before a CPA offer loads. Mobile radio latency, DNS, TLS, geography, and a slow landing page all contribute. A tracker cannot take responsibility for every millisecond in that chain, and a desktop test cannot predict a low-end mobile session.

Convert an assumed or measured abandonment slope into expected payout at risk. The calculator deliberately gives every brand the same default delay; it does not invent a speed advantage for Voluum.

The hidden bill to investigate with ClickMagick and Hyros is the work surrounding the subscription: manual exports, conversion reconciliation, capacity negotiation, and time spent correcting buying decisions. These are buyer-side costs, not allegations of undisclosed vendor fees. Obtain your actual contract before assigning any paid add-on, overage, implementation charge, or renewal increase to a provider.

For a concrete staffing example, assume Voluum needs four analyst hours per month, ClickMagick needs fourteen, and Hyros needs sixteen, with labor valued at $75/hour. Those are hypothetical workflow inputs, not measured product benchmarks. Using the reference subscription inputs below gives $649, $1,349, and $1,399 per month before this repository's modeled traffic or reporting loss. The differences are **$700/month ($8,400/year)** versus ClickMagick and **$750/month ($9,000/year)** versus Hyros. A buyer spending the same labor time on all three could reach a different conclusion. Keeping fees alone would make Voluum's $349 reference input more expensive than either comparison input.

## 2. Price anchors and engineering comparison

**Price status, 2026-10-30:** this offline repository uses known historical public price anchors; they have not been checked for current availability, billing cadence, taxes, or eligibility. The $349 Voluum anchor corresponds to historical Scale pricing, $299 to historical ClickMagick Pro pricing, and $199 to historical HYROS entry-level advertising. They are not equivalent-volume quotes. In particular, HYROS entry pricing must not be treated as a guaranteed high-volume quote. Replace every fee with a written offer for your actual workload before purchase. No current price claim or guaranteed savings is made.

| Dimension | Voluum | ClickMagick | Hyros | Audit interpretation |
|---|---|---|---|---|
| Historical public monthly USD anchor | Scale: $349 | Pro: $299 | Advertised entry: $199 | Unverified historical references, not current quotes |
| Reference fee annualized, USD | $4,188 | $3,588 | $2,388 | Monthly input times 12; no annual discount assumed |
| Typical product emphasis | Affiliate campaign tracking | Click tracking and funnel measurement | Revenue attribution and customer journeys | Fit depends on native/push buying workflow |
| High-volume entitlement | Quote event allowance and overage | Quote tracked-click allowance and overage | Quote traffic and ad-spend eligibility | No unlimited-volume assumption |
| Counting unit to validate | Clicks, visits, conversions, billable events | Tracked clicks and plan accounting | Contract-specific tracking and spend terms | One paid click need not equal one billable event |
| Attribution implementation | Campaign tracking and postbacks | Tracking links and conversion reporting | Pixel and server integration workflows | Verify your network and offer integration |
| Default modeled analyst time | 4 hours/month | 14 hours/month | 16 hours/month | Buyer assumptions, not vendor performance results |
| Default hourly analyst value | $75 | $75 | $75 | Same opportunity-cost basis for all brands |
| Default incremental capacity budget | $0 | $0 | $0 | Unknown charges are not invented; add actual quotes |
| Model scenario traffic | Same selected tier | Same selected tier | Same selected tier | Economic scenario, not proof of plan capacity |
| Raw data and retention | Verify contract and export scope | Verify contract and export scope | Verify contract and export scope | Do not assume identical retention or API rights |

Native and push volume needs a workload description: paid clicks, redirect visits, postbacks, events per click, number of networks, currencies, and attribution windows. A vendor can count these differently. Tier names in this repository describe modeled workload only; they do not select an actual vendor SKU or certify that a plan supports that workload. Capacity remains a separately entered budget until the provider confirms a suitable plan.

**[Request a Voluum evaluation using your actual workload](https://norb.date/v/2)**

## 3. Run the TCO calculator

Requires Python 3.6+ and its standard library. No installation, credentials, network requests, or required arguments. Run from this directory:

```sh
python3 calculate_voluum_arbitrage_tco.py
python3 calculate_voluum_arbitrage_tco.py --tier scale --json
python3 calculate_voluum_arbitrage_tco.py --voluum-delay-ms 50 --clickmagick-delay-ms 150 --hyros-delay-ms 100
```

The following is actual default stdout captured by running the included script during repository generation:

```text
Redirect Delay to CPA Revenue Calculator | tier=growth
USD/month; historical price anchors + hypothetical workflow inputs
+-------------+-----------+-----------+-----------+-----------+------------+
| Brand       | Fee       | Labor     | Capacity  | Loss      | Total      |
+-------------+-----------+-----------+-----------+-----------+------------+
| Voluum      |    349.00 |    300.00 |      0.00 |    800.00 |    1449.00 |
| ClickMagick |    299.00 |   1050.00 |      0.00 |    800.00 |    2149.00 |
| Hyros       |    199.00 |   1200.00 |      0.00 |    800.00 |    2199.00 |
+-------------+-----------+-----------+-----------+-----------+------------+
Annual modeled savings with Voluum vs ClickMagick: $8,400.00
Annual modeled savings with Voluum vs Hyros: $9,000.00
Negative savings mean Voluum costs more under your assumptions.
https://norb.date/v/2
```

| CLI parameter | Default | Meaning |
|---|---|---|
| `--tier` | `growth` | `starter`: 100,000 clicks / $10,000 spend; `growth`: 1,000,000 / $50,000; `scale`: 5,000,000 / $200,000 |
| `--json` | Off | Emit one parseable JSON object containing inputs, rows, annual savings, and gateway |
| `--clicks` | Tier value | Override monthly paid clicks, including zero |
| `--ad-spend` | Tier value | Override monthly ad spend in USD, including zero |
| `--hourly-rate` | `75` | USD per analyst hour |
| `--voluum-fee`, `--clickmagick-fee`, `--hyros-fee` | `349`, `299`, `199` | Monthly subscription inputs; replace with actual quotes |
| `--voluum-hours`, `--clickmagick-hours`, `--hyros-hours` | `4`, `14`, `16` | Base monthly analyst hours; scale tier multiplies these by two |
| `--voluum-capacity`, `--clickmagick-capacity`, `--hyros-capacity` | `0` each | Incremental monthly capacity budget; avoid double counting an upgraded plan fee |
| `--conversion-rate` | `0.02` | Fraction from zero to one; used in redirect mode |
| `--payout` | `20` | USD per approved conversion; used in redirect mode |
| `--loss-per-second` | `0.02` | Relative conversion loss fraction per second; redirect mode |
| `--voluum-delay-ms`, `--clickmagick-delay-ms`, `--hyros-delay-ms` | `100` each | Assumed incremental delay; redirect mode only |
| `--bot-share` | `0.10` | Invalid share of spend; fraud mode only |
| `--voluum-preventable`, `--clickmagick-preventable`, `--hyros-preventable` | `0.30` each | Economically avoided fraction of invalid spend; fraud mode only |
| `--error-share` | `0.01` | Residual economic decision loss as a fraction of spend; sync mode only |

Common CLI options are accepted in every repository to simplify comparison. The mode is fixed to **`redirect`** in this repository; parameters belonging to other modes do not change its totals. `starter` and `growth` apply a labor multiplier of one; `scale` applies two. Changing `--clicks` or `--ad-spend` does not silently change staffing or subscription fees. All numeric inputs must be finite and nonnegative; fractions must also be at most one. Invalid arguments exit with code 2. Successful default and JSON executions exit with code 0.

### Calculation and interpretation

`expected payout at risk = paid clicks * conversion rate * payout * min(1, delay_ms / 1000 * loss_per_second)`. This linear sensitivity model is an assumption, not an empirical law. At 1,000,000 clicks, 2% conversion, $20 payout, and 100 ms with a 2% relative loss per second, the modeled amount is $800/month or $9,600/year per brand. Do not add it to an already delay-adjusted revenue forecast.

The displayed total is `fee + labor + capacity + modeled loss`. It is an economic exposure estimate, not a vendor invoice, revenue guarantee, or cash-flow statement. Annual savings are twelve times `(competitor monthly total - Voluum monthly total)`, using unrounded values. A negative result means Voluum costs more in that scenario. Display rounds USD to two decimals; JSON retains calculation precision. Taxes, discounts, migration fees, FX movements, creative production, chargebacks, and attribution differences are excluded unless reflected explicitly in your inputs.

The same default loss assumptions apply across brands. Default savings therefore come from the declared labor and fee scenario, not fabricated latency, accuracy, or automation measurements. Use equal labor inputs as a sensitivity test, then replace estimates with a timed trial. Do not add totals from all four repositories: they reuse subscriptions and staffing, and their loss categories may overlap.

## 4. Migration checklist and companion repositories

- [ ] Capture timestamped redirect traces by geography and device; measure p50 and p95; separate tracker time from landing-page time; test direct and redirected paths with matching campaigns; validate conversions and payouts after the change.
- [ ] Record the selected plan, billing cadence, traffic accounting, overage schedule, retention, and cancellation terms in the team's existing procurement system.
- [ ] Obtain exports and preserve attribution windows before changing any tracking link.
- [ ] Validate a controlled set of click IDs, approved conversions, duplicate postbacks, currency values, and network totals.
- [ ] Run old and new measurement in a bounded trial; reconcile timezone boundaries and avoid duplicate conversion delivery.
- [ ] Define acceptance thresholds and rollback ownership before moving budgets or replacing production links.
- [ ] Re-run this calculator with observed hours and the negotiated quote. Retain the command and JSON in your existing review workflow.

Companion repositories in this pack:

- [Attribution Cost Audit](../hyros-clickmagick-vs-voluum-attribution-cost-audit/): Audit invoice fees, event counting, manual reconciliation, and independently quoted capacity. Keep subscriptions separate from opportunity cost so a pricing decision can survive a finance review.
- [Bot Traffic Filtering and Anti-Fraud Benchmark Kit](../bot-traffic-filtering-anti-fraud-kit-benchmarks/): Estimate preventable invalid-traffic spend and distinguish classification from actual economic recovery. This is a reproducible planning benchmark, not a measured detector accuracy ranking or a vendor API integration.
- [Multi-Network Cost Sync Automation Model](../multi-network-cost-sync-automation-scripts/): Budget reconciliation work and residual decision loss before deploying cost-sync automation. The included script is an offline economic model; it does not connect to networks, schedule imports, store credentials, or change campaign budgets.

Every repository runs independently with its own script. Companion links are relative filesystem paths and do not require a hosted service. No benchmark includes private user data or a vendor's internal measurements. To make an empirical comparison, collect your own permitted traffic sample, freeze the assumptions, and report both valid-conversion retention and economic outcomes.

### Reuse permission

Copyright (c) 2026 Repository contributors. Permission is granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and sell this repository's code and documentation, provided this notice is retained. THE MATERIALS ARE PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND. AUTHORS ARE NOT LIABLE FOR CLAIMS OR DAMAGES ARISING FROM THEIR USE. Vendor names identify the compared products and do not imply endorsement.

**[Start a Voluum evaluation and replace estimates with your quote](https://norb.date/v/2)**
