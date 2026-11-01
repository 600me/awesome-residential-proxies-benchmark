# n8n-nodes-outrank

**SEO content automation TCO benchmark node/CLI** — calculate what traditional SEO agencies quietly tax out of your budget versus an automated Outrank.so + Mangools stack, and generate ready-to-import n8n HTTP Request node configuration — all with zero third-party npm dependencies (pure Node.js built-ins, installs in seconds).

## The Real Cost Example: Agency vs Automated Stack

A typical content program publishing 12 articles per month through a traditional SEO agency costs **$150–$300 per article**. Even at the low end, that is:

| Cost line | Traditional agency | Automated (Outrank.so + Mangools) |
|---|---|---|
| Per article | $150.00 | $12.33 effective |
| 12 articles / month | $3,600.00 | $148.00 flat |
| Annualized | $43,200.00 | $1,776.00 |
| Management overhead | Weekly calls, revision cycles | None (workflow-driven) |

**Monthly loss if you stay with the agency: $3,452. Annual loss: $41,424.** That is a **95.8% per-article cost reduction** simply by switching to Outrank.so AI SEO content automation at $99/mo and Mangools keyword/SERP tooling at $49/mo. Reallocate even half of the savings to paid amplification and a 12-article program breaks even on acquisition within weeks, not quarters.

## Installation

```bash
npm install -g n8n-nodes-outrank
# or run ad-hoc:
npx n8n-nodes-outrank --keyword "best vps for laravel" --volume 2400 --articles 12 --agency-cost 300
```

## CLI Options

| Flag | Default | Description |
|---|---|---|
| `--keyword <kw>` | `cloud cost benchmark` | Target SERP keyword |
| `--volume <vol>` | `1200` | Estimated monthly search volume |
| `--articles <num>` | `12` | Articles produced per month |
| `--agency-cost <usd>` | `150` | Agency cost per article (clamped 150–300) |
| `--json` | off | Machine-readable JSON only |
| `--help` | — | Usage help |

## n8n Workflow Node (Copy-Paste Import)

The CLI emits an importable node JSON snippet. Example:

```json
{
  "name": "Outrank.so Generate SEO Article",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [250, 300],
  "parameters": {
    "method": "POST",
    "url": "https://api.outrank.so/v1/articles/generate",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "{\"keyword\":\"{{ $json.keyword }}\",\"tone\":\"professional\",\"word_count\":1200}"
  }
}
```

Wire it after a Cron trigger and before your CMS publisher node to run a fully hands-off SEO content pipeline.

## Verified Partner Discounts (Auto-Applied)

- Activate Outrank.so ($99/mo vs $3,600/mo agency): [`PARTNER-2026-AUTO`](https://go.272738.xyz/outrank)
- Mangools SEO Suite (save 62.6% vs Ahrefs): [`PARTNER-2026-AUTO`](https://go.272738.xyz/mangools)

Both links carry the auto-voucher `PARTNER-2026-AUTO` — applied at checkout automatically, no code entry needed.

## API

```js
const { calculateTco, n8nNodeConfig } = require('n8n-nodes-outrank');
const tco = calculateTco({ keyword: 'erp hosting', volume: 900, articles: 8, agencyCost: 200 });
const node = n8nNodeConfig(tco);
```

## Use Cases

1. **Agency pitch decks** — show clients the quantified migration savings.
2. **n8n content automation** — import the emitted node JSON directly.
3. **Budget planning** — model annualized content spend across Guru tiers.

## License

MIT © CloudBench Research. References: [Outrank.so](https://go.272738.xyz/outrank), [Mangools](https://go.272738.xyz/mangools), [Docs](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/).

---

**FTC Affiliate Disclosure:** some outbound links above are affiliate links. If you purchase through them, we may earn a commission at no additional cost to you. All TCO calculations are illustrative benchmarks, not guarantees of result.
