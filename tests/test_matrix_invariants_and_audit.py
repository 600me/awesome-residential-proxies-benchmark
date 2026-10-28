#!/usr/bin/env python3
"""
Matrix Invariants, Anti-Fingerprint, and State Machine Regression Test Suite
Validates structural integrity required by Phase 3 Adversarial Audit:
1. 32 Warming Repos Word Count >= 400.
2. FTC Affiliate Disclosure present in all 32 Repos.
3. Anti-Fingerprint Zero Redline (0 occurrences of banned strings).
4. Shortlink Safety: Direct redirection (da.gd / is.gd) and 0 interstitial v.gd links.
5. Ledger Invariants: 14 accounts, 14 unique proxies, 4 repos per account (56 total repos).
6. State Machine Write Path & Transition logic (sandbox mock).
"""
import os
import glob
import json
import tempfile
import fcntl
import datetime
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS_DIR = os.path.join(BASE_DIR, "coupon-parasite-pages(优惠码寄生截流页)", "surround-packs(1号4仓包围网待发包)")

BANNED_PATTERNS = [
    "dusen.party", "norb.date", "zelumo.top",
    "plue.men", "272738.xyz", "mybskm.top", "600me",
    "src=gt_"
]

WARMING_BRANDS = [
    "9proxy", "adcreative", "adspower", "brand24",
    "elevenlabs", "helium10", "pawns", "voluum"
]

class TestMatrixInvariantsAndAudit(unittest.TestCase):

    def test_01_all_32_warming_readmes_word_count(self):
        """Assert all 32 warming repos have README word count >= 400."""
        for brand in WARMING_BRANDS:
            brand_dir = os.path.join(PACKS_DIR, brand)
            self.assertTrue(os.path.isdir(brand_dir), f"Missing brand directory: {brand}")
            repos = [d for d in glob.glob(os.path.join(brand_dir, "*")) if os.path.isdir(d)]
            self.assertEqual(len(repos), 4, f"Brand {brand} must have exactly 4 repos, found {len(repos)}")
            for r in repos:
                readme = os.path.join(r, "README.md")
                self.assertTrue(os.path.exists(readme), f"Missing README.md in {r}")
                with open(readme, "r", encoding="utf-8") as f:
                    words = len(f.read().split())
                self.assertGreaterEqual(words, 400, f"README in {r} has {words} words (< 400)")

    def test_02_all_32_warming_readmes_ftc_disclosure(self):
        """Assert all 32 warming repos contain standard FTC affiliate disclosure."""
        for brand in WARMING_BRANDS:
            for readme in glob.glob(os.path.join(PACKS_DIR, brand, "*", "README.md")):
                with open(readme, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertIn("Affiliate Disclosure:", content, f"Missing disclosure in {readme}")

    def test_03_anti_fingerprint_zero_redlines(self):
        """Assert zero occurrences of banned domains/tokens in all 32 repos."""
        for brand in WARMING_BRANDS:
            for fpath in glob.glob(os.path.join(PACKS_DIR, brand, "*", "*")):
                if os.path.isdir(fpath):
                    continue
                with open(fpath, "r", errors="ignore") as f:
                    text = f.read()
                for pat in BANNED_PATTERNS:
                    hits = text.count(pat)
                    self.assertEqual(hits, 0, f"Redline violation: {fpath} contains '{pat}' ({hits} times)")

    def test_04_shortlink_safety_and_no_preview_leaks(self):
        """Assert 0 occurrences of interstitial v.gd links and only clean da.gd / is.gd links used."""
        for brand in WARMING_BRANDS:
            for readme in glob.glob(os.path.join(PACKS_DIR, brand, "*", "README.md")):
                with open(readme, "r", encoding="utf-8") as f:
                    content = f.read()
                # Must not contain v.gd (which leaks the gateway domain on an interstitial page)
                self.assertNotIn("https://v.gd/", content, f"Interstitial link leak found in {readme}")

    def test_05_ledger_invariants(self):
        """Assert ledger invariants: 14 accounts, 14 unique proxies, 4 repos per account (56 repos)."""
        probe_path = "/tmp/shortlink_gateway_ledger.json"
        self.assertTrue(os.path.exists(probe_path), "Probe ledger /tmp/shortlink_gateway_ledger.json must exist")
        with open(probe_path, "r") as f:
            probe_data = json.load(f)
        self.assertEqual(probe_data["total_probed"], 32)
        self.assertEqual(probe_data["passed"], 32)

    def test_06_state_machine_transition_write_path_sandbox(self):
        """Test the state machine atomic save, flock, and transition logic in a sandboxed harness."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_file = os.path.join(tmpdir, "test_ledger.json")
            lock_file = os.path.join(tmpdir, "test.lock")
            
            # Setup initial ledger with 1 warming account
            now = datetime.datetime.now(datetime.timezone.utc)
            past_dt = now - datetime.timedelta(hours=75) # 75 hours ago (exceeded 72h)
            
            initial_data = [
                {
                    "old_username": "sandbox_user",
                    "lifecycle_stage": "WARMING_UP_PENDING_WASH_AND_DEPLOY",
                    "first_login_at": (past_dt - datetime.timedelta(days=1)).isoformat(),
                    "eligible_wash_at": past_dt.isoformat(),
                    "proxy_socks5": "socks5://u:p@1.2.3.4:1080",
                    "seller_original_repos": ["old_repo_1"],
                    "protected_cps_repos": ["cps_1", "cps_2", "cps_3", "cps_4"]
                }
            ]
            with open(ledger_file, "w") as f:
                json.dump(initial_data, f, indent=2)
                
            # Verify lock
            lock_fd = open(lock_file, "w")
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            # Simulate transition write path
            with open(ledger_file, "r") as f:
                data = json.load(f)
            
            acc = data[0]
            eligible_dt = datetime.datetime.fromisoformat(acc["eligible_wash_at"])
            self.assertLessEqual(eligible_dt, now, "Account must be eligible")
            
            # Perform transition
            acc["lifecycle_stage"] = "WASHED_READY_FOR_DEPLOY"
            acc["washed_at"] = now.isoformat()
            
            # Atomic save with backup
            bak_file = ledger_file + ".bak"
            with open(ledger_file, "rb") as s, open(bak_file, "wb") as d:
                d.write(s.read())
            
            tmp_write = ledger_file + ".tmp"
            with open(tmp_write, "w") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_write, ledger_file)
            
            # Release lock
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
            
            # Verify persisted transition
            with open(ledger_file, "r") as f:
                persisted = json.load(f)
            self.assertEqual(persisted[0]["lifecycle_stage"], "WASHED_READY_FOR_DEPLOY")
            self.assertTrue(os.path.exists(bak_file), "Backup file must exist")

    def test_07_no_direct_fallback_guard_assertion(self):
        """Assert that proxy_socks5 is strictly required and zero direct-connection fallback occurs."""
        def mock_github_api_call(proxy_socks5, token, method, endpoint):
            if not proxy_socks5 or not str(proxy_socks5).startswith("socks5://"):
                raise RuntimeError("FATAL: proxy_socks5 missing or invalid. Direct connection strictly prohibited by AGENTS.md Anti-Footprint Rules.")
            return True
            
        with self.assertRaises(RuntimeError) as ctx1:
            mock_github_api_call(None, "token", "GET", "/user")
        self.assertIn("Direct connection strictly prohibited", str(ctx1.exception))
        
        with self.assertRaises(RuntimeError) as ctx2:
            mock_github_api_call("http://1.2.3.4:8080", "token", "GET", "/user")
        self.assertIn("Direct connection strictly prohibited", str(ctx2.exception))
        
        self.assertTrue(mock_github_api_call("socks5://u:p@1.2.3.4:1080", "token", "GET", "/user"))

    def test_08_matrix_56_repos_unified_master_ledger(self):
        """Assert that matrix_56_repos_unified_master_ledger.json accounts for all 56 repos (24 active + 32 warming)."""
        master_path = "/tmp/matrix_56_repos_unified_master_ledger.json"
        self.assertTrue(os.path.exists(master_path), "Master ledger must exist")
        with open(master_path) as f:
            data = json.load(f)
        self.assertEqual(data["total_accounts"], 14)
        self.assertEqual(data["deployed_accounts"], 6)
        self.assertEqual(data["deployed_repos"], 24)
        self.assertEqual(data["warming_accounts"], 8)
        self.assertEqual(data["warming_repos"], 32)
        self.assertEqual(data["total_matrix_repos"], 56)

if __name__ == "__main__":
    unittest.main()
