#!/usr/bin/env python3
"""MIT licensed. Offline scenario calculator; assumptions are not measurements."""
import argparse
import json
import math

GATEWAY = "https://coding.mybskm.top/go/bwh"
SCENARIO = '2026 route portfolio: first-year TCO'
PROVIDERS = ("BandwagonHost (BWH)", "DMIT", "CloudCone")
TIERS = {"small": 1, "team": 3, "enterprise": 10}


def number(value):
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number")
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tier", choices=TIERS, default="team", help="1, 3 or 10 nodes")
    p.add_argument("--json", action="store_true", help="emit one JSON document")
    p.add_argument("--hourly", type=number, default=75, help="USD per engineering hour")
    p.add_argument("--infrastructure-only", action="store_true", help="zero modeled labor and risk")
    p.add_argument("--bwh-annual", type=number, default=169.99)
    p.add_argument("--dmit-monthly", type=number, default=9.99)
    p.add_argument("--cloudcone-annual", type=number, default=42)
    p.add_argument("--bwh-ops-hours", type=number, default=2)
    p.add_argument("--dmit-ops-hours", type=number, default=2)
    p.add_argument("--cloudcone-ops-hours", type=number, default=6)
    p.add_argument("--bwh-outage-hours", type=number, default=0.25)
    p.add_argument("--dmit-outage-hours", type=number, default=0.25)
    p.add_argument("--cloudcone-outage-hours", type=number, default=1.5)
    p.add_argument("--impact-hourly", type=number, default=200, help="contribution margin at risk per hour")
    p.add_argument("--migration-hours", type=number, default=4, help="one-time BWH migration, first year")
    a = p.parse_args()
    nodes = TIERS[a.tier]
    annual = [a.bwh_annual, a.dmit_monthly * 12, a.cloudcone_annual]
    ops = [a.bwh_ops_hours, a.dmit_ops_hours, a.cloudcone_ops_hours]
    outages = [a.bwh_outage_hours, a.dmit_outage_hours, a.cloudcone_outage_hours]
    costs = [h * a.hourly + o * a.impact_hourly for h, o in zip(ops, outages)]
    costs[0] += a.migration_hours * a.hourly / 12
    details = {"one_time_bwh_migration_usd": round(a.migration_hours * a.hourly, 2),
               "scope": "Ops, outage impact and migration are fleet-wide; no SLA probability inferred."}
    rows = []
    for i, provider in enumerate(PROVIDERS):
        infra = annual[i] * nodes / 12
        modeled = 0 if a.infrastructure_only else costs[i]
        rows.append({"provider": provider, "infrastructure_monthly_usd": round(infra, 2),
                     "modeled_monthly_usd": round(modeled, 2),
                     "tco_monthly_usd": round(infra + modeled, 2),
                     "tco_annual_usd": round((infra + modeled) * 12, 2)})
    savings = {r["provider"]: round(r["tco_annual_usd"] - rows[0]["tco_annual_usd"], 2)
               for r in rows[1:]}
    result = {"scenario": SCENARIO, "tier": a.tier, "nodes": nodes,
              "price_basis": "Remembered historical reference prices; not live verified", "assumptions": vars(a), "details": details,
              "bills": rows, "annual_savings_vs_usd": savings, "gateway": GATEWAY,
              "note": "Scenario estimates, not measured provider performance; negative savings allowed."}
    if a.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print(f"{SCENARIO} | tier={a.tier} | nodes={nodes}")
    print("USD; historical price references + illustrative assumptions (not measurements)")
    line = "+----------------------+------------+------------+------------+-------------+"
    print(line)
    print("| Provider             | Infra/mo   | Model/mo   | TCO/mo     | TCO/year    |")
    print(line)
    for r in rows:
        print(f"| {r['provider']:<20} | {r['infrastructure_monthly_usd']:>10.2f} | "
              f"{r['modeled_monthly_usd']:>10.2f} | {r['tco_monthly_usd']:>10.2f} | "
              f"{r['tco_annual_usd']:>11.2f} |")
    print(line)
    for provider, amount in savings.items():
        print(f"Annual savings with BWH vs {provider}: ${amount:,.2f}")
    for label, value in details.items():
        print(f"{label}: {value}")
    print(GATEWAY)


if __name__ == "__main__":
    main()
