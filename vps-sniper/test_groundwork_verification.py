#!/usr/bin/env python3
"""Objective acceptance for the step-1 groundwork directive.

Checks, with no vendor SDKs and no secrets in this file:

1. Both live article pages answer HTTP/2 200.
2. Each page carries a self-referencing ``rel="canonical"``.
3. Each page exposes a parseable schema.org ``Article`` JSON-LD block with
   headline, description, author, publisher, datePublished and dateModified.
4. Each Dev.to public page source points its canonical at the site article.
5. Every CTA in the two pages returns a 302 from the affiliate relay and the
   request URI, including the ``src=`` attribution parameter, lands in
   ``/var/log/nginx/affiliate_relay.log``.
6. The local and remote ``published_articles.jsonl`` ledgers agree byte for
   byte and record the new canonical URLs.
7. Both live dashboards link to their new research page.

Run: python3 test_groundwork_verification.py
Exit code 0 means every assertion passed.
"""

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
LOCAL_LEDGER = HERE / "published_articles.jsonl"
REMOTE_LEDGER = "/opt/kais-proxy-sniper/published_articles.jsonl"
RELAY_LOG = "/var/log/nginx/affiliate_relay.log"
SSH_HOST = "us-server"

SITES = [
    {
        "name": "Scraping API Benchmark",
        "url": "https://scrape.mybskm.top/blog/403-tax.html",
        "home": "https://scrape.mybskm.top/",
        "devto": "https://dev.to/600me/the-403-tax-what-anti-bot-protection-really-does-to-your-scraping-bill-50g7",
        "article_id": 4872430,
        "src": "article_403tax",
        "relay_hosts": {"www.scraperapi.com", "visit.decodo.com"},
    },
    {
        "name": "GPU Cloud Benchmark",
        "url": "https://gpu.mybskm.top/blog/h100-rental-trap.html",
        "home": "https://gpu.mybskm.top/",
        "devto": "https://dev.to/600me/the-h100-rental-trap-why-213-per-gpu-hour-is-not-the-price-you-pay-do7",
        "article_id": 4872432,
        "src": "article_h100trap",
        "relay_hosts": {"www.runpod.io", "cloud.vast.ai"},
    },
]

RESULTS = []


def check(name, condition, detail=""):
    RESULTS.append((name, bool(condition), detail))
    print("%s  %s%s" % ("PASS" if condition else "FAIL", name, ("  [" + detail + "]") if detail else ""))
    return bool(condition)


def fetch(url, follow=True, timeout=30):
    """Return (http_version, status, effective_url, body) using curl."""
    with tempfile.NamedTemporaryFile(suffix=".html") as handle:
        command = [
            "curl", "-sS", "--http2", "--max-time", str(timeout),
            "-o", handle.name,
            "-w", "%{http_version} %{http_code} %{url_effective}",
        ]
        if follow:
            command.append("-L")
        command.append(url)
        proc = subprocess.run(command, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError("curl failed for %s: %s" % (url, proc.stderr.strip()))
        version, status, effective = proc.stdout.strip().split(" ", 2)
        body = Path(handle.name).read_text(encoding="utf-8", errors="replace")
    return version, int(status), effective, body


def fetch_redirect(url, timeout=30):
    proc = subprocess.run(
        [
            "curl", "-sS", "--http2", "--max-time", str(timeout),
            "-o", "/dev/null", "-w", "%{http_code} %{redirect_url}",
            url,
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError("curl failed for %s: %s" % (url, proc.stderr.strip()))
    status, location = proc.stdout.strip().split(" ", 1)
    return int(status), location.strip()


def ssh(command, timeout=30):
    proc = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", SSH_HOST, command],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError("ssh failed: %s" % proc.stderr.strip())
    return proc.stdout


def canonical_of(body):
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']',
        body,
        re.I,
    )
    if not match:
        match = re.search(
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']',
            body,
            re.I,
        )
    return match.group(1) if match else None


def article_schema(body):
    for block in re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        body,
        re.S | re.I,
    ):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            check("JSON-LD block parses", False, str(exc))
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict) and item.get("@type") == "Article":
                return item
    return None


def cta_links(body):
    links = []
    for match in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\']', body):
        href = match.group(1).replace("&amp;", "&")
        if "src=" in href and "go.272738.xyz" in href:
            links.append(href)
    return list(dict.fromkeys(links))


def main():
    print("=" * 78)
    print("STEP-1 GROUNDWORK VERIFICATION")
    print("=" * 78)

    log_start = int(ssh("wc -l < " + RELAY_LOG).strip())

    cta_urls = []
    for site in SITES:
        print("\n-- %s" % site["name"])
        version, status, effective, body = fetch(site["url"])
        check("%s: HTTP/2 200" % site["url"], version in ("2", "2.0") and status == 200,
              "http/%s %s" % (version, status))
        check("%s: self-canonical" % site["url"],
              canonical_of(body) == site["url"], str(canonical_of(body)))
        schema = article_schema(body)
        if check("%s: Article JSON-LD present" % site["url"], schema is not None):
            required = ["headline", "description", "author", "publisher",
                        "datePublished", "dateModified"]
            missing = [field for field in required if not schema.get(field)]
            check("%s: schema required fields" % site["url"], not missing, ",".join(missing))
            author = schema.get("author") or {}
            publisher = schema.get("publisher") or {}
            check("%s: author is 600me" % site["url"],
                  isinstance(author, dict) and author.get("name") == "600me")
            check("%s: publisher named" % site["url"],
                  isinstance(publisher, dict) and bool(publisher.get("name")),
                  str(publisher.get("name")))
        site_ctas = cta_links(body)
        check("%s: CTA src=%s present" % (site["url"], site["src"]),
              len(site_ctas) >= 2 and all(("src=" + site["src"]) in link for link in site_ctas),
              "%d CTA links" % len(site_ctas))
        cta_urls.extend(site_ctas)

        version, status, effective, dev_body = fetch(site["devto"])
        check("Dev.to %s: HTTP 200" % site["article_id"], status == 200,
              "http/%s %s" % (version, status))
        check("Dev.to %s: canonical -> %s" % (site["article_id"], site["url"]),
              canonical_of(dev_body) == site["url"], str(canonical_of(dev_body)))

        version, status, effective, home_body = fetch(site["home"])
        check("%s: dashboard links to article" % site["home"],
              site["url"].replace(site["home"], "/") in home_body
              or site["url"] in home_body)

    print("\n-- Affiliate relay")
    fingerprints = []
    for url in cta_urls:
        status, location = fetch_redirect(url)
        expected_host = urlsplit(location).hostname
        site = next(s for s in SITES if s["src"] in url)
        check("relay %s 302" % urlsplit(url).path, status == 302,
              "%s -> %s" % (status, location))
        check("relay %s provider host" % urlsplit(url).path,
              expected_host in site["relay_hosts"], str(expected_host))
        fingerprints.append((urlsplit(url).path, urlsplit(url).query))

    deadline = time.time() + 10
    new_lines = ""
    while time.time() < deadline:
        new_lines = ssh("tail -n +%d %s" % (log_start + 1, RELAY_LOG))
        if all(
            any((" 302 " + path + "?" + query) in line for line in new_lines.splitlines())
            for path, query in fingerprints
        ):
            break
        time.sleep(0.5)
    for path, query in fingerprints:
        matched = [
            line for line in new_lines.splitlines()
            if (" 302 " + path + "?" + query) in line and "curl/" in line
        ]
        check("relay log records %s?%s" % (path, query), bool(matched),
              matched[-1] if matched else "no line")

    print("\n-- Ledger consistency")
    local_bytes = LOCAL_LEDGER.read_bytes()
    remote_bytes = ssh("cat " + REMOTE_LEDGER).encode("utf-8")
    check("ledger local == remote", hashlib.sha256(local_bytes).digest()
          == hashlib.sha256(remote_bytes).digest(),
          hashlib.sha256(local_bytes).hexdigest()[:16])
    receipts = [json.loads(line) for line in local_bytes.decode("utf-8").splitlines() if line.strip()]
    for site in SITES:
        row = next((item for item in receipts if item.get("id") == site["article_id"]), None)
        check("ledger %s canonical" % site["article_id"],
              bool(row) and row.get("canonical_url") == site["url"]
              and row.get("canonical_http_status") == 200,
              str(row.get("canonical_url") if row else None))

    failed = [item for item in RESULTS if not item[1]]
    print("\n" + "=" * 78)
    print("%d checks, %d passed, %d failed" % (len(RESULTS), len(RESULTS) - len(failed), len(failed)))
    for name, _, detail in failed:
        print("FAILED: %s [%s]" % (name, detail))
    print("=" * 78)
    return 0 if not failed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - the acceptance report needs the reason
        print("FATAL: %s" % exc, file=sys.stderr)
        sys.exit(1)
