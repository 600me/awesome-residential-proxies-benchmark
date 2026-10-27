#!/usr/bin/env python3
"""
ScrapingBee vs ScraperAPI Headless Scraping Comparison.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def compare_bee_sapi(pages: Decimal):
    # ScrapingBee: 5 credits/JS request. 
    # Entry plan $49 = 150k credits (30k JS pages, 5 concurrency)
    # Business $99 = 1M credits (200k JS pages, 10-20 concurrency)
    bee_cost = Decimal('49.00') if pages <= Decimal('30000') else Decimal('99.00') if pages <= Decimal('200000') else Decimal('249.00')
    sapi_cost = Decimal('49.00') if pages <= Decimal('20000') else Decimal('149.00') if pages <= Decimal('200000') else Decimal('299.00')

    return {
        'scrapingbee_monthly': bee_cost,
        'scraperapi_monthly': sapi_cost,
        'concurrency_advantage': 'ScraperAPI provides up to 50 concurrent threads on Startup'
    }

def main():
    parser = argparse.ArgumentParser(description="ScrapingBee vs ScraperAPI Cost & Concurrency Comparison")
    parser.add_argument('--pages', type=Decimal, default=Decimal('100000'), help='Monthly JS pages to crawl')
    args = parser.parse_args()

    res = compare_bee_sapi(args.pages)
    print("=== ScrapingBee vs ScraperAPI Breakdown ===")
    print(f"Target JS Pages:         {args.pages}")
    print(f"ScrapingBee Monthly:     ${res['scrapingbee_monthly']}")
    print(f"ScraperAPI Monthly:      ${res['scraperapi_monthly']}")
    print(f"Concurrency Note:        {res['concurrency_advantage']}")

if __name__ == '__main__':
    main()
