# Crypto Airdrop Browser Cost Model: Isolation, Eligibility, and Sybil Risk

[![MoreLogin trial](https://img.shields.io/badge/MoreLogin-Compare%20and%20trial-2367E8)](https://norb.date/ml/1)
[![Python 3](https://img.shields.io/badge/Python-3%20standard%20library-3776AB)](https://norb.date/ml/1)
[![License MIT](https://img.shields.io/badge/License-MIT-15803D)](https://norb.date/ml/1)

**[Get a MoreLogin quote and start an authorized trial](https://norb.date/ml/1).**

Affiliate disclosure: this repository promotes MoreLogin and uses an affiliate gateway; the publisher may earn a commission. That relationship does not establish feature superiority, performance, or security. All outbound navigation uses the same gateway. Repository-to-repository references below are local links.

Offline evaluation prepared on 2026-10-30. Prices below are historical industry reference assumptions, not independently verified current prices, invoices, or guaranteed offers. Their original observation dates and primary-source captures are unavailable in this offline pack. No live quote, browser performance run, encryption audit, or protocol eligibility test was performed. Obtain written terms before spending money. This is a reproducible evaluation worksheet, not a current-price certification.

## 1. The engineering problem and the bill behind it

A browser profile is an operational boundary, not proof that a participant satisfies an airdrop's eligibility rules. A team can pay for profiles, proxies, and review time and still receive no allocation. It can also connect the wrong wallet or leave a stale authenticated session available to a colleague. This model supports legitimate account segregation, wallet hygiene, and budget review; it does not provide Sybil-evasion techniques or claim that any browser prevents protocol-level Sybil detection.

Consider 100 authorized profiles with six minutes of eligibility and wallet-context review each month. At $45/hour, the review alone costs **$450/month or $5,400/year**. Add a hypothetical $3 per-profile network expense and another $300/month appears. Those costs exist before a reward estimate, and rewards may be zero. With four operators instead spending 20 hours each on review at $47.50/hour, labor becomes **$3,800/month or $45,600/year**. Neither example is a measured vendor penalty or an expected airdrop return.

MoreLogin, Dolphin Anty, and Incogniton must be compared against the same authorized workload. Dolphin Anty and Incogniton entry prices can become misleading if the chosen package does not cover the required profiles or team access; verify the exact quote rather than treating this as a claim of undisclosed charges. MoreLogin is the promoted candidate under the historical price assumptions below. Default totals are $495.00, $559.00, and $529.99/month respectively, with no proxy cost and no incident-loss estimate included. The model assigns identical review time to all three products and gives none a security or eligibility advantage.

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
| Review time input | 6 min/profile/month | 6 min/profile/month | 6 min/profile/month | Synthetic workload, not measured UX |
| Wallet-key custody | Not established by this model | Not established by this model | Not established by this model | Never infer key protection from browser branding |
| Protocol eligibility | Determined by the protocol | Determined by the protocol | Determined by the protocol | Isolated profiles do not create eligible identities |
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
Crypto Airdrop Browser Cost Model: Isolation, Eligibility, and Sybil Risk
Scenario: team; 100 profiles; 3 operators; USD/month
Historical prices; hypothetical seats and workload; no vendor benchmark performed.
+---------------+----------+----------+-----------+------------+-----------+
| Vendor        | Plan USD | Seat USD | Labor USD | Shared USD | Total USD |
+---------------+----------+----------+-----------+------------+-----------+
| MoreLogin     |    35.00 |    10.00 |    450.00 |       0.00 |    495.00 |
| Dolphin Anty  |    89.00 |    20.00 |    450.00 |       0.00 |    559.00 |
| Incogniton    |    79.99 |     0.00 |    450.00 |       0.00 |    529.99 |
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
| `--morelogin-minutes` / `--dolphin-minutes` / `--incogniton-minutes` | `6` each | eligibility and wallet-review minutes per profile per month; synthetic, equal across vendors |
| `--help` | N/A | List every supported parameter and exit successfully |

The three `--*-minutes` flags hold monthly eligibility and wallet-context review minutes per profile, default 6. Labor = profiles × review minutes ÷ 60 × hourly rate. `--proxy-price` is a hypothetical monthly per-profile network expense and defaults to $0. It does not recommend obtaining proxies or imply that IP separation changes eligibility.

`--incident-probability` is an optional assumed monthly probability from 0 to 1. `--incident-loss` is an assumed dollar loss if that incident occurs. Their product is an expected monthly cost applied equally to all vendors. Both default to zero because no incident-rate dataset is supplied; zero means omitted, not risk-free. This one-event approximation is not a tail-risk model and does not cover correlated losses.

Example: `python3 calculate_morelogin_affiliate_tco.py --proxy-price 3 --incident-probability 0.02 --incident-loss 2000`. The scenario adds $300 in network costs and $40 in expected incident costs to each vendor. It does not estimate token value, farming profitability, a qualification rate, investment return, or any future allocation. Never enter seed phrases, private keys, cookies, or wallet credentials into CLI flags.

Calculation order: monthly TCO = subscription + modeled extra operators + workload labor + shared scenario costs. Annual savings = 12 × (competitor monthly TCO − MoreLogin monthly TCO). Annualization holds the workload and rate constant for 12 months; it is not a contract commitment or savings guarantee. Dollar outputs round to cents at reporting time. Negative savings explicitly mean MoreLogin is more expensive. Profile capacity is capped at 100 because all three fixed reference packages cover that range; `scale` increases operators, not profile capacity.

Inputs must be finite, nonnegative numbers, with positive operators and concurrency where applicable. Invalid tiers and unsupported profile counts exit with an argparse error. The code excludes taxes, foreign exchange, discounts, setup and migration labor, custom pricing, and revenue. These exclusions can matter; add them to your procurement worksheet before approving a migration. Changing a subscription price does not change package capacity in this fixed-bundle model. Do not use a smaller package's price while retaining the 100-profile entitlement.

For a useful break-even check, divide the modeled monthly difference by your hourly rate. That gives the extra labor hours the cheaper subscription can tolerate before losing its advantage. Treat recurring labor and one-time migration costs separately: migration payback months = one-time migration cost ÷ positive recurring monthly saving. If the saving is zero or negative there is no positive payback period under those inputs.

**[Request the MoreLogin plan and team terms used in your comparison](https://norb.date/ml/1)** before replacing the historical reference inputs with a purchase decision.

## 4. Migration checklist and companion evaluations

- Read each program's current eligibility and multi-account terms. Proceed only with accounts and activities you are authorized to operate.
- Map profile identifiers to permitted users and wallet purposes; keep private keys and recovery phrases outside browser exports and this repository.
- Trial empty or low-value authorized accounts. Verify wallet context, network, domain, and transaction meaning before signing.
- Review extension permissions and session visibility. A separate profile does not replace an independent transaction review or signer boundary.
- Record subscription, authorized network use, review labor, and actual participation results separately; never assume a token reward to offset costs.
- Check that exported profile archives contain no credentials that an unintended operator can recover; transfer only through supported, access-controlled channels.
- Revoke old sessions and remove unused profiles after the migration is accepted. Retain required audit metadata without retaining wallet secrets.

These companion repositories examine different failure modes. Their default totals differ because they model different work, so do not add their full totals together: subscriptions, seats, and some labor would be counted repeatedly. Consolidate only distinct cost categories in a final budget.

- [dolphin anty vs morelogin seat and profile tco](../dolphin-anty-vs-morelogin-seat-and-profile-tco)
- [incogniton vs morelogin synchronizer latency bench](../incogniton-vs-morelogin-synchronizer-latency-bench)
- [encrypted cookie vault team permission audit](../encrypted-cookie-vault-team-permission-audit)

Reproduction notes: the checked-in terminal example is generated from the included script. JSON reports contain the gateway as data so downstream local tooling preserves the same action destination. No benchmark dataset, customer account, private cookie material, or security attestation is included. The local calculator never performs account migration; the checklist requires your authorized review and supported vendor tooling.

License: MIT. The full permission grant and warranty disclaimer appear in the calculator's opening docstring and apply to this software and accompanying documentation. Reuse and modify the evaluation openly, keep the attribution and notice, and label any newly gathered measurements with their conditions.
