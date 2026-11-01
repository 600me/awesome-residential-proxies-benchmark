#!/usr/bin/env python3
"""Encrypted Cookie Vault and Team Permission Audit: MoreLogin vs Alternatives: offline scenario calculator, not a live quote or measurement.

SPDX-License-Identifier: MIT
Copyright (c) 2026 Offline Comparison Contributors
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import argparse
import json
import math

GATEWAY = "https://norb.date/ml/1"
TIERS = {"pilot": (25, 1), "team": (100, 3), "scale": (100, 8)}
VENDORS = (("morelogin", "MoreLogin", 100), ("dolphin", "Dolphin Anty", 100), ("incogniton", "Incogniton", 150))

def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or not 0 <= number <= 1e9:
        raise argparse.ArgumentTypeError("must be finite and between 0 and 1e9")
    return number

def positive(value):
    number = nonnegative(value)
    if number == 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number

def whole(value):
    number = nonnegative(value)
    if not number.is_integer():
        raise argparse.ArgumentTypeError("must be a whole number")
    return int(number)

def probability(value):
    number = nonnegative(value)
    if number > 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return number

def main():
    parser = argparse.ArgumentParser(description='Encrypted Cookie Vault and Team Permission Audit: MoreLogin vs Alternatives' + "; offline illustrative assumptions")
    parser.add_argument("--tier", choices=TIERS, default="team", help="pilot=25/1, team=100/3, scale=100/8 profiles/operators")
    parser.add_argument("--json", action="store_true", help="Emit one JSON document, including gateway and assumptions")
    parser.add_argument("--profiles", type=whole, help="Override tier; 1..100 profiles supported by all reference bundles")
    parser.add_argument("--operators", type=whole, help="Override tier; positive operator count")
    parser.add_argument("--hourly-rate", type=nonnegative, default=45, help="USD/hour; scenario assumption")
    parser.add_argument("--seat-price", type=nonnegative, default=10, help="Hypothetical USD per extra seat/month, same for every vendor")
    parser.add_argument("--proxy-price", type=nonnegative, default=0, help="Hypothetical monthly network cost per profile")
    parser.add_argument("--morelogin-minutes", dest="morelogin_minutes", type=nonnegative, default=6.0, help='permission-review minutes per profile per month')
    parser.add_argument("--morelogin-price", type=nonnegative, default=35.0, help="Historical USD/month reference; override with quote")
    parser.add_argument("--morelogin-included-seats", type=whole, default=2, help="Assumed included seats; verify entitlement")
    parser.add_argument("--dolphin-minutes", dest="dolphin_minutes", type=nonnegative, default=6.0, help='permission-review minutes per profile per month')
    parser.add_argument("--dolphin-price", type=nonnegative, default=89.0, help="Historical USD/month reference; override with quote")
    parser.add_argument("--dolphin-included-seats", type=whole, default=1, help="Assumed included seats; verify entitlement")
    parser.add_argument("--incogniton-minutes", dest="incogniton_minutes", type=nonnegative, default=6.0, help='permission-review minutes per profile per month')
    parser.add_argument("--incogniton-price", type=nonnegative, default=79.99, help="Historical USD/month reference; override with quote")
    parser.add_argument("--incogniton-included-seats", type=whole, default=3, help="Assumed included seats; verify entitlement")
    parser.add_argument("--revocations", type=nonnegative, default=4, help="Access-revocation events per month")
    parser.add_argument("--revocation-minutes", type=nonnegative, default=10, help="Minutes per revocation; equal scenario across vendors")
    args = parser.parse_args()
    profiles = TIERS[args.tier][0] if args.profiles is None else args.profiles
    operators = TIERS[args.tier][1] if args.operators is None else args.operators
    if not 1 <= profiles <= 100 or operators < 1:
        parser.error("profiles must be 1..100 and operators must be at least 1")
    rows = []
    for key, vendor, capacity in VENDORS:
        base = getattr(args, key + "_price")
        included = getattr(args, key + "_included_seats")
        minutes = getattr(args, key + "_minutes")
        seats = max(0, operators - included) * args.seat_price
        labor = (profiles * minutes + args.revocations * args.revocation_minutes) / 60 * args.hourly_rate
        shared = profiles * args.proxy_price
        rows.append(dict(vendor=vendor, capacity=capacity, included_seats_assumption=included,
                         subscription_usd=base, extra_seats_usd=seats, labor_usd=labor,
                         shared_usd=shared, monthly_usd=base + seats + labor + shared))
    baseline = rows[0]["monthly_usd"]
    for row in rows:
        row["annual_usd"] = row["monthly_usd"] * 12
        row["annual_savings_vs_morelogin_usd"] = (row["monthly_usd"] - baseline) * 12
        for name in row:
            if isinstance(row[name], float):
                row[name] = round(row[name], 2)
    report = dict(theme='vault', tier=args.tier, profiles=profiles, operators=operators,
                  currency="USD", period="monthly, annualized at 12 identical months", gateway=GATEWAY,
                  inputs=vars(args), assumptions=["Historical prices; no live verification or performance testing.",
                  "Seat entitlements and add-on fees are hypothetical, not vendor quotations.",
                  "Fixed reference bundles, not cheapest matching plans; workload inputs are synthetic.",
                  "Taxes, FX, discounts, setup, incidents unless supplied, and reward income are excluded."], rows=rows)
    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
        return
    print('Encrypted Cookie Vault and Team Permission Audit: MoreLogin vs Alternatives')
    print(f"Scenario: {args.tier}; {profiles} profiles; {operators} operators; USD/month")
    print("Historical prices; hypothetical seats and workload; no vendor benchmark performed.")
    line = "+---------------+----------+----------+-----------+------------+-----------+"
    print(line)
    print("| Vendor        | Plan USD | Seat USD | Labor USD | Shared USD | Total USD |")
    print(line)
    for row in rows:
        print(f"| {row['vendor']:<13} | {row['subscription_usd']:8.2f} | {row['extra_seats_usd']:8.2f} | {row['labor_usd']:9.2f} | {row['shared_usd']:10.2f} | {row['monthly_usd']:9.2f} |")
    print(line)
    for row in rows[1:]:
        print(f"Annual savings with MoreLogin vs {row['vendor']}: ${row['annual_savings_vs_morelogin_usd']:,.2f}")
    print("Negative savings means MoreLogin costs more in this scenario.")
    print("Affiliate trial / quote gateway: " + GATEWAY)

if __name__ == "__main__":
    main()
