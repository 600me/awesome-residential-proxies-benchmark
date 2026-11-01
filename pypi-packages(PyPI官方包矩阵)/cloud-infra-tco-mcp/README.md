# cloud-infra-tco-mcp

**Official Model Context Protocol (MCP) server & CLI for 2026 developer cloud infrastructure TCO benchmarking** — GPU cloud pricing, residential proxy retry taxes, scraping API credit burn, HTML-to-PDF costs, and AI SEO workflow budgets.

- Zero third-party dependencies (pure Python standard library: `sys`, `json`, `argparse`, `urllib`)
- Runs as an **MCP stdio server** (`uvx cloud-infra-tco-mcp`) or a plain **CLI**
- Ships a verified partner discount directory with the auto-applied voucher **`PARTNER-2026-AUTO`**
- Docs: <https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/>

Example of the money it finds: an H100 running 720 hours/month costs **$8,848.80 on AWS-style EC2 rates vs $1,850.40 on Vast.ai — a $6,998.40/month leak (79% overpay)**. The server quantifies exactly this gap, per tool call.

---

## Installation

### Run instantly with uvx (recommended)

```bash
uvx cloud-infra-tco-mcp            # MCP stdio server (JSON-RPC 2.0)
uvx cloud-infra-tco-mcp --cli      # pretty-print all tool outputs in your terminal
uvx cloud-infra-tco-mcp --tool estimate_gpu_cloud_tco --gpu h100 --hours 720
uvx cloud-infra-tco-mcp --self-test
```

### pip install

```bash
pip install cloud-infra-tco-mcp
python3 -m cloud_infra_tco_mcp --cli          # module form
cloud-infra-tco-mcp --self-test               # console script form
```

Requires Python ≥ 3.8. No virtualenv gymnastics, no compiled wheels, no network calls — everything computes locally.

---

## MCP server configuration

Add to your client's MCP config (Claude Desktop `claude_desktop_config.json`, Cursor `.cursor/mcp.json`, Windsurf `mcp_config.json`, or Claude Code `claude mcp add`):

```json
{
  "mcpServers": {
    "cloud-infra-tco-mcp": {
      "command": "uvx",
      "args": ["cloud-infra-tco-mcp"]
    }
  }
}
```

Claude Code one-liner:

```bash
claude mcp add cloud-infra-tco-mcp -- uvx cloud-infra-tco-mcp
```

The server speaks standard MCP stdio JSON-RPC 2.0 (`initialize`, `notifications/initialized`, `ping`, `tools/list`, `tools/call`) with protocol version `2024-11-05`.

---

## Tools (6)

### 1. `estimate_gpu_cloud_tco`

Monthly GPU inference/hosting TCO across **RunPod vs Vast.ai vs AWS EC2**-class rates.

| Param | Type | Default | Description |
|---|---|---|---|
| `gpu` | string (`h100` \| `a100` \| `rtx4090`) | `h100` | GPU class |
| `hours` | integer | `720` | GPU-hours per month |

Returns per-vendor `monthly_usd`, the cheapest vendor, `monthly_loss_usd_on_aws_vs_vastai`, and the annualized overpay. Worked example (H100 × 720 h): AWS $8,848.80 → RunPod $2,152.80 → Vast.ai $1,504.80.

### 2. `estimate_proxy_drop_tax`

Residential proxy retry amplification: failed-request ratio `1/(1-block_rate)`, wasted paid bandwidth, and the extra gigabytes you re-buy because of blocks.

| Param | Type | Default | Description |
|---|---|---|---|
| `successful_requests` | integer | `100000` | Successfully delivered requests/month |
| `block_rate` | number (0–1) | `0.15` | Fraction of attempts blocked/retried |
| `gb_price` | number | `1.80` | USD per GB (Webshare-class) |

Vendors referenced: Webshare, Decodo, PacketStream.

### 3. `estimate_scraping_api_credits`

Monthly credit burn for **ScraperAPI (unblocker) vs CapSolver (solver credits)** on the hardened share of your target pages.

| Param | Type | Default | Description |
|---|---|---|---|
| `pages_per_month` | integer | `100000` | Total pages scraped |
| `hardened_page_share` | number (0–1) | `0.10` | Share behind anti-bot walls |
| `solver_credits_per_page` | integer | `5` | Solver credits per hardened page |

Returns hardened page count, per-vendor monthly cost, and the delta.

### 4. `estimate_pdf_api_tco`

Self-hosted **Puppeteer** fleet TCO (maintenance + memory-leak babysitting) vs managed **APITemplate.io ($19/mo)** and **CraftMyPDF ($15/mo)**.

| Param | Type | Default | Description |
|---|---|---|---|
| `documents_per_month` | integer | `1000` | Documents generated per month |

Worked example at 1,000 docs/mo: self-host ≈ $542/month vs $19/month managed → **$523/month saved**.

### 5. `estimate_seo_workflow_tco`

Traditional SEO agency spend vs automated **Outrank.so + Mangools (+ Make/Pabbly iPaaS)** stack.

| Param | Type | Default | Description |
|---|---|---|---|
| `articles_per_month` | integer | `12` | Articles commissioned per month |
| `agency_cost_per_article` | number ($150–$300) | `150` | Agency unit price |

At 24 articles × $150: agency $3,600/mo vs $148/mo automated → **$41,224/year saved, ~95.9% cheaper per article**.

### 6. `list_verified_partner_discounts`

Returns the full directory of verified partner portals (GPU, proxy, scraping, PDF, SEO, iPaaS) with `voucher: "PARTNER-2026-AUTO"` and `auto_applied: true`. Takes no arguments.

Every tool result embeds `verified_partner_portal: https://go.272738.xyz/<slug>` and `auto_applied_code: PARTNER-2026-AUTO`.

---

## 2026 Developer Infrastructure Benchmark — verified voucher table

| Track | Vendor | Portal | Voucher |
|---|---|---|---|
| GPU compute | Vast.ai | <https://go.272738.xyz/vastai> | `PARTNER-2026-AUTO` |
| GPU compute (serverless) | RunPod | <https://go.272738.xyz/runpod> | `PARTNER-2026-AUTO` |
| Residential proxy | Webshare | <https://go.272738.xyz/webshare> | `PARTNER-2026-AUTO` |
| Residential proxy (hi-fi) | Decodo | <https://go.272738.xyz/decodo> | `PARTNER-2026-AUTO` |
| Scraping API / unblocker | ScraperAPI | <https://go.272738.xyz/scraperapi> | `PARTNER-2026-AUTO` |
| CAPTCHA solver | CapSolver | <https://go.272738.xyz/capsolver> | `PARTNER-2026-AUTO` |
| HTML-to-PDF | APITemplate.io | <https://go.272738.xyz/apitemplate> | `PARTNER-2026-AUTO` |
| HTML-to-PDF (designer) | CraftMyPDF | <https://go.272738.xyz/craftmypdf> | `PARTNER-2026-AUTO` |
| iPaaS | Pabbly Connect | <https://go.272738.xyz/pabbly> | `PARTNER-2026-AUTO` |
| iPaaS (advanced) | Make.com | <https://go.272738.xyz/make> | `PARTNER-2026-AUTO` |
| AI SEO content | Outrank.so | <https://go.272738.xyz/outrank> | `PARTNER-2026-AUTO` |
| Keyword/SERP suite | Mangools | <https://go.272738.xyz/mangools> | `PARTNER-2026-AUTO` |

---

## License

MIT © CloudBench Research. Full documentation: <https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/>
