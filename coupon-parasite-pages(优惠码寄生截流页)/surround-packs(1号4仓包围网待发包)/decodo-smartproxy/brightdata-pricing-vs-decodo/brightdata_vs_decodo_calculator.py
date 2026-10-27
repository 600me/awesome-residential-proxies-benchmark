#!/usr/bin/env python3
"""
Bright Data vs Decodo (Smartproxy) Head-to-Head Scraping Budget Comparison.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def compare_costs(volume_gb: Decimal, bright_rate: Decimal, decodo_rate: Decimal):
    bright_monthly = (volume_gb * bright_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    decodo_monthly = (volume_gb * decodo_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    monthly_diff = (bright_monthly - decodo_monthly).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    annual_diff = (monthly_diff * Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
        'bright_monthly': bright_monthly,
        'decodo_monthly': decodo_monthly,
        'monthly_savings': monthly_diff,
        'annual_savings': annual_diff
    }

def main():
    parser = argparse.ArgumentParser(description="Bright Data vs Decodo Proxy Cost Comparison")
    parser.add_argument('--volume-gb', type=Decimal, default=Decimal('80'), help='Monthly bandwidth in GB (default: 80)')
    parser.add_argument('--bright-rate', type=Decimal, default=Decimal('8.40'), help='Bright Data rate per GB (default: 8.40)')
    parser.add_argument('--decodo-rate', type=Decimal, default=Decimal('3.75'), help='Decodo rate per GB (default: 3.75)')
    args = parser.parse_args()

    res = compare_costs(args.volume_gb, args.bright_rate, args.decodo_rate)
    print("=== Bright Data vs Decodo Monthly Comparison ===")
    print(f"Monthly Traffic:         {args.volume_gb} GB")
    print(f"Bright Data (@${args.bright_rate}/GB):  ${res['bright_monthly']}/mo")
    print(f"Decodo (@${args.decodo_rate}/GB):       ${res['decodo_monthly']}/mo")
    print(f"Monthly Savings:         ${res['monthly_savings']}/mo")
    print(f"Annual Total Savings:    ${res['annual_savings']}/year")

if __name__ == '__main__':
    main()
