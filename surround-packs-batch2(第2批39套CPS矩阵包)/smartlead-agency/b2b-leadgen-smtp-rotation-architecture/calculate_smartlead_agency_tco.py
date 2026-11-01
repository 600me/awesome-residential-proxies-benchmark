#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline scenario calculator; historical price anchors, not current quotes.
No network calls, credentials, mailbox provisioning, or deliverability claims.
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/mOnQZD"
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
    parser.add_argument("--clients", type=positive_int)
    parser.add_argument("--sends", type=positive_int)
    parser.add_argument("--daily-cap", type=positive_int, default=30)
    parser.add_argument("--send-days", type=positive_int, default=20)
    parser.add_argument("--reserve", type=nonnegative, default=0.20)
    parser.add_argument("--operators", type=positive_int)
    parser.add_argument("--smtp-per-seat", type=positive_int, default=5)
    parser.add_argument("--smart-hours", type=nonnegative, default=6)
    parser.add_argument("--apollo-hours", type=nonnegative, default=12)
    parser.add_argument("--wood-hours", type=nonnegative, default=8)
    args = parser.parse_args()
    if args.reserve >= 1:
        parser.error("--reserve must be below 1")
    presets = {"pilot": (3, 18000, 2, 99),
               "growth": (10, 120000, 5, 329),
               "scale": (25, 300000, 10, 900)}
    c, s, o, w = presets[args.tier]
    clients, sends = args.clients or c, args.sends or s
    healthy = math.ceil(sends / (args.daily_cap * args.send_days))
    mailboxes = math.ceil(healthy / (1 - args.reserve))
    domains = math.ceil(mailboxes / 3)
    seats = max(args.operators or o, math.ceil(mailboxes / args.smtp_per_seat))
    plan, platform, workspaces = smart_plan(sends, math.ceil(sends / 3), clients, args.smart_client_fee,
                                            (args.smart_pro_price, args.smart_scale_price, args.smart_prime_price))
    wood_base = w if args.wood_base is None else args.wood_base
    portal, hosting = 0, 0
    infrastructure = mailboxes * args.mailbox_price + domains * args.domain_year / 12
    hours = (args.smart_hours, args.apollo_hours, args.wood_hours)
    metrics = {"monthly_sends": sends, "healthy_mailboxes_needed": healthy,
               "provisioned_mailboxes": mailboxes, "reserve_mailboxes": mailboxes - healthy,
               "domains": domains, "apollo_smtp_seats": seats,
               "capacity_after_reserve": int(mailboxes * (1 - args.reserve)
                                           * args.daily_cap * args.send_days)}

    SCENARIO = "SMTP rotation capacity and failure reserve architecture"
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

