#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Size a mixed-provider pool after warmup reservations and availability loss."""
import argparse
import json
from math import ceil, isfinite

GATEWAY = "https://is.gd/15s7By"


def positive(value):
    number = float(value)
    if not isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be a finite number greater than zero")
    return number


def show(report, as_json):
    if as_json:
        print(json.dumps(report, indent=2, allow_nan=False))
        return
    print(report["scenario"])
    print("+-------------------------+-------------+-------------+-------------+")
    print("| Platform / plan         | Software/mo | Total/mo    | Annual TCO  |")
    print("+-------------------------+-------------+-------------+-------------+")
    for row in report["bills"]:
        print(f"| {row['plan']:<23} | {row['software_monthly']:>11.2f} | {row['total_monthly']:>11.2f} | {row['annual_tco']:>11.2f} |")
    print("+-------------------------+-------------+-------------+-------------+")
    for key, value in report["details"].items():
        print(f"{key}: {value}")
    for key, value in report["annual_savings_usd"].items():
        print(f"Annual savings vs {key}: ${value:,.2f}")
    print("USD; offline planning baselines. Verify rates and entitlements before purchase.")
    print(GATEWAY)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tier", choices=("small", "growth", "scale"), default="growth")
    p.add_argument("--target", type=int)
    p.add_argument("--days", type=int, default=22)
    p.add_argument("--daily-budget", type=int, default=50)
    p.add_argument("--warmup", type=int, default=20)
    p.add_argument("--availability", type=positive, default=0.8)
    p.add_argument("--google-share", type=float, default=0.6)
    p.add_argument("--google-cost", type=positive, default=7)
    p.add_argument("--outlook-cost", type=positive, default=7)
    p.add_argument("--domain-year", type=positive, default=13)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    target = a.target if a.target is not None else {"small": 15000, "growth": 40000, "scale": 90000}[a.tier]
    if target < 1 or a.days not in range(1, 32) or a.warmup < 0 or a.daily_budget <= a.warmup:
        p.error("positive target, days 1..31, and daily-budget > warmup >= 0 required")
    if a.availability > 1 or not isfinite(a.google_share) or not 0 <= a.google_share <= 1:
        p.error("availability must be <= 1 and google-share must be in [0,1]")
    contacts = ceil(target / 3)
    if contacts > 50000 or target > 150000:
        p.error("model supports at most 50k active contacts and 150k monthly sends")
    boxes = ceil(target / (a.days * (a.daily_budget - a.warmup) * a.availability))
    google = ceil(boxes * a.google_share)
    outlook = boxes - google
    domains = ceil(boxes / 3)
    host = google * a.google_cost + outlook * a.outlook_cost
    shared = host + domains * a.domain_year / 12
    mail = min(max(4, ceil(boxes / 10)) * 99, max(4, ceil(boxes / 2)) * 49)
    volume = next(cost for limit, cost in [(10000, 179), (25000, 299), (50000, 499)] if contacts <= limit)
    smart = 174
    plans = [("Smartlead Smart", smart), ("Mailshake best public", mail), ("Reply Email Volume", volume)]
    report = {"scenario": f"Warmup pool: {target} sends/month; {a.tier}", "currency": "USD",
        "pricing_basis": "Offline planning baselines; not a verified current vendor quote",
        "inputs": vars(a), "bills": [{"plan": name, "software_monthly": cost,
            "total_monthly": round(cost + shared, 2), "annual_tco": round((cost + shared) * 12, 2)}
            for name, cost in plans],
        "details": {"Required real mailboxes": boxes, "Google mailboxes": google,
            "Outlook mailboxes": outlook, "Domains at 3 mailboxes/domain": domains,
            "Modeled active contacts (3 sends/contact)": contacts,
            "Shared hosting/month": round(host, 2), "Shared domains/month": round(shared - host, 2),
            "Pool capacity/month": round(boxes * a.days * (a.daily_budget - a.warmup) * a.availability),
            "Cold capacity lost if warmup ignored/month": round(boxes * a.days * a.warmup * a.availability)},
        "annual_savings_usd": {name: round((cost - smart) * 12, 2) for name, cost in plans[1:]},
        "assumptions": ["50 total messages/day is a scenario ceiling, not an ESP permission.",
            "Warmup has reserved capacity; no deliverability uplift is priced in.",
            "Google Starter and Microsoft Basic with Teams use annual provider rates.",
            "$13/domain/year is a planning assumption; replace with registrar quote.",
            "Four human operators; mailbox capacity determines extra Mailshake licenses.",
            "Labor, tax, provider limits and ramp-up duration require separate validation."],
        "gateway": GATEWAY}
    show(report, a.json)


if __name__ == "__main__":
    main()
