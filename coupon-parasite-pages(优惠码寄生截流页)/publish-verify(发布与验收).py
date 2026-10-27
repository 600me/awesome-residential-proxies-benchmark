#!/usr/local/bin/python3
import argparse,base64,datetime,json,re,subprocess,time
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
ITEMS=[('scraperapi','scraperapi-pricing-coupons','scraperapi','scraperapi'),('decodo-smartproxy','decodo-smartproxy-pricing-coupons','smartproxy','decodo'),('firstbase','firstbase-promo-code-pricing','firstbase','firstbase'),('runpod','runpod-gpu-pricing-coupons','runpod','runpod'),('vastai','vastai-gpu-pricing-coupons','vastai','vastai')]
secret=Path('/Users/a600/.secrets(密钥)/github-token(GitHub发帖令牌).env').read_text()
m=re.search(r'^(?:export\s+)?GITHUB_TOKEN\s*=\s*(.+?)\s*$',secret,re.M)
assert m,'GITHUB_TOKEN missing'
token=m.group(1).strip().strip('\"\'')
s=requests.Session();s.headers.update({'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
def api(method,path,data=None,missing=False):
    r=s.request(method,'https://api.github.com'+path,json=data,timeout=45)
    if missing and r.status_code==404:return None
    if not r.ok:raise RuntimeError(f'{method} {path}: HTTP {r.status_code}')
    return r.json()
def localcheck(d,g,src):
    p=ROOT/d/'README.md';assert p.is_file(),str(p)
    raw=p.read_bytes();assert len(raw)>=2500,(d,len(raw))
    text=raw.decode();url=f'https://go.272738.xyz/{g}?src=gh_coupon_{src}'
    assert text.count(url)==4,(d,'CTA count',text.count(url))
    assert len(re.findall(r'\[[^\]]+\]\('+re.escape(url)+r'\)',text))==4,(d,'anchor count')
    assert text.startswith('# '),(d,'H1')
    return raw,url

def main():
    args=argparse.ArgumentParser();args.add_argument('--publish',action='store_true');args=args.parse_args()
    meta=json.loads((ROOT/'pages(页面资料).json').read_text())['pages']
    for d,repo,g,src in ITEMS:
        localcheck(d,g,src)
        topics=meta[d]['topics'];assert len(topics)>=5
        assert {'coupon-code','promo-code','pricing'}.issubset(topics)
        assert all(re.fullmatch('[a-z0-9][a-z0-9-]{0,49}',t) for t in topics)
        assert 0<len(meta[d]['description'])<=350
    assert api('GET','/user')['login'].lower()=='600me','Token owner mismatch'
    for d,repo,g,src in ITEMS:
        raw,url=localcheck(d,g,src);path='/repos/600me/'+repo
        existing=api('GET',path,missing=True)
        if args.publish:
            old=api('GET',path+'/contents/README.md',missing=True) if existing else None
            if existing:
                backup=ROOT/'backups(发布前备份)'/repo;backup.mkdir(parents=True,exist_ok=True)
                stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
                (backup/(stamp+'.json')).write_text(json.dumps({'repository':existing,'readme':old},ensure_ascii=False,indent=2))
                assert not existing['private'],'Existing private repo: refuse unrequested disclosure'
                api('PATCH',path,{'description':meta[d]['description']})
            else:
                api('POST','/user/repos',{'name':repo,'description':meta[d]['description'],'private':False,'auto_init':False})
            encoded=base64.b64encode(raw).decode()
            if not old or base64.b64decode(old['content'])!=raw:
                payload={'message':'Publish source-checked pricing and coupon guide','content':encoded}
                if old:payload['sha']=old['sha']
                api('PUT',path+'/contents/README.md',payload)
            api('PUT',path+'/topics',{'names':meta[d]['topics']})
            print('PUBLISHED',repo,flush=True)
    results=[]
    for d,repo,g,src in ITEMS:
        raw,url=localcheck(d,g,src);path='/repos/600me/'+repo
        info=api('GET',path)
        assert info['owner']['login'].lower()=='600me' and not info['private'],repo
        assert info['description']==meta[d]['description'],(repo,'description')
        assert set(api('GET',path+'/topics')['names'])==set(meta[d]['topics']),(repo,'topics')
        remote=api('GET',path+'/contents/README.md')
        assert base64.b64decode(remote['content'])==raw,(repo,'readback')
        public='https://github.com/600me/'+repo
        for attempt in range(4):
            r=requests.get(public,timeout=45)
            if r.status_code==200:break
            time.sleep(2)
        assert r.status_code==200,(repo,'public',r.status_code)
        assert url.replace('&','&amp;') in r.text,(repo,'rendered CTA')
        headers=subprocess.run(['curl','-sS','-I','--max-time','30',url],capture_output=True,text=True,check=True).stdout
        codes=re.findall(r'^HTTP/\S+\s+(\d+)',headers,re.M)
        assert codes and codes[-1]=='302',(repo,'gateway',codes)
        location=re.findall(r'^location:\s*(.+)',headers,re.M|re.I)
        assert location,(repo,'redirect location missing')
        row={'repository':public,'gateway':url,'local_bytes':len(raw),'cta_count':4,'public_http':200,'gateway_http':302,'readback_equal':True,'description_verified':True,'topics_verified':True}
        results.append(row);print('PASS',json.dumps(row),flush=True)
    (ROOT/'verification(验收结果).json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'exit_code':0},indent=2))
    print('ALL ASSERTIONS PASSED (5/5)',flush=True)
if __name__=='__main__':main()
