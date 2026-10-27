#!/usr/bin/env python3
"""
Doola Compliance Bundle vs Firstbase Modular CPA Approach.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def compare_doola_firstbase(years: int, cpa_fee: Decimal):
    doola_total = Decimal('1999.00') * Decimal(str(years))
    firstbase_y1 = Decimal('499.00') + cpa_fee
    firstbase_annual = Decimal('159.00') + cpa_fee
    firstbase_total = firstbase_y1 + (firstbase_annual * Decimal(str(max(0, years - 1))))
    savings = (doola_total - firstbase_total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
        'doola_total': doola_total,
        'firstbase_total': firstbase_total,
        'savings': savings
    }

def main():
    parser = argparse.ArgumentParser(description="Doola vs Firstbase Total Cost Comparison")
    parser.add_argument('--years', type=int, default=2, help='Timeline in years')
    parser.add_argument('--cpa-fee', type=Decimal, default=Decimal('600.00'), help='External CPA fee for Form 5472 ($600)')
    args = parser.parse_args()

    res = compare_doola_firstbase(args.years, args.cpa_fee)
    print("=== Doola vs Firstbase Compliance Cost ===")
    print(f"Doola Total ({args.years}y):       ${res['doola_total']}")
    print(f"Firstbase + CPA ({args.years}y): ${res['firstbase_total']}")
    print(f"Net Realized Savings:    ${res['savings']}")

if __name__ == '__main__':
    main()
