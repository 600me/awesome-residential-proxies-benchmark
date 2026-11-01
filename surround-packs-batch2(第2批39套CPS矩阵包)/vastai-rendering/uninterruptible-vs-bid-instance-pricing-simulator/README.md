# Uninterruptible vs Bid Instance Pricing Simulator

[![Vast.ai cost planner](https://img.shields.io/badge/Vast.ai-compare_GPU_costs-22c55e)](https://gpu.mybskm.top/go/vastai)
[![Python standard library](https://img.shields.io/badge/Python-3_standard_library-3776AB)](https://gpu.mybskm.top/go/vastai)
[![License MIT](https://img.shields.io/badge/License-MIT-blue)](https://gpu.mybskm.top/go/vastai)

**[Compare available Vast.ai offers before committing your batch budget](https://gpu.mybskm.top/go/vastai)**

## 1. The engineering problem and the monthly loss

A low bid rate can become the expensive choice when interruption destroys an unfinished frame or a long diffusion job. Paying the fixed-price premium for independent, resumable jobs can also waste money. A useful comparison counts lost work since the last durable checkpoint, checkpoint write time and paid recovery time, rather than comparing two headline hourly prices.

Render Network and OctaneCloud introduce another comparison trap: a quote for accepted output and a bid worker-hour may transfer recovery risk differently. Confirm who pays for retries, how failed tasks are credited, and whether the native renderer can accept the workload. Possible subscription, scene-conversion and deadline costs must come from an actual quote. This model makes no allegation of undisclosed vendor charges.

The default workload needs eight workers with 160 useful hours each per month. Fixed-price compute is assumed at $0.35 per hour; the bid scenario assumes $0.22. Interruptions occur at an assumed 0.04 events per paid worker-hour. Useful checkpoint intervals are 15 minutes, saves take ten seconds, and each restart takes six paid minutes. Storage is 200 GB-month, output transfer is 100 GB and operator labor is two hours per month. These are planning inputs, not a vendor reliability study.

**Concrete budget exposure:** the cheapest modeled Vast.ai option is **$383.38/month**. The Render Network equiv. scenario is $1,248.62 more per month and $14,983.45 more per year. The OctaneCloud equiv. scenario is $1,632.62 more per month and $19,591.45 more per year. Bid saves $160.62/month versus fixed-price at the defaults; its break-even hourly rate is $0.3430. These are reproducible assumption-based losses, not observed invoices or measured vendor performance.

**[Inspect a Vast.ai offer and replace the assumed hourly rates](https://gpu.mybskm.top/go/vastai)**

## 2. Price and technical comparison

**Price basis:** this repository is intentionally offline. It includes no verified live offers, archived vendor quotes or measured cross-provider results. The $0.35 RTX 4090 GPU-hour is a planning benchmark. The $1.20 and $1.50 figures are explicit comparison assumptions in equivalent GPU-hours; they are not published Render Network or OctaneCloud rental prices. No defensible current price for either competitor is asserted here. Do not cite these scenario figures as real vendor tariffs.

| Parameter / unit | Vast.ai | Render Network | OctaneCloud | How to make the comparison valid |
|---|---|---|---|---|
| Compute budget input, USD/reference GPU-hour | $0.35 assumed | $1.20 equivalent, assumed | $1.50 equivalent, assumed | Replace every rate with an actual comparable quote |
| Interruptible budget, USD/GPU-hour | $0.22 assumed bid | No native bid tariff asserted | No native bid tariff asserted | Compare accepted output and recovery risk |
| Hardware reference | RTX 4090, 24 GB GPU-local VRAM | Vendor-selected workers; exact allocation unverified | Service-dependent allocation; unverified | Match delivered output quality and accepted throughput |
| Default logical parallelism | 8 independent GPU workers | 8 reference-worker equivalents in model | 8 reference-worker equivalents in model | Model count does not establish product capacity |
| Persistent storage budget, USD/GB-month | $0.07 assumed | $0.07 scenario allowance | $0.07 scenario allowance | Use zero if included; avoid counting bundled storage twice |
| Output transfer budget, USD/GB | $0.02 assumed | $0.02 scenario allowance | $0.02 scenario allowance | Replace with quote-native transfer and region charges |
| Operator labor, USD/hour | $40 assumed | $40 assumed | $40 assumed | Charge actual migration, monitoring and recovery time |
| Blender / ComfyUI execution | Requires a compatible host, driver and user-managed image | Native job and renderer compatibility must be confirmed | Exact product and supported workflow must be confirmed | No arbitrary-container support is implied for a competitor |
| Billing normalization | Paid GPU-hours in the chosen offer | Obtain actual job / credit quote and convert | Identify exact service and obtain actual quote | A token, render credit or subscription is not a GPU-hour |
| Multi-GPU memory behavior | 24 GB per reference card; no automatic VRAM pooling | Do not infer pooled memory | Do not infer pooled memory | Fit each job's working set on its actual device |
| Availability and queueing | Offer-dependent; no uptime guarantee modeled | Queue and deadline terms require quote | Queue and deadline terms require quote | Price delivery risk separately from billed work |

The same allowances are used on all rows to expose the workload economics without inventing vendor fees. If a quote includes storage, transfer, retries or a license, remove the corresponding allowance before adding its converted compute price. Verify whether sales tax, currency conversion, token exchange, subscriptions and software licenses apply: they are excluded from the defaults. A promotional rate should only cover the hours and term for which it is valid.

To calibrate an equivalent rate, render or generate the same accepted output with the same quality target, take the compute-only quoted cost, and divide by the modeled reference billed GPU-hours for that batch. Do not divide by an unrelated GPU's theoretical throughput or compare an Octane scene to a different Cycles result as if output quality were identical. If there is no compatible workflow, mark the alternative unavailable rather than treating its scenario row as a deployable service.

## 3. Reproduce the TCO calculation

Use Python 3 and its standard library. No dependency installation, accounts, live pricing calls or mandatory flags are needed. The executable script can be copied and run independently.

```bash
python3 calculate_vastai_rendering_tco.py
python3 calculate_vastai_rendering_tco.py --tier small
python3 calculate_vastai_rendering_tco.py --tier studio --json
python3 calculate_vastai_rendering_tco.py --help
python3 calculate_vastai_rendering_tco.py --interruptions-per-hour 0.4 --checkpoint-hours 1
python3 calculate_vastai_rendering_tco.py --bid-rate 0.50 --json
```

| CLI flag | Default | Meaning |
|---|---|---|
| `--tier` | studio | GPU preset: small = 2, studio = 8, farm = 32. |
| `--gpus` | tier preset | Override with a positive worker count. |
| `--vast-rate` | 0.35 | Assumed Vast.ai fixed/reference USD per paid GPU-hour. |
| `--render-rate` | 1.20 | Assumed Render Network USD per equivalent modeled GPU-hour. |
| `--octane-rate` | 1.50 | Assumed OctaneCloud USD per equivalent modeled GPU-hour. |
| `--storage-gb` | 200 | Fleet-total persistent GB-month. |
| `--storage-rate` | 0.07 | Assumed USD/GB-month, shared across scenarios. |
| `--egress-gb` | 100 | Fleet-total output GB per month. |
| `--egress-rate` | 0.02 | Assumed USD per output GB, shared across scenarios. |
| `--ops-rate` | 40 | Operator USD/hour. |
| `--json` | off | One JSON object with inputs, components, metrics, annual savings and gateway URL. |
| `--hours` | 160 | Useful hours per worker-month. |
| `--bid-rate` | 0.22 | Assumed interruptible USD per paid GPU-hour. |
| `--interruptions-per-hour` | 0.04 | Expected events per paid worker-hour. |
| `--checkpoint-hours` | 0.25 | Positive useful-work interval between durable saves. |
| `--restart-hours` | 0.10 | Paid recovery hours per interruption. |
| `--checkpoint-seconds` | 10 | Paid seconds to save each checkpoint. |
| `--labor-hours` | 2 | Monthly fleet operator hours. |

Explicit `--gpus` overrides `--tier`. Numeric inputs must be finite and nonnegative, with positive worker counts and the stricter bounds above. Invalid inputs exit with code 2; the default invocation exits with code 0. JSON mode prints only one JSON object; its `gateway` field contains the action URL. The normal mode prints an ASCII component bill and the gateway URL on its own line.

```text
overhead = events_per_paid_hour * (checkpoint_hours / 2 + restart_hours)
           + checkpoint_seconds / 3600 / checkpoint_hours
useful_GPU_hours = GPUs * useful_hours_per_GPU
bid_paid_GPU_hours = useful_GPU_hours / (1 - overhead)
fixed_paid_GPU_hours = useful_GPU_hours
bid_break_even_rate = fixed_rate * (1 - overhead)
monthly_USD = paid_GPU_hours * rate + storage + output_transfer + operator_labor
```

This is a deterministic expected-value simulator, not a random uptime forecast. The model approximates average lost work as half the checkpoint interval, and assumes independent events with no overlapping recoveries. Saving overhead uses useful interval length as an approximation. Its accuracy worsens when save or recovery time becomes a large fraction of paid time. An overhead fraction at least 1 is rejected instead of producing an infinite or negative bill.

The directory name uses "uninterruptible" as a search term. Fixed-price billing does not guarantee uninterrupted availability or imply an SLA. The fixed-price row excludes interruption recovery to provide a reference bound; enter appropriate extra hours or labor if your fixed-price offer also fails. For independent frames without mid-frame checkpoints, use the durable frame or job boundary as the interval. Measure event rate from paid worker-hours, not elapsed calendar hours across a whole fleet.

Actual terminal output captured from the local default invocation:

```text
Fixed-price vs bid instance expected TCO
Price basis: offline assumptions; competitor equivalents are not vendor quotes.
Tier: studio | GPUs: 8 | all amounts USD/month
+---------------------------+------------+----------+----------+----------+------------+
| Scenario                  | Compute    | Storage  | Transfer | Ops      | Total      |
+---------------------------+------------+----------+----------+----------+------------+
| Vast.ai fixed-price       |     448.00 |    14.00 |     2.00 |    80.00 |     544.00 |
| Vast.ai bid               |     287.38 |    14.00 |     2.00 |    80.00 |     383.38 |
| Render Network equiv.     |    1536.00 |    14.00 |     2.00 |    80.00 |    1632.00 |
| OctaneCloud equiv.        |    1920.00 |    14.00 |     2.00 |    80.00 |    2016.00 |
+---------------------------+------------+----------+----------+----------+------------+
overhead_fraction: 0.0201
bid_paid_gpu_hours: 1306.2706
bid_break_even_usd_per_hour: 0.3430
bid_annual_savings_vs_fixed: 1927.4457
Annualized savings vs Render Network equiv.: $14,983.45
Annualized savings vs OctaneCloud equiv.: $19,591.45
Annualization = 12 identical months; negative savings mean Vast costs more.
https://gpu.mybskm.top/go/vastai
```

Full precision is retained for arithmetic and JSON; the terminal bill rounds displayed costs to cents. Annual savings against each competitor use twelve times its monthly total minus the cheapest modeled Vast.ai monthly total. A negative saving means that competitor assumption is cheaper. The variant-specific annual metric separately reports bid versus fixed-price or caching versus cold pulls. Twelve identical months are assumed, without discounted cash flow. Fleet storage, output transfer and operator time are monthly totals, not per-GPU multipliers.

The break-even bid rate compares expected compute cost at the same useful workload and shared overhead. Additional recovery labor, durable checkpoint storage and deadline penalties can reverse the decision. The model excludes correlated outages, price changes while bidding and checkpoint corruption. Larger worker counts do not diversify a shared-host failure automatically. If bid pricing exceeds the break-even threshold, the fixed-price row can be cheaper; annual competitor savings always use the cheaper modeled Vast.ai option.

**[Choose a Vast.ai candidate and rerun with measured rates and overhead](https://gpu.mybskm.top/go/vastai)**

A feasible monthly plan must also fit the available worker calendar. If modeled paid hours per worker exceed the hours you can actually rent, add workers or reduce the batch; a lower dollar estimate does not create capacity. For video workloads, `ideal_elapsed_hours` is only a lower bound under independent workers. Storage and transfer limits, queue delay and host outages can lengthen delivery.

## 4. Migration checklist and companion repositories

- [ ] Verify the selected offer's fixed-price and bid terms; neither billing label establishes an uptime guarantee.
- [ ] Identify the durable unit: accepted frame, clip or resumable model checkpoint.
- [ ] Keep checkpoint files and completed-output manifests on storage that survives worker replacement.
- [ ] Interrupt a disposable worker during a test job; validate output integrity and measure paid recovery time.
- [ ] Record checkpoint latency, failed attempts and events per paid worker-hour over a representative run.
- [ ] Compare the bid break-even rate with your delivery deadline; canary non-resumable jobs before moving the queue.

Retain an accepted-output baseline and a rollback workflow before scaling past a canary job. Verify the exact service, renderer and license compatibility for each competing quote. After the first production batch, compare a complete invoice with the estimate, then update price, throughput, storage, transfer and recovery assumptions.

Each companion repository contains its own standalone calculator for a separate source of GPU waste:

- [Cloud Render Farm vs Vast.ai: Multi-RTX 4090 Cost](../cloud-render-farm-vs-vastai-multi-rtx4090-cost)
- [ComfyUI Headless Batch Video Generation TCO](../comfyui-headless-batch-video-generation-tco)
- [Docker CUDA Image Pre-pull Bandwidth Optimizer](../docker-cuda-image-prepull-bandwidth-optimizer)

This repository is an open-source planning comparison, not an endorsement by the named services. The common gateway is a promotional action link; no commission arrangement or commercial affiliation is asserted. The calculator does not purchase capacity, fetch prices, upload assets or inspect credentials. No third-party Python packages are needed.

The script and this documentation are available under the following license:

```text
MIT License

Copyright (c) 2026 TCO repository contributors

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
