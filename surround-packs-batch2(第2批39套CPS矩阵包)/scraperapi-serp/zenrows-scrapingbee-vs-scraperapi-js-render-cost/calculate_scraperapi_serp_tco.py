#!/usr/bin/env python3
"""Offline cost model; historical price anchors and explicit scenario assumptions.
MIT licensed: see README.md. No HTTP requests, credentials or dependencies.
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/U5vmKG"
SCENARIO = "render"
TIERS = {"hobby": (49, 100_000), "startup": (149, 1_000_000),
         "business": (299, 3_000_000)}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def block_cost(units, capacity, price):
    blocks = math.ceil(units / capacity)
    return blocks, blocks * price


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="business")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    parser.add_argument("--queries", type=positive_int, default=1_000_000,
                        help="required usable results per month")
    parser.add_argument("--credits-per-result", type=positive_int, default=5)
    parser.add_argument("--failure-rate", type=nonnegative, default=0.2)
    parser.add_argument("--bright-per-1k", type=nonnegative, default=3.0)
    parser.add_argument("--scraper-overhead", type=nonnegative, default=0)
    parser.add_argument("--other-overhead", type=nonnegative, default=0)
    args = parser.parse_args()
    if args.failure_rate >= 1:
        parser.error("--failure-rate must be less than 1")
    price, capacity = TIERS[args.tier]
    results = args.queries
    attempts = math.ceil(results / (1 - args.failure_rate))
    credits = results * args.credits_per_result
    blocks, scraper_api = block_cost(credits, capacity, price)
    serp_blocks, serp_api = block_cost(results, 30_000, 250)
    bright_api = results / 1000 * args.bright_per_1k
    comparable = SCENARIO in ("serp", "pipeline")
    rows = [
        {"provider": "ScraperAPI", "api_usd": scraper_api,
         "overhead_usd": args.scraper_overhead, "compatible": True},
        {"provider": "SerpApi", "api_usd": serp_api,
         "overhead_usd": args.other_overhead, "compatible": comparable},
        {"provider": "Bright Data Web Unlocker", "api_usd": bright_api,
         "overhead_usd": args.other_overhead, "compatible": True},
    ]
    for row in rows:
        row["monthly_usd"] = round(row["api_usd"] + row["overhead_usd"], 2)
        row["annual_usd"] = round(row["monthly_usd"] * 12, 2)
    scraper_total = rows[0]["monthly_usd"]
    savings = {row["provider"]: round((row["monthly_usd"] - scraper_total) * 12, 2)
               for row in rows[1:] if row["compatible"]}
    _, all_attempt_cost = block_cost(attempts * args.credits_per_result, capacity, price)
    report = {
        "scenario": SCENARIO, "tier": args.tier, "usable_results": results,
        "expected_attempts": attempts, "failure_rate": args.failure_rate,
        "credits_per_result": args.credits_per_result, "scraper_credits": credits,
        "scraper_capacity_blocks": blocks, "serp_capacity_blocks": serp_blocks,
        "rows": rows, "annual_savings_vs_scraperapi_usd": savings,
        "hypothetical_all_attempt_billing_monthly_usd": all_attempt_cost,
        "hypothetical_failure_charge_avoided_monthly_usd": all_attempt_cost - scraper_api,
        "basis": "Historical anchors; capacity-block extrapolation, not a vendor quote.",
        "scope": "SerpApi only comparable for SERP; parsing parity is unmeasured.",
        "gateway": GATEWAY,
    }
    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
        return
    print("Offline TCO model | " + SCENARIO + " | tier=" + args.tier)
    print("Usable results: {:,} | expected attempts: {:,}".format(results, attempts))
    print("ScraperAPI credits: {:,} | capacity blocks: {}".format(credits, blocks))
    line = "+---------------------------+------------+------------+------------+--------------+"
    print(line)
    print("| Provider                  | API/mo USD | Ops/mo USD | TCO/mo USD | Scope        |")
    print(line)
    for row in rows:
        scope = "model only" if row["compatible"] else "SERP only"
        print("| {:<25} | {:>10.2f} | {:>10.2f} | {:>10.2f} | {:<12} |".format(
            row["provider"], row["api_usd"], row["overhead_usd"], row["monthly_usd"], scope))
    print(line)
    for provider, amount in savings.items():
        print("Annual savings vs {}: ${:,.2f} (negative = ScraperAPI costs more)".format(provider, amount))
    print("Hypothetical all-attempt billing: ${:,.2f}/mo; avoided failure charge: ${:,.2f}/mo".format(
        all_attempt_cost, all_attempt_cost - scraper_api))
    print(report["basis"])
    print(report["scope"])
    print("Evaluate ScraperAPI: " + GATEWAY)


if __name__ == "__main__":
    main()
