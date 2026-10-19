#!/usr/bin/env python3
"""Step 8 acceptance: GitHub profile portal + 5 repos (homepage/topics/release) + 4 HF Static Spaces.

Run:  python3 verify_step8_matrix.py
Exit code 0 only when every assertion below holds.
"""
import json
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

WORKSPACES = pathlib.Path("/Users/a600/project-workspaces(项目工作区)")
REPOS = {
    "check-proxy-tax": {},
    "awesome-residential-proxies-benchmark": {},
    "awesome-web-scraping-apis-benchmark": {},
    "awesome-gpu-cloud-pricing-benchmark": {},
    "awesome-indie-global-payments-matrix": {},
}
LOCAL = {
    "kais-proxy-cps-benchmark": "https://github.com/600me/awesome-residential-proxies-benchmark",
    "kais-global-payments-matrix": "https://github.com/600me/awesome-indie-global-payments-matrix",
    "kais-gpu-cloud-benchmark": "https://github.com/600me/awesome-gpu-cloud-pricing-benchmark",
    "kais-scraping-apis-benchmark": "https://github.com/600me/awesome-web-scraping-apis-benchmark",
}
SPACES = {
    "residential-proxy-sticky-session-calculator": "https://600me-residential-proxy-sticky-session-calculator.static.hf.space/index.html",
    "ai-saas-stripe-vs-mor-tax-calculator": "https://600me-ai-saas-stripe-vs-mor-tax-calculator.static.hf.space/index.html",
    "llm-gpu-cost-calculator": "https://600me-llm-gpu-cost-calculator.static.hf.space/index.html",
    "rag-web-scraping-cost-calculator": "https://600me-rag-web-scraping-cost-calculator.static.hf.space/index.html",
}

TOKEN = None
try:
    with open("/Users/a600/.secrets(密钥)/github-token(GitHub发帖令牌).env") as fh:
        for line in fh:
            if line.startswith("GITHUB_TOKEN="):
                TOKEN = line.split("=", 1)[1].strip().strip('"').strip("'")
except FileNotFoundError:
    pass

failures = []
checks = []


def record(ok, label, detail=""):
    checks.append((ok, label, detail))
    if not ok:
        failures.append(label)
    print(("PASS  " if ok else "FAIL  ") + label + (("  | " + str(detail)) if detail else ""))


def http_status(url, token=None, accept="application/vnd.github+json", timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "verify-step8/1.0", "Accept": accept})
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def api(path):
    status, body = http_status("https://api.github.com" + path, token=TOKEN)
    try:
        return status, json.loads(body)
    except Exception:
        return status, body


print("== 1. GitHub profile portal ==")
if TOKEN is None:
    record(False, "GitHub token readable from secrets store")
else:
    status, repo = api("/repos/600me/600me")
    record(status == 200 and isinstance(repo, dict), "600me/600me repo exists (HTTP 200)", status)
    record(repo.get("visibility") == "public", "600me/600me is public", repo.get("visibility"))
    record(repo.get("homepage") == "https://scrape.mybskm.top/calculator/",
           "600me/600me homepage set", repo.get("homepage"))
    status, tree = api("/repos/600me/600me/contents/README.md")
    record(status == 200, "600me/600me README.md present", status)
    if status == 200 and isinstance(tree, dict):
        raw = urllib.request.urlopen(
            urllib.request.Request(tree["download_url"], headers={"User-Agent": "verify-step8/1.0"}),
            timeout=30).read().decode()
        for needle in ("llm-gpu-cost-calculator", "rag-web-scraping-cost-calculator",
                       "residential-proxy-sticky-session-calculator",
                       "ai-saas-stripe-vs-mor-tax-calculator", "check-proxy-tax", "utm_source=gh_profile"):
            record(needle in raw, "profile README mentions %s" % needle)
        record(raw.count("utm_source=gh_profile") >= 12,
               "profile README carries gh_profile attribution on the tool/blog links",
               raw.count("utm_source=gh_profile"))

print("\n== 2. Five core repos: homepage + topics + release ==")
for repo in REPOS:
    status, meta = api("/repos/600me/" + repo)
    if status != 200 or not isinstance(meta, dict):
        record(False, "%s metadata reachable" % repo, status)
        continue
    record(bool(meta.get("homepage")), "%s homepage non-empty" % repo, meta.get("homepage"))
    topics = meta.get("topics") or []
    record(len(topics) >= 10, "%s topics >= 10" % repo, len(topics))
    record(len(set(topics)) == len(topics) and all(t == t.lower() and " " not in t for t in topics),
           "%s topics are unique lowercase hyphen tags" % repo, topics[:3])
    status, releases = api("/repos/600me/%s/releases" % repo)
    record(status == 200 and isinstance(releases, list) and len(releases) >= 1,
           "%s has >= 1 release" % repo, len(releases) if isinstance(releases, list) else status)
    if isinstance(releases, list) and releases:
        rel = releases[0]
        record(rel.get("tag_name") == "v1.0.0", "%s release tag is v1.0.0" % repo, rel.get("tag_name"))
        record(rel.get("draft") is False and rel.get("prerelease") is False,
               "%s release is published (not draft/prerelease)" % repo)
        record(len(rel.get("body") or "") > 400, "%s release body is substantive" % repo,
               len(rel.get("body") or ""))
        st, _ = http_status(rel["html_url"], accept="text/html")
        record(st == 200, "%s release page HTTP 200" % repo, st)

print("\n== 3. Hugging Face Static Spaces (4/4 matrix) ==")
for name, url in SPACES.items():
    st, _ = http_status("https://huggingface.co/api/spaces/600me/" + name, accept="application/json")
    record(st == 200, "HF space 600me/%s metadata HTTP 200" % name, st)
    st, body = http_status(url, accept="text/html")
    record(st == 200, "HF static domain serves %s" % name, st)
    if st == 200:
        for needle in ("huggingface.co/spaces/600me/", "mybskm.top"):
            record(needle in body, "%s page links %s" % (name, needle))
        record("go.272738.xyz" in body, "%s page carries the affiliate CTA" % name)

print("\n== 4. New spaces: exact acceptance criteria ==")
for name in ("residential-proxy-sticky-session-calculator", "ai-saas-stripe-vs-mor-tax-calculator"):
    st, meta = http_status("https://huggingface.co/api/spaces/600me/" + name, accept="application/json")
    stage = json.loads(meta)["runtime"]["stage"] if st == 200 else "?"
    record(stage == "RUNNING", "600me/%s stage RUNNING" % name, stage)

print("\n== 5. Local repositories clean and pushed ==")
for local, remote in LOCAL.items():
    path = WORKSPACES / local
    branch = subprocess.run(["git", "-C", str(path), "status", "-sb"], capture_output=True, text=True).stdout.strip()
    record("\n" not in branch and "[" not in branch, "%s git status -sb clean" % local, branch)
    ahead = subprocess.run(["git", "-C", str(path), "rev-list", "--count", "@{u}..HEAD"],
                           capture_output=True, text=True).stdout.strip()
    record(ahead == "0", "%s has no unpushed commits" % local, ahead)
    head = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    rhead = subprocess.run(["git", "-C", str(path), "rev-parse", "@{u}"], capture_output=True, text=True).stdout.strip()
    record(head == rhead, "%s HEAD == upstream" % local, head[:8])

print("\n== 6. New mirror interlinks four Spaces ==")
for local in ("kais-proxy-cps-benchmark", "kais-global-payments-matrix"):
    html = (WORKSPACES / local / "hf-space-mirror" / "index.html").read_text(encoding="utf-8")
    for name in SPACES:
        record("600me/" + name in html, "%s mirror links space %s" % (local, name))
    record('href="/' not in html, "%s mirror has no broken root-relative links" % local)

print("\n%d checks, %d failures" % (len(checks), len(failures)))
if failures:
    print("FAILED: " + "; ".join(failures))
sys.exit(1 if failures else 0)
