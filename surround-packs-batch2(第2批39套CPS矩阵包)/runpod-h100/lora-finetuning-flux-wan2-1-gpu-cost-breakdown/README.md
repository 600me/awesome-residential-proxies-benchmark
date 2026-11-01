[![RunPod GPU planning](https://img.shields.io/badge/RunPod-GPU%20cost%20planner-673AB7)](https://is.gd/GvtNbV)

# FLUX and Wan2.1 LoRA fine-tuning GPU cost breakdown

[Check RunPod capacity and your actual quote](https://is.gd/GvtNbV)

## 1. The engineering pain and the bill it creates

A LoRA experiment is not billed only while the progress bar advances. Dataset extraction, base-model downloads, validation renders, failed launches, and checkpoint uploads can all consume allocated GPU time. A team planning 120 useful training hours per month at 85% productive efficiency actually buys 141.18 hours. At equal billed hours, the H100 reference compute premium over RunPod is $84.71 per month ($1,016.52 annually) for Lambda Labs and $489.89 per month ($5,878.68 annually) for CoreWeave. Replicate that workload across eight independent workers and the modeled monthly premiums become $677.68 and $3,919.12.

The billing trap is quoting the cost of one successful step as the cost of a completed FLUX or Wan2.1 experiment. These model families have different memory and activation patterns, and the 24 GB RTX 4090 can require quantization, reduced resolution, optimizer changes, or CPU offload. An 80 GB H100 may finish sooner even when its hourly price is higher. This repository budgets a workload you measure; it does not invent benchmark throughput or promise that a 4090 runs every configuration. Check base-model and dataset licenses separately from the calculator license.

This is an offline, reproducible purchasing worksheet. The amounts are remembered public list-price reference points, not live-verified October 2026 prices, procurement quotes, measured workloads or a claim of universal provider superiority. RunPod marketplace supply, security class and dedicated capacity can change the price; Lambda Labs and CoreWeave contracts, region and commitment can change theirs. Supply your negotiated rates before making a purchasing decision. No network requests, cloud credentials, paid provisioning or third-party Python packages are used.

## 2. Price and hardware comparison

| Price or technical input | RunPod | Lambda Labs | CoreWeave | Interpretation |
|---|---:|---:|---:|---|
| H100 SXM reference, USD/GPU-hour | $2.69 | $3.29 | $6.16 | Historical public-price planning anchors; confirm SKU and terms |
| Eight H100s, USD/hour | $21.52 | $26.32 | $49.28 | Eight times the reference GPU-hour rate |
| Eight H100s, 720 h/month, compute | $15,494.40 | $18,950.40 | $35,481.60 | No storage, networking, tax or discount |
| Eight H100s, 12 modeled months, compute | $185,932.80 | $227,404.80 | $425,779.20 | 8,640 hours, not a calendar-year forecast |
| H100 SXM memory per GPU | 80 GB HBM3 | 80 GB HBM3 | 80 GB HBM3 | Validate the allocated SKU; PCIe H100 is a different comparison |
| H100 SXM GPU-to-GPU fabric capability | NVLink | NVLink | NVLink | Actual node wiring and multi-node networking require verification |
| RTX 4090 reference, USD/GPU-hour | $0.34 | N/A in model | N/A in model | RunPod community-market reference; capacity/security differ |
| RTX 4090 memory / NVLink | 24 GB / none | No priced SKU here | No priced SKU here | Consumer GPU; distributed scaling needs measurement |
| Persistent network storage reference | $0.07/GB-month first 1,000; $0.05 excess | Quote required | Quote required | Competitor storage must be obtained separately |
| Running / stopped pod-volume storage reference | $0.10 / $0.20 per GB-month | Quote required | Quote required | RunPod lifecycle alternatives, not extra mandatory charges |

For LoRA training, a lower hourly rate is only useful when the configuration fits and completes the same accepted workload. The table is a billing reference, not a FLUX or Wan2.1 performance benchmark.

The price provenance is the providers' public GPU pricing schedules and RunPod storage pricing conventions as historical planning references; no specific current tariff date was verified for this offline pack. Provider product names and billing scope evolve. A reference rate is not evidence of currently orderable capacity. Unsupported competitor SKUs are N/A, never zero. Tax, egress, support, IP addresses, orchestration charges, contracts and data-transfer labor are excluded unless represented by an explicit input. Obtain those costs in a written quote and add them to your procurement worksheet.

[Open RunPod to verify the rate, region and topology](https://is.gd/GvtNbV)

## 3. Run the TCO calculator

Requirements: Python 3.8 or later, standard library only. Run from this repository:

```bash
python3 calculate_runpod_h100_tco.py
python3 calculate_runpod_h100_tco.py --help
python3 calculate_runpod_h100_tco.py --tier h100 --json
```

`--hours` is total useful training wall hours across the month's experiment schedule; `--experiments` defaults to 12 and records the number of completed experiments for per-experiment budgeting. It does not multiply the hours. `--efficiency` defaults to 0.85, so billed hours equal useful hours divided by efficiency. Divide a JSON row's `monthly_usd` by `experiments` to obtain fully allocated experiment cost. With the default RunPod row this is $37.48 per experiment including persistent storage.

Example: `python3 calculate_runpod_h100_tco.py --tier rtx4090 --hours 180 --efficiency 0.75 --experiments 12 --json`. Use separately measured hours for each GPU tier. This model applies one efficiency to the compared H100s; collect provider-specific traces before claiming performance-adjusted savings. Keep batch size, training steps, resolution or frame count, seed policy and evaluation criteria fixed when timing a migration.

Every calculator accepts `--tier h100` or `--tier rtx4090`, `--gpus`, `--hours`, `--storage-gb`, `--runpod-rate`, `--rtx4090-rate`, `--lambda-rate`, `--coreweave-rate` and `--json`. Rates are USD per GPU-hour. Numeric inputs must be finite and nonnegative; GPU counts must be positive integers. Model-specific constraints fail with argparse exit code 2. A normal run exits 0. JSON contains inputs, reference rates, monthly component costs, comparable annual savings, caveats and the gateway URL, with unavailable numeric results represented as `null`.

Annual savings equal twelve times the monthly difference against the selected RunPod target row; negative savings mean the target costs more. Monthly bills are rounded to cents before annualization. A modeled year is twelve repeats of this month's workload, not a leap-year or full-calendar-hour simulation. Network storage assumes decimal GB and a full billing month; actual prorating and rate boundaries must be checked. The ASCII output below was captured by running the default command locally:

```text
FLUX and Wan2.1 LoRA fine-tuning GPU cost breakdown
USD planning baseline; no live quote or capacity guarantee.
Tier: h100 | GPUs: 1 | useful hours/month: 120.00
+-------------------------+------------+-------------+-------------+-------------+
| Scenario                | Hours/GPU  | Compute USD | Storage USD | Monthly USD |
+-------------------------+------------+-------------+-------------+-------------+
| RunPod                  |     141.18 |      379.76 |       70.00 |      449.76 |
| Lambda Labs             |     141.18 |      464.47 |       70.00 |      534.47 |
| CoreWeave               |     141.18 |      869.65 |       70.00 |      939.65 |
+-------------------------+------------+-------------+-------------+-------------+
Annual savings vs Lambda Labs: $1016.52
Annual savings vs CoreWeave: $5878.68
Note: Hours are total useful training wall hours per month, not per experiment.
Note: Efficiency includes loading, validation, restart and other non-training overhead.
Note: Cost per experiment is monthly_usd / experiments; no measured tokens/second or quality equivalence is claimed.
Note: FLUX and Wan2.1 memory fit depends on model variant, resolution, optimizer and quantization.
Launch / verify capacity: https://is.gd/GvtNbV
```

Repeatability check: run the default command twice and compare the totals. For a quote update, pass all applicable rate overrides on the command line; no source edit is necessary. Compare JSON monthly totals with `compute_usd + storage_usd`, allowing one cent for independent rounding. Use measured useful hours and complete checkpoint recovery costs before treating modeled savings as an achievable budget.

## 4. Migration checklist and related repositories

- [ ] Pin model variant, license, framework commit, precision, optimizer, sequence or frame length and resolution.
- [ ] Use one small dataset slice to validate memory headroom; do not add GPU VRAM totals as if they were contiguous memory.
- [ ] Measure data loading, compilation, step time, validation and checkpoint overhead separately.
- [ ] For FLUX or Wan2.1, validate the selected trainer supports your adapter target modules and offload strategy.
- [ ] Copy adapters plus training state and compare validation outputs under the same seed and sampler settings.
- [ ] Complete one full experiment on RunPod and compute cost per accepted result before moving the experiment queue.

Use the related worksheets for a different decision boundary:

- [Dedicated H100 SXM5 cluster pricing: CoreWeave vs Lambda Labs vs RunPod](../coreweave-lambda-vs-runpod-h100-cluster-pricing)
- [Idle GPU pod vs persistent network volume storage calculator](../idle-gpu-pod-vs-network-volume-storage-calculator)
- [Spot pod checkpoint recovery: expected H100 training cost](../automated-spot-pod-checkpoint-recovery-runner)

[Start with a small RunPod validation run](https://is.gd/GvtNbV)

The calculator is MIT-licensed; its executable source includes the permission and warranty notice. Documentation may also be reused under the same MIT terms. Vendor trademarks belong to their owners. This pack is an independent comparison; the gateway is a promotional referral route. Verify its destination and your checkout price before purchasing. No benchmark result, affiliation, production availability or discount is implied by this worksheet.
