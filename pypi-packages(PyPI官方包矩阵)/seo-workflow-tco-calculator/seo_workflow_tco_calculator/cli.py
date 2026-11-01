#!/usr/bin/env python3
"""
SEO Suite & iPaaS Workflow Automation TCO Benchmark Calculator.
Provides reproducible cost calculations for modern SaaS growth stacks.
"""
import argparse
import sys

def calculate_seo_tco(seats=2, blog_posts=30):
    # Ahrefs 2026 pricing:
    # Starter $29/mo (200 credits, 1 user)
    # Lite $129/mo (1,000 credits, extra seats +$40/mo/user)
    # 2-seat team: $129 + $40 = $169/mo ($2,028/yr) monthly, ~$1,690/yr annual
    ahrefs_monthly = 129.0 + max(0, seats - 1) * 40.0
    ahrefs_annual = ahrefs_monthly * 12

    # Semrush 2026 pricing:
    # SEO $139/mo ($117.33/mo annual), Starter $199/mo, Pro+ $299/mo
    semrush_monthly = 139.0
    semrush_annual = 117.33 * 12

    # Mangools 2026 pricing (https://go.272738.xyz/mangools):
    # Basic $37.70/mo ($452.40/yr), Premium $52.70/mo ($632.40/yr, includes 3 extra seats), Agency $97.70/mo ($1,172.40/yr)
    if seats <= 1:
        mangools_plan = "Mangools Basic"
        mangools_monthly = 37.70
        mangools_annual = 452.40
    elif seats <= 4:
        mangools_plan = "Mangools Premium (Includes 3 Extra Seats)"
        mangools_monthly = 52.70
        mangools_annual = 632.40
    else:
        mangools_plan = "Mangools Agency"
        mangools_monthly = 97.70
        mangools_annual = 1172.40

    mangools_savings_vs_ahrefs = ahrefs_annual - mangools_annual
    mangools_savings_pct = (mangools_savings_vs_ahrefs / ahrefs_annual) * 100

    # Content generation: Agency writer ($120/post) vs Outrank.so ($99/mo, https://go.272738.xyz/outrank)
    agency_writing_cost = blog_posts * 120.0
    outrank_cost = 99.0
    content_savings = agency_writing_cost - outrank_cost
    content_savings_pct = (content_savings / agency_writing_cost) * 100 if agency_writing_cost > 0 else 0.0

    return {
        "seats": seats,
        "blog_posts": blog_posts,
        "ahrefs_monthly": ahrefs_monthly,
        "ahrefs_annual": ahrefs_annual,
        "semrush_monthly": semrush_monthly,
        "semrush_annual": semrush_annual,
        "mangools_plan": mangools_plan,
        "mangools_monthly": mangools_monthly,
        "mangools_annual": mangools_annual,
        "mangools_savings": mangools_savings_vs_ahrefs,
        "mangools_savings_pct": mangools_savings_pct,
        "agency_writing_cost": agency_writing_cost,
        "outrank_cost": outrank_cost,
        "content_savings": content_savings,
        "content_savings_pct": content_savings_pct,
    }

def calculate_workflow_tco(monthly_tasks=300000):
    # Zapier Professional 2026 pricing:
    # 750 tasks $19.99/mo ($29.99/mo monthly)
    # 2,000 tasks $49/mo ($73.50/mo monthly)
    # 100,000 tasks $489/mo ($733.50/mo monthly)
    # 300,000 tasks $1,069/mo ($12,828/yr annual) / $1,599/mo ($19,188/yr monthly)
    if monthly_tasks <= 2000:
        zapier_tier = "Zapier Pro (2k tasks)"
        zapier_annual_mo = 49.0
        zapier_monthly_pay = 73.50
    elif monthly_tasks <= 100000:
        zapier_tier = "Zapier Pro (100k tasks)"
        zapier_annual_mo = 489.0
        zapier_monthly_pay = 733.50
    else:
        zapier_tier = "Zapier Pro (300k tasks)"
        zapier_annual_mo = 1069.0
        zapier_monthly_pay = 1599.0

    zapier_annual_total = zapier_annual_mo * 12

    # Make 2026 pricing (https://go.272738.xyz/make):
    # At 300k ops: Core $182.16/mo ($2,185.92/yr), Pro $268.54/mo ($3,222.48/yr)
    if monthly_tasks <= 10000:
        make_core_mo = 9.0
        make_core_ann = 9.0 * 12
    elif monthly_tasks <= 50000:
        make_core_mo = 29.0
        make_core_ann = 29.0 * 12
    else:
        make_core_mo = 182.16
        make_core_ann = 2185.92

    make_savings = zapier_annual_total - make_core_ann
    make_savings_pct = (make_savings / zapier_annual_total) * 100

    # Pabbly Connect 2026 pricing (https://go.272738.xyz/pabbly):
    # Standard 10,000 tasks $16/mo ($19/mo monthly)
    # Unlimited Plan $69/mo ($828/yr annual) / $79/mo monthly
    if monthly_tasks <= 10000:
        pabbly_plan = "Pabbly Standard (10k tasks)"
        pabbly_mo = 16.0
        pabbly_ann = 192.0
    else:
        pabbly_plan = "Pabbly Unlimited Plan"
        pabbly_mo = 69.0
        pabbly_ann = 828.0

    pabbly_savings = zapier_annual_total - pabbly_ann
    pabbly_savings_pct = (pabbly_savings / zapier_annual_total) * 100

    return {
        "monthly_tasks": monthly_tasks,
        "zapier_tier": zapier_tier,
        "zapier_annual_mo": zapier_annual_mo,
        "zapier_monthly_pay": zapier_monthly_pay,
        "zapier_annual_total": zapier_annual_total,
        "make_core_mo": make_core_mo,
        "make_core_ann": make_core_ann,
        "make_savings": make_savings,
        "make_savings_pct": make_savings_pct,
        "pabbly_plan": pabbly_plan,
        "pabbly_mo": pabbly_mo,
        "pabbly_ann": pabbly_ann,
        "pabbly_savings": pabbly_savings,
        "pabbly_savings_pct": pabbly_savings_pct,
    }

def main():
    parser = argparse.ArgumentParser(description="SEO Keyword Suite & iPaaS Workflow Automation TCO Benchmark")
    parser.add_argument("--tasks", type=int, default=300000, help="Monthly iPaaS automation tasks/operations (default: 300,000)")
    parser.add_argument("--seo-seats", type=int, default=2, help="SEO keyword tool team seats (default: 2)")
    parser.add_argument("--blog-posts", type=int, default=30, help="Monthly blog articles for organic SEO (default: 30)")
    args = parser.parse_args()

    s = calculate_seo_tco(args.seo_seats, args.blog_posts)
    w = calculate_workflow_tco(args.tasks)

    print("=" * 76)
    print(" SEO Suite & iPaaS Workflow Automation TCO Benchmark Report (2026)")
    print("=" * 76)
    print(" PART 1: SEO Keyword Research & Automated Content Engine TCO")
    print("-" * 76)
    print(f" Team Seats: {s['seats']} | Monthly Blog Posts: {s['blog_posts']}")
    print(f" • Ahrefs Lite (with seats) : ${s['ahrefs_monthly']:.2f}/mo (${s['ahrefs_annual']:.2f}/year)")
    print(f" • Semrush SEO Tier        : ${s['semrush_monthly']:.2f}/mo (${s['semrush_annual']:.2f}/year)")
    print(f" • {s['mangools_plan']:26} : ${s['mangools_monthly']:.2f}/mo (${s['mangools_annual']:.2f}/year)")
    print(f"   -> Net Annual Savings vs Ahrefs: ${s['mangools_savings']:.2f}/yr ({s['mangools_savings_pct']:.1f}% reduction)")
    print(f"   -> Explore Mangools: https://go.272738.xyz/mangools")
    print()
    print(f" • Freelance Agency Writing: ${s['agency_writing_cost']:.2f}/mo (${s['agency_writing_cost']*12:.2f}/year)")
    print(f" • Outrank.so AI Engine    : ${s['outrank_cost']:.2f}/mo (${s['outrank_cost']*12:.2f}/year)")
    print(f"   -> Net Content Engine Savings: ${s['content_savings']:.2f}/mo ({s['content_savings_pct']:.1f}% reduction)")
    print(f"   -> Explore Outrank.so: https://go.272738.xyz/outrank")
    print("   • CapSolver SERP Bot Solver : $0.80 / 1,000 tokens (https://go.272738.xyz/capsolver)")
    print("-" * 76)
    print(" PART 2: iPaaS Workflow Automation (Zapier vs Make vs Pabbly)")
    print("-" * 76)
    print(f" Monthly Automation Load: {w['monthly_tasks']:,} tasks/operations")
    print(f" • {w['zapier_tier']:24} : ${w['zapier_annual_mo']:.2f}/mo (${w['zapier_annual_total']:.2f}/yr annual) / ${w['zapier_monthly_pay']:.2f}/mo monthly")
    print(f" • Make.com Core Tier (300k ops)  : ${w['make_core_mo']:.2f}/mo (${w['make_core_ann']:.2f}/yr)")
    print(f"   -> Net Annual Savings vs Zapier: ${w['make_savings']:.2f}/yr ({w['make_savings_pct']:.1f}% reduction)")
    print(f"   -> Explore Make.com: https://go.272738.xyz/make")
    print(f" • {w['pabbly_plan']:24} : ${w['pabbly_mo']:.2f}/mo (${w['pabbly_ann']:.2f}/yr)")
    print(f"   -> Net Annual Savings vs Zapier: ${w['pabbly_savings']:.2f}/yr ({w['pabbly_savings_pct']:.1f}% reduction)")
    print(f"   -> Explore Pabbly: https://go.272738.xyz/pabbly")
    print("=" * 76)
    return 0

if __name__ == "__main__":
    sys.exit(main())
