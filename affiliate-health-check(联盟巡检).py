#!/usr/bin/env python3
"""One-shot affiliate relay check; Python 3 standard library, no install or state.

Check live activation status, not email semantics. Gmail stays with the existing
authorized connector; do not create OAuth credentials or infer approval from mail.
Pending placeholder routes exit without logging in or touching production.

Attribution passthrough: every active route is probed twice. The clean request
(`/smartproxy`) must resolve to the vendor with the default `subid=direct`, and
a tagged request (`/smartproxy?src=health_probe_subid`) must carry that exact
token into the vendor's own parameter (`subId1` / `fp_sid` / `utm_content`).
A route that redirects but drops the token is a hard failure, because the
conversion would be unattributable in the affiliate dashboard.

Unaffiliated routes: the 13 dead `?ref=REPLACE_ME` links were removed on
2026-10-18 and replaced with plain official-homepage redirects that carry UTM
tags but no fake affiliate ref. Those routes are pinned to the audited target
below; `REPLACE_ME` reappearing anywhere is a hard failure.
"""

from concurrent.futures import ThreadPoolExecutor
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


BASE = "https://go.272738.xyz/"
SUBID_PROBE = "health_probe_subid"
SUBID_DEFAULT = "direct"
# route -> (display name, target template, vendor subid parameter)
ACTIVE = {
    "smartproxy": ("Smartproxy",
                   "https://visit.decodo.com/k434W0?subId1={subid}", "subId1"),
    "firstbase": ("Firstbase",
                  "https://get.firstbase.io/slcdxtscxrh7?utm_content={subid}",
                  "utm_content"),
    "runpod": ("RunPod",
               "https://www.runpod.io/?ref=zzhi58ly&utm_source=github"
               "&utm_campaign=gpu_benchmark&utm_content={subid}", "utm_content"),
    "vastai": ("Vast.ai",
               "https://cloud.vast.ai/?ref_id=748114&utm_source=github"
               "&utm_campaign=gpu_benchmark&utm_content={subid}", "utm_content"),
    "scraperapi": ("ScraperAPI",
                   "https://www.scraperapi.com/?fp_ref=kais-08a45e&fp_sid={subid}"
                   "&utm_source=github&utm_campaign=scraping_benchmark"
                   "&utm_content={subid}", "fp_sid"),
}
# route -> audited official-homepage target for vendors with no affiliate deal
UNAFFILIATED = {
    "brightdata": "https://brightdata.com/?utm_source=github&utm_campaign=proxy_benchmark",
    "apify": "https://apify.com/?utm_source=github&utm_campaign=proxy_benchmark",
    "doola": "https://www.doola.com/?utm_source=github&utm_campaign=payments_matrix",
    "zenrows": "https://www.zenrows.com/?utm_source=github&utm_campaign=scraping_benchmark",
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
    """Return (route, kind, message, subid_passthrough_ok)."""
    try:
        code, location = redirect(BASE + route)
        if route in ACTIVE:
            name, template, param = ACTIVE[route]
            expected = template.format(subid=SUBID_DEFAULT)
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
            # Tagged request: the sanitized token must reach the vendor intact.
            probe_code, probe_location = redirect(
                BASE + route + "?src=" + SUBID_PROBE)
            probe_expected = template.format(subid=SUBID_PROBE)
            if probe_code != 302 or probe_location != probe_expected:
                raise ValueError(
                    f"subid probe expected 302 Location={probe_expected}; "
                    f"got {probe_code} {probe_location}")
            probe_query = parse_qs(urlsplit(probe_location).query)
            if probe_query.get(param) != [SUBID_PROBE]:
                raise ValueError(
                    f"subid passthrough lost {param} in {probe_location}")
            return (route, "active",
                    f"PASS {name}: HTTP 302; affiliate attribution intact; "
                    f"subid passthrough {param}={SUBID_PROBE}; {detail}", True)
        expected = UNAFFILIATED[route]
        if "REPLACE_ME" in location:
            raise ValueError(f"dead placeholder link is public again: {location}")
        if code not in (301, 302) or location != expected:
            raise ValueError(
                f"unaffiliated route drifted: expected 301/302 Location={expected}; "
                f"got {code} {location}; re-verify affiliation before synchronizing")
        return (route, "unaffiliated",
                f"OK {route}: HTTP {code} {location}; no affiliate ref, no REPLACE_ME",
                False)
    except (OSError, URLError, ValueError) as error:
        return (route, "error", f"FAIL {route}: {error}", False)


def main():
    started = time.monotonic()
    routes = [*ACTIVE, *UNAFFILIATED]
    with ThreadPoolExecutor(max_workers=9) as pool:
        results = list(pool.map(check, routes))
    for _, _, message, _ in results:
        print(message)
    counts = {kind: sum(item[1] == kind for item in results)
              for kind in ("active", "unaffiliated", "error")}
    passthrough = sum(1 for route, _, _, ok in results if route in ACTIVE and ok)
    exit_code = 1 if counts["error"] else 0
    print(f"active={counts['active']}/5 unaffiliated={counts['unaffiliated']}/4 "
          f"subid_passthrough={passthrough}/5 errors={counts['error']} "
          f"elapsed_ms={(time.monotonic() - started) * 1000:.0f} exit={exit_code}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
