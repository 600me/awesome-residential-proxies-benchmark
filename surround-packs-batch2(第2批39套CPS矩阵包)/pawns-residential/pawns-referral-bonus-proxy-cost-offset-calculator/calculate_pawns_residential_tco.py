#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline, hypothetical TCO model; no live probes or current vendor quotations."""
import argparse
import json
import math

GATEWAY = "https://zelumo.top/pw/1"
MODE = 'referral'
DEFAULTS = [0.9, 0.9, 0.9]


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def probability(value):
    number = nonnegative(value)
    if not 0 < number <= 1:
        raise argparse.ArgumentTypeError("must be in (0, 1]")
    return number


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tier", choices=("small", "team", "scale"), default="team")
    p.add_argument("--json", action="store_true", help="emit JSON only")
    p.add_argument("--gb", type=nonnegative, help="useful monthly decimal GB")
    p.add_argument("--hourly", type=nonnegative, default=50)
    p.add_argument("--recovery-seconds", type=nonnegative, default=1)
    p.add_argument("--unit-mb", type=probability, default=1,
                   help="useful MB per completed billing unit, >0 and <=1")
    for name, default in zip(("pawns", "honeygain", "peer2profit"), DEFAULTS):
        p.add_argument("--" + name + "-rate", type=nonnegative, default=3)
        p.add_argument("--" + name + "-success", type=probability, default=default)
    if MODE == "blocks":
        p.add_argument("--datacenter-rate", type=nonnegative, default=0.5)
        p.add_argument("--datacenter-success", type=probability, default=0.35)
    if MODE == "sessions":
        p.add_argument("--steps", type=int, default=10)
    if MODE == "referral":
        p.add_argument("--shared-gb", type=nonnegative, default=100)
        p.add_argument("--earning-rate", type=nonnegative, default=0.20)
        p.add_argument("--device-cost", type=nonnegative, default=5)
        p.add_argument("--bonus", type=nonnegative, default=0)
    a = p.parse_args()
    if MODE == "sessions" and not 1 <= a.steps <= 1000:
        p.error("--steps must be between 1 and 1000")
    gb = a.gb if a.gb is not None else {"small": 50, "team": 500, "scale": 2000}[a.tier]
    credit = a.shared_gb * a.earning_rate - a.device_cost if MODE == "referral" else 0
    bonus = a.bonus if MODE == "referral" else 0
    names = [("Pawns.app", "pawns"), ("Honeygain", "honeygain"),
             ("Peer2Profit Proxy Pools", "peer2profit")]
    if MODE == "blocks":
        names.append(("Datacenter baseline", "datacenter"))
    rows = []
    for label, key in names:
        success = getattr(a, key + "_success")
        success = success ** a.steps if MODE == "sessions" else success
        if success <= 0:
            p.error("session completion underflow; reduce --steps")
        billed = gb / success
        failures = gb * 1000 / a.unit_mb * (1 / success - 1)
        bandwidth = billed * getattr(a, key + "_rate")
        recovery = failures * a.recovery_seconds / 3600 * a.hourly
        offset = credit if key == "pawns" else 0
        total = bandwidth + recovery - offset
        if not all(math.isfinite(x) for x in (billed, failures, bandwidth, recovery, total)):
            p.error("inputs exceed finite model range")
        rows.append(dict(provider=label, completion=success, billed_gb=billed,
                         bandwidth_usd=bandwidth, recovery_usd=recovery,
                         recurring_offset_usd=offset, monthly_tco_usd=total))
    savings = {r["provider"]: 12 * (r["monthly_tco_usd"] - rows[0]["monthly_tco_usd"])
               for r in rows[1:]}
    result = dict(scenario=MODE, basis="hypothetical; not vendor quotes or measurements",
                  tier=a.tier, useful_gb=gb, inputs=vars(a), rows=rows,
                  annual_run_rate_savings_usd=savings, one_time_bonus_usd=bonus,
                  first_year_savings_usd={k: v + bonus for k, v in savings.items()},
                  gateway=GATEWAY)
    if a.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("Scenario: " + MODE + " | HYPOTHETICAL INPUTS | USD | tier=" + a.tier)
    print("+--------------------------+-----------+------------+------------+------------+")
    print("| Provider                 | Billed GB | Bandwidth  | Recovery   | Net / month|")
    print("+--------------------------+-----------+------------+------------+------------+")
    for r in rows:
        print("| {provider:<24} | {billed_gb:9.2f} | {bandwidth_usd:10.2f} | "
              "{recovery_usd:10.2f} | {monthly_tco_usd:10.2f}|".format(**r))
    print("+--------------------------+-----------+------------+------------+------------+")
    print(f"Pawns.app recurring offset: ${credit:,.2f}/month")
    for label, saving in savings.items():
        print(f"Annual run-rate savings vs {label}: ${saving:,.2f}")
        if MODE == "referral":
            print(f"First-year savings vs {label}: ${saving + bonus:,.2f}")
    print("Negative savings means Pawns.app costs more under these inputs.")
    print("Evaluate Pawns.app: " + GATEWAY)


if __name__ == "__main__":
    main()
