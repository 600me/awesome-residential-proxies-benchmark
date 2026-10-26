#!/usr/bin/env python3
"""Run the requested mechanical assertions; report commercial evidence separately."""
import ast
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
HUNT=ROOT/'competitor-hunter(同行反查器)'
REPORT=Path('/Users/a600/project-hub(项目设计实施)/kais-business-findings(生意发现记录)/cps-live-hijack-benchmarks-20261026(海外CPS活体截流同行拆解报告).md')
FAILURES=[]
GITHUB='https://github.com/600me/check-proxy-tax'
BANNED={'agrtech','webscrapinginsider','webdatadiggers','privatepackets','scrapingtheweb'}
ALLOWED={'llc_life','entrepreneur','saas','kickstarter','smallbusiness','ollama','localllm','stablediffusion','localllama','n8n','webdev','webscraping'}
def check(name,fn):
 try:
  detail=fn();print('PASS',name,detail or '')
 except (AssertionError,ValueError,KeyError,TypeError,OSError,IndexError) as e:
  FAILURES.append(name);print('FAIL',name,str(e))
def read(path):return json.loads(path.read_text())
def report_check():
 s=REPORT.read_text();n=len(re.findall(r'^## 案例 \d+：',s,re.M));assert n>=5,f'case count={n}'
 for term in ['Keywords','Bridge Page','佣金','出单证据','像素','https://']:assert term in s,term
 assert '58 个优惠搜索框' not in s
 assert '1 个搜索框，可检索 58 个优惠' in s
 case3=s.split('## 案例 3：')[1].split('## 案例 4：')[0]
 assert '2026-10-05更新' in case3 and '2026-10-03' not in case3
 assert '独立联盟站结构样本：3 个 Hosting/VPS，2 个 SaaS/No-code' in s
 assert s.count('- 同行属性：独立联盟站结构样本；Hosting/VPS')==3
 assert s.count('- 同行属性：独立联盟站结构样本；SaaS/No-code')==2
 proofs=read(HUNT/'evidence(取证)/remediation-redirects(整改跳转证据).json')
 for row,token,endpoint in zip(proofs,['aff118104','a=TeV6VODDJ9'],['https://www.hostinger.com/recommended/mm10','https://www.livechat.com/try-livechat/']):
  assert token in s and token in json.dumps(row)
  assert row['final_url'].startswith(endpoint) and row['final_url'] in s
  assert row['checked_at'] and re.fullmatch(r'[0-9a-f]{64}',row['body_sha256'])
  assert row['hops'][0]['url']==row['source_url']
  assert row['hops'][-1]['status']==200
  for a,b in zip(row['hops'],row['hops'][1:]):assert a['location']==b['url'] and a['status'] in (301,302,303,307,308)
 assert len(proofs)==2
 return f'{n} documented public cases (sales checked separately)'
def reddit_check():
 rows=read(HUNT/'serp_unarchived_reddit_targets(Google首页未锁帖靶标).json');assert isinstance(rows,list)
 assert 12<=len(rows)<=15,f'count={len(rows)}';seen=set();lanes=set();serps=read(HUNT/'evidence(取证)/google-serps.json')
 for r in rows:
  sub=r['subreddit'].lower().removeprefix('r/')
  assert sub not in BANNED,'excluded subreddit: '+sub
  assert sub in ALLOWED,'unreviewed subreddit: '+sub
  assert not r.get('removed_by_category'),'removed post'
  assert '/r/'+r['subreddit']+'/' in r['url'],'subreddit URL mismatch'
  assert r['id'] not in seen,'duplicate ID';seen.add(r['id']);lanes.add(r['lane'])
  assert r['archived'] is False and r['locked'] is False,r['id']+' must be boolean false'
  assert r['http_status']==200,r['id']+' JSON status'
  for k in ['url','title','subreddit','reply','json_url','evidence_file','evidence_sha256']:assert isinstance(r[k],str) and r[k].strip(),r['id']+' '+k
  assert re.fullmatch(r'https://www\.reddit\.com/r/[^/]+/comments/'+re.escape(r['id'])+r'/[^/]+/',r['url']),r['url']
  assert '/.json?' in r['json_url']
  for k in ['created_utc','score','num_comments']:assert type(r[k]) in (int,float),k
  assert 1<=r['google_rank']<=10
  matches=[s for s in serps if s['query']==r['google_query'] and s['checked_at']==r['google_checked_at']]
  assert any(any('/comments/'+r['id']+'/' in l['url'] and l['rank']==r['google_rank'] for l in s['results']) for s in matches),'SERP evidence mismatch'
  proof=HUNT/r['evidence_file'];assert proof.resolve().is_relative_to(HUNT.resolve())
  assert hashlib.sha256(proof.read_bytes()).hexdigest()==r['evidence_sha256'],'JSON proof hash mismatch'
  evidence=read(proof);post=evidence['post'];assert evidence['http_status']==200
  assert evidence['source_url']==r['json_url']
  for k in ['id','title','subreddit','created_utc','score','num_comments','archived','locked']:assert post[k]==r[k],k+' source mismatch'
  assert post['archived'] is False and post['locked'] is False
  assert re.search(r'\d',r['reply']) and '$' in r['reply'],'numeric cost example missing'
  reply=r['reply']
  assert not re.search(r'utm_|reddit_serp|mybskm\.top|go\.272738\.xyz|pxf\.io|sjv\.io',reply,re.I),'marketing marker/domain'
  urls=re.findall(r'https?://[^\s]+',reply)
  assert all(u==GITHUB for u in urls),'only canonical open-source URL permitted'
  assert 'Disclosure:' in reply and 'maintain' in reply,'maintainer disclosure missing'
  if r['lane'] in {'proxy','scrape'}:assert GITHUB in reply,'relevant CLI coverage missing'
  else:assert not urls,'off-topic tool promotion'
  assert len(r['reply'].split())>=45,'reply incomplete'
 assert {'llc','gpu','scrape'}<=lanes,str(lanes)
 relevant=[r for r in rows if r['lane'] in {'proxy','scrape'}]
 assert len(relevant)>=2
 assert all(GITHUB in r['reply'] for r in relevant),'GitHub coverage below 100% of relevant posts'
 print(f'GitHub coverage: {len(relevant)}/{len(relevant)} relevant posts; {len(relevant)}/{len(rows)} overall; other replies link-free')
 return f'{len(rows)} unique posts; source JSON, hashes, allowed communities and Google top-ten observations match'
def materials_check():
 node=(ROOT/'outbound-materials/nodeseek_tco_post.md').read_text();assert len(node)>600
 for x in ['零依赖','403','TCO','https://github.com/600me/check-proxy-tax','proxy.mybskm.top','scrape.mybskm.top','gpu.mybskm.top','pay.mybskm.top','utm_source=nodeseek','0.49','1.225']:assert x in node,x
 for x in ['开源/技术/分享','辅助体验','完整保留上文联盟披露']:assert x in node,x
 assert not re.search(r'https?://(?:go\.272738\.xyz|[^/\s]*pxf\.io|[^/\s]*sjv\.io)',node),'bare affiliate link'
 rows=read(ROOT/'outbound-materials/x_reply_hijack_targets.json');assert isinstance(rows,list) and len(rows)>=10
 assert len({r['id'] for r in rows})==len(rows)
 for r in rows:
  for k in ['id','lane','trigger','reply']:assert r.get(k),k
  assert 40<=len(r['reply'])<=280,(r['id'],len(r['reply']))
  assert '$' in r['reply'] and re.search(r'\d',r['reply']) and 'https://' in r['reply']
 assert {'gpu','proxy','llc'}<=set(r['lane'] for r in rows)
 assert abs(0.49/0.4-1.225)<1e-10
 return f'NodeSeek post + {len(rows)} X drafts; links, numerical examples and length checked'
def script_check():
 for name in ['hunt_live_cps_operators(反查活体CPS同行).py','find_unarchived_serp_reddit(打捞Google首页未锁Reddit活帖).py']:
  text=(HUNT/name).read_text();tree=ast.parse(text)
  assert any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='ThreadPoolExecutor' and any(k.arg=='max_workers' and isinstance(k.value,ast.Constant) and k.value.value==16 for k in n.keywords) for n in ast.walk(tree)),name+' max_workers'
  assert 'timeout=8' in text,name+' timeout'
 return 'both scanners compile and use 16 worker network pools'
def sales_check():
 cases=read(HUNT/'live_cps_operator_candidates(同行候选证据).json')
 confirmed=[];cutoff=dt.datetime.now(dt.timezone.utc)-dt.timedelta(days=30)
 for r in cases:
  if r.get('recent_sales_verified') is not True:continue
  e=r.get('sales_evidence');assert isinstance(e,dict),'sales evidence object required'
  assert e.get('operator')==r.get('operator') and e.get('source_url','').startswith('https://')
  when=dt.datetime.fromisoformat(e['transaction_at'].replace('Z','+00:00'))
  assert cutoff<=when<=dt.datetime.now(dt.timezone.utc),'sale outside last30days'
  assert e.get('public_evidence_file'),'missing transaction evidence'
  assert (HUNT/e['public_evidence_file']).is_file()
  confirmed.append(r['operator'])
 return len(set(confirmed))
if __name__=='__main__':
 check('report',report_check);check('reddit',reddit_check);check('materials',materials_check);check('scripts',script_check)
 sales=sales_check()
 print('EVIDENCE_GAP recent sales:',sales,'of 5 required; historical revenue and live pages are insufficient')
 print(json.dumps({'mechanical_passed':not FAILURES,'failed_checks':FAILURES,'recent_sales_verified':sales,'recent_sales_required':5,'full_task_satisfied':not FAILURES and sales>=5},ensure_ascii=False))
 sys.exit(1 if FAILURES else 0)
