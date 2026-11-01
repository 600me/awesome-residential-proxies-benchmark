"""crossborder-cost-mcp server: STDIO JSON-RPC 2.0 MCP + --cli mode.

Pure Python standard library (sys, json). Author: CloudBench Research (MIT).
"""
import json
import sys

VERSION = "1.0.1"
SITE = "https://cbcost.mybskm.top/"

LINKS = {
    "adspower": "https://cbcost.mybskm.top/go/adspower",
    "morelogin": "https://cbcost.mybskm.top/go/morelogin",
    "bitbrowser": "https://cbcost.mybskm.top/go/bitbrowser",
    "duoplus": "https://coding.mybskm.top/go/duoplus",
    "lisahost": "https://coding.mybskm.top/go/lisahost",
}


def calculate_antidetect_browser_tco(args=None):
    args = args or {}
    profiles = max(10, int(args.get("profiles") or 100))
    seats = max(1, int(args.get("seats") or 3))
    diy_infra, diy_incident = 450.0, 620.0
    rows = []
    for vendor, usd in (
        ("AdsPower", 49 + seats * 29),
        ("MoreLogin", 39 + seats * 25),
        ("BitBrowser", 35 + seats * 22),
    ):
        rows.append({
            "vendor": vendor,
            "usd_monthly": usd,
            "usd_per_profile_per_month": round(usd / profiles, 3),
            "usd_annual": usd * 12,
        })
    return {
        "benchmark": "antidetect-team-tco-2026",
        "inputs": {"profiles": profiles, "seats": seats},
        "rows": rows,
        "diy_fleet_baseline": {
            "usd_monthly_infra": diy_infra,
            "usd_monthly_incidents": diy_incident,
            "usd_monthly": diy_infra + diy_incident,
            "failure_modes": ["webgl/canvas leak linking profiles", "chrome OOM on 200 tabs", "proxy pool contention"],
        },
        "actions": {"adspower": LINKS["adspower"], "morelogin": LINKS["morelogin"], "bitbrowser": LINKS["bitbrowser"]},
        "interactive_site": SITE,
    }


def calculate_cloudphone_matrix_tco(args=None):
    args = args or {}
    devices = max(5, int(args.get("devices") or 50))
    unit = 0.36  # DuoPlus 每台/日折算
    cloud_monthly = round(devices * unit * 30, 2)
    # 基线: 海外实体机房真机 + 漫游卡池 (50台基准 850 USD/mo, 即 17 USD/台/月)
    real_monthly = devices * 17
    return {
        "benchmark": "cloudphone-tiktok-matrix-2026",
        "inputs": {"devices": devices},
        "duoplus": {"usd_monthly": cloud_monthly, "usd_per_device": round(cloud_monthly / devices, 2)},
        "real_phone_fleet": {"usd_monthly": real_monthly, "baseline": "海外实体机房真机+漫游卡池"},
        "savings": {
            "usd_monthly_vs_real": round(real_monthly - cloud_monthly, 2),
            "pct": max(0.0, round((real_monthly - cloud_monthly) / real_monthly * 100, 1)),
        },
        "action": LINKS["duoplus"],
        "interactive_site": SITE,
    }


def calculate_static_isp_proxy_tco(args=None):
    args = args or {}
    gb = max(10, int(args.get("monthly_gb") or 500))
    rotating = gb * 12.5
    static_isp_monthly = 29
    units = max(1, -(-gb // 1000))
    static_cost = units * static_isp_monthly
    return {
        "benchmark": "static-isp-proxy-tco-2026",
        "inputs": {"monthly_gb": gb},
        "rotating_residential": {"usd_monthly": rotating, "usd_per_gb": 12.5},
        "static_isp_vps": {
            "usd_monthly": static_cost,
            "units_needed": units,
            "vendor": "LisaHost dual-ISP residential",
            "advantage": "IP 归属稳定, 平台风控通过率高, 长会话不掉线",
        },
        "savings": {
            "usd_monthly": round(rotating - static_cost, 2),
            "usd_annual": round((rotating - static_cost) * 12, 2),
        },
        "action": LINKS["lisahost"],
        "interactive_site": SITE,
    }


TOOLS = [
    {
        "name": "calculate_antidetect_browser_tco",
        "description": "Compare AdsPower vs MoreLogin vs BitBrowser team seats against a DIY fingerprint VM fleet.",
        "inputSchema": {"type": "object", "properties": {"profiles": {"type": "number"}, "seats": {"type": "number"}}},
    },
    {
        "name": "calculate_cloudphone_matrix_tco",
        "description": "Calculate DuoPlus cloud phone batch farming cost vs real-phone TikTok matrix fleet.",
        "inputSchema": {"type": "object", "properties": {"devices": {"type": "number"}}},
    },
    {
        "name": "calculate_static_isp_proxy_tco",
        "description": "Calculate LisaHost dual-ISP static residential cost vs rotating residential proxies per GB.",
        "inputSchema": {"type": "object", "properties": {"monthly_gb": {"type": "number", "default": 500}}},
    },
]

HANDLERS = {
    "calculate_antidetect_browser_tco": calculate_antidetect_browser_tco,
    "calculate_cloudphone_matrix_tco": calculate_cloudphone_matrix_tco,
    "calculate_static_isp_proxy_tco": calculate_static_isp_proxy_tco,
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
                "serverInfo": {"name": "crossborder-cost-mcp", "version": VERSION},
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
    r1 = calculate_antidetect_browser_tco({"profiles": 100, "seats": 3})
    r2 = calculate_cloudphone_matrix_tco({"devices": 50})
    r3 = calculate_static_isp_proxy_tco({"monthly_gb": 500})
    if tool == "calculate_antidetect_browser_tco":
        print(json.dumps(r1, ensure_ascii=False, indent=2))
    elif tool == "calculate_cloudphone_matrix_tco":
        print(json.dumps(r2, ensure_ascii=False, indent=2))
    elif tool == "calculate_static_isp_proxy_tco":
        print(json.dumps(r3, ensure_ascii=False, indent=2))
    else:
        print("== 指纹浏览器团队席 TCO (100 profiles / 3 seats) ==")
        for r in r1["rows"]:
            print("- %s: $%s/mo (每环境 $%s/mo)" % (r["vendor"], r["usd_monthly"], r["usd_per_profile_per_month"]))
        print("AdsPower → %s | MoreLogin → %s" % (LINKS["adspower"], LINKS["morelogin"]))
        print("DIY 自建基线: $%s/mo" % r1["diy_fleet_baseline"]["usd_monthly"])
        print("\n== 云手机 TikTok 矩阵 (50 devices) ==")
        print("- DuoPlus: $%s/mo vs 真机 $%s/mo (省 %s%%) → %s" % (
            r2["duoplus"]["usd_monthly"], r2["real_phone_fleet"]["usd_monthly"],
            r2["savings"]["pct"], r2["action"]))
        print("\n== 静态 ISP 代理 (500 GB/月) ==")
        print("- 轮换住宅: $%s/mo vs 静态ISP VPS: $%s/mo (年省 $%s) → %s" % (
            r3["rotating_residential"]["usd_monthly"], r3["static_isp_vps"]["usd_monthly"],
            r3["savings"]["usd_annual"], r3["action"]))
        print("主站:", SITE)


def main():
    if "--cli" in sys.argv[1:]:
        cli()
    else:
        serve()
    return 0
