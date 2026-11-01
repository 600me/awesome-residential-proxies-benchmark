#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Coupon and renewal economics: offline scenario calculator, not a live price or IP test."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

GATEWAY = "https://coding.mybskm.top/go/lisahost"
DEFAULT_UNITS = 12
TIERS = {"pilot": max(1, DEFAULT_UNITS // 4), "team": DEFAULT_UNITS,
         "scale": DEFAULT_UNITS * 3}


def nonnegative(value):
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number") from exc
    if not number.is_finite() or number < 0 or number > Decimal("1e12"):
        raise argparse.ArgumentTypeError("number must be finite and between 0 and 1e12")
    return number


def positive_int(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive integer") from exc
    if not 1 <= number <= 1000000:
        raise argparse.ArgumentTypeError("units must be between 1 and 1000000")
    return number


def money(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="team",
                        help="workload count preset: pilot, team (default), scale")
    parser.add_argument("--units", type=positive_int, help="override tier workload count")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    defaults = {
        "gb-per-unit": "8", "proxy-ip-price": "6", "proxy-gb-price": "2.50",
        "proxy-compute": "8", "vps-price": "16", "included-gb": "100",
        "vps-gb-price": "0.02", "broker-fee": "25",
        "proxy-admin-hours": "3", "vps-admin-hours": "1",
        "hourly-rate": "30", "coupon-percent": "0", "setup-fee": "0",
    }
    for name, default in defaults.items():
        parser.add_argument("--" + name, type=nonnegative, default=Decimal(default),
                            help="scenario assumption (default: %(default)s)")
    args = parser.parse_args()
    if args.coupon_percent > 100:
        parser.error("--coupon-percent must be between 0 and 100")
    units = args.units if args.units is not None else TIERS[args.tier]
    count = Decimal(units)
    broker = [count * args.proxy_ip_price, count * args.gb_per_unit * args.proxy_gb_price,
              count * args.proxy_compute, args.broker_fee,
              args.proxy_admin_hours * args.hourly_rate]
    vps = [count * args.vps_price * (1 - args.coupon_percent / 100),
           count * max(Decimal(0), args.gb_per_unit - args.included_gb) * args.vps_gb_price,
           Decimal(0), Decimal(0), args.vps_admin_hours * args.hourly_rate]
    broker = list(map(money, broker))
    vps = list(map(money, vps))
    labels = ["Exit / VPS rental", "Traffic overage", "Separate compute", "Broker fee", "Admin labor"]
    monthly_broker, monthly_vps = sum(broker), sum(vps)
    saving = monthly_broker - monthly_vps
    setup = money(args.setup_fee)
    annual_saving = saving * 12 - setup
    assumptions = {key: str(getattr(args, key.replace("-", "_"))) for key in defaults}
    result = {
        "scenario": "Coupon and renewal economics", "price_status": "unverified editable assumptions; USD",
        "tier": args.tier, "units": units, "assumptions": assumptions,
        "line_items": {label: {"broker_usd": str(b), "lisahost_usd": str(v)}
                       for label, b, v in zip(labels, broker, vps)},
        "broker_monthly_usd": str(monthly_broker), "lisahost_monthly_usd": str(monthly_vps),
        "broker_year_one_usd": str(monthly_broker * 12),
        "lisahost_year_one_usd": str(monthly_vps * 12 + setup),
        "monthly_savings_usd": str(saving), "annual_savings_usd": str(annual_saving),
        "gateway": GATEWAY,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print("Coupon and renewal economics")
    print(f"USD assumptions only | tier={args.tier} | workloads={units}")
    rule = "+------------------------+----------------+----------------+"
    print(rule)
    print(f"| {'Monthly item':<22} | {'ISP broker':>14} | {'LisaHost VPS':>14} |")
    print(rule)
    for label, b, v in zip(labels + ["TOTAL"], broker + [monthly_broker], vps + [monthly_vps]):
        print(f"| {label:<22} | ${b:>13,.2f} | ${v:>13,.2f} |")
    print(rule)
    print(f"Monthly savings: ${saving:,.2f}")
    print(f"Year-one migration/setup: ${setup:,.2f}")
    print(f"Annualized savings (year one): ${annual_saving:,.2f}")
    print("Coupon assumes 12 eligible months; taxes and FX excluded.")
    print("Verify plan terms and assigned IP before purchase: " + GATEWAY)


if __name__ == "__main__":
    main()
