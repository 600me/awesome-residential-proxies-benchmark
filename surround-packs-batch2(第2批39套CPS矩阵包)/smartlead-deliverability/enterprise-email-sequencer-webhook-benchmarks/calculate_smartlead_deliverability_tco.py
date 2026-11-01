#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline webhook capacity and integration TCO model; no live vendor benchmark."""
import argparse
import json
from math import ceil, isfinite

GATEWAY = "https://is.gd/qWLFKo"


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
    p.add_argument("--events-per-send", type=positive, default=1.5)
    p.add_argument("--retry-rate", type=float, default=0.1)
    p.add_argument("--burst-minutes", type=positive, default=15)
    p.add_argument("--worker-ms", type=positive, default=200)
    p.add_argument("--headroom", type=positive, default=2)
    p.add_argument("--hourly-rate", type=positive, default=75)
    p.add_argument("--smart-hours", type=positive, default=6)
    p.add_argument("--mailshake-hours", type=positive, default=6)
    p.add_argument("--reply-hours", type=positive, default=6)
    p.add_argument("--infra-monthly", type=positive, default=50)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if not isfinite(a.retry_rate) or not 0 <= a.retry_rate <= 1 or a.headroom < 1:
        p.error("retry-rate must be in [0,1]; headroom must be >= 1")
    seats, boxes, contacts, sends = {"small": (3, 20, 10000, 15000),
        "growth": (10, 100, 25000, 90000), "scale": (20, 200, 50000, 150000)}[a.tier]
    smart = 174
    mail = min(max(seats, ceil(boxes / 10)) * 99, max(seats, ceil(boxes / 2)) * 49)
    reply = {10000: 179, 25000: 299, 50000: 499}[contacts]
    attempts = ceil(sends * a.events_per_send * (1 + a.retry_rate))
    rps = attempts / (a.burst_minutes * 60)
    workers = ceil(rps * a.worker_ms / 1000 * a.headroom)
    shared = boxes * 7 + a.infra_monthly
    plans = [("Smartlead Smart", smart, a.smart_hours),
             ("Mailshake best public", mail, a.mailshake_hours),
             ("Reply Email Volume", reply, a.reply_hours)]
    bills = [{"plan": name, "software_monthly": cost,
              "total_monthly": round(cost + shared + hours * a.hourly_rate, 2),
              "annual_tco": round((cost + shared + hours * a.hourly_rate) * 12, 2)}
             for name, cost, hours in plans]
    baseline = bills[0]["annual_tco"]
    report = {"scenario": f"Offline webhook model: {a.tier}; {sends} sends/month", "currency": "USD",
        "pricing_basis": "Offline planning baselines; not a verified current vendor quote",
        "inputs": vars(a), "bills": bills,
        "details": {"Monthly delivery attempts incl. retries": attempts,
            "Burst ingress requests/second": round(rps, 2), "Worker concurrency required": workers,
            "Labor/month Smartlead": round(a.smart_hours * a.hourly_rate, 2),
            "Labor/month Mailshake": round(a.mailshake_hours * a.hourly_rate, 2),
            "Labor/month Reply": round(a.reply_hours * a.hourly_rate, 2),
            "Equal-labor annual saving vs Mailshake": round((mail - smart) * 12, 2),
            "Equal-labor annual saving vs Reply": round((reply - smart) * 12, 2)},
        "annual_savings_usd": {b["plan"]: round(b["annual_tco"] - baseline, 2) for b in bills[1:]},
        "assumptions": ["No network calls or measured latency; all event rates are scenario inputs.",
            "One additional attempt per retried event; sustained failure is not modeled.",
            "Labor hours are user estimates, not measured vendor performance.",
            "Whole-month attempts arrive in one burst; deliberately severe receiver-sizing case.",
            "Smart API access and webhook entitlements must be confirmed for your contract.",
            "Mailbox hosting at annual provider rate; domains, tax and migration excluded."],
        "gateway": GATEWAY}
    show(report, a.json)


if __name__ == "__main__":
    main()
