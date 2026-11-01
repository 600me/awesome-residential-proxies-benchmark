#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline single-GPU scenario calculator: AWS SageMaker vs RunPod: vLLM TCO Planning for 2026. No live price retrieval."""
import argparse
import json
import math

GATEWAY = "https://is.gd/aVhLD6"
# Historical public list-price reference inputs, not verified 2026 quotes.
# AWS rates are underlying EC2 p4de/p5 proxies, not SageMaker retail quotes.
RATES = {
    "a100": {"runpod": 0.000760, "modal": 0.000694, "aws_node": 40.96},
    "h100": {"runpod": 0.001160, "modal": 0.001097, "aws_node": 98.32},
}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be a finite nonnegative number")
    return number


def count(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be a nonnegative integer")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=RATES, default="a100")
    parser.add_argument("--json", action="store_true", help="emit one JSON document")
    parser.add_argument("--requests", type=count, default=50000)
    parser.add_argument("--seconds", type=nonnegative, default=8.0)
    parser.add_argument("--cold-fraction", type=nonnegative, default=0.1)
    parser.add_argument("--runpod-start", type=nonnegative, default=0.25)
    parser.add_argument("--modal-start", type=nonnegative, default=4.0)
    parser.add_argument("--hours", type=nonnegative, default=720.0)
    parser.add_argument("--tokens", type=count, default=256)
    args = parser.parse_args()
    if args.cold_fraction > 1:
        parser.error("--cold-fraction must be between 0 and 1")
    rates = RATES[args.tier]
    productive = args.requests * args.seconds
    cold_starts = args.requests * args.cold_fraction
    rp_seconds = productive + cold_starts * args.runpod_start
    modal_seconds = productive + cold_starts * args.modal_start
    aws_node = args.hours * rates["aws_node"]
    costs = {
        "RunPod Flex": rp_seconds * rates["runpod"],
        "Modal Labs GPU": modal_seconds * rates["modal"],
        "SageMaker 1/8 share*": aws_node / 8,
        "SageMaker full node": aws_node,
    }
    if not all(math.isfinite(v) for v in [productive, rp_seconds, modal_seconds, *costs.values()]):
        parser.error("workload overflows; reduce the input values")
    tokens = args.requests * args.tokens
    savings = {name: (cost - costs["RunPod Flex"]) * 12
               for name, cost in costs.items() if name != "RunPod Flex"}
    result = {
        "scenario": "aws-sagemaker-vs-runpod-serverless-vllm-tco-2026",
        "tier": args.tier,
        "inputs": {key: val for key, val in vars(args).items() if key != "json"},
        "reference_rates": rates,
        "productive_gpu_seconds": productive,
        "cold_starts_expected": cold_starts,
        "monthly_compute_usd": costs,
        "annual_savings_with_runpod_usd": savings,
        "output_tokens": tokens,
        "output_tokens_per_productive_gpu_second": tokens / productive if productive else None,
        "output_tokens_per_usd": {name: tokens / cost if cost else None
                                  for name, cost in costs.items()},
        "assumptions": [
            "Offline historical rates; not verified current offers or measured latency.",
            "AWS is an EC2 hardware-price proxy, not a SageMaker retail quote.",
            "AWS full node has 8 GPUs; 1/8 share is accounting only, not purchasable.",
            "Single-GPU work; identical runtime; one initialization per cold request.",
            "Paid startup, zero serverless idle; excludes CPU, RAM, storage, network, tax.",
            "250ms RunPod / 4s Modal are editable assumptions, not guarantees.",
            "Negative savings mean RunPod costs more; 12 identical 30-day months.",
        ],
        "gateway": GATEWAY,
    }
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("Offline GPU TCO | tier=" + args.tier + " | 30-day baseline")
    print("+-----------------------+---------------+------------------+")
    print("| Provider              | Monthly USD   | Output tokens/USD|")
    print("+-----------------------+---------------+------------------+")
    for name, cost in costs.items():
        efficiency = result["output_tokens_per_usd"][name]
        label = f"{efficiency:,.1f}" if efficiency is not None else "n/a"
        print(f"| {name:<21} | {cost:>13,.2f} | {label:>16} |")
    print("+-----------------------+---------------+------------------+")
    for name, amount in savings.items():
        print(f"Annual savings with RunPod vs {name}: ${amount:,.2f}")
    print("* 1/8 AWS node is accounting allocation, not a purchasable endpoint.")
    print(f"Startup assumptions: RunPod {args.runpod_start:g}s; Modal {args.modal_start:g}s (editable).")
    print("AWS uses underlying EC2 price proxies; SageMaker pricing may differ.")
    print("Offline rates; excludes CPU/RAM, storage, network and tax; see README.")
    print("Evaluate RunPod: " + GATEWAY)


if __name__ == "__main__":
    main()
