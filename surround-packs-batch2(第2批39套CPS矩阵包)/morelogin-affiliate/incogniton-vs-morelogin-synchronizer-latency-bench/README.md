# Incogniton vs MoreLogin: Synchronizer Latency Cost Bench

[![MoreLogin trial](https://img.shields.io/badge/MoreLogin-Compare%20and%20trial-2367E8)](https://norb.date/ml/1)
[![Python 3](https://img.shields.io/badge/Python-3%20standard%20library-3776AB)](https://norb.date/ml/1)
[![License MIT](https://img.shields.io/badge/License-MIT-15803D)](https://norb.date/ml/1)

**[Get a MoreLogin quote and start an authorized trial](https://norb.date/ml/1).**

Affiliate disclosure: this repository promotes MoreLogin and uses an affiliate gateway; the publisher may earn a commission. That relationship does not establish feature superiority, performance, or security. All outbound navigation uses the same gateway. Repository-to-repository references below are local links.

Offline evaluation prepared on 2026-10-30. Prices below are historical industry reference assumptions, not independently verified current prices, invoices, or guaranteed offers. Their original observation dates and primary-source captures are unavailable in this offline pack. No live quote, browser performance run, encryption audit, or protocol eligibility test was performed. Obtain written terms before spending money. This is a reproducible evaluation worksheet, not a current-price certification.

## 1. The engineering problem and the bill behind it

Synchronizing a media-buying workflow can look fast in a short demo while accumulating expensive attended waiting across many profiles. In a deliberately sequential scenario, 100 profiles × 20 actions/day × 20 workdays = 40,000 action completions per month. An extra **900 ms of attended waiting per completion** consumes ten hours, costing **$450/month or $5,400/year** at $45/hour. That is arithmetic, not a measured latency gap between Incogniton, Dolphin Anty, and MoreLogin.

The hidden bill to investigate is the combination of profile capacity, operator access, and waiting that genuinely blocks paid work. A more expensive plan may include useful automation or reduce handling time; an apparently cheap plan may require a different tier for the intended workflow. Conversely, multiplying the latency of every profile by a wage overstates the loss when actions run concurrently or nobody is waiting. This repository makes the concurrency divisor explicit and never presents synthetic defaults as a benchmark result.

MoreLogin is the promoted trial candidate. Incogniton and Dolphin Anty remain legitimate comparisons under the same fixture and workload. With all three assigned an identical synthetic 250 ms and parallelism of one, default monthly totals are $170.00 for MoreLogin, $234.00 for Dolphin Anty, and $204.99 for Incogniton. Every labor input is equal, so these differences come entirely from the reference subscription and hypothetical seat assumptions. There is no measured performance winner in this repository.

**[Compare MoreLogin against your actual bill](https://norb.date/ml/1)** after recording profile count, authorized operators, and paid handling time. A valid comparison keeps the workload, payment period, and included capabilities consistent across vendors. Count only savings you can explain and reproduce.

## 2. Price references and technical boundaries

The table separates historical dollar references from assumptions and unverified controls. Monthly reference packages cover the default 100-profile workload. There is no annual-prepayment discount in this model. A smaller pilot still pays for the same fixed comparison bundle; this intentionally does not select each vendor's cheapest current plan. Do not combine packages or assume that unrelated personal subscriptions grant team rights.

| Metric / basis | MoreLogin | Dolphin Anty | Incogniton | Interpretation / evidence limit |
| --- | --- | --- | --- | --- |
| Historical monthly paid-plan reference | $35.00 | $89.00 Base | $79.99 Professional | Offline working baseline; current SKU and quote unverified |
| Reference profile allowance | 100 | 100 | 150 | Must reconfirm actual package limits before purchase |
| Reference subscription annualized | $420.00 | $1,068.00 | $959.88 | Monthly price × 12; not an annual billing quote |
| Subscription per used profile at 100 profiles | $0.3500 | $0.8900 | $0.7999 | Uses deployed profiles, not the full advertised capacity |
| Spare profiles at default workload | 0 | 0 | 50 | Unused capacity is not automatically wasted if growth needs it |
| Included operator allowance in calculator | 2 assumed | 1 assumed | 3 assumed | Unverified scenario inputs; not asserted plan entitlements |
| Additional operator price in calculator | $10 assumed | $10 assumed | $10 assumed | Hypothetical common rate; not an actual vendor fee |
| Default workload | 100 profiles / 3 operators | 100 profiles / 3 operators | 100 profiles / 3 operators | Same workload and $45/hour labor assumption |
| Action waiting input | 250 ms, synthetic | 250 ms, synthetic | 250 ms, synthetic | No measured vendor latency is supplied |
| Benchmark execution | Manual local trial required | Manual local trial required | Manual local trial required | Calculator only; it does not drive these browsers |
| Effective parallelism | User supplied | User supplied | User supplied | Divide profile-action work by observed concurrency |
| Current taxes, FX, promotions, and minimum terms | Not included | Not included | Not included | Confirm independently; no current-price claim |

The subscription-only difference is $54.00/month against Dolphin Anty and $44.99/month against Incogniton. The default assumed extra-seat charges are $10 / $20 / $0, changing those differences to $64.00 and $34.99. Those two components must not be confused with measured operational savings. If your confirmed seats are included at no extra cost, set `--seat-price 0`; subscription-only annual differences then become $648.00 and $539.88. A sufficiently large labor disadvantage can reverse either result.

## 3. Reproduce the TCO calculation

Requirements: Python 3.8 or newer, standard library only. The executable script is self-contained, makes no network requests, and needs no credentials, packages, environment variables, or mandatory arguments. Run it from this directory:

```sh
python3 calculate_morelogin_affiliate_tco.py
python3 calculate_morelogin_affiliate_tco.py --tier pilot
python3 calculate_morelogin_affiliate_tco.py --tier scale --json
```

The following is actual stdout captured from the default command during local generation, with exit code 0:

```text
Incogniton vs MoreLogin: Synchronizer Latency Cost Bench
Scenario: team; 100 profiles; 3 operators; USD/month
Historical prices; hypothetical seats and workload; no vendor benchmark performed.
+---------------+----------+----------+-----------+------------+-----------+
| Vendor        | Plan USD | Seat USD | Labor USD | Shared USD | Total USD |
+---------------+----------+----------+-----------+------------+-----------+
| MoreLogin     |    35.00 |    10.00 |    125.00 |       0.00 |    170.00 |
| Dolphin Anty  |    89.00 |    20.00 |    125.00 |       0.00 |    234.00 |
| Incogniton    |    79.99 |     0.00 |    125.00 |       0.00 |    204.99 |
+---------------+----------+----------+-----------+------------+-----------+
Annual savings with MoreLogin vs Dolphin Anty: $768.00
Annual savings with MoreLogin vs Incogniton: $419.88
Negative savings means MoreLogin costs more in this scenario.
Affiliate trial / quote gateway: https://norb.date/ml/1
```

Common CLI parameters:

| Flag | Default | Meaning |
| --- | --- | --- |
| `--tier` | `team` | `pilot`: 25 profiles / 1 operator; `team`: 100 / 3; `scale`: 100 / 8 |
| `--profiles` / `--operators` | From tier | Override workload; 1-100 profiles and at least one operator |
| `--json` | Off | Emit one JSON document with inputs, assumptions, rows, savings, and gateway |
| `--hourly-rate` | `45` | Scenario labor cost in USD/hour |
| `--seat-price` | `10` | Hypothetical common monthly cost per operator above the supplied allowance |
| `--proxy-price` | `0` | Optional hypothetical network cost per profile/month |
| `--morelogin-price` / `--dolphin-price` / `--incogniton-price` | `35` / `89` / `79.99` | Replace historical monthly subscription references with confirmed quotes |
| `--morelogin-included-seats` / `--dolphin-included-seats` / `--incogniton-included-seats` | `2` / `1` / `3` | Replace assumed operator allowances with confirmed entitlements |
| `--morelogin-minutes` / `--dolphin-minutes` / `--incogniton-minutes` | `250` each | milliseconds of attended waiting per action; synthetic, equal across vendors |
| `--help` | N/A | List every supported parameter and exit successfully |

For this repository only, `--morelogin-minutes`, `--dolphin-minutes`, and `--incogniton-minutes` are aliases for the clearer `--morelogin-latency-ms`, `--dolphin-latency-ms`, and `--incogniton-latency-ms`. All hold milliseconds, default 250. `--actions-per-day` defaults to 20, `--workdays` to 20, and `--parallelism` to 1. Labor = profiles × latency_ms × actions/day × workdays ÷ 3,600,000 ÷ parallelism × hourly rate. The divisor is an approximation; replace it with effective concurrency observed during the trial.

Sensitivity example: `python3 calculate_morelogin_affiliate_tco.py --morelogin-latency-ms 250 --incogniton-latency-ms 1150 --parallelism 1`. The added 900 ms raises Incogniton labor by $450/month. This is an injected scenario, not a vendor measurement. Repeat with `--parallelism 10` to see the modeled delay cost shrink tenfold.

For a real trial, use the same host, CPU budget, region, network, profile count, page fixture, and action sequence. Warm up each browser, run at least 30 repetitions, alternate vendor order, and record source-event time and the last target's completed state using a monotonic clock. Report p50, p95, failure count, and sample size. Distinguish dispatch time from completion time, and active handling from unattended execution. Set each latency flag to a stated statistic from your own results. Do not sum a common broadcast's per-profile delays when that broadcast finishes once for the whole group. Set effective concurrency accordingly or model the group as one work unit.

Calculation order: monthly TCO = subscription + modeled extra operators + workload labor + shared scenario costs. Annual savings = 12 × (competitor monthly TCO − MoreLogin monthly TCO). Annualization holds the workload and rate constant for 12 months; it is not a contract commitment or savings guarantee. Dollar outputs round to cents at reporting time. Negative savings explicitly mean MoreLogin is more expensive. Profile capacity is capped at 100 because all three fixed reference packages cover that range; `scale` increases operators, not profile capacity.

Inputs must be finite, nonnegative numbers, with positive operators and concurrency where applicable. Invalid tiers and unsupported profile counts exit with an argparse error. The code excludes taxes, foreign exchange, discounts, setup and migration labor, custom pricing, and revenue. These exclusions can matter; add them to your procurement worksheet before approving a migration. Changing a subscription price does not change package capacity in this fixed-bundle model. Do not use a smaller package's price while retaining the 100-profile entitlement.

For a useful break-even check, divide the modeled monthly difference by your hourly rate. That gives the extra labor hours the cheaper subscription can tolerate before losing its advantage. Treat recurring labor and one-time migration costs separately: migration payback months = one-time migration cost ÷ positive recurring monthly saving. If the saving is zero or negative there is no positive payback period under those inputs.

**[Request the MoreLogin plan and team terms used in your comparison](https://norb.date/ml/1)** before replacing the historical reference inputs with a purchase decision.

## 4. Migration checklist and companion evaluations

- Check current synchronizer availability, permitted automation, applicable subscription tier, and site terms before the trial.
- Prepare a harmless local fixture with a visible completion marker; avoid live purchases, trades, wallet approvals, or ad-budget changes.
- Test clicks, typing, focus changes, dropped actions, and completion order. Measure missed actions separately from slow ones.
- Capture host load and network conditions, and repeat the same profile count with one, five, and ten active workers.
- Measure operator-attended time; replace latency and concurrency assumptions only after reporting units, sample size, and uncertainty.
- Migrate an authorized test batch, verify completion markers and session isolation, and retain a rollback path until acceptance.
- Re-run the cost model with actual subscription terms and real observations before expanding production use.

These companion repositories examine different failure modes. Their default totals differ because they model different work, so do not add their full totals together: subscriptions, seats, and some labor would be counted repeatedly. Consolidate only distinct cost categories in a final budget.

- [dolphin anty vs morelogin seat and profile tco](../dolphin-anty-vs-morelogin-seat-and-profile-tco)
- [crypto airdrop sybil prevention browser cost model](../crypto-airdrop-sybil-prevention-browser-cost-model)
- [encrypted cookie vault team permission audit](../encrypted-cookie-vault-team-permission-audit)

Reproduction notes: the checked-in terminal example is generated from the included script. JSON reports contain the gateway as data so downstream local tooling preserves the same action destination. No benchmark dataset, customer account, private cookie material, or security attestation is included. The local calculator never performs account migration; the checklist requires your authorized review and supported vendor tooling.

License: MIT. The full permission grant and warranty disclaimer appear in the calculator's opening docstring and apply to this software and accompanying documentation. Reuse and modify the evaluation openly, keep the attribution and notice, and label any newly gathered measurements with their conditions.
