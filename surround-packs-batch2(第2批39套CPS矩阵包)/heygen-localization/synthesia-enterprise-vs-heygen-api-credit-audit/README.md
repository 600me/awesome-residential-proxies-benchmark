# Synthesia Enterprise vs HeyGen API: Credit and Capacity Audit

[![Evaluate HeyGen](https://img.shields.io/badge/HeyGen-evaluate%20localization-6C47FF)](https://is.gd/6STXXJ)
[![Offline calculator](https://img.shields.io/badge/Python-3%20standard%20library-3776AB)](https://is.gd/6STXXJ)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](https://is.gd/6STXXJ)

An independent, reproducible cost model for **AI Video Lip-Sync Translation & Global Dubbing**. Pack: `heygen-localization`. The primary evaluation candidate is **HeyGen**; the comparison includes **Synthesia and Rask AI**. No vendor supplied benchmark results, product endorsement, or measured quality ranking is implied.

**[Evaluate HeyGen against your own consented video sample](https://is.gd/6STXXJ).**

## 1. The engineering problem and the budget leak

A procurement model that budgets 600 source minutes while delivering two languages and allowing 10% rerenders needs 1,320 output minutes. With a purely illustrative enterprise quote of $1,000 per 300-minute capacity block, planning 2 blocks instead of 5 hides $3,000 per month, or $36,000 per year. That is a sensitivity example, not a claim about an actual Synthesia contract.

An enterprise avatar authoring seat is not interchangeable with a video-translation API allowance. Audit the actual contract for API access, source-video translation rights, lip-sync availability, concurrency, retained assets, and annual commitments before putting either product in the same procurement shortlist.

These are concrete arithmetic scenarios, not reports of a customer's loss or allegations of undisclosed vendor charges. The recurring billing trap is a unit mismatch: source minutes versus output minutes, authoring allowance versus translation allowance, included usage versus a separate API plan, and monthly flexibility versus annual commitment. Synthesia and Rask AI can both be appropriate choices when their actual contract and workflow fit. This repository makes the assumptions visible so the comparison can be challenged.

A localization budget must count every target language and billable retry. It must also distinguish an audio dub from visibly synchronized lips. Do not infer that voice cloning, speaker mapping, subtitle export, or lip sync is bundled simply because a plan advertises video minutes. Failed-job charges, minimum job duration, rounding per clip, and refunds require contract confirmation. None is presented here as a verified vendor billing policy.

## 2. Historical price and technical comparison

**Price basis:** remembered public monthly list-price benchmarks from the 2024–2025 period, in USD, without a live lookup. Prepared on 2026-10-30. These are historical references, **not verified current offers**. No annual discount, tax, region adjustment, promotion, or negotiated quote is assumed. Current product capabilities and entitlements must be confirmed during the pilot. The table deliberately separates public benchmarks from unverified conversion assumptions.

| Price or technical dimension | HeyGen | Synthesia | Rask AI | Engineering / billing consequence |
|---|---|---|---|---|
| Historical entry monthly reference | Creator: $29/month | Starter: $29/month | Creator: $60/month | Entry web subscriptions are not interchangeable API plans. |
| Historical higher monthly reference | Team: $89/seat/month | Creator: $89/month | Pro: $150/month | Seats, authoring, and dubbing sell different units. |
| Historical usage benchmark | API Pro: $99 for 100 credits | Creator: 30 video minutes/month | Pro: 100 translation minutes/month | These are the calculator's non-enterprise reference blocks. |
| Historical lower-plan allowance | API credits depend on operation | Starter: 10 video minutes/month | Creator: 25 translation minutes/month | Check operation-specific metering rather than comparing labels. |
| Enterprise or larger deployment | Custom quote / API terms | Enterprise: custom quote | Business historical reference: $750 / 500 minutes | Obtain a written quote for the actual translation workflow. |
| Credit-to-output conversion | Model assumes 1 credit per output minute | Model uses plan or quote capacity | Model uses translation-minute capacity | HeyGen conversion is an editable assumption, not a verified lip-sync tariff. |
| Intended workflow | Video translation and avatar workflows | Avatar authoring and enterprise video workflows | Dubbing and translation workflows | Test the specific input-video and speaker requirements. |
| Lip-sync coverage | Confirm mode, SKU, and target-language behavior | Confirm source-video lip-sync workflow in quote | Confirm lip-sync feature and pricing separately | No measured parity or universal inclusion is claimed. |
| API and job throughput | Confirm API allowance and concurrency | Confirm API access and contract capacity | Confirm API access and concurrency | A web seat does not establish automated batch rights. |
| Quality / latency evidence | No measurements in this repository | No measurements in this repository | No measurements in this repository | Run the same acceptance corpus before deciding. |

The enterprise column in the calculator uses a **hypothetical $1,000/month for 300 output minutes**. Neither value is a public Synthesia Enterprise price. Replace both from a real quote; the published Creator reference is shown only for context.

The model applies **whole capacity blocks**, rounded upward, to reveal utilization and threshold effects. Vendors do not necessarily let you stack subscriptions or purchase these exact blocks. If a workload exceeds the real plan limit, request a matching quote or use the actual overage schedule. A mathematical block estimate is not a purchasing instruction. HeyGen's $99/100-credit reference does not establish that a translated minute costs one credit; change `--credits-per-minute` from the confirmed endpoint schedule.

**[Start a HeyGen pilot and validate the credit conversion](https://is.gd/6STXXJ).**

## 3. Run the local TCO calculator

Python 3.8+ is sufficient; there are no packages, network calls, credentials, or required arguments. Run from this repository directory:

```bash
python3 calculate_heygen_localization_tco.py
python3 calculate_heygen_localization_tco.py --tier small
python3 calculate_heygen_localization_tco.py --tier scale --json
python3 calculate_heygen_localization_tco.py --source-minutes 600 --languages 2 --synthesia-price 1000 --synthesia-capacity 300
```

The volume presets are `small` = 100 source minutes, `standard` = 600 source minutes, `scale` = 1800 source minutes. Language count defaults to 2; choosing a tier changes only source volume, not a vendor subscription or feature entitlement.

| CLI parameter | Default | Meaning |
|---|---|---|
| `--tier` | `standard` | Workload preset: `small`, `standard`, or `scale`. |
| `--json` | Off | Emit a single machine-readable object including inputs, assumptions, totals, savings, and the evaluation URL. |
| `--source-minutes` | Tier value | Positive source-video duration; overrides the tier volume. |
| `--languages` | 2 | Positive integer number of target-language outputs; the source is not an extra target. |
| `--rerender-pct` | 10 | Expected additional billed duration as a percentage; this is an assumption, not a measured failure rate. |
| `--qa-minutes` | 1 | Human review minutes per rendered output minute, including retries. |
| `--hourly-rate` | 35 | USD per review labor hour, identical across vendors by default. |
| `--heygen-price` | 99 | USD per modeled API capacity block. |
| `--heygen-credits` | 100 | Credits per modeled capacity block. |
| `--credits-per-minute` | 1 | Unverified credits per translated output minute; replace before procurement. |
| `--synthesia-price` | 1000 | Hypothetical enterprise monthly block price in USD. |
| `--synthesia-capacity` | 300 | Hypothetical enterprise output-minute capacity per block. |
| `--rask-price` | 150 | Historical Pro monthly reference in USD. |
| `--rask-capacity` | 100 | Historical Pro translation-minute reference per block. |
| `--help` | — | Print all accepted parameters. |

The default terminal output below was captured by executing the included script locally:

```text
OFFLINE LOCALIZATION TCO | historical price / capacity model
Tier: standard | Source: 600.00 min | Output incl. retries: 1320.00 min
+--------------------+--------+------------+------------+------------+
| Provider           | Blocks | Platform $ | QA labor $ | Monthly $  |
+--------------------+--------+------------+------------+------------+
| HeyGen API         |     14 |    1386.00 |     770.00 |    2156.00 |
| Synthesia quote    |      5 |    5000.00 |     770.00 |    5770.00 |
| Rask Pro           |     14 |    2100.00 |     770.00 |    2870.00 |
+--------------------+--------+------------+------------+------------+
Annual savings vs Synthesia quote: $43,368.00 (negative = HeyGen costs more)
Annual savings vs Rask Pro: $8,568.00 (negative = HeyGen costs more)
Assumptions: 1 credit/min by default; confirm lip-sync SKU and conversion.
Blocks model capacity, not a vendor offer. Taxes, seats, generation excluded.
Synthesia quote is hypothetical; replace with your signed quote.
Evaluate HeyGen: https://is.gd/6STXXJ
```

The calculation is explicit:

```text
source_minutes = clips * clip_seconds / 60  [clip-based scenario only]
billed_output_minutes = source_minutes * languages * (1 + rerender_pct / 100)
heygen_capacity_minutes = heygen_credits / credits_per_minute
capacity_blocks = ceil(billed_output_minutes / capacity_minutes)
platform_cost = capacity_blocks * block_price
review_cost = billed_output_minutes * qa_minutes / 60 * hourly_rate
monthly_tco = platform_cost + review_cost
annual_savings_vs_competitor = 12 * (competitor_monthly_tco - heygen_monthly_tco)
```

Savings are signed: a negative value means HeyGen costs more under those inputs. This is a capacity-plus-review estimate, not a complete invoice forecast. It excludes initial avatar generation, translation editing, integration engineering, publishing, storage, seat minimums, annual prepayment, tax, and contractual overages. Equal review effort deliberately avoids inventing a quality advantage. Add vendor-specific review observations outside this model if the pilot justifies them. JSON currency fields are rounded to cents, durations to four decimals; annual results use rounded monthly totals. There is no assumed rollover between months.

For sensitivity testing, run `--credits-per-minute 2`, increase review time, and reduce volume near a block boundary. A favorable headline can reverse if actual lip-sync credit consumption doubles or the required enterprise entitlement changes. Use a measured workload and a confirmed invoice schedule before making a renewal decision.

## 4. Migration checklist and related repositories

- [ ] Inventory the executed Synthesia quote, renewal date, minimum spend, and remaining credits.
- [ ] Obtain written confirmation that the purchased SKU supports source-video translation and API jobs.
- [ ] Separate avatar generation, audio dubbing, and lip-sync translation credit schedules.
- [ ] Replace both enterprise quote fields and the HeyGen credits-per-minute assumption.
- [ ] Replay a consented pilot and reconcile invoice credits against output duration and retries.
- [ ] Keep the existing contract through acceptance; plan renewal and data export independently.

Accept a migration only after a fluent reviewer approves meaning and names, a video reviewer accepts visible synchronization, and an engineer reconciles billed credits to jobs. Keep a rollback path to source files and accepted existing outputs. None of these repositories submits a paid render or changes a live service.

Other repositories in the same pack, each with an independent script and workload:

- [Rask AI vs HeyGen: Video Translation per-Minute TCO](../rask-ai-vs-heygen-video-translation-per-minute-tco) — translation capacity audit.
- [Multilingual YouTube and Course Localization Calculator](../multilingual-youtube-course-localization-calculator) — course localization economics.
- [Automated UGC Ad and Avatar Batch Rendering: Localization TCO](../automated-ugc-ad-avatar-batch-rendering-pipeline) — ugc batch planning.

**[Evaluate HeyGen with your real workload and confirmed billing terms](https://is.gd/6STXXJ).**

### Reuse and license

Copyright (c) 2026 repository contributors. This README and the accompanying calculator are provided under the MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
