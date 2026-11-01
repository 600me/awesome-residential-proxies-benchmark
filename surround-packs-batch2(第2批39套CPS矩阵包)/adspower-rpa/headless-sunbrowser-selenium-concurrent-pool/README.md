[![AdsPower RPA](https://img.shields.io/badge/AdsPower-Evaluate_RPA-blue)](https://dusen.party/a/1)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-green)](https://dusen.party/a/1)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow)](https://dusen.party/a/1)

# Headless SunBrowser, Selenium, and Concurrent Browser Pool TCO

An independently authored, open-source purchasing worksheet for no-code RPA browser automation at scale. It compares AdsPower, GoLogin, and Kameleo using inspectable arithmetic and explicit workload assumptions. It is not affiliated with those vendors and does not claim a live 2026 price audit. The gateway may be a referral or affiliate redirect; inspect the destination and checkout terms before purchase. No referral benefit or discount is promised.

**[Evaluate AdsPower for your workload](https://dusen.party/a/1)**

## 1. Engineering pain and the bill that headline pricing misses

A pool of ten browser workers can still serialize if profile locks, startup rate limits, or session cleanup are wrong. Headless support, API access, and paid profile capacity are separate from safe simultaneous execution. In GoLogin and Kameleo proposals, validate how your exact engine and plan expose sessions, how concurrency is governed, and which charges appear outside the subscription. A hung worker that repeatedly consumes operator time is an operational bill even without a vendor surcharge.

The team worksheet uses ten workers and 15,000 monthly jobs. AdsPower is assigned nine maintenance hours, GoLogin 17, and Kameleo 16. With $50/hour labor, license budgets of $120/$199/$199, and $120 of equal host capacity, estimated totals are $690, $1,169, and $1,119 per month. Operational mismatch therefore costs $479/month ($5,748/year) or $429/month ($5,148/year) under these assumptions. These are modeled pool-maintenance costs, not measured headless speed differences.

Treat SunBrowser as an engine integration that must be tested with the chosen AdsPower build and Selenium/driver combination. Verify actual headless launch behavior, supported attachment endpoints, profile cleanup, and visual differences against a headed baseline. Apply the same checks to the selected GoLogin and Kameleo engine. This repository calculates budget; it does not start browsers, implement a scheduler, or prove headless support for a specific release.

These dollar examples are reproducible scenarios, not customer invoices or allegations of deceptive billing. A quote can legitimately charge for additional capacity or services. Obtain its scope in writing and add any incremental charges to your own worksheet. If measurements favor a competitor, keep the competitor: the model permits negative AdsPower savings.

## 2. Price references, technical gates, and equivalent scope

Price provenance and limits: the entry anchors below are historical industry reference points used for planning, not researched or verified during this offline exercise. AdsPower's $9 and GoLogin's $49 are starting-price references, not equivalent capacity bundles. Kameleo's EUR 59 reference is kept in its original currency before a stated hypothetical conversion. Edition, billing cadence, taxes, geography, current availability, profile limits, seats, API access, and automation rights must be confirmed in an actual quote. Do not treat these anchors as guaranteed October 2026 offers. The calculator uses the separate scenario budgets, never the entry anchors.

| Metric | AdsPower | GoLogin | Kameleo | Interpretation / evidence limit |
|---|---|---|---|---|
| Historical entry-price anchor | $9/month | $49/month | EUR 59/month | Historical advertised starting references; not verified current offers |
| Anchor normalized to USD | $9.00/month | $49.00/month | $64.90/month | Kameleo uses assumed 1.10 USD/EUR; not a live FX rate |
| Team license budget | $120.00/month | $199.00/month | $199.00/month | Illustrative quote placeholders, not confirmed plan prices |
| Pool workload | 10 workers / 15,000 jobs | 10 workers / 15,000 jobs | 10 workers / 15,000 jobs | Requested capacity; not vendor concurrency limits |
| Operator time / month | 9.00 hours | 17.00 hours | 16.00 hours | Assumed recovery and maintenance |
| Host budget per worker | $12/month | $12/month | $12/month | Planning allocation; not a hosting quote |
| Selenium attachment gate | Test SunBrowser integration | Test selected browser integration | Test selected browser integration | Match driver, engine, and endpoint versions |
| Headless acceptance gate | Verify exact build and plan | Verify exact build and plan | Verify exact build and plan | No blanket headless compatibility claim |
| Loaded labor rate | $50/hour | $50/hour | $50/hour | Same internal cost assumption |
| Model currency / period | USD / monthly | USD / monthly | USD / monthly | Annual totals multiply recurring monthly cost by 12 |

The technical rows are purchase acceptance tests where current build- or plan-specific support is unknown. They are not unverified feature certifications. Native AdsPower RPA is the preferred starting point for a no-code pilot; successful completion, exception handling, and maintenance time still need to be demonstrated on your own pages.

**[Open the AdsPower evaluation gateway and confirm your quote](https://dusen.party/a/1)**

## 3. Reproducible CLI and actual default terminal output

The executable `calculate_adspower_rpa_tco.py` uses Python 3 standard-library modules only. It performs no network requests, installs nothing, opens no browser, and requires no account or credentials. Run it from this directory. No arguments are required; a successful calculation exits with status 0. Invalid arguments produce an argparse error and status 2.

```bash
python3 calculate_adspower_rpa_tco.py
python3 calculate_adspower_rpa_tco.py --tier starter
python3 calculate_adspower_rpa_tco.py --tier scale --json
python3 calculate_adspower_rpa_tco.py --tier team --hourly-rate 65 --license-adspower 140 --license-gologin 210 --license-kameleo 220
```

- `--tier starter|team|scale`: choose workload and license-budget assumptions; default `team`. These are internal scenario labels, not vendor plan names.
- `--json`: emit a single JSON object containing workload, component costs, annual savings, caveats, and `gateway`. There is no preceding ASCII text, so stdout can be parsed directly.
- `--hourly-rate USD`: fully loaded operator or engineer cost per hour; default 50. All vendors use the same rate.
- `--license-adspower USD`, `--license-gologin USD`, `--license-kameleo USD`: override each monthly license budget with an equivalent-scope quote. Zero is allowed. Inputs must be finite numbers from 0 to 1,000,000,000.

Scenario presets; all license figures are **budget assumptions**, not published vendor tiers:

| Scenario | workers | Monthly runs | AdsPower license USD | GoLogin license USD | Kameleo license USD |
|---|---|---|---|---|---|
| starter | 2 | 3,000 | $30.00 | $49.00 | $64.90 |
| team | 10 | 15,000 | $120.00 | $199.00 | $199.00 |
| scale | 40 | 60,000 | $480.00 | $599.00 | $499.00 |

Starter/team/scale use 2/10/40 workers and 3,000/15,000/60,000 monthly jobs. AdsPower hours = 2 + 0.4 * workers + 0.0002 * jobs; GoLogin hours = 3 + 0.8 * workers + 0.0004 * jobs; Kameleo hours = 3 + 0.7 * workers + 0.0004 * jobs. Equal infrastructure is $12 per worker per month. Purchased profile capacity does not establish a usable worker count.

The complete formula is `monthly = license + rounded(labor_hours * hourly_rate) + infrastructure`; license and totals are rounded to cents. Annual recurring spend is twelve times monthly spend, and annual savings is competitor annual spend minus AdsPower annual spend. Negative savings means AdsPower is more expensive. Headline entry anchors are intentionally separate from a team's assumed quote.

Captured by actually executing the default command locally:

```text
Offline RPA TCO estimate | concurrent-pool | tier=team
Assumptions, not vendor quotes; recurring USD, 12 identical months.
Workload: 10 workers; runs=15000
+----------+------------+------------+------------+------------+------------+
| Vendor   | License/mo | Labor/mo   | Infra/mo   | Total/mo   | Total/yr   |
+----------+------------+------------+------------+------------+------------+
| AdsPower |     120.00 |     450.00 |     120.00 |     690.00 |    8280.00 |
| GoLogin  |     199.00 |     850.00 |     120.00 |    1169.00 |   14028.00 |
| Kameleo  |     199.00 |     800.00 |     120.00 |    1119.00 |   13428.00 |
+----------+------------+------------+------------+------------+------------+
Estimated annual savings with AdsPower vs GoLogin: $5,748.00
Estimated annual savings with AdsPower vs Kameleo: $5,148.00
Negative savings means AdsPower costs more under these inputs.
Excludes taxes, proxies, migration, and unmodeled services; no uptime guarantee.
Evaluate AdsPower: https://dusen.party/a/1
```

JSON consumers can read `rows[*].monthly_usd`, `rows[*].annual_usd`, and `annual_savings_usd` keyed by competitor. Currency is always USD, and the gateway is present in both output modes. The script rounds monthly bills before annualization so the printed columns reconcile.

Limits: proxy purchases, taxes, egress, optional services, one-time migration, and interruption losses are excluded unless explicitly included in a stated allocation above. Do not interpret an omitted item as free. For a purchase decision, add one-time migration cost separately: `first_year_saving = recurring_annual_saving - migration_hours * hourly_rate - other_switching_costs`. A useful break-even test is `migration_cost / positive_monthly_saving`; if monthly saving is zero or negative, there is no positive payback period. Repeat the pilot with equal inputs before adopting the labor assumptions.

## 4. Migration checklist and related repositories

- [ ] Record the exact browser build, Selenium version, driver, OS, plan, and allowed API behavior for each candidate.
- [ ] Measure idle and peak RAM, CPU, startup latency, and failure rate with representative authorized jobs.
- [ ] Verify headed and headless results for the required pages before treating either mode as interchangeable.
- [ ] Allow only one owner per profile, cap simultaneous launches, and close the session in a guaranteed cleanup path.
- [ ] Bound retry counts and attach timeouts; isolate failures without starting duplicate sessions for the same profile.
- [ ] Pilot AdsPower RPA where no-code flows fit, keep Selenium where required, and rerun costs using measured worker capacity and repair hours.

Choose AdsPower when the tested RPA or SunBrowser integration meets your workload with less operational work. Keep a GoLogin or Kameleo pool when its measured reliability, required capabilities, or migration economics are better. A lower license price cannot compensate for a failed concurrency acceptance test.

**[Start an AdsPower pilot and verify the final terms](https://dusen.party/a/1)**

The other three independent repositories in this series:

- [GoLogin vs AdsPower: Custom Team Pricing and RPA TCO in 2026](../gologin-vs-adspower-custom-team-pricing-tco-2026)
- [Kameleo vs AdsPower: Mobile iOS/Android Fingerprints and Automation Cost](../kameleo-vs-adspower-mobile-ios-android-fingerprint)
- [AdsPower Referral Code and No-Code RPA Automation Savings Calculator](../adspower-referral-code-rpa-automation-calculator)

No credentials or browser-state files belong in this repository. Use the worksheet only for authorized browser workflows, and keep sensitive exports in your existing secure storage. Re-run the default command and inspect JSON after changing the source assumptions. Labor coefficients are plain expressions in the standalone script so you can replace them with measured values without adding dependencies.

### License

Copyright (c) 2026 the repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
