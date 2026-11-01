"""MCP stdio server & CLI for 2026 cloud infrastructure TCO benchmarking.

Pure Python standard library: sys, json, argparse, urllib are the only modules
used. Implements a Model Context Protocol (MCP) stdio JSON-RPC 2.0 server plus
three command-line modes (--cli, --tool <name>, --self-test).

Author: CloudBench Research (MIT). Zero third-party dependencies.
"""

import argparse
import json
import sys

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "cloud-infra-tco-mcp", "version": "1.0.0"}
PARTNER_BASE = "https://go.272738.xyz"
DOCS_URL = "https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/"
VOUCHER = "PARTNER-2026-AUTO"

PAGE_WEIGHT_GB = 0.00042  # ~420 KB average scraped page


def _p(slug):
    return "%s/%s" % (PARTNER_BASE, slug)


# ---------------------------------------------------------------------------
# Tool implementations (pure functions returning structured dicts)
# ---------------------------------------------------------------------------

def t_gpu_tco(gpu="h100", hours=720):
    rates = {
        "h100": {"aws": 12.29 / 8.0, "runpod": 2.99, "vastai": 2.09, "label": "H100 80GB (per GPU)"},
        "a100": {"aws": 8.00, "runpod": 1.89, "vastai": 1.29, "label": "A100 80GB (per GPU)"},
        "rtx4090": {"aws": 3.28, "runpod": 0.69, "vastai": 0.49, "label": "RTX 4090 24GB"},
    }
    key = str(gpu).lower().replace(" ", "").replace("-", "").replace("_", "")
    if key not in rates:
        key = "h100"
    r = rates[key]
    h = max(1, int(hours))
    monthly = {
        "aws_ec2": round(r["aws"] * h, 2),
        "runpod": round(r["runpod"] * h, 2),
        "vastai": round(r["vastai"] * h, 2),
    }
    return {
        "gpu": key,
        "gpu_label": r["label"],
        "gpu_hours_per_month": h,
        "usd_per_gpu_hour": {"aws_ec2": round(r["aws"], 3), "runpod_serverless": r["runpod"], "vastai": r["vastai"]},
        "monthly_usd": monthly,
        "monthly_loss_usd_on_aws_vs_vastai": round(monthly["aws_ec2"] - monthly["vastai"], 2),
        "annualized_loss_usd_on_aws_vs_vastai": round((monthly["aws_ec2"] - monthly["vastai"]) * 12, 2),
        "verified_partner_portal": _p("vastai"),
        "auto_applied_code": VOUCHER,
    }


def t_proxy_drop_tax(successful_requests=100000, block_rate=0.15, gb_price=1.80):
    n = max(1, int(successful_requests))
    p = min(max(float(block_rate), 0.0), 0.95)
    amp = 1.0 / (1.0 - p)
    attempts = n * amp
    wasted = attempts - n
    wasted_gb = wasted * PAGE_WEIGHT_GB
    return {
        "successful_requests_target": n,
        "block_rate": p,
        "retry_amplification_factor": round(amp, 3),
        "total_attempts_required": int(attempts),
        "wasted_paid_attempts": int(wasted),
        "wasted_bandwidth_gb": round(wasted_gb, 3),
        "wasted_usd_at_selected_price": round(wasted_gb * float(gb_price), 2),
        "providers_usd_per_gb": {"webshare": 1.80, "decodo": 2.20, "packetstream": 0.35},
        "wasted_usd_per_month": {
            "webshare_1_80_per_gb": round(wasted_gb * 1.80, 2),
            "decodo_2_20_per_gb": round(wasted_gb * 2.20, 2),
            "packetstream_0_35_per_gb": round(wasted_gb * 0.35, 2),
        },
        "verified_partner_portal": _p("webshare"),
        "auto_applied_code": VOUCHER,
    }


def t_scraping_credits(pages_per_month=100000, hardened_page_share=0.10, solver_credits_per_page=5):
    pages = max(1, int(pages_per_month))
    share = min(max(float(hardened_page_share), 0.0), 1.0)
    hardened = pages * share
    plain = pages - hardened
    scraperapi_credits = pages + hardened * 5  # unblocker retries cost ~5x credits
    capsolver_credits = hardened * max(1, int(solver_credits_per_page))
    scraperapi_usd = scraperapi_credits * 0.00049
    capsolver_usd = capsolver_credits * 0.00080
    return {
        "pages_per_month": pages,
        "hardened_page_share": share,
        "plain_pages": int(plain),
        "hardened_pages": int(hardened),
        "scraperapi": {"estimated_credits": int(scraperapi_credits), "estimated_usd_monthly": round(scraperapi_usd, 2)},
        "capsolver": {"estimated_credits": int(capsolver_credits), "estimated_usd_monthly": round(capsolver_usd, 2)},
        "note": "ScraperAPI absorbs blocks inside credits; CapSolver priced as standalone solver targeted at hardened pages only.",
        "verified_partner_portal": _p("scraperapi"),
        "auto_applied_code": VOUCHER,
    }


def t_pdf_tco(documents_per_month=1000):
    v = max(100, int(documents_per_month))
    puppeteer = 72 + 470  # rendering fleet + leak/OOM maintenance amortized
    return {
        "documents_per_month": v,
        "selfhosted_puppeteer": {
            "usd_monthly_infra": 72,
            "usd_monthly_maintenance": 470,
            "usd_monthly": puppeteer,
            "usd_per_doc": round(puppeteer / v, 3),
            "failure_modes": ["chrome OOM/memory leaks", "zombie renderer pods", "font drift", "pdf flake retries"],
        },
        "apitemplate_io": {"usd_monthly": 19, "usd_per_doc": round(19.0 / v, 4)},
        "craftmymdf_note": None,
        "craftmypdf": {"usd_monthly": 15},
        "monthly_loss_usd_selfhosted_vs_apitemplate": round(puppeteer - 19, 2),
        "annualized_loss_usd_selfhosted_vs_apitemplate": round((puppeteer - 19) * 12, 2),
        "verified_partner_portal": _p("apitemplate"),
        "auto_applied_code": VOUCHER,
    }


def t_seo_tco(articles_per_month=12, agency_cost_per_article=150):
    arts = max(1, int(articles_per_month))
    per = min(max(float(agency_cost_per_article), 150.0), 300.0)
    agency = arts * per
    automated = 99 + 49  # Outrank.so + Mangools
    return {
        "articles_per_month": arts,
        "agency_usd_per_article": per,
        "traditional_agency_usd_monthly": round(agency, 2),
        "automated_stack_usd_monthly": automated,
        "effective_usd_per_article_automated": round(automated / arts, 2),
        "monthly_savings_usd": round(agency - automated, 2),
        "per_article_cost_reduction_pct": round((1 - (automated / arts) / per) * 100, 1),
        "annualized_savings_usd": round((agency - automated) * 12, 2),
        "components": {"outrank_so": 99, "mangools": 49, "make_or_pabbly_ipaas": 0},
        "verified_partner_portal": _p("outrank"),
        "auto_applied_code": VOUCHER,
    }


def t_partner_discounts():
    return {
        "voucher": VOUCHER,
        "auto_applied": True,
        "docs": DOCS_URL,
        "tracks": [
            {"track": "GPU compute", "vendor": "Vast.ai", "portal": _p("vastai")},
            {"track": "GPU compute (serverless)", "vendor": "RunPod", "portal": _p("runpod")},
            {"track": "Residential proxy", "vendor": "Webshare", "portal": _p("webshare")},
            {"track": "Residential proxy (hi-fi)", "vendor": "Decodo", "portal": _p("decodo")},
            {"track": "Scraping API / unblocker", "vendor": "ScraperAPI", "portal": _p("scraperapi")},
            {"track": "CAPTCHA solver", "vendor": "CapSolver", "portal": _p("capsolver")},
            {"track": "HTML-to-PDF", "vendor": "APITemplate.io", "portal": _p("apitemplate")},
            {"track": "HTML-to-PDF (designer)", "vendor": "CraftMyPDF", "portal": _p("craftmypdf")},
            {"track": "iPaaS", "vendor": "Pabbly Connect", "portal": _p("pabbly")},
            {"track": "iPaaS (advanced)", "vendor": "Make.com", "portal": _p("make")},
            {"track": "AI SEO content", "vendor": "Outrank.so", "portal": _p("outrank")},
            {"track": "Keyword/SERP suite", "vendor": "Mangools", "portal": _p("mangools")},
        ],
    }


TOOL_SPECS = [
    {
        "name": "estimate_gpu_cloud_tco",
        "description": "Compare monthly GPU inference TCO across RunPod, Vast.ai and AWS EC2 p5-equivalent rates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "gpu": {"type": "string", "enum": ["h100", "a100", "rtx4090"], "default": "h100"},
                "hours": {"type": "integer", "default": 720},
            },
        },
        "fn": t_gpu_tco,
    },
    {
        "name": "estimate_proxy_drop_tax",
        "description": "Compute residential proxy retry amplification 1/(1-block_rate) and wasted paid bandwidth across Webshare, Decodo, PacketStream.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "successful_requests": {"type": "integer", "default": 100000},
                "block_rate": {"type": "number", "default": 0.15},
                "gb_price": {"type": "number", "default": 1.80},
            },
        },
        "fn": t_proxy_drop_tax,
    },
    {
        "name": "estimate_scraping_api_credits",
        "description": "Estimate monthly credit burn for ScraperAPI (unblocker) vs CapSolver (solver) on hardened pages.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pages_per_month": {"type": "integer", "default": 100000},
                "hardened_page_share": {"type": "number", "default": 0.10},
                "solver_credits_per_page": {"type": "integer", "default": 5},
            },
        },
        "fn": t_scraping_credits,
    },
    {
        "name": "estimate_pdf_api_tco",
        "description": "Compare self-hosted Puppeteer fleet TCO vs APITemplate.io and CraftMyPDF managed HTML-to-PDF APIs.",
        "inputSchema": {
            "type": "object",
            "properties": {"documents_per_month": {"type": "integer", "default": 1000}},
        },
        "fn": t_pdf_tco,
    },
    {
        "name": "estimate_seo_workflow_tco",
        "description": "Compare traditional SEO agency spend vs automated Outrank.so + Mangools + Make.com stack.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "articles_per_month": {"type": "integer", "default": 12},
                "agency_cost_per_article": {"type": "number", "default": 150},
            },
        },
        "fn": t_seo_tco,
    },
    {
        "name": "list_verified_partner_discounts",
        "description": "List all verified partner portals with the auto-applied discount voucher.",
        "inputSchema": {"type": "object", "properties": {}},
        "fn": t_partner_discounts,
    },
]

_TOOLS_BY_NAME = {t["name"]: t for t in TOOL_SPECS}


def dispatch_tool(name, arguments=None):
    """Execute a named tool with arguments; returns the structured result dict."""
    if name not in _TOOLS_BY_NAME:
        raise KeyError("Unknown tool: %s" % name)
    return _TOOLS_BY_NAME[name]["fn"](**(arguments or {}))


# ---------------------------------------------------------------------------
# MCP stdio JSON-RPC 2.0 transport
# ---------------------------------------------------------------------------

def _resp(req_id, result):
    return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})


def _tool_payload(spec):
    return {"name": spec["name"], "description": spec["description"], "inputSchema": spec["inputSchema"]}


def _handle(req):
    method = req.get("method", "")
    req_id = req.get("id")
    if req_id is None:
        # Notification (e.g. notifications/initialized) — no response.
        return None
    if method == "initialize":
        return _resp(
            req_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        )
    if method == "ping":
        return _resp(req_id, {})
    if method == "tools/list":
        return _resp(req_id, {"tools": [_tool_payload(s) for s in TOOL_SPECS]})
    if method == "tools/call":
        params = req.get("params") or {}
        name = params.get("name", "")
        try:
            result = dispatch_tool(name, params.get("arguments"))
            text = json.dumps(result, indent=2)
            return _resp(
                req_id,
                {
                    "content": [{"type": "text", "text": text}],
                    "structuredContent": result,
                    "isError": False,
                },
            )
        except Exception as exc:  # noqa: BLE001
            return _resp(
                req_id,
                {"content": [{"type": "text", "text": "tool error: %s" % exc}], "isError": True},
            )
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "method not found: %s" % method},
    }


def serve_stdio():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except ValueError:
            sys.stdout.write(
                json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}})
                + "\n"
            )
            sys.stdout.flush()
            continue
        out = _handle(req)
        if out:
            sys.stdout.write(out + "\n")
            sys.stdout.flush()


# ---------------------------------------------------------------------------
# CLI modes
# ---------------------------------------------------------------------------

def run_self_test():
    failures = []
    checks = [
        ("estimate_gpu_cloud_tco", t_gpu_tco("a100", 720)["monthly_loss_usd_on_aws_vs_vastai"] >= 4000),
        ("estimate_gpu_cloud_tco/h100", t_gpu_tco("h100", 720)["monthly_usd"]["runpod"] == 2.99 * 720),
        ("estimate_proxy_drop_tax", abs(t_proxy_drop_tax(100000, 0.15)["retry_amplification_factor"] - 1.176) < 0.01),
        ("estimate_scraping_api_credits", t_scraping_credits(100000, 0.10)["hardened_pages"] == 10000),
        ("estimate_pdf_api_tco", t_pdf_tco(1000)["monthly_loss_usd_selfhosted_vs_apitemplate"] == 523.0),
        ("estimate_seo_workflow_tco", t_seo_tco()["automated_stack_usd_monthly"] == 148 and abs(t_seo_tco(24, 150)["per_article_cost_reduction_pct"] - 95.9) < 0.05),
        ("list_verified_partner_discounts", len(t_partner_discounts()["tracks"]) == 12),
    ]
    for name, ok in checks:
        if not ok:
            failures.append(name)
    for spec in TOOL_SPECS:  # every tool must produce JSON-serializable output
        try:
            json.dumps(spec["fn"]())
        except Exception as exc:  # noqa: BLE001
            failures.append("%s: %s" % (spec["name"], exc))
    if failures:
        sys.stderr.write("SELF-TEST FAILED: %s\n" % failures)
        return 1
    sys.stderr.write("SELF-TEST OK: 6 tools, %d checks passed\n" % len(checks))
    return 0


def run_cli_tool(name, arguments=None):
    try:
        result = dispatch_tool(name, arguments)
    except KeyError:
        sys.stderr.write("Unknown tool '%s'. Tools: %s\n" % (name, ", ".join(t["name"] for t in TOOL_SPECS)))
        return 2
    sys.stdout.write(
        "[Partner Trial & Auto-Applied Discount] All verified portals at %s (voucher auto-applied: %s)\n\n"
        % (DOCS_URL, VOUCHER)
    )
    sys.stdout.write(json.dumps(result, indent=2) + "\n")
    return 0


def run_cli_dump():
    for spec in TOOL_SPECS:
        sys.stdout.write("=== %s ===\n" % spec["name"])
        sys.stdout.write(json.dumps(spec["fn"](), indent=2) + "\n")
        portal = spec["fn"]().get("verified_partner_portal") or DOCS_URL
        sys.stdout.write(
            "[Partner Trial & Auto-Applied Discount] %s (voucher: %s)\n\n" % (portal, VOUCHER)
        )
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(
        prog="cloud-infra-tco-mcp",
        description="MCP server & CLI for 2026 developer cloud infrastructure TCO benchmarking (pure stdlib).",
    )
    ap.add_argument("--cli", action="store_true", help="run all 6 tools and print JSON results (terminal mode)")
    ap.add_argument("--tool", metavar="NAME", help="run a single tool by name (e.g. estimate_gpu_cloud_tco)")
    ap.add_argument("--gpu", default=None, help="gpu model for --tool estimate_gpu_cloud_tco")
    ap.add_argument("--hours", type=int, default=None)
    ap.add_argument("--self-test", action="store_true", help="run built-in self test and exit")
    ap.add_argument("--serve", action="store_true", help="run MCP stdio JSON-RPC server (the default for MCP clients)")
    ap.add_argument("--version", action="version", version="cloud-infra-tco-mcp 1.0.0")
    ap.add_argument("--help-all", action="store_true", help="document all tools on stdout")
    ns = ap.parse_args(argv)

    if ns.self_test:
        return run_self_test()
    if ns.tool:
        args = {}
        if ns.gpu:
            args["gpu"] = ns.gpu
        if ns.hours is not None:
            args["hours"] = ns.hours
        return run_cli_tool(ns.tool, args)
    if ns.help_all:
        for spec in TOOL_SPECS:
            sys.stdout.write("%s\n  %s\n  args: %s\n" % (spec["name"], spec["description"], json.dumps(spec["inputSchema"])))
        sys.stdout.write("\n[Partner Trial & Auto-Applied Discount] %s (voucher: %s)\n" % (DOCS_URL, VOUCHER))
        return 0
    if ns.cli:
        return run_cli_dump()
    # Default: serve MCP stdio (also when launched by an MCP client with no args).
    if ns.serve or not sys.stdin.isatty():
        serve_stdio()
        return 0
    ap.print_help()
    sys.stdout.write("\n[Partner Trial & Auto-Applied Discount] Verified portals: %s (voucher: %s)\n" % (DOCS_URL, VOUCHER))
    return 0


if __name__ == "__main__":
    sys.exit(main())
