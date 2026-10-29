#!/usr/bin/env python3
"""Publish Track 6 Dev.to articles (09 and 10) to Dev.to via REST API.

Standard library only. Reads API key from DEVTO_API_KEY or ~/.secrets(密钥)/devto-api(Devto发文API).env.
Appends receipts to published_articles.jsonl.
"""

import argparse
import datetime
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
USER_AGENT = "kais-track6-publisher/1.0 (+https://proxy.mybskm.top/)"
ENV_FILE = Path.home() / ".secrets(密钥)" / "devto-api(Devto发文API).env"
MIN_WORDS = 800
SPACING_SECONDS = 15
MAX_ATTEMPTS = 6

ARTICLES = {
    "09": {
        "file": "09-heygen-vs-synthesia-elevenlabs.md",
        "title": "HeyGen vs Synthesia + ElevenLabs in 2026: AI Video Avatar & Dubbing Localization Unit Economics ($500/mo Production Audit)",
        "canonical_url": "https://gpu.mybskm.top/blog/heygen-vs-synthesia-elevenlabs.html",
        "series": "AI Media Economics",
        "tags": ["ai", "video", "python", "devops"],
        "description": "A commercial video studio costs $500 per localized 2-minute video. Modern AI video pipelines combine HeyGen custom 4K avatars, ElevenLabs low-latency voice cloning, and decentralized GPU rendering to slash unit costs by 91.4% while collapsing turnaround times from days to minutes.",
        "required_links": [
            "https://go.272738.xyz/heygen?src=devto_heygen_elevenlabs_benchmark",
            "https://go.272738.xyz/elevenlabs?src=devto_heygen_elevenlabs_benchmark",
            "https://go.272738.xyz/runpod?src=devto_heygen_elevenlabs_benchmark",
            "https://go.272738.xyz/vastai?src=devto_heygen_elevenlabs_benchmark",
        ],
    },
    "10": {
        "file": "10-morelogin-vs-adspower-packetstream.md",
        "title": "MoreLogin Cloud Phone vs AdsPower & PacketStream $1/GB Residential Proxy Stack: 100-Account Matrix TCO Breakdown",
        "canonical_url": "https://proxy.mybskm.top/blog/morelogin-vs-adspower-packetstream-tco.html",
        "series": "Anti-Detect & Account Matrix Economics",
        "tags": ["devops", "automation", "python", "webscraping"],
        "description": "Operating a 100-account mobile and browser matrix with physical Android phones costs $2,800/mo in capital depreciation and SIM maintenance. Replacing hardware with MoreLogin ARM cloud phones, AdsPower browser profiles, and PacketStream $1.00/GB residential proxies slashes TCO by 88.6% while eliminating Canvas/WebGL fingerprint bans.",
        "required_links": [
            "https://go.272738.xyz/morelogin?src=devto_morelogin_adspower_matrix",
            "https://go.272738.xyz/adspower?src=devto_morelogin_adspower_matrix",
            "https://go.272738.xyz/packetstream?src=devto_morelogin_adspower_matrix",
            "https://go.272738.xyz/9proxy?src=devto_morelogin_adspower_matrix",
            "https://go.272738.xyz/webshare?src=devto_morelogin_adspower_matrix",
            "https://go.272738.xyz/voluum?src=devto_morelogin_adspower_matrix",
        ],
    },
}

def load_api_key():
    key = os.environ.get("DEVTO_API_KEY")
    if key:
        return key.strip()
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("DEVTO_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None

def strip_frontmatter(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text.strip()

def load_document(key):
    spec = ARTICLES[key]
    path = ARTICLES_DIR / spec["file"]
    assert path.exists(), f"Missing article file: {path}"
    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    word_count = len(body.split())
    assert word_count >= MIN_WORDS, f"Word count {word_count} < {MIN_WORDS}"
    for link in spec["required_links"]:
        assert link in body, f"Missing required link {link} in {spec['file']}"
    return {"key": key, "spec": spec, "body": body, "word_count": word_count}

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

def http_json(url, payload=None, api_key_value=None, method="GET", timeout=45):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if api_key_value:
        headers["api-key"] = api_key_value
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8")

def publish(doc, key, force=False):
    spec = doc["spec"]
    receipts = read_ledger()
    if not force and any(
        item.get("canonical_url") == spec["canonical_url"]
        and item.get("status") == "published"
        for item in receipts
    ):
        print(f"Skip (already published): {spec['canonical_url']}")
        return None

    payload = {
        "article": {
            "title": spec["title"],
            "published": True,
            "body_markdown": doc["body"],
            "tags": spec["tags"],
            "canonical_url": spec["canonical_url"],
            "series": spec["series"],
            "description": spec["description"],
        }
    }

    attempt = 0
    while True:
        attempt += 1
        try:
            status, raw = http_json(API_URL, payload=payload, api_key_value=key, method="POST")
            data = json.loads(raw)
            break
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", "replace")[:300]
            if err.code == 429:
                delay = 35
            else:
                delay = 10 * attempt
            if attempt >= MAX_ATTEMPTS:
                raise SystemExit(f"POST failed: HTTP {err.code} {err.reason} {detail}")
            print(f"  HTTP {err.code} on attempt {attempt}, retrying in {delay}s...")
            time.sleep(delay)

    receipt = {
        "posted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "published",
        "http_status": status,
        "id": data.get("id"),
        "url": data.get("url"),
        "slug": data.get("slug"),
        "title": spec["title"],
        "canonical_url": spec["canonical_url"],
        "series": spec["series"],
        "tags": spec["tags"],
        "word_count": doc["word_count"],
    }
    append_receipt(receipt)
    print(f"Successfully published: {data.get('url')}")
    return receipt

def main():
    parser = argparse.ArgumentParser(description="Track 6 Dev.to Publisher")
    parser.add_argument("--dry-run", action="store_true", help="Validate without posting")
    parser.add_argument("--post", action="store_true", help="Post to live Dev.to API")
    parser.add_argument("--force", action="store_true", help="Force republish")
    args = parser.parse_args()

    docs = [load_document(k) for k in sorted(ARTICLES.keys())]
    for d in docs:
        print(f"Loaded: [{d['key']}] {d['spec']['title']} ({d['word_count']} words, canonical: {d['spec']['canonical_url']})")

    if args.dry_run:
        print("Dry run validation PASSED for all articles.")
        return

    if not args.post:
        print("Use --dry-run to validate or --post to publish.")
        return

    api_key = load_api_key()
    assert api_key, "Could not find DEVTO_API_KEY"

    for i, d in enumerate(docs):
        if i > 0:
            print(f"Waiting {SPACING_SECONDS}s between publishes...")
            time.sleep(SPACING_SECONDS)
        publish(d, api_key, force=args.force)

if __name__ == "__main__":
    main()
