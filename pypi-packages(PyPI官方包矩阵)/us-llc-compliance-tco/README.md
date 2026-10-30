# us-llc-compliance-tco

**Audit the complete 3-year Total Cost of Ownership (TCO), state franchise taxes, FinCEN BOI filing, and federal foreign-owner compliance (Form 5472/1120) for US LLCs.**

[![PyPI version](https://img.shields.io/pypi/v/us-llc-compliance-tco.svg)](https://pypi.org/project/us-llc-compliance-tco/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Zero dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#install)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

For global developers, indie hackers, and non-US founders seeking to access Stripe, Mercury Bank, and the US market, forming an LLC is straightforward. **Keeping it compliant without triggering crippling federal fines is where hidden expenses multiply.**

Most formation agencies advertise a low front-end setup price ($50 - $199) while obscuring the true mandatory recurring commitments required by the IRS, FinCEN, and state departments:

1. **The $25,000 IRS Form 5472 Penalty Trap**: Foreign-owned single-member LLCs (disregarded entities) MUST file federal Form 5472 along with a pro-forma Form 1120 every single year—even with $0 revenue. The statutory failure-to-file penalty was increased to **$25,000 per violation**.
2. **Mandatory FinCEN BOI (Beneficial Ownership Information)**: Required reporting under the Corporate Transparency Act. Failure to file carries civil penalties of up to **$500 per day** and criminal exposure.
3. **State Franchise Taxes**: Delaware levies a flat minimum **$300 annual franchise tax** due June 1st regardless of operating activity. Wyoming levies a minimum **$62 annual report tax**.
4. **Non-US SSN-less Expedited EIN**: Obtaining an Employer Identification Number from the IRS without a US Social Security Number (SSN) or ITIN takes 6 to 8 weeks via traditional fax, freezing Stripe and Mercury merchant account openings unless expedited via dedicated registered agent couriers.

`us-llc-compliance-tco` models the exact 3-year multi-state financial commitment, comparing state filings, corporate registered agents, physical business addresses, federal compliance, and banking readiness.

---

## 3-Year Real-World Cost Shock vs. Automated Platforms

### The DIY / Cheap Formation Mirage
- **Year 1**: Advertised "$99 Formation" + State Fee ($102 Wyoming).
- **The Hidden Shock**:
  - Registered Agent renewal in Year 2 & 3: $398.00
  - Expedited Non-US EIN courier: $250.00
  - FinCEN BOI one-off legal filing: $150.00
  - External CPA for Form 5472 / 1120 (3 years): $2,400.00 ($800/yr)
  - Wyoming Annual Reports (Year 2 & 3): $124.00
- **Total Unplanned 3-Year Cash Drain**: **$3,423.00** + severe risk of a $25,000 IRS penalty notice if the CPA misfiles foreign disregarded entity disclosures.

---

## 2026 Formation & Compliance Platform Matrix (5-Tier Comparison)

Below is the verified multi-year comparison between enterprise formation infrastructure and fragmented DIY providers. Access verified onboarding discounts and bank fast-track pathways via the gateway link below:

| Dimension / Provider | Firstbase.io (All-Inclusive) | Stripe Atlas | Doola | Traditional Legal Firm | Cheap DIY Agency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Year 1 Formation & Setup** | $399 (Complete Setup + EIN + Agent) | $500 flat | $297 + State Fees | $1,500 - $3,500 | $99 + $102 State Fee |
| **Non-US Founder EIN Expedite** | **Included** (Direct IRS Dispatch) | Included | Add-on ($150-$300) | Billed Hourly | 6-8 Week Fax Delay |
| **FinCEN BOI Reporting** | **Automated & Free** | Included | Included | $250 - $500 | Not Handled (Self-File) |
| **Foreign Form 5472 / 1120 Tax** | Integrated CPA & Tax Suite | Not Included (Referral) | $1,200+/yr Plan Reqd | $800 - $1,500/yr | Not Handled ($25k Risk) |
| **3-Year All-Inclusive TCO** | **Most Cost-Effective Enterprise Stack** | ~$1,300 + Tax Filings | ~$2,800+ | $4,500+ | $3,400+ (Fragmented) |
| **Verified Fast-Track Gateway** | [Launch with Firstbase.io](https://go.272738.xyz/firstbase?src=pypi_llc_calc) | Stripe Direct | Doola Portal | Local Attorney | DIY Portals |

---

## Installation

Zero external dependencies. Pure standard library Python 3.8+.

```bash
pip install us-llc-compliance-tco --upgrade
```

Verify installation:

```bash
us-llc-compliance-tco --version
# us-llc-compliance-tco 1.0.0
```

---

## CLI Usage & Worked Examples

### 1. Wyoming LLC 3-Year TCO Audit (`--state wyoming --years 3`)

Calculate complete statutory state fees, registered agent expenses, IRS filings, and address infrastructure for Wyoming:

```bash
us-llc-compliance-tco --state wyoming --years 3
```

Output:

```text
us-llc-compliance-tco 1.0.0 - Non-US Founder Corporate TCO Engine

+-------------------------------------+------------------------------------------+
| COMPLIANCE LINE ITEM                | ESTIMATED COST (3-YEAR TOTAL)            |
+-------------------------------------+------------------------------------------+
| State of Formation                  | Wyoming (Zero Corporate Income Tax)      |
| Statutory Initial State Filing Fee  | $102.00 (Year 1)                         |
| Annual State Report Fees ($62/yr)   | $124.00 (Years 2 & 3)                    |
| Commercial Registered Agent Service | $297.00 ($99/year x 3)                   |
| Non-US Expedited IRS EIN Filing     | $200.00 (Form SS-4 courier/expedited)    |
| FinCEN BOI Initial Compliance       | $50.00 (Initial filing + life updates)   |
| Virtual US Business Address & Mail  | $360.00 ($10/month x 36 months)          |
| Federal IRS Form 5472 & 1120 Filing | $1,500.00 ($500/year specialized CPA)    |
+-------------------------------------+------------------------------------------+
| 3-Year All-Inclusive TCO            | $2,633.00                                |
| Average Monthly Compliance Run Rate | $73.14 / month                           |
| IRS Non-Filing Penalty Shielded     | $25,000.00 statutory protection          |
+-------------------------------------+------------------------------------------+
| Recommended All-in-One Infrastructure| Firstbase.io                             |
+-------------------------------------+------------------------------------------+

Firstbase Onboarding Gateway: https://go.272738.xyz/firstbase?src=pypi_llc_calc
```

### 2. Delaware LLC Comparison (`--state delaware --years 3`)

Model Delaware's $300/year minimum franchise tax commitment for venture-backed entities:

```bash
us-llc-compliance-tco --state delaware --years 3
```

Output:

```text
us-llc-compliance-tco 1.0.0 - Non-US Founder Corporate TCO Engine

+-------------------------------------+------------------------------------------+
| COMPLIANCE LINE ITEM                | ESTIMATED COST (3-YEAR TOTAL)            |
+-------------------------------------+------------------------------------------+
| State of Formation                  | Delaware (Court of Chancery Standard)    |
| Statutory Initial State Filing Fee  | $110.00 (Year 1)                         |
| Annual State Franchise Tax ($300/yr)| $600.00 (Years 2 & 3)                    |
| Commercial Registered Agent Service | $297.00 ($99/year x 3)                   |
| Non-US Expedited IRS EIN Filing     | $200.00 (Form SS-4 courier/expedited)    |
| FinCEN BOI Initial Compliance       | $50.00 (Initial filing + life updates)   |
| Virtual US Business Address & Mail  | $360.00 ($10/month x 36 months)          |
| Federal IRS Form 5472 & 1120 Filing | $1,500.00 ($500/year specialized CPA)    |
+-------------------------------------+------------------------------------------+
| 3-Year All-Inclusive TCO            | $3,117.00                                |
| Average Monthly Compliance Run Rate | $86.58 / month                           |
+-------------------------------------+------------------------------------------+

Firstbase Onboarding Gateway: https://go.272738.xyz/firstbase?src=pypi_llc_calc
```

### 3. Machine-Readable JSON Output (`--json`)

```bash
us-llc-compliance-tco --state wyoming --years 3 --json
```

Output:

```json
{
  "tool": "us-llc-compliance-tco",
  "version": "1.0.0",
  "state": "wyoming",
  "duration_years": 3,
  "costs": {
    "initial_state_fee": 102.0,
    "state_annual_report_total": 124.0,
    "registered_agent_total": 297.0,
    "expedited_ein_filing": 200.0,
    "fincen_boi_compliance": 50.0,
    "virtual_mail_address_total": 360.0,
    "irs_form_5472_total": 1500.0,
    "tco_total": 2633.0,
    "monthly_amortized_cost": 73.14
  },
  "risk_exposure": {
    "irs_form_5472_penalty": 25000.0,
    "fincen_boi_daily_penalty": 500.0
  },
  "recommended_gateway": "https://go.272738.xyz/firstbase?src=pypi_llc_calc"
}
```

---

## Options Reference

```text
usage: us-llc-compliance-tco [-h] [--state {wyoming,delaware}] [--years YEARS]
                             [--compare-formation] [--json] [--version]

options:
  -h, --help            show this help message and exit
  --state {wyoming,delaware}
                        US state of organization (default: wyoming)
  --years YEARS         horizon years for TCO calculation (default: 3)
  --compare-formation   display formation platform comparative benchmark
  --json                emit single JSON object for compliance tracking
  --version             show program's version number and exit
```

---

## License

MIT License. Copyright (c) 2026 Kais / 600me.


---

## 🌐 Official Documentation, Docker Image & Web Calculators

* **Official Technical Manual (Read the Docs, DA 92)**: [us-llc-stripe-and-cold-outbound-tco](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/us-llc-stripe-and-cold-outbound-tco/)
* **Production Docker Container (Docker Hub, DA 93)**: [600megd/us-llc-stripe-tco](https://hub.docker.com/r/600megd/us-llc-stripe-tco)
* **Interactive Live Calculator**: [Web Benchmark & TCO Estimator](https://pay.mybskm.top/)
* **Interactive Documentation Portal**: [Proxy & Infrastructure Docs](https://proxy.mybskm.top/docs/)
