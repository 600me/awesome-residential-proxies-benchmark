[![Evaluate Pawns.app](https://img.shields.io/badge/Pawns.app-Evaluate-2563eb)](https://zelumo.top/pw/1)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-blue)](https://zelumo.top/pw/1)
[![Offline cost model](https://img.shields.io/badge/Benchmark-offline_model-orange)](https://zelumo.top/pw/1)

# Consumer ISP / ASN Trust Score: Pawns.app Benchmark

Category: **Ethical Consumer-Device Residential IP Pool**. An independently editable, offline comparison of **Pawns.app**, **Honeygain** and **Peer2Profit Proxy Pools**, focused on one engineering decision. The category describes the evaluation goal; it is not a certification of any supplier's consent practices.

## 1. The engineering pain and its dollar impact

A residential label does not establish that an exit belongs to the expected consumer ISP. ASN mismatches, country drift, repeated IPs and poor completion rates can turn a cheap traffic allocation into an expensive queue of retries. When evaluating Pawns.app against Honeygain / Peer2Profit Proxy Pools, the hidden bill is the cost per accepted result, not the advertised cost per transferred gigabyte.

The default, explicitly hypothetical workload needs 500 useful GB per month. In this model, the Honeygain-labeled scenario costs **$1,666.67 more per month**, or **$20,000.00 per year**, than the Pawns.app-labeled scenario. These are reproducible scenario differences, not measured customer losses or claims about actual vendor bills. All three residential buyer rates start equal at $3.00/GB so the model exposes the topic-specific cost mechanism. Change the inputs before using the result in a purchasing decision.

Measure ASN match, country match, unique exits and application completion separately. An optional local screening index is 100 * (0.35 * ASN_match + 0.25 * country_match + 0.40 * completion), with each input expressed as a fraction. This index is a screening convention, not an externally certified trust score. Do not substitute that index for the completion probability used by the cost model. A successful HTTP response with the wrong country remains a failed business outcome.

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
| Scenario success input | 0.95 | 0.8 | 0.75 | Synthetic inputs; per-step continuity in the session repository |
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
| `--pawns-success`, `--honeygain-success`, `--peer2profit-success` | 0.95 / 0.80 / 0.75 | Hypothetical accepted-result fractions; replace with your measurements. |

Actual terminal output captured locally from this repository's default command:

```text
Scenario: trust | HYPOTHETICAL INPUTS | USD | tier=team
+--------------------------+-----------+------------+------------+------------+
| Provider                 | Billed GB | Bandwidth  | Recovery   | Net / month|
+--------------------------+-----------+------------+------------+------------+
| Pawns.app                |    526.32 |    1578.95 |     365.50 |    1944.44|
| Honeygain                |    625.00 |    1875.00 |    1736.11 |    3611.11|
| Peer2Profit Proxy Pools  |    666.67 |    2000.00 |    2314.81 |    4314.81|
+--------------------------+-----------+------------+------------+------------+
Pawns.app recurring offset: $0.00/month
Annual run-rate savings vs Honeygain: $20,000.00
Annual run-rate savings vs Peer2Profit Proxy Pools: $28,444.44
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
- Verify the intended ISP classification using a versioned ASN dataset; residential-looking names alone are insufficient. Set region-specific acceptance thresholds before the pilot. Check opt-in evidence, withdrawal controls and acceptable-use terms before calling any pool ethical. Retain aggregated measurements rather than raw household identifiers.
- Collect equal-sized, interleaved samples for each candidate on the same permitted endpoint. Record timestamp, requested country, observed ASN, observed country, response validity and elapsed time. Resolve ASN using your approved local dataset and state its version. Estimate completion as accepted results / attempts. Report sample sizes and a confidence interval, and stratify by country so a large easy region cannot hide a failing smaller region.
- Replace every assumed buyer price and completion input with a written quote or a measured pilot result; keep the compared billing scope identical.
- Confirm minimum spend, payout conditions, taxes and cancellation terms. A device-sharing account and a proxy-buyer account have different economics.
- Pilot a small allocation, review both cash cost and accepted results, and retain a rollback route until the acceptance threshold is met.

Companion repositories use relative paths so the complete pack can be cloned or moved together:

- [Pawns.app Referral Bonus and Proxy Cost Offset Calculator](../pawns-referral-bonus-proxy-cost-offset-calculator)
- [Datacenter Block Rate vs Pawns.app Residential IPs](../datacenter-block-rate-vs-pawns-residential-ips)
- [Rotating Gateway Session Persistence: Pawns.app Cost Tester](../rotating-gateway-session-persistence-tester)

**[Start a Pawns.app evaluation with your measured budget](https://zelumo.top/pw/1)**. Choose it when the verified economics and permitted workload fit; a synthetic scenario is only a starting point.

### Reuse license

The README and Python source in this directory are offered under the MIT License. Copyright (c) 2026 repository contributors. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, and to permit persons to whom the Software is furnished to do so, subject to including this copyright and permission notice in all copies or substantial portions. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
