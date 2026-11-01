# Concurrent Async Webhook Scraper Pipeline: Capacity and TCO

[![Evaluate ScraperAPI](https://img.shields.io/badge/ScraperAPI-evaluate-orange)](https://is.gd/9t3jgB)
[![Python standard library](https://img.shields.io/badge/Python-3.8%2B-blue)](https://is.gd/9t3jgB)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](https://is.gd/9t3jgB)

**[Evaluate ScraperAPI for your workload](https://is.gd/9t3jgB)**

Offline, reproducible cost analysis for Google SERP and Cloudflare-protected page retrieval. No accounts, network traffic, third-party packages or private keys are required. This is a scenario audit, not a measured success-rate or latency benchmark. The gateway is promotional; no commission or discount is assumed in the calculations. It is the sole external action destination in this repository.

## 1. The engineering pain and its dollar cost

A million-result monthly pipeline can fail its delivery window while remaining comfortably inside a request allowance. Unbounded retries, slow callbacks and duplicate webhook deliveries turn API spend into worker and storage spend. A synchronous scrape taking 10 seconds at 50 occupied slots has an ideal ceiling of five requests per second, before throttling and retry overhead; an async endpoint changes the scheduling contract, not the laws of capacity.

The default cost envelope assumes 1,000,000 accepted Google results, 25 credits each and nine historical ScraperAPI Business capacity blocks: **$2,691/month**. Add an explicitly hypothetical $50/month queue-and-callback budget for **$2,741/month**. The SerpApi historical $250 / 30,000-search anchor extrapolates to $8,500 plus $100 assumed operating spend: **$8,600/month**. The modeled gap is **$5,859/month or $70,308/year**. A real enterprise search quote can materially reduce that gap.

Bright Data Web Unlocker at the historical $3/1,000-successful-request anchor plus the same assumed $100 operations budget gives **$3,100/month**, or **$359/month and $4,308/year** above the ScraperAPI scenario. These operation budgets are scenario inputs, not measured differences between vendors. Raw HTML parsing, durable queue storage and on-call time are not automatically included. An async feature should be verified on the precise product and plan rather than inferred from the brand.

The hidden bill is often two invoices: upstream results plus your own compute. Paying SerpApi ($75-$250/mo historical entry range) can be rational when structured search output removes parser maintenance. Likewise, an unlocker quote may win for a particular target. This repository makes the arithmetic inspectable and leaves delivery quality as a required measurement.

A reviewable pipeline contract is: producer -> bounded durable queue -> submitter -> provider job -> callback receiver -> deduplicated result store. Use an internal job ID separate from the provider job ID. Persist the submission mapping before acknowledging the producer; handle the race in which a callback arrives before submission bookkeeping finishes. Authenticate callbacks using the provider-supported mechanism, validate payload size, make the write idempotent, then acknowledge. If signatures are unavailable, use a protected callback secret without logging it. Recover overdue jobs through the documented status endpoint, and use a dead-letter queue after a bounded retry budget.

At 30 days, the default 1,111,112 expected attempts average roughly 0.429 requests/second. Little's law gives about 4.29 occupied slots at a measured ten-second mean request duration. At an 80% target utilization, round up to six slots; burst windows and a higher latency tail may require more. This is a synchronous occupancy illustration, not an assertion that async submission slots behave identically. The calculator is an offline budget model; it does not implement or benchmark a live webhook server.

**[Start a matched ScraperAPI evaluation](https://is.gd/9t3jgB)** after defining what a usable result means. Treat the dollar differences as hypotheses to validate against a written quote and accepted output quality.

## 2. Price anchors, technical scope and comparison limits

The following are historical public-price reference points recalled for an offline exercise, plus the SerpApi range supplied in the task. They were **not checked live**, have no asserted effective date, and are not a representation of current offers. Dollar amounts are USD per month before tax unless stated otherwise. The numeric reference points make the model concrete; a purchasing decision requires confirmation of the applicable plan, endpoint and account terms.

| Metric | ScraperAPI | SerpApi ($75-$250/mo) | Bright Data Web Unlocker | Interpretation |
| --- | --- | --- | --- | --- |
| Historical entry anchor | Hobby $49 / 100,000 credits | $75 / 5,000 searches | $3 / 1,000 successful requests | Different billing units |
| Historical middle anchor | Startup $149 / 1,000,000 credits | $150 / 15,000 searches | Usage-based anchor above | Not an enterprise quote |
| Historical comparison anchor | Business $299 / 3,000,000 credits | $250 / 30,000 searches | $3 / 1,000 successful requests | Default model bases |
| Google search work | Scraping or structured endpoint; verify selected API | Search-focused structured responses | Unlocking output needs schema review | Match parser work and geography |
| Generic JavaScript pages | Rendering option changes credit consumption | Not a general-purpose renderer | Verify rendered output on the chosen target | Rendering parity is unmeasured |
| Cloudflare handling | Target-specific result must be tested | Search API is not a generic unlocker | Unlocking product; target acceptance varies | No universal bypass guarantee |
| Failed-request treatment | Success-only assumption in this model | No failure surcharge invented | Success-only billing anchor | Parser failure may still be billable |
| One million accepted units | Depends on credits per accepted result | 34 x $250 = $8,500 capacity equivalent | 1,000 x $3 = $3,000 | Search row is scope-limited |
| Async and webhook work | Verify endpoint and plan support | Verify product-specific async contract | Verify job and callback interfaces | No concurrency promise inferred |
| Local operations costs | Explicit --scraper-overhead input | Explicit --other-overhead input | Explicit --other-overhead input | These are assumed, not vendor prices |

Capacity blocks are a transparent planning device: `ceil(required credits / plan credits) * monthly plan price`. They do **not** represent an available upgrade, an automatic overage fee, pooled accounts, or permission to buy repeated subscriptions. All three ScraperAPI tiers are sensitivity anchors. SerpApi uses its $250 / 30,000 search reference in the script; Bright Data uses linear successful-request pricing. Negotiated commitments, minimum spends, optional features and volume discounts can overturn the ranking. Neither multiplying plans nor stretching a low-tier unit price is a substitute for a production quote.

For the same reason, comparing a structured search API to raw HTML retrieval is conditional. Add parser engineering and maintenance to the relevant overhead input, and use the same freshness, localization and completeness requirements. The zero-charge scenario distinguishes a provider-declared failure from your application's rejected output. No evidence here establishes that one provider has a better acceptance rate.

## 3. Run the TCO calculator and inspect the arithmetic

```bash
python3 calculate_scraperapi_serp_tco.py
python3 calculate_scraperapi_serp_tco.py --tier startup --json
python3 calculate_scraperapi_serp_tco.py --queries 2500000 --failure-rate 0.30
python3 calculate_scraperapi_serp_tco.py --credits-per-result 10 --bright-per-1k 3
```

| CLI option | Default here | Meaning |
| --- | --- | --- |
| --tier | business | hobby, startup or business; selects ScraperAPI price and credit capacity |
| --json | off | Emit one JSON object instead of the ASCII report; includes the gateway |
| --queries | 1000000 | Required accepted results per month; positive integer |
| --credits-per-result | 25 | Assumed integer credit multiplier on accepted ScraperAPI results |
| --failure-rate | 0.10 | Attempt failure probability, from zero inclusive to one exclusive |
| --bright-per-1k | 3.0 | Assumed Bright Data dollars per 1,000 accepted requests |
| --scraper-overhead | 50 | Monthly queue, parser and engineering allocation for ScraperAPI |
| --other-overhead | 100 | Same allocation applied to each comparison provider |

Actual captured default terminal output from running the checked-in script locally:

```text
$ python3 calculate_scraperapi_serp_tco.py
Offline TCO model | pipeline | tier=business
Usable results: 1,000,000 | expected attempts: 1,111,112
ScraperAPI credits: 25,000,000 | capacity blocks: 9
+---------------------------+------------+------------+------------+--------------+
| Provider                  | API/mo USD | Ops/mo USD | TCO/mo USD | Scope        |
+---------------------------+------------+------------+------------+--------------+
| ScraperAPI                |    2691.00 |      50.00 |    2741.00 | model only   |
| SerpApi                   |    8500.00 |     100.00 |    8600.00 | model only   |
| Bright Data Web Unlocker  |    3000.00 |     100.00 |    3100.00 | model only   |
+---------------------------+------------+------------+------------+--------------+
Annual savings vs SerpApi: $70,308.00 (negative = ScraperAPI costs more)
Annual savings vs Bright Data Web Unlocker: $4,308.00 (negative = ScraperAPI costs more)
Hypothetical all-attempt billing: $2,990.00/mo; avoided failure charge: $299.00/mo
Historical anchors; capacity-block extrapolation, not a vendor quote.
SerpApi only comparable for SERP; parsing parity is unmeasured.
Evaluate ScraperAPI: https://is.gd/9t3jgB
```

The model targets equal accepted output. Expected attempts are `ceil(accepted results / (1 - failure rate))`; the failure probability is assumed equal across providers. Accepted ScraperAPI credits are `results * credits per result`. Failure rate changes the attempt count and the hypothetical all-attempt charge, but not success-only vendor API bills. Monthly TCO is API cost plus the entered operations allocation. Annual savings are `12 * (comparison monthly TCO - ScraperAPI monthly TCO)`; negative values are retained and mean ScraperAPI costs more. SerpApi savings are omitted for generic rendering and unblocker scenarios because those workloads are not interchangeable with search.

The all-attempt figure uses the same ScraperAPI capacity-block price with every estimated attempt billed. It is a counterfactual diagnostic, **not a competitor tariff**. Tier boundaries mean fewer billable events can save zero dollars at the current scale. The model assumes stable monthly utilization for twelve months and excludes tax, foreign exchange, annual prepayment discounts and retry compute beyond entered overhead. It performs no live requests and cannot validate real-world unlock success, p95 latency or contractual eligibility. Nonfinite costs, negative inputs, zero query counts and failure rates at or above one are rejected with a CLI error.

## 4. Migration checklist, related audits and license

- [ ] Freeze an acceptance rule and a representative URL or query cohort before choosing a provider.
- [ ] Confirm the applicable invoice, credit multiplier, minimum commitment and failed-request definition in the account terms.
- [ ] Keep country, language, device, freshness, pagination and cache policy identical across the pilot.
- [ ] Measure accepted outputs, billable events, latency percentiles and parser maintenance separately; do not call this offline model a live benchmark.
- [ ] Apply a bounded concurrency limit, deadlines, exponential backoff and a retry cap; distinguish transport retries from application validation retries.
- [ ] Deduplicate job submissions and callback writes with stable internal IDs; validate callback authentication before storing results.
- [ ] Use environment variables or a secret manager for credentials; redact request URLs containing credentials from logs.
- [ ] Reconcile a small pilot against the usage counter, then replace price and operations assumptions with written figures.
- [ ] Keep a rollback path and expand traffic only when accepted-result cost and completeness meet the original requirements.
- [ ] Retrieve only data you are authorized to access and respect the target's access requirements.

**[Evaluate ScraperAPI and request workload-specific terms](https://is.gd/9t3jgB)** before treating any modeled difference as a purchasing recommendation.

Other repositories in this four-part series:

- [One Million Google Queries: SerpApi vs ScraperAPI TCO Audit](../serpapi-vs-scraperapi-1m-google-queries-tco-audit)
- [JavaScript Rendering Cost: ZenRows, ScrapingBee and ScraperAPI](../zenrows-scrapingbee-vs-scraperapi-js-render-cost)
- [Failed Requests and Zero-Charge Billing: A Savings Calculator](../failed-request-zero-charge-savings-calculator)

### Reproducibility and contributions

Run the script from this directory with Python 3.8 or later. It uses only argparse, json and math from the standard library. Every directory contains its own executable script and works without importing a sibling repository. JSON consumers should read numeric fields and scope flags rather than scrape the ASCII table. A useful contribution includes the non-secret workload definition, changed assumptions, exact CLI and resulting accepted-output cost; unsupported performance claims are not measurements.

### MIT License

Copyright (c) 2026 scraperapi-serp contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
