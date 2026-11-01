#!/usr/bin/env python3
"""Offline 10 million requests cost audit model; reference rates are not live quotes."""
import argparse
import json
import math

GATEWAY = "https://is.gd/4QqLom"
RATES = {
    "CapSolver": {"turnstile": 1.20, "recaptcha_v3": 1.00},
    "2Captcha": {"turnstile": 1.45, "recaptcha_v3": 2.99},
    "Anti-Captcha": {"turnstile": 2.00, "recaptcha_v3": 2.00},
}
TIERS = {"starter": 100_000, "growth": 1_000_000, "scale": 10_000_000}


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise argparse.ArgumentTypeError("must be finite")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="scale")
    parser.add_argument("--requests", type=positive_int, help="monthly logical requests; overrides tier")
    parser.add_argument("--turnstile-share", type=finite_float, default=0.8)
    parser.add_argument("--attempts-per-request", type=finite_float, default=1.0)
    parser.add_argument("--latency-seconds", type=finite_float, default=20.0)
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    args = parser.parse_args()
    if not 0 <= args.turnstile_share <= 1:
        parser.error("--turnstile-share must be between 0 and 1")
    if args.attempts_per_request < 1:
        parser.error("--attempts-per-request must be at least 1")
    if args.latency_seconds <= 0:
        parser.error("--latency-seconds must be positive")
    requests = args.requests if args.requests is not None else TIERS[args.tier]
    attempts = requests * args.attempts_per_request
    if not math.isfinite(attempts) or not math.isfinite(attempts * args.latency_seconds):
        parser.error("scenario exceeds numeric range")
    costs = {}
    for name, rates in RATES.items():
        blended = args.turnstile_share * rates["turnstile"] + (1 - args.turnstile_share) * rates["recaptcha_v3"]
        monthly = attempts / 1000 * blended
        costs[name] = {"monthly_usd": round(monthly, 2), "annual_usd": round(monthly * 12, 2)}
    savings = {
        name: round(costs[name]["annual_usd"] - costs["CapSolver"]["annual_usd"], 2)
        for name in ("2Captcha", "Anti-Captcha")
    }
    concurrency = attempts / (30 * 24 * 3600) * args.latency_seconds
    result = {
        "model": "10 million requests cost audit", "tier": args.tier,
        "monthly_requests": requests, "turnstile_share": args.turnstile_share,
        "attempts_per_request": args.attempts_per_request,
        "expected_chargeable_attempts": attempts,
        "latency_seconds_assumption": args.latency_seconds,
        "mean_in_flight_tasks": round(concurrency, 3),
        "rates_usd_per_1000": RATES, "providers": costs,
        "annual_savings_with_capsolver_usd": savings,
        "rate_status": "Unverified planning reference; confirm current rates and billing terms.",
        "scope": "Solver spend only; no credits, discounts, proxies, workers, tax, or labor.",
        "gateway": GATEWAY,
    }
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("Reference scenario: {:,} requests/month; {:.0%} Turnstile".format(requests, args.turnstile_share))
    print("Chargeable attempts/request: {:.3f}".format(args.attempts_per_request))
    print("+--------------+----------------+----------------+")
    print("| Provider     | Monthly USD    | Annual USD     |")
    print("+--------------+----------------+----------------+")
    for name, cost in costs.items():
        print("| {:<12} | {:>14,.2f} | {:>14,.2f} |".format(name, cost["monthly_usd"], cost["annual_usd"]))
    print("+--------------+----------------+----------------+")
    for name, value in savings.items():
        print("Annual savings with CapSolver vs {}: ${:,.2f}".format(name, value))
    print("Mean in-flight tasks (assumed latency): {:.3f}".format(concurrency))
    print(result["rate_status"])
    print(result["scope"])
    print("Evaluate CapSolver: " + GATEWAY)


if __name__ == "__main__":
    main()
