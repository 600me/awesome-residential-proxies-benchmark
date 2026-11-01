#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline bandwidth TCO model. Historical baselines, not current quotes."""
import argparse
import json
import math

GATEWAY = "https://norb.date/ps/1"
TIERS = {"light": 5, "standard": 50, "heavy": 200}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0 or number > 1e12:
        raise argparse.ArgumentTypeError("use a finite number from 0 through 1e12")
    return number


def main():
    parser = argparse.ArgumentParser(description='A reproducible cost model and benchmark protocol for lightweight, authorized search-result collection.')
    parser.add_argument("--tier", choices=TIERS, default="standard")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    parser.add_argument("--gb", type=nonnegative, help="base monthly decimal GB")
    parser.add_argument("--requests", type=nonnegative, help="intended monthly requests")
    parser.add_argument("--response-kib", type=nonnegative, default=100)
    parser.add_argument("--retry-rate", type=nonnegative, default=0,
                        help="extra attempts per intended request; 0.2 adds 20%%")
    parser.add_argument("--tunnel-overhead-pct", type=nonnegative, default=0)
    parser.add_argument("--smart-rate", type=nonnegative, default=10)
    parser.add_argument("--smart-min", type=nonnegative, default=80)
    parser.add_argument("--soax-rate", type=nonnegative, default=6.6)
    parser.add_argument("--soax-min", type=nonnegative, default=99)
    parser.add_argument("--migration-cost", type=nonnegative, default=0)
    args = parser.parse_args()
    if args.requests is not None and args.gb is not None:
        parser.error("choose either --gb or --requests")
    base = args.gb if args.gb is not None else TIERS[args.tier]
    if args.requests is not None:
        base = args.requests * args.response_kib * 1024 / 1_000_000_000
    gb = base * (1 + args.retry_rate) * (1 + args.tunnel_overhead_pct / 100)
    providers = [("PacketStream", 1, 0),
                 ("Smartproxy legacy", args.smart_rate, args.smart_min),
                 ("SOAX legacy", args.soax_rate, args.soax_min)]
    rows = []
    packet_month = round(gb, 2)
    for name, rate, floor in providers:
        monthly = round(max(floor, gb * rate), 2)
        annual = round(monthly * 12, 2)
        saving = round((monthly - packet_month) * 12, 2)
        rows.append({"provider": name, "usd_per_gb": rate, "monthly_floor_usd": floor,
                     "monthly_usd": monthly, "annual_usd": annual,
                     "annual_saving_with_packetstream_usd": saving,
                     "first_year_net_saving_usd": round(saving - args.migration_cost, 2)
                     if name != "PacketStream" else 0})
    result = {"model": "offline legacy unit-equivalent scenario; not a current quote",
              "tier": args.tier, "base_gb": round(base, 6), "billable_gb": round(gb, 6),
              "retry_rate": args.retry_rate, "tunnel_overhead_pct": args.tunnel_overhead_pct,
              "migration_cost_usd": args.migration_cost, "rows": rows,
              "packetstream_deposit_benchmark_usd": 50,
              "gateway": GATEWAY}
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    print("Offline legacy benchmarks | unit-equivalent planning, not current quotes")
    print(f"Tier: {args.tier} | Base GB: {base:.2f} | Billable GB: {gb:.2f}")
    rule = "+---------------------+------------+------------+----------------+"
    print(rule)
    print("| Provider            | Monthly $  | Annual $   | Year saving $  |")
    print(rule)
    for row in rows:
        print(f"| {row['provider']:<19} | {row['monthly_usd']:>10.2f} | "
              f"{row['annual_usd']:>10.2f} | "
              f"{row['annual_saving_with_packetstream_usd']:>14.2f} |")
    print(rule)
    for row in rows[1:]:
        print(f"Annualized savings vs {row['provider']}: "
              f"${row['annual_saving_with_packetstream_usd']:,.2f}; "
              f"first-year net: ${row['first_year_net_saving_usd']:,.2f}")
    print("PacketStream: $1/GB consumption; $50 deposit benchmark is prepaid credit.")
    print("Excludes tax, credit expiry, operator labor, and protocol adapter costs.")
    print(f"Gateway: {GATEWAY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
