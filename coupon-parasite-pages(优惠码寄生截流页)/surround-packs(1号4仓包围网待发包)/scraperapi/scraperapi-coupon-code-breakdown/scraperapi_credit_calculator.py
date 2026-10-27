#!/usr/bin/env python3
"""
ScraperAPI Credit Math & Plan Selector Calculator.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

PLANS = {
    'hobby': {'price': Decimal('49.00'), 'credits': Decimal('100000')},
    'startup': {'price': Decimal('149.00'), 'credits': Decimal('1000000')},
    'business': {'price': Decimal('299.00'), 'credits': Decimal('3000000')}
}

def calculate_scraperapi(requests: Decimal, js_render: bool, residential: bool, annual_discount_pct: Decimal):
    multiplier = Decimal('1')
    if residential:
        multiplier = Decimal('25')
    elif js_render:
        multiplier = Decimal('5')

    total_credits = requests * multiplier

    # Select best fitting plan
    selected_plan = 'business'
    if total_credits <= Decimal('100000'):
        selected_plan = 'hobby'
    elif total_credits <= Decimal('1000000'):
        selected_plan = 'startup'

    plan_base_price = PLANS[selected_plan]['price']
    plan_credits = PLANS[selected_plan]['credits']

    overage_cost = Decimal('0.00')
    if total_credits > plan_credits:
        overage_units = ((total_credits - plan_credits) / Decimal('10000')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        overage_cost = (overage_units * Decimal('2.50')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    monthly_total = plan_base_price + overage_cost
    annual_discount_factor = (Decimal('100') - annual_discount_pct) / Decimal('100')
    annual_total = (monthly_total * Decimal('12') * annual_discount_factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    monthly_effective = (annual_total / Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        'total_credits_needed': total_credits,
        'recommended_plan': selected_plan,
        'monthly_cost': monthly_total,
        'annual_total': annual_total,
        'monthly_effective': monthly_effective,
        'credit_multiplier': multiplier
    }

def main():
    parser = argparse.ArgumentParser(description="ScraperAPI Monthly Credit & Plan Calculator")
    parser.add_argument('--requests', type=Decimal, default=Decimal('200000'), help='Monthly target scraping requests (default: 200,000)')
    parser.add_argument('--js-render', action='store_true', help='Enable headless browser JS rendering (5x multiplier)')
    parser.add_argument('--residential', action='store_true', help='Enable premium residential IP proxy routing (25x multiplier)')
    parser.add_argument('--annual-discount', type=Decimal, default=Decimal('20.0'), help='Annual billing discount percentage (default: 20.0 pct)')
    args = parser.parse_args()

    res = calculate_scraperapi(args.requests, args.js_render, args.residential, args.annual_discount)
    print("=== ScraperAPI Credit & Budget Calculation ===")
    print(f"Target Requests:         {args.requests}")
    print(f"Credit Multiplier:       {res['credit_multiplier']}x")
    print(f"Total Credits Required:  {res['total_credits_needed']}")
    print(f"Optimal Plan Tier:       {res['recommended_plan'].upper()}")
    print(f"Monthly Cost:            ${res['monthly_cost']}")
    print(f"Annual Billed Total:     ${res['annual_total']}")
    print(f"Effective Monthly Cost:  ${res['monthly_effective']}")

if __name__ == '__main__':
    main()
