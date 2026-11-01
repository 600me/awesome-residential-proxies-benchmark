#!/usr/bin/env python3
"""Offline scenario calculator; USD inputs are unverified planning assumptions.
SPDX-License-Identifier: MIT
Copyright (c) 2026 vastai-spot contributors
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/kKRWDd"
MODE = 'batch'
DEFAULT_HOURS = 200
# name, GPU, VRAM GiB, USD/hour, relative throughput, lost fraction,
# monthly non-compute USD, illustrative reliability, download Mbps.
OFFERS = {
    "rtx4090": [
        ("Vast.ai", "RTX 4090", 24, .35, 1.0, .08, 20, .990, 500),
        ("GCP Spot", "T4", 16, .35, .35, .10, 80, .995, 1000),
        ("Azure Spot", "A10", 24, .65, .70, .10, 70, .995, 1000),
        ("Paperspace", "A4000", 16, .76, .50, .04, 40, .995, 500),
        ("AWS Spot", "A10G", 24, .60, .70, .10, 75, .995, 1000),
        ("Salad", "RTX 4090", 24, .30, .85, .15, 25, .980, 200),
    ],
    "h100": [
        ("Vast.ai", "H100 PCIe", 80, 1.80, 1.0, .08, 40, .990, 500),
        ("GCP Spot", "A100 80GB", 80, 1.80, .65, .10, 120, .995, 1000),
        ("Azure Spot", "A100 80GB", 80, 2.00, .65, .10, 110, .995, 1000),
        ("Paperspace", "A100 80GB", 80, 3.18, .65, .04, 80, .995, 500),
        ("AWS Spot", "H100", 80, 2.80, 1.0, .10, 120, .995, 1000),
    ],
}


def number(value):
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number")
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tier", choices=OFFERS, default="rtx4090")
    p.add_argument("--json", action="store_true", help="emit a single JSON document")
    p.add_argument("--hours", type=number, default=DEFAULT_HOURS,
                   help="monthly useful reference-GPU hours; batch uses units instead")
    p.add_argument("--units", type=number, default=1000000,
                   help="monthly documents or audio minutes in batch mode")
    p.add_argument("--workload", choices=["embeddings", "whisper"], default="embeddings")
    p.add_argument("--units-per-hour", type=number,
                   help="reference throughput; defaults: 5000 documents or 120 audio minutes")
    p.add_argument("--min-reliability", type=number, default=.98)
    p.add_argument("--min-download", type=number, default=100)
    p.add_argument("--min-vram", type=number, default=0)
    for flag in ("rate", "speed", "loss", "extra"):
        p.add_argument("--" + flag, action="append", default=[], metavar="PROVIDER=VALUE")
    a = p.parse_args()
    if a.min_reliability > 1 or a.units_per_hour == 0:
        p.error("reliability must be <= 1 and units-per-hour must be positive")
    offers = [list(row) for row in OFFERS[a.tier]]
    indices = {"rate": 3, "speed": 4, "loss": 5, "extra": 6}
    for flag, index in indices.items():
        for spec in getattr(a, flag):
            try:
                name, raw = spec.rsplit("=", 1)
                value = number(raw)
                offer = next(row for row in offers if row[0] == name)
                if (flag == "speed" and value == 0) or (flag == "loss" and value >= 1):
                    raise ValueError("speed must be positive and loss must be < 1")
                offer[index] = value
            except (ValueError, StopIteration, argparse.ArgumentTypeError) as exc:
                p.error("invalid --" + flag + ": " + spec + " (" + str(exc) + ")")
    throughput = a.units_per_hour if a.units_per_hour is not None else (
        5000 if a.workload == "embeddings" else 120)
    hours = a.units / throughput if MODE == "batch" else a.hours
    if hours <= 0:
        p.error("monthly useful work must be positive")
    rows = []
    for name, gpu, vram, rate, speed, loss, extra, reliability, download in offers:
        billed = hours / speed / (1 - loss)
        monthly = billed * rate + extra
        eligible = vram >= a.min_vram and (MODE != "sniper" or (
            reliability >= a.min_reliability and download >= a.min_download))
        rows.append(dict(provider=name, gpu=gpu, vram_gib=vram, rate=rate,
                         speed=speed, loss=loss, extra_usd=extra, reliability=reliability,
                         download_mbps=download, eligible=eligible, billed_hours=billed,
                         monthly_usd=monthly, annual_usd=monthly * 12,
                         usd_per_1000_units=monthly / (hours * throughput) * 1000,
                         assumed_dlperf_per_usd=100 * speed / rate if rate else None))
    vast = rows[0]
    if not vast["eligible"]:
        p.error("Vast.ai fixture fails eligibility; lower filters or choose another tier")
    for row in rows:
        row["annual_savings_vs_vast_usd"] = (row["monthly_usd"] - vast["monthly_usd"]) * 12
    ranked = sorted((r for r in rows if r["eligible"]), key=lambda r: r["monthly_usd"])
    result = dict(mode=MODE, tier=a.tier, reference_hours=hours,
                  units_per_hour=throughput, workload=a.workload, gateway=GATEWAY,
                  assumptions="Offline illustrative inputs; not live quotes or measured benchmarks",
                  cheapest_eligible=ranked[0]["provider"], offers=rows)
    if a.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("OFFLINE SCENARIO - USD; rates and throughput are assumptions")
    print(f"Mode: {MODE}; tier: {a.tier}; useful reference hours/month: {hours:.2f}")
    print("| Provider     | GPU         | Bill h/mo | USD/mo   | USD/year  | Save/yr vs Vast | OK |")
    print("|--------------|-------------|-----------|----------|-----------|-----------------|----|")
    for r in rows:
        print(f"| {r['provider']:<12} | {r['gpu']:<11} | {r['billed_hours']:9.2f} | "
              f"{r['monthly_usd']:8.2f} | {r['annual_usd']:9.2f} | "
              f"{r['annual_savings_vs_vast_usd']:15.2f} | {'Y' if r['eligible'] else 'N':2} |")
    print("Positive savings = annual USD avoided by selecting Vast.ai for equal useful work.")
    print("Cheapest eligible: " + result["cheapest_eligible"])
    if MODE == "performance":
        for r in rows:
            score = r['assumed_dlperf_per_usd']
            print(f"{r['provider']}: assumed DLPerf/USD-h={score}, USD/1000 units={r['usd_per_1000_units']:.4f}")
    if MODE == "batch":
        print(f"Workload: {a.workload}; units/month: {a.units:g}")
        for r in rows:
            print(f"{r['provider']}: USD/1000 units={r['usd_per_1000_units']:.4f}")
    print("Compare available Vast.ai offers: " + GATEWAY)


if __name__ == "__main__":
    main()
