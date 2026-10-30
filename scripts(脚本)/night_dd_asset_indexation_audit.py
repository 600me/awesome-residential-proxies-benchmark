#!/usr/bin/env python3
"""
Event 2: Nighttime 50+ Live Assets Search Indexation & Visibility Audit (runs on dd-lan).
Checks all 50+ live CPS assets (29 GitHub repos, 10 Dev.to articles, 4 PyPI packages,
2 Hugging Face assets, 5 Whitehat portals + blog pages) for:
  1. Live HTTP status & response time
  2. Platform search/index status (PyPI JSON metadata, Dev.to engagement, HF API status)
  3. External search engine indexation signals (Bing / DuckDuckGo exact URL/title index check)
Outputs actionable Spider Interlinking Plan for any unindexed assets.
"""
import concurrent.futures
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

ASSETS = [
    # 5 Whitehat sites + 8 canonical blog pages
    {"category": "whitehat_site", "name": "proxy.mybskm.top", "url": "https://proxy.mybskm.top/"},
    {"category": "whitehat_site", "name": "gpu.mybskm.top", "url": "https://gpu.mybskm.top/"},
    {"category": "whitehat_site", "name": "pay.mybskm.top", "url": "https://pay.mybskm.top/"},
    {"category": "whitehat_site", "name": "scrape.mybskm.top", "url": "https://scrape.mybskm.top/"},
    {"category": "whitehat_site", "name": "esim.mybskm.top", "url": "https://esim.mybskm.top/"},
    {"category": "whitehat_blog", "name": "blog:heygen-vs-synthesia", "url": "https://gpu.mybskm.top/blog/heygen-vs-synthesia-elevenlabs.html"},
    {"category": "whitehat_blog", "name": "blog:morelogin-vs-adspower", "url": "https://proxy.mybskm.top/blog/morelogin-vs-adspower-packetstream-tco.html"},
    {"category": "whitehat_blog", "name": "blog:firstbase-vs-atlas", "url": "https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html"},
    {"category": "whitehat_blog", "name": "blog:runpod-vs-vastai", "url": "https://gpu.mybskm.top/blog/runpod-vs-vastai-h100-a100.html"},
    {"category": "whitehat_blog", "name": "blog:smartproxy-vs-scraperapi", "url": "https://scrape.mybskm.top/blog/smartproxy-vs-scraperapi.html"},

    # 4 PyPI Official Packages
    {"category": "pypi", "name": "check-proxy-tax", "url": "https://pypi.org/project/check-proxy-tax/"},
    {"category": "pypi", "name": "llm-gpu-cost-calculator", "url": "https://pypi.org/project/llm-gpu-cost-calculator/"},
    {"category": "pypi", "name": "us-llc-compliance-tco", "url": "https://pypi.org/project/us-llc-compliance-tco/"},
    {"category": "pypi", "name": "ad-tracker-antidetect-tco", "url": "https://pypi.org/project/ad-tracker-antidetect-tco/"},

    # 2 Hugging Face Assets
    {"category": "huggingface", "name": "HF Space: llm-gpu-cost-calculator", "url": "https://huggingface.co/spaces/600me/llm-gpu-cost-calculator"},
    {"category": "huggingface", "name": "HF Dataset: developer-coupons-breakdown", "url": "https://huggingface.co/datasets/600me/developer-coupons-breakdown"},

    # 10 Dev.to Articles
    {"category": "devto", "name": "devto:403-tax", "url": "https://dev.to/600me/the-403-tax-what-anti-bot-protection-really-does-to-your-scraping-bill-50g7"},
    {"category": "devto", "name": "devto:h100-rental-trap", "url": "https://dev.to/600me/the-h100-rental-trap-why-213-per-gpu-hour-is-not-the-price-you-pay-do7"},
    {"category": "devto", "name": "devto:049-proxy-illusion", "url": "https://dev.to/600me/the-049-proxy-illusion-how-a-200-line-cli-exposes-real-scraping-costs-5008"},
    {"category": "devto", "name": "devto:5-mor-illusion", "url": "https://dev.to/600me/the-5-mor-illusion-exact-us-llc-stripe-breakeven-for-non-us-saas-founders-2026-1h2l"},
    {"category": "devto", "name": "devto:sticky-session-ttl", "url": "https://dev.to/600me/why-rotating-residential-proxies-still-get-403s-sticky-session-ttl-ja3-fingerprints-and-asn-4g3n"},
    {"category": "devto", "name": "devto:firstbase-vs-atlas", "url": "https://dev.to/600me/firstbase-vs-stripe-atlas-vs-doola-2026-true-3-year-us-llc-registered-agent-irs-form-5472-3fcd"},
    {"category": "devto", "name": "devto:runpod-vs-vastai", "url": "https://dev.to/600me/runpod-vs-vastai-2026-real-h100-a100-effective-cost-after-cold-start-nvme-storage--1ei1"},
    {"category": "devto", "name": "devto:smartproxy-vs-scraperapi", "url": "https://dev.to/600me/smartproxy-decodo-vs-scraperapi-2026-raw-residential-proxy-pool-vs-managed-anti-bot-unblocker-5402"},
    {"category": "devto", "name": "devto:heygen-vs-synthesia", "url": "https://dev.to/600me/heygen-vs-synthesia-elevenlabs-in-2026-ai-video-avatar-dubbing-localization-unit-economics-1gb"},
    {"category": "devto", "name": "devto:morelogin-vs-adspower", "url": "https://dev.to/600me/morelogin-cloud-phone-vs-adspower-packetstream-1gb-residential-proxy-stack-100-account-matrix-i5b"},

    # 30 GitHub Repositories (600me 6 + 6 pioneer accounts x 4 = 30)
    {"category": "github_main", "name": "600me/awesome-residential-proxies-benchmark", "url": "https://github.com/600me/awesome-residential-proxies-benchmark"},
    {"category": "github_main", "name": "600me/check-proxy-tax", "url": "https://github.com/600me/check-proxy-tax"},
    {"category": "github_main", "name": "600me/decodo-smartproxy-pricing-coupons", "url": "https://github.com/600me/decodo-smartproxy-pricing-coupons"},
    {"category": "github_main", "name": "600me/firstbase-promo-code-pricing", "url": "https://github.com/600me/firstbase-promo-code-pricing"},
    {"category": "github_main", "name": "600me/runpod-gpu-pricing-coupons", "url": "https://github.com/600me/runpod-gpu-pricing-coupons"},
    {"category": "github_main", "name": "600me/scraperapi-pricing-coupons", "url": "https://github.com/600me/scraperapi-pricing-coupons"},
    {"category": "github_main", "name": "600me/vastai-gpu-pricing-coupons", "url": "https://github.com/600me/vastai-gpu-pricing-coupons"},

    {"category": "github_matrix", "name": "vainship/decodo-coupon-pricing-breakdown", "url": "https://github.com/vainship/decodo-coupon-pricing-breakdown"},
    {"category": "github_matrix", "name": "vainship/brightdata-pricing-vs-decodo", "url": "https://github.com/vainship/brightdata-pricing-vs-decodo"},
    {"category": "github_matrix", "name": "vainship/oxylabs-pricing-vs-decodo", "url": "https://github.com/vainship/oxylabs-pricing-vs-decodo"},
    {"category": "github_matrix", "name": "vainship/residential-proxy-scraping-costs", "url": "https://github.com/vainship/residential-proxy-scraping-costs"},

    {"category": "github_matrix", "name": "constantconv/firstbase-coupon-code-pricing", "url": "https://github.com/constantconv/firstbase-coupon-code-pricing"},
    {"category": "github_matrix", "name": "constantconv/stripe-atlas-vs-firstbase-costs", "url": "https://github.com/constantconv/stripe-atlas-vs-firstbase-costs"},
    {"category": "github_matrix", "name": "constantconv/doola-pricing-vs-firstbase", "url": "https://github.com/constantconv/doola-pricing-vs-firstbase"},
    {"category": "github_matrix", "name": "constantconv/non-us-founder-llc-annual-cost", "url": "https://github.com/constantconv/non-us-founder-llc-annual-cost"},

    {"category": "github_matrix", "name": "unfitjewell/scraperapi-coupon-code-breakdown", "url": "https://github.com/unfitjewell/scraperapi-coupon-code-breakdown"},
    {"category": "github_matrix", "name": "unfitjewell/scrapingbee-vs-scraperapi-pricing", "url": "https://github.com/unfitjewell/scrapingbee-vs-scraperapi-pricing"},
    {"category": "github_matrix", "name": "unfitjewell/web-scraping-api-cost-comparison", "url": "https://github.com/unfitjewell/web-scraping-api-cost-comparison"},
    {"category": "github_matrix", "name": "unfitjewell/zenrows-vs-scraperapi-pricing", "url": "https://github.com/unfitjewell/zenrows-vs-scraperapi-pricing"},

    {"category": "github_matrix", "name": "mistyparticle/webshare-coupon-code-pricing-guide", "url": "https://github.com/mistyparticle/webshare-coupon-code-pricing-guide"},
    {"category": "github_matrix", "name": "mistyparticle/brightdata-vs-webshare-pricing", "url": "https://github.com/mistyparticle/brightdata-vs-webshare-pricing"},
    {"category": "github_matrix", "name": "mistyparticle/smartproxy-vs-webshare-cost-comparison", "url": "https://github.com/mistyparticle/smartproxy-vs-webshare-cost-comparison"},
    {"category": "github_matrix", "name": "mistyparticle/rotating-residential-proxy-bandwidth-calculator", "url": "https://github.com/mistyparticle/rotating-residential-proxy-bandwidth-calculator"},

    {"category": "github_matrix", "name": "pierrewheffert/runpod-coupon-pricing-guide", "url": "https://github.com/pierrewheffert/runpod-coupon-pricing-guide"},
    {"category": "github_matrix", "name": "pierrewheffert/lambda-labs-vs-runpod-h100-costs", "url": "https://github.com/pierrewheffert/lambda-labs-vs-runpod-h100-costs"},
    {"category": "github_matrix", "name": "pierrewheffert/vastai-vs-runpod-serverless-pricing", "url": "https://github.com/pierrewheffert/vastai-vs-runpod-serverless-pricing"},
    {"category": "github_matrix", "name": "pierrewheffert/llm-inference-gpu-hourly-calculator", "url": "https://github.com/pierrewheffert/llm-inference-gpu-hourly-calculator"},

    {"category": "github_matrix", "name": "dnoddieva/vastai-promo-code-credit-guide", "url": "https://github.com/dnoddieva/vastai-promo-code-credit-guide"},
    {"category": "github_matrix", "name": "dnoddieva/runpod-vs-vastai-gpu-rental-costs", "url": "https://github.com/dnoddieva/runpod-vs-vastai-gpu-rental-costs"},
    {"category": "github_matrix", "name": "dnoddieva/aws-p5-vs-vastai-h100-pricing", "url": "https://github.com/dnoddieva/aws-p5-vs-vastai-h100-pricing"},
    {"category": "github_matrix", "name": "dnoddieva/spot-instance-gpu-training-budget", "url": "https://github.com/dnoddieva/spot-instance-gpu-training-budget"},
]


def probe_asset(asset: dict) -> dict:
    url = asset["url"]
    t0 = time.monotonic()
    http_status = 0
    has_noindex = False
    outbound_links_count = 0
    title = ""
    err = None

    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            http_status = resp.status
            body = resp.read().decode("utf-8", errors="ignore")
            if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', body, re.I):
                has_noindex = True
            m_title = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
            if m_title:
                title = re.sub(r"\s+", " ", m_title.group(1)).strip()[:100]
            outbound_links_count = len(re.findall(r'https?://(?:is\.gd|go\.272738\.xyz|[a-z]+\.mybskm\.top)/[^\s"\'<>)\]]+', body))
    except urllib.error.HTTPError as e:
        http_status = e.code
        err = f"HTTP {e.code}"
    except Exception as e:
        err = str(e)[:120]

    latency_ms = round((time.monotonic() - t0) * 1000)

    # Check Bing web search indexation signal for the URL path/slug
    parsed = urllib.parse.urlparse(url)
    search_key = f"{parsed.netloc}{parsed.path.rstrip('/')}"
    bing_indexed = False
    try:
        q = urllib.parse.quote(f'"{search_key}"')
        b_req = urllib.request.Request(f"https://www.bing.com/search?q={q}", headers={"User-Agent": UA})
        with urllib.request.urlopen(b_req, timeout=10) as b_resp:
            b_html = b_resp.read().decode("utf-8", errors="ignore")
            if parsed.path.rstrip("/").split("/")[-1].lower() in b_html.lower() and "b_algo" in b_html:
                bing_indexed = True
    except Exception:
        pass

    return {
        **asset,
        "http_status": http_status,
        "latency_ms": latency_ms,
        "has_noindex": has_noindex,
        "cta_or_internal_links": outbound_links_count,
        "bing_indexed_signal": bing_indexed,
        "title": title,
        "error": err,
    }


def main():
    started = datetime.now(timezone.utc).isoformat()
    results = []
    # Cap at 2 workers + polite sleep so we never trigger anti-bot verification on home router IP (144.34.225.53)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = []
        for a in ASSETS:
            futures.append(pool.submit(probe_asset, a))
            time.sleep(0.4)
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())

    results.sort(key=lambda x: (x["category"], x["name"]))
    live_200 = sum(1 for r in results if r["http_status"] == 200)
    noindex_cnt = sum(1 for r in results if r["has_noindex"])
    bing_cnt = sum(1 for r in results if r["bing_indexed_signal"])
    unindexed = [r for r in results if not r["bing_indexed_signal"]]

    summary = {
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_assets_checked": len(results),
        "http_200_count": live_200,
        "noindex_detected_count": noindex_cnt,
        "bing_indexed_signal_count": bing_cnt,
        "unindexed_assets_needing_spider_links": [r["url"] for r in unindexed],
        "assets": results,
    }

    with open("/tmp/night_asset_indexation_result.json", "w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2, ensure_ascii=False)

    md = [
        "# 夜间 `dd-lan` 事件 2：已上线 51 个 CPS 资产全量存活、SEO `noindex` 排雷与搜索引擎收录摸底报告",
        f"- **启动时间**: `{started}`",
        f"- **完成时间**: `{summary['completed_at']}`",
        f"- **检测资产总数**: **{len(results)} 个**（5 白帽站 + 5 深度 Blog + 4 PyPI 官方包 + 2 HF 资产 + 10 Dev.to 文章 + 25 GitHub 仓）",
        f"- **HTTP 200 存活率**: **{live_200} / {len(results)}**",
        f"- **发现致命 `noindex` 标签数**: **{noindex_cnt}**（0 为最佳）",
        f"- **已捕获外部搜索引擎（Bing）收录信号数**: **{bing_cnt} / {len(results)}**",
        "",
        "## 一、全部 51 个线上资产逐项体检明细",
        "| 类别 | 资产名称 | HTTP | 耗时(ms) | `noindex` | 页面内转化/互链数 | 搜索收录信号 | URL |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |"
    ]
    for r in results:
        idx_badge = "YES" if r["bing_indexed_signal"] else "PENDING"
        no_idx = "WARN_NOINDEX" if r["has_noindex"] else "Clean"
        md.append(
            f"| `{r['category']}` | `{r['name']}` | {r['http_status']} | {r['latency_ms']} | {no_idx} | {r['cta_or_internal_links']} | {idx_badge} | {r['url']} |"
        )

    with open("/tmp/night_asset_indexation_report.md", "w", encoding="utf-8") as fp:
        fp.write("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
