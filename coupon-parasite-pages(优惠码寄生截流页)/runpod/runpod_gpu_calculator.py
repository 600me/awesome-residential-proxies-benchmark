#!/usr/bin/env python3
"""RunPod GPU budget calculator; Python standard library only.

Enter billed GPU hours; include idle hours and quoted storage charges.
Rates are user-supplied USD quotes, never a claim about current pricing.
Annual totals assume twelve identical usage months and exclude unknown fees.
Example: python runpod_gpu_calculator.py --units 100 --unit-rate 0.5
"""
import argparse
from decimal import Decimal, InvalidOperation


def nonnegative(value):
    """Parse finite nonnegative money or usage without float rounding."""
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("Enter a decimal number") from exc
    if not number.is_finite() or number < 0:
        raise argparse.ArgumentTypeError("Value must be finite and >= 0")
    return number


def calculate(args):
    """One-time charges apply once, including when annualizing."""
    excess = max(Decimal(0), args.units - args.included)
    variable = excess * args.unit_rate + args.extras
    monthly = args.base + variable
    first_year = monthly * 12 + args.one_time
    renewal = monthly * 12
    annual_quote = args.annual_base
    alternative = None if annual_quote is None else annual_quote + variable * 12 + args.one_time
    return monthly, first_year, renewal, alternative


def main():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--units', type=nonnegative, required=True,
        help='Monthly billed GPU-hours; include retries/idle consumption')
    parser.add_argument('--unit-rate', type=nonnegative, required=True,
        help='USD per unit above included allowance')
    parser.add_argument('--included', type=nonnegative, default=Decimal(0))
    parser.add_argument('--base', type=nonnegative, default=Decimal(0),
        help='Monthly recurring base charge in USD')
    parser.add_argument('--extras', type=nonnegative, default=Decimal(0),
        help='Additional monthly storage, transfer, taxes or other costs')
    parser.add_argument('--one-time', type=nonnegative, default=Decimal(0),
        help='First-year-only setup/formation/other fees')
    parser.add_argument('--annual-base', type=nonnegative,
        help='Optional annual base quote with SAME allowance and usage terms')
    args = parser.parse_args()
    monthly, first_year, renewal, alternative = calculate(args)
    print('RunPod GPU | USD | user-supplied rates')
    print(f'Recurring monthly estimate: ${monthly:.2f}')
    print(f'First month including setup: ${monthly + args.one_time:.2f}')
    print(f'First year, monthly billing: ${first_year:.2f}')
    print(f'Later year at unchanged rates: ${renewal:.2f}')
    if alternative is not None:
        print(f'First year, annual base quote: ${alternative:.2f}')
        print(f'Annual-quote saving: ${first_year - alternative:.2f}')
    print('Estimate only. Confirm scope, tax, renewal and eligibility at checkout.')


if __name__ == '__main__':
    main()
