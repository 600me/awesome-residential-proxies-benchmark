#!/usr/local/bin/python3
import base64, datetime, importlib.util, json, re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('publisher',ROOT/'publish-verify(发布与验收).py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
REPORT=Path('/Users/a600/project-hub(项目设计实施)/kais-business-findings(生意发现记录)/cps-live-hijack-benchmarks-20261026(海外CPS活体截流同行拆解报告).md')
LICENSE='''MIT License

Copyright (c) 2026 Kais

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
def get(path,missing=False):
    r=p.s.get('https://api.github.com'+path,timeout=45)
    if missing and r.status_code==404:return None
    assert r.status_code==200,(path,r.status_code)
    return r.json()
def put(path,raw,old):
    if old and base64.b64decode(old['content'])==raw:return
    data={'message':'Add CTA position attribution and MIT license','content':base64.b64encode(raw).decode()}
    if old:data['sha']=old['sha']
    p.api('PUT',path,data)
def check(raw,base):
    urls=re.findall(r'https://go\.272738\.xyz/[^\s)]+',raw.decode())
    assert urls==[base+'_cta'+str(i) for i in range(1,5)],urls
    return urls

def main():
    assert get('/user')['login'].lower()=='600me'
    backup=ROOT/'backups(发布前备份)'/datetime.datetime.now().strftime('audit-%Y%m%dT%H%M%S')
    backup.mkdir(parents=True)
    (backup/'report.md').write_bytes(REPORT.read_bytes())
    prepared=[]
    for d,repo,g,src in p.ITEMS:
        path='/repos/600me/'+repo
        assert get(path)['private'] is False
        old=get(path+'/contents/README.md');lic=get(path+'/contents/LICENSE',True)
        local=ROOT/d/'README.md';raw=local.read_bytes()
        (backup/(d+'-README.md')).write_bytes(raw)
        (backup/(d+'-remote.json')).write_text(json.dumps({'readme':old,'license':lic}))
        assert base64.b64decode(old['content'])==raw,(repo,'local/remote divergence')
        base=f'https://go.272738.xyz/{g}?src=gh_coupon_{src}'
        pattern=re.escape(base)+r'(?:_cta[1-4])?(?=\))'
        matches=list(re.finditer(pattern,raw.decode()));assert len(matches)==4
        count=iter(range(1,5))
        new=re.sub(pattern,lambda m:base+'_cta'+str(next(count)),raw.decode()).encode()
        urls=check(new,base)
        prepared.append((d,repo,path,local,new,old,lic,base,urls))
    for d,repo,path,local,new,old,lic,base,urls in prepared:
        local.write_bytes(new);(ROOT/d/'LICENSE').write_text(LICENSE)
        put(path+'/contents/README.md',new,old)
        put(path+'/contents/LICENSE',LICENSE.encode(),lic)
        print('UPDATED '+repo,flush=True)
    def gateway(url):
        r=requests.get(url,allow_redirects=False,timeout=40)
        assert r.status_code==302,(url,r.status_code)
        assert r.headers.get('Location'),url
        return {'url':url,'http':302,'location':r.headers['Location']}
    results=[]
    for d,repo,path,local,new,old,lic,base,urls in prepared:
        check(local.read_bytes(),base)
        remote=base64.b64decode(get(path+'/contents/README.md')['content'])
        assert remote==new;check(remote,base)
        assert base64.b64decode(get(path+'/contents/LICENSE')['content'])==LICENSE.encode()
        with ThreadPoolExecutor(max_workers=4) as pool: redirects=list(pool.map(gateway,urls))
        results.append({'repository':'https://github.com/600me/'+repo,'local_cta_positions':[1,2,3,4],'readme_http':200,'readback_equal':True,'license_http':200,'license_exact':True,'redirects':redirects})
    original='- 本轮只更新报告、读取公开网页并执行文件验收；未注册、未发布、未购买。'
    statement='- 工序3已于 2026-10-26 全量发布 5 个 GitHub 公开截流仓，网关 302 重定向全部实测生效。'
    report=REPORT.read_text();assert original in report or statement in report
    report=report.replace(original,statement)
    marker='\n### DS v4.1 审计整改：公开仓库与 302 参数\n'
    report=report.split(marker)[0]+marker+'\n四个位置依次对应 Top Banner、Pricing Table、Checkout Step、Footer。下列 20 条链接均重新实测 HTTP 302；目标地址为响应 Location。\n'
    for row in results:
        report+='\n- 仓库：'+row['repository']+'\n'
        for red in row['redirects']:report+='  - `'+red['url']+'` → HTTP 302；Location：`'+red['location']+'`\n'
    REPORT.write_text(report)
    assert statement in REPORT.read_text() and original not in REPORT.read_text()
    result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report_updated':True,'results':results,'exit_code':0}
    (ROOT/'audit-verification(审计整改验收).json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
