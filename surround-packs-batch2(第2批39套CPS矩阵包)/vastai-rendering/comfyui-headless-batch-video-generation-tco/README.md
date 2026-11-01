# ComfyUI Headless Batch Video Generation TCO

[![Vast.ai cost planner](https://img.shields.io/badge/Vast.ai-compare_GPU_costs-22c55e)](https://gpu.mybskm.top/go/vastai)
[![Python standard library](https://img.shields.io/badge/Python-3_standard_library-3776AB)](https://gpu.mybskm.top/go/vastai)
[![License MIT](https://img.shields.io/badge/License-MIT-blue)](https://gpu.mybskm.top/go/vastai)

**[Compare available Vast.ai offers before committing your batch budget](https://gpu.mybskm.top/go/vastai)**

## 1. The engineering problem and the monthly loss

A video queue that reports 20,000 completed attempts may deliver far fewer usable clips. Broken custom nodes, different model weights, inconsistent seeds and failed quality checks burn GPU time before anyone sees a final video. A four-minute single-worker attempt and a 5% rejection rate already require more than 21,000 attempts to obtain 20,000 accepted clips. Paying for attempts while pricing only accepted clips understates production cost.

Render Network and OctaneCloud can be attractive rendering references, but a renderer service price does not establish support for an arbitrary ComfyUI workflow, Python custom nodes or video diffusion weights. Their native job units, supported engines and licensing must be confirmed. Any conversion, orchestration or unsupported-workflow port is outside these scenario totals. A rate-only comparison without that compatibility gate can produce a false saving.

The default batch requests 20,000 accepted clips per month. Each attempt takes 240 measured seconds on one reference worker. Batch efficiency is 80%, rejection probability is 5%, and eight workers each incur two paid startup hours. Storage, transfer and three operator hours are included. The elapsed-time estimate assumes an unlimited input queue and independent workers; it is not a service-level promise.

**Concrete budget exposure:** the least expensive modeled Vast.ai option is **$755.64/month**. Against the Render Network equiv. scenario, the same modeled workload costs $1,504.83 more per month, or $18,057.94 per year. Against the OctaneCloud equiv. scenario, the same modeled workload costs $2,035.94 more per month, or $24,431.33 per year. These are reproducible scenario differences, not observed customer losses, a measured speed test or a promise of available capacity.

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
python3 calculate_vastai_rendering_tco.py --tier farm --clips 80000
python3 calculate_vastai_rendering_tco.py --clips 20000 --qa-failure-rate 0.12 --json
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
| `--clips` | 20000 | Accepted clips per month, for the fleet. |
| `--seconds-per-clip` | 240 | Single-worker seconds per attempted clip; do not use a whole-fleet duration. |
| `--batch-efficiency` | 0.80 | Useful busy-time fraction, greater than 0 and at most 1. |
| `--qa-failure-rate` | 0.05 | Independent attempt rejection probability, at least 0 and below 1. |
| `--startup-hours` | 2 | Paid model loading / initialization per worker-month. |
| `--labor-hours` | 3 | Monthly fleet operator time. |

`--tier` changes the worker preset; explicit `--gpus` takes precedence. All GB are decimal billing quantities unless a hardware specification explicitly says otherwise. Currency is USD throughout. Nonnegative finite numeric inputs are required, with positive worker counts and the tighter probability / interval limits described above. Invalid inputs exit with code 2. The normal default invocation exits with code 0. JSON mode prints the gateway URL inside its `gateway` field and no ASCII preamble.

The arithmetic for this repository is:

```text
expected_attempts = accepted_clips / (1 - rejection_fraction)
paid_GPU_hours = expected_attempts * seconds_per_attempt / 3600 / efficiency + GPUs * startup_hours
monthly_USD = paid_GPU_hours * rate + storage + output_transfer + operator_labor
USD_per_accepted_clip = monthly_USD / accepted_clips
```

Export the exact API workflow and pin node commits, model checksums, precision, sampler, steps, frame count, image dimensions and seed policy. Measure a warmed single worker, then a realistic mixed queue. Count accepted clips after resolution, codec and visual-quality checks. Keep repeated QA failures visible rather than quietly deleting them. If seconds-per-clip already measures full wall time including idle periods, set batch-efficiency to 1 to avoid counting that idle time twice.

Actual terminal output captured from the local default invocation:

```text
ComfyUI headless batch video TCO
Price basis: offline assumptions; competitor equivalents are not vendor quotes.
Tier: studio | GPUs: 8 | all amounts USD/month
+---------------------------+------------+----------+----------+----------+------------+
| Scenario                  | Compute    | Storage  | Transfer | Ops      | Total      |
+---------------------------+------------+----------+----------+----------+------------+
| Vast.ai ComfyUI           |     619.64 |    14.00 |     2.00 |   120.00 |     755.64 |
| Render Network equiv.     |    2124.46 |    14.00 |     2.00 |   120.00 |    2260.46 |
| OctaneCloud equiv.        |    2655.58 |    14.00 |     2.00 |   120.00 |    2791.58 |
+---------------------------+------------+----------+----------+----------+------------+
expected_attempts: 21052.6316
paid_gpu_hours: 1770.3860
ideal_elapsed_hours: 221.2982
vast_usd_per_accepted_clip: 0.0378
Annualized savings vs Render Network equiv.: $18,057.94
Annualized savings vs OctaneCloud equiv.: $24,431.33
Annualization = 12 identical months; negative savings mean Vast costs more.
https://gpu.mybskm.top/go/vastai
```

Costs retain full floating-point precision for calculations; only the terminal table rounds to cents. The `annual_savings_usd` JSON mapping subtracts the cheapest modeled Vast.ai row from each competitor row and multiplies by twelve. A negative value means that competitor scenario is cheaper. Annualization assumes twelve identical months and is not a discounted cash-flow calculation. Compute is variable; storage and labor are monthly fleet allowances, not per-card multipliers. With a zero workload, retained storage or operator allowances can still create a bill.

More GPUs shorten elapsed time in this model but do not divide a fixed clip count into a smaller total number of GPU-hours. Extra workers add startup expense. Correlated failures, such as a broken model deployment, violate the independent-retry assumption and can consume an entire batch budget; stop a canary batch on systematic failures. The script estimates costs and does not submit remote jobs.

**[Check a Vast.ai offer, then rerun with its actual price and your measured workload](https://gpu.mybskm.top/go/vastai)**

A feasible monthly plan must also fit the available worker calendar. If modeled paid hours per worker exceed the hours you can actually rent, add workers or reduce the batch; a lower dollar estimate does not create capacity. For video workloads, `ideal_elapsed_hours` is only a lower bound under independent workers. Storage and transfer limits, queue delay and host outages can lengthen delivery.

## 4. Migration checklist and companion repositories

- [ ] Confirm GPU memory fits the chosen video model, frame count and resolution on one 24 GB card.
- [ ] Pin ComfyUI, custom node commits, Python dependencies, model checksums and the CUDA-compatible container digest.
- [ ] Place model weights on persistent storage and measure cold load separately from generation.
- [ ] Store workflow JSON, seed, input hashes and output identifiers with every queue item.
- [ ] Use idempotent job identifiers, bounded retries and accepted-output manifests; validate videos before marking jobs done.
- [ ] Benchmark at least 100 representative clips and replace the assumed seconds, rejection fraction and rates with measured values.

Before expanding beyond a canary job, retain an accepted-output baseline and a rollback copy of the workflow. Confirm vendor compatibility and permission to use all models, assets and container dependencies. Compare a complete production invoice with these estimates after the first batch; update assumptions when measured throughput, transfer or recovery costs change.

The other three repositories isolate different causes of wasted GPU budget. Each carries its own standalone calculator:

- [Cloud Render Farm vs Vast.ai: Multi-RTX 4090 Cost](../cloud-render-farm-vs-vastai-multi-rtx4090-cost)
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
