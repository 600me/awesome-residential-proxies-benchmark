#!/usr/bin/env python3
"""Synthesia Enterprise vs HeyGen API: Credit and Capacity Audit: offline planning; historical prices, not live quotes.
MIT licensed. No network, credentials, paid jobs, or third-party packages.
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/6STXXJ"
TIERS = {"small": 100, "standard": 600, "scale": 1800}
UGC = False
ENTERPRISE = True


def number(value):
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise argparse.ArgumentTypeError("use a finite nonnegative number")
    return result


def positive(value):
    result = number(value)
    if result == 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return result


def count(value):
    result = int(value)
    if result < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return result


def main():
    p = argparse.ArgumentParser(description='Enterprise credit audit')
    p.add_argument("--tier", choices=TIERS, default="standard")
    p.add_argument("--json", action="store_true", help="emit one JSON object")
    if UGC:
        p.add_argument("--clips", type=count, help="source clips; overrides tier")
        p.add_argument("--clip-seconds", type=positive, default=30)
    else:
        p.add_argument("--source-minutes", type=positive, help="overrides tier")
    p.add_argument("--languages", type=count, default=2)
    p.add_argument("--rerender-pct", type=number, default=10)
    p.add_argument("--qa-minutes", type=number, default=1,
                   help="review labor minutes per rendered output minute")
    p.add_argument("--hourly-rate", type=number, default=35)
    p.add_argument("--heygen-price", type=positive, default=99)
    p.add_argument("--heygen-credits", type=positive, default=100)
    p.add_argument("--credits-per-minute", type=positive, default=1,
                   help="UNVERIFIED lip-sync conversion; replace from contract")
    p.add_argument("--synthesia-price", type=positive, default=1000)
    p.add_argument("--synthesia-capacity", type=positive, default=300)
    p.add_argument("--rask-price", type=positive, default=150)
    p.add_argument("--rask-capacity", type=positive, default=100)
    a = p.parse_args()
    source = ((a.clips or TIERS[a.tier]) * a.clip_seconds / 60 if UGC
              else a.source_minutes or TIERS[a.tier])
    volume = source * a.languages * (1 + a.rerender_pct / 100)
    labor = volume * a.qa_minutes / 60 * a.hourly_rate
    specs = [("HeyGen API", a.heygen_price,
              a.heygen_credits / a.credits_per_minute),
             ("Synthesia quote" if ENTERPRISE else "Synthesia Creator",
              a.synthesia_price, a.synthesia_capacity),
             ("Rask Pro", a.rask_price, a.rask_capacity)]
    if not all(math.isfinite(v) and v > 0 for v in [source, volume]):
        p.error("workload exceeds supported numeric range")
    rows = []
    for name, price, capacity in specs:
        ratio = volume / capacity
        if not math.isfinite(ratio) or not math.isfinite(labor):
            p.error("cost exceeds supported numeric range")
        units = math.ceil(round(ratio, 10))
        bill = units * price
        if not math.isfinite(bill + labor):
            p.error("cost exceeds supported numeric range")
        rows.append(dict(provider=name, capacity_minutes=round(capacity, 4),
                         blocks=units, platform_usd=round(bill, 2),
                         qa_usd=round(labor, 2), total_usd=round(bill + labor, 2)))
    savings = {r["provider"]: round((r["total_usd"] - rows[0]["total_usd"]) * 12, 2)
               for r in rows[1:]}
    result = dict(tier=a.tier, source_minutes=round(source, 4),
                  output_minutes=round(volume, 4), rows=rows,
                  annual_savings_vs_heygen_usd=savings, inputs=vars(a),
                  basis="Historical 2024-2025 monthly list-price references; not live quotes",
                  assumptions=["Credit conversion is an unverified planning input",
                               "Capacity blocks are a model, not purchasable add-ons",
                               "Equal QA labor; annualization is 12 monthly workloads",
                               "Enterprise quote is hypothetical" if ENTERPRISE else
                               "Public authoring plan does not establish translation/API access"],
                  action_url=GATEWAY)
    if a.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("OFFLINE LOCALIZATION TCO | historical price / capacity model")
    print(f"Tier: {a.tier} | Source: {source:.2f} min | Output incl. retries: {volume:.2f} min")
    print("+--------------------+--------+------------+------------+------------+")
    print("| Provider           | Blocks | Platform $ | QA labor $ | Monthly $  |")
    print("+--------------------+--------+------------+------------+------------+")
    for r in rows:
        print(f"| {r['provider']:<18} | {r['blocks']:6d} | {r['platform_usd']:10.2f} | {r['qa_usd']:10.2f} | {r['total_usd']:10.2f} |")
    print("+--------------------+--------+------------+------------+------------+")
    for name, saving in savings.items():
        print(f"Annual savings vs {name}: ${saving:,.2f} (negative = HeyGen costs more)")
    print("Assumptions: 1 credit/min by default; confirm lip-sync SKU and conversion.")
    print("Blocks model capacity, not a vendor offer. Taxes, seats, generation excluded.")
    if ENTERPRISE:
        print("Synthesia quote is hypothetical; replace with your signed quote.")
    print(f"Evaluate HeyGen: {GATEWAY}")


if __name__ == "__main__":
    main()
