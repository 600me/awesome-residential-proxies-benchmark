[![RunPod GPU planning](https://img.shields.io/badge/RunPod-GPU%20cost%20planner-673AB7)](https://is.gd/h134js)

# Idle GPU pod vs persistent network volume storage calculator

[Check RunPod capacity and your actual quote](https://is.gd/h134js)

## 1. The engineering pain and the bill it creates

Leaving an H100 allocated while a researcher edits prompts turns an idle shell into an expensive storage device. With 80 active hours in a 720-hour month, the other 640 hours cost $1,721.60 on RunPod, $2,105.60 on Lambda Labs, or $3,942.40 on CoreWeave at the reference compute rates. That is $20,659.20, $25,267.20, or $47,308.80 per year in idle compute alone. A persistent filesystem and an allocated accelerator solve different problems.

The hidden-bill trap is assuming that stopping compute also removes every storage charge, or assuming that a cheaper disk can be mounted from any region. RunPod pod volumes and network volumes have different lifecycle and billing behavior. Lambda Labs and CoreWeave also have storage and shutdown choices: the competitor rows deliberately model keeping compute running and exclude their unknown storage prices. They are lower bounds for that scenario, not claims that either competitor forces customers to rent idle GPUs. Measure your actual idle hours and durable-volume terms before assigning savings.

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

For this storage decision, the competitor GPU rows represent an avoidable keep-running policy. They do not price a competitor network volume. Actual storage products, free allowances and stop semantics may reverse the storage-only comparison.

The price provenance is the providers' public GPU pricing schedules and RunPod storage pricing conventions as historical planning references; no specific current tariff date was verified for this offline pack. Provider product names and billing scope evolve. A reference rate is not evidence of currently orderable capacity. Unsupported competitor SKUs are N/A, never zero. Tax, egress, support, IP addresses, orchestration charges, contracts and data-transfer labor are excluded unless represented by an explicit input. Obtain those costs in a written quote and add them to your procurement worksheet.

[Open RunPod to verify the rate, region and topology](https://is.gd/h134js)

## 3. Run the TCO calculator

Requirements: Python 3.8 or later, standard library only. Run from this repository:

```bash
python3 calculate_runpod_h100_tco.py
python3 calculate_runpod_h100_tco.py --help
python3 calculate_runpod_h100_tco.py --tier h100 --json
```

`--hours` is active monthly wall time; `--month-hours` is the billing-window length, default 720. `--gpus` defaults to one, and `--storage-gb` defaults to 1,000 decimal GB. The keep-warm RunPod row pays GPU rent for the whole window plus running pod storage. The network row pays active GPU hours, a full month of network volume storage, and prorated active scratch. Both copies coexist while training, so the model does not hide duplicate storage.

Example: `python3 calculate_runpod_h100_tco.py --tier h100 --hours 40 --storage-gb 2000 --json`. Running pod disk is budgeted at $0.10/GB-month; a stopped retained pod volume has a separate $0.20/GB-month reference rate and is not the modeled keep-warm case. Full-month network storage uses $0.07/GB up to 1,000 GB and $0.05 for the excess. Confirm the actual billing boundary, disk type, region, transfer charges and scratch size; this simplified model uses one size for both copies.

Every calculator accepts `--tier h100` or `--tier rtx4090`, `--gpus`, `--hours`, `--storage-gb`, `--runpod-rate`, `--rtx4090-rate`, `--lambda-rate`, `--coreweave-rate` and `--json`. Rates are USD per GPU-hour. Numeric inputs must be finite and nonnegative; GPU counts must be positive integers. Model-specific constraints fail with argparse exit code 2. A normal run exits 0. JSON contains inputs, reference rates, monthly component costs, comparable annual savings, caveats and the gateway URL, with unavailable numeric results represented as `null`.

Annual savings equal twelve times the monthly difference against the selected RunPod target row; negative savings mean the target costs more. Monthly bills are rounded to cents before annualization. A modeled year is twelve repeats of this month's workload, not a leap-year or full-calendar-hour simulation. Network storage assumes decimal GB and a full billing month; actual prorating and rate boundaries must be checked. The ASCII output below was captured by running the default command locally:

```text
Idle GPU pod vs persistent network volume storage calculator
USD planning baseline; no live quote or capacity guarantee.
Tier: h100 | GPUs: 1 | useful hours/month: 80.00
+-------------------------+------------+-------------+-------------+-------------+
| Scenario                | Hours/GPU  | Compute USD | Storage USD | Monthly USD |
+-------------------------+------------+-------------+-------------+-------------+
| RunPod keep warm        |     720.00 |     1936.80 |      100.00 |     2036.80 |
| RunPod network          |      80.00 |      215.20 |       81.11 |      296.31 |
| Lambda Labs keep warm   |     720.00 |     2368.80 |        0.00 |     2368.80 |
| CoreWeave keep warm     |     720.00 |     4435.20 |        0.00 |     4435.20 |
+-------------------------+------------+-------------+-------------+-------------+
Annual savings vs RunPod keep warm: $20885.88
Annual savings vs Lambda Labs keep warm: $24869.88
Annual savings vs CoreWeave keep warm: $49666.68
Note: Competitor rows are keep-running compute-only lower bounds; their storage is excluded.
Note: Competitor shutdown and durable-volume options can also avoid idle compute; obtain actual terms.
Note: RunPod network persists all month; active pod scratch is prorated, with transfer and rebuild time excluded.
Launch / verify capacity: https://is.gd/h134js
```

Repeatability check: run the default command twice and compare the totals. For a quote update, pass all applicable rate overrides on the command line; no source edit is necessary. Compare JSON monthly totals with `compute_usd + storage_usd`, allowing one cent for independent rounding. Use measured useful hours and complete checkpoint recovery costs before treating modeled savings as an achievable budget.

## 4. Migration checklist and related repositories

- [ ] Measure real active hours and size durable model/data storage separately from disposable scratch.
- [ ] Choose a RunPod network-volume region with the required GPU capacity; validate mount visibility before moving data.
- [ ] Copy datasets, adapters and complete checkpoints, then verify checksums from a fresh pod.
- [ ] Persist optimizer state and metadata outside the disposable container filesystem; test termination and remount.
- [ ] Confirm deletion, retained-volume, minimum storage and transfer terms on every provider; stopping compute is not a deletion policy.
- [ ] Delete the old pod only after recovery succeeds, then verify the next invoice for orphaned disks and unused reservations.

Use the related worksheets for a different decision boundary:

- [Dedicated H100 SXM5 cluster pricing: CoreWeave vs Lambda Labs vs RunPod](../coreweave-lambda-vs-runpod-h100-cluster-pricing)
- [FLUX and Wan2.1 LoRA fine-tuning GPU cost breakdown](../lora-finetuning-flux-wan2-1-gpu-cost-breakdown)
- [Spot pod checkpoint recovery: expected H100 training cost](../automated-spot-pod-checkpoint-recovery-runner)

[Start with a small RunPod validation run](https://is.gd/h134js)

The calculator is MIT-licensed; its executable source includes the permission and warranty notice. Documentation may also be reused under the same MIT terms. Vendor trademarks belong to their owners. This pack is an independent comparison; the gateway is a promotional referral route. Verify its destination and your checkout price before purchasing. No benchmark result, affiliation, production availability or discount is implied by this worksheet.
