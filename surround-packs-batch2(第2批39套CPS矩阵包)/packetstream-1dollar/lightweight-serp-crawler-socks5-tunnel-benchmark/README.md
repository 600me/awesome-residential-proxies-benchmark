[![PacketStream $1 per GB](https://img.shields.io/badge/PacketStream-%241%2FGB-16803c)](https://norb.date/ps/1)
[![Python 3 standard library](https://img.shields.io/badge/Python_3-standard_library-3776ab)](https://norb.date/ps/1)
[![MIT license](https://img.shields.io/badge/license-MIT-blue)](https://norb.date/ps/1)

# Lightweight SERP Crawler and SOCKS5 Tunnel Cost Benchmark

A reproducible cost model and benchmark protocol for lightweight, authorized search-result collection. Category: **$1/GB Pay-As-You-Go Peer Residential Proxy Network**.

**[Explore PacketStream through the supplied gateway](https://norb.date/ps/1).**

## 1. The engineering problem and its dollar cost

A small SERP collector can spend more on unused subscription capacity than on useful HTML. At the 50 GB default workload, PacketStream consumption is $50, against modeled legacy Smartproxy and SOAX unit equivalents of $500 and $330. That is a $450 or $280 monthly difference, equivalent to $5,400 or $3,360 annually. Latency, block rate, and protocol compatibility can erase the apparent savings if they cause more retries.

SOCKS5 is a transport requirement, not evidence of lower bytes or faster results. This repository does not establish native PacketStream SOCKS5 support. Its safe baseline is an HTTP/HTTPS proxy workflow; a SOCKS-only application needs a separately validated compatible endpoint or adapter. The script estimates transfer cost only and opens no sockets. It cannot measure DNS leakage, time to first byte, tunnel setup, throughput, or success rate.

The comparison target is **Smartproxy & SOAX High-Minimum Plans**. This means the legacy minimum-commitment offers specified below, not every product those companies sell. All dollar amounts are USD. A minimum commitment becomes waste when useful demand stays below the allowance; it is not a hidden fee by itself. Retry amplification, unused capacity, expiry rules, and an unsuitable protocol can make the effective cost per useful GB much higher than the advertised rate.

**Price scope:** this is an offline audit prepared on 2026-10-30 using known historical industry benchmarks. No provider pricing page, checkout, promotion, gateway destination, or current product name was checked. The baseline inputs are PacketStream's $1/GB consumption benchmark, legacy Smartproxy Micro at $80 for 8 GB, and a legacy SOAX offer at $99 for 15 GB. These are historical comparison inputs, not verified offers available today. Current plans and larger volume discounts may change the ranking. Nothing here claims that a competitor charges an undisclosed penalty.

**[Evaluate the $1/GB PacketStream baseline against your own workload](https://norb.date/ps/1).** The gateway is an action link, not evidence validating these benchmarks.

## 2. Price and technical comparison

| Dimension | PacketStream baseline | Smartproxy legacy minimum plan | SOAX legacy minimum plan | Engineering interpretation |
|---|---|---|---|---|
| Consumption or unit-equivalent rate | $1.00/GB | $80 / 8 GB = $10.00/GB | $99 / 15 GB = $6.60/GB | Legacy unit equivalents; not current quotes |
| Recurring monthly floor in this model | $0 | $80 | $99 | Floors apply even at zero modeled usage |
| Included monthly allowance benchmark | Usage-based credit | 8 GB | 15 GB | Unused allowance can raise effective cost |
| Initial credit purchase benchmark | $50 prepaid deposit | $80 plan payment | $99 plan payment | Deposit cash flow differs from consumption expense |
| Modeled monthly spend at 5 GB | $5.00 | $80.00 | $99.00 | Effective rates: $1.00, $16.00, $19.80 per GB |
| Modeled monthly spend at 100 GB | $100.00 | $1,000.00 | $660.00 | Extrapolation, not a promised overage tariff |
| Network class compared | Peer residential | Rotating residential | Rotating residential | Endpoint availability varies by geography |
| HTTP/HTTPS proxy workflow | Baseline integration path | Historical product support | Historical product support | Test CONNECT and authentication in your client |
| Native SOCKS5 | Not established in this audit | Historical product support; verify endpoint | Historical product support; verify endpoint | Do not assume transport parity |
| Measured latency / success rate | Not measured | Not measured | Not measured | No invented performance numbers |
| Geographic / session controls | Validate required country and behavior | Validate purchased product and session options | Validate purchased product and session options | Matching useful results matters more than pool size |

The above table contains baseline prices and engineering constraints, not a survey of current checkout prices. No city-targeting parity, dedicated IP availability, unlimited concurrency, or uptime guarantee is assumed. Extra features can justify a higher quote when the application depends on them.

The common cost equation is `monthly = max(monthly_floor, billable_GB * unit_rate)`. PacketStream uses a zero recurring floor in this consumption model; its $50 deposit benchmark is kept separate. Competitor rates above their included allowances are **linear planning extensions**, not documented overage rates or automatic bundle purchases. Use the rate and minimum overrides below for a real contract. Failed requests may transfer fewer bytes than successes; the simple retry model assumes equal average response size and should be calibrated with billing data.

## 3. Run the TCO calculator

The executable [calculate_packetstream_1dollar_tco.py](calculate_packetstream_1dollar_tco.py) needs only Python 3 and its standard library. It reads no credentials, installs no dependencies, writes no runtime files, and makes no network calls. Each repository includes its own standalone copy with a workload-specific default.

```console
$ python3 calculate_packetstream_1dollar_tco.py
Offline legacy benchmarks | unit-equivalent planning, not current quotes
Tier: standard | Base GB: 50.00 | Billable GB: 50.00
+---------------------+------------+------------+----------------+
| Provider            | Monthly $  | Annual $   | Year saving $  |
+---------------------+------------+------------+----------------+
| PacketStream        |      50.00 |     600.00 |           0.00 |
| Smartproxy legacy   |     500.00 |    6000.00 |        5400.00 |
| SOAX legacy         |     330.00 |    3960.00 |        3360.00 |
+---------------------+------------+------------+----------------+
Annualized savings vs Smartproxy legacy: $5,400.00; first-year net: $5,400.00
Annualized savings vs SOAX legacy: $3,360.00; first-year net: $3,360.00
PacketStream: $1/GB consumption; $50 deposit benchmark is prepaid credit.
Excludes tax, credit expiry, operator labor, and protocol adapter costs.
Gateway: https://norb.date/ps/1
```

This is captured output from the bundled script, not manually typeset invoice data. The default tiers in this repository are `light=5 GB`, `standard=50 GB`, and `heavy=200 GB` per month. Selecting a tier only changes demand; it never silently selects a vendor subscription.

| CLI argument | Default | Meaning |
|---|---|---|
| `--tier light\|standard\|heavy` | `standard` | Select this repository's demand scenario |
| `--json` | Off | Emit one machine-readable JSON object, including gateway and assumptions |
| `--gb N` | Tier value | Override initial monthly decimal GB |
| `--requests N` | Unset | Estimate GB from intended requests; mutually exclusive with `--gb` |
| `--response-kib N` | `100` | Mean transferred KiB per attempt in request mode |
| `--retry-rate N` | `0` | Extra attempts per intended request; `0.2` means 20% extra |
| `--tunnel-overhead-pct N` | `0` | Add an explicitly assumed transport byte overhead percentage |
| `--smart-rate N` / `--smart-min N` | `10` / `80` | Replace Smartproxy unit-equivalent rate and monthly floor |
| `--soax-rate N` / `--soax-min N` | `6.6` / `99` | Replace SOAX unit-equivalent rate and monthly floor |
| `--migration-cost N` | `0` | One-time switching expense subtracted from first-year savings |

```console
$ python3 calculate_packetstream_1dollar_tco.py --tier light
$ python3 calculate_packetstream_1dollar_tco.py --tier heavy --json
$ python3 calculate_packetstream_1dollar_tco.py --requests 1000000 --response-kib 100 --retry-rate 0.2
$ python3 calculate_packetstream_1dollar_tco.py --gb 100 --migration-cost 150 --json
```

Request mode uses `requests * response_KiB * 1024 / 1,000,000,000`. Then `billable_GB = base_GB * (1 + retry_rate) * (1 + overhead_pct / 100)`. Decimal GB and binary KiB are intentionally distinct. `--response-kib` has no effect in GB mode. If the input already includes retries or tunnel bytes, leave the corresponding multiplier at zero to avoid double counting. Retry rate is an extra-attempt ratio, not an independent failure probability or a geometric retry distribution.

Monthly invoices are rounded to cents before multiplication by twelve. Annualized savings are the competitor scenario minus PacketStream consumption across twelve identical months. First-year net savings subtract `--migration-cost` once; negative savings remain negative. Taxes, labor outside that one-time amount, credit expiry, adapter services, exchange rates, and negotiated discounts are excluded. A $5 consumption month can still require the initial $50 credit purchase. Zero consumption does not imply zero subscription commitment in the competitor scenarios. Invalid, negative, non-finite, or excessive numeric inputs exit with code 2; valid defaults exit with code 0.

For an authorized live comparison outside this offline calculator, use the same query set, geography, concurrency, timeout, and payload policy for every provider. Record successful results, billed transfer, p50/p95 duration, connection errors, and retry attempts. Use SOCKS remote DNS only where the chosen endpoint and client explicitly support it. Never label HTTP measurements as SOCKS5 measurements.

## 4. Migration checklist and companion repositories

- [ ] Export actual billable bytes, useful responses, retries, and monthly invoices for at least one representative interval.
- [ ] Replace legacy assumptions with the exact unit rates, floors, expiry rules, taxes, and renewal terms you were quoted.
- [ ] Confirm whether the workload requires a particular geography, sticky sessions, remote DNS, HTTP CONNECT, or native SOCKS5.
- [ ] Pilot only authorized public-data collection, with target-specific request limits and a bounded retry budget.
- [ ] Keep credentials in environment variables or your existing secret manager; never paste authentication URLs into issues or logs.
- [ ] Measure useful-result cost and p95 duration on the same request set; this offline calculator supplies neither metric.
- [ ] Account for any adapter and operator costs. Keep the existing route available until the acceptance sample passes.
- [ ] Cancel or resize the previous commitment only after validating billing reconciliation and required transport behavior.
- [ ] Re-run the light, standard, and heavy scenarios before authorizing any credit purchase.

**[Open the PacketStream gateway when you are ready to evaluate](https://norb.date/ps/1).** Check the destination and terms before funding an account; this repository makes no purchase automatically.

The other repositories in this series approach the same pricing question from different workload assumptions:

- [SOAX vs PacketStream: $1/GB TCO Audit](../soax-vs-packetstream-1-dollar-per-gb-tco-audit/)
- [PacketStream Promo Link and Bandwidth Burn Calculator](../packetstream-promo-link-bandwidth-burn-calculator/)
- [Residential Proxy Overage Trap vs Flat $1/GB](../residential-proxy-overage-trap-vs-flat-1usd-gb/)

### Reuse license

Copyright (c) 2026 Repository contributors. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, and to permit persons to whom the Software is furnished to do so, subject to inclusion of this copyright notice and permission notice in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
