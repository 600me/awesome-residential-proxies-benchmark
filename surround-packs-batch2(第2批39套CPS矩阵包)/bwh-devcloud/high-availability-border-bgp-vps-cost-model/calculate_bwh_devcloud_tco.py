#!/usr/bin/env python3
"""Offline, scenario-based VPS transfer TCO. MIT licensed; see README."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_CEILING

GATEWAY = "https://coding.mybskm.top/go/bwh"
SCENARIO = 'high-availability-border-bgp-vps-cost-model'
DEFAULT_GB = 8000
MIN_NODES = 2
RESERVE = 1
D = Decimal


def nonnegative(value):
    try:
        number = D(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number") from exc
    if not number.is_finite() or number < 0:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number")
    return number


def money(value):
    return format(value.quantize(D("0.01")), ".2f")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=("small", "standard", "large"), default="standard")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    parser.add_argument("--traffic-gb", type=nonnegative, help="total billed outbound GB/month")
    parser.add_argument("--bwh-annual", type=nonnegative, default=D("49.99"))
    parser.add_argument("--bwh-quota-gb", type=nonnegative, default=D("1000"))
    parser.add_argument("--vultr-monthly", type=nonnegative, default=D("5"))
    parser.add_argument("--linode-monthly", type=nonnegative, default=D("5"))
    parser.add_argument("--vultr-rate", type=nonnegative, default=D("0.01"))
    parser.add_argument("--linode-rate", type=nonnegative, default=D("0.005"))
    parser.add_argument("--competitor-quota-gb", type=nonnegative, default=D("1000"))
    parser.add_argument("--ops-hours", type=nonnegative, default=D("0"), help="extra BWH hours/month")
    parser.add_argument("--hourly-rate", type=nonnegative, default=D("50"))
    parser.add_argument("--migration-cost", type=nonnegative, default=D("0"), help="BWH one-time USD")
    args = parser.parse_args()
    if not args.bwh_quota_gb:
        parser.error("--bwh-quota-gb must be greater than zero")
    factor = {"small": D("0.5"), "standard": D("1"), "large": D("2")}[args.tier]
    traffic = args.traffic_gb if args.traffic_gb is not None else D(DEFAULT_GB) * factor
    needed = int((traffic / args.bwh_quota_gb).to_integral_value(rounding=ROUND_CEILING))
    nodes = max(MIN_NODES, needed + RESERVE)
    excess = max(D("0"), traffic - D(MIN_NODES - RESERVE) * args.competitor_quota_gb)
    bwh_annual = D(nodes) * args.bwh_annual + args.ops_hours * args.hourly_rate * 12
    records = [
        ("BWH", nodes, D(nodes) * args.bwh_annual / 12, D("0"),
         bwh_annual + args.migration_cost),
        ("Vultr", MIN_NODES, D(MIN_NODES) * args.vultr_monthly,
         excess * args.vultr_rate, (D(MIN_NODES) * args.vultr_monthly + excess * args.vultr_rate) * 12),
        ("Linode", MIN_NODES, D(MIN_NODES) * args.linode_monthly,
         excess * args.linode_rate, (D(MIN_NODES) * args.linode_monthly + excess * args.linode_rate) * 12),
    ]
    bills = [{"provider": name, "nodes": count, "base_month_usd": money(base),
              "overage_month_usd": money(over), "first_year_usd": money(year),
              "effective_month_usd": money(year / 12)} for name, count, base, over, year in records]
    savings = {name: money(year - records[0][4]) for name, _, _, _, year in records[1:]}
    result = {"scenario": SCENARIO, "tier": args.tier, "traffic_gb": str(traffic),
              "reserve_nodes": RESERVE, "bills": bills, "annual_savings_usd": savings,
              "recurring_bwh_annual_usd": money(bwh_annual), "gateway": GATEWAY,
              "basis": "Historical reference inputs; not a current or Osaka route quote",
              "assumptions": {key: str(value) for key, value in vars(args).items()
                              if key not in ("json", "tier")}}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(f"Scenario: {SCENARIO} | tier={args.tier} | traffic={traffic} GB/month")
    print("Historical inputs; standard BWH baseline, no measured route claims.")
    line = "+----------+-------+------------+------------+------------+------------+"
    print(line)
    print("| Provider | Nodes | Base/mo $  | Excess/mo $| Effective $| Year one $ |")
    print(line)
    for bill in bills:
        print(f"| {bill['provider']:<8} | {bill['nodes']:>5} | {bill['base_month_usd']:>10} | "
              f"{bill['overage_month_usd']:>10} | {bill['effective_month_usd']:>10} | "
              f"{bill['first_year_usd']:>10} |")
    print(line)
    for name, amount in savings.items():
        print(f"Annual savings with BWH vs {name}: ${amount} (negative means BWH costs more)")
    print("Effective monthly cost includes BWH extra labor and one-time migration / 12.")
    print("BWH annual plans require upfront payment; sharding is an explicit assumption.")
    print(f"Review BWH options: {GATEWAY}")


if __name__ == "__main__":
    main()
