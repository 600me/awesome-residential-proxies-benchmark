# Audiobook Publishing: Character and Credit TCO Calculator

[![Offline Python 3](https://img.shields.io/badge/Python-3_standard_library-3776AB)](https://is.gd/zhGCok)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://is.gd/zhGCok)
[![Evaluate ElevenLabs](https://img.shields.io/badge/Evaluate-ElevenLabs-black)](https://is.gd/zhGCok)

**[Evaluate ElevenLabs for this production workflow](https://is.gd/zhGCok)**

An independent, open-source planning repository for professional voice cloning and long-form audio production. All calculations run locally with Python 3 and its standard library. No account, API key, audio upload, network request, or third-party package is required. Pack: `elevenlabs-audiobook`.

## 1. The production problem and the money at risk

A publisher budgeting only the first narration pass misses the most expensive part of a long manuscript: corrections after author review. A 3,000,000-character monthly catalog with 20% regenerated material consumes 3,600,000 modeled credits at one credit per character. Against a 2,000,000-credit historical ElevenLabs Scale allowance, that creates $288 of modeled overage on top of the $330 subscription. An estimate that stops at the subscription understates service spending by $288 each month, or $3,456 each year.

With four assumed ElevenLabs production hours at $60 per hour, the default full-workflow estimate is $858 monthly. The historical WellSaid seat plus twenty-two labor hours produces a $1,519 floor: a $661 monthly or $7,932 annualized difference. Amazon Polly Neural at $16 per million billable characters costs just $57.60 for generation; twenty-four assumed production hours bring its scenario total to $1,497.60. The resulting $639.60 monthly difference comes from workflow assumptions, not from an assertion that ElevenLabs has a lower API price.

The billing traps to audit are mismatched units, unused per-account allowances, regeneration, account access, and manual operations. These are transparent scenario risks, not allegations of undisclosed vendor charges. A WellSaid subscription is not interchangeable with a per-character API tariff; a low Polly synthesis bill does not purchase an editorial workflow. Amazon Polly Studio is the requested comparison label in this pack. The priced AWS service here is **Amazon Polly**, using its Neural engine; no separate product or SKU named "Polly Studio" is assumed.

**[Use the ElevenLabs evaluation gateway, then check the applicable quote](https://is.gd/zhGCok)**

## 2. Price anchors and technical comparison

These are **historical public list-price anchors**, used as editable inputs rather than verified current offers. This repository was assembled offline on 2026-10-30; no live pricing page was fetched. Source provenance is the historically published ElevenLabs Pricing page, Amazon Polly Pricing page, and legacy WellSaid Labs Pricing page. The exact capture dates are unavailable, so do not treat these values as a dated vendor quote. First-month promotions and annual-contract discounts are excluded. All amounts are USD before tax.

| Metric | ElevenLabs | Amazon Polly Studio / Polly | WellSaid Labs | Budget interpretation |
| --- | --- | --- | --- | --- |
| Entry paid anchor | Starter: $5/month, 30,000 credits | Standard: $4 / million characters | Legacy Maker: $49/user/month | Historical prices, not equal feature bundles |
| Creator anchor | $22/month, 100,000 credits | Neural: $16 / million characters | Legacy Creative: $99/user/month | Calculator selects Neural by default |
| Professional anchor | Pro: $99/month, 500,000 credits | Long-Form: $100 / million characters | Legacy Business: $199/user/month | WellSaid default is a subscription floor |
| Higher-volume anchor | Scale: $330/month, 2,000,000 credits | Generative: $30 / million characters | Enterprise: custom quote | AWS engines have different voices and availability |
| Modeled extra usage | Creator $0.30; Pro $0.24; Scale $0.18 / 1,000 credits | Selected engine rate applies to billable characters | No invented character-overage tariff | Confirm eligibility and caps before purchase |
| Billing unit | Model-dependent credits; default 1 credit / character | Billable text characters; supported SSML tags excluded | Seats plus plan-specific workflow limits | Downloads, projects, and characters differ |
| Voice cloning | Instant and Professional options; eligibility and verification apply | Stock engines; custom Brand Voice requires a separate arrangement | Stock AI voices; custom voice options require a quote | These are not equivalent cloning SKUs |
| Speech markup | Engine-specific controls; no general Polly SSML compatibility | Engine-specific SSML support | Studio and contract-dependent controls | Budget a tested translation step |
| Author access | Calculator buys one selected subscription per active seat | IAM access; synthesis billed by usage | Legacy Business price multiplied by seats | No pooled-credit or team-seat entitlement is promised |
| API assumptions | Selected plan and model terms must permit the intended workflow | Usage-based API; infrastructure is additional | API access may require a different contract | A $199 historical seat does not establish API rights |
| Quality evidence | Must be measured on your corpus | Must be measured on your corpus | Must be measured on your corpus | No observed MOS or vendor ranking is supplied |

The three ElevenLabs overage anchors are scenario rates contingent on the relevant plan allowing additional usage. Some models consume a different number of credits per character; use `--credits-per-character` for that difference. Cloning eligibility, training costs, approval time, and commercial rights are not inferred from a price row. WellSaid's actual quote can exceed this floor when workflow limits or required access differ. Enter a comparable effective seat price after checking the contract; the calculator cannot discover missing rights or calculate undisclosed cap charges.

## 3. Run the TCO calculator

From this directory, run:

```sh
python3 calculate_elevenlabs_audiobook_tco.py
python3 calculate_elevenlabs_audiobook_tco.py --tier scale --characters 3000000 --retakes 20 --json
```

Actual stdout captured by running the default command locally during repository creation:

```text
Audiobook Publishing: Character and Credit TCO Calculator
Historical planning anchors; not a current quote. USD, pre-tax.
Tier=scale; seats=1; generated=3,600,000; credits=3,600,000
+--------------------------+-------------+-------------+-------------+
| Provider                 | Service USD | Labor USD   | Monthly USD |
+--------------------------+-------------+-------------+-------------+
| ElevenLabs               |      618.00 |      240.00 |      858.00 |
| Amazon Polly Neural      |       57.60 |    1,440.00 |    1,497.60 |
| WellSaid legacy floor    |      199.00 |    1,320.00 |    1,519.00 |
+--------------------------+-------------+-------------+-------------+
Savings vs Amazon Polly Neural: $639.60/month; $7,675.20/year (12 x monthly)
Savings vs WellSaid legacy floor: $661.00/month; $7,932.00/year (12 x monthly)
Positive savings favor ElevenLabs; negative savings favor the baseline.
WellSaid is a subscription floor; verify caps, API access, and eligibility.
https://is.gd/zhGCok
```

The file is executable and also supports `./calculate_elevenlabs_audiobook_tco.py`. Every repository has its own theme-specific defaults and can run independently of its siblings.

| Argument | Default in this repository | Meaning |
| --- | --- | --- |
| `--tier` | `scale` | `creator`, `pro`, or `scale`; selects historical fee, allowance, and overage anchors |
| `--seats` | `1` | Positive integer; independently licensed ElevenLabs subscriptions and WellSaid seats |
| `--characters` | `3000000` | Total finished spoken characters per month, before additional takes |
| `--retakes` | `20` | Extra generated text as a percentage of finished text; 20 means 1.20 times the finished text |
| `--credits-per-character` | `1` | Positive effective credit multiplier for the chosen ElevenLabs model |
| `--hourly-rate` | `60` | Loaded USD cost per production hour, shared across providers |
| `--el-hours` | `4` | Total monthly ElevenLabs production labor, not per-seat labor |
| `--polly-hours` | `24` | Total monthly Polly production labor |
| `--wellsaid-hours` | `22` | Total monthly WellSaid production labor |
| `--polly-per-million` | `16` | Selected Polly engine rate in USD per million billable characters |
| `--wellsaid-seat-price` | `199` | Effective comparable monthly seat price; no cap or API entitlement is assumed |
| `--eleven-monthly` | Selected tier | Override monthly fee per independent subscription with a written quote |
| `--eleven-included-credits` | Selected tier | Override monthly included credits per subscription |
| `--eleven-overage-per-1000` | Selected tier | Override USD per 1,000 extra credits |
| `--json` | Off | Emit one JSON object including inputs, effective rates, totals, savings, and gateway |

All numeric inputs must be finite and nonnegative; seats must be a positive integer, and the credit multiplier must be greater than zero. Invalid input exits through argparse with a nonzero status. Zero characters do not cancel a subscription. Extremely large inputs are rejected to keep the estimate within its supported numeric range.

The calculation is deliberately inspectable:

```text
generated_characters = finished_characters * (1 + retakes / 100)
modeled_credits = generated_characters * credits_per_character
included_credits = credits_per_subscription * seats
eleven_service = monthly_fee * seats
                 + max(0, modeled_credits - included_credits) / 1000 * overage_rate
polly_service = generated_characters / 1000000 * polly_rate
wellsaid_service_floor = effective_seat_price * seats
monthly_total = service + production_hours * hourly_rate
annualized_savings = 12 * (baseline_monthly_total - eleven_monthly_total)
```

The total-allowance formula assumes equal generation across independent accounts, which makes the aggregate calculation equivalent to separate identical account bills. Uneven usage requires running each account separately and summing the results; this is not a promise of credit pooling. Retakes apply equally to all providers by default to isolate tariffs and labor. For measured provider-specific retakes, run separate scenarios and compare the corresponding provider rows.

Service and labor are rounded to cents with decimal half-up rounding, then added. Annualization uses twelve identical monthly estimates, not an annual billing discount. Positive savings favor ElevenLabs; negative savings favor the named baseline and are never clamped to zero. AWS free allowances, promotions, tax, exchange rates, storage, egress, music, human narrator fees, training charges, and distribution fees are outside this model. Add them consistently when they apply.

For a synthesis-only sensitivity check:

```sh
python3 calculate_elevenlabs_audiobook_tco.py --el-hours 0 --polly-hours 0 --wellsaid-hours 0
```

Polly can be materially cheaper on synthesis charges alone. This check keeps the recommendation honest when an existing AWS workflow already meets your production needs. This CLI estimates costs; it does not render audio, parse SSML, inspect contracts, or measure naturalness.

### Theme-specific evaluation method

Count final spoken text after manuscript cleanup. Exclude navigation, publisher notes, and XML markup that will not be spoken; include every new synthesis request required by corrections. Keep a chapter revision log in the publishing system you already use. Separate failed takes, editorial rewrites, and pronunciation fixes when estimating retakes. Model setup and mastering labor explicitly, then inspect actual invoices before scaling the catalog.

Compare Pro and Scale with the same manuscript and labor inputs. At the default generated volume, Pro service spending is $843 while Scale service spending is $618 under these historical anchors. The $225 difference is a tariff calculation; it does not establish voice quality or current plan availability.

**[Evaluate ElevenLabs with a representative chapter or episode](https://is.gd/zhGCok)**

## 4. Migration checklist and related repositories

- [ ] Confirm audiobook distribution, commercial narration, and voice consent rights for the selected contract.
- [ ] Normalize chapter boundaries, Unicode punctuation, abbreviations, and narrator pronunciation notes.
- [ ] Use a representative chapter to measure regeneration and manual mastering time.
- [ ] Keep chapter IDs stable so corrections replace only affected segments.
- [ ] Check loudness, peaks, opening and closing credits, and distributor delivery requirements independently of TTS cost.
- [ ] Replace every historical price with an applicable quote before committing a budget.
- [ ] Keep the original provider available until a representative pilot passes editorial review.
- [ ] Run the default command and JSON mode locally; retain negative savings when a baseline wins.
- [ ] Reconcile the first invoice against credits, regeneration, labor, and separately billed services.

The other three repositories in this pack explore complementary decisions:

- [WellSaid Labs vs ElevenLabs: Team Seat Pricing Audit](../wellsaid-labs-vs-elevenlabs-team-seat-pricing-audit)
- [Instant vs Professional Voice Cloning: MOS Benchmark and Cost Budget](../instant-vs-professional-voice-clone-mos-benchmark)
- [Automated Podcast Narration: SSML and Workflow Cost Optimizer](../automated-podcast-narration-ssml-cost-optimizer)

Each sibling contains a standalone README and a standalone calculator. Relative links work in a checkout containing all four directories. No sibling imports or package installation are required.

**[Start the ElevenLabs workflow evaluation](https://is.gd/zhGCok)**

### Open-source license

The following MIT license applies to the calculator and this documentation. Product names identify their respective owners and do not imply vendor endorsement. The gateway is the single action destination used by this repository; any commercial relationship or affiliate compensation is not established by these files.

```text
MIT License

Copyright (c) 2026 Repository contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
