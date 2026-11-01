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

parser.add_argument("--clients", type=positive, default=6)
parser.add_argument("--sends-per-client", type=positive, default=15000)
parser.add_argument("--contacts-per-client", type=positive, default=10000)
parser.add_argument("--mailboxes-per-client", type=positive, default=25)
parser.add_argument("--domains-per-client", type=positive, default=9)
parser.add_argument("--mailbox-price", type=number, default=4.5)
parser.add_argument("--domain-year", type=number, default=13)
parser.add_argument("--multichannel-seats", type=positive, default=10)
parser.add_argument("--branding-per-client", type=number, default=0)
parser.add_argument("--hours-saved", type=number, default=0)
parser.add_argument("--hourly-rate", type=number, default=50)
args = parser.parse_args()
smart_name, smart_unit = smart_plan(args.tier, args.sends_per_client, args.contacts_per_client)
instant_name, instant_unit = instant_plan(args.sends_per_client, args.contacts_per_client)
lem_name, lem_unit = lem_plan(args.sends_per_client)
smart = args.clients*(smart_unit+args.branding_per_client)
instant = args.clients*instant_unit
lem = args.clients*lem_unit
multi = args.multichannel_seats*109
infra = args.clients*(args.mailboxes_per_client*args.mailbox_price +
                      args.domains_per_client*args.domain_year/12)
rows = [("Shared infrastructure budget", infra, infra*12)]
for name, price in [("Smartlead isolated clients", smart), ("Instantly isolated clients", instant),
                    ("Lemlist Email isolated clients", lem), ("Lemlist Multichannel reference", multi)]:
    rows.append((name, price, price*12))
    rows.append((name.replace("isolated clients", "total").replace("reference", "total"),
                 price+infra, (price+infra)*12))
labor = args.hours_saved*args.hourly_rate*12
output({"scenario": "Agency TCO: separately paid email account per client", "inputs": vars(args),
        "plans_per_client": [smart_name, instant_name, lem_name],
        "modeled_annual_labor_benefit": labor,
        "annual_net_benefit_vs_instantly": (instant-smart)*12+labor,
        "notes": ["Default isolation is one subscription/client, not a quoted agency bundle.",
                  "Multichannel reference is pooled and includes channels absent from this comparison.",
                  f"Assumed annual labor benefit (separate from bills): ${labor:.2f}",
                  "Branding defaults to zero; enter a confirmed quote if required."]}, rows,
       {"Instantly": (instant-smart)*12, "Lemlist Email": (lem-smart)*12,
        "Lemlist Multichannel reference": (multi-smart)*12})
