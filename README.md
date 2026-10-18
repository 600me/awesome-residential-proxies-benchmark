# Residential Proxy Benchmark — 把预算花在有效抓取上

[![Chrome Web Store](https://img.shields.io/badge/Chrome_Web_Store-Proxy_Fraud_Checker-4285F4?logo=googlechrome&logoColor=white)](https://chromewebstore.google.com/detail/proxy-fraud-checker/ogihjffhcilpepjkpdifmkloioocoajp?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)

电商价格任务跑了一夜，早晨拿到的却是 Cloudflare 403 页面？社媒采集不断重试，垃圾机房 IP 消耗带宽、计算资源和工程师排障时间，真正可用的数据迟迟不能交付。采购代理时，只比较每 GB 标价，很容易把便宜买成昂贵。

本仓库对比 Smartproxy、Bright Data、Apify、Oxylabs 的连接成功率、响应头延迟、HTTP 状态与出口 IP 属性。先看在线生产看板与下方可复现测量，再用自己的目标站小批量验证，最后选择适合预算的服务。

公开展示：[Live Proxy Benchmark](https://proxy.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub Repo](https://github.com/600me/awesome-residential-proxies-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [扩展隐私政策](https://proxy.mybskm.top/privacy.html)

## 实时生产测量与动态排名

实时生产测量与动态排名请直接查看 [Live Proxy Benchmark](https://proxy.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)；本地可直接运行 `python3 probe_runner.py` 进行多厂商连通性实测。

<!-- BENCHMARK:START -->

Updated: 2026-10-18T12:57:30+00:00 (UTC)

**Live run — unconfigured vendors are not tested.**

| Provider / action | Success Rate | Latency ms (headers, median) | HTTP status | IP / ASN | Result | Promo Code |
|---|---:|---:|---|---|---|---|
| Direct (real network) | 100.0% (3/3) | 848 | 200×3 | Unknown; AS? | OK | — |
| [Smartproxy](https://go.272738.xyz/smartproxy?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |
| [Bright Data](https://go.272738.xyz/brightdata?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |
| [Apify](https://go.272738.xyz/apify?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |
| [Oxylabs](https://go.272738.xyz/oxylabs?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) | Not configured | — | — | Unknown | Not tested | — |

<!-- BENCHMARK:END -->

表中推广入口使用 `https://go.272738.xyz/<vendor>?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark` 稳定短链。2026-10-17，Smartproxy（现名 Decodo）联盟申请已获批，对应短链已接入官方专属推广链接；符合条件的购买可能为维护者带来佣金。Bright Data、Apify、Oxylabs 的联盟状态以各后台审核结果为准；未激活的目标不产生佣金，也不代表已确认折扣。当前未确认独家优惠码，不代表有已生效折扣。行动出口：点击对应厂商了解服务，结合下方命令验证自己的目标负载，再按有效单价决策；不要仅凭标价或单一轮次采购。联盟获批不代表已取得厂商代理凭据、完成真实性能测量或产生收入。

## 100GB 抓取：有效单价才是账单真相

以下是**明确假设的成本算例，并非厂商报价或已发生订单**：需要 100GB 有效电商/社媒数据，假设失败流量同样计费，忽略请求大小差异、重试计算费与固定套餐费。

| 方案 | 假设标价 | 有效数据率 | 为获得 100GB 有效数据所需计费流量 | 总带宽费 | 有效单价 |
|---|---:|---:|---:|---:|---:|
| 劣质机房代理，高损耗 | $1/GB | 10% | 1,000GB | $1,000 | $10/有效 GB |
| 高纯度住宅代理 | $5/GB | 80% | 125GB | $625 | $6.25/有效 GB |

公式：有效单价 = 标价 ÷ 有效数据率。这个假设下住宅方案节省 $375（37.5%）。真实成功率随站点、地区、会话和时间变化；住宅标签不保证能通过 Cloudflare，也不保证数据有效。

## 复现测试

```sh
python3 -m pip install -r requirements.txt
python3 probe_runner.py --dry-run
python3 probe_runner.py
```

`--dry-run` 只做本地直连与配置检查，不上传 README、不生成任何厂商测量；`python3 probe_runner.py` 读取四个代理环境变量做真实连通性测试并把结果写入上方表格。未配置的厂商显示 Not configured / Not tested；不会冒充实测。每次请求超时上限 10 秒。

配置文件 `config/affiliates.yaml` 使用合法 YAML 的 JSON 子集，故仅需 `aiohttp`，无需额外 YAML 解析依赖。默认每家并发请求 3 次 `https://api.ipify.org?format=json`。真实代理 URL 从四个同名环境变量读取：`SMARTPROXY_PROXY_URL`、`BRIGHTDATA_PROXY_URL`、`APIFY_PROXY_URL`、`OXYLABS_PROXY_URL`；使用厂商提供的 `http://用户名:密码@主机:端口`，特殊字符应 URL 编码，不把凭据写入仓库。Apify 需提供实际代理网关凭据，此处不把平台 Actor 服务混同代理网关。

Success Rate 是本轮 HTTP 2xx 次数 / 请求次数，不是目标站内容有效率；Latency 是收到响应头的耗时中位数，包含建连与 TLS，不是纯网络 RTT。HTTP 错误仍记录响应延迟。默认端点只验证连通性，**不测量 Cloudflare 绕过能力、电商/社媒业务成功率或带宽吞吐**。更换目标 URL 后，若其响应不含出口 `ip`，IP 属性显示 Unknown。

通过成功响应的出口 IP 查询 [ipapi.is 免费公共接口](https://ipapi.is/free-tier.html)，读取 ASN、hosting/ISP 属性；限频、网络故障或字段缺失均降级为 Unknown。ISP 只表示住宅候选，不证明独享、纯净或住宅用户身份；旋转代理的一个样本不代表整个 IP 池。查询会将出口 IP 提交给该公共服务，每家每轮最多查询一次。

## 自动更新

GitHub Actions 每周三 03:00 UTC（北京时间 11:00）运行，亦可手动触发。将上述代理环境变量配置为同名 GitHub Actions Secrets 后自动使用；空缺时照常输出未测试状态。工作流只在 README 有变更时以 `GITHUB_TOKEN` 提交并推送，仓库分支策略仍需允许该工作流写入。本地生成不代表工作流已在 GitHub 自然运行。

## Sister Projects (Matrix Interlinks)

- [Proxy Infrastructure Benchmark](https://proxy.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-residential-proxies-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)
- [Global GPU Cloud Benchmark](https://gpu.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-gpu-cloud-pricing-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)
- [Global Payments Matrix](https://pay.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-indie-global-payments-matrix?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)
- [Web Scraping APIs Benchmark](https://scrape.mybskm.top/?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark) · [GitHub repository](https://github.com/600me/awesome-web-scraping-apis-benchmark?utm_source=github&utm_medium=readme&utm_campaign=proxy_benchmark)
