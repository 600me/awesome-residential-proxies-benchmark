#!/usr/bin/env python3
"""
ZenRows vs ScraperAPI Anti-Bot Scraping Cost Comparison.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def compare_api(pages: Decimal):
    # ZenRows: 5 credits/page JS. $69 gives 250k credits (50k pages). Extra pages ~$1.40/1k pages
    zr_base = Decimal('69.00')
    zr_included_pages = Decimal('50000')
    zr_cost = zr_base
    if pages > zr_included_pages:
        extra_pages = pages - zr_included_pages
        zr_cost += (extra_pages / Decimal('1000')) * Decimal('1.40')
    
    # ScraperAPI: 5 credits/page JS. $149 Startup gives 1M credits (200k pages).
    sapi_cost = Decimal('149.00') if pages <= Decimal('200000') else Decimal('299.00')

    zr_cost = zr_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    sapi_cost = sapi_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    diff = (zr_cost - sapi_cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        'zenrows_monthly': zr_cost,
        'scraperapi_monthly': sapi_cost,
        'monthly_savings': diff,
        'annual_savings': (diff * Decimal('12')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    }

def main():
    parser = argparse.ArgumentParser(description="ZenRows vs ScraperAPI Scraping Cost Comparison")
    parser.add_argument('--pages', type=Decimal, default=Decimal('150000'), help='Monthly JavaScript rendered pages')
    args = parser.parse_args()

    res = compare_api(args.pages)
    print("=== ZenRows vs ScraperAPI Comparison ===")
    print(f"Monthly JS Pages:        {args.pages}")
    print(f"ZenRows Estimated Cost:  ${res['zenrows_monthly']}/mo")
    print(f"ScraperAPI Cost:         ${res['scraperapi_monthly']}/mo")
    print(f"Net Monthly Difference:  ${res['monthly_savings']}/mo")
    print(f"Annual Total Difference: ${res['annual_savings']}/year")

if __name__ == '__main__':
    main()
