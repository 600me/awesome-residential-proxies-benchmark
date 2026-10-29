"""CLI for ad-tracker-antidetect-tco. Pure standard library."""

import argparse
import json
import sys

from . import __version__

GATEWAYS = {
    "adspower": "https://go.272738.xyz/adspower?src=pypi_adstack_calc",
    "morelogin": "https://go.272738.xyz/morelogin?src=pypi_adstack_calc",
    "voluum": "https://go.272738.xyz/voluum?src=pypi_adstack_calc",
    "9proxy": "https://go.272738.xyz/9proxy?src=pypi_adstack_calc",
    "webshare": "https://go.272738.xyz/webshare?src=pypi_adstack_calc",
}

# Pricing model constants (aligned verbatim with README worked examples)
ADPOWER_BASE = 19.0          # AdsPower Base: $19/mo (100 profiles, 1 seat)
ADPOWER_EXTRA_SEAT = 5.0     # extra synced seat: $5/mo each
MORELOGIN_SOLO = 9.0         # MoreLogin Solo: $9/mo (50 profiles, 2 seats)
VOLUUM_STARTER = 199.0       # Voluum Starter: 1M events base
VOLUUM_GROWTH = 349.0        # Voluum Growth: 3M events base
VOLUUM_OVERAGE_PER_1K = 0.06 # $0.06 per 1,000 excess events
NINEPROXY_PER_IP = 0.20      # 9Proxy: $0.20 per clean residential IP
RISK_ACCOUNTS_SAVED = 5
RISK_VALUE_PER_ACCOUNT = 1500.0


def calc_tco(profiles, events, seats):
    """Deterministic TCO model, numbers aligned with README examples."""
    if profiles <= 50 and seats <= 1:
        browser_cost = MORELOGIN_SOLO
        browser_row = "MoreLogin Solo Plan"
    else:
        extra = max(0, seats - 1)
        browser_cost = ADPOWER_BASE + extra * ADPOWER_EXTRA_SEAT
        browser_row = "AdsPower Base ($19) + %d extra seats ($%d)" % (
            extra, int(extra * ADPOWER_EXTRA_SEAT))

    proxy_cost = profiles * NINEPROXY_PER_IP
    if events <= 1000000:
        overage_label = "Tracker Overage"
        tracker_cost = VOLUUM_STARTER
        overage = 0.0
        tracker_row = "Voluum Starter ($199 base / 1M events)"
        overage_row = "$0.00 (within plan quota)"
    else:
        tracker_cost = VOLUUM_GROWTH
        excess = events - 3000000
        overage = max(0.0, excess / 1000.0 * VOLUUM_OVERAGE_PER_1K)
        tracker_row = "Voluum Growth ($349 base / 3M events)"
        if excess > 0:
            label = _human_millions(excess)
            overage_row = "$%.2f overage surcharge" % overage
            overage_label = "Tracker Overage (%s @ $0.06/1k)" % label
        else:
            overage_row = "$0.00 (within plan quota)"
            overage_label = "Tracker Overage"

    total = browser_cost + tracker_cost + overage + proxy_cost
    cost_per_profile = total / profiles

    result = {
        "browser_cost": browser_cost,
        "browser_row": browser_row,
        "tracker_cost": tracker_cost,
        "overage": overage,
        "tracker_row": tracker_row,
        "overage_label": overage_label,
        "overage_row": overage_row,
        "total": total,
        "cost_per_profile": cost_per_profile,
    }
    return result


def _fmt_money(n):
    return "$%s.%02d" % ("{:,}".format(int(n)), int(round(n * 100) % 100))


def _human_millions(n):
    if n >= 1000000:
        m = n / 1000000.0
        s = ("%.1f" % m).rstrip("0").rstrip(".")
        return s + "M"
    return "%d" % (n // 1000)


def _fmt_num(n):
    return "{:,}".format(n)


def build_table(profiles, events, seats):
    r = calc_tco(profiles, events, seats)
    lines = []
    lines.append("ad-tracker-antidetect-tco %s - Media Buyer Infrastructure TCO" % __version__)
    lines.append("")
    lines.append("+-------------------------------------+------------------------------------------+")
    lines.append("| STACK COMPONENT                     | MONTHLY ALLOCATION & ESTIMATED COST      |")
    lines.append("+-------------------------------------+------------------------------------------+")

    def row(left, right):
        lines.append("| %-35s | %-40s |" % (left[:35], right[:40]))

    row("Browser Profile Environment",
        "%s isolated browser profiles" % _fmt_num(profiles))
    if seats == 1:
        row("Team Operational Seats", "1 operator seat")
    else:
        row("Team Operational Seats",
            "%d synchronized operator seats" % seats)
    row("Recommended Browser Platform", r["browser_row"])
    row("Anti-Detect Browser Subtotal", "$%.2f / month" % r["browser_cost"])
    row("Ad Tracking Monthly Volume", "%s tracking events" % _fmt_num(events))
    row("Recommended Ad Tracker", r["tracker_row"])
    row(r["overage_label"], r["overage_row"])
    row("Ad Tracker Subtotal", "$%.2f / month" % (r["tracker_cost"] + r["overage"]))
    if profiles > 50:
        row("Dedicated Proxy IP Allocation",
            "%s static residential IPs (1 per prof)" % _fmt_num(profiles))
        row("9Proxy Clean IP Pool Cost",
            "$%.2f / month (clean non-expiring IPs)" % (profiles * NINEPROXY_PER_IP))
    else:
        row("Dedicated Proxy IP Allocation", "%s residential IPs" % _fmt_num(profiles))
        row("9Proxy Clean IP Pool Cost",
            "$%.2f (clean non-expiring IPs)" % (profiles * NINEPROXY_PER_IP))
    row("Total Infrastructure Monthly TCO", "$%.2f / month" % r["total"])
    row("Cost Per Active Browser Profile",
        "$%.2f / profile / month" % r["cost_per_profile"])
    if events > 1000000:
        risk = RISK_ACCOUNTS_SAVED * RISK_VALUE_PER_ACCOUNT
        row("Risk Mitigation (%d Accounts Saved)" % RISK_ACCOUNTS_SAVED,
            "~%s asset protection value" % _fmt_money(risk))
    lines.append("+-------------------------------------+------------------------------------------+")
    lines.append("")
    relevant = [k for k in ("adspower", "morelogin", "voluum", "9proxy") if k]
    lines.append("AdsPower Gateway: %s" % GATEWAYS["adspower"])
    lines.append("MoreLogin Gateway: %s" % GATEWAYS["morelogin"])
    lines.append("Voluum Gateway: %s" % GATEWAYS["voluum"])
    lines.append("9Proxy Gateway: %s" % GATEWAYS["9proxy"])
    return "\n".join(lines)


def build_json(profiles, events, seats):
    r = calc_tco(profiles, events, seats)
    return json.dumps({
        "tool": "ad-tracker-antidetect-tco",
        "version": __version__,
        "profiles": profiles,
        "events": events,
        "seats": seats,
        "breakdown": {
            "antidetect_browser_usd": r["browser_cost"],
            "ad_tracker_base_usd": r["tracker_cost"],
            "ad_tracker_overage_usd": r["overage"],
            "proxy_ips_usd": profiles * NINEPROXY_PER_IP,
            "total_monthly_tco_usd": r["total"],
            "cost_per_profile_usd": round(r["cost_per_profile"], 2),
        },
        "gateways": GATEWAYS,
    }, indent=2)


STACK_TABLE_ROWS = [
    ("AdsPower", "Anti-Detect Browser", "$19 / mo (100 profiles, 1 seat)",
     "$45 / mo (300 profiles, 3 seats)", "$120 / mo (1k profiles, 5 seats)",
     "$280+ / mo (Multi-seat Team RPA)", GATEWAYS["adspower"]),
    ("MoreLogin", "Anti-Detect Browser", "$9 / mo (50 profiles, 2 seats)",
     "$35 / mo (200 profiles, 4 seats)", "$85 / mo (600 profiles, 8 seats)",
     "$160+ / mo (Canvas Fingerprint AI)", GATEWAYS["morelogin"]),
    ("Voluum", "Ad Tracker & DSP", "$199 / mo (1M events, 1 seat)",
     "$349 / mo (3M events, 2 seats)", "$599 / mo (10M events, 5 seats)",
     "$999+ / mo (Enterprise 30M+ events)", GATEWAYS["voluum"]),
    ("9Proxy", "Residential IP Pool", "$20 (100 Clean Residential IPs)",
     "$75 (500 Residential IPs)", "$110 (1,000 Clean Residential IPs)",
     "$400 (5,000 Enterprise IPs)", GATEWAYS["9proxy"]),
    ("Webshare", "Private Datacenter / Res", "$2.99 / mo (100 IPs)",
     "$15 / mo (Private Proxy Pool)", "$45 / mo (Dedicated High-Bandwidth)",
     "Custom Bulk Datacenter Hub", GATEWAYS["webshare"]),
]


def build_compare_stack():
    headers = ["Provider", "Category", "Tier 1", "Tier 2", "Tier 3", "Tier 4", "Gateway"]
    widths = []
    for i, h in enumerate(headers):
        w = max(len(str(row[i])) for row in STACK_TABLE_ROWS)
        widths.append(max(w, len(h)))
    def sep():
        return "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    lines = []
    lines.append("ad-tracker-antidetect-tco %s - 2026 Media Buying & Anti-Detect Stack Matrix" % __version__)
    lines.append("")
    lines.append(sep())
    lines.append("| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |")
    lines.append(sep())
    for row in STACK_TABLE_ROWS:
        lines.append("| " + " | ".join(str(c).ljust(w) for c, w in zip(row, widths)) + " |")
    lines.append(sep())
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="ad-tracker-antidetect-tco",
        description="Audit anti-detect browser stacks, tracker event overages, and proxy costs.")
    parser.add_argument("--profiles", type=int, default=50,
                        help="active anti-detect browser profiles required (default: 50)")
    parser.add_argument("--events", type=int, default=1000000,
                        help="monthly tracking click/conversion events (default: 1000000)")
    parser.add_argument("--seats", type=int, default=1,
                        help="team member operational seats (default: 1)")
    parser.add_argument("--compare-stack", action="store_true",
                        help="display 2026 anti-detect and tracking benchmark table")
    parser.add_argument("--json", dest="json_out", action="store_true",
                        help="emit pure JSON payload for infrastructure monitoring")
    parser.add_argument("--version", action="version",
                        version="ad-tracker-antidetect-tco " + __version__)
    args = parser.parse_args(argv)

    if args.profiles < 1 or args.events < 0 or args.seats < 1:
        sys.stderr.write("error: --profiles >=1, --events >=0, --seats >=1 required\n")
        return 2

    if args.compare_stack:
        print(build_compare_stack())
        return 0

    if args.json_out:
        print(build_json(args.profiles, args.events, args.seats))
    else:
        print(build_table(args.profiles, args.events, args.seats))
    return 0


if __name__ == "__main__":
    sys.exit(main())
