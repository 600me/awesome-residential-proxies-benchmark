#!/usr/bin/env python3
"""
Oxylabs vs Decodo (Smartproxy) Residential Proxy Cost Comparison.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def compare_oxylabs_decodo(volume_gb: Decimal, oxy_min_commit: Decimal, oxy_payg_rate: Decimal, decodo_rate: Decimal):
    oxy_cost = max(oxy_min_commit, volume_gb * oxy_payg_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    decodo_cost = (volume_gb * decodo_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    monthly_diff = (oxy_cost - decodo_cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
        'oxylabs_cost': oxy_cost,
        'decodo_cost': decodo_cost,
        'monthly_savings': monthly_diff,
        'annual_savings': (monthly_diff * Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    }

def main():
    parser = argparse.ArgumentParser(description="Oxylabs vs Decodo Proxy Cost Comparison")
    parser.add_argument('--volume-gb', type=Decimal, default=Decimal('35'), help='Monthly proxy bandwidth in GB')
    parser.add_argument('--oxy-min-commit', type=Decimal, default=Decimal('300.00'), help='Oxylabs entry commitment ($300)')
    parser.add_argument('--oxy-payg-rate', type=Decimal, default=Decimal('8.00'), help='Oxylabs Pay-as-you-go rate ($8/GB)')
    parser.add_argument('--decodo-rate', type=Decimal, default=Decimal('4.00'), help='Decodo PAYG rate ($4/GB)')
    args = parser.parse_args()

    res = compare_oxylabs_decodo(args.volume_gb, args.oxy_min_commit, args.oxy_payg_rate, args.decodo_rate)
    print("=== Oxylabs vs Decodo Budget Comparison ===")
    print(f"Bandwidth:               {args.volume_gb} GB/month")
    print(f"Oxylabs Effective Cost:  ${res['oxylabs_cost']}/mo")
    print(f"Decodo Cost:             ${res['decodo_cost']}/mo")
    print(f"Net Monthly Savings:     ${res['monthly_savings']}/mo")
    print(f"Annual Savings:          ${res['annual_savings']}/year")

if __name__ == '__main__':
    main()
