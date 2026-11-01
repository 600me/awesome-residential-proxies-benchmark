# Google Workspace and Outlook Warmup Pool Calculator

[![Smartlead.ai comparison](https://img.shields.io/badge/Smartlead.ai-compare_costs-2563eb)](https://is.gd/15s7By)
[![Python 3 standard library](https://img.shields.io/badge/Python_3-standard_library-3776ab)](https://is.gd/15s7By)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](https://is.gd/15s7By)

**[Evaluate Smartlead.ai for your sending workload](https://is.gd/15s7By)**

## 1. The engineering problem and the avoidable invoice

A pool sized for 50 cold messages per mailbox per day can miss its delivery target when those same mailboxes also reserve capacity for warmup. With 22 sending days, 20 messages reserved from a daily budget of 50, and 80% operational availability, one mailbox supplies only 528 modeled cold-send slots per month. Reaching 40,000 sends therefore requires 76 real mailboxes, not the 37 suggested by ignoring both reservations and availability.

At the default $7/account hosting allowance, those 39 missing accounts represent $273/month in unbudgeted provider spend. The sequencer bill can then step up as connected-account slots are exhausted. This model prices Mailshake's cheapest eligible tier at $792/month against $174 for Smartlead.ai: $618/month or $7,416/year of additional software spend at the same pool size. Reply Email Volume is $299/month at the modeled 25,000-contact band, a smaller $125/month difference.

None of these calculations says that a provider permits this traffic or that warmup increases inbox placement. The daily budget, reserved warmup allowance, and availability are planning inputs. Authenticate domains, obtain permission for intended traffic, and use observed bounce and complaint behavior to decide whether to reduce volume. Do not convert a spreadsheet capacity estimate into an automatic sending target.

## 2. Price and technical assumptions you can audit

Prices below are offline industry planning baselines, not a verified current quote. No pricing pages were fetched for this repository, and no current-price claim is made. Annual figures are monthly equivalents of modeled annual commitments. Replace the explicit constants in the single Python file with your contracted rates and limits before a purchase decision. USD totals exclude tax, purchased lead data, and optional enrichment. Unmetered sender connections do not remove send, contact, provider, or fair-use limits.

| Pool parameter | Smartlead.ai Smart | Mailshake | Reply Email Volume | Provider / technical interpretation |
|---|---|---|---|---|
| Software baseline/month | $174/workspace | Sales $99/license; Outreach $49/license | $299 at 25k contacts | Monthly software scenario |
| Connected-account assumption | Unmetered connections | Sales 10; Outreach 2 per license | Unmetered connections | Hosting is purchased separately |
| Modeled human operators | 4 | 4 | 4 | Mailbox slots can exceed human seats |
| Required pool at default load | 76 mailboxes | 76 mailboxes | 76 mailboxes | ceil(40,000 / 528) |
| Google / Outlook allocation | 46 / 30 | 46 / 30 | 46 / 30 | Google share rounded upward |
| Selected software/month | $174 | $792 Sales | $299 | Outreach alternative is $1,862 |
| Shared mailbox hosting/month | $532 | $532 | $532 | Google $7, Microsoft $7 planning baselines |
| Shared domains/month | $28.17 | $28.17 | $28.17 | 26 domains x $13/year / 12 |
| Cold-send capacity/month | 40,128 | 40,128 | 40,128 | Capacity model, not observed sends |
| Active contacts assumption | 13,334 | 13,334 | 13,334 | ceil(target sends / 3) |
| Annual TCO | $8,810 | $16,226 | $10,310 | Annualized unrounded monthly costs |

Spintax rendering, warmup access, agency permissions, API access, and reply detection must be checked against the purchased plan and your test campaign. This comparison assigns no dollar value to assumed inbox-placement gains and makes no claim that any vendor's warmup bypasses provider restrictions. A sequencer subscription does not include ownership of Google or Microsoft mailboxes.

**[Compare the modeled workload with a Smartlead.ai offer](https://is.gd/15s7By)**

## 3. Run the standalone TCO calculator

Requires Python 3.8 or later and only the standard library. No installation, package manager, credentials, network calls, or third-party modules are required. Run from this repository directory; the executable script also supports `./calculate_smartlead_deliverability_tco.py`. All money is denominated in USD. The `--tier` flag selects workload presets, not a promise about vendor packaging.

Required mailboxes = ceil(target / (days x (daily budget - warmup reservation) x availability)). Google accounts = ceil(mailboxes x google share); Outlook receives the remainder. Domains = ceil(mailboxes / 3), a planning density rather than a provider requirement. Hosting is Google accounts x Google cost + Outlook accounts x Outlook cost. Shared monthly infrastructure adds annual domain cost / 12.

The `small`, `growth`, and `scale` workload presets target 15,000, 40,000, and 90,000 cold sends/month. Active contacts are estimated as ceil(target / 3), which assumes three sends per contact, not a measured engagement rate. The script chooses Reply contact-band prices of $179 up to 10k, $299 up to 25k, and $499 up to 50k. It rejects workloads above 150,000 sends or 50,000 modeled contacts rather than silently buying fictitious capacity.

`Cold capacity lost if warmup ignored/month` uses the final pool's reserved allowance: 76 x 22 x 20 x 0.8 = 26,752. It is a capacity difference, not actual bounced mail. The pool's modeled sending capacity is 40,128. Annual totals use the unrounded domain fraction, so multiplying a displayed two-decimal monthly number can differ by a few cents.

| Argument | Default | Effect |
|---|---|---|
| `--tier {small,growth,scale}` | `growth` | Select default target send volume |
| `--target INTEGER` | From preset | Override monthly cold sends, positive |
| `--days INTEGER` | `22` | Sending days, 1 through 31 |
| `--daily-budget INTEGER` | `50` | Total planned daily message allowance |
| `--warmup INTEGER` | `20` | Reserved daily allowance; nonnegative and below budget |
| `--availability NUMBER` | `0.8` | Available fraction, greater than 0 and at most 1 |
| `--google-share NUMBER` | `0.6` | Google mailbox share between 0 and 1 |
| `--google-cost NUMBER` | `7` | Positive Google USD/mailbox/month allowance |
| `--outlook-cost NUMBER` | `7` | Positive Microsoft USD/mailbox/month allowance |
| `--domain-year NUMBER` | `13` | Positive USD/domain/year allowance |
| `--json` | Disabled | Print a JSON capacity and TCO report |

Default invocation and actual locally captured stdout:

```console
$ python3 calculate_smartlead_deliverability_tco.py
Warmup pool: 40000 sends/month; growth
+-------------------------+-------------+-------------+-------------+
| Platform / plan         | Software/mo | Total/mo    | Annual TCO  |
+-------------------------+-------------+-------------+-------------+
| Smartlead Smart         |      174.00 |      734.17 |     8810.00 |
| Mailshake best public   |      792.00 |     1352.17 |    16226.00 |
| Reply Email Volume      |      299.00 |      859.17 |    10310.00 |
+-------------------------+-------------+-------------+-------------+
Required real mailboxes: 76
Google mailboxes: 46
Outlook mailboxes: 30
Domains at 3 mailboxes/domain: 26
Modeled active contacts (3 sends/contact): 13334
Shared hosting/month: 532
Shared domains/month: 28.17
Pool capacity/month: 40128
Cold capacity lost if warmup ignored/month: 26752
Annual savings vs Mailshake best public: $7,416.00
Annual savings vs Reply Email Volume: $1,500.00
USD; offline planning baselines. Verify rates and entitlements before purchase.
https://is.gd/15s7By
```

Additional scenarios:

```bash
python3 calculate_smartlead_deliverability_tco.py --tier small --json
python3 calculate_smartlead_deliverability_tco.py --target 60000 --google-share 0.5
python3 calculate_smartlead_deliverability_tco.py --availability 0.6 --warmup 25
```

`--json` replaces the ASCII table with one JSON object containing `bills`, `annual_savings_usd`, `inputs`, `details`, `assumptions`, `pricing_basis`, and `gateway`. The gateway remains present in JSON mode. `bills` contains monthly software, monthly total, and annual TCO for each row. Negative savings mean Smartlead costs more in that scenario; they are preserved rather than clipped. Preset-derived inputs and formulas are documented above so the result can be reproduced without vendor access.

A successful default invocation exits with status 0. `--help` describes every flag. Invalid numeric inputs or unknown tiers produce an argparse error and nonzero status. Cost allowances and labor inputs must be finite and positive; zero-cost scenarios require editing the corresponding baseline in the script. The script writes no files and does not create subscriptions or modify live campaigns.

## 4. Migration checks and companion repositories

- [ ] Count real licensed mailboxes and domains; exclude aliases from sender-capacity calculations.
- [ ] Replace the provider allowances with the annual-commitment or monthly rates actually purchased. Sequencer billing and hosting billing are independent.
- [ ] Set target sends from the campaign calendar; reserve explicit capacity for warmup and provider interruptions.
- [ ] Validate Google Workspace and Microsoft tenant restrictions, OAuth consent, SPF, DKIM, DMARC, and alignment before reconnecting accounts.
- [ ] Allocate domains and provider mix using measured tenant health. Three mailboxes per domain is an editable model assumption, not a universal safe ratio.
- [ ] Render spintax samples and verify unsubscribes and stop-on-reply before a small pilot campaign.
- [ ] Ramp gradually after observing accepted sends, bounces, complaints, and reply handling. Pause unhealthy accounts rather than filling every modeled slot.
- [ ] Recalculate the pool when availability or daily limits change; do not purchase Mailshake licenses using only the human operator count.

The following independent repositories examine the other three parts of the same sending architecture. Relative links work when the repositories remain beside one another:

- [Reply.io vs Smartlead.ai: The Seat-Tax Breakdown](../reply-io-vs-smartlead-seat-tax-breakdown)
- [Mailshake vs Smartlead.ai: Annual TCO and Migration Payback](../mailshake-vs-smartlead-annual-tco-audit)
- [Enterprise Email Sequencer Webhook Capacity and TCO Benchmarks](../enterprise-email-sequencer-webhook-benchmarks)

**[Start the Smartlead.ai evaluation after checking your numbers](https://is.gd/15s7By)**

### Open-source license

MIT License — Copyright (c) 2026 Repository contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
