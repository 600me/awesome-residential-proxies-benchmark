#!/usr/bin/env python3
"""Capture Google organic top ten and validate actual Reddit JSON; never infer flags."""
import asyncio, concurrent.futures, datetime, hashlib, json, re, urllib.request
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'evidence(取证)'
QUERIES={
 'llc':['firstbase vs doola reddit','stripe atlas vs firstbase reddit','best llc service for non-us residents reddit','lemon squeezy vs stripe llc reddit'],
 'gpu':['runpod vs vast ai reddit','cheapest h100 rental reddit','vast ai hidden costs reddit','best gpu cloud for llm reddit'],
 'proxy':['best residential proxy for scraping reddit','smartproxy vs bright data reddit','decodo proxy review reddit'],
 'scrape':['scraperapi vs zenrows reddit','cloudflare 403 scraping cost reddit','scraperapi pricing reddit']}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def fetch(item):
 url=item['url'].rstrip('/')+'/.json?raw_json=1&limit=1'
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'cps-benchmark-research/1.0'}),timeout=8) as r:
   return item,url,r.status,r.read().decode(),None
 except Exception as e:return item,url,None,None,str(e)
async def collect_serps(context, queries):
 sem=asyncio.Semaphore(3)
 async def one(lane,q):
  async with sem:
   page=await context.new_page();url='https://www.google.com/search?q='+quote(q)+'&num=10&hl=en&gl=us&pws=0&udm=14'
   result={'query':q,'lane':lane,'url':url,'checked_at':now(),'results':[]}
   try:
    r=await page.goto(url,timeout=8000,wait_until='domcontentloaded');result['status']=r.status
    await page.locator('#rso h3').first.wait_for(timeout=8000)
    links=await page.locator('#rso h3').evaluate_all('es=>es.map(e=>({title:e.innerText,url:e.closest("a")?.href})).filter(e=>e.url)')
    seen=set()
    for link in links:
     if link['url'] in seen:continue
     seen.add(link['url']);link['rank']=len(result['results'])+1;result['results'].append(link)
     if len(result['results'])==10:break
    result['page_text']=(await page.locator('body').inner_text())[:35000]
    await page.screenshot(path=str(EVIDENCE/('serp-'+hashlib.sha256(q.encode()).hexdigest()[:12]+'.png')),full_page=True)
   except Exception as e:result['error']=str(e)[:300]
   finally:await page.close()
   print('SERP',lane,q,len(result['results']),flush=True)
   return result
 return await asyncio.gather(*(one(l,q) for l,qs in queries.items() for q in qs))
def parse_post(item,url,status,body,error):
 base={**item,'json_url':url,'checked_at':now(),'http_status':status}
 if error:return {**base,'error':error}
 try:
  data=json.loads(body)[0]['data']['children'][0]['data']
  if data.get('id')!=item['id']:raise ValueError('post ID mismatch')
  public={k:data[k] for k in ['id','title','subreddit','created_utc','score','num_comments','archived','locked','selftext','permalink','author','removed_by_category'] if k in data}
  proof=EVIDENCE/('reddit-'+item['id']+'.json');save(proof,{'source_url':url,'http_status':status,'checked_at':base['checked_at'],'post':public})
  return {**base,**public,'evidence_file':str(proof.relative_to(ROOT)),'evidence_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'valid':status==200 and public.get('archived') is False and public.get('locked') is False and public.get('removed_by_category') is None}
 except Exception as e:return {**base,'error':type(e).__name__+': '+str(e)[:180]}
async def main():
 from playwright.async_api import async_playwright
 EVIDENCE.mkdir(exist_ok=True)
 target=ROOT/'serp_unarchived_reddit_targets(Google首页未锁帖靶标).json'
 previous={r['id']:r for r in json.loads(target.read_text())} if target.exists() else {}
 async with async_playwright() as p:
  browser=await p.chromium.connect_over_cdp('http://127.0.0.1:9222');context=browser.contexts[0]
  serps=await collect_serps(context,QUERIES);save(EVIDENCE/'google-serps.json',serps)
  candidates={}
  for serp in serps:
   for link in serp['results']:
    m=re.search(r'https://(?:www\.|old\.)?reddit.com/r/[^/]+/comments/([a-z0-9]+)/[^/?#]+/?',link['url'])
    if not m:continue
    ident=m[1];entry={'id':ident,'url':m[0].rstrip('/')+'/','lane':serp['lane'],'google_query':serp['query'],'google_rank':link['rank'],'google_serp_url':serp['url'],'google_checked_at':serp['checked_at']}
    candidates.setdefault(ident,entry)
  with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:raw=list(pool.map(fetch,candidates.values()))
  sem=asyncio.Semaphore(4)
  async def validate(row):
   item,url,status,body,error=row
   if error:
    async with sem:
     page=await context.new_page()
     try:
      r=await page.goto(url,timeout=8000,wait_until='domcontentloaded');status=r.status;body=await page.locator('body').inner_text();error=None
     except Exception as e:error=str(e)[:200]
     finally:await page.close()
   result=parse_post(item,url,status,body,error);print('JSON',item['id'],result.get('valid',False),flush=True);return result
  results=await asyncio.gather(*(validate(r) for r in raw))
  save(EVIDENCE/'reddit-validation-results.json',results)
  valid=[r for r in results if r.get('valid')]
  selected=[]
  for lane in QUERIES:
   matches=[r for r in valid if r['lane']==lane]
   matches.sort(key=lambda r:(r['id'] not in previous,r['google_rank'],-r['num_comments']))
   for row in matches[:5]:
    old=previous.get(row['id'],{})
    if old.get('title')==row['title'] and old.get('selftext')==row.get('selftext') and old.get('reply'):
     row['reply']=old['reply']
     row['copy_source']=old.get('copy_source')
    else:
     row['reply']=None
     row['draft_status']='needs_contextual_copy'
    selected.append(row)
  save(target,selected)
  print(json.dumps({'candidates':len(candidates),'valid':len(valid),'lanes':sorted(set(r['lane'] for r in valid))}))
if __name__=='__main__':asyncio.run(main())
