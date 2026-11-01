[![Compare Vast.ai](https://img.shields.io/badge/Vast.ai-compare_GPU_offers-16a34a)](https://is.gd/kKRWDd)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-blue)](https://is.gd/kKRWDd)

# Batch embeddings and Whisper: cost per completed job

## 1. The engineering bill that an hourly quote misses

A million embedded documents or 18,000 minutes of audio is a deliverable; a rented GPU hour is only an input. A transcription queue pays for silence decoding, model downloads and retried segments as well as useful speech. An embedding queue pays for tokenization, padding and writing vectors. Teams that forecast only active kernel time can overspend even when their Spot VM hourly quote looks attractive.

GCP Spot and Azure Spot restart events can duplicate uncommitted chunks. Paperspace's retained disk and an idle notebook can add costs between batch windows. Vast.ai can reduce the compute line for portable jobs, but image pull time, host storage pricing and data movement still belong in the estimate. The calculator exposes a reference throughput and a lost-work fraction so that these costs remain visible.

In this repository's default scenario, Paperspace costs **$356.67/month** and Vast.ai costs **$96.09/month** for the same assumed useful work. The modeled excess is **$260.58/month**, or **$3,126.96/year**. This is a transparent scenario calculation, not an observed customer loss or a promise of savings. If your throughput, regional quote or interruption rate differs, the ranking can reverse.

**[Compare a Vast.ai offer against your own bill](https://is.gd/kKRWDd)** before committing a batch queue.

## 2. GPU specifications and offline price comparison

The hardware names and memory classes refer to real GPU families. All dollar values are **unverified offline planning inputs**, informed by commonly encountered historical price magnitudes; they are not current vendor quotes, a dated price survey, or guaranteed available inventory. No webpage was fetched to prepare this repository. Exact region, machine bundle, CPU/RAM, disk capacity, billing granularity and quote date are intentionally unspecified, so obtain those inputs before a purchase. No measured benchmark results are claimed.

| Tier / provider | GPU | VRAM (GiB) | Assumed USD/GPU-h | Relative useful speed | Lost billed time | Non-compute USD/month |
|---|---|---:|---:|---:|---:|---:|
| rtx4090 / Vast.ai | RTX 4090 | 24 | $0.35 | 1.00x | 8% | $20 |
| rtx4090 / GCP Spot | T4 | 16 | $0.35 | 0.35x | 10% | $80 |
| rtx4090 / Azure Spot | A10 | 24 | $0.65 | 0.70x | 10% | $70 |
| rtx4090 / Paperspace | A4000 | 16 | $0.76 | 0.50x | 4% | $40 |
| rtx4090 / AWS Spot | A10G | 24 | $0.60 | 0.70x | 10% | $75 |
| rtx4090 / Salad | RTX 4090 | 24 | $0.30 | 0.85x | 15% | $25 |
| h100 / Vast.ai | H100 PCIe | 80 | $1.80 | 1.00x | 8% | $40 |
| h100 / GCP Spot | A100 80GB | 80 | $1.80 | 0.65x | 10% | $120 |
| h100 / Azure Spot | A100 80GB | 80 | $2.00 | 0.65x | 10% | $110 |
| h100 / Paperspace | A100 80GB | 80 | $3.18 | 0.65x | 4% | $80 |
| h100 / AWS Spot | H100 | 80 | $2.80 | 1.00x | 10% | $120 |

The `rtx4090` tier names a reference workload lane, not a claim that GCP, Azure or Paperspace sells an RTX 4090 Spot instance. Likewise, the `h100` lane compares an H100 reference with feasible datacenter substitutes. H100 PCIe uses an 80 GB class here; inspect the exact SKU because other H100 variants differ. RTX 4090 has a 24 GB memory class. GCP and Azure rows model interruptible Spot economics; Paperspace rows model hourly rental, without claiming equivalent Spot eviction semantics. AWS is included for the cloud comparison; Salad is available only in the consumer lane. No Salad H100 listing is assumed.

Non-compute inputs are explicit monthly allowances for persistent storage, data transfer and related bill items. They are not vendor storage tariffs. This model does not double-charge them per GPU hour. Taxes, support, engineering labor, reservations, credits and private discounts are excluded. If these are material, include an amortized monthly amount with `--extra`; this is a scoped infrastructure TCO estimate rather than a complete business accounting model.

The default scenario is 1,000,000 documents at 5,000 documents per useful reference hour: 200 reference hours per month. For Whisper, use `--workload whisper --units 18000`; the assumed 120 audio minutes per reference hour produces 150 reference hours. These are deliberately editable workload assumptions, not measured rates for a named embedding model or Whisper model size. H100 does not automatically inherit an RTX 4090 measured rate: supply a throughput measured on the selected reference tier.

For embeddings, freeze tokenizer version, average token length, truncation policy, precision and output dimensions. For transcription, freeze Whisper variant, language, beam size, VAD settings and audio sample rate. Measure word error rate as well as runtime. Chunk audio with stable identifiers and commit each transcript atomically; deduplicate embeddings by document ID and model version. An interrupted worker should repeat only its uncommitted chunk.

**[Inspect Vast.ai capacity and replace the assumed hourly rate](https://is.gd/kKRWDd)** with the complete price of a suitable offer.

## 3. Reproduce the bill with Python 3

Run from this repository directory. The script uses only the standard library and performs no network requests, provisioning or credential access.

```sh
python3 calculate_vastai_spot_tco.py
python3 calculate_vastai_spot_tco.py --tier h100 --json
python3 calculate_vastai_spot_tco.py --rate 'Vast.ai=0.42' --speed 'Paperspace=0.65' --loss 'Vast.ai=0.12' --extra 'GCP Spot=100'
```

| Argument | Meaning | Default / units |
|---|---|---|
| `--tier` | Reference lane and candidate set | `rtx4090`; alternative `h100` |
| `--json` | One machine-readable JSON document, including gateway and savings | Off |
| `--hours` | Monthly useful hours on the reference GPU; ignored in batch mode | 200 hours |
| `--units` | Batch workload size; used only in batch mode | 1,000,000 documents or audio minutes |
| `--workload` | `embeddings` or `whisper` reference units | `embeddings` |
| `--units-per-hour` | Useful units per reference GPU hour | 5,000 documents or 120 audio minutes |
| `--rate PROVIDER=VALUE` | Override entire required compute rental price | USD/hour; repeatable |
| `--speed PROVIDER=VALUE` | Override useful throughput relative to selected reference | Positive ratio; repeatable |
| `--loss PROVIDER=VALUE` | Fraction of billed time lost to setup, retries and idle | From 0 inclusive to 1 exclusive |
| `--extra PROVIDER=VALUE` | Replace monthly non-compute allowance | Nonnegative USD; repeatable |
| `--min-vram` | Reject insufficient memory in any mode | 0 GiB |
| `--min-reliability` | Sniper-only minimum illustrative reliability | 0.98 |
| `--min-download` | Sniper-only minimum download bandwidth | 100 Mbps |

Provider names must match the table exactly, including spaces; quote the entire assignment in your shell. Unknown providers, invalid tiers, negative inputs and non-finite numbers fail with a nonzero exit code. Eligibility filters mark excluded candidates with `N`; if the reference Vast.ai fixture fails, the script exits rather than recommending an ineligible reference. Reliability and lost time are independent inputs: neither is automatically derived from the other.

The calculator uses:

```text
reference_hours = units / units_per_hour             # batch mode
reference_hours = hours                            # other modes
billed_hours = reference_hours / relative_speed / (1 - lost_fraction)
monthly_USD = billed_hours * hourly_rate + monthly_non_compute_USD
annual_savings_vs_Vast = 12 * (candidate_monthly_USD - Vast_monthly_USD)
USD_per_1000_units = monthly_USD / (reference_hours * units_per_hour) * 1000
```

A positive savings number is the modeled annual amount avoided by choosing Vast.ai instead of that row. A negative number means the alternative is cheaper. Costs are calculated with unrounded floats and rounded only for display. The annual figure extrapolates twelve identical months; it does not forecast future Spot prices. Billed hours are aggregate worker hours, so values above 730 can require multiple workers or a longer deadline. Parallel capacity, queue wait and procurement failure are not simulated.

Actual local terminal output from `python3 calculate_vastai_spot_tco.py`:

```text
OFFLINE SCENARIO - USD; rates and throughput are assumptions
Mode: batch; tier: rtx4090; useful reference hours/month: 200.00
| Provider     | GPU         | Bill h/mo | USD/mo   | USD/year  | Save/yr vs Vast | OK |
|--------------|-------------|-----------|----------|-----------|-----------------|----|
| Vast.ai      | RTX 4090    |    217.39 |    96.09 |   1153.04 |            0.00 | Y  |
| GCP Spot     | T4          |    634.92 |   302.22 |   3626.67 |         2473.62 | Y  |
| Azure Spot   | A10         |    317.46 |   276.35 |   3316.19 |         2163.15 | Y  |
| Paperspace   | A4000       |    416.67 |   356.67 |   4280.00 |         3126.96 | Y  |
| AWS Spot     | A10G        |    317.46 |   265.48 |   3185.71 |         2032.67 | Y  |
| Salad        | RTX 4090    |    276.82 |   108.04 |   1296.54 |          143.50 | Y  |
Positive savings = annual USD avoided by selecting Vast.ai for equal useful work.
Cheapest eligible: Vast.ai
Workload: embeddings; units/month: 1e+06
Vast.ai: USD/1000 units=0.0961
GCP Spot: USD/1000 units=0.3022
Azure Spot: USD/1000 units=0.2763
Paperspace: USD/1000 units=0.3567
AWS Spot: USD/1000 units=0.2655
Salad: USD/1000 units=0.1080
Compare available Vast.ai offers: https://is.gd/kKRWDd
```

For a downside case, increase Vast.ai's rate and lost time or lower a competitor's price using the overrides. Run both tiers and inspect signed savings in JSON. In batch mode, `--units 18000 --workload whisper` switches units to audio minutes; an explicit `--units-per-hour` overrides the synthetic preset. In performance mode, the printed DLPerf/USD-h is an assumed score divided by hourly price, while the completed-unit cost also includes retries and extras.

## 4. Migration checklist and related repositories

- [ ] Write stable document IDs or audio segment IDs before launching retryable workers.
- [ ] Validate embedding similarity or transcription word error rate on a fixed holdout sample.
- [ ] Measure reference units per hour on the selected GPU tier, including preprocessing.
- [ ] Checkpoint each shard and reconcile completed units before destroying scratch storage.
- [ ] Confirm current all-in quote, mandatory GPU count, region, bandwidth terms and disk retention charges.
- [ ] Stage a small representative dataset; verify access controls and avoid putting secrets into images.
- [ ] Export results before teardown and inspect retained disks after the job ends.
- [ ] Compare one real invoice and one completed-work measurement with the offline scenario.

**[Start with a small Vast.ai pilot](https://is.gd/kKRWDd)** and scale after validating completion cost and recovery behavior.

The other three standalone repositories in this pack:

- [GPU TCO: Vast.ai RTX 4090 / H100 versus cloud Spot](../gcp-aws-spot-gpu-vs-vastai-rtx4090-h100-tco)
- [DLPerf per dollar: Paperspace, Salad and Vast.ai](../paperspace-salad-vs-vastai-dlperf-per-dollar)
- [Vast.ai host sniper: cheapest eligible completed work](../vastai-cli-cheapest-reliable-host-sniper)

### Open-source license

MIT License. Copyright (c) 2026 vastai-spot contributors. This license covers the calculator and this README.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
