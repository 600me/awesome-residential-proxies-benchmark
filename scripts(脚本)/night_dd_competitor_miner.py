#!/usr/bin/env python3
"""
Nighttime Competitor CPS & New Vertical Miner (runs detached on dd-lan 36-core node).
Scans npmjs.com, Hugging Face Spaces, Dev.to, and GitHub public repositories
for wild affiliate/CPS parasite patterns, shortlinks, and high-ticket SaaS merchants.
Zero LLM tokens used — pure multi-threaded Python network reconnaissance.
"""
import concurrent.futures
import json
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# Exclude our own accounts and known domains so we only find EXTERNAL competitors
OUR_ACCOUNTS = {
    "600me", "vainship", "constantconv", "unfitjewell", "mistyparticle",
    "pierrewheffert", "dnoddieva", "kais-data-lab", "proxy-finops-lab"
}
OUR_DOMAINS = {
    "272738.xyz", "go.272738.xyz", "mybskm.top", "proxy.mybskm.top",
    "llm.mybskm.top", "llc.mybskm.top", "plue.men", "github.com",
    "npmjs.com", "pypi.org", "huggingface.co", "dev.to", "gist.github.com",
    "google.com", "shields.io", "img.shields.io", "badge.fury.io",
    "pepy.tech", "jsdelivr.net", "unpkg.com", "raw.githubusercontent.com",
    "user-images.githubusercontent.com", "avatars.githubusercontent.com",
    "opensource.org", "mit-license.org", "apache.org", "w3.org",
    "python.org", "nodejs.org", "docker.com", "localhost", "127.0.0.1",
    "example.com", "twitter.com", "x.com", "linkedin.com", "youtube.com",
    "youtu.be", "discord.gg", "discord.com", "t.me", "medium.com",
    "buymeacoffee.com", "ko-fi.com", "patreon.com", "paypal.me", "sponsor"
}

AFFILIATE_URL_PATTERNS = re.compile(
    r'https?://[^\s"\'<>)\]]+(?:'
    r'[?&](?:via|ref|fpr|psr|aff|affiliate|partner|referral|utm_source|promocode|coupon)=[^\s"\'<>)\]]+'
    r'|(?:get|try|go|partner|affiliates?)\.[a-z0-9-]+\.[a-z]{2,}/[^\s"\'<>)\]]*'
    r'|(?:is\.gd|bit\.ly|t\.ly|dub\.sh|tinyurl\.com|cutt\.ly|rebrand\.ly)/[a-zA-Z0-9_-]{4,}'
    r')',
    re.IGNORECASE
)

SEARCH_QUERIES = [
    # High-intent commercial tool queries on npm / HF / Dev.to / GitHub
    "pricing calculator",
    "cost calculator",
    "coupon code",
    "promo code",
    "discount code",
    "affiliate",
    "residential proxy",
    "antidetect browser",
    "gpu cloud pricing",
    "llm cost calculator",
    "ai voice clone",
    "ai video generator",
    "cold email warmup",
    "lead generation scraper",
    "crypto trading bot",
    "forex vps",
    "us llc stripe",
    "virtual credit card",
    "captcha solver",
    "seo backlink",
    "tiktok shop automation",
    "onlyfans agency",
    "shopify spy tool",
    "amazon fba calculator",
]


def fetch_json(url: str, timeout: int = 12):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception:
        return None


def fetch_text(url: str, timeout: int = 12) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def extract_domain(url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(url)
        host = (parsed.netloc or "").lower().split(":")[0]
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def is_external_commercial_url(url: str) -> bool:
    host = extract_domain(url)
    if not host or "." not in host:
        return False
    for d in OUR_DOMAINS:
        if host == d or host.endswith("." + d):
            return False
    return True


def scan_npm_query(query: str):
    findings = []
    encoded = urllib.parse.quote(query)
    url = f"https://registry.npmjs.org/-/v1/search?text={encoded}&size=35"
    data = fetch_json(url)
    if not data or "objects" not in data:
        return findings

    for obj in data.get("objects", []):
        pkg = obj.get("package", {})
        name = pkg.get("name", "")
        publisher = (pkg.get("publisher") or {}).get("username", "")
        if publisher in OUR_ACCOUNTS:
            continue
        # Fetch package metadata readme snippet from registry
        pkg_data = fetch_json(f"https://registry.npmjs.org/{urllib.parse.quote(name, safe='')}")
        if not pkg_data:
            continue
        readme = pkg_data.get("readme", "") or ""
        homepage = pkg_data.get("homepage", "") or ""
        combined = f"{readme}\n{homepage}"
        matches = set(AFFILIATE_URL_PATTERNS.findall(combined))
        ext_urls = [u.rstrip(".,;:!)") for u in matches if is_external_commercial_url(u)]
        if ext_urls:
            findings.append({
                "platform": "npmjs.com",
                "query": query,
                "item": name,
                "author": publisher,
                "url": f"https://www.npmjs.com/package/{name}",
                "description": (pkg.get("description") or "")[:200],
                "affiliate_urls": ext_urls[:10],
                "domains": list({extract_domain(u) for u in ext_urls})
            })
    return findings


def scan_devto_query(tag_or_query: str):
    findings = []
    tag = re.sub(r"[^a-z0-9]", "", tag_or_query.lower().split()[0])
    if not tag:
        return findings
    articles = fetch_json(f"https://dev.to/api/articles?tag={tag}&per_page=30")
    if not isinstance(articles, list):
        return findings

    for art in articles:
        user = (art.get("user") or {}).get("username", "")
        if user in OUR_ACCOUNTS:
            continue
        art_id = art.get("id")
        if not art_id:
            continue
        detail = fetch_json(f"https://dev.to/api/articles/{art_id}")
        if not detail:
            continue
        body = (detail.get("body_markdown") or "") + "\n" + (detail.get("body_html") or "")
        matches = set(AFFILIATE_URL_PATTERNS.findall(body))
        ext_urls = [u.rstrip(".,;:!)") for u in matches if is_external_commercial_url(u)]
        if ext_urls:
            findings.append({
                "platform": "dev.to",
                "query": tag_or_query,
                "item": detail.get("title", ""),
                "author": user,
                "url": detail.get("url", ""),
                "description": (detail.get("description") or "")[:200],
                "affiliate_urls": ext_urls[:10],
                "domains": list({extract_domain(u) for u in ext_urls})
            })
    return findings


def scan_hf_spaces(query: str):
    findings = []
    encoded = urllib.parse.quote(query)
    spaces = fetch_json(f"https://huggingface.co/api/spaces?search={encoded}&limit=25&full=true")
    if not isinstance(spaces, list):
        return findings

    for sp in spaces:
        sp_id = sp.get("id", "")
        author = sp.get("author", "")
        if not sp_id or author in OUR_ACCOUNTS:
            continue
        readme = fetch_text(f"https://huggingface.co/spaces/{sp_id}/raw/main/README.md", timeout=8)
        app_py = fetch_text(f"https://huggingface.co/spaces/{sp_id}/raw/main/app.py", timeout=8)
        combined = f"{readme}\n{app_py}"
        matches = set(AFFILIATE_URL_PATTERNS.findall(combined))
        ext_urls = [u.rstrip(".,;:!)") for u in matches if is_external_commercial_url(u)]
        if ext_urls:
            findings.append({
                "platform": "huggingface.co/spaces",
                "query": query,
                "item": sp_id,
                "author": author,
                "url": f"https://huggingface.co/spaces/{sp_id}",
                "description": f"Likes: {sp.get('likes', 0)} | SDK: {sp.get('sdk', '')}",
                "affiliate_urls": ext_urls[:10],
                "domains": list({extract_domain(u) for u in ext_urls})
            })
    return findings


def scan_github_repos(query: str):
    findings = []
    encoded = urllib.parse.quote(f"{query} in:name,description,readme")
    data = fetch_json(f"https://api.github.com/search/repositories?q={encoded}&sort=updated&per_page=15")
    if not data or "items" not in data:
        return findings

    for repo in data.get("items", [])[:12]:
        full_name = repo.get("full_name", "")
        owner = (repo.get("owner") or {}).get("login", "")
        if not full_name or owner in OUR_ACCOUNTS:
            continue
        default_branch = repo.get("default_branch", "main")
        readme = fetch_text(f"https://raw.githubusercontent.com/{full_name}/{default_branch}/README.md", timeout=8)
        homepage = repo.get("homepage") or ""
        combined = f"{readme}\n{homepage}\n{repo.get('description') or ''}"
        matches = set(AFFILIATE_URL_PATTERNS.findall(combined))
        ext_urls = [u.rstrip(".,;:!)") for u in matches if is_external_commercial_url(u)]
        if ext_urls:
            findings.append({
                "platform": "github.com",
                "query": query,
                "item": full_name,
                "author": owner,
                "url": repo.get("html_url", ""),
                "description": f"Stars: {repo.get('stargazers_count', 0)} | {(repo.get('description') or '')[:150]}",
                "affiliate_urls": ext_urls[:10],
                "domains": list({extract_domain(u) for u in ext_urls})
            })
    return findings


def main():
    started = datetime.now(timezone.utc).isoformat()
    all_findings = []

    # Cap at 2 workers + polite delay so we never pollute the home router exit IP (144.34.225.53)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = []
        for q in SEARCH_QUERIES:
            futures.append(pool.submit(scan_npm_query, q))
            futures.append(pool.submit(scan_hf_spaces, q))
            futures.append(pool.submit(scan_devto_query, q))
        for f in concurrent.futures.as_completed(futures):
            try:
                res = f.result()
                if res:
                    all_findings.extend(res)
            except Exception:
                pass

    # GitHub rate limit is stricter unauthenticated, run sequentially with polite delay
    for q in SEARCH_QUERIES[:10]:
        try:
            res = scan_github_repos(q)
            if res:
                all_findings.extend(res)
        except Exception:
            pass
        time.sleep(2.5)

    # Deduplicate by item URL
    dedup = {}
    domain_counter = defaultdict(list)
    for item in all_findings:
        u = item["url"]
        if u not in dedup:
            dedup[u] = item
            for d in item["domains"]:
                domain_counter[d].append(item)

    sorted_domains = sorted(domain_counter.items(), key=lambda kv: len(kv[1]), reverse=True)

    output = {
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_unique_parasite_projects_found": len(dedup),
        "total_unique_merchant_domains_found": len(sorted_domains),
        "top_merchant_domains": [
            {
                "domain": d,
                "count": len(items),
                "platforms": list({x["platform"] for x in items}),
                "sample_projects": [x["url"] for x in items[:5]],
                "sample_affiliate_links": list({link for x in items for link in x["affiliate_urls"]})[:8]
            }
            for d, items in sorted_domains[:60]
        ],
        "all_findings": list(dedup.values())
    }

    with open("/tmp/night_cps_competitor_mining_result.json", "w", encoding="utf-8") as fp:
        json.dump(output, fp, indent=2, ensure_ascii=False)

    # Also write Markdown summary
    md = [
        "# 夜间 `dd-lan` (36核) 全网野生 CPS 同行逆向掘金报告",
        f"- **启动时间**: `{started}`",
        f"- **完成时间**: `{output['completed_at']}`",
        f"- **捕获外部同行寄生项目总数**: **{len(dedup)} 个**（覆盖 `npmjs.com`、`huggingface.co/spaces`、`dev.to`、`github.com`）",
        f"- **识别出外部商业/联盟目标域名总数**: **{len(sorted_domains)} 个**",
        "",
        "## 一、高频被同行寄生的商业/联盟域名 Top 40",
        "| 排名 | 目标商业/短链域名 | 被寄生项目数 | 涉及寄生平台 | 野生返佣链接样本 | 同行项目样本 |",
        "| :--- | :--- | :---: | :--- | :--- | :--- |"
    ]
    for idx, (d, items) in enumerate(sorted_domains[:40], 1):
        platforms = ", ".join(sorted({x["platform"] for x in items}))
        sample_link = items[0]["affiliate_urls"][0] if items[0]["affiliate_urls"] else ""
        sample_proj = items[0]["url"]
        md.append(f"| {idx} | `{d}` | {len(items)} | {platforms} | `{sample_link[:65]}` | {sample_proj} |")

    with open("/tmp/night_cps_competitor_mining_report.md", "w", encoding="utf-8") as fp:
        fp.write("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
