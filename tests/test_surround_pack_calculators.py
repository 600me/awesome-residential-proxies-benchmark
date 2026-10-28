#!/usr/bin/env python3
"""
Automated regression test suite for 20 Surround Pack Calculators (12 Deployed + 8 Staged).
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

    def check_readme(self, brand, repo_dir, expected_snippets):
        readme_path = os.path.join(SURROUND_DIR, brand, repo_dir, "README.md")
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        for s in expected_snippets:
            self.assertIn(s, content, f"Snippet '{s}' not found in {readme_path}")

    def test_decodo_bandwidth_calculator(self):
        out = self.run_calc("decodo-smartproxy", "decodo-coupon-pricing-breakdown", 
                            ["decodo_bandwidth_calculator.py", "--volume-gb", "100", "--tier", "growth_100gb", "--annual-discount", "10"])
        self.assertIn("Monthly Cost:            $275.00", out)
        self.assertIn("Annual Total (Billed 1y):$2970.00", out)
        self.assertIn("Effective Monthly:       $247.50", out)
        self.assertIn("Annual Savings vs PAYG:  $1830.00", out)
        self.check_readme("decodo-smartproxy", "decodo-coupon-pricing-breakdown",
                          ["$400.00/month", "$247.50/month", "$2,970.00/year", "$1,830.00/year"])

    def test_brightdata_vs_decodo_calculator(self):
        out = self.run_calc("decodo-smartproxy", "brightdata-pricing-vs-decodo",
                            ["brightdata_vs_decodo_calculator.py", "--volume-gb", "80", "--bright-rate", "8.40", "--decodo-rate", "3.75"])
        self.assertIn("Bright Data (@$8.40/GB):  $672.00/mo", out)
        self.assertIn("Decodo (@$3.75/GB):       $300.00/mo", out)
        self.assertIn("Monthly Savings:         $372.00/mo", out)
        self.assertIn("Annual Total Savings:    $4464.00/year", out)
        self.check_readme("decodo-smartproxy", "brightdata-pricing-vs-decodo",
                          ["$672.00/month", "$300.00/month", "$372.00/month", "$4,464.00/year"])

    def test_oxylabs_vs_decodo_calculator(self):
        out = self.run_calc("decodo-smartproxy", "oxylabs-pricing-vs-decodo",
                            ["oxylabs_vs_decodo_calculator.py", "--volume-gb", "35"])
        self.assertIn("Oxylabs Effective Cost:  $300.00/mo", out)
        self.assertIn("Decodo Cost:             $140.00/mo", out)
        self.assertIn("Net Monthly Savings:     $160.00/mo", out)
        self.assertIn("Annual Savings:          $1920.00/year", out)
        self.check_readme("decodo-smartproxy", "oxylabs-pricing-vs-decodo",
                          ["$300.00/month", "$140.00/month", "$160.00/month", "$1,920.00/year"])

    def test_proxy_tco_estimator(self):
        out = self.run_calc("decodo-smartproxy", "residential-proxy-scraping-costs",
                            ["proxy_tco_estimator.py", "--target-gb", "100", "--failure-rate", "20.0", "--rate-per-gb", "4.00"])
        self.assertIn("Target Bandwidth:        100 GB", out)
        self.assertIn("Actual Traffic Billed:   125.0 GB", out)
        self.assertIn("True Real Cost:          $500.00", out)
        self.assertIn("Retry Waste Overhead:    $100.00", out)
        self.check_readme("decodo-smartproxy", "residential-proxy-scraping-costs",
                          ["125.0 GB", "$500.00", "$100.00/month", "$1,200.00/year"])

    def test_scraperapi_credit_calculator(self):
        out = self.run_calc("scraperapi", "scraperapi-coupon-code-breakdown",
                            ["scraperapi_credit_calculator.py", "--requests", "200000", "--js-render"])
        self.assertIn("Optimal Plan Tier:       STARTUP", out)
        self.assertIn("Monthly Cost:            $149.00", out)
        self.assertIn("Annual Billed Total:     $1430.40", out)
        self.assertIn("Effective Monthly Cost:  $119.20", out)
        self.check_readme("scraperapi", "scraperapi-coupon-code-breakdown",
                          ["$225.00", "$274.00/month", "$119.20/month", "$1,430.40/year", "$1,857.60/year"])

    def test_zenrows_vs_scraperapi_calculator(self):
        out = self.run_calc("scraperapi", "zenrows-vs-scraperapi-pricing",
                            ["zenrows_vs_scraperapi_calculator.py", "--pages", "150000"])
        self.assertIn("ZenRows Estimated Cost:  $209.00/mo", out)
        self.assertIn("ScraperAPI Cost:         $149.00/mo", out)
        self.assertIn("Net Monthly Difference:  $60.00/mo", out)
        self.assertIn("Annual Total Difference: $720.00/year", out)
        self.check_readme("scraperapi", "zenrows-vs-scraperapi-pricing",
                          ["$209.00/month", "$149.00", "$60.00/month", "$720.00/year"])

    def test_scrapingbee_vs_scraperapi_calculator(self):
        out = self.run_calc("scraperapi", "scrapingbee-vs-scraperapi-pricing",
                            ["scrapingbee_vs_scraperapi_calculator.py", "--pages", "100000"])
        self.assertIn("ScrapingBee Monthly:     $99.00", out)
        self.assertIn("ScraperAPI Monthly:      $149.00", out)
        self.check_readme("scraperapi", "scrapingbee-vs-scraperapi-pricing",
                          ["$99.00/month", "$149.00/month"])

    def test_api_tco_calculator(self):
        out = self.run_calc("scraperapi", "web-scraping-api-cost-comparison",
                            ["api_tco_calculator.py", "--vps-spend", "160", "--proxy-spend", "200", "--dev-hours", "10", "--dev-rate", "80"])
        self.assertIn("Self-Hosted Total Cost:  $1160.00/mo", out)
        self.assertIn("Managed API Cost:        $149.00/mo", out)
        self.assertIn("Monthly Net Savings:     $1011.00/mo", out)
        self.assertIn("Annual Net Savings:      $12132.00/year", out)
        self.check_readme("scraperapi", "web-scraping-api-cost-comparison",
                          ["$1,160.00/month", "$149.00/month", "$1,011.00/month", "$12,132.00/year"])

    def test_firstbase_formation_calculator(self):
        out = self.run_calc("firstbase", "firstbase-coupon-code-pricing",
                            ["firstbase_formation_calculator.py", "--state", "wyoming", "--years", "3", "--promo-discount", "10"])
        self.assertIn("Year 1 Upfront Total:    $459.10", out)
        self.assertIn("Promo Savings:           $39.90", out)
        self.assertIn("Ongoing Annual Carry:    $159.00/year", out)
        self.assertIn("3-Year Total Cost:       $777.10", out)
        self.check_readme("firstbase", "firstbase-coupon-code-pricing",
                          ["$459.10", "$39.90", "$159.00/year", "$777.10", "$470.00"])

    def test_atlas_vs_firstbase_calculator(self):
        out = self.run_calc("firstbase", "stripe-atlas-vs-firstbase-costs",
                            ["atlas_vs_firstbase_calculator.py", "--years", "3"])
        self.assertIn("Stripe Atlas Total:      $1300.00", out)
        self.assertIn("Firstbase Total:         $817.00", out)
        self.assertIn("Total Bootstrapper Savings: $483.00", out)
        self.check_readme("firstbase", "stripe-atlas-vs-firstbase-costs",
                          ["$1,300.00", "$817.00", "$483.00"])

    def test_doola_vs_firstbase_calculator(self):
        out = self.run_calc("firstbase", "doola-pricing-vs-firstbase",
                            ["doola_vs_firstbase_calculator.py", "--years", "2", "--cpa-fee", "600"])
        self.assertIn("Doola Total (2y):       $3998.00", out)
        self.assertIn("Firstbase + CPA (2y): $1858.00", out)
        self.assertIn("Net Realized Savings:    $2140.00", out)
        self.check_readme("firstbase", "doola-pricing-vs-firstbase",
                          ["$3,998.00", "$1,858.00", "$2,140.00"])

    def test_non_us_llc_calculator(self):
        out = self.run_calc("firstbase", "non-us-founder-llc-annual-cost",
                            ["non_us_llc_calculator.py", "--state-report", "60", "--agent-fee", "99", "--tax-prep", "500", "--mail-forwarding", "120"])
        self.assertIn("Mandatory State & Tax Compliance: $659.00/year", out)
        self.assertIn("Mail/Address Service:             $120.00/year", out)
        self.assertIn("Total True Annual Carry:          $779.00/year", out)
        self.check_readme("firstbase", "non-us-founder-llc-annual-cost",
                          ["$659.00/year", "$120.00/year", "$779.00/year"])

    # ==========================================
    # RunPod Calculators
    # ==========================================

    def test_runpod_gpu_pricing_calculator(self):
        out = self.run_calc("runpod", "runpod-coupon-pricing-guide",
                            ["runpod_gpu_pricing_calculator.py", "--hours", "200", "--rate", "1.89", "--discount", "10"])
        self.assertIn("Base Monthly Compute:    $378.00", out)
        self.assertIn("Discount Rate:           10.0%", out)
        self.assertIn("Monthly Savings:         $37.80", out)
        self.assertIn("Effective Monthly:       $340.20", out)
        self.assertIn("Annual Total Compute:    $4082.40", out)
        self.assertIn("Annual Total Savings:    $453.60", out)
        self.check_readme("runpod", "runpod-coupon-pricing-guide",
                          ["$378.00/month", "$340.20/month", "$4,082.40/year", "$37.80/month", "$453.60/year"])

    def test_lambda_vs_runpod_calculator(self):
        out = self.run_calc("runpod", "lambda-labs-vs-runpod-h100-costs",
                            ["lambda_vs_runpod_calculator.py", "--hours", "500", "--lambda-rate", "3.29", "--runpod-rate", "2.89"])
        self.assertIn("Lambda Labs (@$3.29/hr): $1645.00", out)
        self.assertIn("RunPod (@$2.89/hr):      $1445.00", out)
        self.assertIn("Training Run Savings:    $200.00", out)
        self.check_readme("runpod", "lambda-labs-vs-runpod-h100-costs",
                          ["$1,645.00", "$1,445.00", "$200.00"])

    def test_vastai_vs_runpod_calculator(self):
        out = self.run_calc("runpod", "vastai-vs-runpod-serverless-pricing",
                            ["vastai_vs_runpod_calculator.py", "--invocations", "50000", "--duration", "2.5", "--rate", "0.00045", "--dedicated", "320.00"])
        self.assertIn("Serverless Monthly Cost: $56.25", out)
        self.assertIn("24/7 Dedicated Cost:     $320.00", out)
        self.assertIn("Net Monthly Savings:     $263.75", out)
        self.check_readme("runpod", "vastai-vs-runpod-serverless-pricing",
                          ["$320.00/month", "$56.25", "$263.75", "$3,165.00/year"])

    def test_llm_gpu_hourly_calculator(self):
        out = self.run_calc("runpod", "llm-inference-gpu-hourly-calculator",
                            ["llm_gpu_hourly_calculator.py", "--tokens-per-sec", "85.0", "--rate", "0.74", "--hours", "300"])
        self.assertIn("Monthly Output:          91.80M tokens", out)
        self.assertIn("Monthly Infrastructure:  $222.00", out)
        self.assertIn("Cost Per Million Tokens: $2.4183", out)
        self.check_readme("runpod", "llm-inference-gpu-hourly-calculator",
                          ["91.80M tokens", "$222.00", "$2.42 per million tokens"])

    # ==========================================
    # Webshare Calculators
    # ==========================================

    def test_webshare_proxy_pricing_calculator(self):
        out = self.run_calc("webshare", "webshare-coupon-code-pricing-guide",
                            ["webshare_proxy_pricing_calculator.py", "--gb", "50", "--rate", "4.50", "--annual-discount", "30"])
        self.assertIn("Monthly Base Cost:       $225.00", out)
        self.assertIn("Effective Monthly (1y):  $157.50", out)
        self.assertIn("Annual Total Prepaid:    $1890.00", out)
        self.assertIn("Annual Savings:          $810.00", out)
        self.check_readme("webshare", "webshare-coupon-code-pricing-guide",
                          ["$225.00/month", "$157.50/month", "$1,890.00/year", "$67.50/month", "$810.00/year"])

    def test_brightdata_vs_webshare_calculator(self):
        out = self.run_calc("webshare", "brightdata-vs-webshare-pricing",
                            ["brightdata_vs_webshare_calculator.py", "--volume-gb", "60", "--bright-rate", "8.40", "--webshare-rate", "3.50"])
        self.assertIn("Bright Data (@$8.40/GB): $504.00/mo", out)
        self.assertIn("Webshare (@$3.50/GB):    $210.00/mo", out)
        self.assertIn("Monthly Net Savings:     $294.00/mo", out)
        self.assertIn("Annual Projected Savings:$3528.00/year", out)
        self.check_readme("webshare", "brightdata-vs-webshare-pricing",
                          ["$504.00/month", "$210.00/month", "$294.00/month", "$3,528.00/year"])

    def test_smartproxy_vs_webshare_calculator(self):
        out = self.run_calc("webshare", "smartproxy-vs-webshare-cost-comparison",
                            ["smartproxy_vs_webshare_calculator.py", "--ips", "100", "--smartproxy-cost", "50.00", "--webshare-cost", "6.00"])
        self.assertIn("Smartproxy Monthly:      $50.00", out)
        self.assertIn("Webshare Monthly:        $6.00", out)
        self.assertIn("Monthly Cost Difference: $44.00", out)
        self.assertIn("Annual Projected Savings:$528.00", out)
        self.check_readme("webshare", "smartproxy-vs-webshare-cost-comparison",
                          ["$50.00/month", "$6.00/month", "$44.00/month", "$528.00/year"])

    def test_residential_bandwidth_calculator(self):
        out = self.run_calc("webshare", "rotating-residential-proxy-bandwidth-calculator",
                            ["residential_bandwidth_calculator.py", "--pages", "250000", "--kb-per-page", "120.0", "--rate", "3.50"])
        self.assertIn("Total Bandwidth:         28.61 GB", out)
        self.assertIn("Total Monthly Cost:      $100.14", out)
        self.assertIn("Cost Per 1,000 Pages:    $0.4005", out)
        self.check_readme("webshare", "rotating-residential-proxy-bandwidth-calculator",
                          ["28.61 GB", "$100.14", "$0.4005 per 1,000 pages", "$329.01/month", "$3,948.12/year"])

    # ==========================================
    # Vast.ai Calculators
    # ==========================================

    def test_vastai_credit_calculator(self):
        out = self.run_calc("vastai", "vastai-promo-code-credit-guide",
                            ["vastai_credit_calculator.py", "--credits", "50.0", "--spot-rate", "0.35", "--ondemand-rate", "0.75"])
        self.assertIn("Credit Applied:          $50.00", out)
        self.assertIn("Deliverable Spot Hours:  142.9 hours", out)
        self.assertIn("Equivalent Value:        $107.14", out)
        self.assertIn("Net Realized Savings:    $57.14", out)
        self.check_readme("vastai", "vastai-promo-code-credit-guide",
                          ["$50.00", "142.9 hours", "$107.14", "$57.14"])

    def test_runpod_vs_vastai_calculator(self):
        out = self.run_calc("vastai", "runpod-vs-vastai-gpu-rental-costs",
                            ["runpod_vs_vastai_calculator.py", "--hours", "300", "--runpod-rate", "0.74", "--vastai-rate", "0.35"])
        self.assertIn("RunPod Monthly (@$0.74/hr):  $222.00", out)
        self.assertIn("Vast.ai Monthly (@$0.35/hr): $105.00", out)
        self.assertIn("Monthly Cost Difference:     $117.00", out)
        self.assertIn("Annual Projected Savings:    $1404.00", out)
        self.check_readme("vastai", "runpod-vs-vastai-gpu-rental-costs",
                          ["$222.00/month", "$105.00/month", "$117.00/month", "$1,404.00/year"])

    def test_cloud_vs_vastai_calculator(self):
        out = self.run_calc("vastai", "aws-p5-vs-vastai-h100-pricing",
                            ["cloud_vs_vastai_calculator.py", "--hours", "100", "--aws-rate", "98.32", "--vastai-rate", "23.92"])
        self.assertIn("AWS p5.48xlarge Total:   $9832.00", out)
        self.assertIn("Vast.ai 8x H100 Total:   $2392.00", out)
        self.assertIn("Net Workload Savings:    $7440.00", out)
        self.assertIn("Cost Reduction:          75.7%", out)
        self.assertIn("Annual Net Savings:      $89280.00", out)
        self.check_readme("vastai", "aws-p5-vs-vastai-h100-pricing",
                          ["$9,832.00", "$2,392.00", "$7,440.00", "75.7%", "$89,280.00/year"])

    def test_spot_gpu_budget_estimator(self):
        out = self.run_calc("vastai", "spot-instance-gpu-training-budget",
                            ["spot_gpu_budget_estimator.py", "--budget", "500.0", "--hourly-rate", "0.35", "--overhead-pct", "5.0"])
        self.assertIn("Allocated Budget:        $500.00", out)
        self.assertIn("Gross Compute Hours:     1428.57 hrs", out)
        self.assertIn("Resumption Overhead:    71.43 hrs", out)
        self.assertIn("Net Usable Compute:      1357.14 hrs", out)
        self.assertIn("Effective Rate:          $0.3684/usable-hr", out)
        self.check_readme("vastai", "spot-instance-gpu-training-budget",
                          ["$500.00", "1,428.57 gross hours", "1,357.14 net usable compute hours", "$0.3684/usable-hr"])

    # ==========================================
    # AdsPower Calculators
    # ==========================================

    def test_adspower_discount_calculator(self):
        out = self.run_calc("adspower", "adspower-coupon-code-pricing-breakdown",
                            ["adspower_discount_calculator.py", "--monthly-rate", "50.0", "--months", "12", "--discount-pct", "40.0"])
        self.assertIn("Monthly Base Cost:       $50.00", out)
        self.assertIn("Annual Prepaid Total:    $360.00", out)
        self.assertIn("Effective Monthly:       $30.00/mo", out)
        self.assertIn("Annual Realized Savings: $240.00/year", out)
        self.check_readme("adspower", "adspower-coupon-code-pricing-breakdown",
                          ["$50.00/month", "$360.00", "$30.00/month", "$240.00/year"])

    def test_multilogin_vs_adspower_calculator(self):
        out = self.run_calc("adspower", "multilogin-vs-adspower-pricing",
                            ["multilogin_vs_adspower_calculator.py", "--multilogin-rate", "108.0", "--adspower-rate", "50.0"])
        self.assertIn("Multilogin Monthly Cost: $108.00/mo", out)
        self.assertIn("AdsPower Monthly Cost:   $50.00/mo", out)
        self.assertIn("Monthly Net Savings:     $58.00/mo", out)
        self.assertIn("Annual Projected Savings:$696.00/year", out)
        self.check_readme("adspower", "multilogin-vs-adspower-pricing",
                          ["$108.00/mo", "$50.00/mo", "$58.00/mo", "$696.00/year"])

    def test_gologin_vs_adspower_calculator(self):
        out = self.run_calc("adspower", "gologin-vs-adspower-cost-comparison",
                            ["gologin_vs_adspower_calculator.py", "--gologin-cost", "49.0", "--adspower-base", "50.0", "--discount-pct", "20.0"])
        self.assertIn("GoLogin Monthly Cost:    $49.00/mo", out)
        self.assertIn("AdsPower Discounted Cost:$40.00/mo", out)
        self.assertIn("Monthly Cost Difference: $9.00/mo", out)
        self.assertIn("Annual Net Advantage:    $108.00/year", out)
        self.check_readme("adspower", "gologin-vs-adspower-cost-comparison",
                          ["$49.00/mo", "$40.00/mo", "$9.00/mo", "$108.00/year"])

    def test_profile_tco_estimator(self):
        out = self.run_calc("adspower", "antidetect-browser-profile-tco-estimator",
                            ["profile_tco_estimator.py", "--profiles", "100", "--proxy-cost-per-profile", "3.0", "--software-monthly", "30.0"])
        self.assertIn("Managed Environments:    100 profiles", out)
        self.assertIn("Proxy Subtotal:          $300.00/mo", out)
        self.assertIn("Software License:        $30.00/mo", out)
        self.assertIn("Total Monthly Infra:     $330.00/mo", out)
        self.assertIn("Blended Unit Cost:       $3.30/profile/mo", out)
        self.assertIn("Annual Fleet Expense:    $3960.00/year", out)
        self.check_readme("adspower", "antidetect-browser-profile-tco-estimator",
                          ["100 profiles", "$300.00/mo", "$30.00/mo", "$330.00/mo", "$3.30/profile/mo", "$3960.00/year"])

    # ==========================================
    # 9Proxy Calculators
    # ==========================================

    def test_nineproxy_credit_calculator(self):
        out = self.run_calc("9proxy", "9proxy-coupon-code-pricing-guide",
                            ["nineproxy_credit_calculator.py", "--ips", "500", "--tier-rate", "0.30", "--promo-discount", "10.0"])
        self.assertIn("IP Package Quantity:     500 IPs", out)
        self.assertIn("Standard Catalog Rate:   $0.30/IP", out)
        self.assertIn("Gross Purchase Cost:     $150.00", out)
        self.assertIn("Promotional Savings:     $15.00", out)
        self.assertIn("Net Purchase Total:      $135.00", out)
        self.assertIn("Effective Rate Per IP:   $0.2700/IP", out)
        self.check_readme("9proxy", "9proxy-coupon-code-pricing-guide",
                          ["500 IPs", "$0.30/IP", "$150.00", "$15.00", "$135.00", "$0.2700/IP"])

    def test_iproyal_vs_nineproxy_calculator(self):
        out = self.run_calc("9proxy", "iproyal-vs-9proxy-pricing",
                            ["iproyal_vs_nineproxy_calculator.py", "--sessions", "50", "--gb-per-session", "2.0", "--iproyal-gb-rate", "7.0", "--nineproxy-ip-rate", "0.30"])
        self.assertIn("Scraping Workload:       50 sessions (100.0 GB total)", out)
        self.assertIn("IPRoyal Bandwidth Cost:  $700.00", out)
        self.assertIn("9Proxy Pay-per-IP Cost:  $15.00", out)
        self.assertIn("Net Scraping Savings:    $685.00", out)
        self.check_readme("9proxy", "iproyal-vs-9proxy-pricing",
                          ["50 sessions", "100.0 GB total", "$700.00", "$15.00", "$685.00"])

    def test_pias5_vs_nineproxy_calculator(self):
        out = self.run_calc("9proxy", "pias5-vs-9proxy-cost-comparison",
                            ["pias5_vs_nineproxy_calculator.py", "--ips", "500", "--pia-unit-rate", "0.36", "--nineproxy-unit-rate", "0.30"])
        self.assertIn("Batch Proxy Volume:      500 IPs", out)
        self.assertIn("PIA S5 Total Expense:    $180.00", out)
        self.assertIn("9Proxy Total Expense:    $150.00", out)
        self.assertIn("Net Realized Savings:    $30.00", out)
        self.check_readme("9proxy", "pias5-vs-9proxy-cost-comparison",
                          ["500 IPs", "$180.00", "$150.00", "$30.00"])

    def test_ip_pool_budget_calculator(self):
        out = self.run_calc("9proxy", "residential-ip-pool-budget-calculator",
                            ["ip_pool_budget_calculator.py", "--daily-rotations", "20", "--days", "30", "--unit-cost", "0.27"])
        self.assertIn("Daily Rotation Demand:   20 IPs/day", out)
        self.assertIn("Total Monthly Quantity:  600 IPs", out)
        self.assertIn("Discounted Unit Cost:    $0.27/IP", out)
        self.assertIn("Total Monthly Spend:     $162.00", out)
        self.assertIn("Daily Operating Burn:    $5.40/day", out)
        self.check_readme("9proxy", "residential-ip-pool-budget-calculator",
                          ["20 IPs/day", "600 IPs", "$0.27/IP", "$162.00", "$5.40/day"])

    # ==========================================
    # AdCreative.ai Calculators
    # ==========================================

    def test_adcreative_roi_calculator(self):
        out = self.run_calc("adcreative", "adcreative-ai-coupon-pricing-breakdown",
                            ["adcreative_roi_calculator.py", "--monthly-rate", "149.0", "--annual-discount", "25.0"])
        self.assertIn("Monthly Catalog Rate:    $149.00/mo", out)
        self.assertIn("Annual Discount Rate:    25.0%", out)
        self.assertIn("Effective Monthly Cost:  $111.75/mo", out)
        self.assertIn("Annual Billed Total:     $1341.00", out)
        self.assertIn("Annual Realized Savings: $447.00/year", out)
        self.check_readme("adcreative", "adcreative-ai-coupon-pricing-breakdown",
                          ["$149.00/mo", "25.0%", "$111.75/mo", "$1341.00", "$447.00/year"])

    def test_canva_vs_adcreative_calculator(self):
        out = self.run_calc("adcreative", "canva-pro-vs-adcreative-ai-pricing",
                            ["canva_vs_adcreative_calculator.py", "--canva-sub", "15.0", "--designer-retainer", "500.0", "--adcreative-sub", "149.0", "--review-overhead", "60.0"])
        self.assertIn("Manual Design Stack:     $515.00/mo", out)
        self.assertIn("AdCreative.ai Pipeline:  $209.00/mo", out)
        self.assertIn("Monthly Production Save: $306.00/mo", out)
        self.assertIn("Annual Projected Savings:$3672.00/year", out)
        self.check_readme("adcreative", "canva-pro-vs-adcreative-ai-pricing",
                          ["$515.00/mo", "$209.00/mo", "$306.00/mo", "$3672.00/year"])

    def test_jasper_vs_adcreative_calculator(self):
        out = self.run_calc("adcreative", "jasper-vs-adcreative-cost-comparison",
                            ["jasper_vs_adcreative_calculator.py", "--jasper-sub", "49.0", "--graphic-sub", "400.0", "--adcreative-sub", "149.0"])
        self.assertIn("Split Copy & Graphic Stack: $449.00/mo", out)
        self.assertIn("AdCreative.ai Unified Rate: $149.00/mo", out)
        self.assertIn("Monthly Net Difference:     $300.00/mo", out)
        self.assertIn("Annual Total Advantage:     $3600.00/year", out)
        self.check_readme("adcreative", "jasper-vs-adcreative-cost-comparison",
                          ["$449.00/mo", "$149.00/mo", "$300.00/mo", "$3600.00/year"])

    def test_creative_production_calculator(self):
        out = self.run_calc("adcreative", "ecommerce-ad-creative-production-cost",
                            ["creative_production_calculator.py", "--creatives-per-month", "50", "--agency-unit-rate", "45.0", "--adcreative-sub", "149.0"])
        self.assertIn("Monthly Asset Volume:    50 ad variants", out)
        self.assertIn("Agency Outsourced Total: $2250.00/mo", out)
        self.assertIn("AI-Assisted Total Cost:  $149.00/mo", out)
        self.assertIn("Monthly Net Savings:     $2101.00/mo", out)
        self.assertIn("Production Cost Per Unit:$2.98/asset", out)
        self.check_readme("adcreative", "ecommerce-ad-creative-production-cost",
                          ["50 ad variants", "$2250.00/mo", "$149.00/mo", "$2101.00/mo", "$2.98/asset"])

if __name__ == '__main__':
    unittest.main()
