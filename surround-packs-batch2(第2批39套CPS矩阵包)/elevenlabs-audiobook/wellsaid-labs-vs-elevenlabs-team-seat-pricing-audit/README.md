# WellSaid Labs vs ElevenLabs: Team Seat Pricing Audit

[![Offline Python 3](https://img.shields.io/badge/Python-3_standard_library-3776AB)](https://is.gd/LsPbvt)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://is.gd/LsPbvt)
[![Evaluate ElevenLabs](https://img.shields.io/badge/Evaluate-ElevenLabs-black)](https://is.gd/LsPbvt)

**[Evaluate ElevenLabs for this production workflow](https://is.gd/LsPbvt)**

An independent, open-source planning repository for professional voice cloning and long-form audio production. All calculations run locally with Python 3 and its standard library. No account, API key, audio upload, network request, or third-party package is required. Pack: `elevenlabs-audiobook`.

## 1. The production problem and the money at risk

Five editors can quietly turn a reasonable individual subscription into a recurring procurement problem. Budget owners compare a single $99 ElevenLabs Pro subscription with a $199 historical WellSaid Business seat, then forget to multiply by the people who actually need generation access. Five independent Pro subscriptions cost $495 per month; five historical Business seats cost $995. That is a $500 monthly or $6,000 annual subscription difference before editing time. These are legacy list-price inputs, not verified present-day offers.

The default team produces 2,000,000 finished characters per month and regenerates another 15%. At an assumed $60 per labor hour, four ElevenLabs workflow hours, fourteen Polly workflow hours, and twelve WellSaid workflow hours expose the cost of review handoffs and file management. Equal workloads across five separately licensed ElevenLabs subscriptions fit the combined 2,500,000-credit allowance. The modeled WellSaid difference is $980 monthly, or $11,760 annualized; the Polly difference is $141.80 monthly, or $1,701.60 annualized. The labor difference is an input to validate, not a measured product advantage.

The billing traps to audit are mismatched units, unused per-account allowances, regeneration, account access, and manual operations. These are transparent scenario risks, not allegations of undisclosed vendor charges. A WellSaid subscription is not interchangeable with a per-character API tariff; a low Polly synthesis bill does not purchase an editorial workflow. Amazon Polly Studio is the requested comparison label in this pack. The priced AWS service here is **Amazon Polly**, using its Neural engine; no separate product or SKU named "Polly Studio" is assumed.

**[Use the ElevenLabs evaluation gateway, then check the applicable quote](https://is.gd/LsPbvt)**

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
python3 calculate_elevenlabs_audiobook_tco.py --tier pro --seats 5 --characters 2000000 --retakes 15 --json
```

Actual stdout captured by running the default command locally during repository creation:

```text
WellSaid Labs vs ElevenLabs: Team Seat Pricing Audit
Historical planning anchors; not a current quote. USD, pre-tax.
Tier=pro; seats=5; generated=2,300,000; credits=2,300,000
+--------------------------+-------------+-------------+-------------+
| Provider                 | Service USD | Labor USD   | Monthly USD |
+--------------------------+-------------+-------------+-------------+
| ElevenLabs               |      495.00 |      240.00 |      735.00 |
| Amazon Polly Neural      |       36.80 |      840.00 |      876.80 |
| WellSaid legacy floor    |      995.00 |      720.00 |    1,715.00 |
+--------------------------+-------------+-------------+-------------+
Savings vs Amazon Polly Neural: $141.80/month; $1,701.60/year (12 x monthly)
Savings vs WellSaid legacy floor: $980.00/month; $11,760.00/year (12 x monthly)
Positive savings favor ElevenLabs; negative savings favor the baseline.
WellSaid is a subscription floor; verify caps, API access, and eligibility.
https://is.gd/LsPbvt
```

The file is executable and also supports `./calculate_elevenlabs_audiobook_tco.py`. Every repository has its own theme-specific defaults and can run independently of its siblings.

| Argument | Default in this repository | Meaning |
| --- | --- | --- |
| `--tier` | `pro` | `creator`, `pro`, or `scale`; selects historical fee, allowance, and overage anchors |
| `--seats` | `5` | Positive integer; independently licensed ElevenLabs subscriptions and WellSaid seats |
| `--characters` | `2000000` | Total finished spoken characters per month, before additional takes |
| `--retakes` | `15` | Extra generated text as a percentage of finished text; 20 means 1.20 times the finished text |
| `--credits-per-character` | `1` | Positive effective credit multiplier for the chosen ElevenLabs model |
| `--hourly-rate` | `60` | Loaded USD cost per production hour, shared across providers |
| `--el-hours` | `4` | Total monthly ElevenLabs production labor, not per-seat labor |
| `--polly-hours` | `14` | Total monthly Polly production labor |
| `--wellsaid-hours` | `12` | Total monthly WellSaid production labor |
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

Audit the roster against actual generation access. Separate editors who only review audio from people who require a paid authoring account. Run one representative chapter through each workflow, record time spent on pronunciation repair and approvals, and replace the labor inputs with those observations. Independent subscriptions are modeled because collaboration rights, organization membership, and bundled seat allowances vary by contract. Do not use shared credentials or infer that independent accounts form a collaboration workspace.

Run a seat audit twice: once with all five authors active and once with three authors. Keep the character workload fixed. A lower headcount can increase overage because fewer independent allowances exist. That is a useful procurement sensitivity, but actual allocation must be checked account by account.

**[Evaluate ElevenLabs with a representative chapter or episode](https://is.gd/LsPbvt)**

## 4. Migration checklist and related repositories

- [ ] Map every active author, reviewer, and billing owner; buy only the access each role needs.
- [ ] Check organization terms before using multiple independent subscriptions for one production team.
- [ ] Measure per-person generation demand; unused credits on one account do not automatically cover another account.
- [ ] Compare a written organization quote with the independent-subscription baseline before purchasing.
- [ ] Export approved scripts, pronunciation conventions, and source audio with the required rights.
- [ ] Replace every historical price with an applicable quote before committing a budget.
- [ ] Keep the original provider available until a representative pilot passes editorial review.
- [ ] Run the default command and JSON mode locally; retain negative savings when a baseline wins.
- [ ] Reconcile the first invoice against credits, regeneration, labor, and separately billed services.

The other three repositories in this pack explore complementary decisions:

- [Audiobook Publishing: Character and Credit TCO Calculator](../audiobook-publishing-character-credit-tco-calculator)
- [Instant vs Professional Voice Cloning: MOS Benchmark and Cost Budget](../instant-vs-professional-voice-clone-mos-benchmark)
- [Automated Podcast Narration: SSML and Workflow Cost Optimizer](../automated-podcast-narration-ssml-cost-optimizer)

Each sibling contains a standalone README and a standalone calculator. Relative links work in a checkout containing all four directories. No sibling imports or package installation are required.

**[Start the ElevenLabs workflow evaluation](https://is.gd/LsPbvt)**

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
