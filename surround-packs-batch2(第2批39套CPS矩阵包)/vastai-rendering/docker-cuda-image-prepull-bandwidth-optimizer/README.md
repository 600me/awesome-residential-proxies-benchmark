# Docker CUDA Image Pre-pull Bandwidth Optimizer

[![Vast.ai cost planner](https://img.shields.io/badge/Vast.ai-compare_GPU_costs-22c55e)](https://gpu.mybskm.top/go/vastai)
[![Python standard library](https://img.shields.io/badge/Python-3_standard_library-3776AB)](https://gpu.mybskm.top/go/vastai)
[![License MIT](https://img.shields.io/badge/License-MIT-blue)](https://gpu.mybskm.top/go/vastai)

**[Compare available Vast.ai offers before committing your batch budget](https://gpu.mybskm.top/go/vastai)**

## 1. The engineering problem and the monthly loss

A large CUDA image repeatedly downloaded for short jobs can turn a cheap GPU into a paid network waiter. With eight workers, 40 launches per worker-month and a compressed 32 GB image, cold starts move 10,240 GB before any output video is delivered. At 400 effective Mbps per worker, that is 56.89 aggregate paid GPU-hours fetching image bytes. Source-registry transfer expense can exceed the cost of those idle GPU-hours.

Render Network and OctaneCloud are managed-rendering comparison labels, not verified destinations for arbitrary Docker images. Their asset uploads, scene formats and native caching rules need actual service quotes. The competitor rows are counterfactual equivalent-cost envelopes under the same cold-start workload. They do not claim either provider performs or charges for Docker pulls. A raw render-credit quote cannot substitute for measuring a custom Blender or ComfyUI container startup.

The default fleet performs 1,280 useful GPU-hours per month. It assumes a 90% complete-image cache-hit rate, leaving 1,024 GB downloaded and 5.69 aggregate paid GPU-hours spent pulling images after caching. Source-registry transfer is assumed at $0.02 per downloaded GB, separate from 100 GB of output egress. Persistent storage is 200 GB-month and operator labor is one hour. Cache population remains a paid miss; it is never treated as free.

**Concrete budget exposure:** the cheapest modeled Vast.ai option is **$526.47/month**. The Render Network equiv. scenario is $1,338.60 more per month and $16,063.15 more per year. The OctaneCloud equiv. scenario is $1,739.66 more per month and $20,875.95 more per year. Caching alone saves $202.24/month, or $2,426.88/year, versus cold pulls on the same Vast.ai rate. These are reproducible assumption-based losses, not observed invoices or measured vendor performance.

**[Inspect a Vast.ai offer and replace the assumed hourly rates](https://gpu.mybskm.top/go/vastai)**

## 2. Price and technical comparison

**Price basis:** this repository is intentionally offline. It includes no verified live offers, archived vendor quotes or measured cross-provider results. The $0.35 RTX 4090 GPU-hour is a planning benchmark. The $1.20 and $1.50 figures are explicit comparison assumptions in equivalent GPU-hours; they are not published Render Network or OctaneCloud rental prices. No defensible current price for either competitor is asserted here. Do not cite these scenario figures as real vendor tariffs.

| Parameter / unit | Vast.ai | Render Network | OctaneCloud | How to make the comparison valid |
|---|---|---|---|---|
| Compute budget input, USD/reference GPU-hour | $0.35 assumed | $1.20 equivalent, assumed | $1.50 equivalent, assumed | Replace every rate with an actual comparable quote |
| Source-registry transfer budget, USD/GB | $0.02 assumed | $0.02 counterfactual allowance | $0.02 counterfactual allowance | Replace with quote-native asset transfer rules |
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
python3 calculate_vastai_rendering_tco.py --cache-hit-rate 0 --json
python3 calculate_vastai_rendering_tco.py --image-gb 48 --bandwidth-mbps 100
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
| `--hours` | 160 | Useful compute hours per GPU-month. |
| `--image-gb` | 32 | Compressed bytes per full cold image, decimal GB. |
| `--launches-per-gpu` | 40 | Monthly launches per independent GPU worker. |
| `--bandwidth-mbps` | 400 | Effective download Mbps per worker; must be positive. |
| `--cache-hit-rate` | 0.90 | Fraction of launches downloading zero image bytes, between 0 and 1. |
| `--registry-egress-rate` | 0.02 | Assumed source-registry USD per downloaded GB. |
| `--labor-hours` | 1 | Monthly operator hours for the fleet. |

Explicit `--gpus` overrides `--tier`. Numeric inputs must be finite and nonnegative, with positive worker counts and the stricter bounds above. Invalid inputs exit with code 2; the default invocation exits with code 0. JSON mode prints only one JSON object; its `gateway` field contains the action URL. The normal mode prints an ASCII component bill and the gateway URL on its own line.

```text
cold_GB = GPUs * launches_per_GPU * compressed_image_GB
cached_GB = cold_GB * (1 - cache_hit_fraction)
paid_pull_GPU_hours = downloaded_GB * 8000 / effective_Mbps / 3600
monthly_USD = (useful_GPU_hours + paid_pull_GPU_hours) * rate
              + downloaded_GB * registry_USD_per_GB
              + storage + output_transfer + operator_labor
```

Measure transferred image bytes on a cold host, not the unpacked on-disk size. Decimal GB contain one billion bytes; multiplying by 8,000 converts GB to megabits before dividing by effective Mbps and 3,600 seconds per hour. Effective throughput must include network contention. The model serializes download and useful computation on each paid worker; it does not add aggregate fleet download hours to elapsed wall time.

The cache model treats each hit as avoiding every image byte and every miss as a full image download. Partial layer reuse should be expressed as an empirically equivalent byte-avoidance fraction. The first cold download and later eviction misses must be included in the observed miss count. For multiple GPUs sharing a host cache, adjust per-worker launches or effective bytes so the same physical download is not charged once per GPU and again per host.

Actual terminal output captured from the local default invocation:

```text
Docker CUDA image pre-pull bandwidth TCO
Price basis: offline assumptions; competitor equivalents are not vendor quotes.
Tier: studio | GPUs: 8 | all amounts USD/month
+---------------------------+------------+----------+----------+----------+------------+
| Scenario                  | Compute    | Storage  | Transfer | Ops      | Total      |
+---------------------------+------------+----------+----------+----------+------------+
| Vast.ai cold pulls        |     467.91 |    14.00 |   206.80 |    40.00 |     728.71 |
| Vast.ai pre-pulled        |     449.99 |    14.00 |    22.48 |    40.00 |     526.47 |
| Render Network equiv.     |    1604.27 |    14.00 |   206.80 |    40.00 |    1865.07 |
| OctaneCloud equiv.        |    2005.33 |    14.00 |   206.80 |    40.00 |    2266.13 |
+---------------------------+------------+----------+----------+----------+------------+
cold_registry_gb: 10240.0000
cached_registry_gb: 1024.0000
cold_paid_idle_gpu_hours: 56.8889
cached_paid_idle_gpu_hours: 5.6889
cache_annual_savings_vs_cold: 2426.8800
Annualized savings vs Render Network equiv.: $16,063.15
Annualized savings vs OctaneCloud equiv.: $20,875.95
Annualization = 12 identical months; negative savings mean Vast costs more.
https://gpu.mybskm.top/go/vastai
```

Full precision is retained for arithmetic and JSON; the terminal bill rounds displayed costs to cents. Annual savings against each competitor use twelve times its monthly total minus the cheapest modeled Vast.ai monthly total. A negative saving means that competitor assumption is cheaper. The variant-specific annual metric separately reports bid versus fixed-price or caching versus cold pulls. Twelve identical months are assumed, without discounted cash flow. Fleet storage, output transfer and operator time are monthly totals, not per-GPU multipliers.

Pre-pulling after GPU billing starts does not eliminate the first paid download. Savings come from avoiding repeated pulls or arranging an actual unbilled warm-up period under the offer's terms. The calculator does not contact hosts, modify Docker or pull images. Layer decompression, model-weight downloads, extra cache disk and maintenance labor require separate measured allowances. If the source registry has no egress charge, set its rate to zero; do not pay the same network charge through both registry and output-GB inputs.

**[Choose a Vast.ai candidate and rerun with measured rates and overhead](https://gpu.mybskm.top/go/vastai)**

A feasible monthly plan must also fit the available worker calendar. If modeled paid hours per worker exceed the hours you can actually rent, add workers or reduce the batch; a lower dollar estimate does not create capacity. For video workloads, `ideal_elapsed_hours` is only a lower bound under independent workers. Storage and transfer limits, queue delay and host outages can lengthen delivery.

## 4. Migration checklist and companion repositories

- [ ] Check driver and CUDA runtime compatibility, container support and persistent disk headroom on the selected host.
- [ ] Pin image digests; remove unnecessary layers and never embed credentials in a container.
- [ ] Keep model weights on a persistent mount and budget their downloads separately from image bytes.
- [ ] Measure cold and warm launch-to-ready time, source-registry bytes and image extraction time.
- [ ] Confirm layer persistence across the actual relaunch and eviction pattern; include initial warming in misses.
- [ ] Compare accepted work per billed dollar after a small rollout, including extra cache disk and maintenance labor.

Retain an accepted-output baseline and a rollback workflow before scaling past a canary job. Verify the exact service, renderer and license compatibility for each competing quote. After the first production batch, compare a complete invoice with the estimate, then update price, throughput, storage, transfer and recovery assumptions.

Each companion repository contains its own standalone calculator for a separate source of GPU waste:

- [Cloud Render Farm vs Vast.ai: Multi-RTX 4090 Cost](../cloud-render-farm-vs-vastai-multi-rtx4090-cost)
- [ComfyUI Headless Batch Video Generation TCO](../comfyui-headless-batch-video-generation-tco)
- [Uninterruptible vs Bid Instance Pricing Simulator](../uninterruptible-vs-bid-instance-pricing-simulator)

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
