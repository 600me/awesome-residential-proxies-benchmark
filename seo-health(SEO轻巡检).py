#!/usr/bin/env python3
"""Check three public sites and the directive's Firstbase CPS relay; silent if healthy."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import re
import subprocess
from time import monotonic
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

HOSTS = ("proxy.mybskm.top", "gpu.mybskm.top", "pay.mybskm.top")


def fetch(url, head=False):
    command = ["curl", "-sS", "--connect-timeout", "5", "--max-time", "15",
               "--max-filesize", "1048576"]
    command += ["-I"] if head else []
    response = subprocess.run(command + ["-w", "\n%{http_code}", url],
                              capture_output=True, text=True)
    body, _, status = response.stdout.rpartition("\n")
    if response.returncode:
        raise ValueError(f"{url}: curl {response.returncode}: {response.stderr.strip()}")
    return status, body


def check(item):
    url, kind = item
    try:
        status, body = fetch(url, kind == "relay")
        if kind == "relay":
            locations = re.findall(r"(?im)^location:\s*(.+?)\s*$", body)
            destination = urlsplit(locations[-1] if locations else "")
            if status not in ("301", "302", "307", "308") or destination.scheme != "https" or not destination.hostname or destination.hostname == "go.272738.xyz":
                raise ValueError(f"invalid CPS redirect: HTTP {status}, {locations}")
            if "REPLACE_ME" in locations[-1]:
                raise ValueError("placeholder CPS destination")
        else:
            if status != "200":
                raise ValueError(f"HTTP {status}")
            if kind == "sitemap":
                root = ET.fromstring(body)
                ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
                home = url.removesuffix("sitemap.xml")
                if root.tag != ns + "urlset" or home not in [e.text for e in root.findall(f"{ns}url/{ns}loc")]:
                    raise ValueError("invalid sitemap or missing homepage")
            elif "application/ld+json" not in body or "</html>" not in body.lower():
                raise ValueError("homepage is incomplete or missing JSON-LD")
        return url, body, None
    except (ValueError, ET.ParseError) as error:
        return url, "", f"{url}: {error}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    started = monotonic()
    pages = [(f"https://{host}/", "home") for host in HOSTS]
    pages += [(f"https://{host}/sitemap.xml", "sitemap") for host in HOSTS]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, pages))
        relays = {"https://go.272738.xyz/firstbase"}
        results += list(pool.map(check, [(url, "relay") for url in sorted(relays)]))
    errors = [error for _, _, error in results if error]
    for error in errors:
        print(error)
    if args.verbose:
        print(f"{'FAIL' if errors else 'PASS'}: {len(pages)} site/sitemap checks, "
              f"{len(relays)} CPS relays, {len(errors)} errors, "
              f"{(monotonic() - started) * 1000:.0f} ms")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
