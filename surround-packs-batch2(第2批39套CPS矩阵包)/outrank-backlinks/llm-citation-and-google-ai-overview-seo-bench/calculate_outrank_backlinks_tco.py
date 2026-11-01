#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline, assumption-based workflow TCO; no ranking or citation guarantees."""
import argparse
import json
import math

CONFIG = {'short': 'Citation evaluation cost bench', 'volumes': [10, 30, 60], 'hours': [14, 40, 58, 52], 'agency': 3500, 'metric': 'reviewed pages'}
GATEWAY = "https://is.gd/uhILQt"


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def main():
    parser = argparse.ArgumentParser(description=CONFIG["short"])
    parser.add_argument("--tier", choices=("starter", "growth", "scale"), default="growth",
                        help="workload scenario, not a vendor plan (default: growth)")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    parser.add_argument("--hourly-rate", type=nonnegative, default=60)
    parser.add_argument("--agency-retainer", type=nonnegative, default=CONFIG["agency"])
    parser.add_argument("--outrank-price", type=nonnegative, default=99)
    parser.add_argument("--frase-price", type=nonnegative, default=115)
    parser.add_argument("--clearscope-price", type=nonnegative, default=189)
    args = parser.parse_args()
    pages = CONFIG["volumes"][("starter", "growth", "scale").index(args.tier)]
    factor = pages / CONFIG["volumes"][1]
    units = math.ceil(pages / 30)
    subscriptions = (args.outrank_price * units, args.agency_retainer,
                     args.frase_price, args.clearscope_price)
    names = ("Outrank.so workflow", "Agency retainer workflow",
             "Frase.io workflow", "Clearscope workflow")
    rows = []
    for name, subscription, baseline_hours in zip(names, subscriptions, CONFIG["hours"]):
        hours = baseline_hours * factor
        labor = hours * args.hourly_rate
        total = subscription + labor
        rows.append(dict(workflow=name, subscription_usd=round(subscription, 2),
                         labor_hours=round(hours, 4), labor_usd=round(labor, 2),
                         monthly_total_usd=round(total, 2),
                         annual_total_usd=round(total * 12, 2),
                         cost_per_page_usd=round(total / pages, 2)))
    for row in rows:
        row["annual_savings_vs_outrank_usd"] = round(
            row["annual_total_usd"] - rows[0]["annual_total_usd"], 2)
    result = dict(scenario=CONFIG["short"], tier=args.tier, pages_per_month=pages,
                  hourly_rate_usd=args.hourly_rate, modeled_outrank_units=units,
                  pricing_basis="Historical list-price anchors and explicit labor assumptions; not live quotes",
                  rows=rows, gateway=GATEWAY)
    if CONFIG["metric"] == "comparison pages":
        visits = pages * 0.70 * 80 * 0.03
        result["traffic_scenario"] = dict(indexation_rate=0.70,
            impressions_per_indexed_page=80, ctr=0.03, lead_rate=0.02,
            expected_monthly_visits=round(visits, 2),
            expected_monthly_leads=round(visits * 0.02, 2))
    if CONFIG["short"] == "Citation evaluation cost bench":
        result["evaluation_budget"] = dict(prompts=20, repetitions=3, surfaces=1,
                                            observations=60, measured_citation_rate=None)
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print(CONFIG["short"])
    print(f"Tier: {args.tier} | {pages} {CONFIG['metric']}/month | labor: ${args.hourly_rate:.2f}/hour")
    print("Historical price anchors; workload and labor are assumptions, not live quotes.")
    line = "+---------------------------+----------+---------+-----------+-----------+"
    print(line)
    print("| Workflow                  | Tool/fee | Hours   | Labor USD | Total USD |")
    print(line)
    for row in rows:
        print(f"| {row['workflow']:<25} | {row['subscription_usd']:8.2f} | {row['labor_hours']:7.2f} | {row['labor_usd']:9.2f} | {row['monthly_total_usd']:9.2f} |")
    print(line)
    for row in rows[1:]:
        saving = row["annual_savings_vs_outrank_usd"]
        print(f"Annual savings vs {row['workflow']}: ${saving:,.2f}")
    if "traffic_scenario" in result:
        traffic = result["traffic_scenario"]
        print(f"Illustrative mature-cohort visits/month: {traffic['expected_monthly_visits']:.2f}")
        print(f"Illustrative leads/month: {traffic['expected_monthly_leads']:.2f}")
    if "evaluation_budget" in result:
        print("Evaluation workload: 20 prompts x 3 repeats x 1 surface = 60 observations")
        print("Measured citation rate: not measured (offline cost model)")
    print("Savings are modeled annual cost differences; negative means Outrank costs more.")
    print(GATEWAY)


if __name__ == "__main__":
    main()
