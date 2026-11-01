#!/usr/bin/env python3
"""Offline proxy-cost scenario calculator; rates are assumptions, not vendor quotes.
SPDX-License-Identifier: MIT
Copyright (c) 2026 the repository contributors
"""
import argparse
import json
import math

GATEWAY = "https://norb.date/p/2"
MODE = 'replacement'
TIERS = {"small": (1000, 500), "standard": (5000, 2000), "scale": (20000, 8000)}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be a finite nonnegative number")
    return number


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def fraction(value):
    number = nonnegative(value)
    if number > 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="standard")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    parser.add_argument("--gb", type=nonnegative, help="useful decimal GB per month")
    parser.add_argument("--usable-ips", type=positive, help="usable endpoints needed per month")
    parser.add_argument("--survival", type=fraction, default=0.8)
    parser.add_argument("--retry-fraction", type=nonnegative, default=0.15)
    parser.add_argument("--replacement-eligible", type=fraction, default=0.8)
    parser.add_argument("--nine-ip-price", type=nonnegative, default=0.20)
    for vendor, rate in (("abc", 0.80), ("luna", 0.77)):
        parser.add_argument("--" + vendor + "-model", choices=("bandwidth", "ip"), default="bandwidth")
        parser.add_argument("--" + vendor + "-gb-price", type=nonnegative, default=rate)
        parser.add_argument("--" + vendor + "-ip-price", type=nonnegative, default=0.20)
        parser.add_argument("--" + vendor + "-replacement-eligible", type=fraction, default=0)
    if MODE == "ports":
        parser.add_argument("--ports", type=positive, default=4)
        parser.add_argument("--per-port", type=positive, default=8)
        parser.add_argument("--concurrency", type=positive, default=64)
        parser.add_argument("--base-port", type=positive, default=10000)
    args = parser.parse_args()
    if args.survival == 0:
        parser.error("--survival must be greater than zero")
    if MODE == "ports" and args.base_port + args.ports - 1 > 65535:
        parser.error("planned ports must be in 1..65535")
    gb, usable = TIERS[args.tier]
    gb = gb if args.gb is None else args.gb
    usable = usable if args.usable_ips is None else args.usable_ips
    metered = gb * (1 + args.retry_fraction)
    draws = math.ceil(usable / args.survival)
    failed = draws - usable
    paid = math.ceil(usable + failed * (1 - args.replacement_eligible))
    nine = paid * args.nine_ip_price
    rows = [{"vendor": "9Proxy", "basis": "IP", "units": paid, "monthly_usd": round(nine, 2)}]
    crossovers = {}
    for key, name in (("abc", "ABCProxy"), ("luna", "LunaProxy")):
        model = getattr(args, key + "_model")
        rate = getattr(args, key + "_gb_price")
        units = metered if model == "bandwidth" else math.ceil(usable + failed * (1 - getattr(args, key + "_replacement_eligible")))
        cost = units * (rate if model == "bandwidth" else getattr(args, key + "_ip_price"))
        rows.append({"vendor": name, "basis": "GB" if model == "bandwidth" else "IP", "units": units, "monthly_usd": round(cost, 2)})
        crossovers[name] = round(nine / (rate * (1 + args.retry_fraction)), 2) if model == "bandwidth" and rate else None
    annual = {r["vendor"]: round((r["monthly_usd"] - rows[0]["monthly_usd"]) * 12, 2) for r in rows[1:]}
    result = {"mode": MODE, "tier": args.tier, "currency": "USD", "price_status": "unverified scenario inputs; not current vendor quotes", "inputs": vars(args), "useful_gb": gb, "metered_gb": round(metered, 2), "usable_ips": usable, "expected_draws_rounded": draws, "replacement_draws": failed, "rows": rows, "annual_savings_usd": annual, "replacement_credit_usd_month": round((draws - paid) * args.nine_ip_price, 2), "break_even_useful_gb": crossovers, "gateway": GATEWAY}
    if MODE == "ports":
        capacity = args.ports * args.per_port
        result["port_plan"] = {"capacity": capacity, "waves": math.ceil(args.concurrency / capacity), "route_preview": [args.base_port + i % args.ports for i in range(min(args.concurrency, 16))]}
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("Offline scenario | tier=" + args.tier + " | mode=" + MODE)
    print("USD inputs are assumptions, not verified current vendor prices.")
    print(f"Useful GB: {gb:.2f} | Metered GB: {metered:.2f} | IP draws: {draws}")
    print("+------------+-------+------------+--------------+")
    print("| Provider   | Basis | Units/mo   | USD/month    |")
    print("+------------+-------+------------+--------------+")
    for row in rows:
        print(f"| {row['vendor']:<10} | {row['basis']:<5} | {row['units']:>10.2f} | {row['monthly_usd']:>12.2f} |")
    print("+------------+-------+------------+--------------+")
    for vendor, saving in annual.items():
        print(f"Annual savings vs {vendor}: USD {saving:,.2f}")
    print(f"Replacement credit per month: USD {result['replacement_credit_usd_month']:,.2f}")
    for vendor, volume in crossovers.items():
        print(f"Break-even useful GB vs {vendor}: {volume if volume is not None else 'N/A'}")
    if MODE == "ports":
        plan = result["port_plan"]
        print(f"Port capacity: {plan['capacity']} | Required waves: {plan['waves']}")
        print("Round-robin port preview: " + ", ".join(map(str, plan["route_preview"])))
    print("Compare plan terms and take the next step: " + GATEWAY)


if __name__ == "__main__":
    main()
