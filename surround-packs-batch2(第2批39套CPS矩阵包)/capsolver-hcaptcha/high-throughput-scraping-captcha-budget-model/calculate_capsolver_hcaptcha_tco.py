#!/usr/bin/env python3
"""Offline scenario calculator; model inputs are not vendor measurements. MIT."""
# SPDX-License-Identifier: MIT
import argparse
import json
import math

GATEWAY = "https://zelumo.top/cs/1"
SCENARIO = 'Peak traffic and monthly budget planning'
DEFAULTS = {'retry_rate': 0.1,
 'usable_rate': 0.98,
 'expiry_rate': 0.03,
 'utilization': 0.75,
 'amortization_months': 24.0,
 'worker_capacity': 2000000.0,
 'token_ttl': 120.0,
 'hardware_cost': 1500.0,
 'license_annual': 128.0,
 'power_watts': 250.0,
 'kwh_price': 0.18,
 'hosting_monthly': 80.0,
 'self_ops_hours': 20.0,
 'hourly_rate': 60.0,
 'api_ops_hours': 2.0,
 'dbc_ops_hours': 4.0,
 'peak_factor': 12.0,
 'capsolver_p95': 12.0,
 'dbc_p95': 25.0,
 'capmonster_cloud_p95': 12.0,
 'self_p95': 18.0,
 'consumer_delay': 30.0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tier", choices=("dev", "growth", "enterprise"), default="growth")
    p.add_argument("--json", action="store_true", help="Emit one JSON object")
    p.add_argument("--monthly-tokens", type=int, help="Required usable tokens per month")
    p.add_argument("--task-family", choices=("hcaptcha", "geetest-v4", "datadome"), default="hcaptcha")
    for name in ("capsolver", "dbc", "capmonster-cloud"):
        p.add_argument("--" + name + "-price", type=float, help="USD per 1,000 billed attempts")
    for name, value in DEFAULTS.items():
        p.add_argument("--" + name.replace("_", "-"), type=float, default=value)
    a = p.parse_args()
    d = vars(a)
    volume = a.monthly_tokens if a.monthly_tokens is not None else {
        "dev": 100_000, "growth": 1_000_000, "enterprise": 10_000_000}[a.tier]
    if volume <= 0:
        p.error("--monthly-tokens must be positive")
    for key, value in d.items():
        if isinstance(value, float) and (not math.isfinite(value) or value < 0):
            p.error("--" + key.replace("_", "-") + " must be finite and nonnegative")
    for key in ("usable_rate", "utilization"):
        if not 0 < d[key] <= 1:
            p.error("--" + key.replace("_", "-") + " must be in (0, 1]")
    if a.expiry_rate >= 1:
        p.error("--expiry-rate must be below 1")
    for key in ("amortization_months", "worker_capacity", "token_ttl"):
        if d[key] <= 0:
            p.error("--" + key.replace("_", "-") + " must be positive")
    price_keys = ("capsolver_price", "dbc_price", "capmonster_cloud_price")
    if a.task_family != "hcaptcha" and any(d[k] is None for k in price_keys):
        p.error("non-hCaptcha scenarios require all three explicit vendor price inputs")
    prices = [d[k] if d[k] is not None else v for k, v in zip(price_keys, (0.80, 2.89, 0.80))]
    attempts = volume * (1 + a.retry_rate) / (a.usable_rate * (1 - a.expiry_rate))
    workers = math.ceil(attempts / (a.worker_capacity * a.utilization))
    self_fixed = (a.hardware_cost / a.amortization_months + a.license_annual / 12
                  + a.power_watts / 1000 * 730 * a.kwh_price + a.hosting_monthly
                  + a.self_ops_hours * a.hourly_rate)
    costs = [attempts * prices[0] / 1000 + a.api_ops_hours * a.hourly_rate,
             attempts * prices[1] / 1000 + a.dbc_ops_hours * a.hourly_rate,
             attempts * prices[2] / 1000 + a.api_ops_hours * a.hourly_rate,
             workers * self_fixed]
    names = ("CapSolver API", "DeathByCaptcha API", "CapMonster Cloud", "CapMonster self-host*")
    peak_rps = attempts / (730 * 3600) * a.peak_factor
    latencies = (a.capsolver_p95, a.dbc_p95, a.capmonster_cloud_p95, a.self_p95)
    rows = []
    for name, cost, latency in zip(names, costs, latencies):
        rows.append({"provider": name, "monthly_usd": round(cost, 2),
                     "annual_usd": round(cost * 12, 2),
                     "annual_savings_with_capsolver_usd": round((cost - costs[0]) * 12, 2),
                     "usd_per_1000_usable": round(cost / volume * 1000, 4),
                     "peak_in_flight": math.ceil(peak_rps * latency),
                     "assumed_p95_seconds": latency,
                     "ttl_margin_seconds": round(a.token_ttl - a.consumer_delay - latency, 2)})
    result = {"scenario": SCENARIO, "tier": a.tier, "task_family": a.task_family,
              "monthly_usable_tokens": volume, "modeled_billed_attempts": round(attempts, 2),
              "self_host_workers": workers, "modeled_peak_rps": round(peak_rps, 4),
              "inputs": d, "effective_prices_usd_per_1000": dict(zip(price_keys, prices)),
              "rows": rows, "gateway": GATEWAY,
              "basis": "Offline reference prices; all performance inputs are assumptions.",
              "self_host_caveat": "Conditional capacity budget; validate task support and hardware throughput.",
              "excluded": ["tax", "proxy and egress", "target access", "SLA penalties", "financing"]}
    if a.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(SCENARIO)
    print(f"Task: {a.task_family}; tier: {a.tier}; usable tokens/month: {volume:,}")
    print(f"Modeled billed attempts: {attempts:,.2f}; self-host workers: {workers}")
    border = "+------------------------+---------------+---------------+------------------+"
    print(border)
    print("| Provider               | Monthly USD   | Annual USD    | Annual saved USD |")
    print(border)
    for row in rows:
        print(f"| {row['provider']:<22} | {row['monthly_usd']:>13,.2f} | "
              f"{row['annual_usd']:>13,.2f} | {row['annual_savings_with_capsolver_usd']:>16,.2f} |")
    print(border)
    print("Annual saved = comparison cost minus CapSolver; negative means CapSolver costs more.")
    print(f"Peak modeled requests/s: {peak_rps:.4f}; in-flight planning counts:")
    for row in rows:
        print(f"  {row['provider']}: {row['peak_in_flight']} (TTL margin {row['ttl_margin_seconds']:.1f}s)")
    print("Offline reference prices; latency, usable yield and capacity are assumptions.")
    print("* Self-host cost is conditional on validated task support and measured capacity.")
    print("Excluded: tax, proxy/egress, target access, SLA penalties and financing.")
    print(GATEWAY)


if __name__ == "__main__":
    main()
