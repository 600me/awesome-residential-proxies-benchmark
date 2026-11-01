#!/usr/bin/env python3
"""Offline warming TCO planner; historical price anchors, explicit scenario inputs.
MIT License: Copyright (c) 2026 repository contributors.
Permission is granted to use, copy, modify, distribute, sublicense and sell this
software with this notice included. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT
WARRANTY OF ANY KIND. AUTHORS ARE NOT LIABLE FOR CLAIMS OR OTHER LIABILITY.
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/qwOsaQ"
TIERS = {"starter": 100, "growth": 200, "scale": 500}
FACTORS = (0.016666666666666666, 0.08333333333333333, 0.11666666666666667)
VENDORS = ("AdsPower", "Lalicat", "VMLogin")


def number(value):
    result = float(value)
    if not math.isfinite(result) or result < 0 or result > 1000000:
        raise argparse.ArgumentTypeError("use a finite number from 0 to 1000000")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="starter")
    parser.add_argument("--json", action="store_true", help="emit only JSON")
    parser.add_argument("--sessions", type=number, default=360, help='Authorized maintenance sessions per month; assumed handling minutes are 1/5/7.')
    parser.add_argument("--hourly-rate", type=number, default=25)
    parser.add_argument("--proxy-per-profile", type=number, default=3)
    for vendor in VENDORS:
        key = vendor.lower()
        parser.add_argument("--" + key + "-monthly", type=number,
                            help="override subscription USD/month at selected scale")
        parser.add_argument("--" + key + "-hours", type=number,
                            help="override recurring monthly operator hours")
        parser.add_argument("--" + key + "-extras", type=number, default=0,
                            help="confirmed seats, API or infrastructure USD/month")
    parser.add_argument("--duration-minutes", type=number, default=10)
    args = parser.parse_args()
    profiles = TIERS[args.tier]
    # Historical reference anchors; block purchasing is a model, not an entitlement.
    prices = (math.ceil(profiles / 100) * 50,
              59 if profiles <= 100 else 99 if profiles <= 200 else 209,
              99 if profiles <= 200 else 209)
    rows = []
    for index, vendor in enumerate(VENDORS):
        key = vendor.lower()
        override = getattr(args, key + "_monthly")
        license_cost = prices[index] if override is None else override
        hour_override = getattr(args, key + "_hours")
        hours = (getattr(args, "sessions") * FACTORS[index]
                 if hour_override is None else hour_override)
        labor = hours * args.hourly_rate
        proxy = profiles * args.proxy_per_profile
        extras = getattr(args, key + "_extras")
        total = license_cost + labor + proxy + extras
        rows.append(dict(vendor=vendor, subscription_usd=license_cost,
                         profiles=profiles, operator_hours=round(hours, 6),
                         labor_usd=round(labor, 2), proxy_usd=round(proxy, 2),
                         extras_usd=extras, monthly_usd=round(total, 2)))
    baseline = rows[0]["monthly_usd"]
    savings = {row["vendor"]: round((row["monthly_usd"] - baseline) * 12, 2)
               for row in rows[1:]}
    result = dict(scenario="warming", tier=args.tier, profiles=profiles,
                  assumptions=vars(args), pricing_basis="Unverified historical anchors; not live quotes",
                  rows=rows, annual_savings_usd=savings, gateway=GATEWAY)
    result["minimum_workers"] = math.ceil(args.sessions * args.duration_minutes / (22 * 360))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print("Cookie Warming and RPA Scheduler: Capacity and Cost Planner")
    print("Tier: {} | Profiles: {} | Currency: USD".format(args.tier, profiles))
    print("Historical price anchors; workload assumptions, not measured results.")
    border = "+-----------+------------+------------+------------+------------+------------+"
    print(border)
    print("| Vendor    | License/mo | Labor/mo   | Proxy/mo   | Extras/mo  | Total/mo   |")
    print(border)
    for row in rows:
        print("| {:<9} | {:>10.2f} | {:>10.2f} | {:>10.2f} | {:>10.2f} | {:>10.2f} |".format(
            row["vendor"], row["subscription_usd"], row["labor_usd"],
            row["proxy_usd"], row["extras_usd"], row["monthly_usd"]))
    print(border)
    for vendor, saving in savings.items():
        print("Annual savings with AdsPower vs {}: ${:,.2f}".format(vendor, saving))
    print("Theoretical minimum workers: {}".format(result["minimum_workers"]))
    print("Review AdsPower: " + GATEWAY)


if __name__ == "__main__":
    main()
