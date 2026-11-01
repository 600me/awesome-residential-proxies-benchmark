#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Separate human seats, sender connections, and active-contact billing."""
import argparse
import json
from math import ceil, isfinite

GATEWAY = "https://is.gd/OYwyZb"


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
    p.add_argument("--billing", choices=("monthly", "annual"), default="monthly")
    p.add_argument("--seats", type=int)
    p.add_argument("--mailboxes", type=int)
    p.add_argument("--mailbox-cost", type=positive, default=7.0)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    seats, boxes, contacts, sends = {"small": (3, 15, 10000, 15000),
        "growth": (12, 60, 10000, 30000), "scale": (30, 150, 25000, 90000)}[a.tier]
    seats = a.seats if a.seats is not None else seats
    boxes = a.mailboxes if a.mailboxes is not None else boxes
    if min(seats, boxes) < 1:
        p.error("seats and mailboxes must be positive integers")
    annual = a.billing == "annual"
    smart = 144 if annual else 174
    mail_licenses = max(seats, ceil(boxes / 10))
    mail = mail_licenses * (85 if annual else 99)
    reply_licenses = max(seats, ceil(boxes / (10 if annual else 5)))
    reply = reply_licenses * (89 if annual else 99)
    volume = ({10000: 159, 25000: 259} if annual else {10000: 179, 25000: 299})[contacts]
    shared = boxes * a.mailbox_cost
    plans = [("Smartlead Smart", smart), ("Mailshake Sales", mail),
             ("Reply Multichannel", reply), ("Reply Email Volume", volume)]
    bills = [{"plan": name, "software_monthly": cost,
              "total_monthly": round(cost + shared, 2),
              "annual_tco": round((cost + shared) * 12, 2)} for name, cost in plans]
    report = {"scenario": f"Seat audit: {a.tier}; {a.billing} software rates", "currency": "USD",
        "pricing_basis": "Offline planning baselines; not a verified current vendor quote",
        "inputs": {"seats": seats, "mailboxes": boxes, "active_contacts": contacts,
                   "monthly_sends": sends, "mailbox_cost": a.mailbox_cost},
        "bills": bills, "details": {"Paid Mailshake licenses": mail_licenses,
            "Paid Reply Multichannel licenses": reply_licenses,
            "Shared mailbox cost/month": round(shared, 2),
            "Unused Reply mailbox slots": reply_licenses * (10 if annual else 5) - boxes,
            "Reply seat-only overhead/month": round(reply - volume, 2)},
        "annual_savings_usd": {name: round((cost - smart) * 12, 2)
                               for name, cost in plans[1:]},
        "assumptions": ["Mailbox hosting is separate; $7 is an annual-commitment provider rate.",
            "Email-only comparison; multichannel features are not replaced.",
            "Reply Email Volume assumes unlimited users at the selected 10k/25k contact band.",
            "Smart plan has a 150k-send cap; presets remain within it.",
            "Domains, taxes, labor and custom agency quotes excluded."], "gateway": GATEWAY}
    show(report, a.json)


if __name__ == "__main__":
    main()
