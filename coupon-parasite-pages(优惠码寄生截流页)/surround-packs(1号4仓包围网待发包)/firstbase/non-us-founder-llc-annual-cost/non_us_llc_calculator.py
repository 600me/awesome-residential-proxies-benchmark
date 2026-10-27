#!/usr/bin/env python3
"""
Foreign-Owned Single-Member US LLC Maintenance Cost Simulator.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def simulate_llc_carry(state_report: Decimal, agent_fee: Decimal, form_5472_prep: Decimal, mail_forwarding: Decimal):
    annual_mandatory = state_report + agent_fee + form_5472_prep
    annual_total = annual_mandatory + mail_forwarding
    return {
        'annual_mandatory_compliance': annual_mandatory.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'mail_forwarding': mail_forwarding.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        'total_annual_carry': annual_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    }

def main():
    parser = argparse.ArgumentParser(description="Non-US Founder LLC Annual Compliance Cost Simulator")
    parser.add_argument('--state-report', type=Decimal, default=Decimal('60.00'), help='State annual report fee (WY=$60, DE=$300)')
    parser.add_argument('--agent-fee', type=Decimal, default=Decimal('99.00'), help='Registered agent fee ($99/yr)')
    parser.add_argument('--tax-prep', type=Decimal, default=Decimal('500.00'), help='IRS Form 5472 & 1120 filing preparation ($500)')
    parser.add_argument('--mail-forwarding', type=Decimal, default=Decimal('120.00'), help='Virtual address / scanning ($10/mo = $120/yr)')
    args = parser.parse_args()

    res = simulate_llc_carry(args.state_report, args.agent_fee, args.tax_prep, args.mail_forwarding)
    print("=== Non-US Founder LLC Annual Carry ===")
    print(f"Mandatory State & Tax Compliance: ${res['annual_mandatory_compliance']}/year")
    print(f"Mail/Address Service:             ${res['mail_forwarding']}/year")
    print(f"Total True Annual Carry:          ${res['total_annual_carry']}/year")

if __name__ == '__main__':
    main()
