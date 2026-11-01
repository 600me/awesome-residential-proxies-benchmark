[![Evaluate RunPod](https://img.shields.io/badge/RunPod-Evaluate_GPU_costs-673ab7)](https://is.gd/Wowcpe)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-3776ab)](https://is.gd/Wowcpe)
[![MIT](https://img.shields.io/badge/License-MIT-green)](https://is.gd/Wowcpe)

# LLM Tokens per Dollar: RunPod, SageMaker and Modal Labs

## 1. Engineering pain and the dollars at risk

Cheap GPU seconds do not guarantee cheap successful tokens. Padding, retries, low batching efficiency, and long prompts consume compute without producing equally valuable output. AWS SageMaker idle capacity and Modal Labs billed resource initialization can reverse an apparent unit-rate advantage. Model delivered output against the whole compute bill.

This open-source repository compares **RunPod**, **AWS SageMaker**, and **Modal Labs** for FlashBoot Sub-250ms Serverless GPU Inference. It contains an inspectable offline budget model and an experiment recipe, not collected performance results. Prices are historical public list-price reference baselines from industry knowledge, supplied without online verification on 2026-10-30. They are not verified 2026 offers. Replace them with account-specific quotes before purchasing capacity. All amounts are USD.

For 100,000 monthly requests, 4 productive single-GPU seconds per request, and a 10% cold-request fraction, the default RunPod Flex estimate is **$305.90/month**. The selected AWS node's single-GPU accounting allocation at the EC2 proxy rate is **$3,686.40/month**. Its opportunity-cost difference is **$3,380.50/month**, or **$40,566.00/year**, relative to this RunPod scenario. The allocation is not separately purchasable: a dedicated eight-GPU A100 node at the underlying EC2 proxy rate costs **$29,491.20/month**. Both views appear in the output.

Modal's projected GPU bill is **$305.36/month**. Modal minus RunPod is **$-0.54/month**; a negative value favors Modal. The tool deliberately preserves that result. Hidden budget traps include retained warm capacity, initialization, persistent caches, data transfer, and supporting CPU/RAM. These are invoice items to investigate, not claims that a provider conceals its prices. The model excludes these extras except the explicitly assumed paid startup GPU time.

**[Evaluate RunPod with a small workload pilot](https://is.gd/Wowcpe)** and compare its invoice with the same model on your current provider. The gateway is a promotional referral destination; the calculation assumes no referral discount.

## 2. Price and technical parameter comparison

The table uses real SKU and product categories with historical list-price reference inputs. No rate card was fetched. Equal GPU names do not establish equal throughput, interconnect, availability, or end-to-end latency. The selected AWS nodes are not necessarily the cheapest viable AWS configuration.

| Parameter | RunPod Serverless Flex | AWS SageMaker real-time GPU | Modal Labs | Interpretation / units |
|---|---|---|---|---|
| A100 80 GB reference | $0.000760/GPU-second | EC2 p4de.24xlarge proxy: $40.96/node-hour | $0.000694/GPU-second | Historical baseline; verify your quote |
| A100 hourly equivalent | $2.736/GPU-hour | $5.120/GPU-hour allocated; $40.96/node-hour | $2.4984/GPU-hour | AWS allocation divides a node by eight |
| H100 80 GB reference | $0.001160/GPU-second | EC2 p5.48xlarge proxy: $98.32/node-hour | $0.001097/GPU-second | Select with --tier h100 |
| H100 hourly equivalent | $4.176/GPU-hour | $12.290/GPU-hour allocated; $98.32/node-hour | $3.9492/GPU-hour | No spot, reserved, or negotiated discount |
| Modeled resource shape | One GPU per worker | Eight GPUs per selected node | One GPU per container | More parallel workers mean more GPU-seconds |
| Scale-to-zero model | Flex worker lifecycle | Provisioned real-time endpoint | Container lifecycle | SageMaker Serverless Inference is CPU-only, not this GPU path |
| Startup input | 0.25 seconds, assumed | No per-request startup surcharge | 4 seconds, assumed | Editable inputs, not measurements or guarantees |
| Idle compute input | Zero retained idle GPU time | 720 provisioned node-hours | Zero retained idle GPU time | Add actual warm capacity separately |
| Other billable resources | Storage, transfer, warm workers as applicable | Storage, transfer, supporting services | CPU, RAM, storage, transfer as applicable | Excluded from these GPU-only totals |
| Model-weight readiness | Image and cache dependent | Image and cache dependent | Image and cache dependent | Process startup is not full LLM readiness |

Rate provenance: historical RunPod Flex GPU pricing, Modal GPU resource pricing, and historical US East Linux on-demand EC2 p4de/p5 hardware baselines used as explicit SageMaker cost proxies. **The AWS dollar rows are not SageMaker retail quotes.** SageMaker endpoint prices and service charges must replace these proxies for an actual endpoint budget. A node-hour proxy is not a guaranteed SageMaker price floor or purchasable SageMaker offer. Availability and pricing may have changed. These are continuous-seconds calculations: provider rounding, minimum charges, CPU/RAM allocation, warm-pool policy, and discounts require separate invoice checks. The model does not assert that every observed startup second is GPU-billable. RunPod can cost more than Modal on a warm workload because its listed GPU-second baseline here is higher.

**[Price a comparable RunPod deployment](https://is.gd/Wowcpe)** using the same GPU class, model precision, and successful-output target. A smaller quantized model against a larger full-precision model is not a platform comparison.

## 3. CLI usage and actual local output

Use Python 3 with the standard library. No credentials, packages, or network access are needed. Running without arguments prints an ASCII bill comparison, signed annual savings, and the gateway, then exits with code 0.

```bash
python3 calculate_runpod_serverless_tco.py
python3 calculate_runpod_serverless_tco.py --tier h100
python3 calculate_runpod_serverless_tco.py --tier a100 --json
python3 calculate_runpod_serverless_tco.py --cold-fraction 0 --runpod-start 0 --modal-start 0
```

| Argument | Default here | Meaning |
|---|---|---|
| --tier | a100 | a100 or h100; switches provider GPU baselines together |
| --json | off | One JSON document with inputs, rates, assumptions, costs, ratios, savings, gateway |
| --requests | 100000 | Completed requests per modeled month; nonnegative integer |
| --seconds | 4 | Productive GPU-seconds per request; account for overlapping batches |
| --cold-fraction | 0.1 | Fraction triggering initialization, from 0 to 1 |
| --runpod-start | 0.25 | Assumed paid RunPod startup GPU-seconds per cold request |
| --modal-start | 4 | Assumed paid Modal startup GPU-seconds per cold request |
| --hours | 720 | Provisioned AWS node-hours per modeled month |
| --tokens | 256 | Successfully delivered output tokens per request |
| --help | n/a | Describe all options |

Actual terminal output generated locally from this script:

```text
$ python3 calculate_runpod_serverless_tco.py
Offline GPU TCO | tier=a100 | 30-day baseline
+-----------------------+---------------+------------------+
| Provider              | Monthly USD   | Output tokens/USD|
+-----------------------+---------------+------------------+
| RunPod Flex           |        305.90 |         83,687.5 |
| Modal Labs GPU        |        305.36 |         83,835.5 |
| SageMaker 1/8 share*  |      3,686.40 |          6,944.4 |
| SageMaker full node   |     29,491.20 |            868.1 |
+-----------------------+---------------+------------------+
Annual savings with RunPod vs Modal Labs GPU: $-6.48
Annual savings with RunPod vs SageMaker 1/8 share*: $40,566.00
Annual savings with RunPod vs SageMaker full node: $350,223.60
* 1/8 AWS node is accounting allocation, not a purchasable endpoint.
Startup assumptions: RunPod 0.25s; Modal 4s (editable).
AWS uses underlying EC2 price proxies; SageMaker pricing may differ.
Offline rates; excludes CPU/RAM, storage, network and tax; see README.
Evaluate RunPod: https://is.gd/Wowcpe
```

The model is intentionally small enough to audit:

```text
productive_seconds = requests * seconds
cold_starts = requests * cold_fraction
RunPod_month = (productive_seconds + cold_starts * runpod_start) * RunPod_rate
Modal_month = (productive_seconds + cold_starts * modal_start) * Modal_rate
AWS_node_month = provisioned_hours * AWS_node_hourly_rate
AWS_allocated_GPU_month = AWS_node_month / 8
annual_savings = 12 * (competitor_month - RunPod_month)
output_tokens_per_dollar = requests * tokens / monthly_compute_cost
```

Positive savings favor RunPod; negative savings favor the named competitor. Annualization assumes twelve identical 30-day months, not 365 days. Serverless prices assume sufficient parallel worker capacity and identical productive runtime across providers. They do not prove a throughput or latency target. AWS node-hours must satisfy peak load, not merely average demand. Zero-cost token ratios print as `n/a` in text and `null` in JSON. Negative, non-finite, and out-of-range fraction inputs are rejected. For a new workload, replace the default startup inputs with measured paid GPU initialization time.

### Throughput measurement contract

The script projects output tokens as requests multiplied by `--tokens`. It divides that total by each modeled compute bill and reports output tokens per productive GPU-second in JSON. These are arithmetic projections, not measured vLLM performance. Input prefill work is represented only through the supplied execution time.

Hold prompt-length distribution, output budgets, numerical precision, and concurrency constant. Count all paid retries and failures in compute, but count only usable output tokens in delivered output. Reject configurations missing the same first-token and completion-latency SLO. A concurrency-64 throughput winner may be unsuitable for a concurrency-one interactive service.

Batched request durations overlap. Enter aggregate GPU-seconds divided by requests in `--seconds`, rather than summing overlapping wall-clock latency. For example, 10,000 aggregate GPU-seconds across 5,000 requests implies `--seconds 2`. The calculator assumes all requests complete; adjust the workload inputs from measured successful output and total billed time if failures matter.

## 4. Migration checklist and related repositories

- [ ] Capture a representative week of arrival patterns, prompt lengths, output lengths, failures, and billed resource lifetimes.
- [ ] Match tokenizer, model revision, precision, GPU memory, context limit, and tensor parallelism across providers.
- [ ] Replace historical prices in `RATES` with your actual quotes; record date, currency, SKU, region, and discounts in your fork.
- [ ] Measure cold and warm first-token latency, completion latency, p95/p99, and error rates; do not substitute the 250ms assumption for a measurement.
- [ ] Add CPU/RAM, retained workers, persistent cache, storage, transfer, retries, observability, and tax to the final budget.
- [ ] Check model licenses, gated-model access, secret handling, readiness probes, streaming, payload limits, and cancellation.
- [ ] Replay an identical workload, compare successful outputs and actual invoice line items, and keep a rollback endpoint during the pilot.
- [ ] Shift traffic gradually only after latency, error rate, and cost per successful request satisfy your acceptance criteria.

The other three repositories are independently runnable and linked relatively for a local checkout:

- [AWS SageMaker vs RunPod: vLLM TCO Planning for 2026](../aws-sagemaker-vs-runpod-serverless-vllm-tco-2026)
- [RunPod FlashBoot vs Modal Labs: Cold-Start Budget Bench](../modal-baseten-vs-runpod-flashboot-coldstart-bench)
- [vLLM Worker Recipe: DeepSeek and Llama on RunPod](../vllm-deepseek-llama3-runpod-worker-template)

**[Start a RunPod pilot with the same workload](https://is.gd/Wowcpe)**. Keep invoice evidence and latency samples with your final decision. This repository supplies a reproducible budget scenario, not a substitute for those observations.

### Contributing and license

For a price correction, include the exact SKU, units, region, pricing date, and whether the rate is quoted or invoiced. For a latency claim, include sample counts and the measurement protocol. Update the CLI example when changing defaults. Never submit credentials or customer prompts. The following MIT terms apply to both the documentation and calculator:

```text
MIT License

Copyright (c) 2026 repository contributors

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
