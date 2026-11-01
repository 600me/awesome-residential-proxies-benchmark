#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Audit recurring spend, annual commitments, and migration payback separately."""
import argparse
import json
from math import ceil, isfinite

GATEWAY = "https://is.gd/ttCOOj"


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
    p.add_argument("--billing", choices=("monthly", "annual"), default="annual")
    p.add_argument("--migration-hours", type=positive, default=16)
    p.add_argument("--hourly-rate", type=positive, default=75)
    p.add_argument("--mailbox-cost", type=positive, default=7)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    seats, boxes, contacts, sends = {"small": (3, 20, 10000, 15000),
        "growth": (8, 80, 10000, 60000), "scale": (15, 150, 25000, 120000)}[a.tier]
    annual = a.billing == "annual"
    smart = 144 if annual else 174
    sales = max(seats, ceil(boxes / 10)) * (85 if annual else 99)
    outreach = max(seats, ceil(boxes / 2)) * (45 if annual else 49)
    mail = min(sales, outreach)
    reply = max(seats, ceil(boxes / (10 if annual else 5))) * (89 if annual else 99)
    volume = ({10000: 159, 25000: 259} if annual else {10000: 179, 25000: 299})[contacts]
    host = boxes * a.mailbox_cost
    migration = a.migration_hours * a.hourly_rate
    plans = [("Smartlead Smart", smart), ("Mailshake best public", mail),
             ("Reply Multichannel", reply), ("Reply Email Volume", volume)]
    bills = [{"plan": name, "software_monthly": cost, "total_monthly": cost + host,
              "annual_tco": round((cost + host) * 12 + (migration if i == 0 else 0), 2)}
             for i, (name, cost) in enumerate(plans)]
    savings = {name: round((cost - smart) * 12 - migration, 2) for name, cost in plans[1:]}
    delta = mail - smart
    report = {"scenario": f"Annual audit: {a.tier}; {a.billing} software rates", "currency": "USD",
        "pricing_basis": "Offline planning baselines; not a verified current vendor quote",
        "inputs": {"seats": seats, "mailboxes": boxes, "active_contacts": contacts,
                   "monthly_sends": sends, "migration_hours": a.migration_hours,
                   "hourly_rate": a.hourly_rate, "mailbox_cost": a.mailbox_cost},
        "bills": bills, "details": {"Migration charged to Smartlead first year": migration,
            "Mailshake Outreach alternative/month": outreach,
            "Mailshake Sales alternative/month": sales,
            "Recurring annual saving vs Mailshake": round(delta * 12, 2),
            "Mailshake payback months": round(migration / delta, 2) if delta > 0 else "never",
            "Annual TCO column": "Smartlead includes migration; other plans retain current setup"},
        "annual_savings_usd": savings,
        "assumptions": ["Annual rates are monthly equivalents, not cash payment dates.",
            "Compare Mailshake public tiers by both operator seats and connected mailboxes.",
            "Mailbox hosting uses annual provider commitment regardless of software billing.",
            "Sunk prepaid contracts, domains, taxes, cancellation fees and dual-running excluded.",
            "Email Volume is an email-only alternative, not full multichannel parity."],
        "gateway": GATEWAY}
    show(report, a.json)


if __name__ == "__main__":
    main()
