#!/usr/bin/env python3
"""
Decodo (Smartproxy) Bandwidth Cost & Tiered Savings Calculator.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

TIERS = {
    'payg': Decimal('4.00'),
    'starter_50gb': Decimal('3.75'),
    'growth_100gb': Decimal('2.75'),
    'enterprise_500gb': Decimal('2.20')
}

def calculate_decodo_costs(gb_volume: Decimal, tier: str, annual_discount_pct: Decimal):
    rate = TIERS.get(tier, Decimal('4.00'))
    payg_baseline_rate = Decimal('4.00')

    monthly_payg_baseline = (gb_volume * payg_baseline_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    monthly_plan_cost = (gb_volume * rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    annual_multiplier = (Decimal('100') - annual_discount_pct) / Decimal('100')
    annual_total = (monthly_plan_cost * Decimal('12') * annual_multiplier).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    monthly_effective = (annual_total / Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    annual_payg_baseline = (monthly_payg_baseline * Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    annual_net_savings = (annual_payg_baseline - annual_total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        'rate_per_gb': rate,
        'monthly_cost': monthly_plan_cost,
        'annual_total': annual_total,
        'monthly_effective': monthly_effective,
        'baseline_payg_annual': annual_payg_baseline,
        'annual_savings_vs_payg': annual_net_savings
    }

def main():
    parser = argparse.ArgumentParser(description="Decodo Residential Proxy Bandwidth & Tiered Cost Calculator")
    parser.add_argument('--volume-gb', type=Decimal, default=Decimal('100'), help='Monthly proxy bandwidth consumption in GB (default: 100)')
    parser.add_argument('--tier', choices=list(TIERS.keys()), default='growth_100gb', help='Decodo volume tier (default: growth_100gb @ $2.75/GB)')
    parser.add_argument('--annual-discount', type=Decimal, default=Decimal('10.0'), help='Annual billing discount percentage (default: 10.0 pct)')
    args = parser.parse_args()

    res = calculate_decodo_costs(args.volume_gb, args.tier, args.annual_discount)
    print("=== Decodo (Smartproxy) Cost Breakdown ===")
    print(f"Volume:                  {args.volume_gb} GB/month")
    print(f"Tier Rate:               ${res['rate_per_gb']} / GB")
    print(f"Monthly Cost:            ${res['monthly_cost']}")
    print(f"Annual Total (Billed 1y):${res['annual_total']}")
    print(f"Effective Monthly:       ${res['monthly_effective']}")
    print(f"Annual Savings vs PAYG:  ${res['annual_savings_vs_payg']}")

if __name__ == '__main__':
    main()
