#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline TCO scenario; prices and labor are editable assumptions, not quotes."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

GATEWAY = "https://coding.mybskm.top/go/duoplus"
SCENARIO = 'Messaging workspace isolation'
TIERS = {"pilot": 10, "growth": 60, "scale": 200}
D = Decimal
LABOR = {"duoplus": D(".14"), "vmos": D(".25"), "physical": D(".70")}
PHYSICAL_FIXED_HOURS = D("5")


def money(value):
    return str(value.quantize(D("0.01"), rounding=ROUND_HALF_UP))


def nonnegative(text):
    try:
        value = D(text)
    except InvalidOperation:
        raise argparse.ArgumentTypeError("must be a finite nonnegative number")
    if not value.is_finite() or value < 0 or value > D("1000000"):
        raise argparse.ArgumentTypeError("must be between 0 and 1000000")
    return value


def positive_int(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer")
    if not 1 <= value <= 1000000:
        raise argparse.ArgumentTypeError("must be between 1 and 1000000")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="growth", help="fleet preset, not a vendor plan")
    parser.add_argument("--devices", type=positive_int, help="override tier device count")
    parser.add_argument("--duoplus-monthly", type=nonnegative, default=D("9.90"), help="USD/device/month assumption")
    parser.add_argument("--vmos-monthly", type=nonnegative, default=D("7.00"), help="USD/device/month assumption")
    parser.add_argument("--hardware-unit-cost", type=nonnegative, default=D("120"), help="USD per handset")
    parser.add_argument("--hourly-rate", type=nonnegative, default=D("30"), help="USD per operator hour")
    parser.add_argument("--json", action="store_true", help="print one JSON object instead of the ASCII table")
    args = parser.parse_args()
    n = args.devices if args.devices is not None else TIERS[args.tier]
    count = D(n)
    capex = count * (args.hardware_unit_cost + D("18"))
    hours = {key: count * value + (PHYSICAL_FIXED_HOURS if key == "physical" else D("1"))
             for key, value in LABOR.items()}
    rows = {
        "Device subscription": [count * args.duoplus_monthly, count * args.vmos_monthly, D(0)],
        "Hardware amortization": [D(0), D(0), capex / D(24)],
        "Electricity": [D(0), D(0), count * D("3.8") / D(1000) * D(730) * D("0.18")],
        "Replacement reserve": [D(0), D(0), count * args.hardware_unit_cost * D("0.15") / D(12)],
        "Connectivity allowance": [count * D("1.50")] * 3,
        "Operator labor": [hours[key] * args.hourly_rate for key in ("duoplus", "vmos", "physical")],
    }
    totals = [sum((row[i] for row in rows.values()), D(0)) for i in range(3)]
    annual = [total * D(12) for total in totals]
    cash = [annual[0], annual[1], annual[2] - capex / D(24) * D(12) + capex]
    savings = {key: money(annual[i] - annual[0]) for key, i in (("vmos", 1), ("physical", 2))}
    result = {
        "scenario": SCENARIO, "currency": "USD", "tier": args.tier, "devices": n,
        "price_basis": "Editable planning assumptions; no verified current vendor quote",
        "assumptions": {
            "duoplus_monthly": money(args.duoplus_monthly), "vmos_monthly": money(args.vmos_monthly),
            "hardware_unit_cost": money(args.hardware_unit_cost), "rack_cost_per_device": "18.00",
            "amortization_months": 24, "hardware_residual_value": "0.00",
            "watts_per_physical_device": "3.8", "hours_per_month": 730, "usd_per_kwh": "0.18",
            "annual_handset_replacement_fraction": "0.15", "connectivity_per_device": "1.50",
            "operator_hourly_rate": money(args.hourly_rate),
            "operator_hours_per_device": {key: str(value) for key, value in LABOR.items()},
            "fixed_operator_hours": {"duoplus": "1", "vmos": "1", "physical": str(PHYSICAL_FIXED_HOURS)},
        },
        "operator_hours_monthly": {key: str(value) for key, value in hours.items()},
        "monthly_line_items": {label: [money(value) for value in values] for label, values in rows.items()},
        "column_order": ["duoplus", "vmos", "physical"],
        "monthly_tco": [money(value) for value in totals],
        "annualized_tco": [money(value) for value in annual],
        "first_year_cash": [money(value) for value in cash],
        "hardware_upfront": money(capex), "annual_savings_vs": savings, "gateway": GATEWAY,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(f"{SCENARIO} | tier={args.tier} | devices={n} | USD")
    print("Basis: editable assumptions, not verified current vendor prices.")
    border = "+-------------------------+--------------+--------------+--------------+"
    print(border)
    print(f"| {'Monthly line item':<23} | {'DuoPlus':>12} | {'VMOS Cloud':>12} | {'Physical':>12} |")
    print(border)
    for label, values in rows.items():
        print(f"| {label:<23} | " + " | ".join(f"{money(value):>12}" for value in values) + " |")
    print(border)
    for label, values in (("Monthly TCO", totals), ("Annualized TCO", annual), ("First-year cash", cash)):
        print(f"| {label:<23} | " + " | ".join(f"{money(value):>12}" for value in values) + " |")
    print(border)
    print(f"Physical hardware upfront: ${money(capex)}")
    print(f"Annualized savings with DuoPlus vs VMOS Cloud: ${savings['vmos']}")
    print(f"Annualized savings with DuoPlus vs Physical Phone Farms: ${savings['physical']}")
    print("Savings are signed: a negative value means DuoPlus costs more.")
    print(GATEWAY)


if __name__ == "__main__":
    main()
