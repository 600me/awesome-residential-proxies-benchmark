#!/usr/bin/env python3
"""Public affiliate-footprint discovery. Links prove promotion, never sales."""
import argparse, asyncio, concurrent.futures, hashlib, importlib.util, json,re,urllib.request
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent
SEEDS=[
 {'url':'https://deals.meticsmedia.com/','operator':'Metics Media','platform':'YouTube + own bridge'},
 {'url':'https://www.tooltester.com/en/live-chat/livechat-review/','operator':'Robert Brandl / Tooltester','platform':'independent studio'},
 {'url':'https://onlinemediamasters.com/scalahosting-review/','operator':'Tom Dupuis / OnlineMediaMasters','platform':'independent creator'},
 {'url':'https://tonyteaches.tech/docker-compose-website-stack/','operator':'Tony Teaches Tech','platform':'YouTube + own bridge'},
 {'url':'https://www.emergingtechdaily.com/post/base44-review-2026-honest-no-code-test','operator':'Abhinand PS / Emerging Tech Daily','platform':'independent author'},
 {'url':'https://medium.com/@goldmine28697/unleash-productivity-and-security-with-sentrypc-your-ultimate-employee-monitoring-solution-2a25ccf96d35','operator':'The Digital Goldmine','platform':'Medium'},
 {'url':'https://gist.github.com/scumola/adacad7376eb9c984101feed22fa0fb8','operator':'scumola','platform':'GitHub Gist'},
 {'url':'https://jennleach.substack.com/p/my-creator-income-report','operator':'Jennifer Leach','platform':'Substack'}]

spec=importlib.util.spec_from_file_location('serp',ROOT/'find_unarchived_serp_reddit(打捞Google首页未锁Reddit活帖).py');serp=importlib.util.module_from_spec(spec);spec.loader.exec_module(serp)
PATTERN=re.compile(r'(?:pxf\.io|sjv\.io|7eer\.net|psgrow\.link|ps_partner_key|[?&](?:fpr|via|fp_ref|a_aid)=|shrsl\.com|tkqlhce\.com|anrdoezrs\.net|dpbolvw\.net|awin1\.com|irclickid)',re.I)
QUERIES={
 'reddit':['site:reddit.com "pxf.io"','site:reddit.com "sjv.io"','site:reddit.com "psgrow.link"'],
 'medium':['site:medium.com "pxf.io" "2026"','site:medium.com "7eer.net"','site:medium.com "fpr=" "review"'],
 'gist':['site:gist.github.com "pxf.io"','site:gist.github.com "shrsl.com"','site:gist.github.com "ps_partner_key"'],
 'substack':['site:substack.com "psgrow.link"','site:substack.com "via=" "affiliate"','site:substack.com "fpr=" "review"'],
 'youtube':['site:youtube.com/watch "sjv.io" "review"','site:youtube.com/watch "pxf.io" "2026"','site:youtube.com/watch "shrsl.com"'],
 'cj':['"tkqlhce.com" "review" "2026"','"anrdoezrs.net" "review" "2026"','"dpbolvw.net" "software"'],
 'operators':['"Craylor Made" "review"','"Metics Media" "review"','"Tooltester" "review"']}
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.text=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('script','style'):self.skip+=1
  if tag=='a' and a.get('href'):self.links.append(a['href'])
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip:self.text.append(data)
def scan(row):
 result={**row,'checked_at':serp.now(),'sales_verified':False,'sales_evidence':None}
 try:
  with urllib.request.urlopen(urllib.request.Request(row['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=8) as r:
   body=r.read(3000000).decode(errors='replace');result.update(http_status=r.status,final_url=r.url)
  parser=Extract();parser.feed(body)
  result['affiliate_links']=sorted(set(u for u in parser.links if PATTERN.search(u) and not any(x in u for x in ['twitter.com/intent','x.com/intent'])))
  # Video descriptions and embedded structured content also carry outbound URLs.
  result['embedded_footprints']=sorted(set(re.findall(r'https?[^\s<>"\\]+(?:pxf\.io|sjv\.io|7eer\.net|shrsl\.com)[^\s<>"\\]*',body)))[:30]
  result['text']=' '.join(parser.text)[:35000]
  result['headings']=re.findall(r'<h[123][^>]*>(.*?)</h[123]>',body,re.S)[:35]
  result['body_sha256']=hashlib.sha256(body.encode()).hexdigest()
 except Exception as e:result['error']=str(e)[:180]
 return result
async def main():
 from playwright.async_api import async_playwright
 args=argparse.ArgumentParser();args.add_argument('--skip-search',action='store_true');opts=args.parse_args()
 searches=[]
 async with async_playwright() as p:
  browser=await p.chromium.connect_over_cdp('http://127.0.0.1:9222');context=browser.contexts[0]
  if not opts.skip_search:
   searches=await serp.collect_serps(context,QUERIES)
   serp.save(serp.EVIDENCE/'affiliate-google-serps.json',searches)
  else:
   source=serp.EVIDENCE/'affiliate-google-serps.json'
   if source.exists():searches=json.loads(source.read_text())
  entries={s['url']:s for s in SEEDS}
  for s in searches:
   for link in s['results']:entries.setdefault(link['url'],{**link,'query':s['query'],'platform':s['lane']})
  with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:results=list(ex.map(scan,entries.values()))
  # Render only the five primary case pages and retain measurable layout evidence.
  sem=asyncio.Semaphore(2)
  async def render(row):
   async with sem:
    page=await context.new_page();await page.set_viewport_size({'width':1440,'height':1000})
    try:
     response=await page.goto(row['url'],timeout=8000,wait_until='domcontentloaded')
     row['browser_http_status']=response.status
     row['rendered_text']=(await page.locator('body').inner_text())[:35000]
     links=await page.locator('a[href]').evaluate_all('es=>es.map(e=>({text:e.innerText.slice(0,90),url:e.href,rel:e.rel}))')
     row['outbound_links']=[x for x in links if x['url'].startswith('http')]
     row['affiliate_links']=sorted(set(row.get('affiliate_links',[])+[x['url'] for x in links if PATTERN.search(x['url']) and 'twitter.com/intent' not in x['url']]))
     row['layout']=await page.locator('h1,h2,main,article').evaluate_all('es=>es.slice(0,15).map(e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);return {tag:e.tagName,text:e.innerText.slice(0,100),x:r.x,y:r.y,width:r.width,height:r.height,fontSize:s.fontSize,fontFamily:s.fontFamily,color:s.color}})')
     filename='operator-'+hashlib.sha256(row['url'].encode()).hexdigest()[:12]+'.png'
     await page.screenshot(path=str(serp.EVIDENCE/filename),full_page=False,timeout=8000)
     row['screenshot']='evidence(取证)/'+filename
    except Exception as e:row['browser_error']=str(e)[:200]
    finally:await page.close()
  await asyncio.gather(*(render(r) for r in results[:5]))
 serp.save(ROOT/'live_cps_operator_candidates(同行候选证据).json',results)
 print(json.dumps({'scanned':len(results),'with_fingerprints':sum(bool(r.get('affiliate_links') or r.get('embedded_footprints')) for r in results),'verified_sales':sum(r.get('sales_verified') is True for r in results)}))
if __name__=='__main__':asyncio.run(main())
