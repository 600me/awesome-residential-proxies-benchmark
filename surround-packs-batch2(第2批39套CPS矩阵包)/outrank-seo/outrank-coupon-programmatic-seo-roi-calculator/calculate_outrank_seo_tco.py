#!/usr/bin/env python3
"""Offline, assumption-based SEO TCO calculator. MIT license; see README.md."""
import argparse
import json
import math

GATEWAY = "https://is.gd/ZzMPnz"
SCENARIO = 'Coupon and contribution economics'
STACK_MINUTES, AUTO_MINUTES = 36, 10
STACK_FIXED, AUTO_FIXED, MIGRATION_HOURS = 2, 1, 4
TIERS = {"starter": (30, 1, 1), "growth": (60, 2, 2), "agency": (120, 4, 3)}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0 or number > 1_000_000:
        raise argparse.ArgumentTypeError("must be finite and between 0 and 1000000")
    return number


def percentage(value):
    number = nonnegative(value)
    if number > 100:
        raise argparse.ArgumentTypeError("percentage must be between 0 and 100")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="starter", help="workload preset, not a vendor plan")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    parser.add_argument("--hourly-rate", type=nonnegative, default=50)
    parser.add_argument("--outrank-price", type=nonnegative, default=99, help="USD/site/month budget")
    parser.add_argument("--surfer-price", type=nonnegative, default=89, help="USD/month base budget")
    parser.add_argument("--jasper-price", type=nonnegative, default=49, help="USD/seat/month budget")
    parser.add_argument("--stack-minutes", type=nonnegative, default=STACK_MINUTES)
    parser.add_argument("--outrank-minutes", type=nonnegative, default=AUTO_MINUTES)
    parser.add_argument("--migration-hours", type=nonnegative, default=MIGRATION_HOURS)
    parser.add_argument("--discount-percent", type=percentage, default=0)
    parser.add_argument("--indexed-percent", type=percentage, default=70)
    parser.add_argument("--contribution", type=nonnegative, default=100, help="USD net contribution/conversion")
    parser.add_argument("--conversions", type=nonnegative, default=0, help="incremental conversions/month")
    args = parser.parse_args()
    articles, sites, seats = TIERS[args.tier]
    auto_fee = sites * args.outrank_price * (1 - args.discount_percent / 100)
    stack_fee = args.surfer_price + seats * args.jasper_price
    auto_labor = (articles * args.outrank_minutes / 60 + AUTO_FIXED) * args.hourly_rate
    stack_labor = (articles * args.stack_minutes / 60 + STACK_FIXED) * args.hourly_rate
    auto_total, stack_total = auto_fee + auto_labor, stack_fee + stack_labor
    savings = stack_total - auto_total
    migration = args.migration_hours * args.hourly_rate
    indexed = articles * args.indexed_percent / 100
    result = {
        "scenario": SCENARIO, "tier": args.tier, "currency": "USD",
        "articles": articles, "modeled_sites": sites, "modeled_jasper_seats": seats,
        "inputs": vars(args),
        "fixed_hours": {"stack": STACK_FIXED, "outrank": AUTO_FIXED},
        "stack_software_monthly": round(stack_fee, 2),
        "outrank_software_monthly": round(auto_fee, 2),
        "stack_labor_monthly": round(stack_labor, 2),
        "outrank_labor_monthly": round(auto_labor, 2),
        "stack_tco_monthly": round(stack_total, 2),
        "outrank_tco_monthly": round(auto_total, 2),
        "monthly_savings": round(savings, 2), "annual_savings": round(savings * 12, 2),
        "migration_cost": round(migration, 2),
        "first_year_savings": round(savings * 12 - migration, 2),
        "migration_payback_months": round(migration / savings, 2) if savings > 0 else None,
        "expected_indexed_pages": round(indexed, 2),
        "stack_cost_per_indexed_page": round(stack_total / indexed, 2) if indexed else None,
        "outrank_cost_per_indexed_page": round(auto_total / indexed, 2) if indexed else None,
        "outrank_break_even_conversions": math.ceil(auto_total / args.contribution) if args.contribution else None,
        "outrank_monthly_contribution_less_cost": round(args.conversions * args.contribution - auto_total, 2),
        "gateway": GATEWAY,
        "basis": "Unverified historical price anchors and explicit workload assumptions; not a vendor quote or measured benchmark."
    }
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print(SCENARIO + " | " + args.tier + " | " + str(articles) + " articles/month")
    print("Planning inputs; USD; prices and capacities require confirmation.")
    rule = "+------------------------+-------------------+-------------------+"
    print(rule)
    print("| Monthly bill (USD)     | SurferSEO+Jasper  | Outrank.so        |")
    print(rule)
    for label, stack_value, auto_value in (
        ("Software", stack_fee, auto_fee), ("Editorial + operations", stack_labor, auto_labor),
        ("TOTAL", stack_total, auto_total)):
        print(f"| {label:<22} | {stack_value:>17,.2f} | {auto_value:>17,.2f} |")
    print(rule)
    print(f"Monthly savings: ${savings:,.2f}")
    print(f"Annualized savings: ${savings * 12:,.2f}")
    print(f"One-time migration: ${migration:,.2f}")
    print(f"First-year savings after migration: ${savings * 12 - migration:,.2f}")
    print("Expected indexed pages (assumed): " + str(result["expected_indexed_pages"]))
    unit_cost = result["outrank_cost_per_indexed_page"]
    print("Outrank cost/expected indexed page: " + (f"${unit_cost:,.2f}" if unit_cost is not None else "N/A"))
    print("Outrank break-even conversions/month: " + str(result["outrank_break_even_conversions"]))
    print(f"Contribution less Outrank cost/month: ${result['outrank_monthly_contribution_less_cost']:,.2f}")
    print("Evaluate Outrank.so: " + GATEWAY)


if __name__ == "__main__":
    main()
