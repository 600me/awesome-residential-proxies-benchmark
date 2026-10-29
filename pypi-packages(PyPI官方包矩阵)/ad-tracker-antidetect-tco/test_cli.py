"""Unit tests for ad-tracker-antidetect-tco CLI."""

import json
import subprocess
import sys
import unittest

from ad_tracker_antidetect_tco import cli


def run_cli(args):
    return subprocess.run(
        [sys.executable, "-m", "ad_tracker_antidetect_tco.cli"] + args,
        capture_output=True, text=True)


class TestDefaultOutput(unittest.TestCase):
    def test_default_table(self):
        r = run_cli([])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Total Infrastructure Monthly TCO    | $218.00 / month", r.stdout)
        self.assertIn("Cost Per Active Browser Profile     | $4.36 / profile / month", r.stdout)
        self.assertIn("MoreLogin Solo Plan", r.stdout)
        self.assertIn("Voluum Starter ($199 base / 1M events)", r.stdout)
        self.assertIn("$10.00 (clean non-expiring IPs)", r.stdout)

    def test_default_version_line(self):
        r = run_cli([])
        self.assertIn("ad-tracker-antidetect-tco 1.0.0 - Media Buyer Infrastructure TCO", r.stdout)


class TestAgencyCombo(unittest.TestCase):
    def test_100_profiles_5m_events_5_seats(self):
        r = run_cli(["--profiles", "100", "--events", "5000000", "--seats", "5"])
        self.assertEqual(r.returncode, 0)
        checks = [
            "AdsPower Base ($19) + 4 extra seats ($20",
            "Anti-Detect Browser Subtotal        | $39.00 / month",
            "Tracker Overage (2M @ $0.06/1k)     | $120.00 overage surcharge",
            "Ad Tracker Subtotal                 | $469.00 / month",
            "Total Infrastructure Monthly TCO    | $528.00 / month",
            "Cost Per Active Browser Profile     | $5.28 / profile / month",
            "Risk Mitigation (5 Accounts Saved)  | ~$7,500.00 asset protection value",
        ]
        for c in checks:
            self.assertIn(c, r.stdout)

    def test_gateways_present(self):
        r = run_cli(["--profiles", "100", "--events", "5000000", "--seats", "5"])
        self.assertIn("AdsPower Gateway: https://go.272738.xyz/adspower?src=pypi_adstack_calc", r.stdout)
        self.assertIn("Voluum Gateway: https://go.272738.xyz/voluum?src=pypi_adstack_calc", r.stdout)


class TestCompareStack(unittest.TestCase):
    def test_compare_stack_contains_all_five(self):
        r = run_cli(["--compare-stack"])
        self.assertEqual(r.returncode, 0)
        for brand in ["AdsPower", "MoreLogin", "Voluum", "9Proxy", "Webshare"]:
            self.assertIn(brand, r.stdout)
        self.assertIn("webshare?src=pypi_adstack_calc", r.stdout)


class TestJson(unittest.TestCase):
    def test_json_format_and_numbers(self):
        r = run_cli(["--json", "--profiles", "100", "--events", "5000000", "--seats", "5"])
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["tool"], "ad-tracker-antidetect-tco")
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["profiles"], 100)
        self.assertEqual(data["events"], 5000000)
        self.assertEqual(data["seats"], 5)
        b = data["breakdown"]
        self.assertEqual(b["antidetect_browser_usd"], 39.0)
        self.assertEqual(b["ad_tracker_base_usd"], 349.0)
        self.assertEqual(b["ad_tracker_overage_usd"], 120.0)
        self.assertEqual(b["proxy_ips_usd"], 20.0)
        self.assertEqual(b["total_monthly_tco_usd"], 528.0)
        self.assertEqual(b["cost_per_profile_usd"], 5.28)
        self.assertEqual(data["gateways"]["webshare"],
                         "https://go.272738.xyz/webshare?src=pypi_adstack_calc")

    def test_json_default_params(self):
        r = run_cli(["--json"])
        data = json.loads(r.stdout)
        self.assertEqual(data["breakdown"]["total_monthly_tco_usd"], 218.0)
        self.assertEqual(data["breakdown"]["cost_per_profile_usd"], 4.36)


class TestVersionAndErrors(unittest.TestCase):
    def test_version_flag(self):
        r = run_cli(["--version"])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "ad-tracker-antidetect-tco 1.0.0")

    def test_negative_profiles_exit_code(self):
        r = run_cli(["--profiles", "-1"])
        self.assertNotEqual(r.returncode, 0)

    def test_zero_seats_exit_code(self):
        r = run_cli(["--seats", "0"])
        self.assertNotEqual(r.returncode, 0)

    def test_non_integer_profiles_exit_code(self):
        r = run_cli(["--profiles", "abc"])
        self.assertNotEqual(r.returncode, 0)


class TestModelUnit(unittest.TestCase):
    def test_calc_tco_direct(self):
        r = cli.calc_tco(100, 5000000, 5)
        self.assertEqual(r["total"], 528.0)
        r2 = cli.calc_tco(50, 1000000, 1)
        self.assertEqual(r2["total"], 218.0)


if __name__ == "__main__":
    unittest.main()
