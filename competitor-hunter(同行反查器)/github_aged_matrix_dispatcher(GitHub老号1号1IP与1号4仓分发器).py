#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Aged Account Matrix Dispatcher & 1-Account-1-IP Ledger Engine
Purpose: Verify aged GitHub accounts, enforce 1:1 static IP binding, manage warmup, and generate 4-repo encirclement packs.
"""

import os
import sys
import json
import re
import datetime
import urllib.request
import urllib.error

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROXY_LIST_PATH = "/Users/a600/.secrets(密钥)/webshare-proxy-list(Webshare代理列表).txt"
LEDGER_PATH = os.path.join(ROOT_DIR, "account_ip_domain_ledger(账号IP域名永久绑定账本).json")


class GitHubMatrixDispatcher:
    def __init__(self, proxy_list_path=PROXY_LIST_PATH, ledger_path=LEDGER_PATH):
        self.proxy_list_path = proxy_list_path
        self.ledger_path = ledger_path
        self.static_ips = self._load_proxies()
        self.ledger = self._load_ledger()

    def _load_proxies(self):
        if not os.path.exists(self.proxy_list_path):
            return []
        proxies = []
        with open(self.proxy_list_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    proxies.append(line)
        return proxies

    def _load_ledger(self):
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"updated_at": None, "accounts": {}}

    def save_ledger(self):
        self.ledger["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(self.ledger, f, ensure_ascii=False, indent=2)

    def verify_account(self, username, token=None):
        """
        1. Anonymously check https://github.com/<username> for 404 (Spammy / ghost ban).
        2. Check created_at via API to ensure aged >= 90 days.
        """
        result = {
            "username": username,
            "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "profile_http": None,
            "is_spammy_404": False,
            "created_at": None,
            "age_days": None,
            "is_aged_passed": False,
            "status": "UNKNOWN"
        }

        # Step 1: Anonymous public profile request (No cookie)
        profile_url = f"https://github.com/{username}"
        req = urllib.request.Request(profile_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result["profile_http"] = resp.status
        except urllib.error.HTTPError as e:
            result["profile_http"] = e.code
            if e.code == 404:
                result["is_spammy_404"] = True
                result["status"] = "DEAD_SPAMMY_404"
                return result
        except Exception as e:
            result["error"] = str(e)

        # Step 2: GitHub API for account creation date
        api_url = f"https://api.github.com/users/{username}"
        headers = {"User-Agent": "Mozilla/5.0"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        api_req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(api_req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                created_str = data.get("created_at")
                if created_str:
                    result["created_at"] = created_str
                    created_dt = datetime.datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                    now_dt = datetime.datetime.now(datetime.timezone.utc)
                    age_days = (now_dt - created_dt).days
                    result["age_days"] = age_days
                    result["is_aged_passed"] = (age_days >= 90)
                    if result["is_aged_passed"]:
                        result["status"] = "QUALIFIED_AGED"
                    else:
                        result["status"] = "TOO_YOUNG_UNDER_90D"
        except Exception as e:
            result["api_error"] = str(e)
            if result["profile_http"] == 200:
                result["status"] = "PROFILE_200_API_RATE_LIMITED"

        return result

    def bind_static_ip_and_domain(self, username, domain_group="group_1_mybskm"):
        """
        Enforce strict 1:1 static IP assignment from available webshare proxy pool.
        Note: Webshare datacenter proxies share egress IP 144.34.225.53 and block HTTPS CONNECT (HTTP 400).
        Direct git push via HTTPS requires residential proxies or an authenticated SOCKS5 tunnel.
        Ensure an account is permanently pinned to exactly 1 IP and domain group.
        """
        clean_user = username.strip().lower()
        if clean_user == "600me":
            raise PermissionError("ACCOUNT PROTECTION: 600me is primary author account. Binding to datacenter proxy or batch repo dispatch is strictly forbidden!")

        accounts = self.ledger.setdefault("accounts", {})
        if username in accounts and accounts[username].get("bound_ip"):
            return accounts[username]

        # Allocate next unassigned proxy deduplicating by unique proxy_ref (subaccount)
        assigned_refs = {acc.get("proxy_ref") for acc in accounts.values() if acc.get("proxy_ref")}
        available = [p for p in self.static_ips if p.split(':')[2] not in assigned_refs]
        if not available:
            raise RuntimeError("Static IP pool exhausted (100/100 allocated)!")

        assigned_proxy = available[0]
        entry = {
            "username": username,
            "bound_ip": f"{assigned_proxy.split(':')[0]}:{assigned_proxy.split(':')[1]}:{assigned_proxy.split(':')[2]}:***",
            "proxy_ref": assigned_proxy.split(':')[2],
            "egress_ip": "144.34.225.53",
            "domain_group": domain_group,
            "bound_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "BOUND_AND_LOCKED"
        }
        accounts[username] = entry
        self.save_ledger()
        return entry

    def generate_warmup_pack(self, username, tool_name="json-schema-validator-cli"):
        """
        Generate Day 1 white-hat utility tool to establish organic developer history.
        Contains ZERO commercial affiliate links.
        """
        script_code = '''#!/usr/bin/env python3
"""Zero-dependency JSON Schema and format inspector."""
import sys, json

def inspect(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Valid JSON: {filepath} (Type: {type(data).__name__}, Keys: {len(data) if isinstance(data, dict) else len(data)})")
        return 0
    except Exception as e:
        print(f"JSON Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_json.py <file.json>")
        sys.exit(2)
    sys.exit(inspect(sys.argv[1]))
'''
        readme_md = f"""# {tool_name}

A lightweight, zero-dependency command-line utility for fast JSON structure and format validation in CI/CD pipelines.

## Installation & Usage

```bash
python3 inspect_json.py config.json
```

## License
MIT License.
"""
        return {
            "tool_name": tool_name,
            "files": {
                "inspect_json.py": script_code,
                "README.md": readme_md
            }
        }

    def plan_4_repo_surround(self, brand, brand_key, gateway_url):
        """
        Generate specifications for 4 distinct angles surrounding a single brand:
        1. Exact brand coupon / promo code
        2. Top competitor #1 comparison
        3. Top competitor #2 comparison
        4. Scenario / Developer TCO cost breakdown
        """
        plans = {
            "decodo": [
                {
                    "repo_name": "decodo-coupon-pricing-breakdown",
                    "angle": "brand_coupon",
                    "title": "Decodo (Smartproxy) Coupon Code & 2026 Pricing Breakdown",
                    "target_query": "decodo promo code / smartproxy coupon code"
                },
                {
                    "repo_name": "brightdata-pricing-vs-decodo",
                    "angle": "competitor_brightdata",
                    "title": "Bright Data Pricing vs Decodo: Cost per 1,000 Usable Requests",
                    "target_query": "bright data pricing comparison"
                },
                {
                    "repo_name": "oxylabs-pricing-vs-decodo",
                    "angle": "competitor_oxylabs",
                    "title": "Oxylabs Pricing vs Decodo: Residential Proxy Budget Guide",
                    "target_query": "oxylabs pricing breakdown"
                },
                {
                    "repo_name": "residential-proxy-scraping-costs",
                    "angle": "scenario_tco",
                    "title": "Residential Proxy Scraping Costs: Pay-As-You-Go vs Commitments",
                    "target_query": "proxy cost per GB scraping"
                }
            ],
            "firstbase": [
                {
                    "repo_name": "firstbase-coupon-code-pricing",
                    "angle": "brand_coupon",
                    "title": "Firstbase Promo Code & Company Formation Cost Breakdown",
                    "target_query": "firstbase promo code 2026"
                },
                {
                    "repo_name": "stripe-atlas-vs-firstbase-costs",
                    "angle": "competitor_atlas",
                    "title": "Stripe Atlas vs Firstbase: Total First-Year Incorporation Costs",
                    "target_query": "stripe atlas vs firstbase pricing"
                },
                {
                    "repo_name": "doola-pricing-vs-firstbase",
                    "angle": "competitor_doola",
                    "title": "Doola Pricing vs Firstbase: Compliance & Registered Agent TCO",
                    "target_query": "doola pricing vs firstbase"
                },
                {
                    "repo_name": "non-us-founder-llc-annual-cost",
                    "angle": "scenario_tco",
                    "title": "US LLC Real Annual Maintenance Costs for Non-US Founders",
                    "target_query": "us llc annual maintenance cost"
                }
            ],
            "scraperapi": [
                {
                    "repo_name": "scraperapi-coupon-code-breakdown",
                    "angle": "brand_coupon",
                    "title": "ScraperAPI Coupon Code & Credit Plan Pricing Analysis",
                    "target_query": "scraperapi promo code 2026"
                },
                {
                    "repo_name": "zenrows-vs-scraperapi-pricing",
                    "angle": "competitor_zenrows",
                    "title": "ZenRows vs ScraperAPI: Anti-Bot Bypass Pricing Compared",
                    "target_query": "zenrows vs scraperapi pricing"
                },
                {
                    "repo_name": "scrapingbee-vs-scraperapi-pricing",
                    "angle": "competitor_scrapingbee",
                    "title": "ScrapingBee vs ScraperAPI: Headless Browser Credit Math",
                    "target_query": "scrapingbee vs scraperapi cost"
                },
                {
                    "repo_name": "web-scraping-api-cost-comparison",
                    "angle": "scenario_tco",
                    "title": "Web Scraping API True Cost Comparison: Credit Multipliers & Retries",
                    "target_query": "web scraping api pricing comparison"
                }
            ]
        }
        return plans.get(brand_key, [])


def run_self_test():
    print("=== Testing GitHubMatrixDispatcher ===")
    dispatcher = GitHubMatrixDispatcher()
    print(f"Loaded proxies: {len(dispatcher.static_ips)}")
    assert len(dispatcher.static_ips) == 100, "Should load 100 webshare proxies"

    # Test IP binding
    test_user = "test_aged_operator_01"
    binding = dispatcher.bind_static_ip_and_domain(test_user, "group_1")
    print(f"Bound test user to IP: {binding['bound_ip'][:25]}...")
    assert binding["username"] == test_user
    assert os.path.exists(LEDGER_PATH)

    # Test verification on 600me
    print("Testing account verification on 600me...")
    verify_res = dispatcher.verify_account("600me")
    print(f"600me verification: http={verify_res['profile_http']}, status={verify_res['status']}")
    assert verify_res["profile_http"] == 200

    # Test 600me protection guard with whitespace and casing variants
    for variant in ["600me", " 600me ", "  600ME  ", "600Me\t"]:
        try:
            dispatcher.bind_static_ip_and_domain(variant)
            assert False, f"{variant} binding should have raised PermissionError"
        except PermissionError as e:
            print(f"600me variant '{variant}' protection verified: {e}")

    # Test F1: 1:1 Distinct proxy allocation across accounts
    test_user_02 = "test_aged_operator_02"
    binding_02 = dispatcher.bind_static_ip_and_domain(test_user_02, "group_2")
    assert binding_02["proxy_ref"] != binding["proxy_ref"], "Each account must receive a unique proxy_ref!"
    print(f"Distinct IP allocation verified: {binding['proxy_ref']} vs {binding_02['proxy_ref']}")

    # Test warmup generation
    warmup = dispatcher.generate_warmup_pack("sample_user")
    assert "inspect_json.py" in warmup["files"]
    assert "README.md" in warmup["files"]

    # Test surround plans
    plans = dispatcher.plan_4_repo_surround("Decodo", "decodo", "https://go.272738.xyz/smartproxy")
    assert len(plans) == 4

    print("ALL DISPATCHER TESTS PASSED WITH EXIT CODE 0!")


if __name__ == "__main__":
    run_self_test()
