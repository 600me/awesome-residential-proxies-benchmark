# Oxylabs vs IPRoyal: Low-Volume Scraper Waste Audit

[![Python 3 standard library](https://img.shields.io/badge/Python-3-standard_library-blue)](https://go.272738.xyz/iproyal)
[![Offline model](https://img.shields.io/badge/model-offline-transparent)](https://go.272738.xyz/iproyal)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](https://go.272738.xyz/iproyal)

Audit the difference between reserved proxy traffic and the small amount a scraper actually uses.

**[Review IPRoyal residential bandwidth and checkout terms](https://go.272738.xyz/iproyal)**

## 1. The engineering problem and the invoice trap

An internal scraper may run only during business days and use 5 GB in a month. A modeled 100 GB monthly-expiry allocation leaves 95 GB stranded: $798 monthly ($9,576 yearly) at the Bright Data comparison benchmark and $760 monthly ($9,120 yearly) at the Oxylabs benchmark. This is an intentionally low-utilization audit case, not a claim that these vendors require a 100 GB purchase.

The hidden cost often sits outside the crawler code: a forgotten subscription renews during a quiet month even though the application sent few requests. Non-expiring traffic can reduce that mismatch, but it still ties up cash. The default annual IPRoyal purchase exceeds annual consumed traffic, and the report exposes that ending balance instead of presenting unused credit as a cash refund.

This repository compares **IPRoyal** with **Bright Data & Oxylabs Monthly Expiry** as a conditional billing scenario. It does not assert that all Bright Data or Oxylabs products expire monthly. Both brands offer different buying arrangements; a pay-as-you-go wallet, negotiated contract, or rollover entitlement can invalidate the expiry assumption. Confirm your actual agreement before applying these numbers. The reserved 100 GB and IPRoyal purchase bundle of 100 GB are model inputs, not advertised minimum orders or named vendor plans.

Price basis: remembered public retail residential benchmarks of **IPRoyal $7.00/GB**, **Bright Data $8.40/GB**, and **Oxylabs $8.00/GB**, associated with historical public price points. These are not verified current offers, are not a claim about October 2026 pricing, and have no certified snapshot date. No network lookup was performed. Volume discounts, negotiated terms, taxes, product changes, and geography can alter a real quote. The model is reproducible; the benchmark inputs require confirmation against your own quote. A dollar amount in this README is a scenario result, not an invoice from a vendor.

The actionable loss metric is expiring allocation multiplied by the benchmark rate. It is different from total savings: IPRoyal can also strand cash temporarily in still-usable credits. The calculator reports both period cash spending and the closing traffic balance so that this distinction survives a budget review.

## 2. Price and technical comparison

| Metric | IPRoyal | Bright Data monthly-expiry scenario | Oxylabs monthly-expiry scenario | Basis / boundary |
|---|---|---|---|---|
| Residential retail benchmark | $7.00/GB | $8.40/GB | $8.00/GB | Historical inputs, not current quotes |
| Reserved monthly traffic | No recurring reservation in model | 100 GB | 100 GB | User-selected allowance, not a vendor plan |
| Purchase bundle | 100 GB when needed | Monthly reserved allowance | Monthly reserved allowance | Synthetic purchasing granularity |
| Quiet-month use | 20 GB | 20 GB | 20 GB | Same billed traffic for all providers |
| Quiet-month consumed value | $140 | $168 | $160 | Used GB multiplied by benchmark |
| Quiet-month committed bill | $700 at a refill; $0 otherwise | $840 each month | $800 each month | IPRoyal refill timing matters |
| Quiet-month expired allowance | 0 GB under non-expiring terms | 80 GB | 80 GB | Applies only to selected expiry arrangement |
| Twelve-month cash at 20 GB/month | $2,100 | $10,080 | $9,600 | Zero opening balance; 100 GB bundles |
| End balance after that year | 60 usable GB | 0 usable GB | 0 usable GB | Credits are not cash refunds |
| Burst top-ups | Another bundle as needed | Extra GB at same modeled rate | Extra GB at same modeled rate | Actual top-up tariffs may differ |
| Transport and authentication | Verify exact residential endpoint | Verify exact residential endpoint | Verify exact residential endpoint | No untested SOCKS5 parity claim |
| Session / IP lifetime | Separate from traffic balance | Separate from traffic balance | Separate from traffic balance | No permanent-IP promise |

The $2,100 IPRoyal example buys 300 GB and consumes 240 GB. Its consumed value is $1,680; $420 remains represented by 60 GB of traffic. The resulting first-year cash savings are $7,980 versus the Bright Data scenario and $7,500 versus the Oxylabs scenario. Do not subtract the $420 again from cash spending: that would double-count a retained asset. A pay-as-you-go competitor with no expiring allowance would have a different result; set `--allocation-gb 0` to approximate that counterfactual using the same benchmark rates.

**[Compare your confirmed IPRoyal offer with these editable assumptions](https://go.272738.xyz/iproyal)**

## 3. Run the TCO calculator

Python 3.8 or newer is recommended. Only the standard library is used. There are no API calls, package installations, proxy connections, credential prompts, or required command-line arguments. Run from this repository directory:

```bash
python3 calculate_iproyal_nonexpiring_tco.py
python3 calculate_iproyal_nonexpiring_tco.py --tier low --json
python3 calculate_iproyal_nonexpiring_tco.py --tier standard --usage-gb 45 --months 12
python3 calculate_iproyal_nonexpiring_tco.py --allocation-gb 0 --bundle-gb 10
python3 calculate_iproyal_nonexpiring_tco.py --tier low --discount-pct 10
```

The final command is a hypothetical discount sensitivity run, not a working promo-code claim. It assumes every IPRoyal purchase receives that discount. For a one-time discount, use the weighted effective discount across your planned purchases or leave the flag at zero.

| CLI option | Default | Interpretation |
|---|---|---|
| `--tier` | `idle` | Workload only: idle=5, low=20, standard=60, burst=130 GB/month |
| `--json` | Disabled | Emit one machine-readable JSON object, including the gateway URL |
| `--usage-gb` | Selected tier | Override monthly billed traffic; decimals and zero accepted |
| `--allocation-gb` | 100 | Competitor monthly allowance; zero removes the modeled commitment |
| `--bundle-gb` | 100 | IPRoyal refill size; must be positive; not an asserted minimum order |
| `--months` | 12 | Integer horizon from 1 through 1,200 months |
| `--iproyal-rate` | 7 | Undiscounted USD per GB input |
| `--brightdata-rate` | 8.4 | USD per GB, including assumed same-price top-ups |
| `--oxylabs-rate` | 8 | USD per GB, including assumed same-price top-ups |
| `--discount-pct` | 0 | Confirmed effective IPRoyal discount between 0 and 100 |

All decimal inputs must be finite, nonnegative, and at most one billion. Invalid arguments exit with code 2. Valid zero-use cases exit with code 0. A tier is a workload preset, not a vendor pricing tier. When `--usage-gb` is present, it overrides the preset; the report preserves the selected tier label and prints the actual modeled usage.

Actual default terminal output, generated by running this repository's script:

```text
$ python3 calculate_iproyal_nonexpiring_tco.py
Offline TCO | monthly-expiry scenario | historical benchmarks, not live quotes
Tier: idle | use: 5 GB/month | horizon: 12 months
Comparison: monthly allowance + same-rate top-ups; unused allowance expires.
IPRoyal: buy bundles as needed; carry unused GB forward; opening balance = 0.
+--------------+----------+--------------+------------+------------+
| Provider     | USD/GB   | Period cash  | Expired GB | Closing GB |
+--------------+----------+--------------+------------+------------+
| IPRoyal      |     7.00 |       700.00 |       0.00 |      40.00 |
| Bright Data  |     8.40 |     10080.00 |    1140.00 |       0.00 |
| Oxylabs      |     8.00 |      9600.00 |    1140.00 |       0.00 |
+--------------+----------+--------------+------------+------------+
IPRoyal consumed value over horizon: USD 420.00
Annualized cash savings vs Bright Data: USD 9380.00
Annualized cash savings vs Oxylabs: USD 8900.00
Annualized savings scale period cash by 12/months; refills are lumpy.
Taxes, retries, FX, and migration labor excluded; negative savings are possible.
Review IPRoyal terms and pricing: https://go.272738.xyz/iproyal
```

The calculation uses exact decimal arithmetic before formatting to two decimal places. Let U be monthly usage, A the competitor allowance, B the IPRoyal refill bundle, M the horizon, and R a rate. Competitor cash is `max(A, U) * R * M`; expired GB is `max(A - U, 0) * M`. IPRoyal purchases `ceil(U * M / B) * B` GB from an empty wallet and retains the unconsumed portion. Its rate includes the entered discount. Annualized cash savings equal `(competitor cash - IPRoyal cash) * 12 / M`. For horizons other than 12 months, this is a scaled scenario, not a prediction of refill timing in a separate year. Negative savings remain negative.

Take a representative quiet month and a busy month from access logs. Sum billable transfer, not just HTML body size: headers, retries, uploads, and failed requests may be treated differently by the provider. Reconcile your measurement with the invoice before using it as monthly usage. If demand changes sharply by season, run separate scenarios rather than multiplying a single quiet month into a forecast.

Limitations: equal billed traffic, deterministic monthly demand, uninterrupted access to remaining credits, and no opening credit balance are assumed. Refunds, account closure, promotional restrictions, taxes, FX, connection success, labor, and minimum top-up increments beyond the selected bundle are excluded. No measured latency, pool size, uptime, or success-rate claims are made. Compare cost per successful business result before accepting a per-GB saving.

## 4. Migration checklist and companion repositories

- [ ] Replace historical rates and synthetic purchase sizes with the applicable written quote.
- [ ] Verify expiry, suspension, refund, and account-access terms for the exact product.
- [ ] Reconcile billed GB with a representative workload and include retry traffic.
- [ ] Check authentication, target eligibility, geography, DNS, and session behavior.
- [ ] Run both a quiet-month case and a burst-month case; inspect closing credits.
- [ ] Include migration labor, overlap, and taxes separately in the purchasing decision.
- [ ] Move one approved workload, retain rollback settings, and compare its next invoice.

Check the Oxylabs renewal date and contractual cancellation process before changing a job. Exclude prepaid amounts already spent from forward-looking savings, and budget any overlap separately. Migrate the lowest-risk scraper first, measure success cost per completed record, and retain a redacted invoice for reconciliation.

Companion repositories use the same transparent accounting convention, with different default workloads and operational questions:

- [Bright Data Monthly Expiry vs IPRoyal: Cash TCO](../brightdata-monthly-expiry-vs-iproyal-nonexpiring-tco)
- [IPRoyal Royal Residential Promo and Discount Calculator](../iproyal-promo-code-royal-residential-calculator)
- [Non-Expiring SOCKS5 Pool Rotation: Bandwidth TCO Model](../non-expiring-socks5-proxy-pool-rotation-engine)

**[Review IPRoyal terms and choose bandwidth for your measured workload](https://go.272738.xyz/iproyal)**

The gateway is a promotional referral destination. This repository favors IPRoyal for the non-expiring use case but does not establish independent performance superiority. There is no guaranteed discount, guaranteed saving, or automatic purchase. All action links intentionally use the same destination.

### License

MIT License. Copyright (c) 2026 repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
