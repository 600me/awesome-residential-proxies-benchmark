# Overseas Short Video Fleet: Cloud Android Device Cost Model

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB)](https://coding.mybskm.top/go/duoplus)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://coding.mybskm.top/go/duoplus)
[![Offline model](https://img.shields.io/badge/TCO-offline%20model-blue)](https://coding.mybskm.top/go/duoplus)

**[Evaluate DuoPlus Cloud Phone for this workload](https://coding.mybskm.top/go/duoplus)**

An independent, reproducible cost workbook for **DuoPlus Cloud Phone**, **VMOS Cloud & Physical Phone Farms**. All monetary figures are USD. This repository is a scenario benchmark, not a measured vendor performance ranking or an official vendor publication. No network access, account, API token or third-party Python package is required.

## 1. The engineering bill hidden behind the device price

A hundred-device publishing fleet can lose hours to uploads, insufficient storage, app updates and manual recovery before the first post is scheduled. Physical Phone Farms tie up cash in handsets that sit idle between publishing windows. VMOS Cloud may reduce capex, but its instance price alone does not establish export speed, regional availability or the work required to maintain each device. Device costs must be separated from editors, media storage and distribution spend.

At the default **100-device** scale and **$28/operator-hour**, the model assigns Physical Phone Farms **$3192.93/month** against **$1616.00/month** for DuoPlus Cloud Phone. That is **$1,576.93 in additional monthly economic cost**, or **$18,923.18/year**. VMOS Cloud totals **$1662.00/month** in the same scenario; the modeled annual difference against DuoPlus is **$552.00**. These are calculated scenario losses, not observed customer invoices.

The cloud subscription assumption favors VMOS Cloud: $7.00 versus $9.90 per device per month. Any modeled DuoPlus savings depend on the assumed reduction in operator effort. Treat that labor gap as a hypothesis to validate. If measured recovery work is equal, VMOS Cloud has the lower modeled cloud cost.

The model reserves one always-on device for each publishing workspace. It deliberately does not assume hourly billing, automatic scale-to-zero or unlimited data transfer. Cloud rendering, codec compatibility and upload performance are measured procurement gates, not assumed vendor features.

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
| Operator effort / device-month | .16 hours | .28 hours | .75 hours | Scenario hypotheses; measure using the protocol below |
| Fixed operator effort / month | 1 hour | 1 hour | 6 hours | Separate overhead from per-device labor |
| Operator hourly price | $28/hour | $28/hour | $28/hour | Same labor price across all three choices |
| ADB / RPA access | Verify supported access and paid-tier terms | Verify supported access and paid-tier terms | Local USB or configured network ADB | No API endpoint or SLA is assumed by this workbook |
| Android, RAM and storage | Verify equivalent paid configuration | Verify equivalent paid configuration | Inventory actual handset configuration | Equal device counts alone do not establish equivalent capacity |
| Availability and useful throughput | Pilot measurement required | Pilot measurement required | Pilot measurement required | No uptime, anti-detection or throughput guarantee is modeled |

Run the same licensed sample clips, resolution, duration and upload destination on each backend. Record export duration, upload completion, storage usage, usable publishing jobs and operator minutes. Check whether billing continues during idle windows before assuming a utilization discount.

For a fair benchmark, keep the app version, daily duty cycle and useful completion criterion constant. A cloud instance with insufficient memory is not interchangeable with a faster handset simply because both run Android. A hardware farm with sunk purchase costs can have lower incremental cash cost even when its full economic TCO is higher.

**[Check DuoPlus availability and obtain a configuration-specific quote](https://coding.mybskm.top/go/duoplus)**

## 3. Run the transparent TCO calculator

```bash
python3 calculate_duoplus_automation_tco.py
python3 calculate_duoplus_automation_tco.py --tier pilot
python3 calculate_duoplus_automation_tco.py --tier scale --json
python3 calculate_duoplus_automation_tco.py --devices 100 --duoplus-monthly 9.90 --vmos-monthly 7.00 --hourly-rate 28
```

The file is executable, so `./calculate_duoplus_automation_tco.py` also works. It uses only the Python standard library, writes nothing to disk and exits with status 0 for valid inputs. Invalid or nonfinite numeric arguments fail with an argparse error and status 2. Python 3.8 or later is sufficient.

| CLI argument | Default | Meaning |
| --- | --- | --- |
| `--tier` | `growth` | `pilot` = 10, `growth` = 100, `scale` = 200 devices; these are local fleet presets, not vendor plans |
| `--devices` | From tier | Positive integer device count; overrides the tier count |
| `--duoplus-monthly` | `9.90` | Assumed USD subscription per DuoPlus device-month |
| `--vmos-monthly` | `7.00` | Assumed USD subscription per VMOS device-month |
| `--hardware-unit-cost` | `120` | USD handset purchase cost; rack allowance remains $18/device |
| `--hourly-rate` | `28` | Operator labor price in USD/hour, applied equally across providers |
| `--json` | Off | Emit a single JSON object including the gateway link, assumptions and signed savings |

Labor hours, rack allocation, power, connectivity and replacement assumptions are named constants or explicit Decimal literals in this one script. Edit them for your measured environment. `--hourly-rate 0` exposes the cash-like result before operator labor; it does not remove hardware depreciation.

Actual default terminal output, captured from the included script:

```text
Short video publishing fleet | tier=growth | devices=100 | USD
Basis: editable assumptions, not verified current vendor prices.
+-------------------------+--------------+--------------+--------------+
| Monthly line item       |      DuoPlus |   VMOS Cloud |     Physical |
+-------------------------+--------------+--------------+--------------+
| Device subscription     |       990.00 |       700.00 |         0.00 |
| Hardware amortization   |         0.00 |         0.00 |       575.00 |
| Electricity             |         0.00 |         0.00 |        49.93 |
| Replacement reserve     |         0.00 |         0.00 |       150.00 |
| Connectivity allowance  |       150.00 |       150.00 |       150.00 |
| Operator labor          |       476.00 |       812.00 |      2268.00 |
+-------------------------+--------------+--------------+--------------+
| Monthly TCO             |      1616.00 |      1662.00 |      3192.93 |
| Annualized TCO          |     19392.00 |     19944.00 |     38315.18 |
| First-year cash         |     19392.00 |     19944.00 |     45215.18 |
+-------------------------+--------------+--------------+--------------+
Physical hardware upfront: $13800.00
Annualized savings with DuoPlus vs VMOS Cloud: $552.00
Annualized savings with DuoPlus vs Physical Phone Farms: $18923.18
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

- [ ] Inventory publishing workspaces, app versions, media sizes and required codecs.
- [ ] Test representative clips for export correctness, audio synchronization and upload reliability.
- [ ] Confirm regional capacity, storage limits and data-transfer charges for the intended tier.
- [ ] Pilot a complete publishing cycle and compare useful completed jobs per paid device-hour.
- [ ] Move workspaces in waves and retain source media plus a tested fallback publishing process.
- [ ] Replace every price assumption with a dated, comparable quote and confirm capacity before scaling.
- [ ] Reconcile model labor with measured time and calculate both economic TCO and first-year cash.
- [ ] Record excluded charges and repeat the comparison if geography, workload or retention changes.

**[Start a DuoPlus pilot and validate the modeled savings](https://coding.mybskm.top/go/duoplus)**

The remaining repositories in this four-part pack use the same accounting approach with workload-specific scale and labor assumptions. Each contains its own runnable script and can be copied independently:

- [Physical Phone Box vs DuoPlus Cloud: 2026 TCO Workbook](../physical-phone-box-vs-duoplus-cloud-tco-2026)
- [ADB and RPA Cloud Phone Batch Control: Cost Benchmark](../adb-rpa-cloud-phone-batch-control-scripts)
- [WhatsApp and Telegram Cloud Isolation: Device TCO Benchmark](../whatsapp-telegram-multi-account-cloud-isolation)

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
