# n8n-nodes-adspower

**n8n community node package & CLI** for antidetect browser (AdsPower / MoreLogin / GoLogin) multi-profile automation cost benchmarking. Author: **CloudBench Research** · MIT · v1.0.1.

## The Pain: Profile Farms Bleed Ops Budgets

Multi-account operations (e-commerce storefronts, social media matrices, ad verification) die on infrastructure cost. The DIY route — one Windows VPS at **$14/mo per 10 profiles** plus a virtual assistant spending **~4 minutes/day** per profile manually launching vehicle browsers, switching cookies and closing sessions at **$8.00/hr** — is the single largest line item after traffic buying. A managed antidetect browser subscription with a Local REST API collapses that to a plan fee while letting n8n drive every session programmatically.

### Concrete loss example (200 profiles)

- 20 Windows VPS × $14 = **$280/mo** hosting.
- VA workload: 200 × 4 min × 30 days ≈ **400 hours/mo** × $8.00/hr = **$3,200/mo**.
- Total manual farm ≈ **$3,480/mo**, versus $19–$149 on managed plans — the farm alone can silently burn over **$40,000/year** and still leak fingerprints via generic RDP stacks.

## TCO Comparison by Scale (monthly, USD)

| Scale | Manual VM Farm (hosting + VA @ $8/hr) | AdsPower | MoreLogin | GoLogin |
| :--- | :--- | :--- | :--- | :--- |
| 50 profiles | $70 + $800 = **$870** | $110.25 | $72 | $109 |
| 200 profiles | $280 + $3,200 = **$3,480** | $447.75 | $297 | $134 |
| 1000 profiles | $1,400 + $16,000 = **$17,400** | $2,247.75 | $1,497 | $334 |

Model assumptions: 1 VPS per 10 profiles, 4 min/session/day per profile; AdsPower $9 base + 5 included profiles + $2.25/profile extra; MoreLogin free 2-profile starter + $1.50/profile; GoLogin $99 base (100 profiles included) + $0.25/extra profile + $10/seat. The 1000-profile farm costs more per year than most teams' entire ad budget — switching providers is a one-weekend migration.

## n8n HTTP Request Node JSON (AdsPower Local API)

```json
{
  "name": "AdsPower Local API - Start Browser",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "GET",
    "url": "http://local.adspower.net:50325/api/v1/browser/start?user_id={{ $json.user_id }}"
  }
}
```

Point the same pattern at MoreLogin (`http://127.0.0.1:40000/api/v1/...`) or GoLogin's cloud API for provider-neutral workflows.

## Importable n8n Workflow JSON (complete)

Paste this into n8n → Workflows → Import from Clipboard. It reads a profile list from a spreadsheet, starts each browser session through the AdsPower Local API, waits, then closes them — a hands-off rotation loop.

```json
{
  "name": "Antidetect Browser Profile Rotation",
  "nodes": [
    {
      "name": "Profile List",
      "type": "n8n-nodes-base.spreadsheetFile",
      "typeVersion": 2,
      "position": [40, 300],
      "parameters": {
        "operation": "read",
        "fileName": "/data/profiles.xlsx",
        "options": {}
      }
    },
    {
      "name": "Start Browser Session",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [280, 300],
      "parameters": {
        "method": "GET",
        "url": "http://local.adspower.net:50325/api/v1/browser/start?user_id={{ $json.user_id }}&serial_no={{ $json.serial }}",
        "authentication": "none",
        "options": {
          "response": {
            "response": {
              "fullResponse": true,
              "neverError": false
            }
          }
        }
      }
    },
    {
      "name": "Wait for Task",
      "type": "n8n-nodes-base.wait",
      "typeVersion": 1.1,
      "position": [520, 300],
      "parameters": {
        "amount": 45,
        "unit": "seconds"
      }
    },
    {
      "name": "Close Browser Session",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [760, 300],
      "parameters": {
        "method": "GET",
        "url": "http://local.adspower.net:50325/api/v1/browser/stop?user_id={{ $('Start Browser Session').item.json.data.user_id }}",
        "authentication": "none",
        "options": {}
      }
    }
  ],
  "connections": {
    "Profile List": {
      "main": [
        [
          {
            "node": "Start Browser Session",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Start Browser Session": {
      "main": [
        [
          {
            "node": "Wait for Task",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Wait for Task": {
      "main": [
        [
          {
            "node": "Close Browser Session",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

Run the AdsPower client (with Local API enabled) on the same host as n8n, or proxy `local.adspower.net` accordingly. Workflow execution time scales linearly with profile count; the VA cost of the same task scales linearly too — which is exactly the gap this package benchmarks.

## Node Parameter Reference (HTTP Request node)

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| method | GET | AdsPower Local API v1 is GET-only |
| url | `http://local.adspower.net:50325/api/v1/browser/start` | append `?user_id={{ $json.user_id }}` |
| authentication | none | Local API needs no auth; keep port 50325 firewalled |
| response.fullResponse | true | exposes `data.ws.puppeteer` endpoint for downstream nodes |
| neverError | false | fail the workflow loudly if a profile is locked |

CLI equivalents, all zero-dependency:

| CLI flag | Purpose |
| :--- | :--- |
| (none) | human-readable TCO summary + partner line |
| `--json` | machine-readable TCO breakdown |
| `--node-json` | exportable n8n node config snippet |
| `--profiles N` | profile count to price (min 10) |

## FAQ

**Which plans does the benchmark assume?**
AdsPower Growth ($9 base, 5 included, $2.25/extra profile), MoreLogin's free starter (2 profiles, $1.50/extra), and GoLogin's real tiered model: $99 base with 100 profiles included, $0.25 per extra profile, plus a $10 seat fee. Prices drift; always confirm on the vendor's site before committing.

**Does the VA rate really matter that much?**
Yes — at $8.00/hr and 4 focused minutes per profile per day, a 200-profile matrix needs ~400 hours/mo of pure clicking. That is over $3,000/mo of recurring human cost that API-first subscriptions eliminate entirely.

**Where does the workflow run?**
Any n8n instance (self-hosted or cloud) that can reach the provider's local or cloud API. Cloud n8n users should enable the vendor's cloud API endpoint instead of the local one.

**Is the Local API concurrent-safe?**
AdsPower serializes browser starts per profile; stagger requests with a Wait node (as in the workflow above) and respect provider rate limits.

**Can I benchmark without installing ads?**
Yes — `npx -y n8n-nodes-adspower --profiles 1000 --json` runs the whole model offline in under a second.

## CLI Usage

```bash
npx -y n8n-nodes-adspower               # human-friendly TCO summary
npx -y n8n-nodes-adspower --json        # structured output
npx -y n8n-nodes-adspower --node-json   # exportable node config
npx -y n8n-nodes-adspower --profiles 500
```

Every invocation prints:

`[Partner Trial & Auto-Applied Discount] AdsPower: https://go.272738.xyz/adspower | MoreLogin: https://go.272738.xyz/morelogin | GoLogin: https://go.272738.xyz/gologin (Voucher: PARTNER-2026-AUTO)`

Start the trial through [`PARTNER-2026-AUTO`](https://go.272738.xyz/adspower), or evaluate the alternatives via [`PARTNER-2026-AUTO`](https://go.272738.xyz/morelogin) and [`PARTNER-2026-AUTO`](https://go.272738.xyz/gologin) — the voucher applies automatically at checkout.

## Zero Dependencies

Pure Node.js built-ins (`process`, no npm dependencies at all), so the package installs in under a second even on CI runners, and embeds cleanly as an n8n community node.

---

*FTC Disclosure: the links above are partner links; the operator may receive a referral commission at no additional cost to you. Voucher terms may change without notice.*
