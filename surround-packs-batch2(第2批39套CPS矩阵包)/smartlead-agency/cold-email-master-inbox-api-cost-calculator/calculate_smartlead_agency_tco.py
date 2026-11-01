#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline scenario calculator; historical price anchors, not current quotes.
No network calls, credentials, mailbox provisioning, or deliverability claims.
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/RcXkVf"
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
    parser.add_argument("--events", type=positive_int)
    parser.add_argument("--exception-rate", type=nonnegative, default=0.10)
    parser.add_argument("--smart-seconds", type=nonnegative, default=15)
    parser.add_argument("--apollo-seconds", type=nonnegative, default=45)
    parser.add_argument("--wood-seconds", type=nonnegative, default=30)
    parser.add_argument("--poll-minutes", type=positive_int, default=5)
    parser.add_argument("--campaigns", type=positive_int, default=40)
    parser.add_argument("--pages", type=positive_int, default=2)
    parser.add_argument("--hosting", type=nonnegative, default=30)
    parser.add_argument("--apollo-portal", type=nonnegative, default=200)
    args = parser.parse_args()
    if args.exception_rate > 1:
        parser.error("--exception-rate must be between 0 and 1")
    presets = {"pilot": (3, 3000, 20, 2, 99),
               "growth": (8, 12000, 80, 4, 188),
               "scale": (20, 40000, 200, 8, 587)}
    c, e, mailboxes, seats, w = presets[args.tier]
    clients, events = args.clients or c, args.events or e
    sends, domains = mailboxes * 600, math.ceil(mailboxes / 3)
    plan, platform, workspaces = smart_plan(sends, math.ceil(sends / 3), clients, args.smart_client_fee,
                                            (args.smart_pro_price, args.smart_scale_price, args.smart_prime_price))
    wood_base = w if args.wood_base is None else args.wood_base
    portal, hosting = args.apollo_portal, args.hosting
    infrastructure = mailboxes * args.mailbox_price + domains * args.domain_year / 12
    exceptions = events * args.exception_rate
    hours = tuple(exceptions * s / 3600 for s in
                  (args.smart_seconds, args.apollo_seconds, args.wood_seconds))
    polls = math.ceil(1440 / args.poll_minutes) * 30 * args.campaigns * args.pages
    metrics = {"reply_events": events, "modeled_exceptions": exceptions,
               "poll_requests_per_month": polls,
               "webhook_requests_before_retries": events,
               "requests_avoided": polls - events, "monthly_sends": sends}

    SCENARIO = "Master inbox exception labor and API request budget"
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

