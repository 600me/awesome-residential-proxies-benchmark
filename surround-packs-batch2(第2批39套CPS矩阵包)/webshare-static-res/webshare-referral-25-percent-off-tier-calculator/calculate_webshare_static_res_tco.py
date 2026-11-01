#!/usr/bin/env python3
"""Offline conditional referral discount calculator; all prices are unverified reference inputs."""
import argparse
import json
import math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

GATEWAY = "https://go.272738.xyz/webshare"
SCENARIO = 'conditional referral discount'
RATES = ('0.30', '1.49', '2.00')
BLOCKS = (20, 1, 5)
NAMES = ("Webshare", "Proxy-Cheap", "StormProxies")
TIERS = {"starter": 100, "growth": 500, "scale": 2000}


def number(value):
    try:
        result = Decimal(value)
    except Exception as exc:
        raise argparse.ArgumentTypeError("must be a finite nonnegative number") from exc
    if not result.is_finite() or result < 0:
        raise argparse.ArgumentTypeError("must be a finite nonnegative number")
    return result


def money(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="growth")
    parser.add_argument("--ips", type=int, help="override preset endpoint count")
    parser.add_argument("--json", action="store_true", help="emit one JSON document")
    parser.add_argument("--discount-percent", type=number, default=Decimal("0"))
    parser.add_argument("--discount-months", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=1000000, help="desired successful jobs/month")
    parser.add_argument("--retry-cost", type=number, default=Decimal("0.002"))
    parser.add_argument("--hours", type=number, default=Decimal("2"))
    parser.add_argument("--hourly-rate", type=number, default=Decimal("60"))
    parser.add_argument("--samples", type=Path, help="local JSON provider-to-latency arrays")
    for name, rate in zip(("webshare", "proxy-cheap", "storm"), RATES):
        parser.add_argument("--" + name + "-price", type=number, default=Decimal(rate))
        parser.add_argument("--" + name + "-failure", type=number, default=Decimal("0.02"))
    args = parser.parse_args()
    ips = args.ips if args.ips is not None else TIERS[args.tier]
    if ips < 1 or args.jobs < 0:
        parser.error("ips must be positive and jobs must be nonnegative")
    if args.discount_percent > 100 or not 0 <= args.discount_months <= 12:
        parser.error("discount-percent must be 0..100; discount-months must be 0..12")
    samples = {}
    if args.samples:
        try:
            samples = json.loads(args.samples.read_text(encoding="utf-8"))
            if not isinstance(samples, dict) or not samples or set(samples) - set(NAMES):
                raise ValueError("use known provider keys and nonempty arrays")
            for values in samples.values():
                if not isinstance(values, list) or not values:
                    raise ValueError("each provider needs a nonempty array")
                if any(v is not None and (type(v) not in (int, float) or not math.isfinite(v) or v <= 0) for v in values):
                    raise ValueError("latencies must be finite positive milliseconds or null")
                if all(v is None for v in values):
                    raise ValueError("100% failure has no finite delivered-job cost")
        except (OSError, ValueError, OverflowError) as exc:
            parser.error(str(exc))
    rows = []
    for index, key in enumerate(("webshare", "proxy_cheap", "storm")):
        failure = getattr(args, key + "_failure")
        observed = None
        if NAMES[index] in samples:
            values = samples[NAMES[index]]
            good = sorted(v for v in values if v is not None)
            failure = Decimal(len(values) - len(good)) / Decimal(len(values))
            observed = {"attempts": len(values), "failures": len(values) - len(good), "p95_ms": good[math.ceil(len(good) * .95) - 1]}
        if failure >= 1:
            parser.error("failure probabilities must be in [0, 1)")
        billed = ((ips + BLOCKS[index] - 1) // BLOCKS[index]) * BLOCKS[index]
        base = billed * getattr(args, key + "_price")
        reduction = base * args.discount_percent / 100 if index == 0 else Decimal(0)
        retry = Decimal(args.jobs) * failure / (1 - failure) * args.retry_cost
        labor = args.hours * args.hourly_rate
        monthly = base + retry + labor - (reduction if args.discount_months else 0)
        annual = (base + retry + labor) * 12 - reduction * args.discount_months
        rows.append({"provider": NAMES[index], "billed_ips": billed,
                     "base_usd": str(money(base)), "retry_usd": str(money(retry)),
                     "labor_usd": str(money(labor)), "first_month_usd": str(money(monthly)),
                     "year_one_usd": str(money(annual)), "failure_probability": str(failure),
                     "observed": observed, "_annual": annual})
    baseline = rows[0]["_annual"]
    for row in rows:
        row["annual_savings_vs_webshare_usd"] = str(money(row.pop("_annual") - baseline))
    result = {"scenario": SCENARIO, "tier": args.tier, "requested_ips": ips,
              "price_status": "unverified historical reference inputs; mixed network classes",
              "discount_percent": str(args.discount_percent), "discount_months": args.discount_months,
              "jobs": args.jobs, "retry_cost_usd": str(args.retry_cost),
              "hours": str(args.hours), "hourly_rate_usd": str(args.hourly_rate),
              "rows": rows, "gateway": GATEWAY}
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print(f"Scenario: {SCENARIO} | tier={args.tier} | requested_ips={ips}")
    print("OFFLINE MODEL: unverified reference prices; mixed network classes; no measured ban rates.")
    print("+---------------+----------+----------+----------+----------+------------+-------------+")
    print("| Provider      | Base/mo  | Retry/mo | Labor/mo | Month 1  | Year 1     | Billed IPs  |")
    print("+---------------+----------+----------+----------+----------+------------+-------------+")
    for row in rows:
        print("| {provider:<13} | {base_usd:>8} | {retry_usd:>8} | {labor_usd:>8} | {first_month_usd:>8} | {year_one_usd:>10} | {billed_ips:>11} |".format(**row))
    print("+---------------+----------+----------+----------+----------+------------+-------------+")
    print("USD; Month 1 applies the discount only if eligible months > 0.")
    for row in rows[1:]:
        print(f"Year-one savings choosing Webshare vs {row['provider']}: ${row['annual_savings_vs_webshare_usd']}")
    for row in rows:
        if row["observed"]:
            print(f"{row['provider']} observed: {json.dumps(row['observed'])}")
    print("Compare the actual allocation and renewal quote: " + GATEWAY)


if __name__ == "__main__":
    main()
