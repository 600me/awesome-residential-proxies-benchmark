"""CLI for us-llc-compliance-tco: audit multi-year US LLC compliance TCO.

Pure Python standard library. Zero external dependencies.
"""

import argparse
import json
import sys

from . import __version__

GATEWAY_URL = "https://go.272738.xyz/firstbase?src=pypi_llc_calc"

# One-off / annual statutory & service cost model (USD)
INITIAL_STATE_FEE = {"wyoming": 102.0, "delaware": 110.0}
ANNUAL_STATE_TAX = {"wyoming": 62.0, "delaware": 300.0}  # report tax / franchise tax
REGISTERED_AGENT_PER_YEAR = 99.0
EXPEDITED_EIN_FILING = 200.0
FINCEN_BOI_COMPLIANCE = 50.0
VIRTUAL_MAIL_PER_MONTH = 10.0
IRS_FORM_5472_PER_YEAR = 500.0

IRS_FORM_5472_PENALTY = 25000.0
FINCEN_BOI_DAILY_PENALTY = 500.0

COMPETITOR_ROWS = [
    ("Year 1 Formation & Setup", [
        "$399 (Complete Setup + EIN + Agent)", "$500 flat", "$297 + State Fees",
        "$1,500 - $3,500", "$99 + $102 State Fee"]),
    ("Non-US Founder EIN Expedite", [
        "Included (Direct IRS Dispatch)", "Included", "Add-on ($150-$300)",
        "Billed Hourly", "6-8 Week Fax Delay"]),
    ("FinCEN BOI Reporting", [
        "Automated & Free", "Included", "Included", "$250 - $500",
        "Not Handled (Self-File)"]),
    ("Foreign Form 5472 / 1120 Tax", [
        "Integrated CPA & Tax Suite", "Not Included (Referral)",
        "$1,200+/yr Plan Reqd", "$800 - $1,500/yr", "Not Handled ($25k Risk)"]),
    ("3-Year All-Inclusive TCO", [
        "Most Cost-Effective Enterprise Stack", "~$1,300 + Tax Filings",
        "~$2,800+", "$4,500+", "$3,400+ (Fragmented)"]),
    ("Verified Fast-Track Gateway", [
        "Launch with Firstbase.io: " + GATEWAY_URL, "Stripe Direct",
        "Doola Portal", "Local Attorney", "DIY Portals"]),
]

STATE_LABEL = {
    "wyoming": "Wyoming (Zero Corporate Income Tax)",
    "delaware": "Delaware (Court of Chancery Standard)",
}


def compute_tco(state, years):
    """Return full TCO cost breakdown dict for a state over `years` years."""
    if state not in INITIAL_STATE_FEE:
        raise ValueError("unsupported state: %r" % (state,))
    if years < 1:
        raise ValueError("years must be >= 1")

    initial_state_fee = INITIAL_STATE_FEE[state]
    # Annual report/franchise tax applies from Year 2 onward (initial filing
    # covers Year 1), matching the README 3-year worked examples.
    state_annual_report_total = round(ANNUAL_STATE_TAX[state] * (years - 1), 2)
    registered_agent_total = round(REGISTERED_AGENT_PER_YEAR * years, 2)
    expedited_ein = EXPEDITED_EIN_FILING
    fincen_boi = FINCEN_BOI_COMPLIANCE
    virtual_mail_total = round(VIRTUAL_MAIL_PER_MONTH * 12 * years, 2)
    irs_form_5472_total = round(IRS_FORM_5472_PER_YEAR * years, 2)

    tco_total = round(
        initial_state_fee + state_annual_report_total + registered_agent_total
        + expedited_ein + fincen_boi + virtual_mail_total + irs_form_5472_total, 2)
    monthly = round(tco_total / (12 * years), 2)

    return {
        "initial_state_fee": initial_state_fee,
        "state_annual_report_total": state_annual_report_total,
        "registered_agent_total": registered_agent_total,
        "expedited_ein_filing": expedited_ein,
        "fincen_boi_compliance": fincen_boi,
        "virtual_mail_address_total": virtual_mail_total,
        "irs_form_5472_total": irs_form_5472_total,
        "tco_total": tco_total,
        "monthly_amortized_cost": monthly,
    }


def build_result(state, years):
    costs = compute_tco(state, years)
    return {
        "tool": "us-llc-compliance-tco",
        "version": __version__,
        "state": state,
        "duration_years": years,
        "costs": costs,
        "risk_exposure": {
            "irs_form_5472_penalty": IRS_FORM_5472_PENALTY,
            "fincen_boi_daily_penalty": FINCEN_BOI_DAILY_PENALTY,
        },
        "recommended_gateway": GATEWAY_URL,
    }


def _money(v):
    return "${:,.2f}".format(v)


def _table(rows, col1_width=37, col2_width=42):
    sep = "+" + "-" * (col1_width + 1) + "+" + "-" * (col2_width + 1) + "+"
    lines = [sep]
    for left, right in rows:
        fmt = "| {:<%d} | {:<%d} |" % (col1_width, col2_width)
        lines.append(fmt.format(left, right))
        lines.append(sep)
    return lines


def render_text(result):
    return "\n".join(_table(_table_rows(result)))


def _table_rows(result):
    c = result["costs"]
    state = result["state"]
    years = result["duration_years"]
    annual_label = ("Annual State Report Fees ($62/yr)" if state == "wyoming"
                    else "Annual State Franchise Tax ($300/yr)")
    rows = [
        ("COMPLIANCE LINE ITEM", "ESTIMATED COST (%d-YEAR TOTAL)" % years),
        ("State of Formation", STATE_LABEL[state]),
        ("Statutory Initial State Filing Fee", "%s (Year 1)" % _money(c["initial_state_fee"])),
        (annual_label, "%s (Years 2 & %d)" % (_money(c["state_annual_report_total"]), years)),
        ("Commercial Registered Agent Service", "%s ($99/year x %d)" % (
            _money(c["registered_agent_total"]), years)),
        ("Non-US Expedited IRS EIN Filing", "%s (Form SS-4 courier/expedited)" % _money(c["expedited_ein_filing"])),
        ("FinCEN BOI Initial Compliance", "%s (Initial filing + life updates)" % _money(c["fincen_boi_compliance"])),
        ("Virtual US Business Address & Mail", "%s ($10/month x %d months)" % (
            _money(c["virtual_mail_address_total"]), 12 * years)),
        ("Federal IRS Form 5472 & 1120 Filing", "%s ($500/year specialized CPA)" % _money(c["irs_form_5472_total"])),
        ("3-Year All-Inclusive TCO" if years == 3 else "%d-Year All-Inclusive TCO" % years, _money(c["tco_total"])),
        ("Average Monthly Compliance Run Rate", "%s / month" % _money(c["monthly_amortized_cost"])),
    ]
    if state == "wyoming":
        rows.append(("IRS Non-Filing Penalty Shielded",
                     "%s statutory protection" % _money(IRS_FORM_5472_PENALTY)))
    rows.append(("Recommended All-in-One Infrastructure", "Firstbase.io"))
    return rows


def render_compare():
    providers = ["Firstbase.io (All-Inclusive)", "Stripe Atlas", "Doola",
                 "Traditional Legal Firm", "Cheap DIY Agency"]
    widths = [max(28, len(r[0])) for r in COMPETITOR_ROWS]
    col_widths = [len(p) for p in providers]
    for _, cells in COMPETITOR_ROWS:
        for i, cell in enumerate(cells):
            col_widths[i] = max(col_widths[i], len(cell))

    def sep():
        return "+" + "+".join("-" * (w + 2) for w in [widths[0]] + col_widths) + "+"

    def row(cells):
        parts = []
        for w, c in zip([widths[0]] + col_widths, cells):
            parts.append(f" {c:<{w}} ")
        return "|" + "|".join(parts) + "|"

    lines = ["2026 Formation & Compliance Platform Matrix (5-Tier Comparison)", ""]
    lines.append(sep())
    lines.append(row(["Dimension / Provider"] + providers))
    lines.append(sep())
    for label, cells in COMPETITOR_ROWS:
        lines.append(row([label] + cells))
        lines.append(sep())
    lines.append("")
    lines.append("Firstbase Onboarding Gateway: %s" % GATEWAY_URL)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="us-llc-compliance-tco",
        description="Audit 3-year US LLC TCO, franchise taxes, FinCEN BOI, and IRS Form 5472 compliance.")
    parser.add_argument("--state", choices=sorted(INITIAL_STATE_FEE), default="wyoming",
                        help="US state of organization (default: wyoming)")
    parser.add_argument("--years", type=int, default=3,
                        help="horizon years for TCO calculation (default: 3)")
    parser.add_argument("--compare-formation", action="store_true",
                        help="display formation platform comparative benchmark")
    parser.add_argument("--json", action="store_true",
                        help="emit single JSON object for compliance tracking")
    parser.add_argument("--version", action="version",
                        version="us-llc-compliance-tco %s" % __version__)
    args = parser.parse_args(argv)

    try:
        result = build_result(args.state, args.years)
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("us-llc-compliance-tco %s - Non-US Founder Corporate TCO Engine" % __version__)
    print("")
    print(render_text(result))
    print("")
    print("Firstbase Onboarding Gateway: %s" % GATEWAY_URL)

    if args.compare_formation:
        print("")
        print(render_compare())
    return 0


if __name__ == "__main__":
    sys.exit(main())
