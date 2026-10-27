# 写了个零依赖 Python CLI 测算爬虫 403 重试税，顺手做了 4 个无广告在线 TCO 计算器

各位 NodeSeek 的坛友，在自建爬虫或调用数据采集接口时，经常遇到一个账单陷阱：厂商给出的标称每千次请求价格很便宜，但目标站一旦加了强风控或 Cloudflare 质询，大量请求在 403/429 阶段挂掉并触发后续重试，实际成功拿回数据的综合单价就会翻倍。

为此我写了一个开源、零第三方依赖的轻量 Python CLI 工具，用来实测目标站可用率并换算“重试税”（Retry Tax），同时顺手整理了 4 个无广告在线 TCO 测算页面。

### 1. 核心数学模型与前提说明
在按次计费模式下，计算采用经典简化折算公式：
`每千次成功有效成本 = 标称每千次单价 / 实测成功率`
（即 `effective_cost_per_1k = nominal_price_per_1k / success_ratio`）

**前提说明**：该模型建立在每次发起的请求（无论成功还是 403 阻断）厂商均全额计费、且失败请求无抵扣返还的简化前提下；若实测成功率为 0%，单次有效获取成本在数学上趋近无穷大。

**假设推导算例**：
假设某代理服务标称价格为 **$0.49 / 1000 次尝试**。如果实测目标站成功率仅为 **40%（0.40）**，则实际每获取 1000 次有效成功的真实综合支出为：
`$0.49 / 0.40 = $1.225 / 1000 次成功响应`
实际单价为标称单价的 2.5 倍，即高出 150%。

### 2. 零依赖 Python CLI 安装与使用
与单纯的手动填数字空算不同，该 CLI 会真实向目标站点发送指定数量的小批量探针请求，通过 HTTP 状态码及正文标识（marker）检测真实成功率，并自动套用单价公式换算：

```bash
# 从 GitHub Release 安装纯标准库打包的 wheel (v1.0.0)
pip install https://github.com/600me/check-proxy-tax/releases/download/v1.0.0/check_proxy_tax-1.0.0-py3-none-any.whl

# 运行探针测试示例（指定测试 URL、发包数 20、匹配标记、标称千次价格，并输出 JSON）
check-proxy-tax --url https://example.com --requests 20 --marker "Example Domain" --price-per-1k 0.49 --json
```

GitHub 开源仓库：https://github.com/600me/check-proxy-tax

### 3. 四个无广告在线 TCO 计算器
如果不想在本地装环境或需要做更大维度的成本架构评估，我也上线了 4 个纯净 Web 测算页面：
- **代理重试税计算器**（测算粘性会话中断与步骤重试流量损耗）：https://proxy.mybskm.top/calculator/?utm_source=nodeseek
- **自建 vs 爬虫 API 成本计算器**（输入页面量、平均页面体积、封禁率、JS 渲染比例与工程工时，评估自建与直接买 API 的平衡点）：https://scrape.mybskm.top/calculator/?utm_source=nodeseek
- **GPU 显存与卡时计算器**（根据模型参数量、精度量化及上下文长度估算所需 VRAM、卡数与计算卡时费用；存储与网络需额外预留）：https://gpu.mybskm.top/calculator/?utm_source=nodeseek
- **出海收单 LLC vs MoR 费用对比**（基于 MRR、客单价 AOV、国际卡占比、FX 外汇损耗及年度预算推导综合费率）：https://pay.mybskm.top/?utm_source=nodeseek

### 4. 商业说明与合规免责
1. **无广告与商业化披露**：页面内无第三方横幅弹窗广告，但我作为维护者需透明声明：“无广告不代表完全无商业化”，页面内部分主机或平台的外链可能包含联盟推荐（Affiliate）链接。
2. **报价与算例性质**：文中推导均为理论假设算例；计算器页面内含部分抓取的日期限定市场参考报价，均非当前实时报价承诺，实际费用以厂商实时账单为准。
3. **法务与税务免责**：LLC 与 MoR 模块仅为手续费数值对照，绝不构成任何法律或税务建议，亦不代表注册 LLC 能必然免税或 100% 通过 Stripe 等网关的收单审核。
