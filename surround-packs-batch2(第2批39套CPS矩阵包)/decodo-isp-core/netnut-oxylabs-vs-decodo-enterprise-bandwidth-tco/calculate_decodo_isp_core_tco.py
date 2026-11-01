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
    p = parser("Compare committed bandwidth, retry traffic, and operator time.")
    p.add_argument("--gb", type=positive, help="useful delivered decimal GB per month")
    for name, rate, minimum, failure, hours in (
        ("decodo", 3, 0, .03, .5), ("oxylabs", 6, 1000, .05, 1.5),
        ("netnut", 5, 1500, .06, 2)):
        p.add_argument(f"--{name}-rate", type=nonnegative, default=rate)
        p.add_argument(f"--{name}-minimum", type=nonnegative, default=minimum)
        p.add_argument(f"--{name}-failure", type=probability, default=failure)
        p.add_argument(f"--{name}-hours", type=nonnegative, default=hours)
    p.add_argument("--hourly", type=nonnegative, default=60)
    args = p.parse_args()
    gb = args.gb if args.gb is not None else {"starter": 100, "growth": 500, "enterprise": 2000}[args.tier]
    rows = []
    for key, name in (("decodo", "Decodo (Smartproxy)"), ("oxylabs", "Oxylabs"), ("netnut", "NetNut Enterprise")):
        billed = gb / (1 - getattr(args, key + "_failure"))
        traffic = billed * getattr(args, key + "_rate")
        minimum = getattr(args, key + "_minimum")
        labor = getattr(args, key + "_hours") * args.hourly
        rows.append({"provider": name, "plan": name, "monthly_usd": max(traffic, minimum) + labor,
                     "billed_gb": billed, "traffic_usd": traffic, "minimum_usd": minimum,
                     "unused_commitment_usd": max(0, minimum - traffic), "labor_usd": labor})
    emit(args, rows, {"useful_gb": gb, "retry_model": "independent failures; unlimited geometric retries",
                     "tax_and_external_egress": "excluded; add separately if applicable"},
         "each competitor's modeled monthly commitment plus operator time")


if __name__ == "__main__":
    main()
