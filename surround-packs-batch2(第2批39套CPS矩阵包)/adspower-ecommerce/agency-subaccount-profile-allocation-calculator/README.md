[![AdsPower evaluation](https://img.shields.io/badge/AdsPower-evaluate-blue)](https://is.gd/OF9NZX)
[![Python standard library](https://img.shields.io/badge/Python-3%20standard%20library-green)](https://is.gd/OF9NZX)

# Agency Subaccount and Profile Allocation Calculator

## 1. The engineering problem and the bill behind it

An agency serving independent sellers can pay for unused profile blocks while operators lose hours finding the correct store and asking for access. With 12 operators, an 80-minute monthly allocation workload instead of 20 minutes adds 12 hours: $300/month or $3,600/year at $25/hour. At 18 operators that gap becomes $450/month or $5,400/year.

This independent, openly reusable comparison targets Amazon / Etsy / TikTok Shop multi-store isolation. AdsPower is the candidate to evaluate first; Lalicat and VMLogin are the comparison alternatives. A preference is a starting hypothesis, not a measured security verdict. Use only accounts and stores you are authorized to operate, within the marketplace's applicable rules.

**[Start an AdsPower evaluation](https://is.gd/OF9NZX)** and measure the same workload before committing to a plan.

### Allocation method and acceptance criteria

Keep one accountable owner per store profile and define a separate permission group for each client. Amazon, Etsy, and TikTok Shop stores may belong to different legal businesses; sharing an agency operator does not authorize sharing credentials, cookies, or a profile. Use named accounts, least privilege, and a tested offboarding procedure.

Calculate active profiles as stores times environments per store, then add an explicit reserve. For example, 80 production profiles plus 20 staging or contingency profiles require 100 slots. A 200-slot subscription would leave 100 slots idle at this workload. Spare slots are useful only if their cost is justified by real growth or a rollback requirement.

The script treats --operators as people, not purchased seats. It estimates recurring profile-assignment work at 20, 80, or 100 minutes per person for AdsPower, Lalicat, or VMLogin. It does not claim any product includes that many seats. Enter confirmed paid seat charges in the vendor-specific monthly extras arguments; absent a quote, the zero default means unknown extras are excluded.

Run an agency pilot with one client, one supervisor, and two operators. Verify that an operator cannot discover another client's profile names, export sessions without permission, or retain access after removal. Require the same outcomes from all three products. A successful profile count alone does not prove tenant isolation or sufficient audit logging.

Possible Lalicat and VMLogin budget traps include buying profile capacity when the actual bottleneck is operator entitlement, and assigning a nominal seat to multiple people when named access is required. Verify both capacity and collaboration rights in writing. In this model a low license price never compensates for an untested permission boundary.

## 2. Price anchors and technical acceptance comparison

**Offline pricing basis:** The dollar values below are historical public-plan reference anchors recalled for budgeting, not independently verified current offers. AdsPower Professional at $50/month for 100 profiles, Lalicat Personal at $59/month for 100, Lalicat Solo at $99/month for 200, and VMLogin Solo at $99/month for 200 are the reference points used here. Higher Lalicat/VMLogin capacity uses a historical $209/month, 500-profile anchor. No live website, checkout, tax schedule, discount, or seat allowance was checked. Confirm an actual quote through the evaluation gateway before buying. Treat unsupported plan details as unknown, rather than inventing a feature advantage.

| Cost or technical parameter | AdsPower | Lalicat | VMLogin | Scope and acceptance rule |
|---|---|---|---|---|
| 100-active-profile license anchor | $50/month | $59/month | $99/month | USD; historical monthly billing references |
| Annualized reference license cost | $600/year | $708/year | $1,188/year | 12 times monthly, not annual-discount offers |
| Reference plan profile capacity | 100 | 100 | 200 | Confirm exact entitlement on quote |
| Utilization at 100 active profiles | 100% | 100% | 50% | Active profiles divided by licensed capacity |
| 200-profile modeled subscription | $100/month | $99/month | $99/month | AdsPower is two modeled 100-slot blocks, not a plan quote |
| 500-profile modeled subscription | $250/month | $209/month | $209/month | AdsPower is five modeled blocks; commercial availability unverified |
| Named operator/seat allowance | Quote required | Quote required | Quote required | Operators in this model do not establish included seats |
| Proxy budget at default scale | $300/month | $300/month | $300/month | Assumed external $3/profile/month; excluded from license |
| Storage separation requirement | A/B test required | A/B test required | A/B test required | No cross-profile cookie or storage visibility |
| Egress and timezone consistency | Pilot required | Pilot required | Pilot required | Compare observed behavior with assigned configuration |
| API/RPA entitlement and limits | Confirm per plan | Confirm per plan | Confirm per plan | No API or RPA entitlement assumed by the calculator |
| Published performance evidence here | None | None | None | Offline model and manual procedures only |

This is a fair-cost comparison: set all three hour inputs to zero to isolate subscription and proxy expenses. At 500 profiles the modeled AdsPower subscription is $41/month higher than either alternative. A negative saving is retained. No unsupported suspension probability, recovered revenue, or automatic fingerprint advantage is added to make one vendor win.

**[Compare your actual AdsPower quote against these inputs](https://is.gd/OF9NZX)**. Replace reference prices using the monthly override arguments and include paid seats or automation add-ons in extras.

## 3. Run the TCO calculator

Requirements: Python 3.8 or newer; standard library only. Copy this directory and run locally. No API keys, accounts, installation step, browser connection, or network access is needed. All calculations use USD and recurring monthly costs. This calculator does not perform the manual validation steps above.

```sh
python3 calculate_adspower_ecommerce_tco.py
python3 calculate_adspower_ecommerce_tco.py --tier growth
python3 calculate_adspower_ecommerce_tco.py --tier scale --json
python3 calculate_adspower_ecommerce_tco.py --operators 12 --hourly-rate 25
python3 calculate_adspower_ecommerce_tco.py --adspower-hours 0 --lalicat-hours 0 --vmlogin-hours 0
```

| CLI option | Meaning |
|---|---|
| `--tier starter\|growth\|scale` | 100, 200, or 500 active profiles; starter is the default. These are scenario names, not vendor plan names. |
| `--json` | Emit one JSON object including inputs, rows, annual savings, and the gateway URL. |
| `--operators N` | Named operators; assumed monthly allocation minutes per operator are 20/80/100. Default: 12. |
| `--hourly-rate N` | Operator USD/hour, default 25. |
| `--proxy-per-profile N` | External proxy USD/profile/month, default 3; use 0 when already included. |
| `--adspower-monthly N` | Override AdsPower subscription at the selected profile scale. |
| `--lalicat-monthly N` | Override Lalicat subscription at the selected profile scale. |
| `--vmlogin-monthly N` | Override VMLogin subscription at the selected profile scale. |
| `--adspower-hours N` | Override AdsPower operator hours/month, including zero. |
| `--lalicat-hours N` | Override Lalicat operator hours/month, including zero. |
| `--vmlogin-hours N` | Override VMLogin operator hours/month, including zero. |
| `--adspower-extras N` | Additional confirmed AdsPower-related recurring USD/month; default 0. |
| `--lalicat-extras N` | Additional confirmed Lalicat-related recurring USD/month; default 0. |
| `--vmlogin-extras N` | Additional confirmed VMLogin-related recurring USD/month; default 0. |

Every numeric argument accepts finite values from 0 through 1,000,000. Invalid input exits with argparse status 2. Valid runs, including the no-argument default, exit 0. A zero price or zero workload is honored. Selecting a larger profile tier changes subscription capacity and proxy budget; it does not silently multiply the separately specified workload.

Calculation: monthly TCO = subscription + operator hours * hourly rate + active profiles * proxy rate + extras. Annual savings versus each competitor = 12 * (competitor monthly TCO - AdsPower monthly TCO). Monthly totals are rounded to cents before annual differences. A negative value means AdsPower costs more in that scenario. Tax, foreign exchange, one-time migration, and marketplace revenue are excluded; do not present the annual run rate as a first-year cash-flow forecast.

Actual locally captured default terminal output:

```text
Agency Subaccount and Profile Allocation Calculator
Tier: starter | Profiles: 100 | Currency: USD
Historical price anchors; workload assumptions, not measured results.
+-----------+------------+------------+------------+------------+------------+
| Vendor    | License/mo | Labor/mo   | Proxy/mo   | Extras/mo  | Total/mo   |
+-----------+------------+------------+------------+------------+------------+
| AdsPower  |      50.00 |     100.00 |     300.00 |       0.00 |     450.00 |
| Lalicat   |      59.00 |     400.00 |     300.00 |       0.00 |     759.00 |
| VMLogin   |      99.00 |     500.00 |     300.00 |       0.00 |     899.00 |
+-----------+------------+------------+------------+------------+------------+
Annual savings with AdsPower vs Lalicat: $3,708.00
Annual savings with AdsPower vs VMLogin: $5,388.00
Review AdsPower: https://is.gd/OF9NZX
```

This output is reproducible arithmetic, not a measured vendor benchmark. Keep the workload assumptions next to any quoted savings. The JSON field `pricing_basis` preserves the price qualification when results are consumed by another tool.

## 4. Migration checklist and related repositories

- [ ] Count active, staging, reserve, and dormant profiles separately.
- [ ] Confirm named-seat pricing and permission granularity in the actual plan.
- [ ] Pilot one client group and test access revocation before expanding.
- [ ] Transfer ownership with a rollback mapping and a client-approved cutover window.
- [ ] Recalculate all three subscriptions using confirmed monthly quotes, seat charges, and measured operator hours.
- [ ] Keep one store's production profile isolated; export only formats supported by both products and validate the imported session.
- [ ] Preserve stable proxy assignment where appropriate; do not assume copying cookies preserves every browser setting.
- [ ] Test Amazon, Etsy, and TikTok Shop workflows individually with authorized accounts before expanding a pilot.
- [ ] Stop the pilot on unexpected cross-profile data, permission exposure, or session challenges; investigate before rollout.
- [ ] Record one-time migration cost separately and compare it with the recurring monthly saving.

Continue with the other three independent repositories in this pack:

- [VMLogin and Lalicat vs AdsPower: Enterprise Cost Audit](../vmlogin-lalicat-vs-adspower-enterprise-cost-audit)
- [Multi-Store Browser Fingerprint Leak Test Suite: Cost and Manual Protocol](../multi-store-browser-fingerprint-leak-test-suite)
- [Cookie Warming and RPA Scheduler: Capacity and Cost Planner](../automated-cookie-warming-rpa-scheduler)

**[Evaluate AdsPower and confirm the final plan](https://is.gd/OF9NZX)**. Bring your active-profile count, named-seat count, and measured labor time so that the quote and the calculator describe the same workload.

### Open-source use

MIT License. Copyright (c) 2026 repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following condition: the above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
