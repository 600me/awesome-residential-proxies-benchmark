# CPS截流矩阵排名点击与成交验证

更新：2026-10-29。状态：**首轮取证未完成，不能作为全工单验收或扩张依据**。

## 已核验事实

- 美国服务器匿名GitHub API及README回读：29个目标仓200；另1个check-proxy-tax基础工具仓200，单列。未登录GitHub小号。
- 7个已知账号公开Gist接口：主号3个Gist，描述对应其他项目；6个小号均为空。尚需核对本项目历史Gist直链，不能宣称所有Gist都已找到。
- 29仓创建时间均为10月26–28日。创建时间不是首次公开时间，但截至本次观察均不可能已发布满14天。建议观察，不能因短窗口无效果判停。
- 美国网关读取当前及9份轮转日志，共4252行，事件日期10月18–28；未证明逐小时完整性，也未证明10月29没有流量。日本网关combined日志4403行，10月28日至29日，无hostname字段。
- 日本现有日志中允许路由经所述过滤剩余0条候选302；该0仅是所读样本的计算值，不是历史真人点击为零。美国整改后254条浏览器样式候选涵盖多个既有渠道，不是29仓带来的254次点击。
- ScraperAPI既有登录后台：到期、未付总额、已付总额各0美元，页面要求设置收款方式；导航仍停留收款设置页，点击及注册未取得。未修改收款资料。
- PartnerStack：网络资格待处理，3项计划申请搁置；未取得可用于品牌对账的成交数。申请不是客户注册。
- Impact访问进入安全验证，尚未取得后台数据。
- 美区无Cookie Google请求7次HTTP200均为enablejs壳，排名不可判定。AI Chrome单个ScraperAPI site查询无命中，登录态，仅旁证，截图已存。Bing/DDG及完整关键词排名未完成。

## 整改与审计

Pi实际provider=cc-switch-open-code-go，model=deepseek-v4.1-flash，完成2轮真实审计；原始流式回执和同一会话在validation目录。模型只收到Codex去敏汇总，没有读文件工具，不冒充独立现场取证。

本次分析复用traffic_audit.py函数但不运行其巡检副作用、不改生产脚本。额外剔除路径含test/verify/probe/smoke/health的6条、非Mozilla UA的2条、同UTC分钟IP+UA+路径重复1条；原过滤版本与整改结果分别保留。过滤不能排除伪装UA或识别所有巡检IP，254仍可能含测试和机器人，不作为真实访客证明。

审计确认不可宣布完工。审计提出的新增“至少3点击/有佣金才能加码”不是工单既定规则，未采纳；保持工单原规则，未知状态不触发停/改/加码。审计把0样本值等同禁止记录0、把日本节点当受众位置等说法不能直接作为事实：保留样本计数并单列历史未知，节点位置不证明访客地域。日志覆盖分母应为自有效发布起至观测时刻，不截短到最后一条日志而掩盖尾部缺口。

## 品牌阶段表

|品牌|目标仓数|排名|逐仓点击|注册/付费|佣金|阶段|
|---|---:|---|---|---|---|---|
|Decodo|5|未知|待路由映射与测试排除|未知|未知|观察|
|Firstbase|5|未知|待路由映射与测试排除|未知|未知|观察|
|ScraperAPI|5|未知|待路由映射与测试排除|未知|后台金额显示0美元，不能代替注册数|观察|
|RunPod|5|未知|待路由映射与测试排除|未知|未知|观察|
|Vast.ai|5|未知|待路由映射与测试排除|未知|未知|观察|
|Webshare|4|未知|待路由映射与测试排除|未知|未知|观察|

尚无证据回答能否排到同行附近；一号四仓、横评表、Python脚本对排名/点击的关系无证据。本报告不建议依据现有数据加码，也未停止其他窗口调度。

## 未完成项与复查

- 补查其他公开仓及本项目Gist直链；逐条CTA→网关→联盟终点，确认共享路由，不按仓均摊点击。
- 每仓2–3词、美区英文搜索及同行排名截图，Bing和DDG旁证；验证码或JS壳均记未知。
- 完成Decodo/Impact、RunPod、Vast.ai、Firstbase、ElevenLabs、Voluum、AdsPower及其他已开通品牌后台只读核验；缺数据不填0。
- 补足可重跑脚本、按发布时间截取日志、去重/过滤版本和历史覆盖说明，真实日志和后台同窗口对账。
- 已建立每周四15:30（Asia/Shanghai）本聊天复查，先补基线后持续2–3周更新此表；该调度尚未自然运行验证。成熟度复查11月5日、12日、19日；28天门槛仍取首次收录证据，不自动套创建日。

## 资产清单（API/README层）

|URL|创建时间UTC|API/README|
|---|---|---|
|https://github.com/600me/check-proxy-tax|2026-10-18T16:17:40Z|200|
|https://github.com/600me/decodo-smartproxy-pricing-coupons|2026-10-26T14:41:13Z|200|
|https://github.com/600me/firstbase-promo-code-pricing|2026-10-26T14:41:21Z|200|
|https://github.com/600me/runpod-gpu-pricing-coupons|2026-10-26T14:41:31Z|200|
|https://github.com/600me/scraperapi-pricing-coupons|2026-10-26T14:41:04Z|200|
|https://github.com/600me/vastai-gpu-pricing-coupons|2026-10-26T14:41:39Z|200|
|https://github.com/constantconv/doola-pricing-vs-firstbase|2026-10-27T04:57:56Z|200|
|https://github.com/constantconv/firstbase-coupon-code-pricing|2026-10-27T04:56:54Z|200|
|https://github.com/constantconv/non-us-founder-llc-annual-cost|2026-10-27T04:58:28Z|200|
|https://github.com/constantconv/stripe-atlas-vs-firstbase-costs|2026-10-27T04:57:26Z|200|
|https://github.com/dnoddieva/aws-p5-vs-vastai-h100-pricing|2026-10-28T00:17:07Z|200|
|https://github.com/dnoddieva/runpod-vs-vastai-gpu-rental-costs|2026-10-28T00:16:28Z|200|
|https://github.com/dnoddieva/spot-instance-gpu-training-budget|2026-10-28T00:17:47Z|200|
|https://github.com/dnoddieva/vastai-promo-code-credit-guide|2026-10-28T00:15:47Z|200|
|https://github.com/mistyparticle/brightdata-vs-webshare-pricing|2026-10-28T00:11:08Z|200|
|https://github.com/mistyparticle/rotating-residential-proxy-bandwidth-calculator|2026-10-28T00:12:25Z|200|
|https://github.com/mistyparticle/smartproxy-vs-webshare-cost-comparison|2026-10-28T00:11:47Z|200|
|https://github.com/mistyparticle/webshare-coupon-code-pricing-guide|2026-10-28T00:10:29Z|200|
|https://github.com/pierrewheffert/lambda-labs-vs-runpod-h100-costs|2026-10-28T00:13:48Z|200|
|https://github.com/pierrewheffert/llm-inference-gpu-hourly-calculator|2026-10-28T00:15:07Z|200|
|https://github.com/pierrewheffert/runpod-coupon-pricing-guide|2026-10-28T00:13:06Z|200|
|https://github.com/pierrewheffert/vastai-vs-runpod-serverless-pricing|2026-10-28T00:14:27Z|200|
|https://github.com/unfitjewell/scraperapi-coupon-code-breakdown|2026-10-27T04:58:58Z|200|
|https://github.com/unfitjewell/scrapingbee-vs-scraperapi-pricing|2026-10-27T04:59:57Z|200|
|https://github.com/unfitjewell/web-scraping-api-cost-comparison|2026-10-27T05:00:29Z|200|
|https://github.com/unfitjewell/zenrows-vs-scraperapi-pricing|2026-10-27T04:59:28Z|200|
|https://github.com/vainship/brightdata-pricing-vs-decodo|2026-10-27T04:55:19Z|200|
|https://github.com/vainship/decodo-coupon-pricing-breakdown|2026-10-27T04:54:47Z|200|
|https://github.com/vainship/oxylabs-pricing-vs-decodo|2026-10-27T04:55:50Z|200|
|https://github.com/vainship/residential-proxy-scraping-costs|2026-10-27T04:56:20Z|200|

原始证据目录：/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/validation(验证)。首轮资产直连超时另存，不覆盖美区成功结果。
