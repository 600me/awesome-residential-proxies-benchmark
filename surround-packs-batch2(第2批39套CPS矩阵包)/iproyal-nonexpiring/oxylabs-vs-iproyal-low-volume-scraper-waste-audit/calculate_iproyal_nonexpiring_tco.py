#!/usr/bin/env python3
"""Audit the difference between reserved proxy traffic and the small amount a scraper actually uses. Offline scenario model; prices are editable historical benchmarks."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_CEILING

GATEWAY = "https://go.272738.xyz/iproyal"
TIERS = {"idle": "5", "low": "20", "standard": "60", "burst": "130"}
D = Decimal


def nonnegative(value):
    try:
        number = D(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number")
    if not number.is_finite() or number < 0 or number > D("1000000000"):
        raise argparse.ArgumentTypeError("expected a number from 0 through 1000000000")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="idle")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    parser.add_argument("--usage-gb", type=nonnegative, help="monthly billed GB")
    parser.add_argument("--allocation-gb", type=nonnegative, default=D("100"))
    parser.add_argument("--bundle-gb", type=nonnegative, default=D("100"))
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--iproyal-rate", type=nonnegative, default=D("7"))
    parser.add_argument("--brightdata-rate", type=nonnegative, default=D("8.4"))
    parser.add_argument("--oxylabs-rate", type=nonnegative, default=D("8"))
    parser.add_argument("--discount-pct", type=nonnegative, default=D("0"))
    args = parser.parse_args()
    if not 1 <= args.months <= 1200:
        parser.error("--months must be between 1 and 1200")
    if args.bundle_gb <= 0:
        parser.error("--bundle-gb must be positive")
    if args.discount_pct > 100:
        parser.error("--discount-pct must be between 0 and 100")
    usage = args.usage_gb if args.usage_gb is not None else D(TIERS[args.tier])
    total = usage * args.months
    rate = args.iproyal_rate * (1 - args.discount_pct / 100)
    bundles = (total / args.bundle_gb).to_integral_value(rounding=ROUND_CEILING)
    purchased = bundles * args.bundle_gb
    cash = purchased * rate
    allocated = max(args.allocation_gb, usage)
    expired = max(args.allocation_gb - usage, D(0))
    number = lambda value: float(value.quantize(D("0.01")))
    providers = [{"provider": "IPRoyal", "effective_rate_usd_gb": number(rate),
                  "monthly_consumed_value_usd": number(usage * rate),
                  "period_cash_usd": number(cash), "period_expired_gb": 0.0,
                  "closing_usable_gb": number(purchased - total)}]
    savings = {}
    for name, unit in [("Bright Data", args.brightdata_rate), ("Oxylabs", args.oxylabs_rate)]:
        bill = allocated * unit * args.months
        providers.append({"provider": name, "effective_rate_usd_gb": number(unit),
                          "monthly_consumed_value_usd": number(usage * unit),
                          "period_cash_usd": number(bill),
                          "period_expired_gb": number(expired * args.months),
                          "closing_usable_gb": 0.0})
        savings[name] = number((bill - cash) * 12 / args.months)
    report = {"model": "offline historical benchmarks; monthly-expiry scenario only",
              "tier": args.tier, "monthly_usage_gb": number(usage), "months": args.months,
              "monthly_allocation_gb": number(args.allocation_gb),
              "iproyal_bundle_gb": number(args.bundle_gb),
              "iproyal_discount_pct": number(args.discount_pct),
              "providers": providers, "annualized_cash_savings_usd": savings,
              "gateway": GATEWAY}
    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
        return
    print("Offline TCO | monthly-expiry scenario | historical benchmarks, not live quotes")
    print(f"Tier: {args.tier} | use: {usage} GB/month | horizon: {args.months} months")
    print("Comparison: monthly allowance + same-rate top-ups; unused allowance expires.")
    print("IPRoyal: buy bundles as needed; carry unused GB forward; opening balance = 0.")
    border = "+--------------+----------+--------------+------------+------------+"
    print(border)
    print("| Provider     | USD/GB   | Period cash  | Expired GB | Closing GB |")
    print(border)
    for row in providers:
        print(f"| {row['provider']:<12} | {row['effective_rate_usd_gb']:>8.2f} | "
              f"{row['period_cash_usd']:>12.2f} | {row['period_expired_gb']:>10.2f} | "
              f"{row['closing_usable_gb']:>10.2f} |")
    print(border)
    print(f"IPRoyal consumed value over horizon: USD {total * rate:.2f}")
    for name, saving in savings.items():
        print(f"Annualized cash savings vs {name}: USD {saving:.2f}")
    print("Annualized savings scale period cash by 12/months; refills are lumpy.")
    print("Taxes, retries, FX, and migration labor excluded; negative savings are possible.")
    print(f"Review IPRoyal terms and pricing: {GATEWAY}")


if __name__ == "__main__":
    main()
