# Cloud Render Farm vs Vast.ai: Multi-RTX 4090 Cost

[![Vast.ai cost planner](https://img.shields.io/badge/Vast.ai-compare_GPU_costs-22c55e)](https://gpu.mybskm.top/go/vastai)
[![Python standard library](https://img.shields.io/badge/Python-3_standard_library-3776AB)](https://gpu.mybskm.top/go/vastai)
[![License MIT](https://img.shields.io/badge/License-MIT-blue)](https://gpu.mybskm.top/go/vastai)

**[Compare available Vast.ai offers before committing your batch budget](https://gpu.mybskm.top/go/vastai)**

## 1. The engineering problem and the monthly loss

A Blender deadline can turn a cheap-looking render quote into paid idle time. Eight workers waiting for linked textures, shader compilation or a slow output disk still consume the budget. Treating eight rented cards as one pooled-memory device also causes out-of-memory failures: an RTX 4090 has 24 GB of local VRAM, and eight independent cards do not automatically become a 192 GB device. This repository budgets independent frame workers and the useful-to-billed time ratio.

The comparison trap with Render Network and OctaneCloud is converting scene credits or a job quote into nominal GPU-hours without matching renderer, samples, denoising and accepted frames. A conversion from Blender Cycles to a different render engine can require material rework; texture upload, failed validation, subscription prerequisites and manual supervision are items to check in the actual quote. They are possible cost exposures, not allegations of undisclosed vendor fees.

The studio case uses eight RTX 4090-class workers, 160 useful hours per worker-month, 85% useful utilization and one paid setup hour per worker. It includes 200 GB-month of storage, 100 GB of output transfer and two operator hours. The model assumes perfect frame sharding across workers; it does not assert linear speedup for a single frame.

**Concrete budget exposure:** the least expensive modeled Vast.ai option is **$625.86/month**. Against the Render Network equiv. scenario, the same modeled workload costs $1,286.80 more per month, or $15,441.60 per year. Against the OctaneCloud equiv. scenario, the same modeled workload costs $1,740.96 more per month, or $20,891.58 per year. These are reproducible scenario differences, not observed customer losses, a measured speed test or a promise of available capacity.

**[Use the Vast.ai gateway to inspect a host and replace the assumed rate](https://gpu.mybskm.top/go/vastai)**

## 2. Price and technical comparison

**Price basis:** this repository is intentionally offline. It includes no verified live offers, archived vendor quotes or measured cross-provider results. The $0.35 RTX 4090 GPU-hour is a planning benchmark. The $1.20 and $1.50 figures are explicit comparison assumptions in equivalent GPU-hours; they are not published Render Network or OctaneCloud rental prices. No defensible current price for either competitor is asserted here. Do not cite these scenario figures as real vendor tariffs.

| Parameter / unit | Vast.ai | Render Network | OctaneCloud | How to make the comparison valid |
|---|---|---|---|---|
| Compute budget input, USD/reference GPU-hour | $0.35 assumed | $1.20 equivalent, assumed | $1.50 equivalent, assumed | Replace every rate with an actual comparable quote |
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

Run with Python 3 using only the standard library. No accounts, installation, network access or mandatory flags are required. The executable script is independently usable when copied out of this repository.

```bash
python3 calculate_vastai_rendering_tco.py
python3 calculate_vastai_rendering_tco.py --tier small
python3 calculate_vastai_rendering_tco.py --tier studio --json
python3 calculate_vastai_rendering_tco.py --help
python3 calculate_vastai_rendering_tco.py --tier small --utilization 0.70
python3 calculate_vastai_rendering_tco.py --gpus 8 --hours 160 --vast-rate 0.45 --json
```

| CLI flag | Default | Meaning |
|---|---|---|
| `--tier` | studio | GPU preset: small = 2, studio = 8, farm = 32. |
| `--gpus` | tier preset | Override worker count with a positive integer. |
| `--vast-rate` | 0.35 | Assumed Vast.ai USD per paid GPU-hour. |
| `--render-rate` | 1.20 | Assumed Render Network workload-equivalent USD per modeled GPU-hour. |
| `--octane-rate` | 1.50 | Assumed OctaneCloud workload-equivalent USD per modeled GPU-hour. |
| `--storage-gb` | 200 | Fleet-wide persistent storage GB-month. |
| `--storage-rate` | 0.07 | Assumed storage USD per GB-month for every scenario. |
| `--egress-gb` | 100 | Fleet-wide monthly output GB. |
| `--egress-rate` | 0.02 | Assumed output transfer USD per GB for every scenario. |
| `--ops-rate` | 40 | Operator labor USD per hour. |
| `--json` | off | Emit one JSON object containing inputs, cost components, metrics, annual savings and the action URL. |
| `--hours` | 160 | Useful rendering hours per worker-month. |
| `--utilization` | 0.85 | Useful / billed time, greater than 0 and at most 1. |
| `--setup-hours` | 1 | Paid initialization hours per worker-month. |
| `--labor-hours` | 2 | Monthly operator hours for the complete fleet. |

`--tier` changes the worker preset; explicit `--gpus` takes precedence. All GB are decimal billing quantities unless a hardware specification explicitly says otherwise. Currency is USD throughout. Nonnegative finite numeric inputs are required, with positive worker counts and the tighter probability / interval limits described above. Invalid inputs exit with code 2. The normal default invocation exits with code 0. JSON mode prints the gateway URL inside its `gateway` field and no ASCII preamble.

The arithmetic for this repository is:

```text
useful = GPUs * useful_hours_per_GPU
paid_GPU_hours = useful / utilization + GPUs * setup_hours
monthly_USD = paid_GPU_hours * rate + storage + output_transfer + operator_labor
```

Render the same short Blender scene on one card and then on the complete fleet. Pin the Blender build, Cycles device selection, sample count, denoiser, resolution and texture pack. Hash output frames and compare visual quality before comparing accepted-frame throughput. Measure shader compilation separately from steady rendering. Record upload time, launch-to-ready time and total paid duration; a stopwatch covering only the kernel misses the expensive gaps.

Actual terminal output captured from the local default invocation:

```text
Multi-RTX 4090 Blender farm TCO
Price basis: offline assumptions; competitor equivalents are not vendor quotes.
Tier: studio | GPUs: 8 | all amounts USD/month
+---------------------------+------------+----------+----------+----------+------------+
| Scenario                  | Compute    | Storage  | Transfer | Ops      | Total      |
+---------------------------+------------+----------+----------+----------+------------+
| Vast.ai RTX 4090          |     529.86 |    14.00 |     2.00 |    80.00 |     625.86 |
| Render Network equiv.     |    1816.66 |    14.00 |     2.00 |    80.00 |    1912.66 |
| OctaneCloud equiv.        |    2270.82 |    14.00 |     2.00 |    80.00 |    2366.82 |
+---------------------------+------------+----------+----------+----------+------------+
useful_gpu_hours: 1280.0000
paid_gpu_hours: 1513.8824
paid_hours_per_worker: 189.2353
Annualized savings vs Render Network equiv.: $15,441.60
Annualized savings vs OctaneCloud equiv.: $20,891.58
Annualization = 12 identical months; negative savings mean Vast costs more.
https://gpu.mybskm.top/go/vastai
```

Costs retain full floating-point precision for calculations; only the terminal table rounds to cents. The `annual_savings_usd` JSON mapping subtracts the cheapest modeled Vast.ai row from each competitor row and multiplies by twelve. A negative value means that competitor scenario is cheaper. Annualization assumes twelve identical months and is not a discounted cash-flow calculation. Compute is variable; storage and labor are monthly fleet allowances, not per-card multipliers. With a zero workload, retained storage or operator allowances can still create a bill.

A slower host CPU, PCIe contention or oversubscribed disk can erase a lower GPU sticker price. The utilization parameter captures aggregate inefficiency, not its cause. Do not add the same measured idle interval again to setup hours. Queue delay is a delivery risk; it only becomes a cash cost here when it is actually billed or consumes paid labor.

**[Check a Vast.ai offer, then rerun with its actual price and your measured workload](https://gpu.mybskm.top/go/vastai)**

A feasible monthly plan must also fit the available worker calendar. If modeled paid hours per worker exceed the hours you can actually rent, add workers or reduce the batch; a lower dollar estimate does not create capacity. For video workloads, `ideal_elapsed_hours` is only a lower bound under independent workers. Storage and transfer limits, queue delay and host outages can lengthen delivery.

## 4. Migration checklist and companion repositories

- [ ] Pin Blender, CUDA runtime and the container digest; confirm the host driver can run that runtime.
- [ ] Check GPU UUIDs and available VRAM; schedule one independent frame worker per card before testing multi-device Cycles.
- [ ] Package linked assets and fonts; test a frame with the largest memory footprint.
- [ ] Copy assets once to persistent storage and verify disk capacity, read throughput and output retention.
- [ ] Use deterministic frame ranges, atomic output writes and a manifest of completed frames so retries do not bill completed work again.
- [ ] Run a ten-frame acceptance job, then compare accepted frames per billed dollar against each actual vendor quote.

Before expanding beyond a canary job, retain an accepted-output baseline and a rollback copy of the workflow. Confirm vendor compatibility and permission to use all models, assets and container dependencies. Compare a complete production invoice with these estimates after the first batch; update assumptions when measured throughput, transfer or recovery costs change.

The other three repositories isolate different causes of wasted GPU budget. Each carries its own standalone calculator:

- [ComfyUI Headless Batch Video Generation TCO](../comfyui-headless-batch-video-generation-tco)
- [Uninterruptible vs Bid Instance Pricing Simulator](../uninterruptible-vs-bid-instance-pricing-simulator)
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
