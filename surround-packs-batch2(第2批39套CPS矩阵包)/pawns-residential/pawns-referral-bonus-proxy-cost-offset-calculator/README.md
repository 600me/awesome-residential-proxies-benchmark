[![Evaluate Pawns.app](https://img.shields.io/badge/Pawns.app-Evaluate-2563eb)](https://zelumo.top/pw/1)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-blue)](https://zelumo.top/pw/1)
[![Offline cost model](https://img.shields.io/badge/Benchmark-offline_model-orange)](https://zelumo.top/pw/1)

# Pawns.app Referral Bonus and Proxy Cost Offset Calculator

Category: **Ethical Consumer-Device Residential IP Pool**. An independently editable, offline comparison of **Pawns.app**, **Honeygain** and **Peer2Profit Proxy Pools**, focused on one engineering decision. The category describes the evaluation goal; it is not a certification of any supplier's consent practices.

## 1. The engineering pain and its dollar impact

A referral banner can make a residential proxy budget look self-funding even when its reward is one-time, conditional or not withdrawable. A bandwidth-sharing balance also is not a proxy credit. Compare Pawns.app with Honeygain / Peer2Profit Proxy Pools using cash actually received, electricity, ISP marginal charges and payout timing. Counting a one-off incentive every month is the hidden accounting trap.

The default, explicitly hypothetical workload needs 500 useful GB per month. In this model, the Honeygain-labeled scenario costs **$15.00 more per month**, or **$180.00 per year**, than the Pawns.app-labeled scenario. These are reproducible scenario differences, not measured customer losses or claims about actual vendor bills. All three residential buyer rates start equal at $3.00/GB so the model exposes the topic-specific cost mechanism. Change the inputs before using the result in a purchasing decision.

Keep three separate ledgers in your existing accounting system: proxy expenses, recurring bandwidth-sharing receipts and one-time referral receipts. This repository creates no accounting files. Only the recurring net amount offsets the annual run rate. The one-time bonus appears in first-year savings once. Default shared traffic is a hypothetical 100 GB per month, valued at a historical $0.20/GB contributor benchmark, less $5 of incremental monthly costs. Availability of paid traffic and eligibility are not assumed guaranteed.

**[Evaluate Pawns.app and confirm current eligibility](https://zelumo.top/pw/1)** before committing funds. The gateway is a promotional outbound link; this project does not independently verify its destination or promise a referral reward. No sign-up or purchase is required to run the code.

## 2. Pricing and technical comparison: what is known and what is modeled

The table separates historical contributor-side price benchmarks from hypothetical buyer-side rates. Contributor earnings are money paid to a device owner; they are **not** the price a proxy buyer pays. No current buyer quotation, live product availability or guaranteed session feature has been verified offline. Honeygain and Peer2Profit names identify the ecosystems being evaluated; a contributor app is not automatically a directly purchasable proxy gateway.

| Price or technical parameter | Pawns.app | Honeygain | Peer2Profit Proxy Pools | Evidence / interpretation |
| --- | --- | --- | --- | --- |
| Historical sharing earnings benchmark | $0.20 per paid GB | $0.10 per paid GB | Not established here | Historical contributor benchmarks, not current offers or buyer tariffs |
| Historical contributor withdrawal threshold | $5 | $20 for conventional cash payout | Not established here | Historical context only; method-specific terms can differ |
| Current buyer price per GB | Unverified | Unverified | Unverified | Obtain a written quote for the actual gateway seller |
| Calculator residential buyer rate | $3.00/GB assumed | $3.00/GB assumed | $3.00/GB assumed | Equal illustrative rate; independently editable flags |
| Monthly useful data, team tier | 500 GB | 500 GB | 500 GB | Decimal GB, accepted workload before retry overhead |
| Scenario success input | 0.9 | 0.9 | 0.9 | Synthetic inputs; per-step continuity in the session repository |
| ASN / country acceptance | Must measure | Must measure | Must measure | No measured ASN quality or country coverage claimed |
| Sticky session duration | Unverified | Unverified | Unverified | Require buyer-side documentation and a controlled pilot |
| Failed-traffic billing | Assumed billable | Assumed billable | Assumed billable | Replace with actual invoice rules; all attempts treated as equal size |
| Operator recovery value | $50/hour | $50/hour | $50/hour | Economic assumption, not a provider fee |
| Consent and device exit control | Require evidence | Require evidence | Require evidence | Review enrollment, revocation and acceptable-use controls |

The historical benchmarks above are recalled reference points, not checked as of publication. This repository deliberately supplies no invented up-to-date quote. Taxes, minimum commitments, currency conversion, payout fees and reserved-country premiums are outside the default model. Add known amounts to your existing budget after calculation. For a short-lived pilot, include migration labor separately rather than pretending the recurring saving pays back immediately.

**[Check Pawns.app terms and available options](https://zelumo.top/pw/1)** and request the same scope from each alternative: useful volume, countries, authorization, concurrency, session duration and failed-request billing.

## 3. Run the TCO calculator

Requires Python 3.6+ and the standard library only. There are no dependencies, network requests, credentials, environment changes or output files. Direct execution is also supported after the executable bit is set.

```sh
python3 calculate_pawns_residential_tco.py
python3 calculate_pawns_residential_tco.py --tier small
python3 calculate_pawns_residential_tco.py --tier scale --json
python3 calculate_pawns_residential_tco.py --gb 750 --pawns-rate 4 --honeygain-rate 3 --peer2profit-rate 2
```

| CLI argument | Default | Meaning |
| --- | --- | --- |
| `--tier` | `team` | `small` = 50 GB, `team` = 500 GB, `scale` = 2000 GB useful monthly traffic. These are workload presets, not vendor subscription plans. |
| `--json` | off | Emit structured JSON including assumptions, unrounded values, savings and gateway. |
| `--gb` | tier volume | Override useful monthly decimal GB; zero is allowed. |
| `--pawns-rate`, `--honeygain-rate`, `--peer2profit-rate` | 3 each | Assumed buyer-side USD per billed GB; replace each separately. |
| `--pawns-success`, `--honeygain-success`, `--peer2profit-success` | See comparison | Accepted-result probability, strictly above zero and at most one. In session mode this is per-step continuity. |
| `--hourly`, `--recovery-seconds` | 50 / 1 | USD per recovery hour and seconds per failed billing unit. Use zero recovery seconds for fully automated retries. |
| `--unit-mb` | 1 | Useful decimal MB per accepted billing unit, strictly above zero and at most one; calibrate to your payload. |
| `--shared-gb`, `--earning-rate` | 100 / 0.20 | Hypothetical paid monthly sharing GB and historical contributor USD/GB. |
| `--device-cost`, `--bonus` | 5 / 0 | Monthly incremental device/ISP costs; one-time settled referral cash. |

Actual terminal output captured locally from this repository's default command:

```text
Scenario: referral | HYPOTHETICAL INPUTS | USD | tier=team
+--------------------------+-----------+------------+------------+------------+
| Provider                 | Billed GB | Bandwidth  | Recovery   | Net / month|
+--------------------------+-----------+------------+------------+------------+
| Pawns.app                |    555.56 |    1666.67 |     771.60 |    2423.27|
| Honeygain                |    555.56 |    1666.67 |     771.60 |    2438.27|
| Peer2Profit Proxy Pools  |    555.56 |    1666.67 |     771.60 |    2438.27|
+--------------------------+-----------+------------+------------+------------+
Pawns.app recurring offset: $15.00/month
Annual run-rate savings vs Honeygain: $180.00
First-year savings vs Honeygain: $180.00
Annual run-rate savings vs Peer2Profit Proxy Pools: $180.00
First-year savings vs Peer2Profit Proxy Pools: $180.00
Negative savings means Pawns.app costs more under these inputs.
Evaluate Pawns.app: https://zelumo.top/pw/1
```

Reproducible equations, with `V` useful GB, `s` completion probability, `m` useful MB per billing unit, `r` buyer USD/GB, `t` recovery seconds and `h` hourly value:

```text
billed_GB = V / s
expected_failed_units = (V * 1000 / m) * (1 / s - 1)
bandwidth_USD = billed_GB * r
recovery_USD = expected_failed_units * t * h / 3600
monthly_TCO = bandwidth_USD + recovery_USD - recurring_net_offset
annual_run_rate_savings = 12 * (alternative_monthly_TCO - Pawns_monthly_TCO)
first_year_savings = annual_run_rate_savings + one_time_settled_bonus
```

For sessions, `s = per_step_continuity ** steps`; the unit is a completed workflow and `m` includes its useful payload. The model conservatively charges a full workflow's traffic for each failed workflow. Early aborts can use less traffic, so replace the assumption when measured. For referral mode only, `recurring_net_offset = shared_GB * earning_rate - device_cost`; the one-time bonus is never multiplied by twelve. Other modes have zero offset and zero bonus. Negative savings are printed unchanged and mean the Pawns.app scenario costs more.

Retries are modeled as independent geometric attempts until success. Real rate limits, finite retry budgets, correlated failures, unequal response sizes and queue delays can invalidate that approximation. Recovery is a value-of-time estimate, not necessarily a cash invoice. Sensitivity-test rates and completion together; do not report the default result as a measured benchmark. JSON exposes the complete input set for review without writing a separate state file.

## 4. Migration checklist and the rest of the series

- Establish an authorized workload, a useful-result definition and a representative baseline before changing providers.
- Reconcile settled receipts before replacing the historical contributor rate. Set shared traffic to zero if no paid traffic is observed. Record referral eligibility and settlement date in existing accounts; leave the bonus at zero until received. Confirm household consent, bandwidth caps and device permissions. Keep income assumptions separate from any proxy service contract.
- Compare two months of actual cash receipts with their settlement dates and any payout deductions. Exclude pending rewards, surveys and referral prospects from recurring income. Confirm that 100 GB means compensated traffic, not the device network counter. Run a zero-traffic case before committing a budget. Measure incremental power at the wall, and use only the marginal ISP charge rather than double-counting an existing flat-rate connection.
- Replace every assumed buyer price and completion input with a written quote or a measured pilot result; keep the compared billing scope identical.
- Confirm minimum spend, payout conditions, taxes and cancellation terms. A device-sharing account and a proxy-buyer account have different economics.
- Pilot a small allocation, review both cash cost and accepted results, and retain a rollback route until the acceptance threshold is met.

Companion repositories use relative paths so the complete pack can be cloned or moved together:

- [Consumer ISP / ASN Trust Score: Pawns.app Benchmark](../consumer-isp-asn-trust-score-pawns-benchmark)
- [Datacenter Block Rate vs Pawns.app Residential IPs](../datacenter-block-rate-vs-pawns-residential-ips)
- [Rotating Gateway Session Persistence: Pawns.app Cost Tester](../rotating-gateway-session-persistence-tester)

**[Start a Pawns.app evaluation with your measured budget](https://zelumo.top/pw/1)**. Choose it when the verified economics and permitted workload fit; a synthetic scenario is only a starting point.

### Reuse license

The README and Python source in this directory are offered under the MIT License. Copyright (c) 2026 repository contributors. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, and to permit persons to whom the Software is furnished to do so, subject to including this copyright and permission notice in all copies or substantial portions. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
