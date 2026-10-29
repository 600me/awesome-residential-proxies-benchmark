#!/usr/bin/env python3
"""Read-only HEAD tracing over existing US SSH; never opens merchant destinations."""
import pathlib,json,re,subprocess,datetime
P=pathlib.Path(__file__).resolve().parent
assets=json.loads((P/'assets-us-live(美区在线资产).json').read_text())
allow={'plue.men','da.gd','is.gd','tinyurl.com','v.gd','go.272738.xyz','dusen.party','norb.date','zelumo.top','proxy.mybskm.top','gpu.mybskm.top','scrape.mybskm.top','pay.mybskm.top'}
rows=[]
for a in assets:
 if a['url'].endswith('/check-proxy-tax'):continue
 links=sorted(set(re.findall(r'https?://[^\s<>\)"\]]+',a.get('readme',''))))
 rows.append({'repo':a['url'],'created_at':a.get('created_at'),'cta_candidates':[u for u in links if u.split('/')[2] in allow]})
urls=sorted({u for r in rows for u in r['cta_candidates']})
script=r'''
import urllib.request,urllib.parse,json,concurrent.futures,datetime
urls=URLS
allow=set(ALLOW)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):return None
opener=urllib.request.build_opener(NoRedirect)
def trace(u):
 out=[]; seen=set()
 for i in range(7):
  if u in seen:out.append({'error':'redirect_loop'});break
  seen.add(u)
  if urllib.parse.urlsplit(u).hostname not in allow:out.append({'terminal_url':u,'not_requested':True});break
  try:
   req=urllib.request.Request(u,method='HEAD',headers={'User-Agent':'cps-validation-health-probe/1.0'})
   try:r=opener.open(req,timeout=10)
   except urllib.error.HTTPError as e:r=e
   code=r.code;loc=r.headers.get('Location');out.append({'url':u,'status':code,'location':loc,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
   if code not in (301,302,303,307,308) or not loc:break
   u=urllib.parse.urljoin(u,loc)
  except Exception as e:out.append({'url':u,'error':str(e)});break
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:print(json.dumps(dict(zip(urls,ex.map(trace,urls)))))
'''.replace('URLS',repr(urls)).replace('ALLOW',repr(sorted(allow)))
r=subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','us-server','python3 -'],input=script,text=True,capture_output=True,timeout=500)
if r.returncode:raise RuntimeError('SSH trace failed')
traces=json.loads(r.stdout)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'HEAD; known shortlinks and own gateways only; merchant endpoint never requested','assets':rows,'traces':traces}
f=P/'cta-traces(跳转映射).json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2));print('repos',len(rows),'unique_candidates',len(traces),'terminal_records',sum(any('terminal_url' in h for h in v) for v in traces.values()))
