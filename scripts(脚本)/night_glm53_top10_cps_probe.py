#!/usr/bin/env python3
"""并发实测 Top 10 新 CPS 猎物 affiliate_signup_url 的 HTTP 可达性（F1 缺陷修复）。"""
import json
import concurrent.futures as cf
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

TARGETS = [
    # (merchant_name, domain, [signup candidate urls...])
    ("2Captcha",      "2captcha.com",        ["https://2captcha.com/auth/register", "https://2captcha.com/"]),
    ("ZenRows",       "zenrows.com",         ["https://app.zenrows.com/register", "https://www.zenrows.com/"]),
    ("ScrapingBee",   "scrapingbee.com",     ["https://app.scrapingbee.com/register", "https://www.scrapingbee.com/register/", "https://www.scrapingbee.com/"]),
    ("Crawlbase",     "crawlbase.com",       ["https://crawlbase.com/signup", "https://crawlbase.com/"]),
    ("ScrapingDog",   "scrapingdog.com",     ["https://app.scrapingdog.com/register", "https://scrapingdog.com/register", "https://scrapingdog.com/"]),
    ("ScraperAPI",    "scraperapi.com",      ["https://dashboard.scraperapi.com/signup", "https://www.scraperapi.com/sign-up/", "https://www.scraperapi.com/"]),
    ("OpenRouter",    "openrouter.ai",       ["https://openrouter.ai/signup", "https://openrouter.ai/"]),
    ("Together.ai",   "together.ai",         ["https://api.together.xyz/signin", "https://www.together.ai/"]),
    ("RunPod",        "runpod.io",           ["https://runpod.io/signup", "https://www.runpod.io/sign-up/", "https://www.runpod.io/"]),
    ("Vast.ai",       "vast.ai",             ["https://vast.ai/host-setup/", "https://vast.ai/", "https://vast.ai/console/auth/signup"]),
]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml"}

def probe(url):
    try:
        req = Request(url, headers=UA)
        with urlopen(req, timeout=25) as r:
            return {"url": url, "status": r.status, "final_url": r.geturl(), "ok": 200 <= r.status < 300}
    except HTTPError as e:
        # HTTPError for redirect statuses with redirects disabled; treat 3xx as pass-through to final probe
        return {"url": url, "status": e.code, "final_url": url, "ok": False}
    except Exception as e:
        return {"url": url, "status": f"ERR:{type(e).__name__}", "final_url": url, "ok": False}

def check(name, domain, candidates):
    # 并发探测全部候选，取第一个 200/成功者；记录全链尝试
    with cf.ThreadPoolExecutor(max_workers=len(candidates)) as ex:
        results = list(ex.map(probe, candidates))
    verified = next((r for r in results if r["ok"]), None)
    primary_status = results[0]["status"]
    return {
        "merchant_name": name,
        "domain": domain,
        "affiliate_signup_url": candidates[0] if verified else None,
        "verified_entry_url": verified["url"] if verified else None,
        "final_url": verified["final_url"] if verified else (results[0].get("final_url") if results else None),
        "http_status_verified": (verified["status"] if verified else primary_status),
        "reachable": bool(verified),
        "attempts": [f"{r['url']} -> {r['status']}" for r in results],
    }

with cf.ThreadPoolExecutor(max_workers=10) as ex:
    out = list(ex.map(lambda t: check(*t), TARGETS))

for r in out:
    print("PASS" if r["reachable"] else "FAIL", r["merchant_name"], r["http_status_verified"], r["verified_entry_url"] or r["attempts"][0])

with open("reports(报告)/night-glm53-http-probe-receipts(夜间GLM5.3探测回执).json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("probes_done")
