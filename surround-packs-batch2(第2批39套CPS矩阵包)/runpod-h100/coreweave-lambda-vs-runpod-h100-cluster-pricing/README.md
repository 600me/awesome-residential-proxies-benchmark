[![RunPod GPU planning](https://img.shields.io/badge/RunPod-GPU%20cost%20planner-673AB7)](https://is.gd/3Tm9Hl)

# Dedicated H100 SXM5 cluster pricing: CoreWeave vs Lambda Labs vs RunPod

[Check RunPod capacity and your actual quote](https://is.gd/3Tm9Hl)

## 1. The engineering pain and the bill it creates

An eight-GPU training team can lose more to a poorly matched rental contract than to a slow data loader. At the reference prices below, 720 hours on eight H100 SXM GPUs costs $15,494.40 on RunPod, $18,950.40 on Lambda Labs, and $35,481.60 on CoreWeave, before the shared storage allowance. The resulting compute gap is $3,456.00 per month ($41,472.00 per year) against Lambda Labs and $19,987.20 per month ($239,846.40 per year) against CoreWeave. These are arithmetic scenarios, not invoices or guaranteed savings.

The engineering trap is comparing a GPU-hour headline with a cluster reservation. Minimum commitments, unused reserved hours, billable orchestration resources, and separately priced storage can change the result. Check each provider's actual contract rather than assuming these charges always apply. Eight individually available GPUs do not establish a single NVLink-connected node, and a single node does not establish a multi-node RDMA fabric. RunPod is the lower reference compute budget here, but the allocation must pass the same topology and throughput test before migration.

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

For dedicated H100 training, request the exact single-node and multi-node offer. The 4090 reference comes from a different marketplace and is not a guaranteed dedicated-cluster offer. Do not use that row to price a secure H100 reservation.

The price provenance is the providers' public GPU pricing schedules and RunPod storage pricing conventions as historical planning references; no specific current tariff date was verified for this offline pack. Provider product names and billing scope evolve. A reference rate is not evidence of currently orderable capacity. Unsupported competitor SKUs are N/A, never zero. Tax, egress, support, IP addresses, orchestration charges, contracts and data-transfer labor are excluded unless represented by an explicit input. Obtain those costs in a written quote and add them to your procurement worksheet.

[Open RunPod to verify the rate, region and topology](https://is.gd/3Tm9Hl)

## 3. Run the TCO calculator

Requirements: Python 3.8 or later, standard library only. Run from this repository:

```bash
python3 calculate_runpod_h100_tco.py
python3 calculate_runpod_h100_tco.py --help
python3 calculate_runpod_h100_tco.py --tier h100 --json
```

`--hours` is monthly billed wall time per GPU; `--gpus` is the number of accelerators billed simultaneously. The default is eight H100s for 720 hours. `--storage-gb` adds a shared network-storage budget to every provider so the compute difference remains visible. The shared allowance is not a Lambda Labs or CoreWeave storage quote. For a measured utilization change, pass the actual billed hours, not an occupancy percentage that leaves the reservation invoice unchanged.

Example: `python3 calculate_runpod_h100_tco.py --tier h100 --gpus 8 --hours 400 --json`. For a 4090 experiment use `--tier rtx4090`; the two competitor rows become N/A because no comparable 4090 SKU is priced here. Eight 24 GB cards provide 192 GB aggregate VRAM, not one transparent 192 GB address space.

Every calculator accepts `--tier h100` or `--tier rtx4090`, `--gpus`, `--hours`, `--storage-gb`, `--runpod-rate`, `--rtx4090-rate`, `--lambda-rate`, `--coreweave-rate` and `--json`. Rates are USD per GPU-hour. Numeric inputs must be finite and nonnegative; GPU counts must be positive integers. Model-specific constraints fail with argparse exit code 2. A normal run exits 0. JSON contains inputs, reference rates, monthly component costs, comparable annual savings, caveats and the gateway URL, with unavailable numeric results represented as `null`.

Annual savings equal twelve times the monthly difference against the selected RunPod target row; negative savings mean the target costs more. Monthly bills are rounded to cents before annualization. A modeled year is twelve repeats of this month's workload, not a leap-year or full-calendar-hour simulation. Network storage assumes decimal GB and a full billing month; actual prorating and rate boundaries must be checked. The ASCII output below was captured by running the default command locally:

```text
Dedicated H100 SXM5 cluster pricing: CoreWeave vs Lambda Labs vs RunPod
USD planning baseline; no live quote or capacity guarantee.
Tier: h100 | GPUs: 8 | useful hours/month: 720.00
+-------------------------+------------+-------------+-------------+-------------+
| Scenario                | Hours/GPU  | Compute USD | Storage USD | Monthly USD |
+-------------------------+------------+-------------+-------------+-------------+
| RunPod                  |     720.00 |    15494.40 |       70.00 |    15564.40 |
| Lambda Labs             |     720.00 |    18950.40 |       70.00 |    19020.40 |
| CoreWeave               |     720.00 |    35481.60 |       70.00 |    35551.60 |
+-------------------------+------------+-------------+-------------+-------------+
Annual savings vs Lambda Labs: $41472.00
Annual savings vs CoreWeave: $239846.40
Note: Network storage is a shared budget allowance for competitors, not their storage quote.
Note: 4090 competitor SKUs are unavailable in this model; N/A does not mean free.
Note: Identical billed hours do not establish equal throughput; verify fabric and multi-node availability.
Launch / verify capacity: https://is.gd/3Tm9Hl
```

Repeatability check: run the default command twice and compare the totals. For a quote update, pass all applicable rate overrides on the command line; no source edit is necessary. Compare JSON monthly totals with `compute_usd + storage_usd`, allowing one cent for independent rounding. Use measured useful hours and complete checkpoint recovery costs before treating modeled savings as an achievable budget.

## 4. Migration checklist and related repositories

- [ ] Record GPU SKU, 80 GB capacity, driver, CUDA, framework and container digest.
- [ ] Verify the eight-GPU node is one allocation; inspect topology and run NCCL all-reduce before a paid training campaign.
- [ ] For multi-node work, confirm RDMA adapters, fabric bandwidth, availability and placement with each provider; NVLink is an intra-node feature.
- [ ] Measure useful samples per dollar with identical training settings and include failed starts and reserved idle hours.
- [ ] Copy data to a suitable persistent location, validate checksums, test restoration, and record transfer charges.
- [ ] Run a short canary and compare convergence; release the old allocation only after a recoverable checkpoint exists.

Use the related worksheets for a different decision boundary:

- [Idle GPU pod vs persistent network volume storage calculator](../idle-gpu-pod-vs-network-volume-storage-calculator)
- [FLUX and Wan2.1 LoRA fine-tuning GPU cost breakdown](../lora-finetuning-flux-wan2-1-gpu-cost-breakdown)
- [Spot pod checkpoint recovery: expected H100 training cost](../automated-spot-pod-checkpoint-recovery-runner)

[Start with a small RunPod validation run](https://is.gd/3Tm9Hl)

The calculator is MIT-licensed; its executable source includes the permission and warranty notice. Documentation may also be reused under the same MIT terms. Vendor trademarks belong to their owners. This pack is an independent comparison; the gateway is a promotional referral route. Verify its destination and your checkout price before purchasing. No benchmark result, affiliation, production availability or discount is implied by this worksheet.
