#!/usr/local/bin/python3
"""Capture two US-English Google queries per brand; unknown is never zero."""
import asyncio, datetime, json, sys
from pathlib import Path
from urllib.parse import quote, urlparse
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent
BRANDS = ['ScraperAPI','Decodo (Smartproxy)','Firstbase','RunPod','Vast.ai','ZenRows','ScrapingBee','Apify','Crawlbase','Webshare','IPRoyal','SOAX','Rayobyte','Proxy-Cheap','DataImpulse','Lambda Labs','Together AI','Modal','DigitalOcean','Vultr','Cloudways','ScalaHosting','Doola','Stripe Atlas','Deel','Mercury','BandwagonHost','ZgoCloud','GTHost','ExtraVM','GoMami','Evoxt','HostDare']
PARASITES = ['knowt.com','linkedin.com','medium.com','reddit.com','sites.google.com']
def matches(host, domain): return host == domain or host.endswith('.'+domain)
async def main():
    sem = asyncio.Semaphore(2)
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        owned_pages = []
        async def scan(brand, suffix):
            async with sem:
                page = await context.new_page()
                owned_pages.append(page)
                query = brand+' '+suffix
                row = {'query':query,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':[]}
                row['url'] = 'https://www.google.com/search?q='+quote(query)+'&num=10&hl=en&gl=us&pws=0&udm=14'
                try:
                    response = await page.goto(row['url'],wait_until='domcontentloaded',timeout=25000)
                    row['http_status'] = response.status
                    await page.locator('#rso h3').first.wait_for(timeout=12000)
                    links = await page.locator('#rso h3').evaluate_all('es=>es.filter(e=>!e.closest("[data-text-ad]" )).map(e=>({title:e.innerText,url:e.closest("a")?.href})).filter(e=>e.url)')
                    seen = set()
                    for link in links:
                        host = urlparse(link['url']).hostname or ''
                        if link['url'] in seen or host in ('google.com', 'www.google.com'): continue
                        seen.add(link['url'])
                        row['results'].append({**link,'domain':host.removeprefix('www.'),'rank':len(row['results'])+1})
                        if len(row['results']) == 10: break
                    row['body_excerpt'] = (await page.locator('body').inner_text())[:20000]
                    row['valid'] = response.status == 200 and len(row['results']) >= 5
                except Exception as exc:
                    row['valid'] = False
                    row['error'] = str(exc)[:300]
                finally:
                    await page.close()
                print(query,len(row['results']),row['valid'],flush=True)
                return row
        cached = {}
        target = ROOT/'untapped_high_commission_brands(未占坑高佣品牌蓝海池).json'
        if ('--retry-failed' in sys.argv or '--cached-only' in sys.argv) and target.exists():
            cached = {q['query']:q for b in json.loads(target.read_text())['brands'] for q in b['queries'] if q['valid'] or '--cached-only' in sys.argv}
        async def reuse_or_scan(b, s):
            return cached[b+' '+s] if b+' '+s in cached else await scan(b,s)
        raw = await asyncio.gather(*(reuse_or_scan(b,s) for b in BRANDS for s in ['promo code 2026','coupon code']))
        assert all(page.is_closed() for page in owned_pages), 'Task tab leaked'
    rows = []
    for i, brand in enumerate(BRANDS):
        queries = raw[i*2:i*2+2]
        valid = all(q['valid'] for q in queries)
        unique = {r['url']:r for q in queries for r in q['results']}
        gh = sum(matches(r['domain'],'github.com') or matches(r['domain'],'gist.github.com') for r in unique.values()) if valid else None
        parasite = sum(any(matches(r['domain'],d) for d in PARASITES) for r in unique.values()) if valid else None
        total = gh + parasite if valid else None
        level = '未知：抓取不完整' if not valid else ('🟢 无同行GitHub/寄生占位（传统聚合站占位）' if total == 0 else '🟡 轻度竞争' if total <= 3 else '🔴 已被同行霸屏')
        rows.append({'brand':brand,'github_count':gh,'parasite_count':parasite,'competition_level':level,'top_domains':list(dict.fromkeys(r['domain'] for r in unique.values()))[:10],'commission_rate':None,'commission_status':'未核实当前联盟条款及本账号提现资格','action_priority':'先补抓取' if not valid else '优先核验联盟资格与条款' if total == 0 else '候选研究' if total <= 3 else '低优先级','queries':queries})
    output = {'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'brand_count':len(rows),'query_count':len(raw),'complete':all(q['valid'] for q in raw),'method':'US-English Google web results, first up to 10 organic links per query. Counts deduplicated by URL across both queries. Green means zero specified host results in this sample, not zero market competition; red means >=4 specified-host URLs, not verified common ownership. No search volume or revenue inference.','tabs_closed':True,'brands':rows}
    (ROOT/'untapped_high_commission_brands(未占坑高佣品牌蓝海池).json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print('SCAN COMPLETE',sum(q['valid'] for q in raw),'/',len(raw),flush=True)
if __name__ == '__main__': asyncio.run(main())
