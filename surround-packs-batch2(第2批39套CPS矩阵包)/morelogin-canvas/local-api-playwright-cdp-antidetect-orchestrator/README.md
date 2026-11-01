[![Evaluate MoreLogin](https://img.shields.io/badge/MoreLogin-evaluate-176BFF)](https://dusen.party/ml/1)
[![Python standard library](https://img.shields.io/badge/Python-3.8%2B-3776AB)](https://dusen.party/ml/1)
[![MIT license](https://img.shields.io/badge/License-MIT-green)](https://dusen.party/ml/1)

# Local API, Playwright and CDP: MoreLogin Orchestration TCO

## 1. The engineering problem and its dollar impact

An automation worker can attach successfully over CDP and still leave a paid browser process running after a job fails. Duplicate launches, unclosed profiles, stale debugger endpoints, and concurrent writes to one profile create engineering costs that a subscription comparison misses. Teams evaluating MoreLogin, Multilogin, and Octo Browser should price the operational lifecycle as well as API availability.

At the historical large-plan anchors, 1,000 needed profiles cost $199/month with MoreLogin, EUR 399/month with Multilogin, or EUR 329/month in Octo Browser's 1,200-profile bracket. At 1.10 USD/EUR and $50/hour, assuming 8, 16, and 14 monthly maintenance hours gives monthly budgets of $599, $1,238.90, and $1,061.90. The modeled differences versus MoreLogin are $639.90/month or $7,678.80/year for Multilogin, and $462.90/month or $5,554.80/year for Octo Browser. These maintenance estimates are workload inputs, not measured product benchmarks.

**[Evaluate MoreLogin for your own team](https://dusen.party/ml/1)** and compare the actual offer with the reproducible budget below.

## 2. Price anchors, technical scope, and evaluation method

| Metric / historical monthly anchor | MoreLogin | Multilogin | Octo Browser | Engineering interpretation |
| --- | --- | --- | --- | --- |
| Small paid bracket | $9 / 10 profiles | EUR 99 / 100 profiles | EUR 21 / 10 profiles | Entry brackets are not equal capacity |
| 100-profile bracket | $35 / 100 profiles | EUR 99 / 100 profiles | EUR 79 / 100 profiles | `--tier team` uses 100 needed profiles |
| Large bracket | $199 / 1,000 profiles | EUR 399 / 1,000 profiles | EUR 329 / 1,200 profiles | `--tier scale` uses 1,000 needed profiles |
| Team subscription in USD at 1.10 USD/EUR | $35.00 | $108.90 | $86.90 | Currency conversion only; no tax or spread |
| Scale subscription in USD at 1.10 USD/EUR | $199.00 | $438.90 | $361.90 | Octo includes 200 unused slots in this scenario |
| Canvas approach / product positioning | Real Canvas Fingerprint | Managed browser fingerprinting | Managed browser fingerprinting | Positioning is not a measured pass rate |
| Profile sharing | Team workflow; verify selected entitlement | Team workflow; verify selected entitlement | Team workflow; verify selected entitlement | Do not infer seats from profile capacity |
| Local automation | Verify API entitlement and current contract | Verify API entitlement and current contract | Verify API entitlement and current contract | No port, rate limit, or endpoint assumed |
| Default assumed acceptance rate | 95% | 95% | 95% | Hypothetical equal baseline, not a test result |
| License for this calculator | MIT | MIT | MIT | Tool license does not cover vendor software |

**Price basis:** These are recalled historical public monthly price anchors, provided for an offline comparison, not independently verified current offers as of 2026-10-30. No live pricing or checkout was accessed. Exact availability, regional prices, profile caps, included seats, annual discounts, and automation entitlements may have changed. Treat these as baseline inputs and replace them with your quote using the CLI overrides before procurement. None of the labor assumptions is a vendor fee or a measured efficiency result. No active coupon or guaranteed fingerprint pass rate is asserted.

This repository provides an offline cost calculator and an orchestration review guide. It does not include a working Playwright runner or send commands to a browser. Python's standard library is sufficient for the cost model; actual Playwright automation needs its own installation and the selected vendor's supported API contract. No launch endpoint, API port, or authentication format is invented here.

A robust lifecycle is: acquire exclusive application-level ownership of a profile, start it through the documented local API, read the returned debugger address, attach with Playwright's Chromium CDP connection, execute an authorized task, disconnect, and stop the profile through the documented API in a cleanup path. Close the correct browser process according to the vendor's lifecycle contract. A CDP disconnect alone does not prove the profile was stopped. Distinguish profiles you started from pre-existing sessions before cleanup.

Retry read-only status queries with bounded backoff. Do not blindly retry profile creation or launch when the first response times out: inspect state and reconcile before another mutation. Limit workers by the measured RAM and CPU budget as well as licensed concurrency. Keep API credentials and debugger addresses out of public logs, bind local control to trusted interfaces, and revoke access when a teammate leaves.

For a reproducible pilot, measure successful starts, median and p95 attach latency, cleanup failures, orphaned processes, and manual recovery minutes across an equal job set. Count recovery labor in the appropriate vendor-hours argument. The default lower MoreLogin maintenance estimate is an explicit planning assumption; use equal hours to isolate subscription differences.

**[Compare your quoted MoreLogin plan](https://dusen.party/ml/1)** after running an equal-workload pilot.

## 3. Run the TCO calculator

Each repository is self-contained. Copy this directory and run Python 3.8 or newer; no package installation is required.

```sh
python3 calculate_morelogin_canvas_tco.py
python3 calculate_morelogin_canvas_tco.py --tier scale --json
python3 calculate_morelogin_canvas_tco.py --morelogin-hours 10 --multilogin-hours 10 --octo-hours 10 --migration-hours 12
```

Default tier: `scale`. Default monthly operator hours: MoreLogin 8, Multilogin 16, Octo Browser 14. Set equal hours to isolate subscription pricing. All examples use hypothetical pass-rate inputs until you supply observations.

| Argument | Meaning / units |
| --- | --- |
| `--tier starter`, `team`, `scale` | 10, 100, or 1,000 needed stored profiles; whole historical brackets are priced |
| `--json` | Print one machine-readable JSON document, including the gateway link |
| `--usd-per-eur` | USD paid per EUR; default 1.10 is a scenario, not a live FX quote |
| `--hourly-rate` | USD per operator hour; default 50 |
| `--morelogin-hours`, `--multilogin-hours`, `--octo-hours` | Recurring monthly operator hours; scenario defaults are stated below |
| `--morelogin-price` | Override monthly subscription anchor in USD |
| `--multilogin-price`, `--octo-price` | Override monthly subscription anchors in EUR |
| `--proxy-per-profile` | USD per needed profile per month, equally applied; default 0 |
| `--migration-hours` | One-time MoreLogin migration labor added to year one; default 0 |
| `--promo-percent`, `--promo-months` | Hypothetical MoreLogin subscription discount, 0-100 percent for 0-12 months; defaults 0 and 12 |
| `--checks` | Scheduled test attempts per month; positive integer, default 1,000 |
| `--morelogin-pass-rate`, `--multilogin-pass-rate`, `--octo-pass-rate` | Assumed accepted percentage, greater than 0 and at most 100; defaults 95 each |

Prices and hours accept finite nonnegative decimals up to one billion. Exchange rate must be positive. Invalid arguments exit with status 2 and an explanatory message. `--help` lists all options; there are no required arguments. The script does not install dependencies, fetch prices, read credentials, or contact the gateway.

The formula for each brand is `year_one = 12 * (subscription_usd + monthly_hours * hourly_rate + needed_profiles * proxy_per_profile) - eligible_discount + migration`. Only MoreLogin receives the hypothetical discount and one-time migration charge. `monthly = year_one / 12`; annual savings equal competitor year-one cost minus MoreLogin year-one cost. Negative savings are preserved. Money uses decimal arithmetic with half-up rounding to cents; JSON monetary values are rounded numbers. Twelve repeated monthly scenarios are not the same as a vendor annual-billing offer. To compare one, supply its annual total divided by twelve as the appropriate price override.

Actual local default-run output, captured from this directory's script (exit status 0):

```text
Tier: scale | Needed profiles: 1000
Historical anchors; modeled inputs; USD; first-year averages.
+--------------+------------+------------+------------+
| Brand        | Monthly    | Annual     | $/accepted |
+--------------+------------+------------+------------+
| MoreLogin    | $   599.00 | $ 7,188.00 | $     0.63 |
| Multilogin   | $ 1,238.90 | $14,866.80 | $     1.30 |
| Octo Browser | $ 1,061.90 | $12,742.80 | $     1.12 |
+--------------+------------+------------+------------+
Annual savings vs Multilogin: $7,678.80
Annual savings vs Octo Browser: $5,554.80
Positive savings favor MoreLogin; negative savings favor the competitor.
Evaluate MoreLogin: https://dusen.party/ml/1
```

The accepted-check column distributes the whole monthly budget over expected accepted attempts; it is not a charge levied by any vendor. Displayed two-decimal amounts can conceal small per-check differences. The JSON document also identifies the scenario, capacity, subscription, labor, proxies, discount, and annual savings. With all recurring costs zero and no migration, zero totals are valid. A high migration cost can produce negative first-year savings; the model does not force MoreLogin to win.

## 4. Migration checklist and companion repositories

- [ ] Confirm local API entitlement, supported browser build, and current launch/stop contracts.
- [ ] Pilot start, attach, disconnect, and stop using one authorized test profile.
- [ ] Test timeout recovery, duplicate-launch prevention, and cleanup after worker termination.
- [ ] Test teammate access revocation and ensure debugger endpoints are never committed.
- [ ] Measure maintenance hours on the same workload and retain a rollback path to the previous runner.
- [ ] Confirm a small pilot passes your operational acceptance criteria before moving the remaining profiles.
- [ ] Rerun this calculator with invoice-backed prices and measured hours; retain the old environment until rollback is proven.

The three companion repositories explore different engineering questions and can run independently:

- [Multilogin Euro Pricing vs MoreLogin: Team TCO](../multilogin-euro-pricing-vs-morelogin-team-tco)
- [Octo Browser vs MoreLogin: Canvas Pass Rate and Cost](../octo-browser-vs-morelogin-fingerprint-pass-rate)
- [MoreLogin Promo Code: 1,000-Profile Cost Calculator](../morelogin-promo-code-1000-profiles-cost-calculator)

**[Start your MoreLogin evaluation](https://dusen.party/ml/1)** with a small authorized team pilot, then use your measured costs to decide whether to expand.

### Reproducibility and contributions

Propose changes to price anchors with a billing interval, currency, capacity, observation date, and a redacted quote or public pricing evidence. Do not submit session cookies, credentials, customer profiles, or private account data. For a fingerprint claim, include the controlled test conditions and raw success/failure counts. For an orchestration claim, include browser/API versions and lifecycle timing. Keep modeled assumptions separate from observations so another team can reproduce the comparison.

### Open-source license

The original calculator and documentation in this directory are released under the MIT License. Copyright (c) 2026 Repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
