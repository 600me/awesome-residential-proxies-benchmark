#!/usr/bin/env python3
"""Build vps-sniper/traffic_audit_report.json from the US VPS nginx logs.

Read-only. Runs either on the Mac (reads the logs over SSH) or on the VPS itself
as proxy-sniper (reads the readable log files directly; no SSH loopback). Bot and
scanner noise is separated from browser-like sessions by path allowlist, declared
user-agent signatures, HTTP status, self/probe IP and reverse DNS. Human clicks
are attributed per `src` / `utm_content`. The health check is executed fresh when
its script is present and its 302 relays are recorded verbatim. A one-line
funnel summary JSON is printed at the end for the daily outreach log.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOST = "us-server"
RELAY_LOG = "/var/log/nginx/affiliate_relay.log"
ACCESS_LOG = "/var/log/nginx/access.log"
HEALTH_CANDIDATES = [
    HERE / "affiliate-health-check(联盟巡检).py",
    HERE.parent / "affiliate-health-check(联盟巡检).py",
]
OUT = HERE / "traffic_audit_report.json"
ACTIVE_ROUTES = ["smartproxy", "firstbase", "runpod", "vastai", "scraperapi"]
MONITOR_IPS = {"183.225.0.137"}  # Operator's own line: not an external human.
SELF_IPS = {"96.9.225.9", "127.0.0.1"}  # This VPS: health probes and self-checks.
PROBE_SRC_RE = re.compile(r"^(health_probe|verify_step|selftest|self_probe|smoke)", re.I)
AFFILIATE_ROUTES = {
    "airalo", "apify", "brightdata", "crawlbase", "deepinfra", "doola",
    "firstbase", "lemonsqueezy", "nomad", "openrouter", "oxylabs", "paddle",
    "runpod", "saily", "scraperapi", "scrapingbee", "smartproxy", "together",
    "vastai", "wise", "yesim", "zenrows",
}
PUBLIC_ROUTES = {"/", "/robots.txt"}
DATACENTER = re.compile(
    r"amazonaws\.com|googleusercontent\.com|azure|digitalocean|linode|ovh|"
    r"hetzner|contabo|vultr|oraclecloud|alicdn|alibaba|tencent|choopa|"
    r"colocation|server|hosting|leaseweb|psychz|quadranet", re.I)
BOT_UA = re.compile(
    r"bot|crawler|spider|scanner|scan|curl|python|aiohttp|httpclient|wget|"
    r"go-http|java/|okhttp|axios|node-fetch|phantom|headless|compatible\)|"
    r"synthient|cms-checker|isonsearch|pulsegate|internetmeasurement|"
    r"facebookexternalhit|semrush|ahrefs|yandex|bingpreview|gptbot|"
    r"oai-searchbot|googleother|googlebot|bingbot|ccbot|bytespider", re.I)
RELAY_RE = re.compile(r'^(\S+) (\d{3}) (\S+) (?:-|(\S+)) "(.*)" (\S+)$')
ACCESS_RE = re.compile(
    r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) [^"]*" (\d{3}) (\S+) "([^"]*)" "([^"]*)"')


def ssh_cat(path):
    result = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                             HOST, "cat", path], capture_output=True, text=True, check=True)
    return result.stdout


def read_log(path):
    """Read a log directly when this host owns it, else over SSH (read-only)."""
    local = Path(path)
    if local.is_file() and os.access(local, os.R_OK):
        return local.read_text(encoding="utf-8", errors="replace"), "local"
    return ssh_cat(path), "ssh"


def query_params(raw_path):
    """`?a=1&b=2` -> dict. Values are not URL-decoded: log literals are kept."""
    if "?" not in raw_path:
        return {}
    query = raw_path.split("?", 1)[1]
    return dict(part.split("=", 1) for part in query.split("&") if "=" in part)


def rdns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (OSError, socket.herror):
        return ""


def classify_relay(lines):
    status = Counter()
    routes = Counter()
    src = Counter()
    utm_sources = Counter()
    campaigns = Counter()
    reasons = Counter()
    human = []
    bots = []
    period = {"start": None, "end": None}
    parsed = []
    for line in lines:
        match = RELAY_RE.match(line)
        if not match:
            reasons["parse_error"] += 1
            continue
        ts, code, raw_path, _referrer, ua, ip = match.groups()
        period["start"] = period["start"] or ts
        period["end"] = ts
        status[code] += 1
        route = raw_path.split("?")[0]
        routes[route] += 1
        query = raw_path.split("?", 1)[1] if "?" in raw_path else ""
        if query:
            params = dict(part.split("=", 1) for part in query.split("&") if "=" in part)
            if "src" in params:
                src[params["src"]] += 1
            if "utm_source" in params:
                utm_sources[params["utm_source"]] += 1
            if "utm_campaign" in params:
                campaigns[params["utm_campaign"]] += 1
        parsed.append((ts, code, raw_path, ua, ip))

    scanner_ips = Counter(row[4] for row in parsed
                          if row[2].split("?")[0] not in PUBLIC_ROUTES
                          and row[2].split("?")[0].lstrip("/") not in AFFILIATE_ROUTES)
    tainted = {ip for ip, count in scanner_ips.items() if count >= 10}
    for ts, code, raw_path, ua, ip in parsed:
        route = raw_path.split("?")[0]
        if route not in PUBLIC_ROUTES and route.lstrip("/") not in AFFILIATE_ROUTES:
            reasons["scanner_path"] += 1
            bots.append((ts, code, raw_path, ua, ip, "scanner_path"))
        elif ip in tainted:
            reasons["scanner_ip_history"] += 1
            bots.append((ts, code, raw_path, ua, ip, "scanner_ip_history"))
        elif ip in MONITOR_IPS or ip in SELF_IPS:
            reasons["self_or_monitor_ip"] += 1
            bots.append((ts, code, raw_path, ua, ip, "self_or_monitor_ip"))
        elif BOT_UA.search(ua):
            reasons["bot_user_agent"] += 1
            bots.append((ts, code, raw_path, ua, ip, "bot_user_agent"))
        elif code[0] in "45":
            reasons["http_error"] += 1
            bots.append((ts, code, raw_path, ua, ip, "http_error"))
        else:
            human.append((ts, code, raw_path, ua, ip))
    return status, routes, src, utm_sources, campaigns, reasons, human, bots, period


def classify_access(lines):
    status = Counter()
    pages = Counter()
    reasons = Counter()
    human = []
    for line in lines:
        match = ACCESS_RE.match(line)
        if not match:
            reasons["parse_error"] += 1
            continue
        ip, _ts, method, raw_path, code, _size, referrer, ua = match.groups()
        status[code] += 1
        path = raw_path.split("?")[0]
        if method != "GET":
            reasons["non_get"] += 1
            continue
        if not (path == "/" or path.startswith("/blog/") or path in
                {"/robots.txt", "/sitemap.xml", "/data.json", "/README.md", "/favicon.ico"}
                or path.startswith("/calculator/")):
            reasons["scanner_path"] += 1
            continue
        if BOT_UA.search(ua):
            reasons["bot_user_agent"] += 1
            continue
        if code != "200":
            reasons["http_error"] += 1
            continue
        reasons["browser_like"] += 1
        pages[path] += 1
        human.append((ip, path, referrer, ua))
    return status, pages, reasons, human


def run_health():
    """Run the affiliate relay health check when it is available on this host."""
    script = next((path for path in HEALTH_CANDIDATES if path.is_file()), None)
    if script is None:
        return {"script": None, "exit_code": None, "summary": "", "counts": {},
                "relays": [], "raw": "", "skipped": "health-check script not present on this host"}
    result = subprocess.run([sys.executable, str(script)],
                            capture_output=True, text=True)
    output = result.stdout.strip()
    relays = []
    for line in output.splitlines():
        if line.startswith("PASS "):
            name = line.split(":", 1)[0][5:]
            status_match = re.search(r"HTTP (\d{3})", line)
            location = line.split("intact; ", 1)[-1].split(" -> ")[0].strip()
            relays.append({"name": name, "relay_status": int(status_match.group(1)) if status_match else None,
                           "location": location, "ok": bool(status_match and status_match.group(1) == "302")})
    summary = next((line for line in output.splitlines() if line.startswith("active=")), "")
    counts = {}
    for pair in summary.split():
        if "=" in pair:
            key, value = pair.split("=", 1)
            counts[key] = value
    return {"script": str(script), "exit_code": result.returncode, "summary": summary,
            "counts": counts, "relays": relays, "raw": output}


def shadowban_snapshot():
    """`gh-answer.py --check-shadowban` output, passed in via SHADOWBAN_REPORT."""
    path = os.environ.get("SHADOWBAN_REPORT", "")
    empty = {"source": None, "time": None, "checked": None, "visible": None,
             "hidden": None, "inconclusive": None}
    if not path:
        return empty
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return empty
    if not isinstance(data, dict):
        return empty
    return {"source": path, "time": data.get("time"), "checked": data.get("checked"),
            "visible": data.get("visible"), "hidden": data.get("hidden"),
            "inconclusive": data.get("inconclusive")}


def main():
    relay_text, relay_source = read_log(RELAY_LOG)
    access_text, access_source = read_log(ACCESS_LOG)
    relay_lines = relay_text.splitlines()
    access_lines = access_text.splitlines()

    (status, routes, src, utm_sources, campaigns, reasons,
     human, bots, period) = classify_relay(relay_lines)
    a_status, a_pages, a_reasons, a_human = classify_access(access_lines)

    enriched = []
    for ts, code, path, ua, ip in human:
        reverse = rdns(ip)
        enriched.append({"ts": ts, "status": int(code), "path": path, "ua": ua, "ip": ip,
                         "rdns": reverse, "datacenter": bool(DATACENTER.search(reverse))})
    affiliate_candidates = [row for row in enriched
                            if row["path"].split("?")[0].lstrip("/") in AFFILIATE_ROUTES]
    verified_human = [row for row in affiliate_candidates if not row["datacenter"]]

    claude_src = sum(1 for row in bots if row[5] == "bot_user_agent"
                     and "ClaudeBot" in row[3] and "src=" in row[2])

    # Real external human clicks only: verified human rows minus probe tokens.
    human_src = Counter()
    human_untagged = 0
    human_probe_tagged = 0
    external_human_302 = 0
    for row in verified_human:
        if row["status"] == 302:
            external_human_302 += 1
        params = query_params(row["path"])
        attribution = params.get("src") or params.get("utm_content") or ""
        if not attribution:
            human_untagged += 1
        elif PROBE_SRC_RE.match(attribution):
            human_probe_tagged += 1
        else:
            human_src[attribution] += 1
    attributed_human = sum(human_src.values())
    health = run_health()
    active_ok = sum(1 for r in health["relays"] if r["ok"])
    shadowban = shadowban_snapshot()
    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": HOST,
        "sources": {
            "relay_log": {"path": RELAY_LOG, "lines": len(relay_lines),
                          "bytes": len(relay_text.encode()), "sha256": hashlib.sha256(relay_text.encode()).hexdigest()},
            "access_log": {"path": ACCESS_LOG, "lines": len(access_lines),
                           "bytes": len(access_text.encode()), "sha256": hashlib.sha256(access_text.encode()).hexdigest()},
        },
        "period": period,
        "totals": {
            "requests": len(relay_lines),
            "status_302": status.get("302", 0),
            "status_301": status.get("301", 0),
            "status_404": status.get("404", 0),
            "status_400": status.get("400", 0),
            "redirect_rate_pct": round((status.get("302", 0) + status.get("301", 0)) / max(len(relay_lines), 1) * 100, 2),
        },
        "status_distribution": dict(status.most_common()),
        "route_distribution": dict(routes.most_common()),
        "parameterized": {
            "total": sum(1 for line in relay_lines if "?" in line.split(" ")[2]),
            "by_src": dict(src.most_common()),
            "by_utm_source": dict(utm_sources.most_common()),
            "by_campaign": dict(campaigns.most_common()),
        },
        "bot_filter": {
            "excluded": len(bots),
            "excluded_pct": round(len(bots) / max(len(relay_lines), 1) * 100, 2),
            "reasons": dict(reasons.most_common()),
            "by_ua": dict(Counter(row[3] for row in bots).most_common(10)),
        },
        "human_traffic": {
            "browser_like_candidates": len(enriched),
            "affiliate_route_candidates": len(affiliate_candidates),
            "verified_human_affiliate_clicks": len(verified_human),
            "external_human_302_clicks": external_human_302,
            "human_clicks_by_src": dict(human_src.most_common()),
            "human_clicks_by_src_total": attributed_human,
            "human_clicks_untagged": human_untagged,
            "human_clicks_probe_tagged_excluded": human_probe_tagged,
            "unique_ips": sorted({row["ip"] for row in enriched}),
            "datacenter_candidates": sum(1 for row in enriched if row["datacenter"]),
            "candidates": enriched,
            "affiliate_candidates": affiliate_candidates,
            "note": (f"{len(verified_human)} browser-like affiliate-route clicks survived the path, IP, "
                     f"user-agent, status and reverse-DNS filters; {external_human_302} of them were HTTP 302. "
                     f"{attributed_human} carry a src/utm_content token, {human_untagged} are untagged and "
                     f"{human_probe_tagged} carry a health/self probe token and are excluded from "
                     f"human_clicks_by_src."),
        },
        "access_log_summary": {
            "requests": len(access_lines),
            "status_200": a_status.get("200", 0),
            "status_404": a_status.get("404", 0),
            "status_410": a_status.get("410", 0),
            "browser_like_page_views": a_reasons.get("browser_like", 0),
            "filter_reasons": dict(a_reasons.most_common()),
            "top_pages": dict(a_pages.most_common(10)),
        },
        "health_check": {
            "script": health["script"],
            "expected_active": 5,
            "active_passed": active_ok,
            "all_302": active_ok == 5 and len(health["relays"]) == 5,
            "errors": int(health["counts"].get("errors", -1)),
            "new_links": int(health["counts"].get("new_links", -1)),
            "script_exit_code": health["exit_code"],
            "summary": health["summary"],
            "relays": health["relays"],
            "skipped": health.get("skipped"),
            "note": ("exit=2 is the script's documented signal for out-of-scope NEW_LINK "
                     "placeholders, not a relay failure."),
        },
        "shadowban_check": shadowban,
        "log_read_mode": {"relay": relay_source, "access": access_source},
        "findings": [
            f"{active_ok}/5 active affiliate relays returned HTTP 302 with attribution intact." if health["relays"]
            else f"Relay health check skipped on this host ({health.get('skipped')}).",
            f"{reasons.get('scanner_path', 0)} of {len(relay_lines)} relay requests were scanner probes for secrets and config files; they were excluded by the path allowlist.",
            f"{reasons.get('bot_user_agent', 0)} requests carried declared or tool user agents (curl, python-requests, ShapBot, ClaudeBot, Googlebot, GoogleOther) and were excluded.",
            f"{reasons.get('scanner_ip_history', 0)} requests came from IPs already tainted by scanner paths and were excluded by IP history.",
            f"{reasons.get('self_or_monitor_ip', 0)} requests came from this VPS or the operator's own line (health probes and self-checks) and were excluded.",
            f"{external_human_302} external human 302 clicks in the period; {attributed_human} are src-attributed "
            f"({', '.join(f'{k}={v}' for k, v in human_src.most_common(5)) or 'none'}), {human_untagged} untagged.",
            f"{human_probe_tagged} probe-tagged clicks and {claude_src} ClaudeBot src-tagged fetches are excluded from the human attribution table.",
            f"Access log is dominated by scanner noise; {a_status.get('200', 0)} of {len(access_lines)} requests returned 200.",
        ],
    }
    funnel = {
        "generated_at": report["generated_at"],
        "external_human_302_clicks": external_human_302,
        "human_clicks_by_src": dict(human_src.most_common()),
        "human_clicks_untagged": human_untagged,
        "human_clicks_probe_tagged_excluded": human_probe_tagged,
        "github_comments_visible": shadowban["visible"],
        "github_comments_checked": shadowban["checked"],
        "github_shadowban_hidden": shadowban["hidden"],
        "relay_requests": len(relay_lines),
        "active_relays_302": active_ok,
        "log_read_mode": report["log_read_mode"],
    }
    report["funnel"] = funnel
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("totals", "bot_filter", "human_traffic", "health_check")},
                     indent=2)[:3000])
    print("FUNNEL_SUMMARY " + json.dumps(funnel, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
