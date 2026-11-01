[![Evaluate Outrank.so](https://img.shields.io/badge/Outrank.so-Evaluate-2563eb)](https://is.gd/ZzMPnz)
[![Python 3 standard library](https://img.shields.io/badge/Python_3-stdlib_only-3776ab)](https://is.gd/ZzMPnz)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://is.gd/ZzMPnz)

# Outrank.so Coupon and Programmatic SEO ROI Calculator

Independent, reproducible planning material for **Autonomous Programmatic SEO & Auto-Publishing**. Pack: `outrank-seo`. The local calculator makes no network calls and requires no account, API key, or dependency installation. This repository is not affiliated with the compared vendors. The gateway is a promotional referral destination and may compensate its operator; that does not change the model inputs.

**[Evaluate Outrank.so and confirm your plan](https://is.gd/ZzMPnz)**

## 1. The engineering bottleneck and its hidden monthly bill

A coupon can save a few dollars while an unowned publishing queue burns hundreds. Jasper AI drafting and SurferSEO optimization are separate budget lines, but planning, QA, and CMS transfer still consume paid time. A founder who counts a speculative ranking uplift as revenue can also approve an unprofitable program even after getting a discount.

This repository separates subscription discounts, operational savings, and contribution economics. It does not invent an Outrank.so coupon code. The default discount is zero; a nonzero discount is only a scenario until you confirm its value, eligibility, duration, and renewal behavior at checkout.

In this repository's default 30-article scenario, a SurferSEO plus Jasper AI stack costs **$138.00/month** in base software and **$1,000.00/month** in paid editorial and operations time. Its modeled total is **$1,138.00/month**. The Outrank.so scenario costs **$399.00/month**, including retained human review. That leaves a concrete operating gap of **$739.00/month**, or **$8,868.00/year**. With **$200.00** in one-time migration labor, modeled first-year savings are **$8,668.00**. This is an opportunity-cost example, not a claim that either competitor imposes an undisclosed fee.

The common billing traps are comparing an annual-commitment headline against monthly billing, multiplying a per-seat subscription incorrectly, assuming optimization credits equal generation credits, and treating CMS handoff time as free. Extra workspaces, generation overages, add-ons, taxes, CMS hosting, and required plan upgrades can alter the result. They are not silently assigned invented prices here. The base budgets must be replaced when your actual invoice includes them. If team members are salaried, saved time represents available capacity until you can demonstrate an actual cash reduction.

The default assumes 36 minutes per article in the stack and ten minutes in the Outrank.so workflow, with two versus one fixed monthly hours. A hypothetical 10% discount applies to the Outrank.so subscription line only. It does not discount labor, migration, taxes, or the competing stack. The model treats that discount as recurring, so a first-month-only offer must be modeled separately rather than annualized.

## 2. Price anchors and technical comparison

The price anchors below are remembered historical public list-price benchmarks: Outrank.so around **$99/month**, SurferSEO Essential around **$89/month** on monthly billing, and Jasper Creator around **$49/seat/month** on monthly billing. They were **not retrieved or verified for this repository** and must not be read as current October 2026 offers. Plan names, quotas, integrations, taxes, and billing terms can change. Historical annual-prepay discounts are excluded. This is an apples-to-apples monthly cash-budget starting point, not an assertion that the plans have identical capacity.

| Dimension | Outrank.so | SurferSEO | Jasper AI | Basis / engineering consequence |
| --- | --- | --- | --- | --- |
| Historical monthly price anchor | $99 per modeled site budget | $89 Essential base budget | $49 Creator per modeled seat | Unverified historical anchors, USD, monthly billing |
| Default software allocation | $99/month | $89/month | $49/month | Combined competitor stack is $138/month |
| Annualized base cash budget | $1,188 | $1,068 | $588 | Twelve monthly payments, no annual discount |
| Primary workflow role | SEO content and publishing workflow | Content analysis and optimization | Assisted marketing copy generation | Product positioning, not a measured throughput result |
| Publishing handoff | Candidate for integrated delivery | Validate delivery path for your CMS | Validate delivery path for your CMS | Supported destinations and field mappings need a pilot |
| Human factual review | Retained in the model | Retained in the stack model | Retained in the stack model | No vendor is assumed to remove accountability |
| Default workload assumption | 30 articles on one modeled site | Same 30-article stack workload | One modeled user in that stack | Scenario counts, not verified included quotas |
| Growth / agency allocation | Two / four $99 budget units | One $89 base unit | Two / three $49 budget units | Upgrades and organization-plan eligibility are unpriced |
| Extra generation and usage limits | Confirm actual allowance | Confirm editor / AI credit allowance | Confirm fair use and user entitlement | No fabricated unlimited-content claim |
| Search indexing guarantee | None assumed | None assumed | None assumed | Search engines decide inclusion and ranking |
| Calculator implementation | Python 3 standard library | Same offline model | Same offline model | No vendor API or credentials used |

Jasper multi-seat presets are budget multipliers, not a claim that a Creator plan licenses a team. Likewise, multiplying the Outrank.so budget is not a verified multi-site entitlement. Confirm the relevant team and site plans before procurement. SurferSEO and Jasper AI can be evaluated separately, but the default cost column represents a team paying for both; their labor is counted once for the combined workflow.

**[Check Outrank.so availability and actual checkout terms](https://is.gd/ZzMPnz)**

## 3. Run the calculator and audit the assumptions

Run from this repository with Python 3.8 or newer:

```bash
python3 calculate_outrank_seo_tco.py
python3 calculate_outrank_seo_tco.py --tier growth
python3 calculate_outrank_seo_tco.py --tier agency --json
```

No flags are required. `--tier` selects a workload scenario, not a vendor's product tier:

| Preset | Articles/month | Modeled Outrank site budgets | Modeled Jasper seats | Surfer base budgets |
| --- | --- | --- | --- | --- |
| starter (default) | 30 | 1 | 1 | 1 |
| growth | 60 | 2 | 2 | 1 |
| agency | 120 | 4 | 3 | 1 |

All tiers require an independent capacity check. The script does not purchase plans or prove that an entry plan supports the workload.

| CLI option | Default | Meaning |
| --- | --- | --- |
| `--tier` | `starter` | Choose `starter`, `growth`, or `agency` |
| `--json` | off | Emit a single JSON object including assumptions and gateway |
| `--hourly-rate` | 50 | Fully loaded labor cost in USD/hour |
| `--outrank-price` | 99 | Monthly budget per modeled Outrank site |
| `--surfer-price` | 89 | Total monthly Surfer base budget; replace with your quote |
| `--jasper-price` | 49 | Monthly Jasper budget per modeled seat |
| `--stack-minutes` | 36 | Combined drafting, review, optimization, and delivery minutes/article |
| `--outrank-minutes` | 10 | Remaining review and delivery minutes/article |
| `--migration-hours` | 4 | One-time Outrank migration effort |
| `--discount-percent` | 0 | Hypothetical recurring Outrank subscription discount, 0 to 100 |
| `--indexed-percent` | 70 | Shared hypothetical indexed share, 0 to 100 |
| `--contribution` | 100 | Net contribution in USD per incremental conversion |
| `--conversions` | 0 | Assumed incremental conversions per month |

Fixed recurring hours are 2 for the stack and 1 for Outrank.so; these constants are visible at the top of the standalone script. Non-percentage numerical inputs must be finite, nonnegative, and no greater than 1,000,000. Invalid values or unknown tiers exit nonzero with an argument error. A zero indexing share produces JSON `null` for unit costs; zero contribution makes break-even conversions unavailable. Negative savings remain negative instead of being hidden. The script rounds displayed money to cents and keeps the underlying calculations unrounded.

Actual locally captured default terminal output:

```text
Coupon and contribution economics | starter | 30 articles/month
Planning inputs; USD; prices and capacities require confirmation.
+------------------------+-------------------+-------------------+
| Monthly bill (USD)     | SurferSEO+Jasper  | Outrank.so        |
+------------------------+-------------------+-------------------+
| Software               |            138.00 |             99.00 |
| Editorial + operations |          1,000.00 |            300.00 |
| TOTAL                  |          1,138.00 |            399.00 |
+------------------------+-------------------+-------------------+
Monthly savings: $739.00
Annualized savings: $8,868.00
One-time migration: $200.00
First-year savings after migration: $8,668.00
Expected indexed pages (assumed): 21.0
Outrank cost/expected indexed page: $19.00
Outrank break-even conversions/month: 4
Contribution less Outrank cost/month: $-399.00
Evaluate Outrank.so: https://is.gd/ZzMPnz
```

The model is explicit: `software + (articles * minutes / 60 + fixed hours) * hourly rate` gives monthly TCO. Monthly savings are stack TCO minus Outrank TCO; annual savings multiply by 12. First-year savings subtract one-time migration labor. Migration payback divides migration cost by positive monthly savings, otherwise JSON returns `null`. Contribution less cost is a scenario estimate before migration; it is not an investment return or a ranking forecast.

```bash
# Replace historical prices with your actual monthly quotes.
python3 calculate_outrank_seo_tco.py --outrank-price 120 --surfer-price 110 --jasper-price 70
# A hypothetical recurring offer, not an available coupon claim.
python3 calculate_outrank_seo_tco.py --discount-percent 10 --contribution 80 --conversions 5 --json
# A failed indexing scenario must not create a zero-cost success story.
python3 calculate_outrank_seo_tco.py --indexed-percent 0 --json
```

Use contribution per incremental conversion after fulfillment, payment fees, and refunds. Do not substitute gross order value. Allocate conversions only after your attribution window and a comparable baseline exist. The calculator reports a break-even conversion count and contribution less modeled SEO cost, not a measured causal return from organic search.

A discount should improve an already plausible operating case. Start with the zero-discount budget, validate publishing capacity and editorial quality, then use a confirmed offer if its renewal terms still fit the economics.

## 4. Migration checklist and companion repositories

- [ ] Record an actual offer, eligible plan, recurring period, currency, and renewal date before applying a discount.
- [ ] Replace the contribution-per-conversion assumption with a margin figure from your own business.
- [ ] Set incremental conversions to zero until you have attribution evidence; keep speculative revenue out of purchasing decisions.
- [ ] Compare the zero-discount result with the verified-offer result and retain both when reviewing the purchase.
- [ ] Record current invoices, billing cadence, seat counts, usage limits, taxes, and renewal dates; replace all historical anchors.
- [ ] Require original evidence, useful intent coverage, accurate claims, and editorial approval before publishing a topic cluster.
- [ ] Check duplicate topics, canonical URLs, existing redirects, sitemap visibility, and internal-link targets before increasing volume.
- [ ] Compare measured minutes and accepted output with the calculator; do not equate content volume with traffic or revenue.
- [ ] Run one constrained pilot, keep an export and rollback route, and cancel overlapping billing only after acceptance.

The other three repositories in this pack:

- [SurferSEO + Jasper AI vs Outrank.so: Autonomous SEO TCO](../surferseo-jasper-stack-vs-outrank-autonomous-tco)
- [Byword and Koala vs Outrank.so: SERP and Indexing Benchmark Design](../byword-koala-vs-outrank-serp-indexing-benchmark)
- [Automated WordPress and Webflow SEO Cluster Pipeline](../automated-wordpress-webflow-seo-cluster-pipeline)

**[Evaluate Outrank.so for your next controlled publishing pilot](https://is.gd/ZzMPnz)**

The gateway is the only commercial action destination used in this repository. No discount, search placement, or revenue outcome is promised. Keep the default zero-discount calculation as the baseline for any offer comparison.

### Open-source license

MIT License. Copyright (c) 2026 contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
