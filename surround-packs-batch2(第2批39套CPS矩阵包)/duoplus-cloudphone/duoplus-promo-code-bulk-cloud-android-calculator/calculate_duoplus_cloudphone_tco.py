#!/usr/bin/env python3
"""Offline scenario calculator; rates are editable assumptions, not live quotes."""
import argparse
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext

GATEWAY = "https://coding.mybskm.top/go/duoplus"
TOPIC = 'bulk purchasing and effective discount arithmetic'
DEFAULT_MINUTES = (3, 6, 7)
VENDORS = ("duoplus", "redfinger", "geelark")
LABELS = ("DuoPlus Cloud Phone", "Redfinger", "GeeLark")
D = Decimal
getcontext().prec = 64


def nonnegative(value):
    try:
        number = D(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError("use a finite non-negative number")
    if not number.is_finite() or number < 0:
        raise argparse.ArgumentTypeError("use a finite non-negative number")
    if number > D("1000000000"):
        raise argparse.ArgumentTypeError("number must be at most 1000000000")
    return number


def money(value):
    return value.quantize(D("0.01"), rounding=ROUND_HALF_UP)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=("starter", "growth", "scale"), default="growth")
    parser.add_argument("--phones", type=int, help="override tier quantity; 1 to 1000000")
    parser.add_argument("--json", action="store_true", help="emit JSON only, including gateway")
    parser.add_argument("--proxy", type=nonnegative, default=D("3"), help="USD per phone/month")
    parser.add_argument("--labor-hourly", type=nonnegative, default=D("30"), help="USD per staff hour")
    parser.add_argument("--workdays", type=int, default=30, help="operating days per month; 1 to 31")
    parser.add_argument("--recovery-hours", type=nonnegative, default=D("2"))
    parser.add_argument("--discount-pct", type=nonnegative, default=D("0"),
                        help="assumed recurring DuoPlus rental discount; 0 to 100")
    for vendor, rate, minutes in zip(VENDORS, ("9.90", "14.90", "29.90"), DEFAULT_MINUTES):
        parser.add_argument(f"--{vendor}-rate", type=nonnegative, default=D(rate))
        parser.add_argument(f"--{vendor}-minutes", type=nonnegative, default=D(str(minutes)))
        parser.add_argument(f"--{vendor}-platform-fee", type=nonnegative, default=D("0"))
        parser.add_argument(f"--{vendor}-incident-rate", type=nonnegative, default=D("0"),
                            help="expected incidents per phone/month; scenario input")
    args = parser.parse_args()
    phones = args.phones if args.phones is not None else {"starter": 10, "growth": 50, "scale": 200}[args.tier]
    if not 1 <= phones <= 1000000:
        parser.error("--phones must be between 1 and 1000000")
    if not 1 <= args.workdays <= 31:
        parser.error("--workdays must be between 1 and 31")
    if args.discount_pct > 100:
        parser.error("--discount-pct must be between 0 and 100")
    inputs = {key: str(value) if isinstance(value, D) else value
              for key, value in vars(args).items() if key != "json"}
    inputs["phones"] = phones
    rows = []
    for vendor, label in zip(VENDORS, LABELS):
        rate = getattr(args, f"{vendor}_rate")
        factor = (1 - args.discount_pct / 100) if vendor == "duoplus" else D("1")
        components = {
            "phones": money(phones * rate * factor),
            "proxy": money(phones * args.proxy),
            "labor": money(phones * getattr(args, f"{vendor}_minutes") * args.workdays / 60 * args.labor_hourly),
            "incidents": money(phones * getattr(args, f"{vendor}_incident_rate") * args.recovery_hours * args.labor_hourly),
            "platform": money(getattr(args, f"{vendor}_platform_fee")),
        }
        total = sum(components.values())
        rows.append({"provider": label, **components, "monthly": total, "annual": total * 12})
    savings = {row["provider"]: row["annual"] - rows[0]["annual"] for row in rows[1:]}
    if args.json:
        payload = {"topic": TOPIC, "currency": "USD", "inputs": inputs,
                   "assumptions": "Unverified planning rates; full-month rentals; no observed incident rates; taxes and one-time migration excluded.",
                   "bills": [{k: str(v) if isinstance(v, D) else v for k, v in row.items()} for row in rows],
                   "annual_savings_vs": {k: str(v) for k, v in savings.items()}, "gateway": GATEWAY}
        print(json.dumps(payload, indent=2))
        return
    print(f"{TOPIC} | tier={args.tier} | phones={phones} | USD")
    print("Planning assumptions only; rates and labor are not verified vendor quotes or benchmarks.")
    columns = (("provider", "Provider", 19), ("phones", "Phones", 12), ("proxy", "Proxy", 12),
               ("labor", "Labor", 13), ("incidents", "Incidents", 12), ("platform", "Platform", 12),
               ("monthly", "Monthly", 14), ("annual", "Annual", 15))
    border = "+" + "+".join("-" * (width + 2) for _, _, width in columns) + "+"
    print(border)
    print("| " + " | ".join(label.ljust(width) for _, label, width in columns) + " |")
    print(border)
    for row in rows:
        print("| " + " | ".join(str(row[key]).ljust(width) if key == "provider" else
                                  f"{row[key]:,.2f}".rjust(width) for key, _, width in columns) + " |")
    print(border)
    for competitor, saving in savings.items():
        print(f"Annual savings vs {competitor}: ${saving:,.2f}")
    print("Negative savings means DuoPlus costs more under your inputs. Annual = monthly x 12.")
    print(f"Check the current DuoPlus offer: {GATEWAY}")


if __name__ == "__main__":
    main()
