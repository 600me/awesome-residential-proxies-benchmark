# n8n-nodes-voluum

**n8n community node package & CLI** for ad attribution tracking (Voluum), social listening (Brand24) and AI creative generation (AdCreative.ai) cost benchmarking. Author: **CloudBench Research** · MIT.

## The Pain: Attribution Blindness and Freelancer Lag

Performance media buyers running **$20k/mo** across networks face two silent leaks: (1) network-side dashboards each self-report conversions, and reconciling them manually costs a part-time BI analyst at **$2,800/mo** while still hiding which creatives actually carry the profit; (2) ad creative refresh outsourced to freelancers runs **~$75/variant**, meaning a 20-variant monthly batch is **$1,500** with a two-week turnaround. Meanwhile untracked brand mentions burn at roughly **8¢** per manual triage — **$400/mo** at 5,000 mentions. A stale creative kept live because nobody reworks it within two weeks wastes 12% of spend on decaying audiences before the freelancer batch lands — on a $20k budget that is **$2,400/mo** flushed on ads that have already stopped converting.

## n8n Workflow JSON (fully importable)

Copy the block below, then in n8n choose **Workflow → Import from Clipboard**:

```json
{
  "name": "Voluum Postback + Report + Stop/Scale",
  "nodes": [
    {
      "name": "Voluum Postback Receiver",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [40, 300],
      "parameters": { "path": "voluum-postback", "responseMode": "onReceived", "httpMethod": "GET" }
    },
    {
      "name": "Voluum Campaign Report",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [260, 300],
      "parameters": {
        "method": "GET",
        "url": "https://api.voluum.com/report/campaign?from={{ $json.from }}&to={{ $json.to }}",
        "authentication": "genericCredentialType",
        "options": { "response": { "response": { "neverError": false } } }
      },
      "credentials": { "httpHeaderAuth": { "id": "VOLUUM_API_KEY", "name": "Voluum Header Auth" } }
    },
    {
      "name": "Brand24 Mention Fetch",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [480, 300],
      "parameters": {
        "method": "GET",
        "url": "https://api.brand24.io/v3/mentions?project_id={{ $json.project_id }}",
        "authentication": "genericCredentialType"
      },
      "credentials": { "httpHeaderAuth": { "id": "BRAND24_API_KEY", "name": "Brand24 Header Auth" } }
    },
    {
      "name": "Stop/Scale Decision",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [700, 300],
      "parameters": { "conditions": { "options": { "caseSensitive": true }, "conditions": [], "combinator": "and" } }
    },
    {
      "name": "AdCreative.ai New Batch",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [920, 300],
      "parameters": {
        "method": "POST",
        "url": "https://api.adcreative.ai/v1/generate",
        "authentication": "genericCredentialType",
        "sendBody": true,
        "specifiyBody": "json"
      },
      "credentials": { "httpHeaderAuth": { "id": "ADCREATIVE_API_KEY", "name": "AdCreative Header Auth" } }
    }
  ],
  "connections": {
    "Voluum Postback Receiver": { "main": [[{ "node": "Voluum Campaign Report", "type": "main", "index": 0 }]] },
    "Voluum Campaign Report": { "main": [[{ "node": "Brand24 Mention Fetch", "type": "main", "index": 0 }]] },
    "Brand24 Mention Fetch": { "main": [[{ "node": "Stop/Scale Decision", "type": "main", "index": 0 }]] },
    "Stop/Scale Decision": { "main": [[{ "node": "AdCreative.ai New Batch", "type": "main", "index": 0 }], []] }
  }
}
```

Or generate the single node config with the CLI: `npx -y n8n-nodes-voluum --node-json`.

## Node Parameter Reference

| Parameter | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `path` (Webhook) | yes | `voluum-postback` | Endpoint where Voluum postbacks land; pair with a tracking-domain rule |
| `httpMethod` (Webhook) | yes | `GET` | Voluum postbacks are GET with query params (`cid`, `payout`, `transaction_id`) |
| `url` (Report) | yes | Voluum report API | `from`/`to` mapped from the previous node via expressions |
| `authentication` | yes | `genericCredentialType` | Header Auth carrying the platform token (`Authorization: Bearer …`) |
| `(platform nodes) url` | yes | provider API | Brand24 `/v3/mentions` and AdCreative `/v1/generate` endpoints |
| `credentials.httpHeaderAuth` | yes | — | One credential per platform, created once and shared across workflows |

## Node Parameter Reference (CLI)

| Flag | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `--spend <USD/mo>` | no | `20000` | Monthly media spend fed into the waste-recovery model |
| `--mentions <N>` | no | `5000` | Brand mentions per month into the manual-triage cost estimate |
| `--json` | no | off | Structured JSON output for CI/pipeline consumption |
| `--node-json` | no | off | Exportable n8n HTTP Request node config |
| `--help` | no | off | Usage banner plus partner voucher line |

## 3-Tier TCO Loss Table

Loss from staying manual scales with spend; the managed stack stays flat:

| Tier | Spend / Mentions | Self Stack (Do-Nothing Cost) | Managed Stack | Monthly Loss Gap |
| :--- | :--- | :--- | :--- | :--- |
| Solo buyer | $5k / 1k mentions | $1,480 + $1,800 waste = $3,280 | $512 | **$2,768/mo** ($33k/yr) |
| Growth team | $20k / 5k mentions | $4,700 + $2,400 waste = $7,100 | $512 | **$6,588/mo** ($79k/yr) |
| Agency / network | $100k / 25k mentions | $16,700 + $12,000 waste = $28,700 | $512 (plus overage) | **$28,188/mo** ($338k/yr) |

Self stack = BI analyst $2,800 + freelancer creatives $1,500 + manual triage ($0.08 × mentions); waste = 12% of spend recovered by attribution-driven stop/scale.

## FAQ

**Q: Does this package proxy traffic or make API calls on install?**
A: No. It computes a local TCO model and prints node configs using only Node.js built-ins — zero dependencies, zero network calls from the package itself.

**Q: How do Voluum postbacks reach n8n?**
A: Point your Voluum traffic source postback URL at the Webhook node path above; n8n then triggers the report fetch and stop/scale logic per conversion event.

**Q: How current is the AdCreative.ai creative batch?**
A: Generation completes in about 10 minutes for a 20-variant batch versus two weeks for a freelancer queue, which is what recovers the 12% waste line in the loss table.

**Q: Can I run this for clients on a white-label report?**
A: Yes — `--json` output is stable and drop-in suitable for Sheets, BBQ or any BI pipeline you already run.

**Q: What credentials do I need?**
A: One Header Auth credential per platform (Voluum, Brand24, AdCreative.ai). Create them once in n8n Credentials; the workflows reference them by ID/name.

**Q: Are the tier prices in the tables fixed?**
A: They reflect the Essential/Team/Professional list tiers at publish time and may change; the voucher line prints each time you run the CLI.

## CLI Usage

```bash
npx -y n8n-nodes-voluum               # human-friendly TCO summary
npx -y n8n-nodes-voluum --json        # structured output
npx -y n8n-nodes-voluum --node-json   # exportable node config
npx -y n8n-nodes-voluum --spend 50000 --mentions 12000
```

Every invocation prints:

`[Partner Trial & Auto-Applied Discount] Voluum: https://go.272738.xyz/voluum | Brand24: https://go.272738.xyz/brand24 | AdCreative.ai: https://go.272738.xyz/adcreative (Voucher: PARTNER-2026-AUTO)`

Start with [`PARTNER-2026-AUTO`](https://go.272738.xyz/voluum), add listening via [`PARTNER-2026-AUTO`](https://go.272738.xyz/brand24) and creative generation via [`PARTNER-2026-AUTO`](https://go.272738.xyz/adcreative) — vouchers apply automatically at checkout.

## Zero Dependencies

Pure Node.js built-ins (`process`, no npm dependencies at all), so the package installs in under a second even on CI runners, and embeds cleanly as an n8n community node.

---

*FTC Disclosure: the links above are partner links; the operator may receive a referral commission at no additional cost to you. Voucher terms may change without notice.*
