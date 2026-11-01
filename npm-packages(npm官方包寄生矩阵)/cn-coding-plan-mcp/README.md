# cn-coding-plan-mcp / 国内 Coding Plan 比价 MCP Server 与 CLI

**Author: CloudBench Research** · MIT
围观主站 (Interactive Site): https://coding.mybskm.top/

## 中文说明

`cn-coding-plan-mcp` 是一个面向国内开发者的 **MCP Server + CLI** 双形态工具包：

1. `compare_cn_coding_plans` — 对比阿里云百炼 Coding Plan、阿里云大模型推理（DashScope/Dashi）、火山方舟、智谱 GLM Coding、腾讯云轻量/双11 的入门价与额度梯度，返回优惠券跳板：

   - 阿里云 Coding Plan: https://coding.mybskm.top/go/aliyun-coding
   - 阿里云 Dashi 推理: https://coding.mybskm.top/go/aliyun-dashi
   - 火山方舟: https://coding.mybskm.top/go/volcengine-coding
   - 智谱 GLM: https://coding.mybskm.top/go/zhipu-glm
   - 腾讯云轻量/双11: https://coding.mybskm.top/go/tencent-double11

2. `calculate_claude_cursor_card_tco` — 计算国内开发者订阅 Claude Code / Cursor / OpenAI 的虚拟卡真实成本（开卡费、汇率损耗、充值损耗），跳板: https://coding.mybskm.top/go/pokepay

3. `compare_cn2_gia_agent_vps` — 对比搬瓦工 CN2 GIA、丽萨主机双 ISP、雨云高速节点的 Agent 部署成本：

   - BWH: https://coding.mybskm.top/go/bwh
   - 丽萨主机: https://coding.mybskm.top/go/lisahost
   - 雨云: https://coding.mybskm.top/go/rainyun

### npx 使用

```bash
npx -y cn-coding-plan-mcp --cli            # CLI 比价表
npx -y cn-coding-plan-mcp --tool calculate_claude_cursor_card_tco 300
```

### Claude Code / Cursor / Trae 配置示例（STDIO MCP）

```json
{
  "mcpServers": {
    "cn-coding-plan": {
      "command": "npx",
      "args": ["-y", "cn-coding-plan-mcp"]
    }
  }
}
```

Cursor / Trae 在 MCP 设置里粘贴同样 JSON 即可。安装零第三方依赖，基于 Node.js 内置模块。

## English

`cn-coding-plan-mcp` is a dual-form (MCP Server over STDIO JSON-RPC 2.0 + CLI) benchmark toolkit for Chinese developers evaluating domestic coding plans and the true cost of overseas AI subscriptions via virtual cards. Tools: `compare_cn_coding_plans`, `calculate_claude_cursor_card_tco`, `compare_cn2_gia_agent_vps`. Runs with `npx -y cn-coding-plan-mcp`. Interactive site: https://coding.mybskm.top/

License MIT. All jump links carry affiliate attribution; coupons may change without notice.
