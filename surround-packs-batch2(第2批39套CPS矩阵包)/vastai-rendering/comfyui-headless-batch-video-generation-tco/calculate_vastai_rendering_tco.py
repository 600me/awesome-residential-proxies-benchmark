#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline, assumption-based TCO model; no live quotes or measured benchmarks."""
import argparse
import json
import math

GATEWAY = "https://gpu.mybskm.top/go/vastai"
TIERS = {"small": 2, "studio": 8, "farm": 32}
BASIS = ("USD planning assumptions, not live vendor quotes. Render Network and "
         "OctaneCloud rates are workload-equivalent scenarios, not GPU rental tariffs. "
         "Taxes, token conversion, subscriptions and unsupported-workload porting excluded.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tier", choices=TIERS, default="studio", help="GPU preset: small=2, studio=8, farm=32")
    p.add_argument("--json", action="store_true", help="Emit one JSON object instead of ASCII")
    p.add_argument("--gpus", type=int, help="Override preset worker count")
    p.add_argument("--vast-rate", type=float, default=0.35, help="Assumed Vast USD/GPU-hour")
    p.add_argument("--render-rate", type=float, default=1.20, help="Render assumed USD/equivalent GPU-hour")
    p.add_argument("--octane-rate", type=float, default=1.50, help="OctaneCloud assumed USD/equivalent GPU-hour")
    p.add_argument("--storage-gb", type=float, default=200, help="Persistent GB-month, fleet total")
    p.add_argument("--storage-rate", type=float, default=0.07, help="Assumed USD/GB-month for each scenario")
    p.add_argument("--egress-gb", type=float, default=100, help="Monthly output GB, fleet total")
    p.add_argument("--egress-rate", type=float, default=0.02, help="Assumed USD/output GB for each scenario")
    p.add_argument("--ops-rate", type=float, default=40, help="Operator USD/hour")
    p.add_argument("--clips", type=int, default=20000, help="Accepted clips per month, fleet total")
    p.add_argument("--seconds-per-clip", type=float, default=240, help="Measured single-worker seconds per attempt")
    p.add_argument("--batch-efficiency", type=float, default=0.80, help="Useful GPU busy fraction, (0, 1]")
    p.add_argument("--qa-failure-rate", type=float, default=0.05, help="Independent rejected-attempt fraction, [0, 1)")
    p.add_argument("--startup-hours", type=float, default=2, help="Paid model-load/setup hours per GPU-month")
    p.add_argument("--labor-hours", type=float, default=3, help="Monthly fleet operator hours")
    a = p.parse_args()
    a.gpus = a.gpus if a.gpus is not None else TIERS[a.tier]
    for key, value in vars(a).items():
        if isinstance(value, (float, int)) and not isinstance(value, bool):
            if not math.isfinite(value) or value < 0:
                p.error(key + " must be finite and nonnegative")
    if a.gpus < 1:
        p.error("gpus must be positive")
    if not 0 < a.batch_efficiency <= 1 or not 0 <= a.qa_failure_rate < 1:
        p.error("efficiency must be in (0, 1] and failure rate in [0, 1)")
    storage = a.storage_gb * a.storage_rate
    transfer = a.egress_gb * a.egress_rate
    ops = a.labor_hours * a.ops_rate
    rows = []

    def bill(name, hours, rate, extra_transfer=0):
        compute = hours * rate
        rows.append(dict(provider=name, billed_gpu_hours=hours, compute_usd=compute,
                         storage_usd=storage, transfer_usd=transfer + extra_transfer,
                         operations_usd=ops,
                         monthly_usd=compute + storage + transfer + extra_transfer + ops))

    attempts = a.clips / (1 - a.qa_failure_rate)
    useful = attempts * a.seconds_per_clip / 3600
    paid = useful / a.batch_efficiency + a.gpus * a.startup_hours
    bill("Vast.ai ComfyUI", paid, a.vast_rate)
    bill("Render Network equiv.", paid, a.render_rate)
    bill("OctaneCloud equiv.", paid, a.octane_rate)
    metrics = dict(expected_attempts=attempts, paid_gpu_hours=paid,
                   ideal_elapsed_hours=paid / a.gpus,
                   vast_usd_per_accepted_clip=rows[0]["monthly_usd"] / a.clips if a.clips else 0)
    vast = min(row["monthly_usd"] for row in rows if row["provider"].startswith("Vast.ai"))
    savings = {row["provider"]: (row["monthly_usd"] - vast) * 12
               for row in rows if not row["provider"].startswith("Vast.ai")}
    result = dict(model="comfyui-headless-batch-video-generation-tco", currency="USD", price_basis=BASIS,
                  inputs=vars(a), metrics=metrics, rows=rows,
                  annual_savings_usd=savings, gateway=GATEWAY)
    numbers = [value for row in rows for value in row.values() if isinstance(value, (int, float))]
    numbers += list(metrics.values()) + list(savings.values())
    if not all(math.isfinite(value) for value in numbers):
        p.error("inputs overflow the model; use smaller values")
    if a.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("ComfyUI headless batch video TCO")
    print("Price basis: offline assumptions; competitor equivalents are not vendor quotes.")
    print("Tier: %s | GPUs: %d | all amounts USD/month" % (a.tier, a.gpus))
    rule = "+---------------------------+------------+----------+----------+----------+------------+"
    print(rule)
    print("| Scenario                  | Compute    | Storage  | Transfer | Ops      | Total      |")
    print(rule)
    for row in rows:
        print("| %-25s | %10.2f | %8.2f | %8.2f | %8.2f | %10.2f |" %
              (row["provider"], row["compute_usd"], row["storage_usd"],
               row["transfer_usd"], row["operations_usd"], row["monthly_usd"]))
    print(rule)
    for key, value in metrics.items():
        print("%s: %.4f" % (key, value))
    for name, value in savings.items():
        print("Annualized savings vs %s: $%s" % (name, format(value, ",.2f")))
    print("Annualization = 12 identical months; negative savings mean Vast costs more.")
    print(GATEWAY)


if __name__ == "__main__":
    main()
