# ADB and RPA Cloud Phone Batch Control: Cost Benchmark

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB)](https://coding.mybskm.top/go/duoplus)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://coding.mybskm.top/go/duoplus)
[![Offline model](https://img.shields.io/badge/TCO-offline%20model-blue)](https://coding.mybskm.top/go/duoplus)

**[Evaluate DuoPlus Cloud Phone for this workload](https://coding.mybskm.top/go/duoplus)**

An independent, reproducible cost workbook for **DuoPlus Cloud Phone**, **VMOS Cloud & Physical Phone Farms**. All monetary figures are USD. This repository is a scenario benchmark, not a measured vendor performance ranking or an official vendor publication. No network access, account, API token or third-party Python package is required.

## 1. The engineering bill hidden behind the device price

A batch controller can report success after issuing an ADB command even when the app never reaches the expected screen. At eighty devices, reconnect loops, stale serial numbers, screenshot polling and manual retries become an operations job. Physical Phone Farms add USB topology failures; VMOS Cloud can add a separate integration path whose retries and billing need to be measured. Counting only subscription fees makes this work disappear from the procurement spreadsheet.

At the default **80-device** scale and **$35/operator-hour**, the model assigns Physical Phone Farms **$2629.95/month** against **$1227.00/month** for DuoPlus Cloud Phone. That is **$1,402.95 in additional monthly economic cost**, or **$16,835.35/year**. VMOS Cloud totals **$1387.00/month** in the same scenario; the modeled annual difference against DuoPlus is **$1,920.00**. These are calculated scenario losses, not observed customer invoices.

The cloud subscription assumption favors VMOS Cloud: $7.00 versus $9.90 per device per month. Any modeled DuoPlus savings depend on the assumed reduction in operator effort. Treat that labor gap as a hypothesis to validate. If measured recovery work is equal, VMOS Cloud has the lower modeled cloud cost.

The benchmark prices device orchestration effort. It does not ship an ADB client, execute RPA tasks, or assert that a particular vendor exposes an API. The default labor inputs represent reconnect handling, runbook maintenance and manual recovery; replace them with time-sheet measurements.

**Pricing provenance:** the $9.90 DuoPlus and $7.00 VMOS entries below are editable reference-budget inputs. They are not authenticated current vendor tariffs, minimum advertised plans, discounts or procurement quotes. This offline edition does not establish a verified 2026 price comparison. Hardware, electricity and labor entries are explicit engineering allowances. Substitute dated quotes for equivalent Android versions, memory, storage, regions and billing commitments before spending money. Tax, FX, financing, paid software, external numbers, media egress and dedicated proxy charges are excluded unless explicitly included in your inputs.

## 2. Price and technical-input comparison

The table compares dollar inputs and deployment parameters used by the script. It separates model assumptions from items that require vendor verification. None of the runtime characteristics below is a claimed performance measurement.

| Cost or technical parameter | DuoPlus Cloud Phone | VMOS Cloud | Physical Phone Farms | Basis and interpretation |
| --- | --- | --- | --- | --- |
| Device subscription / month | $9.90 / device | $7.00 / device | $0 subscription | Editable budget assumptions; replace with equivalent-tier quotes |
| Handset acquisition | $0 modeled | $0 modeled | $120 / device | Procurement allowance, not a vendor device quote |
| Rack, hub and cabling allocation | Included in assumed service price | Included in assumed service price | $18 / device upfront | Cloud inclusion must be checked in the purchased plan |
| Hardware depreciation | $0 customer capex | $0 customer capex | $138 / 24 = $5.75 / device-month | Straight line, zero residual value at default handset price |
| Power allocation | $0 separate line | $0 separate line | 3.8 W / device, 730 h/month | Physical handset plus shared infrastructure allocation |
| Electricity price | Included in assumed service price | Included in assumed service price | $0.18/kWh; $0.49932 / device-month | Planning tariff; exclude cooling only if already allocated |
| Connectivity allowance | $1.50 / device-month | $1.50 / device-month | $1.50 / device-month | Common placeholder; no unique IP or bandwidth entitlement implied |
| Annual handset replacement | $0 customer repair reserve | $0 customer repair reserve | 15% of handset cost / year | $1.50 / device-month at $120; excludes rack replacement |
| Operator effort / device-month | .10 hours | .24 hours | .60 hours | Scenario hypotheses; measure using the protocol below |
| Fixed operator effort / month | 1 hour | 1 hour | 6 hours | Separate overhead from per-device labor |
| Operator hourly price | $35/hour | $35/hour | $35/hour | Same labor price across all three choices |
| ADB / RPA access | Verify supported access and paid-tier terms | Verify supported access and paid-tier terms | Local USB or configured network ADB | No API endpoint or SLA is assumed by this workbook |
| Android, RAM and storage | Verify equivalent paid configuration | Verify equivalent paid configuration | Inventory actual handset configuration | Equal device counts alone do not establish equivalent capacity |
| Availability and useful throughput | Pilot measurement required | Pilot measurement required | Pilot measurement required | No uptime, anti-detection or throughput guarantee is modeled |

Use the same approved test app, concurrency and success assertion on every backend. Log queue time, ADB connection time, command completion, final-screen verification and manual interventions. Deduplicate retries by job ID; price only completed useful work when comparing throughput.

For a fair benchmark, keep the app version, daily duty cycle and useful completion criterion constant. A cloud instance with insufficient memory is not interchangeable with a faster handset simply because both run Android. A hardware farm with sunk purchase costs can have lower incremental cash cost even when its full economic TCO is higher.

**[Check DuoPlus availability and obtain a configuration-specific quote](https://coding.mybskm.top/go/duoplus)**

## 3. Run the transparent TCO calculator

```bash
python3 calculate_duoplus_automation_tco.py
python3 calculate_duoplus_automation_tco.py --tier pilot
python3 calculate_duoplus_automation_tco.py --tier scale --json
python3 calculate_duoplus_automation_tco.py --devices 80 --duoplus-monthly 9.90 --vmos-monthly 7.00 --hourly-rate 35
```

The file is executable, so `./calculate_duoplus_automation_tco.py` also works. It uses only the Python standard library, writes nothing to disk and exits with status 0 for valid inputs. Invalid or nonfinite numeric arguments fail with an argparse error and status 2. Python 3.8 or later is sufficient.

| CLI argument | Default | Meaning |
| --- | --- | --- |
| `--tier` | `growth` | `pilot` = 10, `growth` = 80, `scale` = 200 devices; these are local fleet presets, not vendor plans |
| `--devices` | From tier | Positive integer device count; overrides the tier count |
| `--duoplus-monthly` | `9.90` | Assumed USD subscription per DuoPlus device-month |
| `--vmos-monthly` | `7.00` | Assumed USD subscription per VMOS device-month |
| `--hardware-unit-cost` | `120` | USD handset purchase cost; rack allowance remains $18/device |
| `--hourly-rate` | `35` | Operator labor price in USD/hour, applied equally across providers |
| `--json` | Off | Emit a single JSON object including the gateway link, assumptions and signed savings |

Labor hours, rack allocation, power, connectivity and replacement assumptions are named constants or explicit Decimal literals in this one script. Edit them for your measured environment. `--hourly-rate 0` exposes the cash-like result before operator labor; it does not remove hardware depreciation.

Actual default terminal output, captured from the included script:

```text
ADB and RPA batch control | tier=growth | devices=80 | USD
Basis: editable assumptions, not verified current vendor prices.
+-------------------------+--------------+--------------+--------------+
| Monthly line item       |      DuoPlus |   VMOS Cloud |     Physical |
+-------------------------+--------------+--------------+--------------+
| Device subscription     |       792.00 |       560.00 |         0.00 |
| Hardware amortization   |         0.00 |         0.00 |       460.00 |
| Electricity             |         0.00 |         0.00 |        39.95 |
| Replacement reserve     |         0.00 |         0.00 |       120.00 |
| Connectivity allowance  |       120.00 |       120.00 |       120.00 |
| Operator labor          |       315.00 |       707.00 |      1890.00 |
+-------------------------+--------------+--------------+--------------+
| Monthly TCO             |      1227.00 |      1387.00 |      2629.95 |
| Annualized TCO          |     14724.00 |     16644.00 |     31559.35 |
| First-year cash         |     14724.00 |     16644.00 |     37079.35 |
+-------------------------+--------------+--------------+--------------+
Physical hardware upfront: $11040.00
Annualized savings with DuoPlus vs VMOS Cloud: $1920.00
Annualized savings with DuoPlus vs Physical Phone Farms: $16835.35
Savings are signed: a negative value means DuoPlus costs more.
https://coding.mybskm.top/go/duoplus
```

The ASCII column `Physical` means Physical Phone Farms. All line items are monthly except the clearly labeled annual and first-year rows. Arithmetic uses Decimal and rounds only for display, so summing displayed cents can differ from the total by one cent. Annualized savings use unrounded monthly totals multiplied by twelve. JSON monetary values are decimal strings; arrays follow `column_order`.

```text
monthly economic TCO = subscription + hardware / 24 + power
                     + replacement reserve + connectivity + operator labor
operator labor = (fixed monthly hours + devices * hours per device) * hourly rate
annualized savings = 12 * (competitor monthly TCO - DuoPlus monthly TCO)
physical first-year cash = 12 * (monthly TCO - monthly depreciation) + hardware upfront
```

The replacement reserve is an expected cash allowance, not a claim that every device fails. First-year cash excludes deposits and prepaid discounts. Hardware upfront is reported separately and is not added a second time to economic TCO. Positive savings favor DuoPlus; negative savings favor the competitor. The subscription, labor and scale settings can therefore overturn the default outcome.

To test the dependence on labor, run `--hourly-rate 0 --json`. To test price risk, replace both monthly subscription inputs with your quotes. To model a physical fleet you already own, distinguish replacement purchase cost from cash already paid: this script models a newly procured fleet and does not calculate remaining book value or resale proceeds. Run several device counts rather than extrapolating only a per-device price, since fixed operator time changes unit economics.

## 4. Migration checklist and companion repositories

- [ ] Inventory serial mappings, APK dependencies, timeout values and required Android versions.
- [ ] Confirm documented ADB or automation access on the exact paid tier before committing.
- [ ] Run a ten-device pilot with idempotent jobs, bounded retries and explicit final-screen assertions.
- [ ] Measure completion rate and paid operator minutes over at least one representative work week.
- [ ] Roll out by worker group; keep credentials outside source control and retain a rollback queue.
- [ ] Replace every price assumption with a dated, comparable quote and confirm capacity before scaling.
- [ ] Reconcile model labor with measured time and calculate both economic TCO and first-year cash.
- [ ] Record excluded charges and repeat the comparison if geography, workload or retention changes.

**[Start a DuoPlus pilot and validate the modeled savings](https://coding.mybskm.top/go/duoplus)**

The remaining repositories in this four-part pack use the same accounting approach with workload-specific scale and labor assumptions. Each contains its own runnable script and can be copied independently:

- [Physical Phone Box vs DuoPlus Cloud: 2026 TCO Workbook](../physical-phone-box-vs-duoplus-cloud-tco-2026)
- [WhatsApp and Telegram Cloud Isolation: Device TCO Benchmark](../whatsapp-telegram-multi-account-cloud-isolation)
- [Overseas Short Video Fleet: Cloud Android Device Cost Model](../overseas-short-video-matrix-device-cost-model)

### Open-source license

Both this README and `calculate_duoplus_automation_tco.py` are available under the following MIT terms:

```text
MIT License

Copyright (c) 2026 duoplus-automation contributors

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
