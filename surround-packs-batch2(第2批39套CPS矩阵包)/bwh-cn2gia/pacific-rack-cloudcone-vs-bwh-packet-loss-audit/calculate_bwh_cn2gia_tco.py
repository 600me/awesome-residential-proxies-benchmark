#!/usr/bin/env python3
"""MIT licensed. Offline scenario calculator; assumptions are not measurements."""
import argparse
import json
import math

GATEWAY = "https://coding.mybskm.top/go/bwh"
SCENARIO = 'Packet-loss audit: job retry TCO'
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
    p.add_argument("--jobs", type=number, default=10000, help="monthly logical jobs, fleet-wide")
    p.add_argument("--job-minutes", type=number, default=4)
    p.add_argument("--worker-hourly", type=number, default=0.20)
    p.add_argument("--incident-hours", type=number, default=2, help="engineer hours per failed-job fraction of 1%")
    p.add_argument("--bwh-failure-percent", type=number, default=0.2)
    p.add_argument("--dmit-failure-percent", type=number, default=0.2)
    p.add_argument("--cloudcone-failure-percent", type=number, default=3)
    a = p.parse_args()
    failures = [a.bwh_failure_percent, a.dmit_failure_percent, a.cloudcone_failure_percent]
    if max(failures) >= 100:
        p.error("failure percentages must be < 100")
    nodes = TIERS[a.tier]
    annual = [a.bwh_annual, a.dmit_monthly * 12, a.cloudcone_annual]
    retries = [a.jobs * (f / 100) / (1 - f / 100) for f in failures]
    costs = [retry * a.job_minutes / 60 * a.worker_hourly + f * a.incident_hours * a.hourly
             for retry, f in zip(retries, failures)]
    details = {"extra_attempts_per_provider": [round(r, 4) for r in retries],
               "scope": "Failure percentages describe whole jobs, not packet loss; PacificRack unpriced."}
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
