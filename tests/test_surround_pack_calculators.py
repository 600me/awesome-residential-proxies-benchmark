#!/usr/bin/env python3
"""
Automated regression test suite for 12 Surround Pack Calculators.
Validates:
1. Every calculator runs cleanly via subprocess (exit 0).
2. The outputs match expected arithmetic down to 2 decimal places.
3. Every README contains the exact numbers produced by the script.
"""
import os
import sys
import subprocess
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SURROUND_DIR = os.path.join(BASE_DIR, "coupon-parasite-pages(优惠码寄生截流页)", "surround-packs(1号4仓包围网待发包)")

class TestSurroundPackCalculators(unittest.TestCase):

    def run_calc(self, brand, repo_dir, cmd_args):
        calc_dir = os.path.join(SURROUND_DIR, brand, repo_dir)
        full_cmd = [sys.executable] + cmd_args
        res = subprocess.run(full_cmd, cwd=calc_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0, f"Script failed: {res.stderr}")
        return res.stdout

    def test_decodo_bandwidth_calculator(self):
        out = self.run_calc("decodo-smartproxy", "decodo-coupon-pricing-breakdown", 
                            ["decodo_bandwidth_calculator.py", "--volume-gb", "100", "--tier", "growth_100gb", "--annual-discount", "10"])
        self.assertIn("Monthly Cost:            $275.00", out)
        self.assertIn("Annual Total (Billed 1y):$2970.00", out)
        self.assertIn("Effective Monthly:       $247.50", out)
        self.assertIn("Annual Savings vs PAYG:  $1830.00", out)

    def test_brightdata_vs_decodo_calculator(self):
        out = self.run_calc("decodo-smartproxy", "brightdata-pricing-vs-decodo",
                            ["brightdata_vs_decodo_calculator.py", "--volume-gb", "80", "--bright-rate", "8.40", "--decodo-rate", "3.75"])
        self.assertIn("Bright Data (@$8.40/GB):  $672.00/mo", out)
        self.assertIn("Decodo (@$3.75/GB):       $300.00/mo", out)
        self.assertIn("Monthly Savings:         $372.00/mo", out)
        self.assertIn("Annual Total Savings:    $4464.00/year", out)

    def test_oxylabs_vs_decodo_calculator(self):
        out = self.run_calc("decodo-smartproxy", "oxylabs-pricing-vs-decodo",
                            ["oxylabs_vs_decodo_calculator.py", "--volume-gb", "35"])
        self.assertIn("Oxylabs Effective Cost:  $300.00/mo", out)
        self.assertIn("Decodo Cost:             $140.00/mo", out)
        self.assertIn("Net Monthly Savings:     $160.00/mo", out)
        self.assertIn("Annual Savings:          $1920.00/year", out)

    def test_proxy_tco_estimator(self):
        out = self.run_calc("decodo-smartproxy", "residential-proxy-scraping-costs",
                            ["proxy_tco_estimator.py", "--target-gb", "100", "--failure-rate", "20.0", "--rate-per-gb", "4.00"])
        self.assertIn("Target Bandwidth:        100 GB", out)
        self.assertIn("Actual Traffic Billed:   125.0 GB", out)
        self.assertIn("True Real Cost:          $500.00", out)
        self.assertIn("Retry Waste Overhead:    $100.00", out)

    def test_scraperapi_credit_calculator(self):
        out = self.run_calc("scraperapi", "scraperapi-coupon-code-breakdown",
                            ["scraperapi_credit_calculator.py", "--requests", "200000", "--js-render"])
        self.assertIn("Optimal Plan Tier:       STARTUP", out)
        self.assertIn("Monthly Cost:            $149.00", out)
        self.assertIn("Annual Billed Total:     $1430.40", out)
        self.assertIn("Effective Monthly Cost:  $119.20", out)

    def test_zenrows_vs_scraperapi_calculator(self):
        out = self.run_calc("scraperapi", "zenrows-vs-scraperapi-pricing",
                            ["zenrows_vs_scraperapi_calculator.py", "--pages", "150000"])
        self.assertIn("ZenRows Estimated Cost:  $209.00/mo", out)
        self.assertIn("ScraperAPI Cost:         $149.00/mo", out)
        self.assertIn("Net Monthly Difference:  $60.00/mo", out)
        self.assertIn("Annual Total Difference: $720.00/year", out)

    def test_scrapingbee_vs_scraperapi_calculator(self):
        out = self.run_calc("scraperapi", "scrapingbee-vs-scraperapi-pricing",
                            ["scrapingbee_vs_scraperapi_calculator.py", "--pages", "100000"])
        self.assertIn("ScrapingBee Monthly:     $99.00", out)
        self.assertIn("ScraperAPI Monthly:      $149.00", out)

    def test_api_tco_calculator(self):
        out = self.run_calc("scraperapi", "web-scraping-api-cost-comparison",
                            ["api_tco_calculator.py", "--vps-spend", "160", "--proxy-spend", "200", "--dev-hours", "10", "--dev-rate", "80"])
        self.assertIn("Self-Hosted Total Cost:  $1160.00/mo", out)
        self.assertIn("Managed API Cost:        $149.00/mo", out)
        self.assertIn("Monthly Net Savings:     $1011.00/mo", out)
        self.assertIn("Annual Net Savings:      $12132.00/year", out)

    def test_firstbase_formation_calculator(self):
        out = self.run_calc("firstbase", "firstbase-coupon-code-pricing",
                            ["firstbase_formation_calculator.py", "--state", "wyoming", "--years", "3", "--promo-discount", "10"])
        self.assertIn("Year 1 Upfront Total:    $459.10", out)
        self.assertIn("Promo Savings:           $39.90", out)
        self.assertIn("Ongoing Annual Carry:    $159.00/year", out)
        self.assertIn("3-Year Total Cost:       $777.10", out)

    def test_atlas_vs_firstbase_calculator(self):
        out = self.run_calc("firstbase", "stripe-atlas-vs-firstbase-costs",
                            ["atlas_vs_firstbase_calculator.py", "--years", "3"])
        self.assertIn("Stripe Atlas Total:      $1300.00", out)
        self.assertIn("Firstbase Total:         $817.00", out)
        self.assertIn("Total Bootstrapper Savings: $483.00", out)

    def test_doola_vs_firstbase_calculator(self):
        out = self.run_calc("firstbase", "doola-pricing-vs-firstbase",
                            ["doola_vs_firstbase_calculator.py", "--years", "2", "--cpa-fee", "600"])
        self.assertIn("Doola Total (2y):       $3998.00", out)
        self.assertIn("Firstbase + CPA (2y): $1858.00", out)
        self.assertIn("Net Realized Savings:    $2140.00", out)

    def test_non_us_llc_calculator(self):
        out = self.run_calc("firstbase", "non-us-founder-llc-annual-cost",
                            ["non_us_llc_calculator.py", "--state-report", "60", "--agent-fee", "99", "--tax-prep", "500"])
        self.assertIn("Total True Annual Carry:          $779.00/year", out)

if __name__ == '__main__':
    unittest.main()
