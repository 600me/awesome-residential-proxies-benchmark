# Residential Proxy Benchmark — 把预算花在有效抓取上

电商价格任务跑了一夜，早晨拿到的却是 Cloudflare 403 页面？社媒采集不断重试，垃圾机房 IP 消耗带宽、计算资源和工程师排障时间，真正可用的数据迟迟不能交付。采购代理时，只比较每 GB 标价，很容易把便宜买成昂贵。

本仓库对比 Smartproxy、Bright Data、Apify、Oxylabs 的连接成功率、响应头延迟、HTTP 状态与出口 IP 属性。先看下面的可复现测量，再用自己的目标站小批量验证，最后选择适合预算的服务。

公开展示：[Benchmark](https://proxy.mybskm.top/) · [GitHub Repo](https://github.com/600me/awesome-residential-proxies-benchmark) · [扩展隐私政策](https://proxy.mybskm.top/privacy.html)

## 100GB 抓取：有效单价才是账单真相

以下是**明确假设的成本算例，并非厂商报价或已发生订单**：需要 100GB 有效电商/社媒数据，假设失败流量同样计费，忽略请求大小差异、重试计算费与固定套餐费。

| 方案 | 假设标价 | 有效数据率 | 为获得 100GB 有效数据所需计费流量 | 总带宽费 | 有效单价 |
|---|---:|---:|---:|---:|---:|
| 劣质机房代理，高损耗 | $1/GB | 10% | 1,000GB | $1,000 | $10/有效 GB |
| 高纯度住宅代理 | $5/GB | 80% | 125GB | $625 | $6.25/有效 GB |

公式：有效单价 = 标价 ÷ 有效数据率。这个假设下住宅方案节省 $375（37.5%）。真实成功率随站点、地区、会话和时间变化；住宅标签不保证能通过 Cloudflare，也不保证数据有效。

## 实测对比与试用入口

<!-- BENCHMARK:START -->

Updated: 2026-10-16T10:47:19+00:00 (UTC)

**DRY RUN — direct network measurement + synthetic vendor fixtures; not vendor performance evidence.**

| Provider / action | Success Rate | Latency ms (headers, median) | HTTP status | IP / ASN | Result | Promo Code |
|---|---:|---:|---|---|---|---|
| Direct (real network) | 100.0% (3/3) | 864 | 200×3 | Unknown; AS? | OK | — |
| [Smartproxy](https://go.272738.xyz/smartproxy) | 100.0% (3/3) | 250 | 200×3 | ISP (MOCK) | MOCK / OK | SMARTPROXY_PROMO_TBD |
| [Bright Data](https://go.272738.xyz/brightdata) | 0.0% (0/3) | 180 | 403×3 | Unknown (MOCK) | MOCK / Failed | BRIGHTDATA_PROMO_TBD |
| [Apify](https://go.272738.xyz/apify) | 0.0% (0/3) | — | Timeout×3 | Unknown (MOCK) | MOCK / Timeout | APIFY_PROMO_TBD |
| [Oxylabs](https://go.272738.xyz/oxylabs) | 0.0% (0/3) | 300 | 503×3 | Hosting (MOCK) | MOCK / Failed | OXYLABS_PROMO_TBD |

<!-- BENCHMARK:END -->

表中推广入口使用 `https://go.272738.xyz/<vendor>` 稳定短链，当前跳转目标保留 Referral 参数模板，`REPLACE_ME` 与 `*_PROMO_TBD` 是尚未激活的合作链接及独家 Promo Code 占位符，不代表已有返佣关系或已生效优惠。行动出口：点击对应厂商了解服务，结合下方命令验证自己的目标负载，再按有效单价决策；不要仅凭 Mock 数据采购。未来替换为有效联盟链接后，符合条件的购买可能为维护者带来佣金。

## 复现测试

```sh
python3 -m pip install -r requirements.txt
python3 probe_runner.py --dry-run
python3 probe_runner.py
```

配置文件 `config/affiliates.yaml` 使用合法 YAML 的 JSON 子集，故仅需 `aiohttp`，无需额外 YAML 解析依赖。默认每家并发请求 3 次 `https://api.ipify.org?format=json`。真实代理 URL 从四个同名环境变量读取：`SMARTPROXY_PROXY_URL`、`BRIGHTDATA_PROXY_URL`、`APIFY_PROXY_URL`、`OXYLABS_PROXY_URL`；使用厂商提供的 `http://用户名:密码@主机:端口`，特殊字符应 URL 编码，不把凭据写入仓库。Apify 需提供实际代理网关凭据，此处不把平台 Actor 服务混同代理网关。

未配置的厂商显示 Not configured / Not tested；不会冒充实测。`--dry-run` 始终尝试真实直连，并渲染四家明确标为 MOCK 的固定数据，覆盖 200、403、503 和 Timeout。离线或单家故障也会完成渲染，超时上限每次请求 10 秒。

Success Rate 是本轮 HTTP 2xx 次数 / 请求次数，不是目标站内容有效率；Latency 是收到响应头的耗时中位数，包含建连与 TLS，不是纯网络 RTT。HTTP 错误仍记录响应延迟。默认端点只验证连通性，**不测量 Cloudflare 绕过能力、电商/社媒业务成功率或带宽吞吐**。更换目标 URL 后，若其响应不含出口 `ip`，IP 属性显示 Unknown。

通过成功响应的出口 IP 查询 [ipapi.is 免费公共接口](https://ipapi.is/free-tier.html)，读取 ASN、hosting/ISP 属性；限频、网络故障或字段缺失均降级为 Unknown。ISP 只表示住宅候选，不证明独享、纯净或住宅用户身份；旋转代理的一个样本不代表整个 IP 池。查询会将出口 IP 提交给该公共服务，每家每轮最多查询一次。

## 自动更新

GitHub Actions 每周三 03:00 UTC（北京时间 11:00）运行，亦可手动触发。将上述代理环境变量配置为同名 GitHub Actions Secrets 后自动使用；空缺时照常输出未测试状态。工作流只在 README 有变更时以 `GITHUB_TOKEN` 提交并推送，仓库分支策略仍需允许该工作流写入。本地生成不代表工作流已在 GitHub 自然运行。

## Sister Projects (Matrix Interlinks)

- [Proxy Infrastructure Benchmark](https://proxy.mybskm.top) · [GitHub repository](https://github.com/600me/awesome-residential-proxies-benchmark)
- [Global GPU Cloud Benchmark](https://gpu.mybskm.top) · [GitHub repository](https://github.com/600me/awesome-gpu-cloud-pricing-benchmark)
- [Global Payments Matrix](https://pay.mybskm.top) · [GitHub repository](https://github.com/600me/awesome-indie-global-payments-matrix)
