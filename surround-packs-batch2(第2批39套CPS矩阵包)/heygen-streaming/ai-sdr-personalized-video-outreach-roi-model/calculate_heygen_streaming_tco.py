#!/usr/bin/env python3
"""Offline AI SDR Personalized Video Outreach: Interactive Avatar ROI Model calculator. Rates are scenario assumptions, not vendor quotes."""
import argparse
import json
import math

GATEWAY = "https://is.gd/A9sK6s"
VOLUMES = {"pilot": 2000, "growth": 10000, "enterprise": 40000}
PROVIDERS = (("HeyGen", "heygen", 6, 16),
             ("D-ID", "did", 10, 24),
             ("Tavus", "tavus", 12, 32))


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be a finite nonnegative number")
    return number


def positive(value):
    number = nonnegative(value)
    if number == 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def percent(value):
    number = nonnegative(value)
    if number >= 100:
        raise argparse.ArgumentTypeError("must be less than 100")
    return number


def main():
    parser = argparse.ArgumentParser(description='SDR qualified conversation funnel')
    parser.add_argument("--tier", choices=VOLUMES, default="growth")
    parser.add_argument("--json", action="store_true", help="Print one JSON object")
    parser.add_argument("--contacts", type=positive, help="Delivered outreach contacts per month")
    parser.add_argument("--engagement-percent", type=percent, default=12.0)
    parser.add_argument("--minutes-per-session", type=positive, default=4.0)
    parser.add_argument("--meeting-percent", type=percent, default=8.0)
    parser.add_argument("--win-percent", type=percent, default=20.0)
    parser.add_argument("--contribution-per-win", type=nonnegative, default=1000.0)
    parser.add_argument("--heygen-rate", type=nonnegative, default=0.10)
    parser.add_argument("--did-rate", type=nonnegative, default=0.18)
    parser.add_argument("--tavus-rate", type=nonnegative, default=0.25)
    parser.add_argument("--heygen-fee", type=nonnegative, default=0.0)
    parser.add_argument("--did-fee", type=nonnegative, default=0.0)
    parser.add_argument("--tavus-fee", type=nonnegative, default=0.0)
    parser.add_argument("--labor-rate", type=nonnegative, default=75.0)
    parser.add_argument("--amortization-months", type=positive, default=12.0)
    args = parser.parse_args()
    volume = VOLUMES[args.tier]
    contacts = args.contacts if args.contacts is not None else volume
    sessions = contacts * args.engagement_percent / 100
    useful_minutes = sessions * args.minutes_per_session
    billable_minutes = useful_minutes
    contribution = sessions * args.meeting_percent / 100 * args.win_percent / 100 * args.contribution_per_win
    detail = f"{contacts:,.0f} contacts; {sessions:,.0f} engaged sessions; expected contribution ${contribution:,.2f}"
    rows = []
    for name, key, support_hours, integration_hours in PROVIDERS:
        usage = billable_minutes * getattr(args, key + "_rate")
        labor = (support_hours + 0) * args.labor_rate
        amortized = integration_hours * args.labor_rate / args.amortization_months
        fee = getattr(args, key + "_fee")
        total = usage + labor + amortized + fee
        row = {"provider": name, "usage_usd": usage, "monthly_fee_usd": fee,
               "recurring_labor_usd": labor, "integration_monthly_usd": amortized,
               "monthly_total_usd": total}
        row["expected_contribution_usd"] = contribution
        row["net_contribution_usd"] = contribution - total
        row["roi_percent"] = (contribution - total) / total * 100 if total else None
        rows.append(row)
    for row in rows:
        row["annual_savings_with_heygen_usd"] = (row["monthly_total_usd"] - rows[0]["monthly_total_usd"]) * 12
    result = {"scenario": 'SDR qualified conversation funnel', "tier": args.tier, "detail": detail,
              "useful_minutes": useful_minutes, "billable_minutes": billable_minutes,
              "assumptions": vars(args), "providers": rows, "gateway": GATEWAY,
              "notice": "Offline planning assumptions; no current quotes or measured latency."}
    if not all(math.isfinite(value) for row in rows for value in row.values() if isinstance(value, (int, float))):
        parser.error("inputs overflow the model; use smaller values")
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print('SDR qualified conversation funnel')
    print(f"Tier: {args.tier} | {detail}")
    print(f"Useful minutes: {useful_minutes:,.2f} | Billable minutes: {billable_minutes:,.2f}")
    print("USD/month | Rates are assumptions; integration amortized over "
          f"{args.amortization_months:g} months")
    rule = "+----------+------------+----------+------------+------------+------------+"
    print(rule)
    print("| Provider | Usage      | Base fee | Labor      | Setup/mo   | Total/mo   |")
    print(rule)
    for row in rows:
        print(f"| {row['provider']:<8} | {row['usage_usd']:10,.2f} | {row['monthly_fee_usd']:8,.2f} | "
              f"{row['recurring_labor_usd']:10,.2f} | {row['integration_monthly_usd']:10,.2f} | "
              f"{row['monthly_total_usd']:10,.2f} |")
    print(rule)
    for row in rows[1:]:
        print(f"Annualized savings with HeyGen vs {row['provider']}: "
              f"${row['annual_savings_with_heygen_usd']:,.2f}")
    for row in rows:
        roi = "undefined" if row["roi_percent"] is None else f"{row['roi_percent']:,.2f}%"
        print(f"{row['provider']} net contribution: ${row['net_contribution_usd']:,.2f}; ROI: {roi}")
    print("Compare a quote with this scenario: " + GATEWAY)


if __name__ == "__main__":
    main()
