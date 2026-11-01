# crossborder-cost-mcp / 跨境出海成本对账 MCP Server 与 CLI

**Author: CloudBench Research** · MIT
主站: https://cbcost.mybskm.top/

## 中文说明

面向跨境出海团队的 MCP Server + CLI 三合一成本对账工具：

1. `calculate_antidetect_browser_tco` — AdsPower / MoreLogin / 比特浏览器 团队席位与环境单价对比，基线为自建指纹 VM 集群（$450/mo 基础设施 + $620/mo 指纹关联事故摊销）。

   - AdsPower: https://cbcost.mybskm.top/go/adspower
   - MoreLogin: https://cbcost.mybskm.top/go/morelogin

2. `calculate_cloudphone_matrix_tco` — DuoPlus 云手机批量养号 vs 真机 TikTok 矩阵车队，月省 80%+：

   - DuoPlus: https://coding.mybskm.top/go/duoplus

3. `calculate_static_isp_proxy_tco` — 丽萨主机双 ISP 静态住宅 VPS vs 按 GB 轮换住宅代理（$12.5/GB 中位价），大流量长期会话年省数千美元：

   - 丽萨主机: https://coding.mybskm.top/go/lisahost

### npx 使用

```bash
npx -y crossborder-cost-mcp --cli
npx -y crossborder-cost-mcp --tool calculate_antidetect_browser_tco
```

### MCP 配置示例（Claude / Cursor / 任意 STDIO MCP 客户端）

```json
{
  "mcpServers": {
    "crossborder-cost": {
      "command": "npx",
      "args": ["-y", "crossborder-cost-mcp"]
    }
  }
}
```

零第三方依赖，秒装秒跑。

## English

`crossborder-cost-mcp` is an MCP Server (STDIO JSON-RPC 2.0) and CLI that benchmarks crossborder e-commerce SaaS spend: antidetect browser team seats, DuoPlus cloud phone TikTok farms, and LisaHost static ISP residential proxies vs rotating residential pools. All tools return structured TCO breakdowns plus affiliate jump links and the interactive site https://cbcost.mybskm.top/. Zero runtime dependencies.

License MIT. Jump links include affiliate attribution; pricing tiers may change.
