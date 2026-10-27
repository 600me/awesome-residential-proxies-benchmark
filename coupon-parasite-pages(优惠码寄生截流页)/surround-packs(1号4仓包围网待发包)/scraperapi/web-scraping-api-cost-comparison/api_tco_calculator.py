#!/usr/bin/env python3
"""
Self-Hosted Headless Scraper vs Managed Web Scraping API TCO Calculator.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def calculate_scraping_tco(vps_spend: Decimal, proxy_spend: Decimal, dev_hours: Decimal, dev_hourly_rate: Decimal, api_plan_cost: Decimal):
    dev_spend = (dev_hours * dev_hourly_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    self_hosted_monthly = (vps_spend + proxy_spend + dev_spend).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    monthly_savings = (self_hosted_monthly - api_plan_cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    annual_savings = (monthly_savings * Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
        'self_hosted_total': self_hosted_monthly,
        'dev_maintenance_cost': dev_spend,
        'api_plan_cost': api_plan_cost,
        'monthly_net_savings': monthly_savings,
        'annual_net_savings': annual_savings
    }

def main():
    parser = argparse.ArgumentParser(description="Self-Hosted vs Managed Scraping API TCO Calculator")
    parser.add_argument('--vps-spend', type=Decimal, default=Decimal('160.00'), help='Monthly VPS server costs for browser cluster ($160)')
    parser.add_argument('--proxy-spend', type=Decimal, default=Decimal('200.00'), help='Monthly residential proxy bandwidth cost ($200)')
    parser.add_argument('--dev-hours', type=Decimal, default=Decimal('10.0'), help='Monthly dev hours fixing anti-bot blocks (10 hrs)')
    parser.add_argument('--dev-rate', type=Decimal, default=Decimal('80.00'), help='Developer hourly wage ($80/hr)')
    parser.add_argument('--api-cost', type=Decimal, default=Decimal('149.00'), help='Managed ScraperAPI plan ($149/mo)')
    args = parser.parse_args()

    res = calculate_scraping_tco(args.vps_spend, args.proxy_spend, args.dev_hours, args.dev_rate, args.api_cost)
    print("=== Scraping Infrastructure TCO ===")
    print(f"Self-Hosted Total Cost:  ${res['self_hosted_total']}/mo (Infrastructure + Dev)")
    print(f"Developer Time Waste:    ${res['dev_maintenance_cost']}/mo")
    print(f"Managed API Cost:        ${res['api_plan_cost']}/mo")
    print(f"Monthly Net Savings:     ${res['monthly_net_savings']}/mo")
    print(f"Annual Net Savings:      ${res['annual_net_savings']}/year")

if __name__ == '__main__':
    main()
