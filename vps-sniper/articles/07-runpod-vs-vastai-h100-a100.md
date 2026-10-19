On the sticker, Vast.ai rents H100 SXM capacity about **25%** below RunPod's Community Cloud ($2.01 against $2.69) and A100 80GB about **26%** below its Secure tier ($1.319 against $1.79). On the invoice, a two-hour model test is **63%** more expensive on Vast and a 7×24 production node flips to RunPod above **5.4 TB/month** of transfer — while a 72-hour preemptible fine-tune is still **52.8% cheaper** on Vast. Same two providers, three different winners.

*Affiliate disclosure (FTC): this article contains affiliate links for RunPod and Vast.ai. If you rent capacity through them, this site may earn a commission at no extra cost to you. That has no effect on the arithmetic, the ordering of the tables or which provider wins a scenario — the two links are worth the same, and one scenario below is deliberately won by each provider. Rates are a planning baseline captured from the providers' own APIs on 2026-10-18T16:37:25Z, not a quote; GPU markets move daily and host-set network rates vary per machine.*

## The two prices on every GPU page, and the third one that decides the bill

A pricing page shows one number per GPU: dollars per GPU-hour. Renting an H100 80GB looks like a comparison of $2.01 against $2.69, and the decision looks like arithmetic in one dimension. It is not, because the hourly rate is the only line item that both providers bill the same way.

The three charges that differ:

- **Wall-clock time that is not GPU time.** A pod that spends 40 minutes pulling a 150 GB set of weights and a 25 GB container image is still renting the GPU. If that pull happens on every fresh host — as it does on a peer-to-peer marketplace without a shared image cache — the overhead is billed at the full hourly rate and produces nothing.
- **Network transfer.** RunPod does not meter pod traffic. Vast.ai hosts set their own inbound and outbound rates, commonly quoted in the $0.01–$0.08 per GB band, and both directions can appear on the invoice. For a text LLM endpoint that is noise. For a workload that pulls 150 GB of weights per cold start, or serves a public demo, it is a real second line item.
- **Storage that survives the pod.** A stopped pod still owns its disk. Network volumes and container disks are billed per GB-month in both ecosystems, but on a marketplace the instance can also disappear when the host needs the machine back, which turns "storage cost" into "storage cost plus re-provisioning".

The metric that reconciles all three is **dollars per useful GPU-hour**: the total invoice for a workload divided by the GPU-hours that actually produced work. It is the only number comparable across the two providers, and it moves in opposite directions depending on the workload shape.

```text
effective $/useful GPU-hour =
    (gpu_hours_billed * hourly_rate
     + ingress_gb * in_rate
     + egress_gb * out_rate
     + storage_gb_month * storage_rate
     + reserve_for_interruption)
    / useful_gpu_hours
```

## Six dimensions, one table

| Dimension | RunPod | Vast.ai |
|---|---|---|
| **1. H100 80GB / A100 80GB hourly rate** | H100 SXM $2.69 Community / $3.99 Secure. H100 PCIe $1.99 / $2.89. A100 80GB SXM $1.39 / $1.79. A100 80GB PCIe $1.19 / $1.79. | H100 SXM $2.01 verified on-demand sample. H100 PCIe $2.002. A100 80GB SXM $1.319. A100 80GB PCIe $0.935. Interruptible bids clear far lower, around 55–60% of on-demand. |
| **2. Billing granularity & cold start** | Per-second billing. FlashBoot serves a cached container image in roughly a minute when the image is already on the host, so a restart is cheap. Stopping a pod frees the GPU but keeps the volume. | Per-second billing. No cross-host image cache: a new host pulls the container from the registry again, and any weights not on a persistent volume are re-downloaded. Restarts land on a different physical machine by design. |
| **3. Network bandwidth billing** | $0 for pod ingress and egress. A 150 GB weight download and an API serving 6 TB a month cost nothing extra. | Host-set, typically $0.01–$0.08/GB, and it applies to pulls as well as serving. 150 GB at $0.02/GB is $3.00 before the GPU does any work. |
| **4. Persistent storage** | Network volume around $0.10/GB-month. A 500 GB volume is $50/month whether the pod runs or is stopped, and it follows you between GPUs. | Host local disk billed per GB-month at the host's rate, commonly $0.10–$0.20. Cheaper for short jobs, riskier for long ones: if the host reclaims the instance, the data is gone. |
| **5. Preemption & physical reliability** | Secure Cloud runs in tier 3/4 datacenters with an uptime commitment; Community Cloud is shared inventory but still a single operator with a support path. | A peer-to-peer marketplace of independent hosts. Verified hosts are screened, unverified hosts are cheaper and less predictable. There is no SLA on a rented desktop, and a host can go offline mid-run. |
| **6. Best workload fit** | Anything that repeats: interactive notebooks, short tests, 24/7 inference, anything where a cold start is a tax you pay repeatedly. | Anything that is long, batch, checkpointed and preemptible: fine-tunes, distillation, synthetic data generation, offline evaluation sweeps. |

*Rates captured from the RunPod GraphQL catalog and the Vast.ai bundles API on 2026-10-18T16:37:25Z (HTTP 200 on both). Vast figures are the lowest verified rentable single-GPU offers sampled, before host network and storage charges. Interruptible pricing and storage rates are vendor and host list values, not a quote.*

## Scenario A — pull a 150 GB model and run a two-hour test

This is the workload that produces the most misleading price comparison in the ecosystem, because the sticker says Vast is 25% cheaper and the invoice says the opposite.

| Line item | Vast.ai H100 SXM @ $2.01 | RunPod H100 SXM @ $2.69 (Community) |
|---|---|---|
| GPU time, 2.0 hours | $4.02 | $5.38 |
| Weights: 150 GB ingress @ $0.02/GB | $3.00 | $0.00 |
| Container image: 25 GB pull @ $0.02/GB | $0.50 | $0.00 |
| Cold start billed at full rate | $1.34 (40 min) | $0.04 (60 s FlashBoot) |
| **Total for the test** | **$8.86** | **$5.42** |
| Effective $/useful GPU-hour | $4.43 | $2.71 |

Vast is cheaper on the only line most people compare — $4.02 against $5.38 of GPU time — and then loses $3.44 on transfer and cold start. The effective rate is **63% higher** ($4.43 against $2.71) for a job that took two hours. If your test takes twenty minutes instead of two hours, the distortion gets worse: the transfer, image pull and cold start are fixed costs that do not shrink with job length, so the same 20-minute test carries $4.84 of overhead against $0.67 of GPU time.

> **The rule this scenario produces:** if the job does not amortise a 150 GB transfer, the hourly rate is the wrong number to optimise. Rent the platform that already has the weights.

## Scenario B — a 7×24 vLLM inference node

Now the same two providers for 730 hours a month, one H100 SXM, 500 GB of persistent data, and a serving surface that moves 6 TB a month. This is where RunPod's zero-rated network starts paying for the higher hourly rate, and where a peer-to-peer marketplace needs an availability reserve that a datacenter contract does not.

| Line item, 730 hours | Vast.ai H100 SXM @ $2.01 | RunPod H100 SXM @ $2.69 (Community) |
|---|---|---|
| GPU time | $1,467.30 | $1,963.70 |
| Egress: 6,144 GB @ $0.05/GB | $307.20 | $0.00 |
| Persistent storage: 500 GB @ $0.10/GB-mo | $50.00 | $50.00 |
| Interruption / failover reserve (15% of GPU time) | $220.10 | $0.00 |
| **Monthly total** | **$2,044.60** | **$2,013.70** |
| Effective $/useful GPU-hour | $2.80 | $2.76 |

RunPod wins by **$30.90 a month** — a thin margin that exists only because of the reserve. Drop the 15% interruption reserve and Vast wins at $1,824.50 against $2,013.70. That is the honest version of this comparison: the two providers are within 2% of each other for a 24/7 node, and which one is cheaper depends on two inputs you control, not on the sticker.

The first input is transfer volume. Hold the other assumptions fixed and solve for the egress at which the two bills cross:

```text
crossover_gb = (runpod_total - vast_fixed_costs) / vast_egress_rate
             = ($2,013.70 - $1,737.40) / $0.05
             = 5,526 GB  (~5.4 TB per month)
```

Below about 5.4 TB a month, Vast's hourly discount survives the bandwidth bill. Above it, RunPod is cheaper — and the curve keeps diverging, because RunPod's marginal cost per extra terabyte is zero. A text-only vLLM endpoint moving a few hundred GB a month sits comfortably below the crossover and should probably stay on Vast if it can accept the availability risk. An endpoint that also distributes model artifacts, serves a public demo, streams large outputs, or hosts multimodal traffic crosses it quickly.

The second input is how much you are willing to pay for not being evicted. If a host disappears at 03:00 and your clients see 502s for forty minutes while you migrate a pod and re-pull weights, that event has a cost that no rate card contains. A 15% reserve is a crude way to price it. Teams with paying customers usually price it higher, and at that point RunPod Secure at $3.99 becomes the rational choice even though it is the most expensive hourly rate in this article.

## Scenario C — a 72-hour LoRA / distillation batch on three H100s

The mirror image. Long, checkpointed, tolerant of a restart, and utterly indifferent to a cold start that happens twice in three days. This is the workload peer-to-peer GPU markets were built for.

| Line item, 3 × H100 SXM × 72 h | Vast.ai interruptible @ $1.19 | RunPod H100 SXM @ $2.69 (Community) |
|---|---|---|
| GPU time, 216 GPU-hours | $257.04 | $581.04 |
| Weights: 450 GB ingress @ $0.02/GB | $9.00 | $0.00 |
| NVMe: 1.5 TB for 72 h, pro-rated | $15.15 | $15.15 |
| Checkpoint restarts: 2 evictions × 12 min | $0.48 | $0.00 |
| **Total for the run** | **$281.67** | **$596.19** |
| Effective $/useful GPU-hour | $1.30 | $2.76 |

Vast saves **$314.52 on a single three-day run**, and the saving is not a rounding error on the transfer bill: the transfer, storage and restart charges together add $24.63, which is 8.7% of Vast's total and still leaves it 52.8% cheaper. Two evictions costing twelve minutes each are priced in at $0.48, because a checkpointed batch job only loses the work since the last checkpoint.

> **One honest caveat.** RunPod also sells preemptible capacity, and at roughly $1.50/GPU-hour the gap narrows to about **$57.48** for this run. The wide margin in the table reflects the practical reality that three H100s of interruptible capacity are not always available on RunPod when you want to start, while a marketplace has thousands of independent sellers. If you can get RunPod spot immediately, the premium you are paying for a managed platform is small.

The A100 80GB version of the same job is cheaper again on both sides: at $1.319 on-demand and around $0.78 interruptible, 216 A100 GPU-hours for 72 hours cost **$168.48** of GPU time and about **$177** including weight transfer, and the gap to RunPod's $1.39 Community rate stays in the same proportion. For LoRA-scale fine-tuning of models that fit in 80 GB, A100 capacity is the value tier — H100 only pays when you need FP8 or the extra memory bandwidth.

## What none of these tables price

Three costs are real, recurring, and absent from every line item above.

- **Re-provisioning time.** A cold start on a new Vast host is 25–40 minutes for a large model. If your team does that four times a week, it is a working day per month spent watching a progress bar.
- **Data loss on eviction.** Local disk on a rented machine is not durable storage. Checkpoints belong on a volume, an object store or the host you control, and that replication has its own cost.
- **Prepaid credit and billing friction.** Marketplaces run on prepaid balances; a card decline mid-run stops a pod. Managed platforms invoice. Neither is wrong, but a finance team will price the difference at more than zero.

There is also a correctness risk that shows up as a performance mystery: a "verified" marketplace host can have a degraded interconnect, PCIe lanes shared with other tenants, or a thermal limit that quietly halves sustained throughput. The cure is measurement, not a rate card.

## Measure your own effective rate in ten minutes

Warm up, time a fixed workload, and divide dollars by useful work. The script below is the same shape used to fill the tables in this article.

```python
import time, subprocess, json

start = time.time()                 # pod clocks in at this moment
subprocess.run(["python", "-m", "pip", "install", "-q", "transformers"])
load_start = time.time()
# ... download weights and build the engine here ...
load_seconds = time.time() - load_start

work_start = time.time()
# ... run the fixed 200-prompt evaluation here ...
work_seconds = time.time() - work_start

print(json.dumps({
    "billed_seconds": round(time.time() - start, 1),
    "load_seconds": round(load_seconds, 1),
    "work_seconds": round(work_seconds, 1),
    "overhead_ratio": round((load_seconds) / max(work_seconds, 1e-9), 3),
}))
```

If `overhead_ratio` is above 0.2, you are renting cold-start time and should be on a platform with a cached image and free ingress. If it is below 0.05 and the job is checkpointed, you are the workload a marketplace is built for and the hourly discount is yours to keep.

## The three-line decision

1. **Short and interactive, or 24/7 serving:** RunPod. The hourly premium is smaller than the transfer, cold-start and failover costs it removes. The crossover for a serving node is about 5.4 TB/month of egress; below that the difference is under $31 a month either way.
2. **Long, checkpointed and preemptible:** Vast.ai. A 72-hour three-GPU batch run saves $314.52 against RunPod Community rates, or roughly $57 against RunPod spot if spot is available.
3. **Unsure:** price the transfer first. At $0.02/GB, 150 GB of weights is $3.00 per cold start. Multiply that by the number of cold starts you will actually have, and the answer usually appears before you finish the multiplication.

## Price your own workload

The calculator takes GPU model, hours, utilisation, egress and storage and returns the effective dollars per useful GPU-hour, so you can put your own numbers into the tables above.

- **[Open the GPU cost calculator →](https://gpu.mybskm.top/calculator/)**
- **[Run it on Hugging Face Spaces →](https://huggingface.co/spaces/600me/llm-gpu-cost-calculator)**
- **[Read the full teardown with every table and source note →](https://gpu.mybskm.top/blog/runpod-vs-vastai-h100-a100.html)**

## Rent the capacity, if the arithmetic says so

Both links below are affiliate links carrying the same tracking parameter, and both providers win a scenario in this article. Pick with the tables, not the discounts.

- **[Rent H100 on RunPod ↗](https://go.272738.xyz/runpod?src=devto_runpod_vast)**
- **[Rent H100 on Vast.ai ↗](https://go.272738.xyz/vastai?src=devto_runpod_vast)**

*Affiliate links: a commission may be paid at no extra cost to you. Rates change daily; verify the current price and the host's network terms before renting.*

## Method and sources

Hourly rates were pulled directly from each provider's catalog API on 2026-10-18T16:37:25Z, both returning HTTP 200: the RunPod GraphQL catalog for Community and Secure tiers, and the Vast.ai bundles endpoint for the lowest verified rentable single-GPU offers. Every dollar figure in the scenario tables is a multiplication of those rates by the stated quantities, plus the stated network, storage and reserve assumptions. Nothing is a vendor quote and nothing is a promotion.

Assumptions worth restating: Vast ingress and egress at $0.02/GB for weights and $0.05/GB for serving traffic, both inside the commonly quoted $0.01–$0.08 band; persistent storage at $0.10/GB-month for both providers; a 15% interruption reserve for the marketplace in a production scenario; interruptible Vast capacity at $1.19/GPU-hour, approximately 59% of the verified on-demand sample. Change any of them and the tables change; the method does not.

*Related research: [The H100 Rental Trap](https://gpu.mybskm.top/blog/h100-rental-trap.html), and the [live rate index](https://gpu.mybskm.top/) that feeds these tables.*
