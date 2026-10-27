#!/usr/local/bin/python3
import concurrent.futures,datetime,importlib.util,json,re
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import requests
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('hardening',ROOT/'harden-publish(测算器发布验收).py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
def check(url):
 r=requests.get(url,allow_redirects=False,timeout=35)
 location=r.headers.get('Location','');src=parse_qs(urlparse(url).query)['src'][0]
 values=[v for vals in parse_qs(urlparse(location).query).values() for v in vals]
 assert r.status_code==302 and src in values,(url,r.status_code)
 return {'url':url,'http_status':r.status_code,'location':location,'attribution_preserved':True,'traffic_type':'operator QA, not human acquisition'}
def main():
 assert h.api('GET','/user')['login'].lower()=='600me'
 rows=[]
 for d,brand,repo,script in [('decodo-smartproxy','decodo','decodo-smartproxy-pricing-coupons','smartproxy_calculator.py'),('vastai','vastai','vastai-gpu-pricing-coupons','vastai_gpu_calculator.py')]:
  content=(ROOT/d/'README.md').read_text()
  content=re.sub('src=gh_coupon_'+brand+r'_cta([1-4])',r'src=gist_coupon_'+brand+r'_cta\1',content)
  content+='\n\n## Reproduce the budget before choosing a plan\n\n'
  content+=f'[Download the zero-dependency Python calculator](https://github.com/600me/{repo}/blob/main/{script}). All rates in the command below are hypothetical USD inputs, not a live offer.\n\n'
  if brand=='decodo':
   content+=f'```sh\npython3 {script} --units 10 --unit-rate 4\npython3 {script} --units 10 --included 10 --unit-rate 4 --base 35\n```\n\nThe first scenario costs $40/month or $480/year. The second costs $35/month or $420/year. The $60 difference assumes identical usage for twelve months and excludes tax and other charges. Confirm the actual allowance, excess rate and expiry rules before treating the second scenario as a purchasable package.\n'
  else:
   content+=f'```sh\npython3 {script} --units 150 --unit-rate 0.30\npython3 {script} --units 100 --unit-rate 0.40\n```\n\nThe first scenario costs $45/month or $540/year; the second costs $40/month or $480/year. These are assumed billed hours, not benchmark results. The first scenario assumes fifty extra hours from restarts or setup. Checkpoint behavior and your measured workload determine whether that assumption is useful.\n'
  filename=brand+'-coupon-code-cost-breakdown.md';(ROOT/d/filename).write_text(content)
  links=re.findall(r'https://go\.272738\.xyz/[^\s)]+',content)
  assert len(links)==4 and len(set(links))==4
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:checks=list(pool.map(check,links))
  row={'brand':brand,'local_file':str(ROOT/d/filename),'cta_count':4,'gateway_checks':checks,'gist_url':None,'public_http':None,'copy_source':'Existing Gemini-authored approved full buying guide, CTA attribution replacement and reproducible calculator appendix; no new unverified price claim.'}
  found=None
  for page in range(1,11):
   batch=h.api('GET',f'/gists?per_page=100&page={page}')
   found=next((g for g in batch if filename in g['files']),None)
   if found or len(batch)<100:break
  data={'description':brand+' independent coupon and cost breakdown with runnable calculator','files':{filename:{'content':content}}}
  try:
   gist=h.api('PATCH','/gists/'+found['id'],data) if found else h.api('POST','/gists',{**data,'public':True})
   assert gist['public']
   live=h.api('GET','/gists/'+gist['id'])
   assert live['files'][filename]['content']==content
   public=requests.get(gist['html_url'],timeout=35);assert public.status_code==200
   row.update(gist_url=gist['html_url'],public_http=200,readback_equal=True)
  except RuntimeError as exc:row['blocker']=str(exc)+'; designated token scope public_repo lacks gist'
  rows.append(row);print(brand,'CTA PASS','PUBLISHED' if row['gist_url'] else 'PUBLICATION BLOCKED',flush=True)
 out={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':rows,'complete':all(r['public_http']==200 for r in rows),'new_repositories_created':0,'forum_posts':0,'new_spend':0,'gist_creation_blocker':'Existing token lacks gist scope; scope update required' if any(not r['gist_url'] for r in rows) else None}
 (ROOT/'expansion-verification(扩铺与报告验收).json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
