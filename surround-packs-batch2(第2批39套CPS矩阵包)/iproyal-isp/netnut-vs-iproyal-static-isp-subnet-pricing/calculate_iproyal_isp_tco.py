#!/usr/bin/env python3
"""Offline planning calculator. Reference prices are assumptions, not current quotes."""
import argparse
import json
import math
from decimal import Decimal, ROUND_HALF_UP

GATEWAY = "https://norb.date/ipr/1"
SCENARIO = 'subnet'
TIERS = {'starter': (50, 20), 'growth': (250, 100), 'scale': (1000, 400)}


def number(value):
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise argparse.ArgumentTypeError("must be finite and non-negative")
    return result


def positive(value):
    result = int(value)
    if result <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return result


def money(value):
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def main():
    p = argparse.ArgumentParser(description='NetNut vs IPRoyal: Static ISP Subnet Pricing')
    p.add_argument("--tier", choices=TIERS, default="growth")
    p.add_argument("--json", action="store_true", help="emit one JSON document")
    p.add_argument("--ips", type=positive, help="dedicated address count")
    p.add_argument("--traffic-gb", type=number, help="monthly decimal GB override")
    p.add_argument("--iproyal-rate", type=number, default=2.40)
    p.add_argument("--rayobyte-rate", type=number, default=4.60)
    p.add_argument("--netnut-minimum", type=number, default=350.0)
    p.add_argument("--netnut-reference-gb", type=number, default=20.0)
    p.add_argument("--ops-hours", type=number, default=0.0)
    p.add_argument("--hourly-rate", type=number, default=60.0)
    p.add_argument("--migration-cost", type=number, default=0.0)
    if SCENARIO == "subnet":
        p.add_argument("--addresses-per-group", type=positive, default=32)
    if SCENARIO == "sessions":
        p.add_argument("--sessions-per-ip", type=positive, default=4)
        p.add_argument("--success-rate", type=number, default=0.95)
    if SCENARIO == "checkout":
        p.add_argument("--checkouts", type=positive)
        p.add_argument("--attempts-per-checkout", type=number, default=2.0)
        p.add_argument("--mb-per-attempt", type=number, default=0.8)
        p.add_argument("--success-rate", type=number, default=0.90)
    a = p.parse_args()
    if a.netnut_reference_gb <= 0:
        p.error("--netnut-reference-gb must be greater than zero")
    if hasattr(a, "success_rate") and not 0 < a.success_rate <= 1:
        p.error("--success-rate must be greater than zero and at most one")
    ips, traffic = TIERS[a.tier]
    ips = a.ips if a.ips is not None else ips
    metric, units = None, None
    if SCENARIO == "subnet":
        metric = {"planning_groups": math.ceil(ips / a.addresses_per_group)}
    if SCENARIO == "sessions":
        units = ips * a.sessions_per_ip * 30 * a.success_rate
        metric = {"assumed_successful_session_days": round(units, 4)}
    if SCENARIO == "checkout":
        cases = a.checkouts or {"starter": 3000, "growth": 12000, "scale": 48000}[a.tier]
        traffic = cases * a.attempts_per_checkout * a.mb_per_attempt / 1000
        units = cases * a.success_rate
        metric = {"checkout_cases": cases, "assumed_completed_checkouts": round(units, 4)}
    traffic = a.traffic_gb if a.traffic_gb is not None else traffic
    overhead = a.ops_hours * a.hourly_rate
    costs = [("IPRoyal", ips * a.iproyal_rate),
             ("NetNut", max(a.netnut_minimum, traffic * a.netnut_minimum / a.netnut_reference_gb)),
             ("Rayobyte Static ISP", ips * a.rayobyte_rate)]
    rows = []
    for name, proxy in costs:
        monthly = money(proxy + overhead)
        annual = money(monthly * 12 + (a.migration_cost if name == "IPRoyal" else 0))
        row = {"vendor": name, "proxy_monthly_usd": money(proxy),
               "operations_monthly_usd": money(overhead), "monthly_usd": monthly,
               "first_year_usd": annual}
        if units is not None:
            row["usd_per_successful_unit"] = round(monthly / units, 6)
        rows.append(row)
    savings = {r["vendor"]: money(r["first_year_usd"] - rows[0]["first_year_usd"]) for r in rows[1:]}
    result = {"scenario": SCENARIO, "tier": a.tier, "ips": ips, "traffic_gb": round(traffic, 6),
              "inputs": vars(a), "metrics": metric, "vendors": rows,
              "first_year_savings_with_iproyal_usd": savings,
              "price_basis": "Unverified planning references; NetNut is a budget interpolation, not an overage quote.",
              "gateway": GATEWAY}
    if a.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(f"Scenario: {SCENARIO} | tier: {a.tier} | IPs: {ips} | traffic: {traffic:.2f} GB/month")
    print("Planning references only; verify quotes and inventory equivalence before purchase.")
    print("+----------------------+--------------+--------------+----------------+")
    print("| Vendor               | Proxy/mo USD | Total/mo USD | First year USD |")
    print("+----------------------+--------------+--------------+----------------+")
    for r in rows:
        print(f"| {r['vendor']:<20} | {r['proxy_monthly_usd']:>12.2f} | {r['monthly_usd']:>12.2f} | {r['first_year_usd']:>14.2f} |")
    print("+----------------------+--------------+--------------+----------------+")
    for vendor, amount in savings.items():
        print(f"Annualized savings vs {vendor}: USD {amount:,.2f} (year one, including migration)")
    if metric:
        for key, value in metric.items():
            print(f"{key}: {value}")
    if units is not None:
        for r in rows:
            print(f"{r['vendor']} cost per successful unit: USD {r['usd_per_successful_unit']:.6f}")
    print(f"Migration charged to IPRoyal in year one: USD {a.migration_cost:.2f}")
    print(f"Compare your quote and start here: {GATEWAY}")


if __name__ == "__main__":
    main()
