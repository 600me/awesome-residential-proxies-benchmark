#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline USD planning model using historical list-price benchmarks.
Prices and packaging have not been checked live; replace with written quotes.
See README.md for capacity assumptions, exclusions and the MIT license.
"""
import argparse
import json
import math

GATEWAY = "https://go.272738.xyz/smartlead"
PLANS = {"base": (39, 6000, 2000), "pro": (94, 90000, 30000),
         "smart": (174, 150000, 60000), "prime": (379, 500000, 100000)}


def number(value):
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return result


def positive(value):
    result = int(value)
    if result <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return result


def smart_plan(tier, sends, contacts):
    choices = PLANS.items() if tier == "auto" else [(tier, PLANS[tier])]
    for name, (price, send_cap, contact_cap) in choices:
        if sends <= send_cap and contacts <= contact_cap:
            return name, args.smartlead_price if args.smartlead_price is not None else price
    parser.error("Smartlead tier cannot cover sends/contacts; custom quote required")


def instant_plan(sends, contacts):
    for name, price, cap, stored in [("Growth", 47, 5000, 1000),
                                    ("HyperGrowth", 97, 125000, 25000),
                                    ("Light Speed", 358, 500000, 100000)]:
        if sends <= cap and contacts <= stored:
            return name, args.instantly_price if args.instantly_price is not None else price
    parser.error("Instantly capacity needs a custom quote; no invented overage packs")


def lem_plan(sends):
    for cap, price in [(50000, 69), (100000, 89), (200000, 159), (500000, 359), (1000000, 659)]:
        if sends <= cap:
            return f"Email {cap}", args.lemlist_price if args.lemlist_price is not None else price
    parser.error("Lemlist volume needs a custom quote")


def output(data, rows, savings):
    data.update(gateway=GATEWAY, rows=rows, annual_savings_vs_smartlead=savings,
                price_basis="offline historical baseline, not a live quote", currency="USD")
    if args.json:
        print(json.dumps(data, indent=2, allow_nan=False))
        return
    print(data["scenario"])
    print("Price basis: offline benchmarks; confirm current quotes and packaging.")
    print("+----------------------------------------+--------------+--------------+")
    print("| Cost item                              | Monthly USD  | Annual USD   |")
    print("+----------------------------------------+--------------+--------------+")
    for name, month, year in rows:
        print(f"| {name:<38} | {month:>12.2f} | {year:>12.2f} |")
    print("+----------------------------------------+--------------+--------------+")
    for name, amount in savings.items():
        print(f"Annual savings vs {name}: ${amount:,.2f} (negative = Smartlead costs more)")
    for note in data.get("notes", []):
        print(note)
    print(GATEWAY)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tier", choices=["auto", *PLANS], default="auto")
parser.add_argument("--json", action="store_true", help="emit one JSON document")
parser.add_argument("--smartlead-price", type=number, help="quoted monthly platform price")
parser.add_argument("--instantly-price", type=number, help="quoted monthly platform price")
parser.add_argument("--lemlist-price", type=number, help="quoted email-only monthly platform price")

parser.add_argument("--sends", type=positive, default=20000)
parser.add_argument("--contacts", type=positive, default=5000)
parser.add_argument("--mailboxes", type=positive, default=40)
parser.add_argument("--domains", type=positive, default=14)
parser.add_argument("--mailbox-price", type=number, default=4.5)
parser.add_argument("--domain-year", type=number, default=13)
parser.add_argument("--discount", type=number, default=0, help="hypothetical percentage, no verified code")
parser.add_argument("--discount-months", type=positive, default=1)
parser.add_argument("--duplicate-warmup", type=number, default=1.5, help="assumed redundant USD/mailbox/month")
args = parser.parse_args()
if args.discount > 100 or args.discount_months > 12:
    parser.error("discount must be 0..100 and discount-months 1..12")
smart_name, smart = smart_plan(args.tier, args.sends, args.contacts)
instant_name, instant = instant_plan(args.sends, args.contacts)
lem_name, lem = lem_plan(args.sends)
infra = args.mailboxes*args.mailbox_price + args.domains*args.domain_year/12
coupon = smart*args.discount/100*args.discount_months
smart_year = (smart+infra)*12-coupon
redundant = args.mailboxes*args.duplicate_warmup
rows = [("Common mailbox + domain cost", infra, infra*12),
        ("Smartlead recurring total", smart+infra, (smart+infra)*12),
        ("Smartlead first-year effective", smart_year/12, smart_year),
        ("Instantly total", instant+infra, (instant+infra)*12),
        ("Lemlist Email total", lem+infra, (lem+infra)*12),
        ("Avoidable duplicate warmup (separate)", redundant, redundant*12)]
output({"scenario": "Coupon duration and duplicate-warmup audit", "inputs": vars(args),
        "plans": [smart_name, instant_name, lem_name], "hypothetical_coupon_savings": coupon,
        "duplicate_warmup_annual_avoidable": redundant*12,
        "notes": ["No coupon code or live promotion is verified; default discount is zero.",
                  "Duplicate warmup is optional waste for ANY provider; excluded from totals.",
                  "Coupon applies to platform fee only; annual column is first-year cost."]}, rows,
       {"Instantly": (instant+infra)*12-smart_year, "Lemlist Email": (lem+infra)*12-smart_year})
