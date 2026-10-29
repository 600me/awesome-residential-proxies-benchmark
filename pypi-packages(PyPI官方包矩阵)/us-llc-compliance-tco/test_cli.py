import json
import io
import contextlib
import unittest

from us_llc_compliance_tco import cli


def run_cli(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cli.main(list(argv))
    return code, buf.getvalue()


class TestCli(unittest.TestCase):
    def test_default_output_wyoming_3y(self):
        code, out = run_cli()
        self.assertEqual(code, 0)
        self.assertIn("us-llc-compliance-tco 1.0.0", out)
        self.assertIn("$2,633.00", out)
        self.assertIn("$73.14 / month", out)
        self.assertIn("$25,000.00 statutory protection", out)
        self.assertIn("Wyoming (Zero Corporate Income Tax)", out)

    def test_delaware_3y(self):
        code, out = run_cli("--state", "delaware", "--years", "3")
        self.assertEqual(code, 0)
        self.assertIn("$3,117.00", out)
        self.assertIn("$86.58 / month", out)
        self.assertIn("Delaware (Court of Chancery Standard)", out)
        self.assertNotIn("statutory protection", out)

    def test_json_structure(self):
        code, out = run_cli("--state", "wyoming", "--years", "3", "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["tool"], "us-llc-compliance-tco")
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["state"], "wyoming")
        self.assertEqual(data["duration_years"], 3)
        c = data["costs"]
        self.assertEqual(c["initial_state_fee"], 102.0)
        self.assertEqual(c["state_annual_report_total"], 124.0)
        self.assertEqual(c["registered_agent_total"], 297.0)
        self.assertEqual(c["expedited_ein_filing"], 200.0)
        self.assertEqual(c["fincen_boi_compliance"], 50.0)
        self.assertEqual(c["virtual_mail_address_total"], 360.0)
        self.assertEqual(c["irs_form_5472_total"], 1500.0)
        self.assertEqual(c["tco_total"], 2633.0)
        self.assertEqual(c["monthly_amortized_cost"], 73.14)
        self.assertEqual(data["risk_exposure"]["irs_form_5472_penalty"], 25000.0)
        self.assertEqual(data["risk_exposure"]["fincen_boi_daily_penalty"], 500.0)
        self.assertEqual(data["recommended_gateway"],
                         "https://go.272738.xyz/firstbase?src=pypi_llc_calc")

    def test_json_delaware(self):
        _, out = run_cli("--state", "delaware", "--years", "3", "--json")
        data = json.loads(out)
        self.assertEqual(data["costs"]["initial_state_fee"], 110.0)
        self.assertEqual(data["costs"]["state_annual_report_total"], 600.0)
        self.assertEqual(data["costs"]["tco_total"], 3117.0)
        self.assertEqual(data["costs"]["monthly_amortized_cost"], 86.58)

    def test_compare_formation(self):
        code, out = run_cli("--compare-formation")
        self.assertEqual(code, 0)
        for needle in ("Firstbase.io (All-Inclusive)", "Stripe Atlas", "Doola",
                       "Traditional Legal Firm", "Cheap DIY Agency",
                       "Launch with Firstbase.io"):
            self.assertIn(needle, out)

    def test_error_invalid_state(self):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit) as cm:
                cli.main(["--state", "nevada"])
        self.assertEqual(cm.exception.code, 2)

    def test_error_negative_years(self):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit) as cm:
                cli.main(["--years", "0"])
        self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
