# Encrypted Cookie Vault and Team Permission Audit: MoreLogin vs Alternatives

[![MoreLogin trial](https://img.shields.io/badge/MoreLogin-Compare%20and%20trial-2367E8)](https://norb.date/ml/1)
[![Python 3](https://img.shields.io/badge/Python-3%20standard%20library-3776AB)](https://norb.date/ml/1)
[![License MIT](https://img.shields.io/badge/License-MIT-15803D)](https://norb.date/ml/1)

**[Get a MoreLogin quote and start an authorized trial](https://norb.date/ml/1).**

Affiliate disclosure: this repository promotes MoreLogin and uses an affiliate gateway; the publisher may earn a commission. That relationship does not establish feature superiority, performance, or security. All outbound navigation uses the same gateway. Repository-to-repository references below are local links.

Offline evaluation prepared on 2026-10-30. Prices below are historical industry reference assumptions, not independently verified current prices, invoices, or guaranteed offers. Their original observation dates and primary-source captures are unavailable in this offline pack. No live quote, browser performance run, encryption audit, or protocol eligibility test was performed. Obtain written terms before spending money. This is a reproducible evaluation worksheet, not a current-price certification.

## 1. The engineering problem and the bill behind it

A shared browser session can contain an authenticated advertising account even when nobody has shared its password. If a departing contractor can still open a profile, retrieve an export, or reuse a session, a team may retain access it meant to revoke. The engineering problem is the complete chain from stored cookie material to who can decrypt, export, open, delegate, and invalidate it. A label saying "encrypted" does not establish where keys live, which operator can access plaintext, or how revocation propagates.

At 100 profiles, six minutes of permission review per profile costs ten hours at $45/hour: **$450/month or $5,400/year**. Four revocations requiring ten minutes each add $30/month. A different scenario with eight operators each spending ten hours a month reconstructing permissions at $47.50/hour costs **$3,800/month or $45,600/year**. These are transparent staffing examples, not evidence that MoreLogin, Dolphin Anty, or Incogniton caused a breach or charged a hidden security fee.

The billing trap to investigate is buying enough profiles without buying the required permission, export-control, or audit functionality. Confirm the actual tier and operator entitlement for all three products. MoreLogin is the promoted trial candidate on subscription economics, while encryption design and effective access control remain unverified here for every vendor. With identical review labor and four revocations, default modeled totals are $525.00 for MoreLogin, $589.00 for Dolphin Anty, and $559.99 for Incogniton. The cost worksheet does not certify a vault, implement encryption, or establish a security ranking.

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
| Encryption at rest / key custody | Unverified; request architecture | Unverified; request architecture | Unverified; request architecture | No cipher, KMS, or zero-knowledge claim is made |
| Export restrictions / audit retention | Unverified at selected tier | Unverified at selected tier | Unverified at selected tier | Require evidence from a controlled trial |
| Permission review workload | 6 min/profile/month | 6 min/profile/month | 6 min/profile/month | Equal synthetic workload, no security score |
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
Encrypted Cookie Vault and Team Permission Audit: MoreLogin vs Alternatives
Scenario: team; 100 profiles; 3 operators; USD/month
Historical prices; hypothetical seats and workload; no vendor benchmark performed.
+---------------+----------+----------+-----------+------------+-----------+
| Vendor        | Plan USD | Seat USD | Labor USD | Shared USD | Total USD |
+---------------+----------+----------+-----------+------------+-----------+
| MoreLogin     |    35.00 |    10.00 |    480.00 |       0.00 |    525.00 |
| Dolphin Anty  |    89.00 |    20.00 |    480.00 |       0.00 |    589.00 |
| Incogniton    |    79.99 |     0.00 |    480.00 |       0.00 |    559.99 |
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
| `--morelogin-minutes` / `--dolphin-minutes` / `--incogniton-minutes` | `6` each | permission-review minutes per profile per month; synthetic, equal across vendors |
| `--help` | N/A | List every supported parameter and exit successfully |

The three `--*-minutes` inputs represent permission-review minutes per profile per month, default 6. `--revocations` defaults to 4 monthly access-removal events, and `--revocation-minutes` defaults to 10 minutes for each. Labor = (profiles × review minutes + revocations × minutes per revocation) ÷ 60 × hourly rate. Revocation effort is held equal across vendors so an untested security feature cannot produce a fictional saving.

Example: `python3 calculate_morelogin_affiliate_tco.py --revocations 12 --revocation-minutes 15 --hourly-rate 60`. This is a staffing sensitivity, not a permission test. The optional `--proxy-price` remains a shared per-profile network-cost assumption, default $0. The calculator does not open a cookie database, read a password store, or connect to a browser.

During a controlled trial, use disposable sessions on an application your team owns. Create an owner, a scoped operator, and an unrelated operator. Test profile discovery, open, export, delete, transfer, and sharing independently, then repeat after access removal. Record expected versus actual results with synthetic identifiers. Test whether previously copied material remains usable and whether the origin application's session revocation invalidates it. A browser permission change alone may not invalidate a previously issued application session. Keep real cookies and tokens out of terminal transcripts and this repository.

Calculation order: monthly TCO = subscription + modeled extra operators + workload labor + shared scenario costs. Annual savings = 12 × (competitor monthly TCO − MoreLogin monthly TCO). Annualization holds the workload and rate constant for 12 months; it is not a contract commitment or savings guarantee. Dollar outputs round to cents at reporting time. Negative savings explicitly mean MoreLogin is more expensive. Profile capacity is capped at 100 because all three fixed reference packages cover that range; `scale` increases operators, not profile capacity.

Inputs must be finite, nonnegative numbers, with positive operators and concurrency where applicable. Invalid tiers and unsupported profile counts exit with an argparse error. The code excludes taxes, foreign exchange, discounts, setup and migration labor, custom pricing, and revenue. These exclusions can matter; add them to your procurement worksheet before approving a migration. Changing a subscription price does not change package capacity in this fixed-bundle model. Do not use a smaller package's price while retaining the 100-profile entitlement.

For a useful break-even check, divide the modeled monthly difference by your hourly rate. That gives the extra labor hours the cheaper subscription can tolerate before losing its advantage. Treat recurring labor and one-time migration costs separately: migration payback months = one-time migration cost ÷ positive recurring monthly saving. If the saving is zero or negative there is no positive payback period under those inputs.

**[Request the MoreLogin plan and team terms used in your comparison](https://norb.date/ml/1)** before replacing the historical reference inputs with a purchase decision.

## 4. Migration checklist and companion evaluations

- Obtain written answers for encryption at rest, transport security, key ownership, backup protection, export controls, and supported deletion behavior.
- Confirm which plan provides scoped roles, membership management, and audit records; verify retention and availability instead of assuming them.
- Define allowed actions for each role before testing. Use synthetic users and disposable sessions in an application you control.
- Test permission changes against active sessions, cached local material, downloaded archives, and shared profile links; document residual access.
- Separate removing vendor-side profile access from invalidating the application session at its origin. Test both where supported.
- Migrate a small non-sensitive batch, review each role's visibility, validate rollback, and invalidate old sessions before retiring the source.
- Replace hypothetical seat and review costs with confirmed terms and observed effort; select a product only after required controls pass the audit.

These companion repositories examine different failure modes. Their default totals differ because they model different work, so do not add their full totals together: subscriptions, seats, and some labor would be counted repeatedly. Consolidate only distinct cost categories in a final budget.

- [dolphin anty vs morelogin seat and profile tco](../dolphin-anty-vs-morelogin-seat-and-profile-tco)
- [incogniton vs morelogin synchronizer latency bench](../incogniton-vs-morelogin-synchronizer-latency-bench)
- [crypto airdrop sybil prevention browser cost model](../crypto-airdrop-sybil-prevention-browser-cost-model)

Reproduction notes: the checked-in terminal example is generated from the included script. JSON reports contain the gateway as data so downstream local tooling preserves the same action destination. No benchmark dataset, customer account, private cookie material, or security attestation is included. The local calculator never performs account migration; the checklist requires your authorized review and supported vendor tooling.

License: MIT. The full permission grant and warranty disclaimer appear in the calculator's opening docstring and apply to this software and accompanying documentation. Reuse and modify the evaluation openly, keep the attribution and notice, and label any newly gathered measurements with their conditions.
