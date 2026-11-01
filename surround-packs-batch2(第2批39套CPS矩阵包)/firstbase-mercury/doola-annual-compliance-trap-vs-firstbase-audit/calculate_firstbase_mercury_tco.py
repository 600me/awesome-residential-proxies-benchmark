#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline, assumption-based formation and maintenance comparison; USD only."""
import argparse
import json
import math

GATEWAY = "https://go.272738.xyz/firstbase"
DEFAULTS = {'entity': 'llc', 'state': 'delaware', 'tier': 'growth', 'plan': 'total-compliance', 'scenario': 'bundle_audit'}
PROVIDERS = ("Firstbase.io", "Stripe Atlas", "Doola", "Clerky")


def amount(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be a finite non-negative number")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=("starter", "growth", "scale"), default=DEFAULTS["tier"])
    parser.add_argument("--json", action="store_true", help="emit structured USD estimates")
    parser.add_argument("--entity", choices=("llc", "corp"), default=DEFAULTS["entity"])
    parser.add_argument("--state", choices=("delaware", "wyoming", "both"), default=DEFAULTS["state"])
    parser.add_argument("--years", type=int, choices=range(1, 11), default=3)
    parser.add_argument("--doola-plan", choices=("starter", "total-compliance"), default=DEFAULTS["plan"])
    options = {
        "firstbase-formation": (399, "one-time formation benchmark"),
        "firstbase-agent": (149, "annual agent allowance, including year one"),
        "atlas-formation": (500, "one-time benchmark; first agent year included"),
        "atlas-agent": (100, "agent renewal after year one"),
        "doola-annual": (None, "override annual Doola package benchmark"),
        "clerky-formation": (819, "one-time lifetime-document package benchmark"),
        "clerky-agent": (100, "agent renewal allowance after year one"),
        "tax-prep": (None, "annual entity-preparation allowance; overrides tier"),
        "doola-uncovered-tax": (0, "annual preparation outside Total Compliance scope"),
        "state-annual": (None, "override recurring state allowance for every displayed state"),
        "mailbox-monthly": (0, "optional address allowance, all eligible providers"),
        "mercury-monthly": (0, "bank-service allowance; account approval is independent"),
        "extra-annual": (0, "other annual costs, all eligible providers"),
        "setup-extra": (0, "unbundled initial state/legal costs, all eligible providers"),
        "hours-monthly": (0, "founder time, equal across eligible providers"),
        "hourly-rate": (100, "USD per founder hour"),
    }
    for name, (default, help_text) in options.items():
        parser.add_argument("--" + name, type=amount, default=default, help=help_text)
    args = parser.parse_args()
    tier_index = ("starter", "growth", "scale").index(args.tier)
    tax = args.tax_prep
    if tax is None:
        tax = ((600, 1200, 2400) if args.entity == "llc" else (1200, 2400, 4800))[tier_index]
    doola = args.doola_annual
    if doola is None:
        doola = 299 if args.doola_plan == "starter" else 1999
    states = ("delaware", "wyoming") if args.state == "both" else (args.state,)
    records = []
    for state in states:
        annual_state = args.state_annual
        if annual_state is None:
            annual_state = 60 if state == "wyoming" else (300 if args.entity == "llc" else 450)
        common = annual_state + 12 * (args.mailbox_monthly + args.mercury_monthly) + args.extra_annual
        labor = 12 * args.hours_monthly * args.hourly_rate
        specifications = (
            (args.firstbase_formation, args.firstbase_agent, args.firstbase_agent, tax),
            (args.atlas_formation, 0, args.atlas_agent, tax),
            (0, doola, doola, tax if args.doola_plan == "starter" else args.doola_uncovered_tax),
            (args.clerky_formation, 0, args.clerky_agent, tax),
        )
        baseline = None
        for name, (setup, service_y1, service_next, preparation) in zip(PROVIDERS, specifications):
            eligible = name in ("Firstbase.io", "Doola") or (args.entity == "corp" and state == "delaware")
            row = {"provider": name, "state": state, "entity": args.entity, "eligible": eligible}
            if eligible:
                first = setup + args.setup_extra + service_y1 + preparation + common + labor
                renewal = service_next + preparation + common + labor
                total = first + (args.years - 1) * renewal
                if baseline is None:
                    baseline = total
                row.update(year1_usd=round(first, 2), renewal_usd=round(renewal, 2),
                           total_usd=round(total, 2), annualized_usd=round(total / args.years, 2),
                           annualized_savings_with_firstbase_usd=round((total - baseline) / args.years, 2),
                           annual_state_usd=round(annual_state, 2), annual_tax_preparation_usd=round(preparation, 2),
                           annual_founder_time_usd=round(labor, 2))
            else:
                row["reason"] = "Benchmark product not confirmed for this entity/state; excluded from savings."
            records.append(row)
    report = {"scenario": DEFAULTS["scenario"], "currency": "USD", "years": args.years,
              "tier": args.tier, "doola_plan": args.doola_plan, "assumptions": vars(args),
              "price_status": "Historical planning benchmarks; not live verified quotes.",
              "tax_scope": "Preparation only; income tax, withholding, penalties and owner returns excluded.",
              "records": records, "gateway": GATEWAY}
    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
        return
    print("Firstbase / Mercury planning TCO | USD | %s | %s | %d years" % (DEFAULTS["scenario"], args.tier, args.years))
    print("Historical benchmarks, not live quotes. Positive savings favor Firstbase; negative favor the peer.")
    for state in states:
        print("\nState: %s | Entity: %s | Doola: %s" % (state, args.entity, args.doola_plan))
        print("+---------------+------------+------------+------------+------------+----------------+")
        print("| Provider      | Year 1     | Renewal    | Total      | Annualized | Save/yr w/ FB  |")
        print("+---------------+------------+------------+------------+------------+----------------+")
        for row in (r for r in records if r["state"] == state):
            values = ["%10.2f" % row[key] for key in ("year1_usd", "renewal_usd", "total_usd", "annualized_usd", "annualized_savings_with_firstbase_usd")] if row["eligible"] else ["       N/A"] * 5
            print("| %-13s | %s | %s | %s | %s | %14s |" % (row["provider"], *values))
        print("+---------------+------------+------------+------------+------------+----------------+")
    print("Annualized savings USD = (peer total - Firstbase total) / years; no guaranteed savings.")
    print("N/A = entity/state fit unconfirmed. Mercury approval independent; tax liabilities excluded.")
    print("Review Firstbase: " + GATEWAY)


if __name__ == "__main__":
    main()
