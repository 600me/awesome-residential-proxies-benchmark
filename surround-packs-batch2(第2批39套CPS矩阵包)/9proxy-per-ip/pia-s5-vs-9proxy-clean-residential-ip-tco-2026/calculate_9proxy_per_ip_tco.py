#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline, assumption-driven proxy TCO; optional local SOCKS5 readiness probe."""
import argparse
import json
import math
import socket
import time

GATEWAY = "https://norb.date/p/1"
PROFILE = {'name': 'clean', 'ips': 10000, 'gb': 1000, 'q9': 0.9, 'qp': 0.8, 'h9': 2, 'hp': 6}
TIERS = {"starter": 0.2, "growth": 1.0, "scale": 5.0}


def finite_number(value):
    number = float(value)
    if not math.isfinite(number):
        raise argparse.ArgumentTypeError("must be finite")
    return number


def probe(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout) as connection:
            connection.settimeout(timeout)
            connection.sendall(b"\x05\x01\x00")
            reply = b""
            while len(reply) < 2:
                part = connection.recv(2 - len(reply))
                if not part:
                    break
                reply += part
            return {"ready": reply == b"\x05\x00", "reply_hex": reply.hex(),
                    "scope": "local unauthenticated SOCKS5 greeting only"}
    except OSError as error:
        return {"ready": False, "error": str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="growth")
    parser.add_argument("--json", action="store_true", help="print one JSON object")
    for name, default in (("ips", None), ("gb", None), ("rate-9", .20),
                          ("rate-pia", .25), ("per-gb-rate", 3.50),
                          ("clean-rate-9", PROFILE["q9"]),
                          ("clean-rate-pia", PROFILE["qp"]),
                          ("coupon-percent", 0), ("hourly-rate", 30),
                          ("hours-9", PROFILE["h9"]), ("hours-pia", PROFILE["hp"])):
        parser.add_argument("--" + name, type=finite_number, default=default)
    parser.add_argument("--health-check", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=1080)
    parser.add_argument("--timeout", type=finite_number, default=2)
    parser.add_argument("--watch", type=int, default=1, help="bounded probe count")
    parser.add_argument("--interval", type=finite_number, default=5)
    args = parser.parse_args()
    if not (0 < args.clean_rate_9 <= 1 and 0 < args.clean_rate_pia <= 1):
        parser.error("clean rates must be greater than 0 and at most 1")
    if not 0 <= args.coupon_percent <= 100:
        parser.error("coupon percent must be between 0 and 100")
    quantities = [args.rate_9, args.rate_pia, args.per_gb_rate, args.hourly_rate,
                  args.hours_9, args.hours_pia, args.interval]
    if any(value < 0 for value in quantities):
        parser.error("rates, labor hours and interval cannot be negative")
    if args.watch < 1 or not 1 <= args.port <= 65535 or args.timeout <= 0:
        parser.error("watch >= 1, valid port and positive timeout required")
    if args.watch > 1 and not args.health_check:
        parser.error("--watch requires --health-check")
    factor = TIERS[args.tier]
    ips = args.ips if args.ips is not None else PROFILE["ips"] * factor
    gb = args.gb if args.gb is not None else PROFILE["gb"] * factor
    if ips < 0 or gb < 0 or ips != int(ips):
        parser.error("ips must be a nonnegative integer; gb must be nonnegative")
    credits_9 = math.ceil(ips / args.clean_rate_9)
    credits_pia = math.ceil(ips / args.clean_rate_pia)
    cost_9 = round(credits_9 * args.rate_9 * (1 - args.coupon_percent / 100)
                   + args.hours_9 * args.hourly_rate, 2)
    cost_pia = round(credits_pia * args.rate_pia + args.hours_pia * args.hourly_rate, 2)
    cost_gb = round(gb * args.per_gb_rate, 2)
    rows = [{"provider": name, "credits": count, "monthly_usd": cost,
             "annual_usd": round(cost * 12, 2)}
            for name, count, cost in (("9Proxy", credits_9, cost_9),
                                      ("Pia S5", credits_pia, cost_pia),
                                      ("Per-GB reference", None, cost_gb))]
    result = {"scenario": PROFILE["name"], "tier": args.tier, "ips": int(ips),
              "gb": gb, "rows": rows, "assumptions": vars(args),
              "annual_savings_vs_pia_usd": round((cost_pia - cost_9) * 12, 2),
              "annual_savings_vs_per_gb_usd": round((cost_gb - cost_9) * 12, 2),
              "breakeven_gb": round(cost_9 / args.per_gb_rate, 2)
                  if args.per_gb_rate else None,
              "gateway": GATEWAY, "pricing_status": "historical reference; unverified"}
    if args.health_check:
        result["health"] = []
        for index in range(args.watch):
            result["health"].append(probe(args.host, args.port, args.timeout))
            if index + 1 < args.watch:
                time.sleep(args.interval)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Offline reference model | " + PROFILE["name"] + " | tier=" + args.tier)
        print(f"Accepted IP allocations/month: {int(ips):,} | Traffic: {gb:,.2f} GB")
        print("+-------------------+----------+---------------+---------------+")
        print("| Provider          | Credits  | Monthly USD   | Annual USD    |")
        print("+-------------------+----------+---------------+---------------+")
        for row in rows:
            credits = str(row["credits"]) if row["credits"] is not None else "n/a"
            print(f"| {row['provider']:<17} | {credits:>8} | {row['monthly_usd']:>13,.2f} | {row['annual_usd']:>13,.2f} |")
        print("+-------------------+----------+---------------+---------------+")
        print(f"Annual savings vs Pia S5: ${result['annual_savings_vs_pia_usd']:,.2f}")
        print(f"Annual savings vs per-GB: ${result['annual_savings_vs_per_gb_usd']:,.2f}")
        boundary = result["breakeven_gb"]
        print("Per-GB break-even: " + (f"{boundary:,.2f} GB/month" if boundary is not None else "undefined (zero GB rate)"))
        if args.health_check:
            print("Local SOCKS5 checks: " + json.dumps(result["health"]))
        print("Reference prices; replace with your quote. Negative savings = higher cost.")
        print("Compare plans: " + GATEWAY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
