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
    p = parser("Calculate prepaid tier utilization, overage, and PAYG break-even.")
    p.add_argument("--gb", type=nonnegative, help="total billed decimal GB per month")
    p.add_argument("--payg-rate", type=positive, default=8.5)
    p.add_argument("--monthly-rate", type=nonnegative)
    p.add_argument("--included-gb", type=positive)
    p.add_argument("--overage-rate", type=nonnegative, default=4)
    p.add_argument("--oxylabs-rate", type=nonnegative, default=8)
    p.add_argument("--netnut-rate", type=nonnegative, default=15)
    p.add_argument("--netnut-minimum", type=nonnegative, default=300)
    args = p.parse_args()
    included, rate, typical = {"starter": (20, 5, 15), "growth": (200, 3, 120),
                               "enterprise": (1000, 2, 800)}[args.tier]
    included = args.included_gb if args.included_gb is not None else included
    rate = args.monthly_rate if args.monthly_rate is not None else rate
    gb = args.gb if args.gb is not None else typical
    commitment = included * rate
    monthly = commitment + max(0, gb - included) * args.overage_rate
    payg = gb * args.payg_rate
    rows = [{"provider": "Decodo (Smartproxy)", "plan": "Decodo PAYG", "monthly_usd": payg},
            {"provider": "Decodo (Smartproxy)", "plan": "Decodo monthly", "monthly_usd": monthly},
            {"provider": "Oxylabs", "plan": "Oxylabs PAYG benchmark", "monthly_usd": gb * args.oxylabs_rate},
            {"provider": "NetNut Enterprise", "plan": "NetNut legacy starter benchmark",
             "monthly_usd": max(args.netnut_minimum, gb * args.netnut_rate)}]
    threshold = commitment / args.payg_rate
    details = {"billed_gb": gb, "included_gb": included, "monthly_commitment_usd": commitment,
               "unused_gb_no_rollover": max(0, included - gb),
               "annual_monthly_plan_savings_vs_payg_usd": round((payg - monthly) * 12, 2),
               "break_even_within_allowance_gb": round(threshold, 4) if threshold <= included else None,
               "above_allowance_rule": "compare commitment + (GB - included) * overage against GB * PAYG"}
    emit(args, rows, details, "competitor benchmarks at the same billed GB; no success-rate adjustment")


if __name__ == "__main__":
    main()
