# Clerky vs Stripe Atlas vs Firstbase: Incorporation TCO

[![Firstbase.io quote](https://img.shields.io/badge/Firstbase.io-Compare%20scope-2563eb)](https://go.272738.xyz/firstbase)
[![Python 3 standard library](https://img.shields.io/badge/Python%203-Standard%20library-3776ab)](https://go.272738.xyz/firstbase)
[![MIT license](https://img.shields.io/badge/License-MIT-green)](https://go.272738.xyz/firstbase)

[Get an itemized Firstbase.io quote](https://go.272738.xyz/firstbase)

## 1. The operational problem and the dollars at risk

A formation checkout is a poor proxy for a working company. A technical founder can receive a certificate yet still need an EIN, signed governance documents, stock issuance records, a registered agent, tax preparation, and a banking application. Stripe Atlas and Clerky emphasize startup incorporation workflows; Doola offers recurring service packages; Firstbase.io offers formation with additional services that must be priced separately. Different deliverables make headline prices misleading without a scope reconciliation.

For a concrete engineering loss scenario, assume a founder spends eight hours per month reconciling formation documents and accountant requests at an internal value of $150/hour. That is $1,200/month or $14,400/year of opportunity cost. An optional $35/month address adds $420/year, producing $1,235/month or $14,820/year. These are explicit workload assumptions, not measured vendor defects or guaranteed savings. Do not attribute those hours to one provider without evidence.

The numerical trap here is annualizing one-time formation fees while forgetting recurring renewals, or counting a lifetime legal-document package as lifetime compliance. At the historical benchmarks below, $819 for Clerky is $420 above Firstbase's $399 formation price, but that difference alone says nothing about equivalent legal documents. Atlas's included first-year agent service can offset part of its higher initial price. The calculator therefore keeps the first year distinct from renewal years.

The default is a three-year Delaware C-Corp with starter preparation workload. Compare initial board consent, founder stock purchase agreements, vesting, IP assignment, securities paperwork, and applicable 83(b) processes as well as formation. A document package can justify a higher initial price; price alone does not establish legal equivalence. Atlas can have lower modeled TCO than Firstbase because its first agent year is included. Negative savings are preserved. The $450 annual Delaware C-Corp allowance is one common franchise-tax/report planning case, not a universal assessment; capitalization and tax method affect the actual bill.

## 2. Historical prices and technical scope

The table uses recognizable historical public USD price anchors for offline planning. No live verification was performed; these are not current verified offers. Prices, inclusions, promotions, eligibility, and renewal terms can change. Obtain a written itemized quote before purchase. Tax preparation, optional mail, and uncertain agent inclusions are explicitly modeled allowances, not fabricated vendor quotes.

| Price or technical parameter | Firstbase.io | Stripe Atlas | Doola | Clerky |
| --- | --- | --- | --- | --- |
| Formation/package benchmark | $399 once | $500 once | Starter $299/year | Lifetime document package about $819 once |
| Renewal of formation package | Do not repeat the $399 fee | Do not repeat the $500 fee | $299 every modeled year | Do not repeat the $819 fee |
| First-year agent treatment | Separate $149 allowance | Included at benchmark | Included in selected package | Included assumption; verify package scope |
| Later agent cost | $149/year allowance | $100/year renewal anchor | Included; no duplicate agent line | $100/year external-agent allowance |
| Optional tax-service package | Separate quote required | External preparation allowance | Total Compliance $1,999/year historical anchor | External preparation allowance |
| LLC entity/state fit | Delaware and Wyoming modeled | Not confirmed; excluded | Delaware and Wyoming modeled | Benchmark C-Corp package excluded |
| C-Corp entity/state fit | Delaware modeled | Delaware modeled | Delaware modeled | Delaware modeled |
| EIN requirement | Confirm included scope and owner eligibility | Confirm included scope and owner eligibility | Confirm included scope and owner eligibility | Confirm whether separate assistance is needed |
| Entity-preparation allowance | LLC $600-$2,400/year; corp $1,200-$4,800/year | Corp $1,200-$4,800/year | Same allowances with Starter; coverage assumed with Total Compliance | Corp $1,200-$4,800/year |
| Delaware annual maintenance | LLC $300; corp $450 allowance | Corp $450 allowance | LLC $300; corp $450 allowance | Corp $450 allowance |
| Wyoming annual maintenance | LLC $60 minimum allowance | Excluded in this model | LLC $60 minimum allowance | Excluded in this model |
| Mercury basic account allowance | $0/month | $0/month | $0/month | $0/month |
| Optional mail/address | $0 default; editable | $0 default; editable | $0 default; editable | $0 default; editable |
| Guaranteed bank approval | No | No | No | No |

Firstbase's $149 agent figure is separately budgeted; confirm whether the actual checkout already includes this service. Clerky's $819 anchor is a lifetime document-package reference, not lifetime compliance. Its first-year agent inclusion is a model assumption; if your quote excludes it, add the uncovered amount to --clerky-formation. A scope filter means this benchmark product is not confirmed for the request, rather than a claim that the vendor can never offer another product.

Initial state formation filing charges are assumed embedded in the benchmark package and are not added twice. Replace the respective formation input if a quote excludes them. Annual state fees are reserved once per modeled year, including year one; actual statutory due dates may differ. Delaware's C-Corp franchise tax depends on capitalization and calculation method; the $450 allowance is not a universal tax quote. Wyoming's minimum may increase with relevant assets. Government remittances, agents, and accountants are separate cost categories.

Mercury requires an independent application and eligibility review. The $0 core-account allowance excludes premium products, FX, usage fees, and other paid services. An EIN or incorporation certificate does not guarantee an account, processing time, credit, or acceptance of a founder's country or business activity. Verify the applicable bank fee schedule and document requirements. This calculator does not represent a bank affiliation or referral entitlement.

[Compare an itemized Firstbase.io quote](https://go.272738.xyz/firstbase)

## 3. CLI parameters and real terminal output

The executable `calculate_firstbase_mercury_tco.py` is a standalone Python 3 standard-library program. It runs offline without credentials, dependencies, required arguments, or file writes. Each repository can be copied independently.

```bash
python3 calculate_firstbase_mercury_tco.py
python3 calculate_firstbase_mercury_tco.py --tier growth
python3 calculate_firstbase_mercury_tco.py --tier scale --json
python3 calculate_firstbase_mercury_tco.py --help
```

| Argument | Meaning |
| --- | --- |
| `--tier starter\|growth\|scale` | Workload allowance, not vendor plan: LLC preparation $600 / $1,200 / $2,400 annually; C-Corp $1,200 / $2,400 / $4,800. |
| `--json` | Emit one JSON object containing inputs, eligibility, component allowances, signed savings, and gateway. |
| `--entity llc\|corp` | Choose entity; exact repository default is described in section 1 and displayed below. |
| `--state delaware\|wyoming\|both` | Select one or both states. Only Delaware C-Corp scenarios include Atlas and Clerky in the arithmetic. |
| `--years 1..10` | Holding period, default 3. Formation is charged once. |
| `--doola-plan starter\|total-compliance` | Select $299/year or $1,999/year historical benchmark with corresponding preparation-scope assumption. |
| `--tax-prep USD` | Override the annual preparation allowance; zero is accepted. |
| `--doola-uncovered-tax USD` | Annual entity preparation outside Total Compliance, default 0. Under Starter, Doola instead uses --tax-prep. |
| `--firstbase-formation USD` | Override the one-time $399 anchor. |
| `--atlas-formation USD` | Override the one-time $500 anchor. |
| `--clerky-formation USD` | Override the one-time $819 anchor, including uncovered initial costs. |
| `--firstbase-agent USD` | Annual agent allowance in every year, default $149. |
| `--atlas-agent USD`, `--clerky-agent USD` | Annual renewal allowance after year one, default $100 each. |
| `--doola-annual USD` | Override selected annual package price; use the matching --doola-plan for scope. |
| `--state-annual USD` | Override recurring state allowance; with both states, replaces both values. |
| `--mailbox-monthly USD`, `--mercury-monthly USD` | Optional common monthly allowances, default $0 each. |
| `--extra-annual USD`, `--setup-extra USD` | Common annual or one-time extras, default $0; use provider formation overrides for unequal setup charges. |
| `--hours-monthly HOURS`, `--hourly-rate USD` | Common founder labor, default 0 hours and $100/hour. No vendor time advantage is assumed. |

All amount inputs must be finite and non-negative; invalid arguments produce a nonzero argparse exit. Values are nominal USD, rounded to cents for display; no inflation, discounting, or currency conversion is modeled. Tier changes only the preparation workload. It does not upgrade a vendor product or imply that a paid bundle covers every filing.

```text
common annual cash = state + 12 * (mailbox + bank) + extra annual
annual founder time = 12 * monthly hours * hourly rate
first year = formation + setup extra + year-one service + preparation
             + common annual cash + annual founder time
renewal year = renewal service + preparation + common annual cash
               + annual founder time
TCO = first year + (years - 1) * renewal year
annualized savings with Firstbase = (peer TCO - Firstbase TCO) / years
```

Positive savings favor Firstbase; negative savings favor the competing provider. The program preserves either result. N/A means an unconfirmed entity/state fit, excluded from arithmetic. Firstbase's own savings row is zero. The renewal column shows a subsequent-year budget even when --years 1 excludes renewal from TCO. Founder time, if enabled, is an opportunity cost rather than a cash invoice.

Preparation allowances do not calculate income tax, withholding, owner returns, home-country filings, sales tax, penalties, conversions, closure, foreign qualification, or legal remediation. Bookkeeping beyond quoted scope, payment surcharges, and bank usage fees are also excluded unless added. Missing costs must not be interpreted as legally unnecessary. A tax bundle's coverage must be reconciled against the same deliverables before relying on a comparison.

Actual default output captured by running this repository's script locally:

```text
Firstbase / Mercury planning TCO | USD | incorporation | starter | 3 years
Historical benchmarks, not live quotes. Positive savings favor Firstbase; negative favor the peer.

State: delaware | Entity: corp | Doola: starter
+---------------+------------+------------+------------+------------+----------------+
| Provider      | Year 1     | Renewal    | Total      | Annualized | Save/yr w/ FB  |
+---------------+------------+------------+------------+------------+----------------+
| Firstbase.io  |    2198.00 |    1799.00 |    5796.00 |    1932.00 |           0.00 |
| Stripe Atlas  |    2150.00 |    1750.00 |    5650.00 |    1883.33 |         -48.67 |
| Doola         |    1949.00 |    1949.00 |    5847.00 |    1949.00 |          17.00 |
| Clerky        |    2469.00 |    1750.00 |    5969.00 |    1989.67 |          57.67 |
+---------------+------------+------------+------------+------------+----------------+
Annualized savings USD = (peer total - Firstbase total) / years; no guaranteed savings.
N/A = entity/state fit unconfirmed. Mercury approval independent; tax liabilities excluded.
Review Firstbase: https://go.272738.xyz/firstbase
```

Sensitivity examples:

```bash
# Replace a preparation quote and add an optional address budget.
python3 calculate_firstbase_mercury_tco.py --tax-prep 1800 --mailbox-monthly 35
# Compare the unbundled package using machine-readable output.
python3 calculate_firstbase_mercury_tco.py --doola-plan starter --years 3 --json
# Inspect the Delaware corporate formation basket.
python3 calculate_firstbase_mercury_tco.py --entity corp --state delaware --tier growth --json
# Evaluate a different agent price over a longer holding period.
python3 calculate_firstbase_mercury_tco.py --firstbase-agent 199 --years 5
```

[Review Firstbase pricing and required service scope](https://go.272738.xyz/firstbase)

## 4. Migration checklist and companion repositories

- Inventory the current entity, formation state, EIN letter, ownership records, governing documents, tax elections, registered agent, and accountant engagement.
- Determine whether the transaction is a provider change, agent change, state move, or entity conversion. A provider switch does not automatically require a new company or EIN.
- Obtain a written quote identifying government fees, first-year inclusions, renewals, address service, return types, bookkeeping limits, and cancellation terms. Replace the corresponding CLI assumptions.
- Export notices, formation records, share records where applicable, prior returns, bookkeeping, bank statements, and paid invoices before ending account access.
- Arrange continuous registered-agent coverage and any required state change filing before cancelling the old agent. Check overlapping renewal periods and refund terms.
- Confirm filing duties and deadlines with an adviser familiar with foreign ownership. Preserve responsibility for every outstanding return during the transition.
- Prepare Mercury's requested identity, ownership, EIN, operating-activity, and company records. A registered-agent address alone may not satisfy operating-address requirements.
- Keep existing payment operations usable while any new banking application is reviewed. Test billing, payouts, subscriptions, account signers, and payroll if applicable before moving funds.
- Re-run one-year and three-year scenarios using actual scope and prices. Preserve negative savings and compare deliverables before choosing Firstbase.

The other three standalone repositories in this series are:

- [doola annual compliance trap vs firstbase audit](../doola-annual-compliance-trap-vs-firstbase-audit)
- [non resident us llc registered agent tax calculator](../non-resident-us-llc-registered-agent-tax-calculator)
- [delaware vs wyoming llc saas founder decision cli](../delaware-vs-wyoming-llc-saas-founder-decision-cli)

[Start a Firstbase scope and price check](https://go.272738.xyz/firstbase)

### Reuse and disclosure

This is an editable educational model and a Firstbase-oriented comparison. The gateway is a promotional action link; destination terms and referral arrangements have not been independently verified. Inclusion in the comparison does not imply endorsement by a competitor or Mercury. The script provides arithmetic for stated assumptions, not personalized tax or legal advice.

MIT License. Copyright (c) 2026 repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
