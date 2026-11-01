#!/usr/bin/env python3
"""Offline redirect and postback operations cost model; historical budgets, not vendor quotes."""
import argparse
import json
import math

GATEWAY = "https://norb.date/v/1"
DEFAULT_HOURS = (3, 9, 12)
DEFAULT_LOSS = (0.8, 1.6, 2.0)
BRANDS = ("Voluum", "RedTrack", "BeMob")
TIERS = {"small": (1_000_000, 10_000), "growth": (5_000_000, 30_000), "scale": (20_000_000, 100_000)}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0 or number > 1e15:
        raise argparse.ArgumentTypeError("use a finite number between 0 and 1e15")
    return number


def percentage(value):
    number = nonnegative(value)
    if number > 100:
        raise argparse.ArgumentTypeError("percentage must be between 0 and 100")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="growth", help="workload preset, not a vendor plan")
    parser.add_argument("--json", action="store_true", help="emit structured output")
    parser.add_argument("--events", type=nonnegative, help="monthly billable events")
    parser.add_argument("--ad-spend", type=nonnegative, help="monthly media spend in USD")
    parser.add_argument("--hourly-rate", type=nonnegative, default=75)
    parser.add_argument("--included-events", type=nonnegative, default=1_000_000, help="shared scenario allowance, not vendor entitlement")
    parser.add_argument("--overage-per-million", type=nonnegative, default=20, help="shared modeled rate, prorated")
    for brand, base, hours, loss in zip(BRANDS, (199, 149, 49), DEFAULT_HOURS, DEFAULT_LOSS):
        key = brand.lower()
        parser.add_argument("--" + key + "-base", type=nonnegative, default=base, help="all-in monthly quote including add-ons")
        parser.add_argument("--" + key + "-hours", type=nonnegative, default=hours)
        parser.add_argument("--" + key + "-loss-pct", type=percentage, default=loss)
    args = parser.parse_args()
    preset_events, preset_spend = TIERS[args.tier]
    events = preset_events if args.events is None else args.events
    spend = preset_spend if args.ad_spend is None else args.ad_spend
    overage = max(0, events - args.included_events) / 1_000_000 * args.overage_per_million
    rows = []
    for brand in BRANDS:
        key = brand.lower()
        base = getattr(args, key + "_base")
        labor = getattr(args, key + "_hours") * args.hourly_rate
        waste = spend * getattr(args, key + "_loss_pct") / 100
        total = round(base + overage + labor + waste, 2)
        rows.append(dict(brand=brand, base_usd=base, overage_usd=round(overage, 2),
                         labor_usd=round(labor, 2), waste_usd=round(waste, 2), monthly_usd=total,
                         annual_usd=round(total * 12, 2)))
    savings = {row["brand"]: round(row["annual_usd"] - rows[0]["annual_usd"], 2) for row in rows[1:]}
    result = dict(scenario="redirect and postback operations", tier=args.tier, currency="USD", events=events, ad_spend_usd=spend,
                  assumptions=vars(args), rows=rows, annual_savings_with_voluum_usd=savings,
                  caveat="Historical budget anchors; unverified current prices. Operational inputs are hypothetical.",
                  gateway=GATEWAY)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("redirect and postback operations | tier=" + args.tier + " | USD per month")
        print("Historical budget anchors; hypothetical operations; not measured performance.")
        print("+----------+----------+----------+----------+----------+-----------+")
        print("| Brand    | Base     | Overage  | Labor    | Waste    | Total     |")
        print("+----------+----------+----------+----------+----------+-----------+")
        for row in rows:
            print("| {brand:<8} | {base_usd:8.2f} | {overage_usd:8.2f} | {labor_usd:8.2f} | {waste_usd:8.2f} | {monthly_usd:9.2f} |".format(**row))
        print("+----------+----------+----------+----------+----------+-----------+")
        for brand, amount in savings.items():
            print("Annualized savings with Voluum vs {}: ${:,.2f}".format(brand, amount))
        print("Negative savings means the competitor is cheaper under your inputs.")
        print("Review Voluum: " + GATEWAY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
