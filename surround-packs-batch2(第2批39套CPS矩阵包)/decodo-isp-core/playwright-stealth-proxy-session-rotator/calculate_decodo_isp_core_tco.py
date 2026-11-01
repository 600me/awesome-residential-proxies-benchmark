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
    p = parser("Offline session rotation accounting; no Playwright dependency or network activity.")
    p.add_argument("--sessions", type=positive, help="successful sessions per month")
    p.add_argument("--requests-per-session", type=positive, default=8)
    p.add_argument("--kb", type=positive, default=128, help="KiB transferred per request attempt")
    p.add_argument("--failure", type=probability, default=.1, help="independent request failure probability")
    p.add_argument("--rotate-every", type=int, default=20, help="successful sessions per proxy lease")
    p.add_argument("--endpoints", type=int, default=10)
    p.add_argument("--switch-ms", type=nonnegative, default=50)
    p.add_argument("--request-seconds", type=positive, default=1.2)
    p.add_argument("--worker-hourly", type=nonnegative, default=.04)
    for name, rate, minimum in (("decodo", 3, 0), ("oxylabs", 6, 1000), ("netnut", 5, 1500)):
        p.add_argument(f"--{name}-rate", type=nonnegative, default=rate)
        p.add_argument(f"--{name}-minimum", type=nonnegative, default=minimum)
    args = p.parse_args()
    if args.rotate_every < 1 or args.endpoints < 1:
        p.error("--rotate-every and --endpoints must be positive integers")
    sessions = args.sessions if args.sessions is not None else {"starter": 5000, "growth": 50000, "enterprise": 500000}[args.tier]
    attempts = sessions * args.requests_per_session / (1 - args.failure)
    gb = attempts * args.kb * 1024 / 1e9
    leases = math.ceil(sessions / args.rotate_every)
    switches = max(0, leases - 1)
    worker_hours = (attempts * args.request_seconds + switches * args.switch_ms / 1000) / 3600
    rows = []
    for key, name in (("decodo", "Decodo (Smartproxy)"), ("oxylabs", "Oxylabs"), ("netnut", "NetNut Enterprise")):
        bandwidth = gb * getattr(args, key + "_rate")
        minimum = getattr(args, key + "_minimum")
        rows.append({"provider": name, "plan": name, "monthly_usd": max(bandwidth, minimum) + worker_hours * args.worker_hourly,
                     "bandwidth_usd": bandwidth, "minimum_usd": minimum, "worker_hours": worker_hours})
    emit(args, rows, {"successful_sessions": sessions, "expected_request_attempts": round(attempts, 4),
                     "billed_gb": round(gb, 6), "leases": leases, "switches": switches,
                     "endpoint_lease_imbalance_max": 1 if leases % args.endpoints else 0,
                     "assignment": "lease_index modulo endpoint_count; counters only, no actual requests",
                     "model_limit": "request retries only; whole-session replay is excluded"},
         "equal browser workload and failure probability for every provider")


if __name__ == "__main__":
    main()
