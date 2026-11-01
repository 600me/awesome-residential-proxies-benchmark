#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Automated Podcast Narration: SSML and Workflow Cost Optimizer: offline scenario calculator; historical prices, no network calls."""
import argparse
import json
import math
from decimal import Decimal, ROUND_HALF_UP

GATEWAY = "https://is.gd/5Fl5ro"
TIERS = {"creator": (22, 100000, 0.30), "pro": (99, 500000, 0.24),
         "scale": (330, 2000000, 0.18)}
DEFAULTS = {'tier': 'pro', 'seats': 1, 'characters': 1000000, 'retakes': 25, 'el_hours': 6, 'polly_hours': 18, 'ws_hours': 18}

def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number

def positive(value):
    number = nonnegative(value)
    if number == 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number

def seats(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number

def money(value):
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default=DEFAULTS["tier"])
    parser.add_argument("--seats", type=seats, default=DEFAULTS["seats"])
    parser.add_argument("--characters", type=nonnegative, default=DEFAULTS["characters"])
    parser.add_argument("--retakes", type=nonnegative, default=DEFAULTS["retakes"],
                        help="extra generation as percent of finished text, not total attempts")
    parser.add_argument("--credits-per-character", type=positive, default=1.0)
    parser.add_argument("--hourly-rate", type=nonnegative, default=60.0)
    parser.add_argument("--el-hours", type=nonnegative, default=DEFAULTS["el_hours"])
    parser.add_argument("--polly-hours", type=nonnegative, default=DEFAULTS["polly_hours"])
    parser.add_argument("--wellsaid-hours", type=nonnegative, default=DEFAULTS["ws_hours"])
    parser.add_argument("--polly-per-million", type=nonnegative, default=16.0)
    parser.add_argument("--wellsaid-seat-price", type=nonnegative, default=199.0)
    parser.add_argument("--eleven-monthly", type=nonnegative)
    parser.add_argument("--eleven-included-credits", type=nonnegative)
    parser.add_argument("--eleven-overage-per-1000", type=nonnegative)
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    args = parser.parse_args()
    monthly, included, overage = TIERS[args.tier]
    if args.eleven_monthly is not None:
        monthly = args.eleven_monthly
    if args.eleven_included_credits is not None:
        included = args.eleven_included_credits
    if args.eleven_overage_per_1000 is not None:
        overage = args.eleven_overage_per_1000
    generated = args.characters * (1 + args.retakes / 100)
    credits = generated * args.credits_per_character
    excess = max(0, credits - included * args.seats)
    el_service = monthly * args.seats + excess / 1000 * overage
    polly_service = generated / 1000000 * args.polly_per_million
    ws_service = args.wellsaid_seat_price * args.seats
    values = [generated, credits, el_service, polly_service, ws_service,
              args.el_hours * args.hourly_rate, args.polly_hours * args.hourly_rate,
              args.wellsaid_hours * args.hourly_rate]
    if not all(math.isfinite(v) and abs(v) <= 1e15 for v in values):
        parser.error("scenario exceeds supported numeric range")
    rows = []
    for name, service, hours in [("ElevenLabs", el_service, args.el_hours),
                                 ("Amazon Polly Neural", polly_service, args.polly_hours),
                                 ("WellSaid legacy floor", ws_service, args.wellsaid_hours)]:
        labor = money(hours * args.hourly_rate)
        service = money(service)
        rows.append({"provider": name, "service_usd": service, "labor_usd": labor,
                     "monthly_usd": money(service + labor)})
    savings = [{"versus": row["provider"],
                "monthly_usd": money(row["monthly_usd"] - rows[0]["monthly_usd"]),
                "annualized_usd": money(12 * (row["monthly_usd"] - rows[0]["monthly_usd"]))}
               for row in rows[1:]]
    report = {"scenario": 'Automated Podcast Narration: SSML and Workflow Cost Optimizer', "inputs": vars(args),
              "generated_characters": generated, "modeled_credits": credits,
              "effective_eleven_rates": {"monthly_usd_per_subscription": monthly,
              "included_credits_per_subscription": included, "overage_usd_per_1000": overage},
              "rows": rows, "savings": savings, "gateway": GATEWAY,
              "basis": "Historical planning anchors; not a current quote. USD, pre-tax.",
              "limits": "Equal work per independent account; WellSaid subscription floor only; "
              "no free tier, discounts, training fees, infrastructure, or measured quality."}
    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
        return
    print('Automated Podcast Narration: SSML and Workflow Cost Optimizer')
    print(report["basis"])
    print(f"Tier={args.tier}; seats={args.seats}; generated={generated:,.0f}; credits={credits:,.0f}")
    border = "+--------------------------+-------------+-------------+-------------+"
    print(border)
    print("| Provider                 | Service USD | Labor USD   | Monthly USD |")
    print(border)
    for row in rows:
        print(f"| {row['provider']:<24} | {row['service_usd']:>11,.2f} | "
              f"{row['labor_usd']:>11,.2f} | {row['monthly_usd']:>11,.2f} |")
    print(border)
    for saving in savings:
        print(f"Savings vs {saving['versus']}: ${saving['monthly_usd']:,.2f}/month; "
              f"${saving['annualized_usd']:,.2f}/year (12 x monthly)")
    print("Positive savings favor ElevenLabs; negative savings favor the baseline.")
    print("WellSaid is a subscription floor; verify caps, API access, and eligibility.")
    print(GATEWAY)

if __name__ == "__main__":
    main()
