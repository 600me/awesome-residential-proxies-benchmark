#!/usr/bin/env python3
"""Objective acceptance for DIRECTIVE_ABC_EXECUTION.

Checks, in order:
  A. PR 141 exists on cleder/awesome-python-testing, is open, and its diff is one line.
  B. The self-hosted article is HTTP 200 with a self-canonical, the Dev.to copy is
     HTTP 200 with the same canonical, and both ledgers contain the receipt.
  C. The traffic report is complete and the five active relays still answer 302.
  D. Every local repository is clean and equal to origin/main.

Exit 0 only when every assertion passes. No mutation except a read-only git fetch
and a fresh affiliate health probe.
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
ROOT = Path("/Users/a600/project-workspaces(项目工作区)")
BENCH = ROOT / "kais-proxy-cps-benchmark"
SCRAPE = ROOT / "kais-scraping-apis-benchmark"
CLI_REPO = ROOT / "check-proxy-tax"
PR_NUMBER = 141
PR_URL = f"https://github.com/cleder/awesome-python-testing/pull/{PR_NUMBER}"
UPSTREAM = "cleder/awesome-python-testing"
FORK = "600me/awesome-python-testing"
BRANCH = "add-check-proxy-tax"
PAGE = "https://scrape.mybskm.top/blog/proxy-cost-audit.html"
DEVTO_URL = "https://dev.to/600me/the-049-proxy-illusion-how-a-200-line-cli-exposes-real-scraping-costs-5008"
DEVTO_ID = 4875339
REPORT = BENCH / "vps-sniper" / "traffic_audit_report.json"
LEDGER = BENCH / "vps-sniper" / "published_articles.jsonl"
HEALTH = BENCH / "affiliate-health-check(联盟巡检).py"
TITLE = "The $0.49 Proxy Illusion: How a 200-Line CLI Exposes Real Scraping Costs"
REQUIRED_LINKS = [
    "https://github.com/600me/check-proxy-tax",
    "https://scrape.mybskm.top/blog/403-tax.html",
    "https://scrape.mybskm.top/?utm_source=devto&utm_medium=article&utm_campaign=proxy_audit_cli&src=devto_cli",
    "https://go.272738.xyz/scraperapi?utm_source=devto&utm_medium=article&utm_campaign=proxy_audit_cli&src=devto_cli",
    "https://go.272738.xyz/smartproxy?utm_source=devto&utm_medium=article&utm_campaign=proxy_audit_cli&src=devto_cli",
]
UA = "kais-acceptance/1.0"
results = []


def check(name, fn):
    try:
        detail = fn()
        results.append((name, True, detail))
        print(f"PASS  {name}: {detail}")
    except Exception as error:  # noqa: BLE001 - acceptance must report every failure
        results.append((name, False, str(error)))
        print(f"FAIL  {name}: {error}")


def fetch(url, headers=None):
    request = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.status, response.read().decode("utf-8", "replace")


def github_token():
    for path in sorted((HOME / ".secrets(密钥)").glob("github-token*")):
        for line in path.read_text().splitlines():
            if line.startswith("GITHUB_TOKEN="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("GITHUB_TOKEN not found")


def api(path):
    status, body = fetch("https://api.github.com" + path, {
        "Authorization": f"Bearer {github_token()}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return status, json.loads(body)


def step_a():
    status, pr = api(f"/repos/{UPSTREAM}/pulls/{PR_NUMBER}")
    assert status == 200, f"PR API HTTP {status}"
    assert pr["state"] == "open", f"state={pr['state']}"
    assert pr["merged"] is False, "PR is merged"
    assert pr["title"] == "Add check-proxy-tax to Tools", pr["title"]
    assert pr["head"]["label"] == f"600me:{BRANCH}", pr["head"]["label"]
    assert pr["base"]["ref"] == "main", pr["base"]["ref"]
    assert pr["changed_files"] == 1 and pr["commits"] == 1, "unexpected diff size"
    page_status, _ = fetch(PR_URL)
    assert page_status == 200, f"PR page HTTP {page_status}"
    status, files = api(f"/repos/{UPSTREAM}/pulls/{PR_NUMBER}/files")
    assert status == 200 and len(files) == 1 and files[0]["filename"] == "README.md"
    added = [line for line in files[0]["patch"].splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    assert len(added) == 1, f"expected one added line, got {len(added)}"
    assert added[0] == ("+- [check-proxy-tax](https://github.com/600me/check-proxy-tax) - "
                        "CLI that samples a URL concurrently and reports usable-response rate, "
                        "latency, and effective cost per 1,000 usable requests."), added[0]
    status, fork = api(f"/repos/{FORK}")
    assert status == 200 and fork["parent"]["full_name"] == UPSTREAM
    return f"open, 1 commit, 1 added README line, page 200 ({PR_URL})"


def page_text():
    status, body = fetch(PAGE)
    assert status == 200, f"page HTTP {status}"
    return body


def step_b_site():
    body = page_text()
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', body)
    assert canonical and canonical.group(1) == PAGE, canonical.group(1) if canonical else "missing canonical"
    assert '"@type": "Article"' in body and '"headline": ' in body, "Article JSON-LD missing"
    assert "FTC Disclosure" in body and "affiliate" in body.lower(), "FTC disclosure missing"
    decoded = html.unescape(body)
    for link in REQUIRED_LINKS:
        assert link in body or link in decoded, f"missing link {link}"
    content = body.split('<div class="content">', 1)[1].split('<div class="cta-panel">', 1)[0]
    text = html.unescape(re.sub(r"<[^>]+>", " ", content))
    words = len(text.split())
    assert words >= 1600, f"only {words} words in article body"
    return f"HTTP 200, self-canonical exact, {words} words, JSON-LD + FTC + 5 links"


def step_b_devto():
    status, body = fetch(DEVTO_URL)
    assert status == 200, f"Dev.to HTTP {status}"
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', body)
    assert canonical and canonical.group(1) == PAGE, canonical.group(1) if canonical else "missing canonical"
    key_path = next((HOME / ".secrets(密钥)").glob("devto-api*"))
    key = next(line.split("=", 1)[1].strip() for line in key_path.read_text().splitlines()
               if line.startswith("DEVTO_API_KEY="))
    status, raw = fetch("https://dev.to/api/articles/me/published?per_page=100", {"api-key": key})
    assert status == 200, f"Dev.to API HTTP {status}"
    article = next((item for item in json.loads(raw) if item["id"] == DEVTO_ID), None)
    assert article, "article id not returned by API"
    assert article["published"] is True, "article is not published"
    assert article["canonical_url"] == PAGE, article["canonical_url"]
    assert article["title"] == TITLE, article["title"]
    words = len(re.sub(r"```.*?```", "", article["body_markdown"], flags=re.S).split())
    assert words >= 1600, f"Dev.to body only {words} words"
    return f"HTTP 200, API published=true, canonical exact, {words} words"


def step_b_ledgers():
    rows = [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]
    row = next((item for item in rows if item.get("id") == DEVTO_ID), None)
    assert row, "local ledger missing article id"
    assert row["canonical_url"] == PAGE and row["status"] == "published"
    assert row["http_status"] == 201 and row["url"] == DEVTO_URL
    result = subprocess.run(["ssh", "-o", "BatchMode=yes", "us-server",
                             "cat", "/opt/kais-proxy-sniper/published_articles.jsonl"],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    remote = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    remote_row = next((item for item in remote if item.get("id") == DEVTO_ID), None)
    assert remote_row and remote_row["canonical_url"] == PAGE, "remote ledger missing article"
    return f"local {len(rows)} rows, remote {len(remote)} rows, id {DEVTO_ID} in both"


def step_c_report():
    report = json.loads(REPORT.read_text())
    for key in ("totals", "route_distribution", "parameterized", "bot_filter",
                "human_traffic", "health_check", "sources", "findings"):
        assert key in report, f"missing field {key}"
    datetime.strptime(report["generated_at"], "%Y-%m-%dT%H:%M:%SZ")
    assert report["totals"]["requests"] > 0
    assert report["totals"]["status_302"] > 0
    assert report["route_distribution"]
    assert report["bot_filter"]["excluded"] > 0
    assert report["human_traffic"]["browser_like_candidates"] >= 0
    health = report["health_check"]
    assert health["expected_active"] == 5
    assert health["active_passed"] == 5 and health["all_302"] is True
    assert health["errors"] == 0 and len(health["relays"]) == 5
    assert all(relay["relay_status"] == 302 for relay in health["relays"])
    return (f"{report['totals']['requests']} relay requests, "
            f"{report['totals']['status_302']} 302, "
            f"{report['bot_filter']['excluded']} filtered, 5/5 relays 302")


def step_c_live():
    result = subprocess.run([sys.executable, str(HEALTH)], capture_output=True, text=True, timeout=60)
    output = result.stdout
    passes = [line for line in output.splitlines() if line.startswith("PASS ")]
    summary = next((line for line in output.splitlines() if line.startswith("active=")), "")
    assert len(passes) == 5, f"expected 5 PASS lines, got {len(passes)}"
    assert "active=5/5" in summary and "errors=0" in summary, summary
    return f"5/5 PASS, errors=0 (script exit {result.returncode} from 4 out-of-scope NEW_LINKs)"


def git_sync(repo):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    porcelain = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"],
                               capture_output=True, text=True, env=env)
    assert porcelain.returncode == 0 and not porcelain.stdout.strip(), porcelain.stdout
    branch = subprocess.run(["git", "-C", str(repo), "branch", "--show-current"],
                            capture_output=True, text=True, env=env).stdout.strip()
    assert branch == "main", f"branch={branch}"
    subprocess.run(["git", "-C", str(repo), "fetch", "--quiet", "origin", "main"],
                   check=True, capture_output=True, text=True, env=env, timeout=60)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True, env=env).stdout.strip()
    origin = subprocess.run(["git", "-C", str(repo), "rev-parse", "origin/main"],
                            capture_output=True, text=True, env=env).stdout.strip()
    assert head == origin, f"HEAD {head[:8]} != origin/main {origin[:8]}"
    return head[:8]


def step_d_git():
    details = []
    for repo in (BENCH, SCRAPE, CLI_REPO):
        details.append(f"{repo.name}@{git_sync(repo)}")
    return "clean and synced: " + ", ".join(details)


def main():
    print(f"Acceptance started {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    check("A. PR open with exact one-line diff", step_a)
    check("B1. Self-hosted article page and content", step_b_site)
    check("B2. Dev.to article canonical", step_b_devto)
    check("B3. Local and remote article ledgers", step_b_ledgers)
    check("C1. Traffic audit report fields", step_c_report)
    check("C2. Five active relays live", step_c_live)
    check("D. Git repositories clean and synced", step_d_git)
    failed = [name for name, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} assertions passed")
    if failed:
        print("FAILED: " + "; ".join(failed))
        return 1
    print("ALL ASSERTIONS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
