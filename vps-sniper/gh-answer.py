#!/usr/bin/env python3
"""Turn public GitHub issue reports into scored, four-part technical replies.

    python3 gh-answer.py --dry-run                 # offline fixtures, no network
    python3 gh-answer.py --once                    # draft only, one live round
    python3 gh-answer.py --once --post --limit 3   # post up to 3 real replies

For a qualifying issue (score >= 3) DeepSeek writes an issue-specific four-part
reply. The model name is read from DEEPSEEK_MODEL and defaults to the permanent
alias `deepseek-chat`. DeepSeek keeps that alias pointed at its latest
production chat model (V3, V3.5, V4, ...), so backend upgrades need no code
change; set DEEPSEEK_MODEL only when an explicit snapshot must be pinned. Every
AI call has a hard 6 second timeout and falls back to the curated expert
templates on a missing key, timeout, HTTP error or malformed answer, so a bad
network never blocks a run.

`--post` writes real comments through the official GitHub REST API. Safety
gates: repository stars >= 20, issue open and updated within 21 days, never a
600me-owned repository, never an issue already recorded with posted: true,
one comment per repository per 30-day cooldown, at most --limit posts per run
(default 2, hard max 5), and a random 3-7 second pause between posts.
Successful receipts (comment_url / comment_id / post_time) are appended
atomically to outreach_gh.jsonl beside this file.

Outreach links point at the owned research sites (with utm_source=gh_issue),
never at a short-link relay. `build_draft`, `disclosure`, the DeepSeek prompt
and every ledger record read the same per-category `target_url`.

`--dry-run` is fully offline: it scores local fixtures across all four
categories, never calls GitHub or DeepSeek, and never writes the ledger.
Only the Python standard library is used; no database or message queue.
"""

import argparse
import datetime
import json
import os
import random
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
USER_AGENT = "kais-proxy-benchmark-gh-answer/1.2 (+https://proxy.mybskm.top/)"
MAX_BYTES = 2 * 1024 * 1024
MIN_SCORE = 3
MIN_STARS = 20
MAX_ISSUE_AGE_DAYS = 21
REPO_COOLDOWN_DAYS = 30
MAX_POSTS = 5
POST_SLEEP_MIN = 3.0
POST_SLEEP_MAX = 7.0
# Permanent alias pointer: DeepSeek resolves `deepseek-chat` to the current
# production chat model. DEEPSEEK_MODEL is the documented escape hatch for
# pinning an explicit snapshot without touching this file.
DEEPSEEK_API_URL = os.environ.get(
    "DEEPSEEK_CHAT_URL", "https://api.deepseek.com/chat/completions")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_TIMEOUT = 6
DEEPSEEK_SYSTEM_PROMPT = (
    "You are a senior production engineer replying to a public GitHub issue. "
    "Write a concise, technically specific Markdown answer with exactly four parts:\n"
    "1. **Root cause.** Explain the most likely cause using the issue's actual error "
    "text, status codes, versions and environment. Do not invent logs or facts.\n"
    "2. **Verify it with one command.** Give one copy-paste command that isolates the "
    "failure, followed by one sentence explaining what the result means.\n"
    "3. **What to change.** Give concrete fixes, configuration or code changes, "
    "ordered by expected impact.\n"
    "4. A final line starting with `Disclosure:` stating that you maintain the linked "
    "open-source benchmark, including its URL.\n"
    "No greeting, no sales pitch, no 'check out my tool'. Stay under 450 words. "
    "Return only the Markdown reply."
)

INTENT_RE = re.compile(
    r"(?:\?|how (?:do|can|should|to)|need (?:help|advice|recommendations?)|"
    r"looking for|recommend|suggest|alternatives?|workaround|anyone|"
    r"is there|best way|help me|advice|steps to reproduce|expected behavior|"
    r"actual behavior|traceback|stack\s*trace|```)",
    re.I,
)

NEGATIVE_TITLE_RE = re.compile(
    r"\b(?:roadmap|rfc|epic|tracking|digest|changelog|release\s+notes|"
    r"bump\b|deps\b|translation|weekly|todo\s+list)\b",
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
        "keywords": ("cloudflare 403 proxy", "residential proxy 403",
                     "cf_clearance 403", "curl_cffi 403"),
        "target_url": "https://scrape.mybskm.top/blog/proxy-cost-audit.html?utm_source=gh_issue",
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
        "keywords": ("turnstile playwright", "cloudflare 403 playwright",
                     "scraping blocked cloudflare", "puppeteer turnstile"),
        "target_url": "https://scrape.mybskm.top/blog/403-tax.html?utm_source=gh_issue",
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
        "keywords": ("stripe banned", "stripe account closed",
                     "stripe alternative saas", "paddle vs stripe"),
        "target_url": "https://pay.mybskm.top/?utm_source=gh_issue",
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
        "keywords": ("runpod expensive", "h100 gpu cloud",
                     "vllm cuda out of memory", "runpod vs vast"),
        "target_url": "https://gpu.mybskm.top/calculator/?utm_source=gh_issue",
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
        + disclosure(category)
    )


def disclosure(category):
    """Disclosure points at the owned research page, never a short-link relay."""
    spec = CATEGORIES[category]
    target = spec["target_url"]
    if category == "proxy":
        return ("Disclosure: I maintain the open-source proxy cost CLI "
                "(https://github.com/600me/check-proxy-tax) and benchmark data: "
                + target)
    if category == "scraping":
        return ("Disclosure: I maintain the open-source scraping API benchmark "
                "(https://github.com/600me/awesome-web-scraping-apis-benchmark) "
                "and benchmark data: " + target)
    return ("Disclosure: I maintain the open-source benchmark at github.com/"
            + spec["repo"] + ". Measured success rate, latency, HTTP status and "
            "IP/ASN data: " + target)


def canonical_disclosure(content, category):
    """Keep one canonical disclosure line, even when the model writes its own."""
    kept = [line for line in content.splitlines()
            if not re.match(r"^\s*\**\s*disclosure\s*:", line, re.I)]
    body = "\n".join(kept).rstrip()
    return (body + "\n\n" if body else "") + disclosure(category)


def deepseek_prompt(category, issue, evidence):
    spec = CATEGORIES[category]
    target = spec["target_url"]
    signals = ", ".join(dict.fromkeys(
        evidence.get("error", [])[:3] + evidence.get("vendor", [])[:3]
        + evidence.get("intent", [])[:2])) or "none"
    body = (issue.get("body") or "").strip()
    if len(body) > 6000:
        body = body[:6000] + "\n[body truncated]"
    return (
        "Category: " + category + "\n"
        "Repository: " + issue["repo"] + "\n"
        "Issue title: " + issue["title"] + "\n"
        "Issue body:\n" + (body or "(empty)") + "\n\n"
        "Detected signals: " + signals + "\n"
        "Reference benchmark (use this exact disclosure link): " + target + "\n"
        "Category background you may use, but tailor it to this issue: "
        + spec["root_cause"] + "\n"
        "Usual fix direction: " + spec["fix"] + "\n\n"
        "Answer this specific report. If the body lacks a key detail, state the "
        "assumption instead of inventing it."
    )


def deepseek_draft(category, issue, evidence):
    """Return an issue-specific four-part reply, or None to trigger fallback."""
    api_key = (os.environ.get("DEEPSEEK_API_KEY") or "").strip()
    if not api_key:
        log("ai_skip", reason="DEEPSEEK_API_KEY not set")
        return None
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": DEEPSEEK_SYSTEM_PROMPT},
            {"role": "user", "content": deepseek_prompt(category, issue, evidence)},
        ],
        "temperature": 0.3,
        "max_tokens": 700,
        "stream": False,
    }
    request = urllib.request.Request(
        DEEPSEEK_API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + api_key,
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=DEEPSEEK_TIMEOUT) as response:
            raw = response.read(MAX_BYTES)
    except urllib.error.HTTPError as error:
        detail = ""
        try:
            detail = error.read(300).decode("utf-8", "replace")
        except Exception:
            pass
        log("ai_error", status=error.code, model=DEEPSEEK_MODEL, detail=detail[:200])
        return None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        log("ai_error", model=DEEPSEEK_MODEL, detail=str(error)[:200])
        return None
    try:
        data = json.loads(raw)
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as error:
        log("ai_error", model=DEEPSEEK_MODEL,
            detail="bad response: " + str(error)[:160])
        return None
    if not isinstance(content, str):
        log("ai_reject", model=DEEPSEEK_MODEL, reason="non-text content")
        return None
    content = content.strip()
    lowered = content.lower()
    if "go.272738.xyz" in lowered:
        log("ai_reject", model=DEEPSEEK_MODEL, reason="forbidden short link")
        return None
    required = ("root cause", "verify", "what to change")
    if len(content) < 200 or not all(marker in lowered for marker in required):
        log("ai_reject", model=DEEPSEEK_MODEL, chars=len(content),
            reason="missing four-part structure")
        return None
    content = canonical_disclosure(content, category)
    log("ai_draft", model=DEEPSEEK_MODEL, category=category,
        chars=len(content), issue_url=issue["issue_url"])
    return content


def draft_for(issue):
    """AI first; the curated template is the zero-interruption fallback."""
    response = deepseek_draft(issue["category"], issue, issue["evidence"])
    if response:
        return response, "deepseek"
    return build_draft(issue["category"], issue["evidence"]), "template"


def iter_records(path=LEDGER_PATH):
    try:
        with open(path, encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if isinstance(record, dict):
                    yield record
    except FileNotFoundError:
        return


def load_seen(path=LEDGER_PATH):
    return {record["issue_url"] for record in iter_records(path)
            if isinstance(record.get("issue_url"), str)}


def load_posted(path=LEDGER_PATH):
    """Only a recorded receipt blocks a second comment; drafts do not."""
    posted = set()
    for record in iter_records(path):
        issue_url = record.get("issue_url")
        if not isinstance(issue_url, str):
            continue
        if record.get("posted") is True or (
                record.get("comment_url") and record.get("comment_id")):
            posted.add(issue_url)
    return posted


def load_recent_posted_repos(path=LEDGER_PATH, days=REPO_COOLDOWN_DAYS):
    """Repos that already received a comment inside the cooldown window."""
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    cooled = set()
    for record in iter_records(path):
        repo = record.get("repo")
        if not isinstance(repo, str) or not repo:
            continue
        if not (record.get("posted") is True or record.get("comment_url")):
            continue
        stamp = record.get("post_time") or record.get("time")
        if not isinstance(stamp, str):
            continue
        try:
            posted_at = datetime.datetime.strptime(
                stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            continue
        if posted_at >= cutoff:
            cooled.add(repo)
    return cooled


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


def make_record(category, issue, stars, score, evidence, dry_run,
                response=None, source="template"):
    target = CATEGORIES[category]["target_url"]
    return {
        "time": now(),
        "issue_url": issue["issue_url"],
        "repo": issue["repo"],
        "stars": stars,
        "category": category,
        "score": score,
        "signals": evidence,
        "draft_source": source,
        "draft_response": response if response else build_draft(category, evidence),
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


def github_post(url, payload):
    """POST JSON to GitHub. Returns the parsed receipt, or None on any error."""
    token = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "").strip()
    if not token:
        log("post_error", reason="GITHUB_TOKEN/GH_TOKEN not set")
        return None
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read(MAX_BYTES)
            status = getattr(response, "status", 0)
    except urllib.error.HTTPError as error:
        detail = ""
        try:
            detail = error.read(300).decode("utf-8", "replace")
        except Exception:
            pass
        log("post_error", status=error.code, url=url, detail=detail[:200])
        return None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        log("post_error", url=url, detail=str(error)[:200])
        return None
    if status and not 200 <= status < 300:
        log("post_error", status=status, url=url)
        return None
    try:
        data = json.loads(raw)
    except (ValueError, TypeError) as error:
        log("post_error", url=url, detail="invalid JSON: " + str(error)[:120])
        return None
    if not isinstance(data, dict) or not data.get("html_url") or data.get("id") is None:
        log("post_error", url=url, detail="response missing html_url/id")
        return None
    return data


def post_comment(repo, number, body):
    url = (REPO_URL + urllib.parse.quote(repo, safe="/")
           + "/issues/" + str(number) + "/comments")
    return github_post(url, {"body": body})


def search_issues(keyword, per_page=15):
    cutoff = time.strftime("%Y-%m-%d",
                           time.gmtime(time.time() - MAX_ISSUE_AGE_DAYS * 86400))
    query = (keyword + " in:title,body is:issue is:open comments:<8 updated:>="
             + cutoff)
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
    number = item.get("number")
    if not repo or not issue_url or not isinstance(number, int):
        return None
    return {
        "issue_url": issue_url,
        "repo": repo,
        "number": number,
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


def fresh_enough(updated_at):
    try:
        updated = datetime.datetime.strptime(
            updated_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except (TypeError, ValueError):
        return False
    age = (datetime.datetime.now(datetime.timezone.utc) - updated).total_seconds()
    return 0 <= age <= MAX_ISSUE_AGE_DAYS * 86400


def collect_candidates(per_page):
    """One live search pass over all four categories, deduplicated by issue URL."""
    candidates = {}
    searched = 0
    first_call = True
    for category, spec in CATEGORIES.items():
        for keyword in spec["keywords"]:
            # GitHub Search has a strict secondary rate limit. Space the 16
            # category/keyword queries instead of firing them back-to-back.
            if not first_call:
                time.sleep(1.2)
            first_call = False
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
                if not issue:
                    continue
                if issue["repo"].split("/", 1)[0].lower() == "600me":
                    continue
                if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", issue["repo"]):
                    continue
                if NEGATIVE_TITLE_RE.search(issue["title"]):
                    continue
                text = issue["title"] + "\n" + issue["body"]
                # The short title only has to identify the surface (vendor or
                # error). The full title+body must satisfy the two-dimension
                # category gate, so real stack traces and repro steps qualify.
                if not (spec["vendor_re"].search(issue["title"])
                        or spec["error_re"].search(issue["title"])):
                    continue
                if not spec["gate_re"].search(text):
                    continue
                score, evidence = score_issue(text, category)
                if score < MIN_SCORE:
                    continue
                issue["category"] = category
                issue["score"] = score
                issue["evidence"] = evidence
                previous = candidates.get(issue["issue_url"])
                if previous is None or score > previous["score"]:
                    candidates[issue["issue_url"]] = issue
    return list(candidates.values()), searched


def run_draft_round(candidates, searched, limit):
    """Draft-only round: up to --limit drafts per category, never posts."""
    seen = load_seen()
    cache = {}
    emitted = 0
    for category in CATEGORIES:
        ranked = sorted((issue for issue in candidates if issue["category"] == category),
                        key=lambda value: (value["score"], value["updated_at"]),
                        reverse=True)
        selected = 0
        for issue in ranked:
            if selected >= limit:
                break
            if issue["issue_url"] in seen:
                continue
            stars = fetch_stars(issue["repo"], cache)
            response, source = draft_for(issue)
            record = make_record(category, issue, stars, issue["score"],
                                 issue["evidence"], dry_run=False,
                                 response=response, source=source)
            append_record(record)
            seen.add(record["issue_url"])
            print(json.dumps(record, ensure_ascii=False), flush=True)
            selected += 1
            emitted += 1
    log("round", searched=searched, candidates=len(candidates), emitted=emitted,
        limit=limit, ledger=LEDGER_PATH)
    return 0 if searched else 1


def run_post_round(candidates, searched, limit):
    """Post at most `limit` real comments, with every anti-abuse gate applied."""
    posted = load_posted()
    cooled_repos = load_recent_posted_repos()
    posted_repos = set()
    cache = {}
    ranked = sorted(candidates,
                    key=lambda value: (value["score"], value["updated_at"]),
                    reverse=True)
    attempts = 0
    published = 0
    for index, issue in enumerate(ranked):
        if attempts >= limit:
            break
        if issue["issue_url"] in posted:
            log("post_skip", issue_url=issue["issue_url"], reason="already posted")
            continue
        if issue["repo"] in cooled_repos or issue["repo"] in posted_repos:
            log("post_skip", issue_url=issue["issue_url"], reason="repo_cooldown")
            continue
        if not fresh_enough(issue["updated_at"]):
            log("post_skip", issue_url=issue["issue_url"], reason="stale")
            continue
        stars = fetch_stars(issue["repo"], cache)
        if not isinstance(stars, int) or stars < MIN_STARS:
            log("post_skip", issue_url=issue["issue_url"], reason="stars", stars=stars)
            continue
        response, source = draft_for(issue)
        attempts += 1
        result = post_comment(issue["repo"], issue["number"], response)
        if result:
            record = make_record(issue["category"], issue, stars, issue["score"],
                                 issue["evidence"], dry_run=False,
                                 response=response, source=source)
            record.update({
                "posted": True,
                "comment_url": result["html_url"],
                "comment_id": result["id"],
                "post_time": now(),
            })
            append_record(record)
            posted.add(issue["issue_url"])
            posted_repos.add(issue["repo"])
            print(json.dumps(record, ensure_ascii=False), flush=True)
            published += 1
        else:
            log("post_failed", issue_url=issue["issue_url"], repo=issue["repo"])
        if attempts < limit and index + 1 < len(ranked):
            delay = random.uniform(POST_SLEEP_MIN, POST_SLEEP_MAX)
            log("post_pause", seconds=round(delay, 2))
            time.sleep(delay)
    log("post_round", searched=searched, candidates=len(candidates),
        attempts=attempts, published=published, limit=limit, ledger=LEDGER_PATH)
    return 0 if searched else 1


def run_live(limit, per_page, post=False):
    candidates, searched = collect_candidates(per_page)
    if post:
        return run_post_round(candidates, searched, limit)
    return run_draft_round(candidates, searched, limit)


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
    """Offline acceptance: no HTTP, no ledger writes, all four categories."""
    accepted = []
    for fixture in FIXTURES:
        issue = {
            "issue_url": "https://github.com/" + fixture["repo"] + "/issues/" + str(fixture["number"]),
            "repo": fixture["repo"],
            "number": fixture["number"],
            "title": fixture["title"],
            "body": fixture["body"],
            "updated_at": fixture["updated_at"],
        }
        text = issue["title"] + "\n" + issue["body"]
        spec = CATEGORIES[fixture["category"]]
        if NEGATIVE_TITLE_RE.search(issue["title"]):
            log("gate_reject", issue_url=issue["issue_url"], score=0,
                reason="negative title")
            continue
        if not (spec["vendor_re"].search(issue["title"])
                or spec["error_re"].search(issue["title"])):
            log("gate_reject", issue_url=issue["issue_url"], score=0,
                reason="title vendor/error")
            continue
        if not spec["gate_re"].search(text):
            log("gate_reject", issue_url=issue["issue_url"], score=0,
                reason="category gate")
            continue
        score, evidence = score_issue(text, fixture["category"])
        if score < MIN_SCORE:
            log("gate_reject", issue_url=issue["issue_url"], score=score)
            continue
        record = make_record(fixture["category"], issue, fixture["stars"], score, evidence,
                             dry_run=True)
        accepted.append(record)
        print(json.dumps(record, ensure_ascii=False), flush=True)
    categories = {record["category"] for record in accepted}
    assert categories == set(CATEGORIES), "dry run must cover all four categories"
    assert all(record["score"] >= MIN_SCORE for record in accepted), "gate must hold"
    assert all(record["draft_source"] == "template" for record in accepted), \
        "dry run must not call DeepSeek"
    assert len(accepted) == 6, "dry run must accept exactly the six qualifying fixtures"
    assert all(record["recommended_target"].endswith("?utm_source=gh_issue")
               for record in accepted), "every target needs the gh_issue UTM tag"
    assert all(record["recommended_target"] == CATEGORIES[record["category"]]["target_url"]
               for record in accepted), "record target must match the category target_url"
    assert all("go.272738.xyz" not in record["draft_response"]
               for record in accepted), "public replies must never contain a short link"
    log("dry_run_pass", categories=sorted(categories), accepted=len(accepted),
        rejected=len(FIXTURES) - len(accepted), min_score=MIN_SCORE,
        offline=True, network_calls=0, ledger_writes=0)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="score offline fixtures; no network and no ledger writes")
    parser.add_argument("--once", action="store_true",
                        help="one real public GitHub search round (default)")
    parser.add_argument("--post", action="store_true",
                        help="post real comments through the GitHub REST API")
    parser.add_argument("--limit", type=int, default=2,
                        help="maximum drafts per category, or posts per run (default: 2, max: 5)")
    parser.add_argument("--per-page", type=int, default=15,
                        help="search results per keyword, 1-30 (default: 15)")
    args = parser.parse_args()
    if not 1 <= args.limit <= MAX_POSTS:
        parser.error("--limit must be between 1 and " + str(MAX_POSTS))
    if not 1 <= args.per_page <= 30:
        parser.error("--per-page must be between 1 and 30")
    if args.dry_run:
        if args.post:
            log("dry_run_post_ignored", reason="offline mode never posts")
        return dry_run()
    if args.post and not (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")):
        parser.error("--post requires GITHUB_TOKEN or GH_TOKEN")
    return run_live(args.limit, args.per_page, args.post)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
