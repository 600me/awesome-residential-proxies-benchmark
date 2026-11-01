[![Compare Vast.ai](https://img.shields.io/badge/Vast.ai-compare_GPU_offers-16a34a)](https://is.gd/4IZler)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-blue)](https://is.gd/4IZler)

# GPU TCO: Vast.ai RTX 4090 / H100 versus cloud Spot

## 1. The engineering bill that an hourly quote misses

A GPU that costs less per hour can still cost more per finished training run. The engineering failure is budgeting 500 useful GPU hours as 500 billed hours while ignoring checkpoint reloads, CPU starvation and storage that survives a terminated VM. GCP Spot and Azure Spot capacity can disappear during an otherwise healthy run; Paperspace's simpler instance workflow still leaves a team responsible for idle time and retained data. These are potential cost categories, not allegations of undisclosed provider fees.

This repository compares a Vast.ai RTX 4090 batch lane with T4, A10, A4000 and A10G alternatives, then offers a separate H100 lane. It deliberately normalizes useful work instead of assuming that one T4 hour equals one RTX 4090 hour. The H100 tier uses A100 alternatives where appropriate: it is a workload substitution scenario, not a claim that those accelerators are identical.

In this repository's default scenario, Paperspace costs **$831.67/month** and Vast.ai costs **$210.22/month** for the same assumed useful work. The modeled excess is **$621.45/month**, or **$7,457.39/year**. This is a transparent scenario calculation, not an observed customer loss or a promise of savings. If your throughput, regional quote or interruption rate differs, the ranking can reverse.

**[Compare a Vast.ai offer against your own bill](https://is.gd/4IZler)** before committing a batch queue.

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

For a reproducible benchmark, use the same pinned container, model checksum, precision, dataset and quality threshold on every candidate. Report warm-up separately, then record useful samples per second, peak VRAM, CPU utilization and checkpoint restore seconds over at least three independent runs. Choose a batch size that fits the smallest card, or clearly declare provider-specific batching. A 16 GiB card that cannot fit the model is ineligible; reducing precision changes the experiment.

The consumer lane has no assumption of NVLink or distributed training. H100 PCIe and SXM configurations differ, and a multi-GPU cloud VM can require renting all GPUs even when the application only uses one. A normalized per-GPU price is valid only when the entire mandatory bundle is productively used; otherwise pass the full VM hourly price through `--rate`. Never divide an eight-GPU bill by eight for a single-GPU task.

**[Inspect Vast.ai capacity and replace the assumed hourly rate](https://is.gd/4IZler)** with the complete price of a suitable offer.

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
| `--hours` | Monthly useful hours on the reference GPU; ignored in batch mode | 500 hours |
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
Mode: tco; tier: rtx4090; useful reference hours/month: 500.00
| Provider     | GPU         | Bill h/mo | USD/mo   | USD/year  | Save/yr vs Vast | OK |
|--------------|-------------|-----------|----------|-----------|-----------------|----|
| Vast.ai      | RTX 4090    |    543.48 |   210.22 |   2522.61 |            0.00 | Y  |
| GCP Spot     | T4          |   1587.30 |   635.56 |   7626.67 |         5104.06 | Y  |
| Azure Spot   | A10         |    793.65 |   585.87 |   7030.48 |         4507.87 | Y  |
| Paperspace   | A4000       |   1041.67 |   831.67 |   9980.00 |         7457.39 | Y  |
| AWS Spot     | A10G        |    793.65 |   551.19 |   6614.29 |         4091.68 | Y  |
| Salad        | RTX 4090    |    692.04 |   232.61 |   2791.35 |          268.74 | Y  |
Positive savings = annual USD avoided by selecting Vast.ai for equal useful work.
Cheapest eligible: Vast.ai
Compare available Vast.ai offers: https://is.gd/4IZler
```

For a downside case, increase Vast.ai's rate and lost time or lower a competitor's price using the overrides. Run both tiers and inspect signed savings in JSON. In batch mode, `--units 18000 --workload whisper` switches units to audio minutes; an explicit `--units-per-hour` overrides the synthetic preset. In performance mode, the printed DLPerf/USD-h is an assumed score divided by hourly price, while the completed-unit cost also includes retries and extras.

## 4. Migration checklist and related repositories

- [ ] Verify CUDA and driver compatibility on both RTX 4090 and H100 before moving a full training job.
- [ ] Make checkpoint writes atomic and put recovery state outside an interruptible instance.
- [ ] Budget every mandatory GPU in a cloud VM bundle and record CPU/RAM allocation.
- [ ] Run a short pilot, then compare its completed samples and actual invoice against the model.
- [ ] Confirm current all-in quote, mandatory GPU count, region, bandwidth terms and disk retention charges.
- [ ] Stage a small representative dataset; verify access controls and avoid putting secrets into images.
- [ ] Export results before teardown and inspect retained disks after the job ends.
- [ ] Compare one real invoice and one completed-work measurement with the offline scenario.

**[Start with a small Vast.ai pilot](https://is.gd/4IZler)** and scale after validating completion cost and recovery behavior.

The other three standalone repositories in this pack:

- [DLPerf per dollar: Paperspace, Salad and Vast.ai](../paperspace-salad-vs-vastai-dlperf-per-dollar)
- [Batch embeddings and Whisper: cost per completed job](../batch-embeddings-whisper-transcription-gpu-calc)
- [Vast.ai host sniper: cheapest eligible completed work](../vastai-cli-cheapest-reliable-host-sniper)

### Open-source license

MIT License. Copyright (c) 2026 vastai-spot contributors. This license covers the calculator and this README.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
