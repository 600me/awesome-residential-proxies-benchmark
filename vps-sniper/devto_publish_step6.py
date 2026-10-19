#!/usr/bin/env python3
"""Step 6A Dev.to publisher: sync three canonical-bound articles.

    python3 devto_publish_step6.py --dry-run
    python3 devto_publish_step6.py --post            # 05, 06, 07 in order
    python3 devto_publish_step6.py --post --only 06

Standard library only.  The API key is read from ``DEVTO_API_KEY`` or from
``~/.secrets(密钥)/devto-api(Devto发文API).env`` and is never printed, logged or
written to the ledger.

Retry policy: HTTP 429 honours ``Retry-After`` (fallback 35 s); 5xx retries with
linear backoff.  Articles are spaced 15 s apart to stay inside the write rate
limit.  Each success appends one receipt to ``published_articles.jsonl`` beside
this file, and then verifies that the live Dev.to page advertises the canonical
URL of the independent site.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "published_articles.jsonl"
ARTICLES_DIR = HERE / "articles"
API_URL = "https://dev.to/api/articles"
USER_AGENT = "kais-step6-publisher/1.0 (+https://pay.mybskm.top/)"
ENV_FILE = Path.home() / ".secrets(密钥)" / "devto-api(Devto发文API).env"
MIN_WORDS = 1200
SPACING_SECONDS = 15
MAX_ATTEMPTS = 6

ARTICLES = {
    "05": {
        "file": "05-residential-proxy-sticky-session-guide.md",
        "title": "Why Rotating Residential Proxies Still Get 403s: Sticky Session TTL, JA3 Fingerprints and ASN Economics (2026)",
        "canonical_url": "https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html",
        "series": "Anti-Bot Economics",
        "tags": ["webscraping", "python", "devops", "security"],
        "description": "Residential bandwidth is not the bottleneck. ASN reputation, session binding and the JA3/JA4 fingerprint are three separate failure layers, and the re-run tax is the part of the bill nobody quotes. Three curl diagnostics and a drop-rate model.",
        "required_links": [
            "https://proxy.mybskm.top/calculator/",
            "https://github.com/600me/check-proxy-tax",
            "https://go.272738.xyz/smartproxy?src=devto_sticky_guide",
        ],
    },
    "06": {
        "file": "06-firstbase-vs-stripe-atlas-vs-doola.md",
        "title": "Firstbase vs Stripe Atlas vs Doola (2026): True 3-Year US LLC, Registered Agent & IRS Form 5472 Cost for Non-US Founders",
        "canonical_url": "https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html",
        "series": "Payment Economics",
        "tags": ["saas", "indiehackers", "stripe", "startup"],
        "description": "Formation fees are $399, $500 and $297. Three years of holding the company cost $876, $1,600 and $6,177 once Wyoming vs Delaware state fees, agent renewals and the $25,000 Form 5472 penalty are counted.",
        "required_links": [
            "https://pay.mybskm.top/?mrr=8000&aov=40&intl=70",
            "https://go.272738.xyz/firstbase?src=devto_firstbase_atlas",
            "https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html",
        ],
    },
    "07": {
        "file": "07-runpod-vs-vastai-h100-a100.md",
        "title": "RunPod vs Vast.ai (2026): Real H100 & A100 Effective Cost After Cold-Start, NVMe Storage & Bandwidth Billing",
        "canonical_url": "https://gpu.mybskm.top/blog/runpod-vs-vastai-h100-a100.html",
        "series": "GPU Cloud Cost Notes",
        "tags": ["gpu", "cloud", "machinelearning", "devops"],
        "description": "Vast.ai lists H100 capacity about 25% below RunPod. After egress billing at $0.01-$0.08/GB, a 40-minute cold start and a 15% failover reserve, a two-hour test is 63% more expensive on Vast while a 72-hour preemptible fine-tune is still 52.8% cheaper.",
        "required_links": [
            "https://gpu.mybskm.top/calculator/",
            "https://huggingface.co/spaces/600me/llm-gpu-cost-calculator",
            "https://go.272738.xyz/runpod?src=devto_runpod_vast",
            "https://go.272738.xyz/vastai?src=devto_runpod_vast",
            "https://gpu.mybskm.top/blog/runpod-vs-vastai-h100-a100.html",
        ],
    },
}

ORDER = ["05", "06", "07"]


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def read_body(spec):
    path = ARTICLES_DIR / spec["file"]
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):  # tolerate frontmatter written by earlier runs
        end = text.find("\n---\n", 4)
        if end > 0:
            text = text[end + 5:]
    return text.strip()


def api_key():
    key = os.environ.get("DEVTO_API_KEY", "").strip()
    if key:
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("DEVTO_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("DEVTO_API_KEY not found in the environment or in %s" % ENV_FILE)


def load_document(key, spec):
    body = read_body(spec)
    words = word_count(body)
    if words < MIN_WORDS:
        raise SystemExit("%s: body is only %d words (minimum %d)"
                         % (spec["file"], words, MIN_WORDS))
    for link in spec["required_links"]:
        if link not in body:
            raise SystemExit("%s: required link missing: %s"
                             % (spec["file"], link))
    if not body:
        raise SystemExit("%s: empty article body" % spec["file"])
    return {"key": key, "spec": spec, "body": body, "words": words}


def read_ledger():
    if not LEDGER.exists():
        return []
    receipts = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            receipts.append(json.loads(line))
    return receipts


def append_receipt(receipt):
    with LEDGER.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(receipt, ensure_ascii=False) + "\n")


def http_json(url, payload=None, api_key_value=None, headers=None,
              method="GET", timeout=45):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request_headers = {"Accept": "application/json",
                       "User-Agent": USER_AGENT}
    if headers:
        request_headers.update(headers)
    if api_key_value:
        request_headers["api-key"] = api_key_value
    if data is not None:
        request_headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=request_headers,
                                     method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8")


def retry_delay(error, attempt):
    """Seconds to wait after a failed POST attempt."""
    if isinstance(error, urllib.error.HTTPError):
        retry_after = error.headers.get("Retry-After") if error.headers else None
        if retry_after:
            try:
                return max(int(float(retry_after)), 5)
            except ValueError:
                pass
        if error.code == 429:
            return 35
        if 500 <= error.code < 600:
            return 20 * attempt
    return None


def publish(document, key, force=False):
    spec = document["spec"]
    receipts = read_ledger()
    if not force and any(
        item.get("canonical_url") == spec["canonical_url"]
        and item.get("status") == "published"
        for item in receipts
    ):
        print("skip (already published): %s" % spec["canonical_url"])
        return None

    payload = {"article": {
        "title": spec["title"],
        "published": True,
        "body_markdown": document["body"],
        "tags": spec["tags"],
        "canonical_url": spec["canonical_url"],
        "series": spec["series"],
        "description": spec["description"],
    }}

    attempt = 0
    while True:
        attempt += 1
        try:
            status, raw = http_json(API_URL, payload=payload,
                                    api_key_value=key, method="POST")
            data = json.loads(raw)
            break
        except urllib.error.HTTPError as error:  # noqa: PERF203
            detail = error.read().decode("utf-8", "replace")[:300]
            delay = retry_delay(error, attempt)
            if delay is None or attempt >= MAX_ATTEMPTS:
                raise SystemExit("POST failed: HTTP %s %s %s"
                                 % (error.code, error.reason, detail))
            print("  HTTP %s on attempt %d, retrying in %ds"
                  % (error.code, attempt, delay))
            time.sleep(delay)

    if status not in (200, 201):
        raise SystemExit("unexpected Dev.to status: %s" % status)

    canonical_status = verify_canonical(data.get("url"), spec["canonical_url"])
    receipt = {
        "posted_at": now(),
        "status": "published",
        "http_status": status,
        "id": data.get("id"),
        "url": data.get("url"),
        "slug": data.get("slug"),
        "title": spec["title"],
        "canonical_url": spec["canonical_url"],
        "series": spec["series"],
        "tags": spec["tags"],
        "word_count": document["words"],
        "canonical_synced_at": now(),
        "canonical_http_status": canonical_status,
    }
    append_receipt(receipt)
    print("  published %s (HTTP %s, canonical %s)"
          % (data.get("url"), status, canonical_status))
    return receipt


def verify_canonical(devto_url, expected, attempts=6, delay=20):
    """Fetch the live Dev.to page and confirm the canonical link matches.

    Dev.to renders the canonical tag a short while after the article is
    accepted, so this polls instead of failing on the first miss.
    """
    if not devto_url:
        return None
    for attempt in range(attempts):
        try:
            _, html = http_json(devto_url, headers={"Accept": "text/html"})
        except Exception:  # noqa: BLE001
            time.sleep(delay)
            continue
        links = re.findall(r'<link[^>]+rel="canonical"[^>]+>', html)
        for link in links:
            match = re.search(r'href="([^"]+)"', link)
            if match and match.group(1).rstrip("/") == expected.rstrip("/"):
                return 200
        if attempt + 1 < attempts:
            time.sleep(delay)
    return 0


def rewrite_ledger(entries):
    """Rewrite the ledger in place, preserving order and formatting."""
    with LEDGER.open("w", encoding="utf-8") as stream:
        for entry in entries:
            stream.write(json.dumps(entry, ensure_ascii=False) + "\n")


def verify_ledger(keys):
    """Re-check Dev.to canonicals and repair stale verification fields."""
    entries = read_ledger()
    canonicals = {ARTICLES[key]["canonical_url"] for key in keys}
    changed = 0
    for entry in entries:
        if entry.get("canonical_url") not in canonicals:
            continue
        status = verify_canonical(entry.get("url"), entry["canonical_url"])
        print("%s -> canonical HTTP %s" % (entry.get("url"), status))
        if status == 200 and entry.get("canonical_http_status") != 200:
            entry["canonical_http_status"] = 200
            entry["canonical_synced_at"] = now()
            changed += 1
    if changed:
        rewrite_ledger(entries)
    print("ledger entries repaired: %d" % changed)
    return 0


def dry_run():
    print("dry run: %d article(s), ledger=%s" % (len(ORDER), LEDGER))
    for key in ORDER:
        document = load_document(key, ARTICLES[key])
        spec = document["spec"]
        print("- %s %s" % (key, spec["file"]))
        print("    title    : %s" % spec["title"])
        print("    canonical: %s" % spec["canonical_url"])
        print("    tags     : %s" % ", ".join(spec["tags"]))
        print("    series   : %s" % spec["series"])
        print("    words    : %d" % document["words"])
        for link in spec["required_links"]:
            print("    link     : %s (%d occurrences)"
                  % (link, document["body"].count(link)))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--post", action="store_true",
                        help="publish to Dev.to (default is a dry run)")
    parser.add_argument("--only", action="append", default=None,
                        help="publish only this article key (repeatable)")
    parser.add_argument("--force", action="store_true",
                        help="repost even when the canonical URL is in the ledger")
    parser.add_argument("--dry-run", action="store_true",
                        help="validate locally without network access")
    parser.add_argument("--verify", action="store_true",
                        help="re-check uploaded canonicals and repair the ledger")
    args = parser.parse_args(argv)

    if args.verify:
        return verify_ledger(args.only or ORDER)

    if not args.post or args.dry_run:
        return dry_run()

    keys = args.only or ORDER
    for key in keys:
        if key not in ARTICLES:
            raise SystemExit("unknown article key: %s" % key)
    key = api_key()
    print("publishing: %s" % ", ".join(keys))
    for index, article_key in enumerate(keys):
        if index:
            print("  waiting %ds before the next POST" % SPACING_SECONDS)
            time.sleep(SPACING_SECONDS)
        document = load_document(article_key, ARTICLES[article_key])
        publish(document, key, force=args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
