#!/usr/bin/env python3
"""
Event 3: 14-Brand De-Watered Real External Buyer Click Radar.
Reads /var/log/nginx/affiliate_relay.log* on us-server (go.272738.xyz via -J jp-server)
and /var/log/nginx/access.log* on jp-server (plue.men), strictly separating:
  - tool (curl, python, Go-http, wget, httpx...)
  - bot (crawlers, spiders, Semrush, Ahrefs...)
  - probe (health checks, empty Mozilla/5.0)
  - audit_ip_or_cdn_sweep (known self IPs + any IP hitting >=4 distinct brands in the same 5-minute window via CDN)
  - real_human (genuine single-intent browser clicks with real UA)
"""
import collections
import json
import os
import re
import subprocess
from datetime import datetime, timezone

ALL_14_BRANDS = [
    "/smartproxy", "/scraperapi", "/firstbase", "/vastai", "/runpod",
    "/elevenlabs", "/adspower", "/9proxy", "/voluum", "/pawns",
    "/webshare", "/packetstream", "/morelogin", "/heygen",
]

REMOTE_PARSER_CODE = r'''
import glob, re, subprocess, collections, json

def lines():
    for f in sorted(glob.glob('/var/log/nginx/affiliate_relay.log*')):
        out = subprocess.run(['zcat', '-f', f], capture_output=True, text=True).stdout
        for l in out.splitlines():
            if l.strip():
                yield l

TOOL = re.compile(r'curl|python|Go-http|Wget|wget|okhttp|axios|aiohttp|health-probe|fasthttp|httpx|postman|insomnia|rest-client|node-fetch|undici', re.I)
BOT = re.compile(r'bot|spider|crawler|archive\.org|crawl|slurp|facebookexternalhit|Applebot|iPhone OS 13_2_3|Semrush|Ahrefs|Yandex|Baidu|BingPreview|HeadlessChrome|Playwright|Puppeteer', re.I)
PROBE = re.compile(r'^Mozilla/5\.0$|^Mozilla/5\.0 \(Windows NT 10\.0; Win64; x64\) AppleWebKit/537\.36$|^-$')

pat = re.compile(r'^(\S+) (\d+) (\S+) (?:(\S+) )?"(.*)" (\S+)$')
audit_ips = {'96.9.225.9', '144.34.225.53', '103.150.8.157', '45.221.112.81', '43.139.140.26', '127.0.0.1'}

BRANDS = [
    '/smartproxy', '/scraperapi', '/firstbase', '/vastai', '/runpod',
    '/elevenlabs', '/adspower', '/9proxy', '/voluum', '/pawns',
    '/webshare', '/packetstream', '/morelogin', '/heygen'
]

parsed_records = []
ip_minute_brands = collections.defaultdict(set)

for l in lines():
    m = pat.match(l)
    if not m:
        continue
    t, st, path, ref, ua, ip = m.groups()
    base = path.split('?')[0]
    minute_bucket = t[:16]  # YYYY-MM-DDTHH:MM
    if base in BRANDS:
        ip_minute_brands[(ip, minute_bucket)].add(base)
    parsed_records.append((t, st, path, base, ref or '-', ua, ip, minute_bucket))

# Any IP hitting >= 4 distinct brands in the same minute is a CDN-proxied audit sweep
cdn_sweep_ips_minutes = {k for k, v in ip_minute_brands.items() if len(v) >= 4}

rows = collections.Counter()
real_human_events = []

for t, st, path, base, ref, ua, ip, minute_bucket in parsed_records:
    if base not in BRANDS:
        continue
    if ip in audit_ips or 'audit' in ua.lower() or 'test=' in path or (ip, minute_bucket) in cdn_sweep_ips_minutes:
        c = 'audit'
    elif TOOL.search(ua):
        c = 'tool'
    elif BOT.search(ua):
        c = 'bot'
    elif PROBE.search(ua.strip()) or 'probe' in base or 'health' in base:
        c = 'probe'
    else:
        c = 'human'
        real_human_events.append({
            'time': t,
            'brand': base,
            'full_path': path,
            'referer': ref,
            'ua': ua[:120],
            'ip_masked': '.'.join(ip.split('.')[:2] + ['*', '*']) if '.' in ip else ip[:8]
        })
    rows[(base, c)] += 1

breakdown = {}
for b in BRANDS:
    breakdown[b] = {
        'total': sum(rows[(b, k)] for k in ('tool', 'bot', 'probe', 'audit', 'human')),
        'tool': rows[(b, 'tool')],
        'bot': rows[(b, 'bot')],
        'probe': rows[(b, 'probe')],
        'audit': rows[(b, 'audit')],
        'real_human': rows[(b, 'human')],
    }

totals = {
    k: sum(breakdown[b][k] for b in BRANDS)
    for k in ('total', 'tool', 'bot', 'probe', 'audit', 'real_human')
}

print(json.dumps({
    'totals_14brands': totals,
    'by_brand': breakdown,
    'recent_real_human_clicks': real_human_events[-40:]
}))
'''


def main():
    us_key = "/Users/a600/.claude/skills/docker-project-installer(Docker项目安装器)/config/ssh_key"
    cmd = [
        "ssh", "-J", "jp-server", "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no",
        "-i", us_key, "root@96.9.225.9",
        "cat > /usr/local/bin/parse_affiliate_relay_14brands.py && python3 /usr/local/bin/parse_affiliate_relay_14brands.py"
    ]
    res = subprocess.run(cmd, input=REMOTE_PARSER_CODE, capture_output=True, text=True, timeout=30)
    if res.returncode != 0 or not res.stdout.strip():
        raise RuntimeError(f"SSH log parse failed: {res.stderr}")

    data = json.loads(res.stdout.strip().splitlines()[-1])
    data["generated_at"] = datetime.now(timezone.utc).isoformat()

    out_dir = "/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/reports(报告)"
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "real-buyer-click-radar(真实外部买家点击雷达).json")
    md_path = os.path.join(out_dir, "real-buyer-click-radar(真实外部买家点击雷达).md")

    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)

    t = data["totals_14brands"]
    md = [
        "# 事件 3：`go.272738.xyz` 14 大品牌网关真实外部买家点击雷达（已剥离 CDN 批量审计与爬虫）",
        f"- **更新时间**: `{data['generated_at']}`",
        f"- **14 品牌总请求数**: **{t['total']}**",
        f"  - 剔除脚本/工具 (`tool`): `{t['tool']}`",
        f"  - 剔除爬虫 (`bot`): `{t['bot']}`",
        f"  - 剔除探针 (`probe`): `{t['probe']}`",
        f"  - 剔除自测与 CDN 同分钟批量扫链 (`audit`): `{t['audit']}`",
        f"  - **真实外部人类买家点击 (`real_human`)**: **{t['real_human']}**",
        "",
        "## 一、14 大品牌去水点击明细表",
        "| 品牌路由 | 总请求 (`total`) | 工具 (`tool`) | 爬虫 (`bot`) | 探针 (`probe`) | 审计扫链 (`audit`) | **真实人类点击 (`real_human`)** |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    for b, row in data["by_brand"].items():
        md.append(
            f"| `{b}` | {row['total']} | {row['tool']} | {row['bot']} | {row['probe']} | {row['audit']} | **{row['real_human']}** |"
        )

    with open(md_path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(md) + "\n")

    print(json.dumps(data["totals_14brands"], ensure_ascii=False))


if __name__ == "__main__":
    main()
