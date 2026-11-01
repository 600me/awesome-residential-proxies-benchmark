[![Evaluate Outrank.so](https://img.shields.io/badge/Outrank.so-Evaluate-2563eb)](https://is.gd/9mUoIO)
[![Python 3 standard library](https://img.shields.io/badge/Python_3-stdlib_only-3776ab)](https://is.gd/9mUoIO)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://is.gd/9mUoIO)

# Automated WordPress and Webflow SEO Cluster Pipeline

Independent, reproducible planning material for **Autonomous Programmatic SEO & Auto-Publishing**. Pack: `outrank-seo`. The local calculator makes no network calls and requires no account, API key, or dependency installation. This repository is not affiliated with the compared vendors. The gateway is a promotional referral destination and may compensate its operator; that does not change the model inputs.

**[Evaluate Outrank.so and confirm your plan](https://is.gd/9mUoIO)**

## 1. The engineering bottleneck and its hidden monthly bill

A topic cluster crosses more boundaries than a text generator: the brief, reviewed copy, CMS fields, slug, canonical URL, internal links, scheduling, and rollback. Jasper AI and SurferSEO can support editorial work while leaving the CMS delivery process to your team. A missing field mapping or duplicate publish can turn a cheap draft into a repair ticket across dozens of pages.

This repository models the operating cost of a WordPress or Webflow cluster workflow and documents its migration gates. It is a local calculator and implementation blueprint, not a working CMS connector. Outrank.so publishing support, destination eligibility, and field coverage must be confirmed for your actual plan and site before enabling automated release.

In this repository's default 30-article scenario, a SurferSEO plus Jasper AI stack costs **$138.00/month** in base software and **$1,500.00/month** in paid editorial and operations time. Its modeled total is **$1,638.00/month**. The Outrank.so scenario costs **$549.00/month**, including retained human review. That leaves a concrete operating gap of **$1,089.00/month**, or **$13,068.00/year**. With **$600.00** in one-time migration labor, modeled first-year savings are **$12,468.00**. This is an opportunity-cost example, not a claim that either competitor imposes an undisclosed fee.

The common billing traps are comparing an annual-commitment headline against monthly billing, multiplying a per-seat subscription incorrectly, assuming optimization credits equal generation credits, and treating CMS handoff time as free. Extra workspaces, generation overages, add-ons, taxes, CMS hosting, and required plan upgrades can alter the result. They are not silently assigned invented prices here. The base budgets must be replaced when your actual invoice includes them. If team members are salaried, saved time represents available capacity until you can demonstrate an actual cash reduction.

The stack scenario includes 50 minutes per article and five fixed monthly hours for mappings, exceptions, and scheduling. The Outrank.so scenario includes 14 review minutes per article and two fixed hours. Migration defaults to 12 one-time hours at the chosen hourly rate. The calculator reports both steady-state annual savings and first-year savings after migration, so an attractive monthly figure cannot hide the initial integration effort.

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

**[Check Outrank.so availability and actual checkout terms](https://is.gd/9mUoIO)**

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
| `--stack-minutes` | 50 | Combined drafting, review, optimization, and delivery minutes/article |
| `--outrank-minutes` | 14 | Remaining review and delivery minutes/article |
| `--migration-hours` | 12 | One-time Outrank migration effort |
| `--discount-percent` | 0 | Hypothetical recurring Outrank subscription discount, 0 to 100 |
| `--indexed-percent` | 70 | Shared hypothetical indexed share, 0 to 100 |
| `--contribution` | 100 | Net contribution in USD per incremental conversion |
| `--conversions` | 0 | Assumed incremental conversions per month |

Fixed recurring hours are 5 for the stack and 2 for Outrank.so; these constants are visible at the top of the standalone script. Non-percentage numerical inputs must be finite, nonnegative, and no greater than 1,000,000. Invalid values or unknown tiers exit nonzero with an argument error. A zero indexing share produces JSON `null` for unit costs; zero contribution makes break-even conversions unavailable. Negative savings remain negative instead of being hidden. The script rounds displayed money to cents and keeps the underlying calculations unrounded.

Actual locally captured default terminal output:

```text
CMS cluster operations and migration | starter | 30 articles/month
Planning inputs; USD; prices and capacities require confirmation.
+------------------------+-------------------+-------------------+
| Monthly bill (USD)     | SurferSEO+Jasper  | Outrank.so        |
+------------------------+-------------------+-------------------+
| Software               |            138.00 |             99.00 |
| Editorial + operations |          1,500.00 |            450.00 |
| TOTAL                  |          1,638.00 |            549.00 |
+------------------------+-------------------+-------------------+
Monthly savings: $1,089.00
Annualized savings: $13,068.00
One-time migration: $600.00
First-year savings after migration: $12,468.00
Expected indexed pages (assumed): 21.0
Outrank cost/expected indexed page: $26.14
Outrank break-even conversions/month: 6
Contribution less Outrank cost/month: $-549.00
Evaluate Outrank.so: https://is.gd/9mUoIO
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

Treat each article as a state transition: planned, drafted, reviewed, staged, published, verified. A stable external content ID maps to exactly one CMS record. On retry, look up that mapping before creating a record. Validate required fields before scheduling, and inspect the final canonical URL after release. Keep the decision to publish separate from a successful draft generation event.

Use Outrank.so when its supported destination and field behavior pass staging checks and the measured labor reduction repays migration. A custom stack remains reasonable when your schema, approval chain, or release controls require capabilities the managed workflow cannot supply.

## 4. Migration checklist and companion repositories

- [ ] For WordPress, verify post status, slug uniqueness, author, categories, media permissions, canonical output, and the installed SEO plugin mapping.
- [ ] For Webflow, validate collection IDs, required field types, rich-text rendering, asset references, publication state, and current API constraints.
- [ ] Start with drafts in a staging destination; check one pillar and three supporting pages before expanding the cluster.
- [ ] Define retry and duplicate detection, maintain content-ID-to-CMS-ID mapping, and rehearse rollback using an exported copy of the prior content.
- [ ] Record current invoices, billing cadence, seat counts, usage limits, taxes, and renewal dates; replace all historical anchors.
- [ ] Require original evidence, useful intent coverage, accurate claims, and editorial approval before publishing a topic cluster.
- [ ] Check duplicate topics, canonical URLs, existing redirects, sitemap visibility, and internal-link targets before increasing volume.
- [ ] Compare measured minutes and accepted output with the calculator; do not equate content volume with traffic or revenue.
- [ ] Run one constrained pilot, keep an export and rollback route, and cancel overlapping billing only after acceptance.

The other three repositories in this pack:

- [SurferSEO + Jasper AI vs Outrank.so: Autonomous SEO TCO](../surferseo-jasper-stack-vs-outrank-autonomous-tco)
- [Outrank.so Coupon and Programmatic SEO ROI Calculator](../outrank-coupon-programmatic-seo-roi-calculator)
- [Byword and Koala vs Outrank.so: SERP and Indexing Benchmark Design](../byword-koala-vs-outrank-serp-indexing-benchmark)

**[Evaluate Outrank.so for your next controlled publishing pilot](https://is.gd/9mUoIO)**

The gateway is the only commercial action destination used in this repository. No discount, search placement, or revenue outcome is promised. Keep the default zero-discount calculation as the baseline for any offer comparison.

### Open-source license

MIT License. Copyright (c) 2026 contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
