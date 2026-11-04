# cn-coding-plan-mcp (PyPI)

**Author: CloudBench Research** · MIT
主站: https://coding.mybskm.top/

## 中文

纯 Python 标准库实现的 MCP Server（STDIO JSON-RPC 2.0）+ CLI，与 npm 版工具集完全一致。

```bash
uvx cn-coding-plan-mcp          # 直接启动 STDIO MCP
uvx cn-coding-plan-mcp --cli    # CLI 比价表
pip install cn-coding-plan-mcp && cn-coding-plan-mcp --cli
```

### MCP 配置示例

```json
{
  "mcpServers": {
    "cn-coding-plan": {
      "command": "uvx",
      "args": ["cn-coding-plan-mcp"]
    }
  }
}
```

工具：`compare_cn_coding_plans`（阿里云百炼/Dashi・火山方舟・智谱 GLM・腾讯云轻量）、`calculate_claude_cursor_card_tco`（海外防封双 ISP 住宅 IP 与国内百炼 Coding Plan 平替成本）、`compare_cn2_gia_agent_vps`（BWH / 丽萨 / 雨云）。跳板归因链接见 https://coding.mybskm.top/go/aliyun-coding 等。

## English

Zero-dependency MCP Server + CLI for CN coding plan comparison and overseas AI subscription anti-ban proxy TCO. Install with `uvx cn-coding-plan-mcp` or `pip install cn-coding-plan-mcp`. Interactive site: https://coding.mybskm.top/
