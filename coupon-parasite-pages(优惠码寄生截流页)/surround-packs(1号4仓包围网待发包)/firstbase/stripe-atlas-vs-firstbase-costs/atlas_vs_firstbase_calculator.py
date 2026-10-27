#!/usr/bin/env python3
"""
Stripe Atlas (Delaware) vs Firstbase (Wyoming) 3-Year TCO Comparison.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def compare_atlas_firstbase(years: int):
    # Stripe Atlas: $500 upfront (DE only). Year 2+ $100 Registered Agent + $300 DE Tax
    atlas_y1 = Decimal('500.00')
    atlas_annual = Decimal('400.00')
    atlas_total = atlas_y1 + (atlas_annual * Decimal(str(max(0, years - 1))))

    # Firstbase Wyoming: $399 base + $100 WY fee = $499. Year 2+ $99 Agent + $60 WY Report = $159/yr
    firstbase_y1 = Decimal('499.00')
    firstbase_annual = Decimal('159.00')
    firstbase_total = firstbase_y1 + (firstbase_annual * Decimal(str(max(0, years - 1))))

    difference = (atlas_total - firstbase_total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
        'atlas_total': atlas_total,
        'firstbase_total': firstbase_total,
        'net_savings': difference
    }

def main():
    parser = argparse.ArgumentParser(description="Stripe Atlas vs Firstbase TCO Comparison")
    parser.add_argument('--years', type=int, default=3, help='Projection years (default: 3)')
    args = parser.parse_args()

    res = compare_atlas_firstbase(args.years)
    print("=== Stripe Atlas vs Firstbase 3-Year Comparison ===")
    print(f"Stripe Atlas Total:      ${res['atlas_total']}")
    print(f"Firstbase Total:         ${res['firstbase_total']}")
    print(f"Total Bootstrapper Savings: ${res['net_savings']}")

if __name__ == '__main__':
    main()
