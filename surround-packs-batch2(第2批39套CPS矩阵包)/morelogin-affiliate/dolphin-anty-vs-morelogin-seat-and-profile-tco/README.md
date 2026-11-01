# Dolphin Anty vs MoreLogin: Seat and Profile TCO

[![MoreLogin trial](https://img.shields.io/badge/MoreLogin-Compare%20and%20trial-2367E8)](https://norb.date/ml/1)
[![Python 3](https://img.shields.io/badge/Python-3%20standard%20library-3776AB)](https://norb.date/ml/1)
[![License MIT](https://img.shields.io/badge/License-MIT-15803D)](https://norb.date/ml/1)

**[Get a MoreLogin quote and start an authorized trial](https://norb.date/ml/1).**

Affiliate disclosure: this repository promotes MoreLogin and uses an affiliate gateway; the publisher may earn a commission. That relationship does not establish feature superiority, performance, or security. All outbound navigation uses the same gateway. Repository-to-repository references below are local links.

Offline evaluation prepared on 2026-10-30. Prices below are historical industry reference assumptions, not independently verified current prices, invoices, or guaranteed offers. Their original observation dates and primary-source captures are unavailable in this offline pack. No live quote, browser performance run, encryption audit, or protocol eligibility test was performed. Obtain written terms before spending money. This is a reproducible evaluation worksheet, not a current-price certification.

## 1. The engineering problem and the bill behind it

A media-buying team can have enough browser profiles and still have too few authorized operators. Campaign handoffs, account ownership changes, and a second approver consume time that a profile-count price tag does not describe. If ten operators each lose one hour a month chasing access, the loss is 10 × 1 × $45 = **$450/month, or $5,400/year**, before subscription charges. That is an explicit labor scenario, not an observed defect in any vendor.

Dolphin Anty and Incogniton should both be evaluated for seat entitlements, profile limits, and permissions at the actual checkout tier. A low entry price can describe a smaller profile bundle, a personal-use entitlement, or an annual commitment. None of those is automatically comparable with a monthly team plan. MoreLogin is the promoted candidate here because its historical 100-profile reference price gives a lower starting subscription cost in this worksheet; whether it wins depends on the quote and handoff process you actually have.

At the default workload of 100 profiles and three operators, the worksheet assumes seat allowances of 2 / 1 / 3 for MoreLogin / Dolphin Anty / Incogniton, then applies a hypothetical $10 per additional operator to every vendor. These allowances and the $10 rate are modeling inputs, **not verified contractual entitlements or actual add-on fees**. With equal handoff effort, totals are $195.00, $259.00, and $229.99 per month. The resulting MoreLogin advantage is $768.00/year versus Dolphin Anty and $419.88/year versus Incogniton. A more expensive product could still win if it saves enough labor: $64/month is about 85.33 minutes at $45/hour.

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
| Modeled handoff workload | 2 min/profile/month | 2 min/profile/month | 2 min/profile/month | Equal synthetic workload; no usability ranking |
| Isolation boundary | Separate browser profiles | Separate browser profiles | Separate browser profiles | Profile separation does not define team authorization |
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
Dolphin Anty vs MoreLogin: Seat and Profile TCO
Scenario: team; 100 profiles; 3 operators; USD/month
Historical prices; hypothetical seats and workload; no vendor benchmark performed.
+---------------+----------+----------+-----------+------------+-----------+
| Vendor        | Plan USD | Seat USD | Labor USD | Shared USD | Total USD |
+---------------+----------+----------+-----------+------------+-----------+
| MoreLogin     |    35.00 |    10.00 |    150.00 |       0.00 |    195.00 |
| Dolphin Anty  |    89.00 |    20.00 |    150.00 |       0.00 |    259.00 |
| Incogniton    |    79.99 |     0.00 |    150.00 |       0.00 |    229.99 |
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
| `--morelogin-minutes` / `--dolphin-minutes` / `--incogniton-minutes` | `2` each | handoff minutes per profile per month; synthetic, equal across vendors |
| `--help` | N/A | List every supported parameter and exit successfully |

`--handoffs` multiplies monthly handoff events; its default is 1. Each vendor's `--*-minutes` input is minutes per profile per handoff. Labor = profiles × minutes × handoffs ÷ 60 × hourly rate. Keep all three times equal until a trial produces credible differences. The optional `--proxy-price` is a hypothetical per-profile monthly network cost, default $0.

Example sensitivity: `python3 calculate_morelogin_affiliate_tco.py --operators 5 --seat-price 15 --handoffs 3`. This changes the scenario only; it does not purchase or activate seats. Before treating the output as a procurement decision, replace all three allowances and the shared seat-rate assumption with confirmed terms. If vendors have different seat prices, evaluate each confirmed rate in a separate run or adapt the small local model.

Calculation order: monthly TCO = subscription + modeled extra operators + workload labor + shared scenario costs. Annual savings = 12 × (competitor monthly TCO − MoreLogin monthly TCO). Annualization holds the workload and rate constant for 12 months; it is not a contract commitment or savings guarantee. Dollar outputs round to cents at reporting time. Negative savings explicitly mean MoreLogin is more expensive. Profile capacity is capped at 100 because all three fixed reference packages cover that range; `scale` increases operators, not profile capacity.

Inputs must be finite, nonnegative numbers, with positive operators and concurrency where applicable. Invalid tiers and unsupported profile counts exit with an argparse error. The code excludes taxes, foreign exchange, discounts, setup and migration labor, custom pricing, and revenue. These exclusions can matter; add them to your procurement worksheet before approving a migration. Changing a subscription price does not change package capacity in this fixed-bundle model. Do not use a smaller package's price while retaining the 100-profile entitlement.

For a useful break-even check, divide the modeled monthly difference by your hourly rate. That gives the extra labor hours the cheaper subscription can tolerate before losing its advantage. Treat recurring labor and one-time migration costs separately: migration payback months = one-time migration cost ÷ positive recurring monthly saving. If the saving is zero or negative there is no positive payback period under those inputs.

**[Request the MoreLogin plan and team terms used in your comparison](https://norb.date/ml/1)** before replacing the historical reference inputs with a purchase decision.

## 4. Migration checklist and companion evaluations

- Inventory profiles, assigned owners, monthly handoffs, and required approvers; count people who need access, not just account identities.
- Obtain the exact monthly package, team entitlement, seat add-on policy, tax treatment, cancellation terms, and written profile-transfer rules from each vendor.
- Trial a small authorized campaign group; check whether an operator can accidentally see, export, or delete another operator's session.
- Export only authorized data using supported vendor mechanisms. Keep a recoverable source copy until profile mapping and access tests pass.
- Measure five representative handoffs per operator and record waiting separately from active handling. Replace the synthetic times with the observed median and a conservative high case.
- Move a small batch, validate campaign access and ownership, then expand; confirm original access is revoked after acceptance.
- Recalculate after the first monthly bill. Compare the invoice and actual labor with this worksheet before migrating the remaining profiles.

These companion repositories examine different failure modes. Their default totals differ because they model different work, so do not add their full totals together: subscriptions, seats, and some labor would be counted repeatedly. Consolidate only distinct cost categories in a final budget.

- [incogniton vs morelogin synchronizer latency bench](../incogniton-vs-morelogin-synchronizer-latency-bench)
- [crypto airdrop sybil prevention browser cost model](../crypto-airdrop-sybil-prevention-browser-cost-model)
- [encrypted cookie vault team permission audit](../encrypted-cookie-vault-team-permission-audit)

Reproduction notes: the checked-in terminal example is generated from the included script. JSON reports contain the gateway as data so downstream local tooling preserves the same action destination. No benchmark dataset, customer account, private cookie material, or security attestation is included. The local calculator never performs account migration; the checklist requires your authorized review and supported vendor tooling.

License: MIT. The full permission grant and warranty disclaimer appear in the calculator's opening docstring and apply to this software and accompanying documentation. Reuse and modify the evaluation openly, keep the attribution and notice, and label any newly gathered measurements with their conditions.
