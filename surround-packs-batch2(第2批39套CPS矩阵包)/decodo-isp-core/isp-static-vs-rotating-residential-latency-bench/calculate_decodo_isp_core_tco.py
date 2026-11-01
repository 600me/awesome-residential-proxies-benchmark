#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline planning calculator. Rates are assumptions, not current vendor quotes."""
import argparse
import json
import math

GATEWAY = "https://go.272738.xyz/smartproxy"


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number")
    return number


def positive(value):
    number = nonnegative(value)
    if number == 0:
        raise argparse.ArgumentTypeError("expected a positive number")
    return number


def probability(value):
    number = nonnegative(value)
    if number >= 1:
        raise argparse.ArgumentTypeError("expected a probability in [0, 1)")
    return number


def emit(args, rows, details, baseline):
    best = min(rows, key=lambda row: row["monthly_usd"])
    decodo = min((r for r in rows if r["provider"] == "Decodo (Smartproxy)"),
                 key=lambda row: row["monthly_usd"])
    competitors = [r for r in rows if r["provider"] != "Decodo (Smartproxy)"]
    savings = {r["plan"]: round((r["monthly_usd"] - decodo["monthly_usd"]) * 12, 2)
               for r in competitors}
    result = {"tier": args.tier, "currency": "USD", "price_status": "unverified planning assumptions",
              "rows": rows, "details": details, "annual_savings_vs_competitors_usd": savings,
              "baseline": baseline, "cheapest_modeled_plan": best["plan"], "gateway": GATEWAY}
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("OFFLINE TCO MODEL | USD | unverified planning assumptions")
    print("+------------------------------------+---------------+---------------+")
    print("| Plan                               | Monthly USD   | Annual USD    |")
    print("+------------------------------------+---------------+---------------+")
    for row in rows:
        print(f'| {row["plan"]:<34} | {row["monthly_usd"]:>13.2f} | {row["monthly_usd"]*12:>13.2f} |')
    print("+------------------------------------+---------------+---------------+")
    for key, value in details.items():
        print(f"{key}: {value}")
    print("Annual savings with lowest modeled Decodo option (negative = extra cost):")
    for name, amount in savings.items():
        print(f"  vs {name}: ${amount:,.2f}")
    print("Cheapest modeled plan: " + best["plan"])
    print("Explore Decodo: " + GATEWAY)


def parser(description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--tier", choices=("starter", "growth", "enterprise"), default="growth")
    p.add_argument("--json", action="store_true", help="emit a JSON object including the gateway")
    return p


def main():
    p = parser("Translate assumed or measured latency into monthly cost; no live benchmark.")
    p.add_argument("--jobs", type=positive, help="successful jobs per month")
    p.add_argument("--kb", type=positive, default=512, help="KiB transferred per attempt")
    p.add_argument("--ips", type=positive, default=10, help="allocated dedicated ISP IPs")
    p.add_argument("--static-seconds", type=positive, default=.9)
    p.add_argument("--rotating-seconds", type=positive, default=1.8)
    p.add_argument("--static-failure", type=probability, default=.04)
    p.add_argument("--rotating-failure", type=probability, default=.12)
    p.add_argument("--worker-hourly", type=nonnegative, default=.03)
    for vendor, static_rate, rotating_rate, ip_rate in (("decodo", 2, 3, 3), ("oxylabs", 3, 6, 5), ("netnut", 3.5, 5, 6)):
        p.add_argument(f"--{vendor}-static-rate", type=nonnegative, default=static_rate)
        p.add_argument(f"--{vendor}-rotating-rate", type=nonnegative, default=rotating_rate)
        p.add_argument(f"--{vendor}-ip-rate", type=nonnegative, default=ip_rate)
    args = p.parse_args()
    jobs = args.jobs if args.jobs is not None else {"starter": 10000, "growth": 100000, "enterprise": 1000000}[args.tier]
    rows = []
    for key, name, label in (("decodo", "Decodo (Smartproxy)", "Decodo"), ("oxylabs", "Oxylabs", "Oxylabs"), ("netnut", "NetNut Enterprise", "NetNut Enterprise")):
        for mode in ("static", "rotating"):
            attempts = jobs / (1 - getattr(args, mode + "_failure"))
            gb = attempts * args.kb * 1024 / 1e9
            worker_hours = attempts * getattr(args, mode + "_seconds") / 3600
            ip_bill = args.ips * getattr(args, key + "_ip_rate") if mode == "static" else 0
            cost = gb * getattr(args, key + "_" + mode + "_rate") + ip_bill + worker_hours * args.worker_hourly
            rows.append({"provider": name, "plan": label + " " + mode, "monthly_usd": cost,
                         "billed_gb": gb, "attempts": attempts, "worker_hours": worker_hours,
                         "dedicated_ip_usd": ip_bill})
    emit(args, rows, {"successful_jobs": jobs, "latency_status": "scenario inputs, not measured results",
                     "worker_model": "aggregate serial attempt time; no concurrency multiplier",
                     "billing_assumption": "metered bandwidth plus IP rental; replace with your quote"},
         "each competitor and mode at equal successful jobs; modeled scenarios only")


if __name__ == "__main__":
    main()
