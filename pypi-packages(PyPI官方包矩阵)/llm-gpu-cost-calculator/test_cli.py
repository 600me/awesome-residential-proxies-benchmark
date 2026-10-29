#!/usr/bin/env python3
"""Unit tests for llm-gpu-cost-calculator CLI."""

import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(ROOT, "llm_gpu_cost_calculator")


def run(args):
    env = dict(os.environ)
    env["PYTHONPATH"] = ROOT
    return subprocess.run(
        [sys.executable, "-m", "llm_gpu_cost_calculator.cli"] + args,
        capture_output=True, text=True, env=env)


class TestBasics(unittest.TestCase):
    def test_version(self):
        r = run(["--version"])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "llm-gpu-cost-calculator 1.0.0")

    def test_help(self):
        r = run(["-h"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("--gpu", r.stdout)

    def test_invalid_gpu_exits_nonzero(self):
        r = run(["--gpu", "v100"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("invalid choice", r.stderr)

    def test_invalid_float_hours_exits_nonzero(self):
        r = run(["--hours", "abc"])
        self.assertNotEqual(r.returncode, 0)


class TestComputeOutput(unittest.TestCase):
    def test_h100_300_matches_readme(self):
        r = run(["--gpu", "h100", "--hours", "300"])
        self.assertEqual(r.returncode, 0)
        for needle in [
            "$747.00", "$22.41", "$769.41", "$498.15", "$386.10",
            "$271.26", "35.25% net reduction", "$112.05",
            "NVIDIA H100 80GB SXM5", "RunPod (On-Demand), Vast.ai (Spot)",
            "https://go.272738.xyz/runpod?src=pypi_gpu_calc",
            "https://go.272738.xyz/vastai?src=pypi_gpu_calc",
        ]:
            self.assertIn(needle, r.stdout)

    def test_default_is_h100_100_hours(self):
        r = run([])
        self.assertEqual(r.returncode, 0)
        self.assertIn("300.0 hours" if False else "100.0 hours", r.stdout)
        self.assertIn("$249.00", r.stdout)  # 100 * 2.49


class TestJsonOutput(unittest.TestCase):
    def test_json_structure_and_values(self):
        r = run(["--gpu", "a100", "--hours", "120", "--json"])
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["tool"], "llm-gpu-cost-calculator")
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["mode"], "compute")
        self.assertEqual(data["gpu"], "a100")
        self.assertEqual(data["hours"], 120.0)
        self.assertEqual(data["nominal_rate_per_hour"], 1.64)
        self.assertEqual(data["nominal_cost"], 196.8)
        self.assertEqual(data["cold_start_cost"], 5.9)
        self.assertEqual(data["spot_rate_per_hour"], 0.95)
        self.assertEqual(data["spot_base_cost"], 114.0)
        self.assertEqual(data["spot_penalty"], 28.5)
        self.assertEqual(data["effective_ondemand_tco"], 202.7)
        self.assertEqual(data["effective_spot_tco"], 142.5)
        self.assertEqual(data["net_savings_usd"], 60.2)
        self.assertEqual(data["savings_percentage"], 29.7)
        self.assertIn("gateways", data)

    def test_json_media_mode(self):
        r = run(["--voice-chars", "500000", "--video-mins", "60", "--json"])
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "media")
        self.assertEqual(data["voice_cost_usd"], 99.0)
        self.assertEqual(data["video_cost_usd"], 164.0)
        self.assertEqual(data["total_media_tco_usd"], 263.0)


class TestMediaOutput(unittest.TestCase):
    def test_readme_media_example(self):
        r = run(["--voice-chars", "500000", "--video-mins", "60"])
        self.assertEqual(r.returncode, 0)
        for needle in [
            "500,000 characters (~55 hours of speech)",
            "Pro Tier (500k quota)", "$99.00",
            "60 minutes generated video",
            "Team Tier (30m base + 30m overage)",
            "$164.00 ($89.00 base + $75.00 overage)".replace("$164.00 ($89.00", "$164.00 ($89.00"),
            "$263.00 / month", "$4.38",
            "https://go.272738.xyz/elevenlabs?src=pypi_gpu_calc",
            "https://go.272738.xyz/heygen?src=pypi_gpu_calc",
        ]:
            self.assertIn(needle, r.stdout)

    def test_voice_only(self):
        r = run(["--voice-chars", "50000"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Starter Tier (30k quota)", r.stdout)
        self.assertIn("$9.00", r.stdout)  # Starter 30k quota: 5 + 20k/1000*0.20

    def test_zero_media_fallback(self):
        r = run(["--voice-chars", "0"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("Total Media Pipeline TCO", r.stdout)


class TestCompareCloud(unittest.TestCase):
    def test_compare_table_contains_all_brands(self):
        r = run(["--compare-cloud"])
        self.assertEqual(r.returncode, 0)
        for brand in ["RunPod", "Vast.ai", "ElevenLabs", "HeyGen", "Tier 1", "Tier 5"]:
            self.assertIn(brand, r.stdout)
        for url in ["https://go.272738.xyz/runpod?src=pypi_gpu_calc",
                    "https://go.272738.xyz/vastai?src=pypi_gpu_calc",
                    "https://go.272738.xyz/elevenlabs?src=pypi_gpu_calc",
                    "https://go.272738.xyz/heygen?src=pypi_gpu_calc"]:
            self.assertIn(url, r.stdout)


if __name__ == "__main__":
    unittest.main()
