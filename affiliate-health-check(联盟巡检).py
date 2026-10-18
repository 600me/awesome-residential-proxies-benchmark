#!/usr/bin/env python3
"""One-shot affiliate relay check; Python 3 standard library, no install or state.

Check live activation status, not email semantics. Gmail stays with the existing
authorized connector; do not create OAuth credentials or infer approval from mail.
Pending placeholder routes exit without logging in or touching production.
"""

from concurrent.futures import ThreadPoolExecutor
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


BASE = "https://go.272738.xyz/"
ACTIVE = {
    "smartproxy": ("Smartproxy", "https://visit.decodo.com/k434W0"),
    "firstbase": ("Firstbase", "https://get.firstbase.io/slcdxtscxrh7"),
    "runpod": ("RunPod", "https://www.runpod.io/?ref=zzhi58ly&utm_source=github&utm_campaign=gpu_benchmark"),
    "vastai": ("Vast.ai", "https://cloud.vast.ai/?ref_id=748114&utm_source=github&utm_campaign=gpu_benchmark"),
    "scraperapi": ("ScraperAPI", "https://www.scraperapi.com/?fp_ref=kais-08a45e&utm_source=github&utm_campaign=scraping_benchmark"),
}
PENDING = {
    "brightdata": "brightdata.com", "apify": "apify.com",
    "doola": "www.doola.com", "zenrows": "www.zenrows.com",
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


def redirect(url, method="HEAD"):
    request = Request(url, method=method, headers={"User-Agent": "curl/8.7.1"})
    try:
        response = build_opener(NoRedirect()).open(request, timeout=10)
    except HTTPError as error:
        response = error
    with response:
        return response.code, response.headers.get("Location", "")


def check(route):
    try:
        code, location = redirect(BASE + route)
        if route in ACTIVE:
            name, expected = ACTIVE[route]
            if code != 302 or location != expected:
                raise ValueError(f"expected 302 Location={expected}; got {code} {location}")
            detail = location
            if route in ("smartproxy", "firstbase"):
                # These two affiliate IDs live in a path; GET resolves their
                # tracking parameters. Firstbase HEAD can return a false 404.
                downstream_code, downstream = redirect(location, method="GET")
                parsed = urlsplit(downstream)
                query = parse_qs(parsed.query)
                if route == "smartproxy":
                    valid = (parsed.hostname == "decodo.com"
                             and bool(query.get("irclickid", [""])[0])
                             and query.get("mediapartnerid") == ["7982506"])
                else:
                    valid = (parsed.hostname == "www.firstbase.io"
                             and query.get("ps_partner_key") == ["NmU0MjMzOGY4OWJj"]
                             and bool(query.get("ps_xid", [""])[0]))
                if downstream_code not in (301, 302, 303, 307, 308) or not valid:
                    raise ValueError(f"tracking hop failed: HTTP {downstream_code} {downstream}")
                detail += f" -> HTTP {downstream_code} {downstream}"
            return "active", f"PASS {name}: HTTP 302; affiliate attribution intact; {detail}"
        parsed = urlsplit(location)
        if code not in (301, 302) or parsed.scheme != "https" or parsed.hostname != PENDING[route]:
            raise ValueError(f"unexpected pending route: HTTP {code} {location}")
        if "REPLACE_ME" not in location:
            return "changed", f"NEW_LINK {route}: {location}; verify official approval before synchronizing"
        return "pending", f"SKIP {route}: inactive REPLACE_ME; no login, no deploy, no retry loop"
    except (OSError, URLError, ValueError) as error:
        return "error", f"FAIL {route}: {error}"


def main():
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=9) as pool:
        results = list(pool.map(check, [*ACTIVE, *PENDING]))
    for _, message in results:
        print(message)
    counts = {kind: sum(item[0] == kind for item in results)
              for kind in ("active", "pending", "changed", "error")}
    exit_code = 1 if counts["error"] else 2 if counts["changed"] else 0
    print(f"active={counts['active']}/5 pending={counts['pending']}/4 "
          f"new_links={counts['changed']} errors={counts['error']} "
          f"elapsed_ms={(time.monotonic() - started) * 1000:.0f} exit={exit_code}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
