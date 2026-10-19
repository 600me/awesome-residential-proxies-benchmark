#!/usr/bin/env python3
"""Screen awesome-list candidates concurrently (16 workers, 8s timeouts).

Budget: <=15s wall clock for the whole screen. Search results carry stars /
archived / pushed_at, so no per-repo metadata call is needed. Only the top 18
starred candidates get a merged-PR check, and only the top 6 of those get a
README/CONTRIBUTING rule scan.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

TOKEN = re.search(r"GITHUB_TOKEN\s*=\s*(\S+)",
                  open("/Users/a600/.secrets(密钥)/github-token(GitHub发帖令牌).env").read()).group(1)
H = {"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json",
     "User-Agent": "600me-screen", "X-GitHub-Api-Version": "2022-11-28"}
QUERIES = [
    "awesome python tools in:name,description stars:>300",
    "awesome python cli in:name,description stars:>200",
    "awesome http api tools in:name,description stars:>200",
    "awesome web scraping in:name,description stars:>150",
    "awesome llm rag engineering in:name,description stars:>200",
    "awesome indie saas gpu cloud in:name,description stars:>100",
]
SUFFIX = " archived:false pushed:>2026-07-21 fork:false"
EXCLUDE = {"cleder/awesome-python-testing", "denji/awesome-http-benchmark",
           "aliesbelik/load-testing-toolkit", "YSGStudyHards/Awesome-Tools",
           "vinta/awesome-python"}
BAD = ["do not submit", "no self-promotion", "no self promotion", "self-promotion is not",
       "no ai-generated", "no ai generated", "ai-generated content", "no ai tools",
       "minimum of 6 months", "at least 6 months", "account must be", "at least 30 days",
       "older than 30 days", "minimum star", "requires 100 stars", "at least 100 stars",
       "not accept", "we do not accept"]


def get(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.load(r)
    except Exception as e:  # noqa: BLE001
        return {"_error": str(e)}


def search(q):
    d = get("/search/repositories?q=%s&sort=stars&order=desc&per_page=6" % urllib.parse.quote(q + SUFFIX))
    return d.get("items", [])


def raw(full, path):
    req = urllib.request.Request("https://raw.githubusercontent.com/%s/HEAD/%s" % (full, path),
                                 headers={"User-Agent": "600me-screen"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return ""


def merged_recent(full):
    pulls = get("/repos/%s/pulls?state=closed&sort=updated&direction=desc&per_page=5" % full)
    if isinstance(pulls, dict):
        return None
    for p in pulls:
        if p.get("merged_at"):
            return p["merged_at"]
    return None


def rules(full):
    text = (raw(full, "CONTRIBUTING.md") + "\n" + raw(full, "README.md")).lower()
    hits = [w for w in BAD if w in text]
    return hits


def main():
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=16) as pool:
        items = {}
        for lst in pool.map(search, QUERIES):
            for it in lst:
                if it["full_name"] not in EXCLUDE:
                    items[it["full_name"]] = it
        top = sorted(items.values(), key=lambda r: r["stargazers_count"], reverse=True)[:18]
        merged = dict(zip([r["full_name"] for r in top], pool.map(lambda r: merged_recent(r["full_name"]), top)))
    live = [r for r in top if merged.get(r["full_name"]) and merged[r["full_name"]] >= "2026-07-21"]
    live.sort(key=lambda r: r["stargazers_count"], reverse=True)
    with ThreadPoolExecutor(max_workers=16) as pool:
        hits = dict(zip([r["full_name"] for r in live[:6]], pool.map(lambda r: rules(r["full_name"]), live[:6])))
    passed, rejected = [], []
    for r in live:
        full = r["full_name"]
        if full in hits:
            if hits[full]:
                rejected.append({"repo": full, "reject": "rule gate: %s" % hits[full]})
                continue
        passed.append({"repo": full, "stars": r["stargazers_count"], "pushed_at": r["pushed_at"],
                       "last_merged": merged[full], "desc": (r["description"] or "")[:100],
                       "rules_scanned": full in hits})
    for full, m in merged.items():
        if not m or m < "2026-07-21":
            rejected.append({"repo": full, "reject": "no merged PR within 90d (%s)" % m})
    print(json.dumps({"candidates": len(items), "seconds": round(time.time() - t0, 1),
                      "passed": passed, "rejected": rejected}, indent=1))


if __name__ == "__main__":
    main()
