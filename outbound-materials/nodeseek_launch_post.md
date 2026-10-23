# 写了个零依赖 Python CLI 测算爬虫 403 重试税，顺手做了 4 个免注册在线工程计算器（代理/反爬API/GPU/出海收单）

> 发布账号：`WalterPGale`｜目标板块：技术 / 开源工具
> 内容性质：开源工具 + 免费在线计算器。文末有联盟链接披露，页面零广告无弹窗。
> 事实核对（2026-10-23）：仓库 MIT、stdlib-only；wheel 安装命令已在干净 venv 实测通过；4 个计算器 URL 均返回 HTTP 200；文中数字全部可复算。

---

## 一、先说我踩到的坑：403 不是"买贵了代理"能解决的

做电商价格监控和 RAG 抓取的朋友大概率都遇到过这个循环：

1. 目标站上 Cloudflare，返回 `403` 或 `cf-mitigated: challenge`；
2. 换成住宅代理，过了；
3. 抓了十几分钟，`cf_clearance` 失效或者 IP 被标，又开始 `403`；
4. 加大并发、加轮换频率，`403` 更多，带宽消耗翻倍。

问题在于 `cf_clearance` 这一类 cookie 是**跟 TLS/JA3 指纹 + 出口 IP 绑定**的。你每换一次出口 IP，就相当于从头做一次握手挑战；每换一次 UA 或者换一套 HTTP 客户端指纹，挑战结果也不能复用。于是真正发生在账单上的不是"我买了 100GB 流量"，而是：

- 一次 `403` 响应照样计费（按请求计费的代理尤其明显）；
- 一次 `403` 之后的重试也计费；
- 一次 `200` 但返回的是挑战页 / 空壳页 / 登录墙，同样计费，但对你毫无价值。

**算例（纯算术，不是厂商报价）**：某代理标价 `$0.49 / 1,000 请求`。

| 可用率 | 拿到 1,000 条可用响应需要发 | 有效单价 | 相对标价倍数 |
|---:|---:|---:|---:|
| 100% | 1,000 次 | $0.49 | 1.00x |
| 70% | 1,429 次 | $0.70 | 1.43x |
| 50% | 2,000 次 | $0.98 | 2.00x |
| 40% | 2,500 次 | $1.225 | 2.50x |
| 33% | 3,030 次 | $1.485 | 3.03x |

如果厂商按 GB 计费，同一件事换个单位：你需要 **100GB 有效数据**，可用率 40%，那么计费流量是 **250GB**。所以"每 GB 标价便宜 30%"在低可用率面前完全不够看——这就是我把这套东西叫 **403 Tax（403 重试税）** 的原因：它是标价和真实成本之间的差额，而且不写在报价单上。

---

## 二、开源方案：check-proxy-tax（MIT，零依赖，单文件核心模块）

仓库：<https://github.com/600me/check-proxy-tax>（MIT，Python 3.8+，只用标准库，无账号无 API Key 无后台服务）

它做的事很窄：**对同一个 URL 打一小波并发请求，把每个响应判定成 usable / blocked，然后告诉你"每 1,000 条可用响应"到底花了多少钱。**

判定标准故意从严——必须同时满足：

1. 最终 HTTP 状态码是 `200`（重定向会跟随，按最终状态判定）；
2. 如果传了 `--marker`，响应体里必须包含这个字符串。

`403`、`429`、其它 `4xx`、`5xx`、超时、连接/TLS 失败、以及**没有 marker 的 200**，一律算 blocked。

### 安装（一条命令，不用 clone）

```bash
pip install https://github.com/600me/check-proxy-tax/releases/download/v1.0.0/check_proxy_tax-1.0.0-py3-none-any.whl
check-proxy-tax --help
```

### 跑一次真实测算

```bash
check-proxy-tax \
  --url "https://example.com" \
  --requests 20 \
  --marker "Example Domain" \
  --price-per-1k 0.49 \
  --json
```

这是我刚在本机跑出来的真实输出（`example.com`，无代理，20 次采样）：

```json
{
  "tool": "check-proxy-tax",
  "version": "1.0.0",
  "url": "https://example.com",
  "marker": "Example Domain",
  "requests": 20,
  "concurrency": 4,
  "timeout_seconds": 10.0,
  "proxy_configured": false,
  "nominal_price_per_1k": 0.49,
  "usable_count": 20,
  "blocked_count": 0,
  "usable_pct": 100.0,
  "effective_cost_per_1k": 0.49,
  "tax_multiplier": 1.0,
  "cost_status": "finite",
  "latency_ms": { "p50": 931.98, "p95": 1924.37, "min": 716.4, "max": 2153.02 },
  "total_bytes": 11540,
  "status_counts": { "200": 20 },
  "blocked_reasons": {},
  "exit_code": 0,
  "benchmark_url": "https://scrape.mybskm.top/?utm_source=cli&utm_content=check-proxy-tax",
  "ftc_disclosure": "FTC Disclosure: Benchmark links may include affiliate tracking."
}
```

把 `--proxy` 换成你自己的代理、URL 换成真实目标页、`--marker` 换成商品页上的"加入购物车"之类的稳定字符串，`usable_pct` 就会立刻掉下来，`effective_cost_per_1k` 和 `tax_multiplier` 会告诉你真实差价。如果一次都没成功，`cost_status` 是 `infinite`——这种情况下标价再低也买不到可用数据。

数学就三行：

```text
usable_pct            = usable_count / total_requests * 100
effective_cost_per_1k = nominal_price_per_1k / (usable_pct / 100)
tax_multiplier        = effective_cost_per_1k / nominal_price_per_1k
```

### 放进 CI 当门禁

退出码是设计过的：`0` 全部可用、`1` 部分被拦（降级）、`2` 一条都不可用、`3` 参数错误。所以可以直接这么用：

```bash
check-proxy-tax --url "$TARGET" --requests 50 --marker "$MARKER" \
  --proxy "$PROXY_URL" --price-per-1k 0.49 --json > probe.json \
  || echo "::warning::可用率下降，检查代理池或指纹配置"
```

一个提醒：单次采样只能说明"这一个时间点、这一个出口"。要做采购决策，至少覆盖不同时段 + 多个出口，别看一次数字就下单。

---

## 三、顺手做的 4 个在线计算器（都免注册、零广告）

ClI 只回答"这次采样多少钱"，但采购决策往往要先估算模型。所以另外做了 4 个纯前端计算器，全部免注册、打开就能改参数：

**1）住宅代理 403 重试税与有效每 GB 单价**
<https://proxy.mybskm.top/calculator/?utm_source=nodeseek>
按 GB 计费场景下，把可用率、重试次数、页面体积带进去，算"为了拿到 N GB 有效数据要付多少"。同时有 9 个维度的厂商公开政策对照表（价格粒度、最低充值、试用、退款、KYC、粘性会话窗口等），这些格子都能在不注册、不付款的前提下从厂商公开页面核实。

**2）RAG / 反爬云 API 综合 TCO**
<https://scrape.mybskm.top/calculator/?utm_source=nodeseek>
自建（代理 + 无头浏览器 + 指纹维护 + 人力）vs 托管抓取 API（按成功请求计费）的总成本对比。适合正在纠结"要不要自己维护一套浏览器农场"的团队。

**3）H100 / A100 GPU 租用冷启动与存储真实成本**
<https://gpu.mybskm.top/calculator/?utm_source=nodeseek>
输入模型参数量、精度、上下文、并发，先算显存需求（权重 + KV cache + CUDA context，再乘 1.15 安全余量），再按卡数给出 RunPod / Vast.ai 的小时成本对照。这里有个真实的坑：**per-GPU-hour 不是账单单位**。同一张卡的公开抽样价，Vast.ai 的 H100 是 $2.01/卡时、RunPod 是 $2.69/卡时（低 25.3%），但 Vast 的部分 offer 只能按 2 卡捆绑租：一个只需要单卡的任务，4090 上实际是 $0.858/小时 vs RunPod 的 $0.34/小时，反而贵 **152%**。所以"便宜 25%"只在特定卡型 + 特定卡数下成立。

**4）非美出海 SaaS：MoR（Paddle / Lemon Squeezy）vs 美区 LLC（Firstbase + Stripe）盈亏平衡点**
<https://pay.mybskm.top/?utm_source=nodeseek>
把 MRR、客单价、卡组织构成（美国卡 vs 国际卡）、FX、年合规成本带进去，直接算"你从多少 MRR 开始，5% 的 MoR 抽成超过了自建 LLC + Stripe 的固定成本"。参考量级：在最理想的卡构成下平衡点约 **$3,205 MRR**，70% 国际卡时抬到 **$5,376**，再叠加货币转换能到 **$15,152**。也就是说"5% 划算还是 LLC 划算"根本没有统一答案，只有"你的 MRR 和卡构成决定答案"。

---

## 四、态度与反馈

- 代码是 MIT，单模块、零依赖，欢迎直接读、直接改、直接拿去接自己的监控。有 bug 或想加的指标（比如按 GB 计价模式、并发梯度扫描）开 Issue 就行。
- 计算器全部是静态前端，参数全在 URL 之外自己改，不存你的数据、不要求注册、没有弹窗广告。
- **透明披露**：部分厂商入口是联盟链接，通过它们购买我可能拿到佣金，价格对你不变；表格里的公开政策数字与联盟关系无关，且都可以自己复核。所有"实测"数字都标了采样时间和采样方式，没测的格子直接写"未测试"，不会填示意值。

如果这篇对你有用，GitHub 点个 Star 就是最好的反馈；如果你测出来某家代理在你自己的目标站上可用率很高，也欢迎在楼里贴数据——这种来自真实负载的数字比任何厂商页面都有用。
