[![RunPod GPU planning](https://img.shields.io/badge/RunPod-GPU%20cost%20planner-673AB7)](https://is.gd/o7iYHB)

# Spot pod checkpoint recovery: expected H100 training cost

[Check RunPod capacity and your actual quote](https://is.gd/o7iYHB)

## 1. The engineering pain and the bill it creates

A discounted GPU becomes expensive when an interrupted distributed run restarts from step zero. For an eight-H100 job needing 300 useful wall hours per month, losing 60 extra hours costs $1,291.20 at the RunPod reference on-demand rate, $1,579.20 at Lambda Labs, or $2,956.80 at CoreWeave. Repeating that failure pattern for a year wastes $15,494.40, $18,950.40, or $35,481.60 before storage. These are explicit loss scenarios, not measured interruption histories.

The trap is treating an advertised spot discount as a completed-training discount. Checkpoint writes, lost progress, restoring optimizer state, unavailable replacement capacity, and whole-job restarts all consume the margin. Lambda Labs and CoreWeave on-demand prices below are reference alternatives, not assertions about their spot products or interruption policies. RunPod spot pricing is also variable: the default 30% discount is an editable scenario assumption. This repository supplies the cost model and a recovery implementation checklist; its Python entry point is an offline calculator, not an operational pod recovery service.

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

For interruption planning, all table GPU prices are on-demand reference anchors. Apply the spot scenario discount only to the RunPod spot row; no published spot rate or SLA is asserted.

The price provenance is the providers' public GPU pricing schedules and RunPod storage pricing conventions as historical planning references; no specific current tariff date was verified for this offline pack. Provider product names and billing scope evolve. A reference rate is not evidence of currently orderable capacity. Unsupported competitor SKUs are N/A, never zero. Tax, egress, support, IP addresses, orchestration charges, contracts and data-transfer labor are excluded unless represented by an explicit input. Obtain those costs in a written quote and add them to your procurement worksheet.

[Open RunPod to verify the rate, region and topology](https://is.gd/o7iYHB)

## 3. Run the TCO calculator

Requirements: Python 3.8 or later, standard library only. Run from this repository:

```bash
python3 calculate_runpod_h100_tco.py
python3 calculate_runpod_h100_tco.py --help
python3 calculate_runpod_h100_tco.py --tier h100 --json
```

`--hours` is useful completed training wall time. `--spot-discount` is a fraction, with 0.30 meaning 30% below the supplied RunPod on-demand rate. `--checkpoint-minutes` is the scheduled wall-clock period, including the checkpoint pause; `--save-minutes` is that pause. `--mtbf-hours` describes interruption frequency for the entire distributed job, and `--resume-minutes` covers rehydrating and restoring a complete checkpoint. The default is eight H100s, 300 useful hours, a 20-minute interval, one-minute saves, a 12-hour job MTBF and five-minute restoration.

The first-order overhead fraction is `save / interval + (interval / 2 + resume) / (60 * MTBF)`. Expected billed time is `useful_hours / (1 - overhead)`. This approximation treats interruptions as uniformly distributed between checkpoints and ignores repeated failures during restore. It should not be used when outages are correlated, saves frequently fail, or the computed overhead approaches one. Annual savings against the RunPod on-demand row isolate the modeled interruption tradeoff; cross-provider savings also include price differences.

Example: `python3 calculate_runpod_h100_tco.py --tier h100 --spot-discount 0.15 --mtbf-hours 4 --checkpoint-minutes 10 --json`. Probe both discount and MTBF instead of selecting only a favorable case. Replacement capacity is not guaranteed by a checkpoint file.

Every calculator accepts `--tier h100` or `--tier rtx4090`, `--gpus`, `--hours`, `--storage-gb`, `--runpod-rate`, `--rtx4090-rate`, `--lambda-rate`, `--coreweave-rate` and `--json`. Rates are USD per GPU-hour. Numeric inputs must be finite and nonnegative; GPU counts must be positive integers. Model-specific constraints fail with argparse exit code 2. A normal run exits 0. JSON contains inputs, reference rates, monthly component costs, comparable annual savings, caveats and the gateway URL, with unavailable numeric results represented as `null`.

Annual savings equal twelve times the monthly difference against the selected RunPod target row; negative savings mean the target costs more. Monthly bills are rounded to cents before annualization. A modeled year is twelve repeats of this month's workload, not a leap-year or full-calendar-hour simulation. Network storage assumes decimal GB and a full billing month; actual prorating and rate boundaries must be checked. The ASCII output below was captured by running the default command locally:

```text
Spot pod checkpoint recovery: expected H100 training cost
USD planning baseline; no live quote or capacity guarantee.
Tier: h100 | GPUs: 8 | useful hours/month: 300.00
+-------------------------+------------+-------------+-------------+-------------+
| Scenario                | Hours/GPU  | Compute USD | Storage USD | Monthly USD |
+-------------------------+------------+-------------+-------------+-------------+
| RunPod on-demand        |     300.00 |     6456.00 |       70.00 |     6526.00 |
| RunPod spot model       |     322.87 |     4863.71 |       70.00 |     4933.71 |
| Lambda Labs on-demand   |     300.00 |     7896.00 |       70.00 |     7966.00 |
| CoreWeave on-demand     |     300.00 |    14784.00 |       70.00 |    14854.00 |
+-------------------------+------------+-------------+-------------+-------------+
Annual savings vs RunPod on-demand: $19107.48
Annual savings vs Lambda Labs on-demand: $36387.48
Annual savings vs CoreWeave on-demand: $119043.48
Note: 30% spot discount is a scenario input, not a published or guaranteed spot price.
Note: MTBF applies to the entire job; one worker interruption restarts all ranks in this model.
Note: Expected-value approximation excludes capacity queue time, correlated failures and failed saves.
Note: Competitor rows use on-demand references; this does not imply that they lack spot offerings.
Note: This offline calculator does not provision pods, run training or implement a recovery controller.
Launch / verify capacity: https://is.gd/o7iYHB
```

Repeatability check: run the default command twice and compare the totals. For a quote update, pass all applicable rate overrides on the command line; no source edit is necessary. Compare JSON monthly totals with `compute_usd + storage_usd`, allowing one cent for independent rounding. Use measured useful hours and complete checkpoint recovery costs before treating modeled savings as an achievable budget.

## 4. Migration checklist and related repositories

- [ ] Write model, optimizer, scheduler, gradient-scaler, RNG and data-sampler state to a staging checkpoint.
- [ ] Coordinate all ranks, flush durable writes, verify a manifest and checksum, then atomically publish a completed-checkpoint marker.
- [ ] Keep at least two completed generations on a durable network volume; never resume a partial staging directory.
- [ ] Have an external controller detect exit, request replacement capacity with bounded backoff, mount storage and select the newest valid checkpoint.
- [ ] Restore all ranks from the same committed step; ensure resume is idempotent and record completed work outside ephemeral pod storage.
- [ ] Inject a worker failure and validate convergence and data ordering; measure actual job MTBF, save duration and recovery delay.
- [ ] Set an explicit retry budget and spend ceiling, and test unavailable capacity. This calculator itself performs none of these controller actions.

Use the related worksheets for a different decision boundary:

- [Dedicated H100 SXM5 cluster pricing: CoreWeave vs Lambda Labs vs RunPod](../coreweave-lambda-vs-runpod-h100-cluster-pricing)
- [Idle GPU pod vs persistent network volume storage calculator](../idle-gpu-pod-vs-network-volume-storage-calculator)
- [FLUX and Wan2.1 LoRA fine-tuning GPU cost breakdown](../lora-finetuning-flux-wan2-1-gpu-cost-breakdown)

[Start with a small RunPod validation run](https://is.gd/o7iYHB)

The calculator is MIT-licensed; its executable source includes the permission and warranty notice. Documentation may also be reused under the same MIT terms. Vendor trademarks belong to their owners. This pack is an independent comparison; the gateway is a promotional referral route. Verify its destination and your checkout price before purchasing. No benchmark result, affiliation, production availability or discount is implied by this worksheet.
