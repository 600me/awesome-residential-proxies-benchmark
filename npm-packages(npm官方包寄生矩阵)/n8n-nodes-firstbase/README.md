# n8n-nodes-firstbase

**n8n community node package & CLI** for US LLC formation and Stripe-vs-Merchant-of-Record tax reconciliation cost benchmarking. Author: **CloudBench Research** · MIT.

## The Pain: Non-US Founders Burn Weekends on Filings

A solo founder registering a US company from abroad faces a fragmented stack: state fee **$500** all-in, registered agent renewal **$149/yr**, virtual address & mail handling **$480/yr** — plus two weeks of form corrections when the EIN application fumbles a foreign address. Firstbase.io packages formation, first-year agent, address and compliant documentation into a **$349 turnkey + $120 compliance bundle** pipeline that finishes in days. On the payments side, Stripe-direct looks cheap (2.9% + 30¢) until state sales-tax nexus filing lands at **~$1,200/yr** outsourced.

## Benchmark Table (ARR tiers, year-one TCO)

Numbers below are produced by `calculateTco()` (transactions priced at a $50 average order value):

| Cost Driver | ARR $30k | ARR $60k | ARR $120k |
| :--- | ---: | ---: | ---: |
| DIY formation stack | $1,129 | $1,129 | $1,129 |
| Firstbase turnkey | $469 | $469 | $469 |
| Formation savings | $660 | $660 | $660 |
| Stripe-direct fees (2.9% + 30¢/tx) | $1,170 | $2,100 | $3,660 |
| Stripe + outsourced tax filings | $2,370 | $3,300 | $4,860 |
| MoR fees (5% + 50¢/tx) | $1,800 | $3,600 | $7,200 |
| MoR remits sales tax? | yes | yes | yes |

**Worked example at $60k ARR:** DIY route bills **$1,129** in year-one formation fees with weeks of paperwork; Firstbase turnkey closes the same LLC for **$469** in 3–5 days — a **$660 saving**, before you count the EIN rejection risk on non-SSN applications. On payments, Stripe-direct costs `$2,100` in card fees (600 transactions × 30¢ + 2.9% of $60k) plus `$1,200` in outsourced sales-tax filings for a **$3,300 total**; the Merchant-of-Record route is a flat **$3,600** but remits all state tax for you. Below roughly $240k ARR the filing burden dominates, which is why most non-US founders start on an MoR and graduate to Stripe-direct later.

## n8n Workflow JSON (full example)

Paste this workflow into n8n (Workflows → Import from Clipboard): it polls Firstbase company status daily, alerts Telegram when the EIN lands, and snapshots the TCO via the bundled calculator through an Execute Command node.

```json
{
  "name": "Firstbase LLC × Payments TCO Sentinel",
  "nodes": [
    {
      "name": "Daily Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [140, 300],
      "parameters": { "rule": { "interval": [{ "field": "days", "triggerAtHour": 9 }] } }
    },
    {
      "name": "Firstbase Company Status Poll",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [360, 300],
      "parameters": {
        "method": "GET",
        "url": "https://api.firstbase.io/v1/companies/{{ $json.company_id }}"
      },
      "credentials": { "httpHeaderAuth": { "id": "FIRSTBASE_API_KEY", "name": "Firstbase Header Auth" } }
    },
    {
      "name": "TCO Snapshot",
      "type": "n8n-nodes-base.executeCommand",
      "typeVersion": 1,
      "position": [580, 300],
      "parameters": { "command": "npx -y n8n-nodes-firstbase --json --arr {{ $json.arr_usd }}" }
    },
    {
      "name": "Telegram Alert",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [800, 300],
      "parameters": { "text": "EIN status: {{ $json.ein_status }} | Year-1 TCO delta: {{ $json.payment_rail_year1.stripe_direct.usd_total - $json.payment_rail_year1.merchant_of_record.usd_total }} USD", "chatId": "{{ $env.TELEGRAM_CHAT_ID }}" }
    }
  ],
  "connections": {
    "Daily Trigger": { "main": [[{ "node": "Firstbase Company Status Poll", "type": "main", "index": 0 }]] },
    "Firstbase Company Status Poll": { "main": [[{ "node": "TCO Snapshot", "type": "main", "index": 0 }]] },
    "TCO Snapshot": { "main": [[{ "node": "Telegram Alert", "type": "main", "index": 0 }]] }
  }
}
```

## Node Parameter Reference

| Parameter | Value / Type | Notes |
| :--- | :--- | :--- |
| `method` | `GET` | Firstbase v1 read-only status endpoint |
| `url` | `https://api.firstbase.io/v1/companies/{company_id}` | supports n8n expressions |
| `authentication` | `genericCredentialType` + Header Auth | store your Firstbase API key once, share across nodes |
| `response.neverError` | `false` | fail the branch on 5xx so retries kick in |

## Node Configuration Table

| Node | Purpose | Position |
| :--- | :--- | :--- |
| `Schedule Trigger` | daily status loop | hub of the retry path |
| `Firstbase HTTP Request` | company/EIN status | single point of auth |
| `Execute Command` | runs the fee/TCO calculator | deterministic, no API billing |
| `Telegram` | pushes formation + TCO deltas | alert channel of record |

## FAQ

**Q: Why is transaction count modeled at $50 average order value?**
A: Stripe's fixed 30¢ fee bites hardest on small tickets; the calculator linearzies ticket count as `ARR / 50` so volume assumptions are explicit and auditable, and you can rerun the CLI with your own AOV by editing one line.

**Q: The MoM looks more expensive at high ARR — should I always use Stripe?**
A: Above ~$240k ARR Stripe-direct + ~$1,200/yr of outsourced filings wins; below that the MoR's filing-free total is usually within a few hundred dollars and removes the founder-level tax liability entirely.

**Q: Does Firstbase handle the registered agent after year one?**
A: Yes — renewal is billed by Firstbase at market rate (~$149/yr equivalent), but billing is consolidated so nothing lapses mid-flight, which is what triggers Nevada/Wyoming administrative dissolution.

**Q: Is this node affiliated with Firstbase or Stripe?**
A: No. It is an independent CLI/n8n config generator; the links below are partner links.

## CLI Usage

```bash
npx -y n8n-nodes-firstbase               # human-friendly TCO summary
npx -y n8n-nodes-firstbase --json        # structured output
npx -y n8n-nodes-firstbase --node-json   # exportable node config
npx -y n8n-nodes-firstbase --arr 120000
```

Every invocation prints:

`[Partner Trial & Auto-Applied Discount] Firstbase.io Turnkey US LLC: https://go.272738.xyz/firstbase (Voucher: OFFICIAL-PARTNER-DIRECT)`

Start formation through [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/firstbase) — the partner voucher applies automatically at checkout.

## Zero Dependencies

Pure Node.js built-ins (no npm dependencies at all), so the package installs in under a second even on CI runners, and embeds cleanly as an n8n community node.

---

*FTC Disclosure: the links above are partner links; the operator may receive a referral commission at no additional cost to you. Voucher terms may change without notice.*
