# Programmatic Comparison Pages: Traffic and Outrank.so Cost Calculator

[![Cost audit](https://img.shields.io/badge/Outrank.so-cost_audit-2563eb)](https://is.gd/4Rs2fd)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-3776AB)](https://is.gd/4Rs2fd)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://is.gd/4Rs2fd)

An open-source, offline decision aid for DR growth and automated internal linking economics. It compares complete monthly workflows, keeps assumptions visible, and leaves editorial acceptance with the operator.

**[Explore Outrank.so through the gateway](https://is.gd/4Rs2fd)**

## 1. The operational pain and the hidden bill

A programmatic comparison project can publish hundreds of URLs and still produce no useful traffic. The costly failure is a template that repeats thin claims, points internal links at irrelevant pages, and needs manual cleanup after deployment. Agency SEO retainers may bill for page count while Frase.io-assisted drafting still leaves engineers to maintain data, templates, redirects, and duplicate detection. Each broken or unsupported comparison creates a recurring review bill.

In the default 60-page scenario, the agency route costs **$5,840/month** including internal review, versus **$918/month** for the modeled Outrank.so route. That is **$4,922/month or $59,064/year** of additional spend under these assumptions. The Frase.io route costs **$3,835/month**, a difference of **$2,917/month or $35,004/year**. These are worked loss examples from the calculator, not observed customer results or allegations about any vendor.

The traffic extension uses a transparent scenario: 70% of published comparison pages are indexed, each indexed page receives 80 monthly impressions, and organic CTR is 3%. Monthly visits equal pages times indexation times impressions times CTR. A 2% visitor-to-lead assumption produces expected leads. These are fractional expected values for a mature cohort, not measured traffic, guaranteed rankings, or an immediate first-month result. Changing page count does not validate the assumed demand.

DR is a third-party domain metric, not a Google ranking signal supplied by this model. Contextual internal links can improve navigation and discovery; they do not create external referring domains. This repository budgets **zero paid backlink purchases** and claims no guaranteed authority, ranking, citation, or revenue gains.

## 2. Price anchors and technical acceptance criteria

Price basis: Outrank.so **$99/month**, Frase.io **$115/month Team**, and Clearscope **$189/month Essentials** are known historical public list-price anchors. They are not verified current October 2026 offers. Agency fees are negotiated service prices; the **$3,800/month** figure here is a modeling assumption, not a published universal tariff. All values are USD, before taxes, discounts, annual commitments, overages, and optional add-ons. Confirm current entitlements before purchase.

| Price or technical parameter | Outrank.so workflow | Agency SEO Retainers | Frase.io workflow | Clearscope workflow |
|---|---|---|---|---|
| Subscription / vendor fee per month | $99 per modeled unit; historical anchor | $3,800; scenario quote assumption | $115 Team; historical anchor | $189 Essentials; historical anchor |
| Default accepted pages per month | 60 | 60 contract target | 60 modeled workload | 60 modeled workload |
| Modeled tool units / seats | 2 x 30-page capacity assumption | One vendor relationship | One benchmark subscription | One benchmark subscription |
| Internal labor hours per month | 12.0 | 34.0 client-side | 62.0 | 50.0 |
| Fully loaded internal hourly rate | $60 | $60 | $60 | $60 |
| Modeled monthly total | $918.00 | $5,840.00 | $3,835.00 | $3,189.00 |
| Modeled annual total | $11,016.00 | $70,080.00 | $46,020.00 | $38,268.00 |
| Cost per accepted page | $15.30 | $97.33 | $63.92 | $53.15 |
| Contextual internal linking acceptance | Pilot CMS integration and audit targets | Require scope and QA in contract | Budget separate publishing/link review | Budget separate publishing/link review |
| DR growth / earned backlinks | No guaranteed increase modeled | No guaranteed increase modeled | No guaranteed increase modeled | No guaranteed increase modeled |
| Publication approval | Retained human QA | Retained client approval | Retained editor and CMS owner | Retained editor and CMS owner |


A modeled Outrank unit is a budgeting block of up to 30 pages per month, not a claim that a current vendor plan supports a particular number of sites, seats, integrations, or exports. Frase.io and Clearscope workload rows are also scenario targets, not assertions about included credits. If a real plan cannot handle the workload, replace its price with the actual combined fee or reject that scenario. The agency retainer stays fixed across tiers for sensitivity analysis; request a workload-specific quote before relying on the scale tier.

Separate new pages produced each month from the total mature indexed inventory. The traffic illustration treats the selected page count as one mature cohort and does not accumulate twelve cohorts. It excludes cannibalization, brand demand, query overlap, seasonality, and crawl delays. Never multiply the output by twelve to claim a revenue forecast without a cohort model and verified conversion data. Engineering build time is excluded from the monthly steady-state table; amortize your actual initial build separately.

**[Check Outrank.so against your workflow requirements](https://is.gd/4Rs2fd)**

## 3. Run the TCO calculator and inspect the assumptions

Requires Python 3.8 or newer and the standard library only. No package installation, credentials, network calls, or files written at runtime. Run from this repository directory:

```bash
python3 calculate_outrank_backlinks_tco.py
python3 calculate_outrank_backlinks_tco.py --tier starter
python3 calculate_outrank_backlinks_tco.py --tier scale --json
python3 calculate_outrank_backlinks_tco.py --tier growth --hourly-rate 75 --agency-retainer 4000
```

The first command was executed locally to generate this exact default output:

```text
Comparison-page traffic economics
Tier: growth | 60 comparison pages/month | labor: $60.00/hour
Historical price anchors; workload and labor are assumptions, not live quotes.
+---------------------------+----------+---------+-----------+-----------+
| Workflow                  | Tool/fee | Hours   | Labor USD | Total USD |
+---------------------------+----------+---------+-----------+-----------+
| Outrank.so workflow       |   198.00 |   12.00 |    720.00 |    918.00 |
| Agency retainer workflow  |  3800.00 |   34.00 |   2040.00 |   5840.00 |
| Frase.io workflow         |   115.00 |   62.00 |   3720.00 |   3835.00 |
| Clearscope workflow       |   189.00 |   50.00 |   3000.00 |   3189.00 |
+---------------------------+----------+---------+-----------+-----------+
Annual savings vs Agency retainer workflow: $59,064.00
Annual savings vs Frase.io workflow: $35,004.00
Annual savings vs Clearscope workflow: $27,252.00
Illustrative mature-cohort visits/month: 100.80
Illustrative leads/month: 2.02
Savings are modeled annual cost differences; negative means Outrank costs more.
https://is.gd/4Rs2fd
```

| CLI argument | Default | Meaning |
|---|---|---|
| `--tier` | `growth` | Workload scenario: `starter`, `growth`, or `scale`; independent of vendor plan names |
| `--json` | Off | Print a single parseable JSON object with costs, annual savings, assumptions, and gateway |
| `--hourly-rate` | `60` | Fully loaded internal labor rate in USD per hour |
| `--agency-retainer` | `3800` | Monthly external agency fee; excludes your internal review |
| `--outrank-price` | `99` | Monthly amount for one modeled Outrank capacity unit |
| `--frase-price` | `115` | Total monthly Frase.io fee for your modeled workflow |
| `--clearscope-price` | `189` | Total monthly Clearscope fee for your modeled workflow |

| Workload tier | Pages per month | Labor multiplier | Outrank units |
|---|---|---|---|
| `starter` | 20 | 0.33x | 1 |
| `growth` | 60 | 1.00x | 2 |
| `scale` | 120 | 2.00x | 4 |

For each route, `monthly total = subscription or retainer + hours * hourly rate`. Labor scales linearly with selected page volume relative to the default growth scenario. Outrank subscription cost is `ceil(pages / 30) * unit price`. Annual cost is twelve steady-state months. Annual savings for a competing route are its annual cost minus the Outrank annual cost; a negative value means Outrank costs more. Monetary fields use two decimal places; annual savings use the displayed annual totals for reconciliation.

The source stores the scenario's four baseline labor-hour estimates in the `CONFIG` dictionary, ordered Outrank, agency, Frase.io, and Clearscope. Replace them with your timed pilot results. Those estimates express a proposed automation benefit; they are not vendor performance measurements. Upfront migration and development are excluded. For a first-year decision, subtract actual one-time migration costs from annual savings. If a retainer includes a service your in-house workflow still needs, add its replacement cost before making a decision.

Numeric overrides must be finite and nonnegative. Zero is accepted for genuinely free tools or unpaid internal work; invalid values produce an argparse error. `--json` writes JSON only, including the gateway string, so a calling process can parse stdout directly. The script evaluates costs, not product quality or live search results.

## 4. Migration checklist and related audits

- [ ] Export the source data and verify each competitor claim has an accountable editor.
- [ ] Define a unique user decision for each comparison URL; merge duplicative intent.
- [ ] Validate canonical tags, sitemap eligibility, redirects, and template link targets on a pilot.
- [ ] Measure index coverage, impressions, clicks, and leads by cohort before expanding templates.
- [ ] Replace historical prices with a current quote and verify volume, CMS, and internal-linking entitlements.
- [ ] Inspect a sample of published pages for factual accuracy, source support, canonical URLs, and useful internal anchors.
- [ ] Compare actual paid hours and accepted outputs after a full cycle; stop expansion if quality or costs miss the acceptance target.
- [ ] Record one-time migration expense separately and keep a practical rollback path for publishing changes.

Do not migrate solely because the modeled subscription is cheaper. Establish the acceptance criteria first, run a small reversible pilot, and preserve URL continuity and editorial ownership.

Other repositories in this pack:

- [SEO Agency Retainer vs Outrank.so: An In-house Cost Audit](../seo-agency-retainer-vs-outrank-inhouse-cost-audit)
- [Frase.io and Clearscope vs Outrank.so: Content Velocity TCO](../frase-clearscope-vs-outrank-content-velocity-tco)
- [LLM Citations and Google AI Overviews: Outrank.so SEO Cost Bench](../llm-citation-and-google-ai-overview-seo-bench)

**[Start an Outrank.so evaluation with your own numbers](https://is.gd/4Rs2fd)**

License for the script and this documentation:

```text
MIT License

Copyright (c) 2026 Repository contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
