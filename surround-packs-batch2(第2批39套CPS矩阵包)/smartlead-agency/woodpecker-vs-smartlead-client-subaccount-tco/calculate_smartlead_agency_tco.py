#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline scenario calculator; historical price anchors, not current quotes.
No network calls, credentials, mailbox provisioning, or deliverability claims.
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/3awPq2"
PLANS = (("Pro", 94, 90000, 30000, 0),
         ("Unlimited Smart", 174, 150000, math.inf, 0),
         ("Unlimited Prime", 379, 500000, math.inf, 3))


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def smart_plan(sends, contacts, clients, fee, prices):
    options = [(price + max(0, clients - included) * fee, name)
               for (name, _, cap, storage, included), price in zip(PLANS, prices)
               if sends <= cap and contacts <= storage]
    if not options:
        raise ValueError("Smartlead workload exceeds modeled 500,000-send plans")
    total, name = min(options)
    price = prices[next(i for i, row in enumerate(PLANS) if row[0] == name)]
    return name, price, total - price


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=("pilot", "growth", "scale"), default="growth",
                        help="workload preset; named numeric flags override it")
    parser.add_argument("--json", action="store_true", help="print one JSON document")
    parser.add_argument("--hourly-rate", type=nonnegative, default=50)
    parser.add_argument("--mailbox-price", type=nonnegative, default=4.50)
    parser.add_argument("--domain-year", type=nonnegative, default=13)
    parser.add_argument("--apollo-seat-price", type=nonnegative, default=79,
                        help="monthly equivalent of annually billed Professional")
    parser.add_argument("--wood-base", type=nonnegative,
                        help="scenario allowance for volume subscription; replace with quote")
    parser.add_argument("--wood-api", type=nonnegative, default=20,
                        help="conservative API allowance; use 0 if included in your quote")
    for name, price in (("pro", 94), ("scale", 174), ("prime", 379)):
        parser.add_argument("--smart-" + name + "-price", type=nonnegative, default=price)
    parser.add_argument("--smart-client-fee", type=nonnegative, default=29)
    parser.add_argument("--wood-client-fee", type=nonnegative, default=32)
    parser.add_argument("--clients", type=positive_int, help="total contracted clients")
    parser.add_argument("--inactive", type=nonnegative, default=0)
    parser.add_argument("--mailboxes", type=positive_int)
    parser.add_argument("--operators", type=positive_int)
    parser.add_argument("--apollo-portal", type=nonnegative, default=200)
    parser.add_argument("--smart-hours", type=nonnegative, default=8)
    parser.add_argument("--apollo-hours", type=nonnegative, default=20)
    parser.add_argument("--wood-hours", type=nonnegative, default=10)
    args = parser.parse_args()
    presets = {"pilot": (5, 15, 2, 99), "growth": (20, 60, 5, 188),
               "scale": (50, 150, 10, 587)}
    c, m, o, w = presets[args.tier]
    contracted = args.clients or c
    if not float(args.inactive).is_integer() or args.inactive >= contracted:
        parser.error("--inactive must be an integer below --clients")
    clients, mailboxes = contracted - int(args.inactive), args.mailboxes or m
    seats = args.operators or o
    sends, domains = clients * 1800, math.ceil(mailboxes / 3)
    plan, platform, workspaces = smart_plan(sends, clients * 600, clients, args.smart_client_fee,
                                            (args.smart_pro_price, args.smart_scale_price, args.smart_prime_price))
    wood_base = w if args.wood_base is None else args.wood_base
    portal, hosting = args.apollo_portal, 0
    infrastructure = mailboxes * args.mailbox_price + domains * args.domain_year / 12
    hours = (args.smart_hours, args.apollo_hours, args.wood_hours)
    metrics = {"contracted_clients": contracted, "active_clients": clients,
               "paused_clients": int(args.inactive), "monthly_sends": sends,
               "mailboxes_retained": mailboxes, "apollo_operator_seats": seats}

    SCENARIO = "Active client and white-label subaccount TCO"
    rows = {
        "Platform": [platform, seats * args.apollo_seat_price, wood_base],
        "Client access": [workspaces, portal, clients * args.wood_client_fee],
        "Mailbox + domain": [infrastructure] * 3,
        "Operations labor": [hours[0] * args.hourly_rate,
                             hours[1] * args.hourly_rate,
                             hours[2] * args.hourly_rate],
        "API / hosting": [hosting, hosting, hosting + args.wood_api],
    }
    totals = [sum(row[i] for row in rows.values()) for i in range(3)]
    savings = {"Apollo.io": round((totals[1] - totals[0]) * 12, 2),
               "Woodpecker": round((totals[2] - totals[0]) * 12, 2)}
    report = {"scenario": SCENARIO, "tier": args.tier, "smartlead_plan": plan,
              "metrics": metrics, "inputs": vars(args), "rows_usd_monthly": rows,
              "vendors": ["Smartlead.ai", "Apollo.io", "Woodpecker"],
              "monthly_totals_usd": [round(x, 2) for x in totals],
              "annual_totals_usd": [round(x * 12, 2) for x in totals],
              "annual_savings_usd": savings,
              "qualification": "Offline historical anchors; caps, client/API/portal fees and labor are assumptions; "
                               "not current quotes or measured performance. Apollo annual billing equivalent; "
                               "tax, data, setup and migration excluded. SMTP seat limit is conditional.",
              "gateway": GATEWAY}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    print(SCENARIO)
    print("Tier: " + args.tier + " | Smartlead plan: " + plan)
    for key, value in metrics.items():
        print(f"{key}: {value}")
    border = "+" + "-" * 23 + "+" + ("-" * 16 + "+") * 3
    print(border)
    print(f"| {'USD / month':<21} | {'Smartlead.ai':>14} | {'Apollo.io':>14} | {'Woodpecker':>14} |")
    print(border)
    for label, values in list(rows.items()) + [("TOTAL monthly", totals),
                                              ("TOTAL annual", [x * 12 for x in totals])]:
        print(f"| {label:<21} | " + " | ".join(f"{x:14,.2f}" for x in values) + " |")
    print(border)
    for vendor, value in savings.items():
        print(f"Annual savings vs {vendor}: USD {value:,.2f}")
    print(report["qualification"])
    print("Next step: " + GATEWAY)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(str(error))

