# Residential Proxy Benchmark — 把预算花在有效抓取上

[![Chrome Web Store](https://img.shields.io/badge/Chrome_Web_Store-Proxy_Fraud_Checker-4285F4?logo=googlechrome&logoColor=white)](https://chromewebstore.google.com/detail/proxy-fraud-checker/ogihjffhcilpepjkpdifmkloioocoajp?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)

电商价格任务跑了一夜，早晨拿到的却是 Cloudflare 403 页面？社媒采集不断重试，垃圾机房 IP 消耗带宽、计算资源和工程师排障时间，真正可用的数据迟迟不能交付。采购代理时，只比较每 GB 标价，很容易把便宜买成昂贵。

本仓库对比 Smartproxy、Bright Data、Apify、Oxylabs 的连接成功率、响应头延迟、HTTP 状态与出口 IP 属性。先看在线生产看板与下方可复现测量，再用自己的目标站小批量验证，最后选择适合预算的服务。

公开展示：[Live Proxy Benchmark](https://proxy.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [Sticky-Session Calculator](https://proxy.mybskm.top/calculator/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [Research Blog](https://proxy.mybskm.top/blog/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub Repo](https://github.com/600me/awesome-residential-proxies-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [扩展隐私政策](https://proxy.mybskm.top/privacy.html)

## FTC Affiliate Disclosure（返佣披露）

本站/本仓库中的 Smartproxy（现名 Decodo）链接为联盟链接；通过该链接购买符合条件的套餐，维护者可能获得佣金，价格对购买者不变。Bright Data、Oxylabs、Apify 以及下方列出的免费开源方案**不产生任何佣金**。佣金关系不影响实测数字、公开政策事实或表格排序：Table 1 每一格都可在不注册、不付款的前提下从厂商公开页面核实，Table 2 由真实探测程序生成，表格中额外保留一个 $0 的免费开源基线作为无佣金对照。

## Table 1: 9-Dimension Public Commercial & Policy Matrix（Verified 2026-10）

九个采购决策维度全部取自厂商公开定价页、文档与条款（2026-10 核实），**无需代理凭据即可 100% 核实**，因此表中不出现任何 `Not tested` 占位。价格为其公开标价、不含 VAT，可能随时变动，购买前请回厂商页面复核。

| Provider | ① Entry $/GB (PAYG) | ② Billing Granularity | ③ Min Deposit | ④ Free Trial | ⑤ Refund SLA | ⑥ Geo / ASN Coverage | ⑦ KYC Friction | ⑧ Sticky Session Window | ⑨ Best For |
|---|---|---|---|---|---|---|---|---|---|
| [**Smartproxy (Decodo)**](https://go.272738.xyz/smartproxy?src=proxy_table_winner)<br>*Verified Partner · Best Self-Serve Value* | $4.00 list PAYG；3GB 起 $3.75/GB，100GB 降到 $2.75/GB | 按 GB 计费；月度套餐或 Pay-As-You-Go，可中途追加 GB | $11.25（3GB 套餐）+VAT | 3 天 / 100MB 住宅试用（激活需绑定卡） | 自助购买 14 天退款（使用过免费试用后不适用） | 115M+ IP，195+ 地区；国家/州/城市/ZIP/ASN 定向 | 自助注册，无公司 KYC | 1–1440 分钟可配置，默认 10 分钟 | 月流量 <100GB、不想走人工 KYC 的自助团队 |
| **Bright Data**<br>*Direct Reference · Enterprise KYC* | $8.00 list PAYG（常做 50% 到 $4.00/GB）；$499/141GB 起 $3.50/GB | 按 GB；PAYG 或 $499/$999/$1,999 月度承诺；Web Unlocker 另按 1k 请求计费 | $10 PAYG 起充 | 7 天 $2 代理额度（住宅还需先过 KYC 并充值） | 无公开自助退款窗口，按合同协商 | 400M+ 旋转 IP，195 国；国家/州/城市/ZIP 免费定向 | **人工 KYC**，仅限通过审核的公司，**2026-07 起无即时自助通道** | 最长 30 分钟 | 已通过合规审查、月采购数百 GB 的企业 |
| **Oxylabs**<br>*Direct Reference · Corporate Tier* | $6.00 入门档；20GB $5.00/GB，1TB $2.50/GB | 按 GB 月度订阅（$30/$100/$500/$2,500+），也提供一次性 PAYG | $30（Starter）起 | $5 welcome credit | 自助购买标注为不可退款，建议先用 welcome credit 验证 | 175M+ IP，195 国；坐标级定向 | **强制 KYC**，需企业开户流程 | 最长 24 小时（本表最长） | 需要长会话与正式开户流程的企业/中型数据团队 |
| **Apify Residential**<br>*Direct Reference · Actor Bundled* | $8.00（含 Free 档全部套餐）；$999 Business 档 $7.00/GB | 预付费平台额度，住宅按 GB 与 Actor 计算量共用额度 | $0（无最低 GB 采购；付费套餐 $19/月起） | 每月 $5 免费额度、无需绑卡（$8/GB 约合 625MB；对外使用代理需付费套餐） | 费用一般不可退；Actor 运行失败以额度补偿 | 住宅池通过 Apify 平台与 Actor 使用，非独立网关 | 普通邮箱注册，无 KYC | 同一 `session` ID 约 30 分钟 | 已在 Apify 平台跑 Actor、想把代理费并入同一账单的团队 |
| **Direct `curl_cffi` + Cloudflare WARP / IPv6**<br>*Free Open-Source Baseline · $0 Commission Anchor* | **$0.00**（账单链路中没有任何代理厂商） | 无计费、无额度、无发票 | $0 | 永久免费（MIT/BSD 工具 + WARP 免费层） | N/A（没有可退款的厂商） | 使用你主机/WARP 的出口（Cloudflare 边缘，通常属机房 ASN） | 无账号、无审核 | N/A：连接级控制，自己掌握 TLS/JA3，没有会过期的会话 TTL | 低频 (<1,000 请求/天) 且住宅代理属过度采购的场景 |

> **Why the free row is in the table**：We earn **$0 from this open-source option**; recommended for **low-volume <1,000 req/day where residential proxies are overkill**。若爬取量小、只对 JA3/JA4 敏感而目标站没有强 bot 防护，`curl_cffi` + 免费 WARP/IPv6 出口往往零边际成本即可通过同一批目标；只有在确需旋转住宅 ASN、精细地理定向或跨多步流程的粘性会话时才购买住宅带宽。

来源（2026-10 核实）：Decodo/Smartproxy [定价](https://decodo.com/proxies/residential-proxies/pricing) · [试用条款](https://help.decodo.com/docs/trials) · [粘性会话文档](https://help.decodo.com/docs/residential-proxy-custom-sticky-sessions) · [退款政策](https://decodo.com/faq/billing/can-i-get-a-refund)；Bright Data [定价](https://brightdata.com/pricing/proxy-network/residential-proxies) · [住宅网络访问/KYC 政策](https://docs.brightdata.com/products/residential/network-access)；Oxylabs [住宅定价](https://oxylabs.io/pricing/residential-proxy-pool) · [会话控制文档](https://developers.oxylabs.io/help-center/products-and-features/how-to-use-session-control)；Apify [定价](https://apify.com/pricing) · [代理文档](https://docs.apify.com/proxy) · [通用条款](https://docs.apify.com/legal/general-terms-and-conditions)。

## 实时生产测量与动态排名

实时生产测量与动态排名请直接查看 [Live Proxy Benchmark](https://proxy.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)；本地可直接运行 `python3 probe_runner.py` 进行多厂商连通性实测。

<!-- BENCHMARK:START -->

Updated: 2026-10-28T09:28:38+00:00 (UTC)

**Live run — unconfigured vendors are not tested.**

| Provider / action | Success Rate | Latency ms (headers, median) | HTTP status | IP / ASN | Result | Promo Code |
|---|---:|---:|---|---|---|---|
| Direct (real network) | 100.0% (3/3) | 94 | 200×3 | Unknown; AS? | OK | — |
| [Smartproxy](https://go.272738.xyz/smartproxy?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |
| [Bright Data](https://go.272738.xyz/brightdata?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |
| [Apify](https://go.272738.xyz/apify?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |
| [Oxylabs](https://go.272738.xyz/oxylabs?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |

<!-- BENCHMARK:END -->

上方表格是**仪器读数**，与 Table 1 的商业/政策矩阵刻意分离：只要 `SMARTPROXY_PROXY_URL` 未配置，Smartproxy 行就如实显示未测试，不填入任何示意性成功率、延迟或住宅 ASN。Decodo 的 100MB 住宅试用在激活时需要绑定支付卡（属付款动作），因此本仓库不会自动注册；配置凭据后重跑探针，该行会由真实测量自动填充。第三方一键复现工具：<https://github.com/600me/check-proxy-tax>。

表中推广入口使用 `https://go.272738.xyz/<vendor>?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark` 稳定短链。2026-10-17，Smartproxy（现名 Decodo）联盟申请已获批，对应短链已接入官方专属推广链接；符合条件的购买可能为维护者带来佣金。Bright Data、Apify、Oxylabs 的联盟状态以各后台审核结果为准；未激活的目标不产生佣金，也不代表已确认折扣。当前未确认独家优惠码，不代表有已生效折扣。行动出口：点击对应厂商了解服务，结合下方命令验证自己的目标负载，再按有效单价决策；不要仅凭标价或单一轮次采购。联盟获批不代表已取得厂商代理凭据、完成真实性能测量或产生收入。

## 100GB 抓取：有效单价才是账单真相

以下是**明确假设的成本算例，并非厂商报价或已发生订单**：需要 100GB 有效电商/社媒数据，假设失败流量同样计费，忽略请求大小差异、重试计算费与固定套餐费。

| 方案 | 假设标价 | 有效数据率 | 为获得 100GB 有效数据所需计费流量 | 总带宽费 | 有效单价 |
|---|---:|---:|---:|---:|---:|
| 劣质机房代理，高损耗 | $1/GB | 10% | 1,000GB | $1,000 | $10/有效 GB |
| 高纯度住宅代理 | $5/GB | 80% | 125GB | $625 | $6.25/有效 GB |

公式：有效单价 = 标价 ÷ 有效数据率。这个假设下住宅方案节省 $375（37.5%）。真实成功率随站点、地区、会话和时间变化；住宅标签不保证能通过 Cloudflare，也不保证数据有效。想换成自己的并发、流程时长与掉线率，用 [sticky-session & concurrency-loss calculator](https://proxy.mybskm.top/calculator/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)。

## 复现测试

```sh
python3 -m pip install -r requirements.txt
python3 probe_runner.py --dry-run
python3 probe_runner.py
python3 test_calculator_math.py     # 计算器数学 + canonical/JSON-LD + sitemap 断言，仅需 Node
```

`--dry-run` 只做本地直连与配置检查，不上传 README、不生成任何厂商测量；`python3 probe_runner.py` 读取四个代理环境变量做真实连通性测试并把结果写入上方表格。未配置的厂商显示 Not configured / Not tested；不会冒充实测。每次请求超时上限 10 秒。`test_calculator_math.py` 把 `web/calculator/index.html` 内嵌的纯 JS 计算核心抽出来，用 Node 与独立 Python 实现逐字段对照，并校验四个页面的 canonical / JSON-LD 与两份 sitemap。

配置文件 `config/affiliates.yaml` 使用合法 YAML 的 JSON 子集，故仅需 `aiohttp`，无需额外 YAML 解析依赖。默认每家并发请求 3 次 `https://api.ipify.org?format=json`。真实代理 URL 从四个同名环境变量读取：`SMARTPROXY_PROXY_URL`、`BRIGHTDATA_PROXY_URL`、`APIFY_PROXY_URL`、`OXYLABS_PROXY_URL`；使用厂商提供的 `http://用户名:密码@主机:端口`，特殊字符应 URL 编码，不把凭据写入仓库。Apify 需提供实际代理网关凭据，此处不把平台 Actor 服务混同代理网关。

Success Rate 是本轮 HTTP 2xx 次数 / 请求次数，不是目标站内容有效率；Latency 是收到响应头的耗时中位数，包含建连与 TLS，不是纯网络 RTT。HTTP 错误仍记录响应延迟。默认端点只验证连通性，**不测量 Cloudflare 绕过能力、电商/社媒业务成功率或带宽吞吐**。更换目标 URL 后，若其响应不含出口 `ip`，IP 属性显示 Unknown。

通过成功响应的出口 IP 查询 [ipapi.is 免费公共接口](https://ipapi.is/free-tier.html)，读取 ASN、hosting/ISP 属性；限频、网络故障或字段缺失均降级为 Unknown。ISP 只表示住宅候选，不证明独享、纯净或住宅用户身份；旋转代理的一个样本不代表整个 IP 池。查询会将出口 IP 提交给该公共服务，每家每轮最多查询一次。

## 自动更新

GitHub Actions 每周三 03:00 UTC（北京时间 11:00）运行，亦可手动触发。将上述代理环境变量配置为同名 GitHub Actions Secrets 后自动使用；空缺时照常输出未测试状态。工作流只在 README 有变更时以 `GITHUB_TOKEN` 提交并推送，仓库分支策略仍需允许该工作流写入。本地生成不代表工作流已在 GitHub 自然运行。

## 深度研究

- [Why Rotating Residential Proxies Still Get 403s: Sticky Session TTL, JA3 Fingerprints, and ASN Economics (2026)](https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) — 三层失败机理、厂商粘性窗口对照、三档重跑损耗算例，以及可复制的 `curl` / `curl_cffi` 诊断命令。

## Sister Projects (Matrix Interlinks)

- [Proxy Infrastructure Benchmark](https://proxy.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [Calculator](https://proxy.mybskm.top/calculator/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [Blog](https://proxy.mybskm.top/blog/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-residential-proxies-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)
- [Global GPU Cloud Benchmark](https://gpu.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GPU calculator](https://gpu.mybskm.top/calculator/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-gpu-cloud-pricing-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)
- [Global Payments Matrix](https://pay.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-indie-global-payments-matrix?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)
- [Web Scraping APIs Benchmark](https://scrape.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [Scraping TCO calculator](https://scrape.mybskm.top/calculator/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-web-scraping-apis-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)


## 2026-10-26 双轨采集与物料交付

- 已运行两个16线程采集脚本；14组Google查询、97个唯一Reddit候选、74个真实JSON未锁/未归档结果，精选20条（四赛道各5条）附逐帖英文评论。
- 同行报告记录5个真实公开主体，含入口、offer/官方佣金、页面尺寸与截图；近期出单证据合格数为0，历史转化和作者收入自述不替代近期成交。
- 已写入 `outbound-materials/nodeseek_tco_post.md` 与 `outbound-materials/x_reply_hijack_targets.json`（12条草案）。本轮未发布。
- `python3 verify_dual_track.py` 实测退出0；仅表示工单指定机械断言与取证一致性通过。输出 `full_task_satisfied=false`，商业证据指标未达到。完整输出在 `competitor-hunter(同行反查器)/evidence(取证)/verification-result.txt`。
- 报告：`/Users/a600/project-hub(项目设计实施)/kais-business-findings(生意发现记录)/cps-live-hijack-benchmarks-20261026(海外CPS活体截流同行拆解报告).md`。
- CLI发布wheel已下载至临时目录，实际 `--help` 退出0，稿件参数有效；临时目录已清理。浏览器取证标签均通过finally关闭，未改变生产调度。
