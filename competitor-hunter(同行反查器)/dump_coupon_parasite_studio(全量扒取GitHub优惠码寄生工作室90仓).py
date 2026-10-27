#!/usr/bin/env python3
"""Read-only GitHub fingerprint inventory; requires the locally installed requests."""
import base64, collections, concurrent.futures as cf, datetime as dt, html, json, re, time
from pathlib import Path
from urllib.parse import urlparse, urljoin, parse_qsl
import requests

OUT = Path(__file__).with_name('coupon_parasite_studio_full_inventory(优惠码寄生工作室全量选品与链接池).json')
SECRET = Path('/Users/a600/.secrets(密钥)/github-token(GitHub发帖令牌).env')
QUERIES = ['"Pricing Breakdown" "Promo Code"', '"Coupon Code" "Pricing Breakdown"', '"Pricing Analysis" "Promo Code"', '"Coupon Code Guide" "Pricing"', '"Coupon Code" "Pricing"']
SHORT = {'bit.ly','bitly.com','tinyurl.com','t.co','t.ly','shorturl.at','rebrand.ly','cutt.ly','rb.gy','is.gd','goo.gl','buff.ly','ow.ly','s.id'}
AFF = re.compile(r'^(?:fp_ref|ref|referral|referral_code|refcode|aff|affid|aff_id|affiliate|affiliate_id|via|r|invite|invite_code|irclickid|clickid|partner|partner_id|coupon|promo|promo_code|aid)$',re.I)
TOKEN = None

def api(path, params=None):
    for attempt in range(7):
        r = requests.get('https://api.github.com'+path, params=params, headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/vnd.github+json','User-Agent':'public-coupon-inventory'},timeout=40)
        if r.status_code in (403,429) or r.status_code >= 500:
            delay = min(65,max(3, int(r.headers.get('X-RateLimit-Reset',time.time()+5))-int(time.time())+1))
            print('API retry',r.status_code,'wait',delay,flush=True); time.sleep(delay); continue
        r.raise_for_status(); return r.json()
    raise RuntimeError('GitHub API retries exhausted: '+path)

def search(q, records, evidence):
    page=1
    while True:
        data=api('/search/repositories',{'q':q,'per_page':100,'page':page,'sort':'updated','order':'desc'})
        if data.get('incomplete_results'):
            time.sleep(3); data=api('/search/repositories',{'q':q,'per_page':100,'page':page,'sort':'updated','order':'desc'})
            if data.get('incomplete_results'): raise RuntimeError('Incomplete search: '+q)
        if data['total_count']>1000:
            raise RuntimeError('Search requires partitioning: '+q)
        evidence.append({'query':q,'page':page,'total_count':data['total_count'],'returned':len(data['items']),'incomplete_results':data['incomplete_results']})
        for x in data['items']:
            k=x['full_name']
            if k not in records:
                records[k]={key:x.get(key) for key in ('full_name','created_at','updated_at','pushed_at','description','html_url','default_branch')}
                records[k].update(owner=x['owner']['login'],stars=x['stargazers_count'],forks=x['forks_count'],matched_queries=[])
            if q not in records[k]['matched_queries']: records[k]['matched_queries'].append(q)
        print('Search',q,'page',page,'total',data['total_count'],'unique',len(records),flush=True)
        if page*100>=data['total_count']: break
        page+=1; time.sleep(2.1)

def readme(repo):
    raw='https://raw.githubusercontent.com/'+repo['full_name']+'/'+repo['default_branch']+'/README.md'
    try:
        r=requests.get(raw,timeout=25)
        if r.status_code==200: body=r.text; source=raw
        else:
            d=api('/repos/'+repo['full_name']+'/readme'); body=base64.b64decode(d['content']).decode('utf-8',errors='replace');source=d['html_url']
        urls=sorted(set(html.unescape(u).rstrip('.,;:!?') for u in re.findall(r'https?://[^\s<>\[\]"\x27`\)]+',body)))
        repo.update(readme={'status':'ok','source':source,'text':body},external_links=[u for u in urls if urlparse(u).hostname not in {'github.com','raw.githubusercontent.com','githubusercontent.com'}])
    except Exception as e: repo.update(readme={'status':'error','error':type(e).__name__},external_links=[])
    return repo

def resolve(url):
    chain=[]; current=url; seen=set()
    try:
        for _ in range(12):
            if current in seen: return {'source':url,'chain':chain,'final_url':current,'resolved':False,'error':'redirect_loop'}
            seen.add(current)
            if urlparse(current).scheme not in ('http','https'): raise ValueError('non HTTP redirect')
            r=requests.head(current,allow_redirects=False,timeout=15,headers={'User-Agent':'Mozilla/5.0'})
            if not r.is_redirect:
                r.close();r=requests.get(current,allow_redirects=False,timeout=15,stream=True,headers={'User-Agent':'Mozilla/5.0'})
            loc=r.headers.get('Location');status=r.status_code;r.close()
            chain.append({'url':current,'http_status':status,'location':loc})
            if status in (301,302,303,307,308) and loc: current=urljoin(current,loc);continue
            return {'source':url,'chain':chain,'final_url':current,'final_domain':urlparse(current).hostname,'resolved':status<400 and urlparse(current).hostname not in SHORT}
        return {'source':url,'chain':chain,'final_url':current,'resolved':False,'error':'hop_limit'}
    except Exception as e: return {'source':url,'chain':chain,'final_url':current,'resolved':False,'error':type(e).__name__}

def brand(repo):
    name=repo['full_name'].split('/')[1].lower()
    text=(name+' '+(repo.get('description') or '')).lower()
    aliases={'bandwagonhost':['bandwagonhost','bandwagon host','bandwagon'], 'zgocloud':['zgocloud','zgovps'], 'gomami':['gomami','go-mami','go mami'], 'extravm':['extravm','extra-vm'], 'linuxfoundation':['linuxfoundation','linux foundation']}
    known=['scraperapi','vultr','gthost','evoxt','nordvpn','digitalocean','hostinger','hostdare','aragon','artistly','dataimpulse','pikpak','mangools','lisahost','dmit','holafly','vmiss','nfvideo','elevenlabs','revid','hoka','zappos','nuuly','oliveyoung','squarespace','bitdefender','babylovegrowth','ourdream']
    for b in known: aliases.setdefault(b,[b])
    # Prefer explicit merchant in repository name, then description. No generic project name becomes a brand.
    for source in (name,text):
        matches=[b for b,terms in aliases.items() if any(t in source for t in terms)]
        if matches: return matches[0]
    m=re.match(r'^(.+?)-(?:coupon|promo|discount)(?:-|$)',name)
    if m and m.group(1) not in {'active','github','magento2','m2','cart','spree','coupon'}:
        return re.sub('[^a-z0-9]','',m.group(1))
    return 'unclassified'

def main():
    global TOKEN
    import shlex
    for line in SECRET.read_text().splitlines():
        m=re.match(r'\s*(?:export\s+)?GITHUB_TOKEN\s*=\s*(.*)',line)
        if m: TOKEN=shlex.split(m.group(1),comments=True)[0];break
    if not TOKEN: raise RuntimeError('Missing GITHUB_TOKEN')
    repos={};evidence=[]
    for q in QUERIES: search(q,repos,evidence);time.sleep(2.1)
    with cf.ThreadPoolExecutor(max_workers=12) as pool:
        results=list(pool.map(readme,repos.values()))
    print('README fetched',len(results),flush=True)
    urls=sorted({u for r in results for u in r['external_links']})
    shorts=[u for u in urls if (urlparse(u).hostname or '').removeprefix('www.') in SHORT]
    with cf.ThreadPoolExecutor(max_workers=16) as pool:
        redirects=list(pool.map(resolve,shorts))
    lookup={x['source']:x for x in redirects}; groups={};params=[]
    for r in results:
        b=brand(r);r['target_brand']=b;r['brand_basis']='explicit merchant alias in name/description, otherwise coupon-name prefix; unclassified is not a merchant'
        g=groups.setdefault(b,{'brand':b,'repositories':[],'owners':set(),'affiliate_parameters':{},'activity_2026_09_10':[]})
        g['repositories'].append(r['full_name']);g['owners'].add(r['owner']);r['affiliate_links']=[]
        for u in r['external_links']:
            red=lookup.get(u); candidates=[u]+([h['url'] for h in red['chain']]+[red['final_url']] if red else [])
            for link in dict.fromkeys(candidates):
                parsed=urlparse(link)
                pairs=[{'name':k,'value':v} for k,v in parse_qsl(parsed.query,keep_blank_values=True) if AFF.match(k)]
                pathmatch=re.search(r'/(?:aff(?:iliate)?|ref(?:erral)?|invite|r)/([^/?#]+)',parsed.path,re.I)
                if pathmatch:pairs.append({'name':'path_referral','value':pathmatch.group(1)})
                if not pairs:continue
                item={'source_url':u,'observed_url':link,'domain':parsed.hostname,'parameters':pairs,'via_shortlink':bool(red),'redirect_resolved':red['resolved'] if red else None}
                r['affiliate_links'].append(item)
                for p in pairs:
                    key=(parsed.hostname,p['name'],p['value']); params.append(key)
                    entry=g['affiliate_parameters'].setdefault(key,{'domain':parsed.hostname,**p,'repositories':set()});entry['repositories'].add(r['full_name'])
        activity={k:r[k] for k in ('created_at','updated_at','pushed_at') if r.get(k) and '2026-09-01'<=r[k]<'2026-11-01'}
        if activity:g['activity_2026_09_10'].append({'repository':r['full_name'],**activity})
    for g in groups.values():
        g['repository_count']=len(g['repositories']);g['owners']=sorted(g['owners'])
        g['affiliate_parameters']=sorted([{**v,'repositories':sorted(v['repositories']),'repository_count':len(v['repositories'])} for v in g['affiliate_parameters'].values()],key=lambda v:-v['repository_count'])
    summary={'repository_count':len(results),'brand_count':len([b for b in groups if b!='unclassified']),'unclassified_repository_count':len(groups.get('unclassified',{}).get('repositories',[])),'owner_count':len({r['owner'] for r in results}),'readme_success_count':sum(r['readme']['status']=='ok' for r in results),'external_url_count':len(urls),'shortlink_count':len(shorts),'resolved_shortlink_count':sum(x['resolved'] for x in redirects),'unique_affiliate_parameter_count':len(set(params)),'shortlink_derived_parameter_count':len({(x['domain'],p['name'],p['value']) for r in results for x in r['affiliate_links'] if x['via_shortlink'] and x['observed_url']!=x['source_url'] for p in x['parameters']})}
    payload={'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'All paginated results for the five requested GitHub repository fingerprints; common ownership is unverified. Brand labels use explicit merchant aliases in names/descriptions or coupon-name prefixes; unclassified is not a merchant. Referral parameters are observed strings, not proof of payout validity. Activity uses GitHub repository timestamps, not inferred sales.','summary':summary,'searches':evidence,'brands':sorted(groups.values(),key=lambda x:-x['repository_count']),'repositories':sorted(results,key=lambda x:x['full_name']),'shortlink_resolutions':redirects}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    check=json.loads(OUT.read_text());assert check['summary']['repository_count']>=80,'Fewer than 80 real matches';assert params and groups
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
    print('JSON:',OUT,flush=True)

if __name__=='__main__': main()
