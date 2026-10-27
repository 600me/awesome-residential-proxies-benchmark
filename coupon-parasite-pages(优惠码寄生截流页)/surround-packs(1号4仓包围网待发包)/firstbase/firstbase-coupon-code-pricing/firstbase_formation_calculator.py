#!/usr/bin/env python3
"""
Firstbase US Company Formation & Multi-Year Maintenance Calculator.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

STATE_FEES = {
    'wyoming': {'state_fee': Decimal('100.00'), 'annual_report': Decimal('60.00')},
    'delaware': {'state_fee': Decimal('90.00'), 'annual_report': Decimal('300.00')}
}

def calculate_firstbase(state: str, years: int, promo_discount_pct: Decimal, include_mailroom: bool):
    base_package = Decimal('399.00')
    discount_multiplier = (Decimal('100') - promo_discount_pct) / Decimal('100')
    discounted_base = (base_package * discount_multiplier).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    state_info = STATE_FEES.get(state, STATE_FEES['wyoming'])
    year1_state_fee = state_info['state_fee']
    annual_compliance_fee = state_info['annual_report'] + Decimal('99.00') # $99/yr registered agent after yr 1
    
    mailroom_annual = Decimal('35.00') * Decimal('12') if include_mailroom else Decimal('0.00')

    year1_total = discounted_base + year1_state_fee + mailroom_annual
    subsequent_years_total = (annual_compliance_fee + mailroom_annual) * Decimal(str(max(0, years - 1)))
    cumulative_total = year1_total + subsequent_years_total

    return {
        'year1_upfront': year1_total,
        'annual_maintenance_ongoing': annual_compliance_fee + mailroom_annual,
        'cumulative_total': cumulative_total,
        'promo_discount_saved': (base_package - discounted_base).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    }

def main():
    parser = argparse.ArgumentParser(description="Firstbase US Company Formation & Maintenance Calculator")
    parser.add_argument('--state', choices=['wyoming', 'delaware'], default='wyoming', help='Incorporation state (default: wyoming)')
    parser.add_argument('--years', type=int, default=3, help='Total projection horizon in years (default: 3)')
    parser.add_argument('--promo-discount', type=Decimal, default=Decimal('10.0'), help='Promo discount percentage (default: 10.0 pct)')
    parser.add_argument('--mailroom', action='store_true', help='Include virtual US physical address and mailroom ($35/mo)')
    args = parser.parse_args()

    res = calculate_firstbase(args.state, args.years, args.promo_discount, args.mailroom)
    print(f"=== Firstbase US Formation ({args.state.upper()}) ===")
    print(f"Year 1 Upfront Total:    ${res['year1_upfront']}")
    print(f"Promo Savings:           ${res['promo_discount_saved']}")
    print(f"Ongoing Annual Carry:    ${res['annual_maintenance_ongoing']}/year")
    print(f"{args.years}-Year Total Cost:       ${res['cumulative_total']}")

if __name__ == '__main__':
    main()
