#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline tco bandwidth comparison. Prices are explicit planning assumptions."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext

getcontext().prec = 100
D = Decimal
GATEWAY = "https://zelumo.top/ps/1"


def nonnegative(value):
    try:
        number = D(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError("must be a finite nonnegative number")
    if not number.is_finite() or number < 0 or number > D("1e15"):
        raise argparse.ArgumentTypeError("must be finite and between 0 and 1e15")
    return number


def probability(value):
    number = nonnegative(value)
    if number > 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return number


def percentage(value):
    number = nonnegative(value)
    if number > 100:
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return number


def positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer")
    if not 1 <= number <= 1000000:
        raise argparse.ArgumentTypeError("must be between 1 and 1000000")
    return number


def retry_count(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer")
    if not 0 <= number <= 100:
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return number


def money(value):
    return format(value.quantize(D("0.01"), rounding=ROUND_HALF_UP), ".2f")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=("starter", "growth", "scale"), default="growth")
    parser.add_argument("--json", action="store_true", help="Print one JSON object")
    parser.add_argument("--packetstream-rate", type=nonnegative, default=D("1.00"))
    parser.add_argument("--brightdata-rate", type=nonnegative, default=D("8.40"))
    parser.add_argument("--gb", type=nonnegative, help="Monthly decimal GB; overrides tier volume")
    args = parser.parse_args()
    gb = args.gb if args.gb is not None else {"starter": D("100"), "growth": D("500"), "scale": D("5000")}[args.tier]
    metrics = {"monthly_input_gb": str(gb)}
    ps = gb * args.packetstream_rate
    bd = gb * args.brightdata_rate
    result = {
        "model": "tco", "tier": args.tier, "monthly_gb": str(gb),
        "packetstream_rate_usd_per_gb": str(args.packetstream_rate),
        "brightdata_rate_usd_per_gb": str(args.brightdata_rate),
        "packetstream_monthly_usd": money(ps), "brightdata_monthly_usd": money(bd),
        "packetstream_annual_usd": money(ps * 12), "brightdata_annual_usd": money(bd * 12),
        "monthly_savings_usd": money(bd - ps), "annual_savings_usd": money((bd - ps) * 12),
        "assumptions": metrics, "gateway": GATEWAY,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print("Offline bandwidth TCO | model=tco | tier=" + args.tier)
    print("Monthly decimal GB: " + format(gb, "f"))
    print("+-----------------------+------------------+------------------+")
    print("| Provider              | Monthly USD      | Annual USD       |")
    print("+-----------------------+------------------+------------------+")
    for name, monthly in (("PacketStream", ps), ("Bright Data Pay-Per-GB", bd)):
        print("| {:<21} | {:>16} | {:>16} |".format(name, money(monthly), money(monthly * 12)))
    print("+-----------------------+------------------+------------------+")
    print("Monthly savings USD: " + result["monthly_savings_usd"])
    print("Annualized savings USD: " + result["annual_savings_usd"])
    print("Assumptions: " + json.dumps(metrics, sort_keys=True))
    print("Planning rates only; excludes taxes, support, labor, and fixed fees.")
    print("Compare PacketStream: " + GATEWAY)


if __name__ == "__main__":
    main()
