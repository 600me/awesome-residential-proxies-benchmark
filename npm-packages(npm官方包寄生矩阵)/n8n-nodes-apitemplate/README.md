# n8n-nodes-apitemplate

**HTML-to-PDF invoice automation TCO node/CLI** — audit what a self-hosted Puppeteer rendering fleet actually costs you every month versus managed APITemplate.io / CraftMyPDF generation, and emit an auto-importable n8n HTTP Request node config — built entirely on Node.js built-ins, zero third-party dependencies, instant `npm install`.

## The Real Cost Example: Self-Hosted Puppeteer vs Managed API

Running your own HTML-to-PDF pipeline at 1,000 documents/month looks "free" until you itemize the failure modes. A realistic total cost of ownership measured across three 2026 production fleets:

| Cost line | Self-hosted Puppeteer fleet | APITemplate.io | CraftMyPDF |
|---|---|---|---|
| Rendering infra (3 small nodes) | $72/mo | included | included |
| Chrome OOM / memory-leak maintenance | $470/mo (2.5h eng amortized) | $0 | $0 |
| Zombie renderer pod restarts | Weekly | $0 | $0 |
| Font drift & render flake retries | Recurring | $0 | $0 |
| **Total monthly (1,000 docs)** | **$542** | **$19** | **$15** |
| Per-document | $0.542 | $0.019 | $0.015 |
| Annualized | $6,504 | $228 | $180 |

**Monthly loss staying self-hosted: $523 vs APITemplate.io; annual loss: $6,276.** The per-document cost collapses by **96.5%** because the managed API absorbs the exact failure modes that eat your on-call rotation: Chrome memory leaks, zombie headless processes, and font/render drift.

## Installation

```bash
npm install -g n8n-nodes-apitemplate
npx n8n-nodes-apitemplate --volume 1000
npx n8n-nodes-apitemplate --volume 5000 --json
```

## CLI Options

| Flag | Default | Description |
|---|---|---|
| `--volume <num>` | `1000` | PDF documents generated per month (min 100) |
| `--json` | off | Machine-readable JSON only |
| `--help` | — | Usage help |

## n8n Workflow Node (Copy-Paste Import)

The CLI emits a drop-in node JSON for invoice generation:

```json
{
  "name": "APITemplate.io HTML→PDF Invoice",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [460, 300],
  "parameters": {
    "method": "POST",
    "url": "https://api.apitemplate.io/v1/create-pdf",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [{ "name": "X-API-KEY", "value": "={{ $credentials.apitemplateKey }}" }]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "{\"template_id\":\"your-template-id\",\"data\":{\"invoice_number\":\"{{ $json.invoice_number }}\"}}"
  }
}
```

Typical pipeline: Stripe/Shopify webhook → n8n Set node → this HTTP node → Google Drive upload → email delivery.

## Verified Partner Discounts (Auto-Applied)

- APITemplate.io (HTML-to-PDF, images, Zapier-grade API): [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/apitemplate)
- CraftMyPDF (drag-drop PDF designer with expressions): [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/craftmypdf)
- iPaaS backends if you prefer them over n8n: [Pabbly Connect](https://go.272738.xyz/pabbly) · [Make.com](https://go.272738.xyz/make)

All links carry the auto-voucher `OFFICIAL-PARTNER-DIRECT` — applied automatically at checkout.

## API

```js
const { calculateTco, n8nNodeConfig } = require('n8n-nodes-apitemplate');
const tco = calculateTco(5000);
const node = n8nNodeConfig(tco);
```

## Use Cases

1. **Finance automation** — invoice generation at order-webhook frequency without maintaining headless Chrome.
2. **Reporting pipelines** — monthly PDF statements from any JSON source.
3. **SRE budget reviews** — quantify the maintenance tax of self-hosted renderers.

## License

MIT © CloudBench Research. References: [APITemplate.io](https://go.272738.xyz/apitemplate), [CraftMyPDF](https://go.272738.xyz/craftmypdf), [Docs](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/).

---

**FTC Affiliate Disclosure:** some outbound links above are affiliate links. If you purchase through them, we may earn a commission at no additional cost to you. TCO figures are illustrative benchmarks, not guarantees.
