#!/usr/local/bin/python3
import base64, concurrent.futures, datetime, hashlib, json, re, subprocess, time
from html.parser import HTMLParser
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
ITEMS=[('scraperapi','scraperapi-pricing-coupons','scraperapi_calculator.py'),('decodo-smartproxy','decodo-smartproxy-pricing-coupons','smartproxy_calculator.py'),('firstbase','firstbase-promo-code-pricing','firstbase_calculator.py'),('runpod','runpod-gpu-pricing-coupons','runpod_gpu_calculator.py'),('vastai','vastai-gpu-pricing-coupons','vastai_gpu_calculator.py')]
def session():
    secret=Path('/Users/a600/.secrets(密钥)/github-token(GitHub发帖令牌).env').read_text()
    token=re.search(r'^(?:export\s+)?GITHUB_TOKEN\s*=\s*(.+?)\s*$',secret,re.M)[1].strip().strip('\"\'')
    s=requests.Session();s.headers.update({'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'});return s
S=session()
def api(method,path,data=None):
    r=S.request(method,'https://api.github.com'+path,json=data,timeout=45)
    if r.status_code==404 and method=='GET':return None
    if not r.ok:raise RuntimeError(f'{method} {path}: HTTP {r.status_code}')
    return r.json()
def put(repo,name,raw):
    path='/repos/600me/'+repo+'/contents/'+name;old=api('GET',path)
    if old and base64.b64decode(old['content'])==raw:return
    if old:
        b=ROOT/'backups(发布前备份)'/repo;b.mkdir(parents=True,exist_ok=True)
        (b/(datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'-'+name)).write_bytes(base64.b64decode(old['content']))
    data={'message':'Add runnable cost calculator and reference index','content':base64.b64encode(raw).decode()}
    if old:data['sha']=old['sha']
    api('PUT',path,data)
class Robots(HTMLParser):
    def __init__(self):super().__init__();self.tags=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta' and a.get('name','').lower() in ('robots','googlebot'):self.tags.append(a)
def inspect(item):
    d,repo,name=item;url='https://github.com/600me/'+repo
    r=requests.get(url,timeout=45);parser=Robots();parser.feed(r.text)
    directives=' '.join(t.get('content','') for t in parser.tags)+' '+r.headers.get('X-Robots-Tag','')
    return {'repository':url,'public_http':r.status_code,'robots_meta':parser.tags,'x_robots_tag':r.headers.get('X-Robots-Tag'),'indexable':r.status_code==200 and not re.search(r'\b(noindex|none)\b',directives,re.I),'html_sha256':hashlib.sha256(r.content).hexdigest(),'cookie_sent':'Cookie' in r.request.headers}
def main():
    assert api('GET','/user')['login'].lower()=='600me'
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:rows=list(ex.map(inspect,ITEMS))
    assert all(r['indexable'] and not r['cookie_sent'] for r in rows)
    for item,row in zip(ITEMS,rows):
        d,repo,name=item;raw=(ROOT/d/name).read_bytes();assert 50<=len(raw.splitlines())<=80
        run=subprocess.run(['/usr/local/bin/python3',str(ROOT/d/name),'--units','100','--unit-rate','.5','--base','10','--one-time','100','--annual-base','100'],capture_output=True,text=True,check=True)
        assert '$820.00' in run.stdout and '$800.00' in run.stdout
        put(repo,name,raw)
        remote=api('GET','/repos/600me/'+repo+'/contents/'+name)
        assert base64.b64decode(remote['content'])==raw
        r=requests.get(remote['download_url'],timeout=45);assert r.status_code==200 and r.content==raw
        row.update(script_url='https://github.com/600me/'+repo+'/blob/main/'+name,raw_url=remote['download_url'],script_http=r.status_code,readback_equal=True,lines=len(raw.splitlines()),test_exit_code=run.returncode,test_output=run.stdout)
        print('SCRIPT VERIFIED',repo,flush=True)
    filename='awesome-cloud-and-developer-tools-benchmarks.md'
    content='# Cloud and developer tools: runnable cost calculators\n\nIndependent, standard-library Python budget worksheets. These are arithmetic tools, not measured performance benchmarks. Rates are user supplied; no live price or coupon is promised. Linked buying guides disclose affiliate links.\n\n'
    for item,row in zip(ITEMS,rows):
        d,repo,name=item
        content+=f'## {d}\n\n[Repository and buying guide]({row["repository"]}) · [Python calculator]({row["script_url"]})\n\n```sh\npython3 {name} --units 100 --unit-rate 0.5 --base 10 --one-time 100 --annual-base 100\n```\n\nIllustrative first-year monthly billing: $820; annual base alternative: $800. Replace every rate and usage input with your actual quote.\n\n'
    existing=[]
    for page in range(1,11):
        batch=api('GET',f'/gists?per_page=100&page={page}');existing.extend(batch)
        if len(batch)<100:break
    found=next((g for g in existing if filename in g['files']),None)
    data={'description':'Independent runnable cost calculators for cloud and developer tools','files':{filename:{'content':content}}}
    gist_record={'url':None,'http_status':None,'bidirectional_links':False}
    try:
        if found:gist=api('PATCH','/gists/'+found['id'],data)
        else:gist=api('POST','/gists',{**data,'public':True})
        assert gist['public'];url=gist['html_url']
        for d,repo,name in ITEMS:
            p=ROOT/d/'README.md';text=p.read_text()
            addition=f'\n\n## Runnable budget calculator\n\nUse [{name}]({name}) with your own quoted rates. Compare monthly billing, first-year cost and an optional annual base quote. [Browse all five calculators]({url}).\n'
            if url not in text:
                put(repo,'README.md',(text+addition).encode());p.write_text(text+addition)
        r=requests.get(url,timeout=45);assert r.status_code==200
        gist_record={'url':url,'id':gist['id'],'http_status':r.status_code,'bidirectional_links':True}
    except RuntimeError as exc:
        gist_record['error']=str(exc)
        gist_record['token_scopes']=S.get('https://api.github.com/user',timeout=30).headers.get('X-OAuth-Scopes')
        (ROOT/filename).write_text(content)
    for attempt in range(12):
        for item,row in zip(ITEMS,rows):row['languages']=api('GET','/repos/600me/'+item[1]+'/languages')
        if all(r['languages'].get('Python',0)>0 for r in rows):break
        time.sleep(5)
    result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':rows,'index_gist':gist_record,'indexability_scope':'No noindex in anonymous HTML/headers; not evidence of Google inclusion or immunity from moderation.','repository_checks_passed':all(r['languages'].get('Python',0)>0 for r in rows),'complete':gist_record['bidirectional_links'] and all(r['languages'].get('Python',0)>0 for r in rows)}
    (ROOT/'hardening-verification(防封加固验收).json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('HARDENING', 'PASSED' if result['complete'] else 'INCOMPLETE', json.dumps(gist_record),flush=True)
if __name__=='__main__':main()
