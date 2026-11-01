# RedTrack vs Voluum: S2S Postback and Redirect Latency

[![Review Voluum](https://img.shields.io/badge/Review-Voluum-orange)](https://norb.date/v/1)
[![Python 3 standard library](https://img.shields.io/badge/Python-3-standard_library-blue)](https://norb.date/v/1)
[![Offline scenario calculator](https://img.shields.io/badge/Calculator-offline-green)](https://norb.date/v/1)

Independent, reproducible cost analysis for **Cloud-Native Server-to-Server Ad Tracking & AI Traffic Distribution**. This repository evaluates Voluum alongside RedTrack and BeMob through explicit operating assumptions. The recommended next step is to evaluate Voluum against your actual campaign requirements: **[Review Voluum and request a matching plan](https://norb.date/v/1)**.

## 1. The engineering problem and the bill behind it

A redirect chain can accumulate DNS, TLS, regional routing and destination response time. A conversion can also arrive after an attribution window closes. Buying a tracker does not establish how much revenue either failure costs. RedTrack and BeMob subscription savings can disappear when engineers repeatedly diagnose callback retries or campaign routing, but the size of that cost depends on your deployment.

With 30,000 monthly clicks worth $1 each, an assumed 1.5% avoidable conversion-value loss costs $450 per month or $5,400 per year. This is a business sensitivity calculation, not a measured difference between vendors.

The hidden-bill checklist covers billable event definitions, event allowance, excess-event charges, automation access, API access, reporting retention, extra users and support. These are procurement questions, not allegations of undisclosed charges by either competitor. Ask each supplier to identify which features are included in its specific quote. A click, impression, conversion and retry may have different billing treatment; normalize the event definition before comparing allowances.

The model treats Voluum as a candidate for reducing manual work and preventable loss. Its favorable default assumptions are a hypothesis to validate. No benchmark traffic was sent, no latency measurement was collected, and no savings are guaranteed. Start with the engineering issue, collect evidence, and then **[evaluate the Voluum workflow](https://norb.date/v/1)** using a comparable plan.

## 2. Price and technical comparison

The dollar anchors below are known historical public starting-price benchmarks used for offline planning: Voluum $199/month, RedTrack $149/month and BeMob $49/month for an entry paid offering. They are not verified October 2026 quotes and do not establish matching feature entitlements. BeMob has also offered a free tier; the paid benchmark does not describe every available option. Current pricing, billing cadence and eligibility must be confirmed before purchase. Annual base figures simply multiply the monthly anchors by 12; they do not claim annual-contract discounts. This repository deliberately makes no unverified claim about current plan quotas, latency or AI uplift.

| Price or technical parameter | Voluum | RedTrack | BeMob | Basis and interpretation |
| --- | --- | --- | --- | --- |
| Historical monthly paid entry anchor | $199 | $149 | $49 | Historical public benchmark; replace with quote |
| Annual base at monthly anchor | $2,388 | $1,788 | $588 | Monthly times 12; no discount assumed |
| Hosting model | Cloud SaaS | Cloud SaaS | Cloud SaaS | No tracker server included in this model |
| S2S postback workflow | Supported | Supported | Supported | Mapping and source compatibility require testing |
| API / automation entitlement | Verify selected plan | Verify selected plan | Verify selected plan | No assumption of identical API coverage |
| Included monthly events in calculator | 1,000,000 | 1,000,000 | 1,000,000 | Shared hypothetical allowance, not vendor quotas |
| Excess cost per million in calculator | $20 | $20 | $20 | Shared hypothetical prorated rate, not vendor tariffs |
| Monthly operating hours in default | 3 | 9 | 12 | Scenario inputs, not observed vendor results |
| Preventable media loss in default | 0.8% | 1.6% | 2.0% | Hypothetical sensitivity assumptions |
| Redirect latency / attribution coverage | Measure locally | Measure locally | Measure locally | No invented p95 or delivery percentage |

The shared allowance and excess rate isolate operational sensitivity; they cannot reproduce three actual vendor invoices. Use all-in quote amounts with `--included-events` above your workload to remove the hypothetical excess line when comparing fixed quotes. Include add-ons, required support and automation in each `--*-base` amount. Taxes, exchange rates, historical data import and one-time implementation costs are excluded. Add one-time migration spend separately when estimating first-year payback.

## 3. Run the reproducible TCO calculator

Requires Python 3 with only the standard library. No account, credentials, network access or package installation is needed. The script is executable and also supports direct Python invocation.

```bash
python3 calculate_voluum_dsp_tco.py
python3 calculate_voluum_dsp_tco.py --tier small
python3 calculate_voluum_dsp_tco.py --tier scale --json
python3 calculate_voluum_dsp_tco.py --ad-spend 30000 --events 5000000 --hourly-rate 75
```

| CLI option | Default | Meaning |
| --- | --- | --- |
| `--tier` | `growth` | Workload preset: `small`, `growth`, or `scale`; not a vendor plan |
| `--json` | Off | Emit the same calculation as JSON, including assumptions and gateway |
| `--events` | From tier | Monthly normalized billable events; zero is allowed |
| `--ad-spend` | From tier | Monthly media spend in USD |
| `--hourly-rate` | 75 | Fully loaded hourly operating cost in USD |
| `--included-events` | 1000000 | Shared hypothetical event allowance |
| `--overage-per-million` | 20 | Shared hypothetical prorated excess charge |
| `--voluum-base`, `--redtrack-base`, `--bemob-base` | 199 / 149 / 49 | Replace historical anchors with all-in monthly quotes |
| `--voluum-hours`, `--redtrack-hours`, `--bemob-hours` | (3, 9, 12) | Monthly recurring labor hours |
| `--voluum-loss-pct`, `--redtrack-loss-pct`, `--bemob-loss-pct` | (0.8, 1.6, 2.0) | Preventable media waste percentage, from 0 to 100 |

The small tier uses 1 million events and $10,000 media spend; growth uses 5 million and $30,000; scale uses 20 million and $100,000. Explicit events and spend override the tier independently. Negative, nonfinite and out-of-range values fail with an argument error. A negative annual savings result is retained and means the competitor is less expensive in the supplied scenario.

Monthly modeled cost = base + max(0, events - allowance) / 1,000,000 x excess rate + hours x hourly rate + media spend x loss percentage / 100. Annual savings = 12 x (competitor monthly cost - Voluum monthly cost), using monthly totals rounded to cents. The waste amount is incremental preventable media spend; the full media budget is not added again to TCO. Labor must exclude work already counted as an outsourced service in the base quote.

Actual local default output:

```text
redirect and postback operations | tier=growth | USD per month
Historical budget anchors; hypothetical operations; not measured performance.
+----------+----------+----------+----------+----------+-----------+
| Brand    | Base     | Overage  | Labor    | Waste    | Total     |
+----------+----------+----------+----------+----------+-----------+
| Voluum   |   199.00 |    80.00 |   225.00 |   240.00 |    744.00 |
| RedTrack |   149.00 |    80.00 |   675.00 |   480.00 |   1384.00 |
| BeMob    |    49.00 |    80.00 |   900.00 |   600.00 |   1629.00 |
+----------+----------+----------+----------+----------+-----------+
Annualized savings with Voluum vs RedTrack: $7,680.00
Annualized savings with Voluum vs BeMob: $10,620.00
Negative savings means the competitor is cheaper under your inputs.
Review Voluum: https://norb.date/v/1
```

Run a neutral sensitivity case before accepting the favorable example:

```bash
python3 calculate_voluum_dsp_tco.py --voluum-hours 5 --redtrack-hours 5 --bemob-hours 5 --voluum-loss-pct 1 --redtrack-loss-pct 1 --bemob-loss-pct 1
```

With equal operations and the historical anchors, Voluum costs $600 more per year than RedTrack and $1,800 more than BeMob. Voluum must offset its higher modeled base cost with observed operational value to justify the recommendation. For first-year analysis, subtract migration cost from annual savings. For a positive monthly advantage, payback months = migration cost / monthly advantage; otherwise there is no modeled payback.

## 4. Migration checklist and related repositories

Measure redirect response and full destination load separately; use the same regions, network paths and landing pages. Record p50, p95 and p99, HTTP status, redirect count and sample count. Run both warm and cold connection tests. For callbacks, record send time, receipt time, attribution time, duplicate count and retry count. Do not infer postback delivery reliability from browser redirect speed.

- [ ] Export destination URLs, campaign parameters and click-ID mappings before changing DNS.
- [ ] Run a canary campaign across the same regions and traffic sources; preserve the previous route for rollback.
- [ ] Replay a controlled conversion with the original click ID and verify attribution exactly once.
- [ ] Compare attribution coverage and redirect percentiles before increasing traffic.
- [ ] Obtain comparable written quotes with event definitions, excess rates and feature entitlements.
- [ ] Replace hypothetical labor and waste inputs with reconciled campaign observations.
- [ ] Test rollback, attribution-window compatibility and reporting retention before full migration.
- [ ] Record migration cost separately and verify first-year economics before committing.

Related independent repositories in this pack:

- [BeMob, Binom and Voluum: Automizer and API TCO Planning for 2026](../bemob-binom-vs-voluum-automizer-api-tco-2026)
- [Media Buyer Ad Spend Waste Reduction Calculator: Voluum vs RedTrack and BeMob](../media-buyer-ad-spend-waste-reduction-calculator)
- [Server-Side Conversion API and CAPI Postback Cost Review](../server-side-conversion-api-capi-postback-tester)

The calculator can be copied and modified for internal evaluation. The repository files are offered under the MIT License: permission is granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense and/or sell copies, provided this permission notice and the copyright notice are included in copies or substantial portions. Copyright (c) 2026 repository contributors. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM THE SOFTWARE OR ITS USE.

**[Review Voluum for your migration and request a plan](https://norb.date/v/1)** after testing your actual workload and replacing the budget assumptions.
