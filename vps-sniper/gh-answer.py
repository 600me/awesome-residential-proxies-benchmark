#!/usr/bin/env python3
"""Turn public GitHub issue reports into scored, four-part technical reply drafts.

    python3 gh-answer.py --dry-run   # offline fixtures, no GitHub API calls
    python3 gh-answer.py --once      # one real public GitHub search round
    python3 gh-answer.py             # same as --once

The script is read-only against GitHub: it never posts comments, opens PRs or
uses credentials other than an optional GITHUB_TOKEN / GH_TOKEN for rate limits.
Candidates are appended atomically to outreach_gh.jsonl beside this file.
Only the Python standard library is used; no database or message queue.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(HERE, "outreach_gh.jsonl")
SEARCH_URL = "https://api.github.com/search/issues"
REPO_URL = "https://api.github.com/repos/"
USER_AGENT = "kais-proxy-benchmark-gh-answer/1.0 (+https://proxy.mybskm.top/)"
MAX_BYTES = 2 * 1024 * 1024
MIN_SCORE = 3

INTENT_RE = re.compile(
    r"(?:\?|how (?:do|can|should|to)|need (?:help|advice|recommendations?)|"
    r"looking for|recommend|suggest|alternatives?|workaround|anyone|"
    r"is there|best way|help me|advice)",
    re.I,
)


def log(event, **fields):
    """Diagnostics go to stderr so stdout stays machine-readable JSONL."""
    print(json.dumps({"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      "event": event, **fields}, ensure_ascii=False),
          file=sys.stderr, flush=True)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def unique_matches(pattern, text, limit=4):
    found = []
    for match in pattern.finditer(text):
        value = match.group(0).strip().lower()
        if value and value not in found:
            found.append(value)
        if len(found) >= limit:
            break
    return found


def score_issue(text, category):
    """Three independent, category-specific signals; the gate is >= 3."""
    spec = CATEGORIES[category]
    evidence = {
        "error": unique_matches(spec["error_re"], text),
        "vendor": unique_matches(spec["vendor_re"], text),
        "intent": unique_matches(INTENT_RE, text),
    }
    return sum(1 for values in evidence.values() if values), evidence


CATEGORIES = {
    "proxy": {
        "keywords": ("cloudflare 403", "residential proxy"),
        "error_re": re.compile(
            r"\b(?:403|429|407|blocked|banned|denied|timeout|timed out|rate[- ]?limit|"
            r"challenge|captcha|cf_clearance)\b", re.I),
        "vendor_re": re.compile(
            r"\b(?:cloudflare|smartproxy|decodo|bright\s?data|oxylabs|apify|iproyal|"
            r"soax|zyte|residential\s+prox(?:y|ies)|prox(?:y|ies)|datacenter|asn)\b", re.I),
        "gate_re": re.compile(
            r"(?=.*\b(?:prox(?:y|ies)|cloudflare|residential|smartproxy|decodo|"
            r"bright\s?data|oxylabs)\b)"
            r"(?=.*\b(?:403|block(?:ed|ing)?|banned|denied|challenge|captcha)\b)", re.I),
        "repo": "600me/awesome-residential-proxies-benchmark",
        "root_cause": (
            "A Cloudflare 403 through a residential proxy is usually a fingerprint/session "
            "mismatch, not a missing `User-Agent`. Cloudflare scores the TLS/JA3 and HTTP/2 "
            "fingerprint, ASN reputation, cookie (`cf_clearance`) consistency and request rate "
            "together. A residential exit fixes only the ASN signal: a Python `requests`/`urllib` "
            "TLS stack, an IP rotation mid-session, or a clearance cookie issued to a different IP "
            "will still return 403."
        ),
        "command": (
            'curl -sS -x "$PROXY_URL" -o /dev/null -w '
            '\'status=%{http_code} tls=%{time_appconnect}s\\n\' "$TARGET_URL"'
        ),
        "verify_note": (
            "Run it once with `PROXY_URL` empty and once with the proxy, using the same target and "
            "headers. A direct 200 plus a proxied 403 isolates the exit/fingerprint path rather "
            "than a target outage."
        ),
        "fix": (
            "Use a sticky session for at least the checkout/login flow, keep one egress IP for the "
            "whole cookie lifetime, and present a real browser TLS stack (`curl_cffi` with "
            "`impersonate=\"chrome\"` or a browser context). Lower concurrency to roughly 1 request/s "
            "per IP and retry 403 with backoff; rotating IP on every request makes clearance worse."
        ),
    },
    "scraping": {
        "keywords": ("turnstile", "scraping blocked"),
        "error_re": re.compile(
            r"\b(?:turnstile|captcha|blocked|403|429|rate[- ]?limit|challenge|"
            r"timeout)\b", re.I),
        "vendor_re": re.compile(
            r"\b(?:turnstile|cloudflare|playwright|puppeteer|selenium|scraperapi|"
            r"apify|zyte|scrap(?:e|er|ers|ing)|crawl(?:er|ers|ing)?|headless|"
            r"chromium|docker)\b", re.I),
        "gate_re": re.compile(
            r"(?=.*\b(?:turnstile|scrap(?:e|er|ers|ing)|crawl(?:er|ers|ing)?|"
            r"cloudflare|playwright|puppeteer|selenium)\b)"
            r"(?=.*\b(?:turnstile|captcha|block(?:ed|ing)?|403|429|challenge)\b)", re.I),
        "repo": "600me/awesome-web-scraping-apis-benchmark",
        "root_cause": (
            "Turnstile is not a plain image CAPTCHA. The token is bound to the sitekey, action, "
            "cdata, the browser fingerprint (fonts, canvas/WebGL, timezone, languages) and the "
            "egress IP. Headless Chromium commonly fails because Arial/Helvetica are absent, "
            "`navigator.webdriver` is true, or the token is solved on one IP and submitted from "
            "another. A token is also single-use."
        ),
        "command": (
            "curl -sS -o /dev/null -w 'turnstile_js=%{http_code} "
            "tls=%{time_appconnect}s\\n' https://challenges.cloudflare.com/turnstile/v0/api.js"
        ),
        "verify_note": (
            "If this returns 200, the challenge script is reachable and the failure is in browser "
            "fingerprint or token binding, not DNS or egress filtering."
        ),
        "fix": (
            "Use one persistent browser context per identity, install the usual font pack, run "
            "headful under Xvfb when needed, keep one egress IP for the page load and token submit, "
            "and read the token from `cf-turnstile-response` only after the callback fires. Do not "
            "reuse tokens or parallelize the widget across contexts."
        ),
    },
    "payments": {
        "keywords": ("stripe banned", "stripe alternative"),
        "error_re": re.compile(
            r"\b(?:banned|closed|suspended|deactivated|chargeback|dispute|reserve|"
            r"restricted|declined|frozen|payout\s+hold|5\.7)\b", re.I),
        "vendor_re": re.compile(
            r"\b(?:stripe|paddle|lemonsqueezy|paypal|wise|merchant\s+account|"
            r"payment\s+(?:processor|gateway)|billing)\b", re.I),
        "gate_re": re.compile(
            r"(?=.*\b(?:stripe|payment|payout|merchant|chargeback|billing|paddle|"
            r"lemonsqueezy|paypal)\b)"
            r"(?=.*\b(?:banned|closed|suspended|chargeback|alternative|reserve|"
            r"restricted|declined|frozen|failed)\b)", re.I),
        "repo": "600me/awesome-indie-global-payments-matrix",
        "root_cause": (
            "A Stripe closure is a risk-model decision, not a pricing threshold. The usual triggers "
            "are a chargeback ratio above 0.75%, a sudden jump in cross-border volume, a restricted "
            "business category, a statement descriptor that does not match the site, or an "
            "unresolved reserve. The ~5.7% all-in effective cost on cross-border charges "
            "(2.9% + $0.30, +1.5% international, +1% conversion) hurts margin but does not itself "
            "trigger a ban; reopening with the same risk profile usually gets closed again."
        ),
        "command": (
            'curl -sS -w \'\\nhttp=%{http_code}\\n\' '
            'https://api.stripe.com/v1/balance -u "$STRIPE_SECRET_KEY:"'
        ),
        "verify_note": (
            "A 200 with `available`/`pending` balances means the key and account are live; 401 means "
            "the key was revoked; 403 with a risk message means the account, not the API version, "
            "is restricted."
        ),
        "fix": (
            "Export the Dashboard risk view (chargeback rate, Radar blocks, dispute reasons), keep "
            "chargebacks below 0.5%, make the statement descriptor match the site, and add a clear "
            "refund policy. For global sales, a merchant-of-record such as Paddle or Lemon Squeezy "
            "removes the need for a US entity but shifts fees and payout timing; compare reserve, "
            "payout country, FX and effective rate before switching."
        ),
    },
    "gpu": {
        "keywords": ("runpod expensive", "h100 gpu cloud"),
        "error_re": re.compile(
            r"\b(?:expensive|cost(?:s|ly)?|price|pricing|cheaper|budget|billing|"
            r"invoice|overpriced)\b", re.I),
        "vendor_re": re.compile(
            r"\b(?:runpod|vast\.?ai|lambda\s?labs|coreweave|h100|a100|gpu|cuda|"
            r"nvidia|nvlink|sxm|pcie|aws|gcp|azure)\b", re.I),
        "gate_re": re.compile(
            r"(?=.*\b(?:gpu|h100|a100|runpod|vast\.?ai|cuda|nvidia)\b)"
            r"(?=.*\b(?:expensive|cost(?:s|ly)?|price|pricing|cheaper|budget|"
            r"billing|overpriced)\b)", re.I),
        "repo": "600me/awesome-gpu-cloud-pricing-benchmark",
        "root_cause": (
            "The H100 SXM premium is mostly interconnect and host topology, not the GPU die. SXM5 "
            "uses NVLink at roughly 900 GB/s and a 700 W board, while PCIe Gen5 x16 provides about "
            "64 GB/s at roughly 350 W. Providers price SXM higher because NVSwitch, host CPU/RAM, "
            "InfiniBand and capacity are included. RunPod Community vs Secure Cloud also changes "
            "preemption and host reliability, so the headline $/GPU-hour is not comparable until "
            "storage, egress, idle time and preemption are included."
        ),
        "command": (
            "nvidia-smi --query-gpu=name,memory.total,pcie.link.gen.current,"
            "pcie.link.width.current,power.limit --format=csv,noheader"
        ),
        "verify_note": (
            "This prints the actual link generation/width and power cap, so an SXM host is "
            "distinguishable from a PCIe host before comparing hourly prices."
        ),
        "fix": (
            "Match the interconnect to the workload: single-GPU inference is usually fine on PCIe, "
            "while multi-GPU training needs NVLink/SXM. For community or spot capacity, checkpoint "
            "every few minutes and price in preemption, storage and egress. Measure tokens/s per "
            "dollar on your own model instead of comparing headline $/GPU-hour."
        ),
    },
}


def build_draft(category, evidence):
    spec = CATEGORIES[category]
    target = "https://github.com/" + spec["repo"] + "?utm_source=gh_issue"
    signals = ", ".join(dict.fromkeys(value for value in
                                     evidence["error"][:2] + evidence["vendor"][:2]
                                     if value != "?"))
    lead = "The reported signals"
    if signals:
        lead += " (" + signals + ")"
    lead += " point to the **" + category + "** failure pattern."
    return (
        "**Root cause.** " + lead + " " + spec["root_cause"] + "\n\n"
        "**Verify it with one command.**\n\n"
        "```sh\n" + spec["command"] + "\n```\n\n"
        + spec["verify_note"] + "\n\n"
        "**What to change.** " + spec["fix"] + "\n\n"
        "Disclosure: I maintain the open-source benchmark at github.com/" + spec["repo"] + ". "
        "Measured success rate, latency, HTTP status and IP/ASN data: " + target
    )


def load_seen(path=LEDGER_PATH):
    seen = set()
    try:
        with open(path, encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if isinstance(record, dict) and isinstance(record.get("issue_url"), str):
                    seen.add(record["issue_url"])
    except FileNotFoundError:
        pass
    return seen


def append_record(record, path=LEDGER_PATH):
    """One O_APPEND write plus fsync keeps a complete JSON line contiguous."""
    line = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        original_size = os.fstat(fd).st_size
        if os.write(fd, line) != len(line):
            os.ftruncate(fd, original_size)
            raise OSError("incomplete ledger append")
        os.fsync(fd)
    finally:
        os.close(fd)


def make_record(category, issue, stars, score, evidence, dry_run):
    target = "https://github.com/" + CATEGORIES[category]["repo"] + "?utm_source=gh_issue"
    return {
        "time": now(),
        "issue_url": issue["issue_url"],
        "repo": issue["repo"],
        "stars": stars,
        "category": category,
        "score": score,
        "signals": evidence,
        "draft_response": build_draft(category, evidence),
        "recommended_target": target,
        "dry_run": dry_run,
    }


def github_get(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as error:
        detail = ""
        try:
            detail = error.read(200).decode("utf-8", "replace")
        except Exception:
            pass
        log("api_error", status=error.code, url=url.split("?", 1)[0], detail=detail[:160])
        return None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        log("api_error", url=url.split("?", 1)[0], detail=str(error)[:160])
        return None
    if len(raw) > MAX_BYTES:
        log("api_error", url=url.split("?", 1)[0], detail="response exceeds 2 MiB")
        return None
    try:
        return json.loads(raw)
    except (ValueError, TypeError) as error:
        log("api_error", url=url.split("?", 1)[0], detail="invalid JSON: " + str(error)[:120])
        return None


def search_issues(keyword, per_page=10):
    cutoff = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 365 * 86400))
    query = keyword + " in:title,body is:issue is:open updated:>=" + cutoff
    data = github_get(SEARCH_URL, {
        "q": query,
        "sort": "updated",
        "order": "desc",
        "per_page": str(per_page),
    })
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        return None
    return data["items"]


def repo_from_item(item):
    repository_url = item.get("repository_url") or ""
    marker = "/repos/"
    if marker not in repository_url:
        return ""
    return repository_url.split(marker, 1)[1].split("?", 1)[0].strip("/")


def issue_from_item(item):
    repo = repo_from_item(item)
    issue_url = item.get("html_url") or ""
    if not repo or not issue_url:
        return None
    return {
        "issue_url": issue_url,
        "repo": repo,
        "title": str(item.get("title") or ""),
        "body": str(item.get("body") or ""),
        "updated_at": str(item.get("updated_at") or ""),
    }


def fetch_stars(repo, cache):
    if repo in cache:
        return cache[repo]
    data = github_get(REPO_URL + urllib.parse.quote(repo, safe="/"))
    stars = data.get("stargazers_count") if isinstance(data, dict) else None
    cache[repo] = stars if isinstance(stars, int) else None
    return cache[repo]


def run_live(limit, per_page):
    seen = load_seen()
    cache = {}
    searched = 0
    emitted = 0
    for category, spec in CATEGORIES.items():
        candidates = {}
        for keyword in spec["keywords"]:
            items = search_issues(keyword, per_page)
            if items is None:
                continue
            searched += 1
            for item in items:
                if item.get("pull_request") or item.get("state") != "open" or item.get("locked"):
                    continue
                user = item.get("user") or {}
                if isinstance(user, dict) and user.get("type") == "Bot":
                    continue
                issue = issue_from_item(item)
                if not issue or issue["issue_url"] in seen:
                    continue
                if issue["repo"].split("/", 1)[0].lower() == "600me":
                    continue
                if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", issue["repo"]):
                    continue
                text = issue["title"] + "\n" + issue["body"]
                # Require the category term in the title: huge tracker threads often
                # mention Cloudflare/Stripe/GPU in passing and are not support asks.
                if not spec["gate_re"].search(issue["title"]):
                    continue
                score, evidence = score_issue(text, category)
                if score < MIN_SCORE:
                    continue
                issue["score"] = score
                issue["evidence"] = evidence
                candidates[issue["issue_url"]] = issue
        ranked = sorted(candidates.values(),
                        key=lambda value: (value["score"], value["updated_at"]),
                        reverse=True)
        selected = 0
        for issue in ranked:
            if selected >= limit:
                break
            stars = fetch_stars(issue["repo"], cache)
            record = make_record(category, issue, stars, issue["score"],
                                 issue["evidence"], dry_run=False)
            append_record(record)
            seen.add(record["issue_url"])
            print(json.dumps(record, ensure_ascii=False), flush=True)
            selected += 1
            emitted += 1
    log("round", searched=searched, emitted=emitted, limit=limit, ledger=LEDGER_PATH)
    return 0 if searched else 1


FIXTURES = (
    {
        "category": "proxy",
        "repo": "acme/data-pipeline",
        "number": 312,
        "stars": 1842,
        "title": "Cloudflare 403 with Smartproxy residential proxy on checkout page",
        "body": ("Direct requests return 200, but through Smartproxy we get HTTP 403 after 5 "
                 "requests. Sticky session is on. How do we fix this?"),
        "updated_at": "2026-10-18T08:12:00Z",
    },
    {
        "category": "proxy",
        "repo": "northwind/scrape-worker",
        "number": 87,
        "stars": 436,
        "title": "Residential proxy still gets Cloudflare 403 on login",
        "body": ("Bright Data rotating session returns 403 on the login POST. Need a workaround "
                 "without rotating the IP on every request."),
        "updated_at": "2026-10-18T07:40:00Z",
    },
    {
        "category": "scraping",
        "repo": "octo-labs/pricing-crawler",
        "number": 154,
        "stars": 1207,
        "title": "Turnstile token rejected in Playwright headless",
        "body": ("The widget renders but submit returns 403. Running Playwright in Docker. "
                 "Looking for advice on the token and font fingerprint."),
        "updated_at": "2026-10-18T06:05:00Z",
    },
    {
        "category": "scraping",
        "repo": "dataforge/scraper",
        "number": 641,
        "stars": 2890,
        "title": "Scraping blocked by Cloudflare Turnstile after 20 pages",
        "body": ("Selenium in Docker gets 429 and a Turnstile challenge after 20 pages. "
                 "How to solve this without a proxy rotation storm?"),
        "updated_at": "2026-10-18T05:22:00Z",
    },
    {
        "category": "payments",
        "repo": "indie-saas/billing",
        "number": 209,
        "stars": 734,
        "title": "Stripe banned our SaaS account; looking for an alternative",
        "body": ("Chargebacks at 0.9%, cross-border volume grew, and Stripe asked for a reserve. "
                 "Need recommendations for a replacement with global payouts."),
        "updated_at": "2026-10-18T04:10:00Z",
    },
    {
        "category": "gpu",
        "repo": "ml-team/inference",
        "number": 95,
        "stars": 3120,
        "title": "RunPod H100 SXM too expensive; pods time out during model load",
        "body": ("CUDA OOM and timeout on community cloud at $2.99/hr. Recommend a cheaper GPU "
                 "provider or a PCIe setup?"),
        "updated_at": "2026-10-18T03:45:00Z",
    },
    {
        "category": "proxy",
        "repo": "notes/proxy-rotation",
        "number": 3,
        "stars": 12,
        "title": "Notes on proxy rotation",
        "body": "Archived notes about Cloudflare and header order.",
        "updated_at": "2026-10-17T20:00:00Z",
    },
    {
        "category": "proxy",
        "repo": "docs/cloudflare-status-codes",
        "number": 44,
        "stars": 8,
        "title": "Cloudflare 403 documentation",
        "body": "Archived vendor documentation for 403 responses.",
        "updated_at": "2026-10-17T19:00:00Z",
    },
)


def dry_run():
    seen = load_seen()
    accepted = []
    for fixture in FIXTURES:
        issue = {
            "issue_url": "https://github.com/" + fixture["repo"] + "/issues/" + str(fixture["number"]),
            "repo": fixture["repo"],
            "title": fixture["title"],
            "body": fixture["body"],
            "updated_at": fixture["updated_at"],
        }
        text = issue["title"] + "\n" + issue["body"]
        if not CATEGORIES[fixture["category"]]["gate_re"].search(issue["title"]):
            log("gate_reject", issue_url=issue["issue_url"], score=0, reason="category gate")
            continue
        score, evidence = score_issue(text, fixture["category"])
        if score < MIN_SCORE:
            log("gate_reject", issue_url=issue["issue_url"], score=score)
            continue
        record = make_record(fixture["category"], issue, fixture["stars"], score, evidence,
                             dry_run=True)
        if record["issue_url"] not in seen:
            append_record(record)
            seen.add(record["issue_url"])
        accepted.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
    categories = {record["category"] for record in accepted}
    assert categories == set(CATEGORIES), "dry run must cover all four categories"
    assert all(record["score"] >= MIN_SCORE for record in accepted), "gate must hold"
    assert len(accepted) == 6, "dry run must accept exactly the six qualifying fixtures"
    assert all(record["recommended_target"].endswith("?utm_source=gh_issue")
               for record in accepted), "every target needs the gh_issue UTM tag"
    log("dry_run_pass", categories=sorted(categories), accepted=len(accepted),
        rejected=len(FIXTURES) - len(accepted), min_score=MIN_SCORE,
        ledger=LEDGER_PATH, offline=True)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="score offline fixtures; no GitHub requests")
    parser.add_argument("--once", action="store_true",
                        help="one real public GitHub search round (default)")
    parser.add_argument("--limit", type=int, default=2,
                        help="maximum drafts per category in a live round (default: 2)")
    parser.add_argument("--per-page", type=int, default=10,
                        help="search results per keyword, 1-30 (default: 10)")
    args = parser.parse_args()
    if not 1 <= args.limit <= 10:
        parser.error("--limit must be between 1 and 10")
    if not 1 <= args.per_page <= 30:
        parser.error("--per-page must be between 1 and 30")
    if args.dry_run:
        return dry_run()
    return run_live(args.limit, args.per_page)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
