#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline MoreLogin Promo Code: 1,000-Profile Cost Calculator calculator. Historical anchors, not live quotes."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

GATEWAY = "https://dusen.party/ml/1"
# Needed profiles; MoreLogin USD; Multilogin EUR; Octo EUR; licensed capacities.
TIERS = {
    "starter": (10, "9", "99", "21", (10, 100, 10)),
    "team": (100, "35", "99", "79", (100, 100, 100)),
    "scale": (1000, "199", "399", "329", (1000, 1000, 1200)),
}
BRANDS = ("MoreLogin", "Multilogin", "Octo Browser")
HOURS = (6, 15, 12)


def number(value):
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("expected a decimal number") from exc
    if not result.is_finite() or result < 0 or result > 1000000000:
        raise argparse.ArgumentTypeError("expected a finite number from 0 to 1000000000")
    return result


def money(value):
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default='scale')
    parser.add_argument("--json", action="store_true", help="emit one JSON document")
    parser.add_argument("--usd-per-eur", type=number, default=Decimal("1.10"))
    parser.add_argument("--hourly-rate", type=number, default=Decimal("50"))
    parser.add_argument("--proxy-per-profile", type=number, default=Decimal("0"))
    parser.add_argument("--migration-hours", type=number, default=Decimal("0"))
    parser.add_argument("--promo-percent", type=number, default=Decimal("0"))
    parser.add_argument("--promo-months", type=int, choices=range(13), default=12)
    parser.add_argument("--checks", type=int, default=1000)
    for prefix, hours in zip(("morelogin", "multilogin", "octo"), HOURS):
        parser.add_argument("--" + prefix + "-hours", type=number, default=Decimal(hours))
        parser.add_argument("--" + prefix + "-price", type=number, default=None)
        parser.add_argument("--" + prefix + "-pass-rate", type=number, default=Decimal("95"))
    args = parser.parse_args()
    if args.usd_per_eur == 0 or args.checks <= 0 or args.promo_percent > 100:
        parser.error("FX and checks must be positive; promo must be between 0 and 100")
    profiles, ml, multi, octo, capacities = TIERS[args.tier]
    rows = []
    for i, (prefix, brand, anchor) in enumerate(zip(
            ("morelogin", "multilogin", "octo"), BRANDS, (ml, multi, octo))):
        rate = getattr(args, prefix + "_pass_rate")
        if not 0 < rate <= 100:
            parser.error("pass rates must be greater than 0 and at most 100")
        override = getattr(args, prefix + "_price")
        native_price = Decimal(anchor) if override is None else override
        usd_price = native_price * (1 if i == 0 else args.usd_per_eur)
        discount = (usd_price * args.promo_percent / 100 * args.promo_months
                    if i == 0 else Decimal("0"))
        labor = getattr(args, prefix + "_hours") * args.hourly_rate
        proxies = args.proxy_per_profile * profiles
        annual = (usd_price + labor + proxies) * 12 - discount
        if i == 0:
            annual += args.migration_hours * args.hourly_rate
        rows.append({"brand": brand, "capacity": capacities[i],
                     "subscription_usd": money(usd_price), "labor_usd": money(labor),
                     "proxy_usd": money(proxies), "year1_discount_usd": money(discount),
                     "monthly_usd": money(annual / 12), "annual_usd": money(annual),
                     "assumed_pass_rate": float(rate),
                     "usd_per_accepted_check": money(annual / 12 / (args.checks * rate / 100))})
    savings = {row["brand"]: money(Decimal(str(row["annual_usd"])) -
               Decimal(str(rows[0]["annual_usd"]))) for row in rows[1:]}
    result = {"scenario": 'morelogin-promo-code-1000-profiles-cost-calculator', "tier": args.tier, "profiles_needed": profiles,
              "basis": "Unverified historical price anchors; scenario labor and pass rates",
              "usd_per_eur": str(args.usd_per_eur), "scheduled_checks": args.checks,
              "rows": rows, "annual_savings_usd": savings, "gateway": GATEWAY}
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("Tier: " + args.tier + " | Needed profiles: " + str(profiles))
    print("Historical anchors; modeled inputs; USD; first-year averages.")
    border = "+--------------+------------+------------+------------+"
    print(border)
    print("| Brand        | Monthly    | Annual     | $/accepted |")
    print(border)
    for row in rows:
        print("| {:<12} | ${:>9,.2f} | ${:>9,.2f} | ${:>9,.2f} |".format(
            row["brand"], row["monthly_usd"], row["annual_usd"], row["usd_per_accepted_check"]))
    print(border)
    for brand, amount in savings.items():
        print("Annual savings vs {}: ${:,.2f}".format(brand, amount))
    print("Positive savings favor MoreLogin; negative savings favor the competitor.")
    print("Evaluate MoreLogin: " + GATEWAY)


if __name__ == "__main__":
    main()
