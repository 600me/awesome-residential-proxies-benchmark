#!/usr/bin/env python3
"""Assemble the source-bound research report without upgrading promotion to sales."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPORT=Path('/Users/a600/project-hub(项目设计实施)/kais-business-findings(生意发现记录)/cps-live-hijack-benchmarks-20261026(海外CPS活体截流同行拆解报告).md')
rows=json.loads((ROOT/'live_cps_operator_candidates(同行候选证据).json').read_text())[:5]
cases=[
 dict(offer='Hostinger Website Builder / WordPress hosting',price='官方 Premium 当前展示 $2.49/月，48 个月预付合计 $119.52，续费 $10.99/月；这是公开套餐价，不是该同行真实订单客单价。',commission='官方基础佣金从合资格销售额的 40% 起，随销量增加；不能据此声称 Metics 的私下协议也是 40%。',offer_sources=['https://www.hostinger.com/pricing','https://www.hostinger.com/affiliates'],keywords=['Hostinger website builder tutorial','Hostinger WordPress tutorial','Hostinger discount'],traffic='YouTube @MeticsMedia → deals.meticsmedia.com 分类优惠页 → meticsmedia.com/hostinger-deal-websitebuilder。页面提供 Tutorial 与 Get Deal 两种出口。',bridge='首屏标题、58 个优惠搜索框、多分类筛选、三列产品卡、折扣标签、主行动按钮与教程次按钮。',sale='未找到可归属该主体的最近30天订单/佣金证据；优惠页在线、推荐卡存在均不等于出单。',activity='页面本次 HTTP 200；未取得最近30天内容发布日期证据。',observed='页面明确说明优惠链接支持频道；未观察到小号互顶、删帖规避或绕过审核证据。',actions=[('搜索入口','围绕教程里实际演示的单一任务建立标题；本次只有关键词推断，没有该频道搜索流量后台。'),('中转布局','参考截图的搜索框、分类标签、三列卡片顺序；保留既有四计算器，不另建优惠门户。'),('痛点算例','以1000次成功请求成本展示失败重试损耗；只填实测或明确假设。'),('行动出口','卡片主按钮指向现有对应计算器，次按钮指向开源工具；标注维护者与联盟关系。')]),
 dict(offer='LiveChat / Text',price='官方定价页本次展示 Essential $19/user/month、Growth $79/user/month；计费周期及具体套餐以结账为准，不能还原同行历史客单价。',commission='官方帮助页：起始20%持续佣金，带来5个付费客户后新许可证22%；该主体的实际合同档位未公开。',offer_sources=['https://www.livechat.com/pricing/','https://partners.livechat.com/help/affiliate-commission/','https://partners.livechat.com/blog/tooltester-success-story/'],keywords=['LiveChat review','best live chat software','LiveChat alternatives'],traffic='Robert Brandl 创建的独立评测团队 Tooltester；独立评测页 → /out/livechat → livechat.com/try-livechat/?a=TeV6VODDJ9，能对应同一推广标识。',bridge='左侧评分和优缺点，右侧长评测、作者/更新日期、视频、功能分节、价格比较、反复出现试用按钮。',sale='官方伙伴案例记载九年累计超过300个订阅转化，属于历史实证；没有最近30天订单，因此不计入近期活跃出单合格数。',activity='页标题含2026，但页面可见更新日期为2025-10-10；标题年份不当成最近更新证据。',observed='评测页有联盟披露并呈现缺点；未核实其在 Reddit 的发布策略，也不能保证同样格式不会被删除。',actions=[('搜索入口','单一offer review词 → 对比长文 → 计算器，不冒充该主体或引用其私有成绩。'),('中转布局','按左评分栏/右正文的阅读顺序拆解；像素参考见下表，现有网站本轮不改。'),('可信信息','将价格、更新日期、适合/不适合场景并排呈现，不用年份替代更新证据。'),('行动出口','以现有计算器给用户自行代入的操作出口；渠道参数独立归因。')]),
 dict(offer='ScalaHosting Entry Cloud / Managed VPS',price='该主体带标识落地页本次显示 Entry Cloud $10.65/月促销，续费 $39.95/月；有36M/12M/1M选项，未核实所选周期，因此不推算预付订单总额。',commission='官方联盟页宣传每单最高$500，属于固定/协商奖励，不是统一百分比；Tom 的实际协议未公开。',offer_sources=['https://www.scalahosting.com/affiliate.html','https://www.scalahosting.com/OMM-cloud-servers.html?promocode=OMM10#onlinemediamasters','https://onlinemediamasters.com/how-to-make-money-with-affiliate-marketing/'],keywords=['ScalaHosting review','Cloudways alternatives','WordPress hosting CPU limits'],traffic='Tom Dupuis / OnlineMediaMasters 技术长文 → ScalaHosting OMM 专属套餐页；a_aid=onlinemediamasters 和 #onlinemediamasters 等公开标识对应该主体。',bridge='具体CPU/资源限制切题，评测图、资源表、价格与续费分节、迁移入口，长文内嵌多个同一商家链接。',sale='2026-10-03更新的作者文章自述年收入约$150k、往年黑五$14k；这是作者自述及历史数字，不等于已核验最近30天成交。',activity='收入文章可见近期更新；该主体收入来源与本篇当前offer的逐单对应关系仍未知。',observed='作者公开联盟披露；其收入文章写到因负面评价失去部分合作资格，不能据此承诺“防封”。',actions=[('搜索入口','从具体计费/资源问题进入，而不是泛化best工具清单。'),('中转布局','参考800px正文容器和40px标题的技术长文结构；不复制作者图片或测试结果。'),('痛点算例','把GPU加载小时或代理失败请求列入成本，不把标价差等同实际省钱。'),('行动出口','指向现有成本计算器；若无自己测量的数据，明确标假设。')]),
 dict(offer='Verpex VPS-D4',price='官方VPS页：12个月首次优惠$10/月，续费$19.99/月；2 vCPU、4GB RAM、80GB NVMe；实际订单税费及附加项未知。',commission='官方表中 Resellers/Unmanaged Servers 按月推荐量为$60/$80/$100/$120固定奖励，Managed Servers为$100/$120/$150/$200；Tony该具体交易适用档位未公开。',offer_sources=['https://verpex.com/vps-hosting','https://affiliates.verpex.com/affiliates/'],keywords=['self hosted website stack one VPS','Docker Compose Ghost Matomo Uptime Kuma','Verpex VPS D4'],traffic='Tony Teaches Tech 的同名技术站/视频体系 → 可执行Docker教程 → blog.ttt.do/VerpexVPS → clients.verpex.com/aff/，a_aid=ttt、chan=website-stack、data1=blog。',bridge='开头联盟披露，四组件表格，最低资源需求，采购链接放在“Get a VPS”步骤，之后为DNS/Docker/监控的实际操作。',sale='查到带作者标识的活跃推广链路；未找到最近30天可归属的成交或到账证据。',activity='正文显示2026-10-01更新和2026-07-28日期；这能支持近期内容维护，不能支持近期销量。',observed='正文开头披露可能获得佣金，先交付具体可执行教程；没有防封后台或删帖率证据。',actions=[('搜索入口','CLI如何量化403损耗，原帖问题和工具功能必须一致。'),('中转布局','参考顶部标题+左860px正文的步骤式教程；不制作空泛推荐目录。'),('交付核心','命令、参数、公式、一次采样局限必须齐全；示例金额明确是假设。'),('行动出口','GitHub工具与四计算器；不发裸AFF短链；公开说明维护者身份。')]),
 dict(offer='Base44',price='官方Starter年付折算$16/月（$192/年），Builder $40/月年付折算；文章写$29/月与当前官方页不一致，报告采用官方值。',commission='官方每个合资格付费推荐固定$100，非百分比；高表现合作方可有另行安排，最低支付阈值$300。',offer_sources=['https://base44.com/pricing','https://base44.com/affiliates'],keywords=['Base44 review 2026','Base44 vs Bubble vs Softr','AI no code client portal'],traffic='署名Abhinand PS / Emerging Tech Daily文章 → base44.pxf.io/c/3540428/2049275/25619?trafcat=base；Impact指纹直接可见。',bridge='快速结论、三产品对比表、演示步骤、适用场景与CTA；文章自称做过原型与付费工具，未独立核实这些经历。',sale='文章所称“300用户”涉及自己的工具，不是Base44联盟转化；没有近期联盟订单证据。',activity='文章标Jan 13，未取得最近30天更新或推广证据；作者页面在线不计为近期活跃。',observed='未从采集文本核实充分的联盟披露；无防封手段证据。此案例保留为反例：有指纹、有故事仍不能算成交证明。',actions=[('搜索入口','仅记录review/vs关键词结构；不采用未经证实的用户数或测试速度。'),('中转布局','参考740px正文及对比表顺序；价格必须改为有日期的官方来源。'),('痛点算例','以自己的工具可复算的金额代替“45分钟上线”等无法重现的宣称。'),('行动出口','现有无广告计算器/GitHub工具，清楚披露商业出口；不用伪造经历。')])]
report=['# 海外 CPS 双轨实证拆解报告','',
'取证日期：2026-10-26。范围：当前已启动项目的同行研究与物料交付，不是新增生意推荐。',
'','**结论：取得5个真实个人/独立团队的公开推广案例，但“5个最近30天正在出单”的硬指标未通过。以下均按证据等级标注，不能把5个案例数量当成5个合格成交主体。**',
'','轨道二：本次14组Google查询得到97个唯一Reddit候选，真实.json校验通过74个；交付精选20条，四赛道各5条。Google页截图、查询URL、排名、UTC检查时间、帖子ID和JSON哈希均已保存。排名仅是本次hl=en/gl=us/pws=0请求结果，不是长期排名或流量承诺。archived/locked为false也不保证账号具备发言资格或自动通过版规。',
'','## 证据与执行方式','',
'两个采集脚本均使用 ThreadPoolExecutor(max_workers=16)，HTTP timeout=8。普通HTTP Reddit返回403后，使用本机既有AI Chrome读取原始.json；只保存公开字段，不保存会话信息。所有新建标签均在finally关闭。Google后续指纹查询触发异常流量页，相关结果保留为失败，不把验证码页面算搜索结果；使用已找到的公开来源补充直达核验。',
'','扫描覆盖 Impact（pxf.io、sjv.io、7eer.net、irclickid）、PartnerStack/FirstPromoter（psgrow.link、ps_partner_key、fpr=、via=、fp_ref=）、ShareASale、CJ、Awin；via=仅是候选信号，已排除Twitter分享按钮误报。中转短链另做跳转核验。',
'','正文尺寸均来自1440×1000视口的DOM实测；下表是结构复刻执行表和测量值，不宣称已经复刻部署。既有四计算器保持原样。同行原有logo、截图、作者身份、销量与口碑不属于可冒用材料。','']
for i,(r,c) in enumerate(zip(rows,cases),1):
 r.update(offer=c['offer'],sales_verified=False,recent_sales_verified=False,sales_evidence_note=c['sale'],keywords=c['keywords'],offer_sources=c['offer_sources'])
 report += [f"## 案例 {i}：{r['operator']}（推广可核验，近期成交未证实）",'',f"- 主体/入口：[{r['operator']}]({r['url']})；HTTP {r.get('browser_http_status',r.get('http_status'))}。",f"- Offer：{c['offer']}。",f"- 客单价口径：{c['price']}",f"- 佣金：{c['commission']}",'- 官方/主体原始来源：'+'；'.join(f'[{u.split("/")[2]}]({u})' for u in c['offer_sources']),f"- Keywords：{', '.join(c['keywords'])}。关键词由页面标题/内容拆出；未取得真实点击查询词。",f"- 载体与链路：{c['traffic']}",f"- Bridge Page结构：{c['bridge']}",f"- 活跃性：{c['activity']}",f"- 出单证据：{c['sale']}",f"- 防封手段核验：{c['observed']}",'', '### 1:1结构/像素参考执行表','', '| 顺序 | 可复刻动作 | 客观验收 |','|---|---|---|']
 for j,(label,action) in enumerate(c['actions'],1):report.append(f'| {j}. {label} | {action} | 文案与实测/原始来源一致，点击可达；不以浏览量计成交 |')
 report+=['','| 原站元素 | x / y | width / height | 字号与字体 |','|---|---:|---:|---|']
 for el in [e for e in r.get('layout',[]) if e['tag'] in ('H1','MAIN','ARTICLE') and e['width']>0][:3]:
  report.append(f"| {el['tag']} | {el['x']:.2f} / {el['y']:.2f} | {el['width']:.2f} / {el['height']:.2f} | {el['fontSize']} / {el['fontFamily']} |")
 if r.get('screenshot'):report+=['',f"首屏证据：[1440×1000截图]({ROOT/r['screenshot']})。"]
 report+=['']
report+=['## 剔除与限制','',
'- Craylor公开销售学院课程，未纳入上述5案例；培训导流主体不作为合格对标。',
'- Medium The Digital Goldmine有SentryPC 7eer.net指纹，但所见文章为2024年，不能算近期活体；Gist scumola只是短链域名统计，不能算操盘手；Substack Jennifer Leach收入文包含付费墙且公开部分为混合收入，不能推定某个高佣offer成交。',
'- 现有证据不能证明任何主体依靠本文指定的“Google老帖截流”路径在最近30天赚到30万–50万元，更不能承诺复刻收益。',
'','## 交付文件与机械验收','',
'- 同行原始记录：`competitor-hunter(同行反查器)/live_cps_operator_candidates(同行候选证据).json`，包含抓取文本、链接、尺寸、截图位置。',
'- Reddit清单：`competitor-hunter(同行反查器)/serp_unarchived_reddit_targets(Google首页未锁帖靶标).json`。',
'- NodeSeek发布稿：`outbound-materials/nodeseek_tco_post.md`。',
'- X场景草案：`outbound-materials/x_reply_hijack_targets.json`；是模板，未伪装成已经定位的真实推文。',
'- 运行 `python3 verify_dual_track.py`；机械验收核验文件、数量、字段与Reddit/Google取证链；近期成交证据单列输出。机械检查退出0不代表近期成交指标通过，full_task_satisfied仍为false。',
'- 本轮最新工单要求发布稿和草案，未发送社区消息、未调整X生产调度，未把内部QA点击计入人类访问。','']
REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text('\n'.join(report))
all_rows=json.loads((ROOT/'live_cps_operator_candidates(同行候选证据).json').read_text());all_rows[:5]=rows
(ROOT/'live_cps_operator_candidates(同行候选证据).json').write_text(json.dumps(all_rows,ensure_ascii=False,indent=2)+'\n')
print(REPORT)
