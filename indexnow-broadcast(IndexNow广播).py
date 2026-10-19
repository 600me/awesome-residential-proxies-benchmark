#!/usr/bin/env python3
"""IndexNow broadcast driven by each site's live sitemap.xml.

One-shot submission; no timer, no retries, no persistent queue, standard library
only. Every URL that a host publishes in its own sitemap is read back over HTTPS
and forwarded to api.indexnow.org as a single per-host payload, so search engines
are notified about /calculator/ and /blog/* pages rather than only the homepage.

Usage:
    python3 "indexnow-broadcast(IndexNow广播).py"

Exit code is 0 only when every host's key file verifies, every sitemap yields at
least one URL, every host is accepted with HTTP 200/202, and the fleet published
at least MIN_TOTAL_URLS URLs in total.
"""

import json
import re
import subprocess
from datetime import datetime, timezone
from urllib.parse import urlsplit

KEY = "e9a7c3b2f1048a90d8e27c1b5049a3ef"
KEY_LOCATION = "https://{host}/{key}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"

# Hosts whose online sitemap.xml is walked and rebroadcast.
HOSTS = (
    "proxy.mybskm.top",
    "scrape.mybskm.top",
    "gpu.mybskm.top",
    "pay.mybskm.top",
    "esim.mybskm.top",
)

# The fleet must forward at least this many URLs for the run to count as complete.
MIN_TOTAL_URLS = 16

LOC_RE = re.compile(r"<loc>\s*([^<\s]+?)\s*</loc>", re.IGNORECASE)
DOH_ARGS = ["--doh-url", "https://cloudflare-dns.com/dns-query"]


def curl(url, *, method="GET", payload=None, timeout=30):
    """Return (returncode, stdout, stderr) for a curl invocation."""
    command = ["curl", *DOH_ARGS, "-sS", "--max-time", str(timeout),
               "-w", "\n%{http_code}", "-X", method]
    if payload is not None:
        command += ["-H", "Content-Type: application/json; charset=utf-8",
                    "--data-binary", "@-"]
    command.append(url)
    result = subprocess.run(command, input=payload, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def verify_key(host):
    returncode, stdout, stderr = curl(KEY_LOCATION.format(host=host, key=KEY), timeout=20)
    if returncode != 0:
        raise RuntimeError(f"{host}: key fetch failed: {stderr.strip()}")
    body = stdout.rsplit("\n", 1)[0].strip()
    if body != KEY:
        raise RuntimeError(f"{host}: public key mismatch at {KEY_LOCATION.format(host=host, key=KEY)}")


def sitemap_urls(host):
    """Read https://<host>/sitemap.xml and return its same-host https URLs."""
    returncode, stdout, stderr = curl(f"https://{host}/sitemap.xml", timeout=20)
    if returncode != 0:
        raise RuntimeError(f"{host}: sitemap fetch failed: {stderr.strip()}")
    body = stdout.rsplit("\n", 1)[0]
    seen, urls = set(), []
    for candidate in LOC_RE.findall(body):
        parts = urlsplit(candidate)
        if parts.scheme != "https" or parts.netloc != host:
            continue
        if candidate in seen:
            continue
        seen.add(candidate)
        urls.append(candidate)
    if not urls:
        raise RuntimeError(f"{host}: sitemap.xml published no usable URLs")
    return urls


def broadcast(host, url_list):
    payload = json.dumps({"host": host, "key": KEY,
                          "keyLocation": KEY_LOCATION.format(host=host, key=KEY),
                          "urlList": url_list})
    returncode, stdout, stderr = curl(ENDPOINT, method="POST", payload=payload, timeout=30)
    body, _, status = stdout.rpartition("\n")
    accepted = returncode == 0 and status in ("200", "202")
    return accepted, status.strip(), body.strip(), stderr.strip()


def main():
    # Phase 1: verify every public key before a single notification is sent.
    for host in HOSTS:
        verify_key(host)

    # Phase 2: read every live sitemap.
    listings = {host: sitemap_urls(host) for host in HOSTS}
    total_urls = sum(len(urls) for urls in listings.values())

    # Phase 3: one POST per host, grouped by domain.
    failed = False
    for host in HOSTS:
        url_list = listings[host]
        accepted, status, body, error = broadcast(host, url_list)
        failed |= not accepted
        print(json.dumps({
            "time": datetime.now(timezone.utc).isoformat(),
            "host": host,
            "urls": url_list,
            "url_count": len(url_list),
            "http_status": status,
            "accepted": accepted,
            "response": body,
            "error": error,
        }, ensure_ascii=False))

    if total_urls < MIN_TOTAL_URLS:
        failed = True
        print(json.dumps({"summary": "insufficient coverage", "total_urls": total_urls,
                          "required": MIN_TOTAL_URLS}, ensure_ascii=False))
    else:
        print(json.dumps({"summary": "ok", "hosts": len(HOSTS), "total_urls": total_urls},
                         ensure_ascii=False))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
