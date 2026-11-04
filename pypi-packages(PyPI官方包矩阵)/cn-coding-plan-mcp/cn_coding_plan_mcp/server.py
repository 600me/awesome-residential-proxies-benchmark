"""cn-coding-plan-mcp server: STDIO JSON-RPC 2.0 MCP + --cli mode.

Pure Python standard library (sys, json). Author: CloudBench Research (MIT).
"""
import json
import sys

VERSION = "1.0.1"
SITE = "https://coding.mybskm.top/"

LINKS = {
    "aliyun_coding": "https://coding.mybskm.top/go/aliyun-coding",
    "aliyun_dashi": "https://coding.mybskm.top/go/aliyun-dashi",
    "volcengine": "https://coding.mybskm.top/go/volcengine-coding",
    "zhipu": "https://coding.mybskm.top/go/zhipu-glm",
    "tencent": "https://coding.mybskm.top/go/tencent-double11",
    "bwh": "https://coding.mybskm.top/go/bwh",
    "rainyun": "https://coding.mybskm.top/go/rainyun",
    "lisahost": "https://coding.mybskm.top/go/lisahost",
}


def compare_cn_coding_plans(args=None):
    return {
        "benchmark": "cn-coding-plan-2026",
        "best_for": "Claude Code / Cursor / Trae 国内合规接入",
        "rows": [
            {"vendor": "Aliyun百炼 Coding Plan", "entry": "¥49/月起", "quota": "Token 包梯度", "action": LINKS["aliyun_coding"]},
            {"vendor": "阿里云大模型推理 (Dashi)", "entry": "新客代金券", "quota": "按量 + 预付折扣", "action": LINKS["aliyun_dashi"]},
            {"vendor": "火山方舟 Volcengine", "entry": "首发抵扣券", "quota": "按量 + 资源包", "action": LINKS["volcengine"]},
            {"vendor": "智谱 GLM Coding", "entry": "GLM 包月订阅", "quota": "不限速 Coding", "action": LINKS["zhipu"]},
            {"vendor": "腾讯云轻量/双11", "entry": "轻量服务器折扣", "quota": "年度券包", "action": LINKS["tencent"]},
        ],
        "interactive_site": SITE,
    }


def calculate_claude_cursor_card_tco(args=None):
    args = args or {}
    monthly_usd = max(1, float(args.get("monthly_usd") or 200))
    fx_loss_pct = 2.5
    open_card_fee = 9.9
    topup_fee_pct = 1.0
    card_monthly = monthly_usd * (1 + (fx_loss_pct + topup_fee_pct) / 100)
    return {
        "benchmark": "claude-cursor-card-tco-2026",
        "inputs": {"monthly_usd": monthly_usd},
        "card_route": {
            "fx_loss_pct": fx_loss_pct,
            "topup_loss_pct": topup_fee_pct,
            "open_card_fee_usd": open_card_fee,
            "usd_monthly_effective": round(card_monthly, 2),
            "usd_annual_effective": round(card_monthly * 12 + open_card_fee, 2),
            "pain_points": ["风控拒付", "汇率二次损耗", "余额沉淀"],
        },
        "action": LINKS["lisahost"],
        "action_domestic": LINKS["aliyun_coding"],
        "interactive_site": SITE,
    }


def compare_cn2_gia_agent_vps(args=None):
    return {
        "benchmark": "cn2-gia-agent-vps-2026",
        "rows": [
            {"vendor": "BWH 搬瓦工 CN2 GIA", "region": "DC6/DC9", "price": "$49.99/年起", "action": LINKS["bwh"]},
            {"vendor": "雨云 Rainyun 高速节点", "region": "华东出口", "price": "¥/月起", "action": LINKS["rainyun"]},
            {"vendor": "丽萨主机 LisaHost 双ISP", "region": "住宅 IP", "price": "按流量/静态", "action": LINKS["lisahost"]},
        ],
        "interactive_site": SITE,
    }


TOOLS = [
    {
        "name": "compare_cn_coding_plans",
        "description": "Compare CN coding plans (Aliyun Bailian, Volcengine Ark, Zhipu GLM, Tencent) with coupon jump links.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "calculate_claude_cursor_card_tco",
        "description": "Calculate TCO of overseas AI subscriptions via virtual card (open fee, FX & top-up loss).",
        "inputSchema": {"type": "object", "properties": {"monthly_usd": {"type": "number"}}},
    },
    {
        "name": "compare_cn2_gia_agent_vps",
        "description": "Compare CN2 GIA / dual-ISP agent VPS (BWH, LisaHost, Rainyun) with jump links.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]

HANDLERS = {
    "compare_cn_coding_plans": compare_cn_coding_plans,
    "calculate_claude_cursor_card_tco": calculate_claude_cursor_card_tco,
    "compare_cn2_gia_agent_vps": compare_cn2_gia_agent_vps,
}


def _send(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def serve():
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except ValueError:
            continue
        msg_id, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
        if method == "initialize":
            _send({"jsonrpc": "2.0", "id": msg_id, "result": {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "cn-coding-plan-mcp", "version": VERSION},
            }})
        elif method == "notifications/initialized":
            pass
        elif method == "ping":
            _send({"jsonrpc": "2.0", "id": msg_id, "result": {}})
        elif method == "tools/list":
            _send({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}})
        elif method == "tools/call":
            handler = HANDLERS.get(params.get("name"))
            if not handler:
                _send({"jsonrpc": "2.0", "id": msg_id,
                       "error": {"code": -32602, "message": "Unknown tool: %s" % params.get("name")}})
                continue
            result = handler(params.get("arguments"))
            _send({"jsonrpc": "2.0", "id": msg_id, "result": {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                "structuredContent": result,
            }})
        elif msg_id is not None:
            _send({"jsonrpc": "2.0", "id": msg_id,
                   "error": {"code": -32601, "message": "Method not found: %s" % method}})


def cli(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if "--cli" in argv:
        argv = [a for a in argv if a != "--cli"]
    if "--tool" in argv:
        i = argv.index("--tool")
        tool = argv[i + 1] if i + 1 < len(argv) else "all"
        del argv[i:i + 2]
    else:
        tool = "all"
    if tool == "compare_cn_coding_plans":
        print(json.dumps(compare_cn_coding_plans(), ensure_ascii=False, indent=2))
    elif tool == "calculate_claude_cursor_card_tco":
        monthly = float(argv[0]) if argv and argv[0].replace(".", "", 1).isdigit() else 200.0
        print(json.dumps(calculate_claude_cursor_card_tco({"monthly_usd": monthly}), ensure_ascii=False, indent=2))
    elif tool == "compare_cn2_gia_agent_vps":
        print(json.dumps(compare_cn2_gia_agent_vps(), ensure_ascii=False, indent=2))
    else:
        print("== CN Coding Plan 比价 ==")
        for r in compare_cn_coding_plans()["rows"]:
            print("- %s (%s) → %s" % (r["vendor"], r["entry"], r["action"]))
        print("主站:", SITE)
        r2 = calculate_claude_cursor_card_tco({"monthly_usd": 200})
        print("\n== Claude/Cursor 虚拟卡 TCO (200 USD/月) ==")
        print("- 月度实际: $%s/月, 年度 $%s → %s" % (
            r2["card_route"]["usd_monthly_effective"],
            r2["card_route"]["usd_annual_effective"], r2["action"]))


def main():
    argv = sys.argv[1:]
    if "--cli" in argv:
        cli()
    else:
        serve()
    return 0
