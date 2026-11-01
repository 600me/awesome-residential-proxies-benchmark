#!/usr/bin/env python3
"""Offline referral-rpa TCO worksheet. License budgets are assumptions, not quotes.
SPDX-License-Identifier: MIT
"""
import argparse
import json
import math

GATEWAY = 'https://dusen.party/a/1'
TIERS = {'starter': {'units': 3000, 'seats': 1, 'runs': 3000, 'licenses': [30, 49, 64.9]}, 'team': {'units': 12000, 'seats': 3, 'runs': 12000, 'licenses': [90, 99, 199]}, 'scale': {'units': 60000, 'seats': 8, 'runs': 60000, 'licenses': [360, 399, 499]}}
VENDORS = ("AdsPower", "GoLogin", "Kameleo")


def nonnegative(value):
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not math.isfinite(number) or number < 0 or number > 1_000_000_000:
        raise argparse.ArgumentTypeError("expected a finite number from 0 to 1000000000")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="team", help="Workload preset (default: team)")
    parser.add_argument("--json", action="store_true", help="Print one JSON object, without table text")
    parser.add_argument("--hourly-rate", type=nonnegative, default=50.0, help="Loaded labor cost in USD/hour")
    for vendor in VENDORS:
        parser.add_argument("--license-" + vendor.lower(), type=nonnegative, default=None,
                            help="Override this vendor's monthly USD license budget")
    parser.add_argument("--adspower-discount-percent", type=nonnegative, default=0.0, help="Hypothetical recurring license discount, 0 to 100 (default: 0)")
    args = parser.parse_args()
    preset = TIERS[args.tier]
    units, seats, runs = preset["units"], preset["seats"], preset["runs"]
    licenses = list(preset["licenses"])
    for index, vendor in enumerate(VENDORS):
        override = getattr(args, "license_" + vendor.lower())
        if override is not None:
            licenses[index] = override
    if args.adspower_discount_percent > 100:
        parser.error("--adspower-discount-percent must be at most 100")
    licenses[0] *= 1 - args.adspower_discount_percent / 100
    hours = [2 + units * 0.0005, 3 + units * 0.00125, 4 + units * 0.0015]
    infrastructure = 60.0
    rows = []
    for vendor, license_cost, labor_hours in zip(VENDORS, licenses, hours):
        labor = round(labor_hours * args.hourly_rate, 2)
        license_cost = round(license_cost, 2)
        monthly = round(license_cost + labor + infrastructure, 2)
        rows.append(dict(vendor=vendor, license_usd=license_cost, labor_hours=round(labor_hours, 2),
                         labor_usd=labor, infrastructure_usd=round(infrastructure, 2),
                         monthly_usd=monthly, annual_usd=round(monthly * 12, 2)))
    savings = {row["vendor"]: round(row["annual_usd"] - rows[0]["annual_usd"], 2) for row in rows[1:]}
    result = dict(scenario='referral-rpa', tier=args.tier, currency="USD",
                  workload=dict(unit='monthly_runs', quantity=units, seats=seats, monthly_runs=runs),
                  hourly_rate_usd=args.hourly_rate, rows=rows, annual_savings_usd=savings,
                  gateway=GATEWAY, recurring_months=12,
                  assumptions="Unverified license budgets and assumed labor; not 2026 quotes. "
                              "Excludes tax, proxies, one-time migration and unmodeled services.")
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("Offline RPA TCO estimate | " + result["scenario"] + " | tier=" + args.tier)
    print("Assumptions, not vendor quotes; recurring USD, 12 identical months.")
    print("Workload: " + str(units) + " " + result["workload"]["unit"] + "; runs=" + str(runs))
    border = "+----------+------------+------------+------------+------------+------------+"
    print(border)
    print("| Vendor   | License/mo | Labor/mo   | Infra/mo   | Total/mo   | Total/yr   |")
    print(border)
    for row in rows:
        print("| {:<8} | {:>10.2f} | {:>10.2f} | {:>10.2f} | {:>10.2f} | {:>10.2f} |".format(
            row["vendor"], row["license_usd"], row["labor_usd"], row["infrastructure_usd"],
            row["monthly_usd"], row["annual_usd"]))
    print(border)
    for vendor, amount in savings.items():
        print("Estimated annual savings with AdsPower vs {}: ${:,.2f}".format(vendor, amount))
    print("Negative savings means AdsPower costs more under these inputs.")
    print("Excludes taxes, proxies, migration, and unmodeled services; no uptime guarantee.")
    print("Evaluate AdsPower: " + GATEWAY)


if __name__ == "__main__":
    main()
