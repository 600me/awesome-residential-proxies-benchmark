#!/usr/local/bin/python3
import collections,datetime,json,shutil
from pathlib import Path
ROOT=Path(__file__).parent
REPORT=Path('/Users/a600/project-hub(项目设计实施)/kais-business-findings(生意发现记录)/cps-live-hijack-benchmarks-20261026(海外CPS活体截流同行拆解报告).md')
SCAN=ROOT.parent/'competitor-hunter(同行反查器)/untapped_high_commission_brands(未占坑高佣品牌蓝海池).json'
h=json.loads((ROOT/'hardening-verification(防封加固验收).json').read_text());s=json.loads(SCAN.read_text());e=json.loads((ROOT/'expansion-verification(扩铺与报告验收).json').read_text())
header='## 五、 实战防封体检、未占坑蓝海品牌排行榜与扩盘准备清单'
text='\n\n'+header+'\n\n实测时间：'+datetime.datetime.now(datetime.timezone.utc).isoformat()+'。本章是当前执行状态，未完成项不以脚本退出码或本地文件代替发布成功。\n\n'
text+='### 5 大仓库匿名索引体检与可运行 Python\n\n全部使用无 Cookie GET 首页；indexable 仅指本次响应未出现 noindex/none，不代表 Google 收录、排名或防封保证。增加的是可独立使用的真实预算工具，不是免于平台审核的证明。所有参数均由使用者输入，不硬编码未经核实的实时报价。\n\n| 仓库 | 首页HTTP | robots meta | indexable | 脚本HTTP | Python字节 | 行数 | 本地测试退出码 |\n|---|---:|---|---|---:|---:|---:|---:|\n'
for r in h['results']:
 text+=f'| [{r["repository"].split("/")[-1]}]({r["repository"]}) | {r["public_http"]} | {r["robots_meta"] or "未发现"} | {str(r["indexable"]).lower()} | [{r["script_http"]}]({r["script_url"]}) | {r["languages"].get("Python",0)} | {r["lines"]} | {r["test_exit_code"]} |\n'
text+='\n统一算术检验：100单位×$0.50+$10月基础费=$60/月；加$100一次性费用，首年$820；年基础报价$100时首年$800。仅依赖Python标准库。\n\n'
g=h['index_gist']
text+=f'汇总Gist：{g.get("url") or "未发布"}；双向索引：{g["bidirectional_links"]}。'
if g.get('error'):text+='阻塞：'+g['error']+'；现有令牌权限为 public_repo，缺少 gist。'
text+='\n\n### 33 品牌 Google 首页排行榜\n\n实际候选池是33个品牌、66组查询。美国地区参数、英文、关闭个性化参数，AI Chrome CDP抓取每组最多10个自然结果，两组按URL去重统计；GitHub含Gist，寄生平台只计Knowt/LinkedIn/Medium/Reddit/Google Sites。绿色=样本内0个指定平台结果；黄色=1至3；红色=4个以上。颜色不表示搜索量、商业可行性或已经确认同一同行控制；传统优惠网站仍可能竞争很强。抓取不完整标未知，不当零。全部本次标签已在finally关闭。\n\n'
text+='| 品牌 | 竞争标记 | GitHub | 寄生平台 | 主要域名 | 官方佣金及限制 | 行动优先级 |\n|---|---|---:|---:|---|---|---|\n'
rows=sorted(s['brands'],key=lambda r:(r['github_count'] is None,(r['github_count'] or 0)+(r['parasite_count'] or 0),r['brand']))
for r in rows:
 rate=r['commission_rate'] or '未知，未核实现金CPS条款'
 if r.get('commission_sources'):rate+=' '+ ' '.join(f'[来源{i+1}]({u})' for i,u in enumerate(r['commission_sources']))
 text+=f'| {r["brand"]} | {r["competition_level"]} | {r["github_count"] if r["github_count"] is not None else "未知"} | {r["parasite_count"] if r["parasite_count"] is not None else "未知"} | {", ".join(r["top_domains"][:4])} | {rate} | {r["action_priority"]} |\n'
valid=sum(q['valid'] for b in s['brands'] for q in b['queries'])
text+=f'\n成功查询：{valid}/66。官方佣金有来源20/33；其余保留未知。本次未验证任一新联盟账户的可提现状态，也未把用户消费赠金或主机出租收入当作CPS现金收入。完整结果、查询URL、逐项排名及抓取时间见[{SCAN.name}]({SCAN})。\n'
for b in s['brands']:
 for q in b['queries']:
  if not q['valid']:text+=f'\n- 未完成：`{q["query"]}`，HTTP {q.get("http_status")}；错误 {q.get("error", "unknown").splitlines()[0]}。\n'
text+='\n### 第二载体 Gist 与归因链路\n\n选择已激活的代表品牌Decodo与Vast.ai，正文加入可复现预算命令，与原仓文章形成用途区分。现有Gemini原稿保留，替换独立CTA归因；新Gemini复核有实质回应，但另一次成文调用response为空，不冒充得到新稿。\n'
for r in e['pages']:
 text+=f'\n**{r["brand"]}**：公网Gist：{r["gist_url"] or "未发布，权限阻塞"}；HTTP：{r["public_http"] or "未取得"}。可审阅正文：[{Path(r["local_file"]).name}]({r["local_file"]})。\n\n'
 for c in r['gateway_checks']:text+=f'- `{c["url"]}` → HTTP {c["http_status"]}；Location：`{c["location"]}`；独立归因参数保留：{c["attribution_preserved"]}。\n'
text+='\n上述8次跳转均为操作者QA请求，不能计作真实获客或收益。公开Gist未发布时，不存在可声称HTTP 200的Gist链接。\n\n### 后续百仓扩张准备清单（仅准备，未执行）\n\n- 账号采购隔离：本次未采购账号、未新增营销仓。后续先核验账号来源、所有权和平台条款；付款逐次确认。隔离项目凭据与现有业务，账号隔离不构成规避封禁的方案。\n- 短链维护：保留清晰目的地与联盟披露，逐CTA检查302及商家支持的归因字段；HTTP正常不代表佣金获批。不以换域名承诺防封。\n- 联盟审查：先确认账号批准、流量来源、优惠站准入、码传播权限和现金提现门槛。[ScraperAPI条款](https://www.scraperapi.com/affiliate-terms/)要求优惠站人工审批且费率另定；[Evoxt条款](https://evoxt.com/terms-of-service/)限制优惠码站传播。\n- 内容与扩张：以真实可用工具、完整算例、有效官方依据和清晰联盟披露为基础；未验证的代码优惠、基准性能、排名、销量均不宣称。百仓只是待准备范围，本工单未执行扩张。\n- 当前实际阻塞：指定GitHub令牌缺少gist权限；入口 https://github.com/settings/tokens 。Google限流查询待恢复后重抓，未知字段不得补零。\n'
b=ROOT/'backups(发布前备份)'/('report-'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'.md');shutil.copy2(REPORT,b)
old=REPORT.read_text();old=old.split('\n\n'+header)[0]
REPORT.write_text(old+text)
assert header in REPORT.read_text() and all(r['brand'] in REPORT.read_text() for r in rows)
e.update(report_path=str(REPORT),report_written=True,search_success_count=valid,search_expected_count=66,all_work_complete=h['complete'] and e['complete'] and s['complete'])
(ROOT/'expansion-verification(扩铺与报告验收).json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
print('REPORT UPDATED',REPORT,'overall_complete',e['all_work_complete'])
