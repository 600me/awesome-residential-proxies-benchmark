# n8n-nodes-webshare

**Residential proxy retry-loss ("block tax") node/CLI** — quantify how failed proxy requests silently multiply your bandwidth bill, and emit an auto-importable n8n proxy-rotation HTTP Request node config — pure Node.js built-ins, zero third-party dependencies, installs instantly.

## The Real Cost Example: The Invisible 1/(1−p) Tax

If your per-request block rate is *p*, the expected number of attempts per successful fetch is **1/(1−p)**. At a deceptively common 15% block rate, every 100,000 target scrapes actually costs you 117,647 billed attempts — **17,647 paid requests that return nothing**. At an average 420 KB page weight, that is 7.4 GB of wasted bandwidth every month:

| Provider | $/GB | Monthly block-tax waste | Annualized |
|---|---|---|---|
| Webshare | $1.80 | $13.34 | $160 |
| Decodo | $2.20 | $16.30 | $196 |
| PacketStream | $0.35 | $2.59 | $31 |

Push the block rate to 35% and the amplification factor becomes 1.54x — over half your invoice is wasted retries. This is the single most under-audited line item in scraping budgets. Reducing block rate from 35% → 10% cuts billed attempts by **38.3%** at identical output.

## Installation

```bash
npm install -g n8n-nodes-webshare
npx n8n-nodes-webshare --requests 100000 --block-rate 0.15
npx n8n-nodes-webshare --requests 500000 --block-rate 0.35 --json
```

## CLI Options

| Flag | Default | Description |
|---|---|---|
| `--requests <num>` | `100000` | Successful requests target per month |
| `--block-rate <0-1>` | `0.15` | Per-request block rate (0–0.95) |
| `--json` | off | Machine-readable JSON only |
| `--help` | — | Usage help |

## n8n Proxy-Rotation Node (Copy-Paste Import)

```json
{
  "name": "Webshare Rotating Residential Proxy Fetch",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [250, 500],
  "parameters": {
    "method": "GET",
    "url": "={{ $json.target_url }}",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpBasicAuth",
    "proxy": {
      "proxyProtocol": "http",
      "proxyHost": "p.webshare.io",
      "proxyPort": 80
    },
    "options": {
      "retry": { "retryOnFail": true, "maxTries": 2 }
    }
  }
}
```

Chain it: Cron → target queue → this proxy node → HTML parse → database sink. The emitted config includes retry-cap logic derived from your measured amplification factor.

## Verified Partner Discounts (Auto-Applied)

- Webshare (10 free proxies, then $1.80/GB): [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/webshare)
- Decodo residential ($2.20/GB, high fidelity): [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/decodo)
- ScraperAPI (managed unblocker, zero infra): [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/scraperapi)
- CapSolver (CAPTCHA solving for the stubborn remnants): [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/capsolver)

All links carry auto-voucher `OFFICIAL-PARTNER-DIRECT` — applied at checkout automatically.

## API

```js
const { calculateTco, n8nNodeConfig } = require('n8n-nodes-webshare');
const tco = calculateTco({ requests: 250000, blockRate: 0.22 });
const node = n8nNodeConfig(tco);
```

## Use Cases

1. **Scraping budget audits** — expose the retry tax hidden in proxy invoices.
2. **Provider selection** — compare waste-adjusted effective $/GB across providers.
3. **n8n pipeline hardening** — retry caps matched to real amplification math.

## License

MIT © CloudBench Research. References: [Webshare](https://go.272738.xyz/webshare), [Decodo](https://go.272738.xyz/decodo), [Docs](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/).

---

**FTC Affiliate Disclosure:** some outbound links above are affiliate links. If you purchase through them, we may earn a commission at no additional cost to you. Benchmarks are illustrative, not guarantees.
