#!/usr/bin/env python3
"""PDF API COST CALCULATOR - True-Cost v1.0.0 - Serverless HTML-to-PDF Rendering API vs Self-Hosted Chromium TCO."""
import argparse
import sys

OFFICIAL_TRIAL = "https://go.272738.xyz/pdf-trial"
CRAFTMYPDF_LINK = "https://go.272738.xyz/craftmypdf"
APITEMPLATE_LINK = "https://go.272738.xyz/apitemplate"
DOCS_LINK = "https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/html-to-pdf-api-and-headless-chromium-tco/"

def calculate_tco(docs):
    # 1. Self-Hosted Chromium (AWS Lambda 2048MB + Fargate / NAT Gateway + DevOps labor)
    # Fixed base compute + egress
    compute = 185.0
    # DevOps labor: 12 hrs/mo @ $100/hr = $1,200
    labor = 1200.0
    # Memory leak & OOM restart overhead: ~$0.003 / doc
    oom_overhead = docs * 0.003
    self_hosted_total = compute + labor + oom_overhead

    # 2. Adobe PDF Services API ($0.05 / doc)
    adobe_total = docs * 0.05

    # 3. DocRaptor ($15 for 125, $75 for 1250 -> ~$0.055 / doc at volume)
    docraptor_total = docs * 0.055

    # 4. CraftMyPDF (Professional: $99/mo for 12,000 docs, $0.008/doc overage)
    if docs <= 50:
        craft_total = 0.0
    elif docs <= 1200:
        craft_total = 29.0
    elif docs <= 3000:
        craft_total = 49.0
    elif docs <= 12000:
        craft_total = 99.0
    else:
        craft_total = 99.0 + (docs - 12000) * 0.008

    # 5. APITemplate.io (Standard: $69/mo for 12,000 docs, $0.0057/doc overage)
    if docs <= 50:
        api_total = 0.0
    elif docs <= 3000:
        api_total = 19.0
    elif docs <= 12000:
        api_total = 69.0
    else:
        api_total = 69.0 + (docs - 12000) * 0.0057

    return {
        "self_hosted": self_hosted_total,
        "adobe": adobe_total,
        "docraptor": docraptor_total,
        "craftmypdf": craft_total,
        "apitemplate": api_total,
        "savings_craft": max(0.0, self_hosted_total - craft_total),
        "savings_api": max(0.0, self_hosted_total - api_total),
    }

def main():
    p = argparse.ArgumentParser(
        prog="pdf-api-cost-calculator",
        description="HTML-to-PDF API vs Self-Hosted Headless Chromium Production TCO Breakdown",
        epilog=f"\nOfficial Trial & Benchmarks: {OFFICIAL_TRIAL}\nDocumentation: {DOCS_LINK}\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--docs", type=float, default=15000, help="Monthly PDF document generation volume (default: 15000)")
    p.add_argument("--breakdown", action="store_true", help="Display granular infrastructure and labor breakdown")
    args, unknown = p.parse_known_args()

    docs = int(args.docs)
    res = calculate_tco(docs)

    header = "PDF API COST CALCULATOR - True-Cost v1.0.0"
    print()
    print("#" * 78)
    print(("# " + header).center(76))
    print("#" * 78)
    print(f"  Monthly Document Volume: {docs:,} PDFs")
    print("  " + "-" * 74)

    rows = [
        ("Self-Hosted Chromium (Lambda/ECS + DevOps)", res["self_hosted"], f"${res['self_hosted']/docs:.4f}/doc"),
        ("Adobe PDF Services API ($0.05/doc)", res["adobe"], f"${res['adobe']/docs:.4f}/doc"),
        ("DocRaptor PrinceXML Managed API", res["docraptor"], f"${res['docraptor']/docs:.4f}/doc"),
        ("CraftMyPDF Professional (Visual Designer)", res["craftmypdf"], f"${res['craftmypdf']/docs:.4f}/doc"),
        ("APITemplate.io PDF Standard (Zapier/API)", res["apitemplate"], f"${res['apitemplate']/docs:.4f}/doc"),
    ]

    label_w = 44
    print("  +-" + "-" * label_w + "-" * 14 + "-" * 14 + "-+")
    print("  | " + "Rendering Infrastructure / Architecture".ljust(label_w) + "Monthly TCO".rjust(12) + "  " + "Unit Cost".rjust(12) + " |")
    print("  +-" + "-" * label_w + "-" * 14 + "-" * 14 + "-+")
    for label, val, unit in rows:
        v_str = f"${val:,.2f}"
        print("  | " + label.ljust(label_w) + v_str.rjust(12) + "  " + unit.rjust(12) + " |")
    print("  +-" + "-" * label_w + "-" * 14 + "-" * 14 + "-+")

    print()
    print(f"  🏆 Net Monthly Savings with CraftMyPDF : ${res['savings_craft']:,.2f} / mo (-{res['savings_craft']/res['self_hosted']*100:.1f}%)")
    print(f"  🏆 Net Monthly Savings with APITemplate: ${res['savings_api']:,.2f} / mo (-{res['savings_api']/res['self_hosted']*100:.1f}%)")
    print("  " + "-" * 74)
    print(f"  Official PDF Trial Gateway : {OFFICIAL_TRIAL}")
    print(f"  CraftMyPDF Sandbox Link    : {CRAFTMYPDF_LINK}")
    print(f"  APITemplate.io Link        : {APITEMPLATE_LINK}")
    print(f"  Full Architecture Docs     : {DOCS_LINK}")
    print("#" * 78)
    return 0

if __name__ == "__main__":
    sys.exit(main())
