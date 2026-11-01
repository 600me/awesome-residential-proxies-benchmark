#!/usr/bin/env python3
"""Offline Multi-Network Cost Sync Automation Model. All workflow assumptions are editable scenarios."""
import argparse
import json
import math

GATEWAY = "https://norb.date/v/2"
MODE = "sync"
BRANDS = ("Voluum", "ClickMagick", "Hyros")
TIERS = {"starter": (100000, 10000, 1), "growth": (1000000, 50000, 1),
         "scale": (5000000, 200000, 2)}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def fraction(value):
    number = nonnegative(value)
    if number > 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return number


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tier", choices=TIERS, default="growth")
    p.add_argument("--json", action="store_true", help="emit one JSON object")
    p.add_argument("--clicks", type=nonnegative, help="monthly paid clicks")
    p.add_argument("--ad-spend", type=nonnegative, help="monthly USD spend")
    p.add_argument("--hourly-rate", type=nonnegative, default=75)
    p.add_argument("--conversion-rate", type=fraction, default=0.02)
    p.add_argument("--payout", type=nonnegative, default=20)
    p.add_argument("--loss-per-second", type=fraction, default=0.02)
    p.add_argument("--bot-share", type=fraction, default=0.10)
    p.add_argument("--error-share", type=fraction, default=0.01)
    for key, fee, hours in (("voluum", 349, 4), ("clickmagick", 299, 14),
                            ("hyros", 199, 16)):
        p.add_argument("--" + key + "-fee", type=nonnegative, default=fee)
        p.add_argument("--" + key + "-hours", type=nonnegative, default=hours)
        p.add_argument("--" + key + "-capacity", type=nonnegative, default=0)
        p.add_argument("--" + key + "-delay-ms", type=nonnegative, default=100)
        p.add_argument("--" + key + "-preventable", type=fraction, default=0.30)
    a = p.parse_args()
    clicks, spend, labor_multiplier = TIERS[a.tier]
    clicks = clicks if a.clicks is None else a.clicks
    spend = spend if a.ad_spend is None else a.ad_spend
    rows = []
    for brand in BRANDS:
        key = brand.lower()
        fee = getattr(a, key + "_fee")
        labor = getattr(a, key + "_hours") * labor_multiplier * a.hourly_rate
        capacity = getattr(a, key + "_capacity")
        if MODE == "redirect":
            delay = getattr(a, key + "_delay_ms")
            loss = clicks * a.conversion_rate * a.payout * min(1, delay / 1000 * a.loss_per_second)
        elif MODE == "fraud":
            loss = spend * a.bot_share * (1 - getattr(a, key + "_preventable"))
        elif MODE == "sync":
            loss = spend * a.error_share
        else:
            loss = 0.0
        total = fee + labor + capacity + loss
        if not all(math.isfinite(x) for x in (labor, loss, total, total * 12)):
            p.error("inputs overflow the USD calculation; use smaller values")
        rows.append(dict(brand=brand, fee_usd=fee, labor_usd=labor,
                         capacity_usd=capacity, loss_usd=loss, monthly_usd=total))
    savings = {r["brand"]: 12 * (r["monthly_usd"] - rows[0]["monthly_usd"])
               for r in rows[1:]}
    result = dict(mode=MODE, tier=a.tier, monthly_clicks=clicks, ad_spend_usd=spend,
                  assumptions=vars(a), rows=rows, annual_savings_usd=savings,
                  gateway=GATEWAY, price_status="unverified historical anchors; replace with quotes")
    if a.json:
        print(json.dumps(result, indent=2, allow_nan=False))
    else:
        print("Multi-Network Cost Sync Automation Model | tier=" + a.tier)
        print("USD/month; historical price anchors + hypothetical workflow inputs")
        print("+-------------+-----------+-----------+-----------+-----------+------------+")
        print("| Brand       | Fee       | Labor     | Capacity  | Loss      | Total      |")
        print("+-------------+-----------+-----------+-----------+-----------+------------+")
        for r in rows:
            print("| {:<11} | {:>9.2f} | {:>9.2f} | {:>9.2f} | {:>9.2f} | {:>10.2f} |".format(
                r["brand"], r["fee_usd"], r["labor_usd"], r["capacity_usd"], r["loss_usd"], r["monthly_usd"]))
        print("+-------------+-----------+-----------+-----------+-----------+------------+")
        for brand, amount in savings.items():
            print("Annual modeled savings with Voluum vs {}: ${:,.2f}".format(brand, amount))
        print("Negative savings mean Voluum costs more under your assumptions.")
        print(GATEWAY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
