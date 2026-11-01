#!/usr/bin/env python3
"""Offline planning calculator. USD reference rates are assumptions, not live quotes.
SPDX-License-Identifier: MIT
Copyright (c) 2026. Permission is granted, free of charge, to any person obtaining
this software to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies, provided this notice is retained. THE SOFTWARE IS PROVIDED "AS IS",
WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT SHALL THE AUTHORS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY ARISING FROM THE SOFTWARE.
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/o7iYHB"

def number(value):
    try:
        result = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not math.isfinite(result) or result < 0:
        raise argparse.ArgumentTypeError("expected a finite, nonnegative number")
    return result

def main():
    p = argparse.ArgumentParser(description='Spot pod checkpoint recovery: expected H100 training cost')
    p.add_argument("--tier", choices=("h100", "rtx4090"), default="h100")
    p.add_argument("--json", action="store_true", help="machine-readable result")
    p.add_argument("--gpus", type=int, default=8)
    p.add_argument("--hours", type=number, default=300, help="monthly useful wall hours")
    p.add_argument("--storage-gb", type=number, default=1000)
    p.add_argument("--runpod-rate", type=number, default=2.69, help="H100 USD/GPU-hour")
    p.add_argument("--rtx4090-rate", type=number, default=0.34, help="USD/GPU-hour")
    p.add_argument("--lambda-rate", type=number, default=3.29, help="H100 USD/GPU-hour")
    p.add_argument("--coreweave-rate", type=number, default=6.16, help="H100 USD/GPU-hour")
    p.add_argument("--spot-discount", type=number, default=0.30)
    p.add_argument("--checkpoint-minutes", type=number, default=20)
    p.add_argument("--save-minutes", type=number, default=1)
    p.add_argument("--mtbf-hours", type=number, default=12)
    p.add_argument("--resume-minutes", type=number, default=5)
    a = p.parse_args()
    if a.gpus < 1:
        p.error("--gpus must be at least 1")
    if a.spot_discount >= 1 or a.checkpoint_minutes <= 0 or a.mtbf_hours <= 0:
        p.error("require discount < 1 and positive checkpoint interval and MTBF")
    overhead = a.save_minutes / a.checkpoint_minutes + (a.checkpoint_minutes / 2 + a.resume_minutes) / (60 * a.mtbf_hours)
    if overhead >= 1:
        p.error("checkpoint and recovery overhead must be below 100%")
    rp_rate = a.runpod_rate if a.tier == "h100" else a.rtx4090_rate
    network = min(a.storage_gb, 1000) * 0.07 + max(a.storage_gb - 1000, 0) * 0.05
    rows = []
    def add(name, hours, rate, storage, comparable=True):
        compute = None if rate is None else hours * a.gpus * rate
        total = None if compute is None else compute + storage
        rows.append(dict(provider=name, billed_hours=round(hours, 4),
                         compute_usd=None if compute is None else round(compute, 2),
                         storage_usd=round(storage, 2),
                         monthly_usd=None if total is None else round(total, 2),
                         comparable=comparable))
    add("RunPod on-demand", a.hours, rp_rate, network)
    add("RunPod spot model", a.hours / (1 - overhead), rp_rate * (1 - a.spot_discount), network)
    for name, rate in (("Lambda Labs on-demand", a.lambda_rate), ("CoreWeave on-demand", a.coreweave_rate)):
        add(name, a.hours, rate if a.tier == "h100" else None, network)
    target = next(r for r in rows if r["provider"] == 'RunPod spot model')
    savings = {r["provider"]: round((r["monthly_usd"] - target["monthly_usd"]) * 12, 2)
               for r in rows if r is not target and r["comparable"] and r["monthly_usd"] is not None}
    result = dict(model='spot-checkpoint', tier=a.tier, assumptions=vars(a),
                  reference_rates_usd=dict(runpod_h100=a.runpod_rate,
                  runpod_rtx4090=a.rtx4090_rate, lambda_h100=a.lambda_rate,
                  coreweave_h100=a.coreweave_rate), rows=rows,
                  annual_savings_usd=savings, notes=['30% spot discount is a scenario input, not a published or guaranteed spot price.', 'MTBF applies to the entire job; one worker interruption restarts all ranks in this model.', 'Expected-value approximation excludes capacity queue time, correlated failures and failed saves.', 'Competitor rows use on-demand references; this does not imply that they lack spot offerings.', 'This offline calculator does not provision pods, run training or implement a recovery controller.'], gateway=GATEWAY)
    if a.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print('Spot pod checkpoint recovery: expected H100 training cost')
    print("USD planning baseline; no live quote or capacity guarantee.")
    print("Tier: %s | GPUs: %d | useful hours/month: %.2f" % (a.tier, a.gpus, a.hours))
    border = "+-------------------------+------------+-------------+-------------+-------------+"
    print(border)
    print("| Scenario                | Hours/GPU  | Compute USD | Storage USD | Monthly USD |")
    print(border)
    for r in rows:
        compute = "N/A" if r["compute_usd"] is None else "%.2f" % r["compute_usd"]
        total = "N/A" if r["monthly_usd"] is None else "%.2f" % r["monthly_usd"]
        print("| %-23s | %10.2f | %11s | %11.2f | %11s |" %
              (r["provider"], r["billed_hours"], compute, r["storage_usd"], total))
    print(border)
    for name, amount in savings.items():
        print("Annual savings vs %s: $%.2f" % (name, amount))
    if not savings:
        print("Annual savings: N/A; no comparable competitor SKU in this tier.")
    for note in result["notes"]:
        print("Note: " + note)
    print("Launch / verify capacity: " + GATEWAY)

if __name__ == "__main__":
    main()
