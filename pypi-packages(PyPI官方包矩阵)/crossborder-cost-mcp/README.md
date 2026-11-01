# crossborder-cost-mcp (PyPI)

**Author: CloudBench Research** · MIT
主站: https://cbcost.mybskm.top/

## 中文

纯 Python 标准库实现的跨境出海成本对账 MCP Server（STDIO JSON-RPC 2.0）+ CLI。

```bash
uvx crossborder-cost-mcp          # STDIO MCP 启动
uvx crossborder-cost-mcp --cli    # CLI 对账表
pip install crossborder-cost-mcp && crossborder-cost-mcp --cli
```

### MCP 配置示例

```json
{
  "mcpServers": {
    "crossborder-cost": {
      "command": "uvx",
      "args": ["crossborder-cost-mcp"]
    }
  }
}
```

工具：`calculate_antidetect_browser_tco`（AdsPower vs MoreLogin vs 比特浏览器）、`calculate_cloudphone_matrix_tco`（DuoPlus 云手机矩阵）、`calculate_static_isp_proxy_tco`（丽萨双 ISP vs 轮换住宅代理）。跳板: https://cbcost.mybskm.top/go/adspower 等。

## English

Zero-dependency Python MCP Server + CLI benchmarking antidetect browsers, cloud phone TikTok farms and static ISP proxies. Install via `uvx crossborder-cost-mcp` or `pip install crossborder-cost-mcp`. Site: https://cbcost.mybskm.top/
