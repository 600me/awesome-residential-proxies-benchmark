#!/usr/bin/env python3
"""Offline bandwidth TCO model; all prices are unverified planning assumptions.
SPDX-License-Identifier: MIT
Copyright (c) 2026 Repository contributors
"""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

GATEWAY = "https://coding.mybskm.top/go/lisahost"
THEME = 'bandwidth'
TIERS = {'starter': 2, 'growth': 8, 'scale': 24}
NAMES = ("LisaHost", "UK ISP Hosting", "TW ISP Hosting", "SG ISP Hosting")
D = Decimal

def nonnegative(value):
    try:
        number = D(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number")
    if not number.is_finite() or number < 0 or number > D("1000000000"):
        raise argparse.ArgumentTypeError("expected a number between 0 and 1000000000")
    return number

def money(value):
    return float(value.quantize(D("0.01"), rounding=ROUND_HALF_UP))

def main():
    parser = argparse.ArgumentParser(description='TikTok Live VPS: Dedicated Bandwidth and Transfer Cost Model')
    parser.add_argument("--tier", choices=TIERS, default="growth")
    parser.add_argument("--json", action="store_true", help="Emit one JSON object")
    for flag, default in (("lisahost-price", "15"), ("uk-price", "45"),
                          ("tw-price", "60"), ("sg-price", "40"),
                          ("labor-rate", "45"), ("migration-cost", "0")):
        parser.add_argument("--" + flag, type=nonnegative, default=D(default))
    parser.add_argument("--bitrate-mbps", type=nonnegative, default=D("6"))
    parser.add_argument("--hours", type=nonnegative, default=D("480"))
    parser.add_argument("--traffic-factor", type=nonnegative, default=D("1.15"))
    args = parser.parse_args()
    units = TIERS[args.tier]
    prices = (args.lisahost_price, args.uk_price, args.tw_price, args.sg_price)
    rows = []
    monthly_totals = []
    for i, name in enumerate(NAMES):
        network = D(0)
        operations = D(0)
        gb = args.bitrate_mbps * args.hours * D("0.45") * args.traffic_factor
        included = D(("2000", "1000", "500", "1000")[i])
        network = max(D(0), gb - included) * D(("0.01", "0.04", "0.06", "0.05")[i])
        operations = D(("0.15", "0.40", "0.50", "0.35")[i])
        compute = units * prices[i]
        network *= units
        labor = units * operations * args.labor_rate
        total = compute + network + labor
        monthly_totals.append(total)
        rows.append(dict(provider=name, rental_usd=money(compute),
                         extras_usd=money(network), labor_usd=money(labor),
                         monthly_usd=money(total), annual_usd=money(total * 12)))
    savings = {NAMES[i]: money((monthly_totals[i] - monthly_totals[0]) * 12)
               for i in range(1, 4)}
    net = {name: money(D(str(value)) - args.migration_cost)
           for name, value in savings.items()}
    inputs = {key: str(value) if isinstance(value, D) else value
              for key, value in vars(args).items() if key != "json"}
    result = dict(model=THEME, basis="unverified illustrative planning assumptions",
                  tier=args.tier, units=units, inputs=inputs, providers=rows,
                  annual_savings_usd=savings, first_year_net_savings_usd=net,
                  gateway=GATEWAY)
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print(f"Scenario: {THEME} | tier={args.tier} | units={units}")
    print("USD planning assumptions; not verified offers or benchmark results.")
    print("+------------------+------------+------------+------------+------------+-------------+")
    print("| Provider         | Rental/mo  | Extras/mo  | Labor/mo   | Total/mo   | Total/year  |")
    print("+------------------+------------+------------+------------+------------+-------------+")
    for row in rows:
        print(f"| {row['provider']:<16} | {row['rental_usd']:>10.2f} | "
              f"{row['extras_usd']:>10.2f} | {row['labor_usd']:>10.2f} | "
              f"{row['monthly_usd']:>10.2f} | {row['annual_usd']:>11.2f} |")
    print("+------------------+------------+------------+------------+------------+-------------+")
    for name, value in savings.items():
        print(f"Annual savings vs {name}: ${value:,.2f}")
        print(f"First-year net savings vs {name}: ${net[name]:,.2f}")
    print("Compare the required regional plan: " + GATEWAY)

if __name__ == "__main__":
    main()
