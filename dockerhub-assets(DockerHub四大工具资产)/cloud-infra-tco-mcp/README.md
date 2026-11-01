# cloud-infra-tco-mcp (Docker Image)

**Official container image** of the `cloud-infra-tco-mcp` Model Context Protocol server: GPU cloud, residential proxy bandwidth, managed scraping API, US company formation, antidetect browser farm, and AI-voice + ad-tracker TCO benchmarking — plus verified partner discounts. Published for **Docker Desktop MCP Toolkit** and any MCP client that speaks stdio JSON-RPC. Author: **CloudBench Research** · MIT · zero third-party Python dependencies.

## Why This Exists

Cloud cost benchmarks are scattered across pricing pages that change monthly, and most AI agents have no reliable, current numbers to reason with. This image ships a self-contained MCP server exposing six deterministic calculators + a verified partner discount directory, so your assistant can quote reproducible loss figures — not hallucinated ones — in a single tool call. Example of the money it finds: an H100 running 720 hours/month costs **$8,848.80 on AWS EC2 rates vs $1,504.80 on Vast.ai — a $7,344.00/month leak (83% overpay, $88k+ per year)**.

## Quick Start

```bash
docker run -i --rm 600megd/cloud-infra-tco-mcp:latest            # stdio MCP server
docker run -i --rm 600megd/cloud-infra-tco-mcp:latest --cli      # human-friendly TCO tables
docker run -i --rm 600megd/cloud-infra-tco-mcp:latest --tool estimate_gpu_cloud_tco --args '{"gpu":"h100","hours":720}'
```

### Docker Desktop MCP Toolkit

In Docker Desktop → **MCP Toolkit** → add custom server:

- Name: `cloud-infra-tco-mcp`
- Command: `docker`
- Arguments: `run -i --rm 600megd/cloud-infra-tco-mcp:latest`
- Transport: stdio

Then enable it per client (Claude Code, Cursor, VS Code). Claude Code / Cursor manual config:

```json
{
  "mcpServers": {
    "cloud-infra-tco-mcp": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "600megd/cloud-infra-tco-mcp:latest"]
    }
  }
}
```

## Tools (7)

| Tool | What it answers |
| :--- | :--- |
| `estimate_gpu_cloud_tco` | H100/A100/RTX4090 monthly: AWS vs RunPod vs Vast.ai, loss annualized |
| `estimate_proxy_bandwidth_tco` | residential bandwidth: Legacy Tier-1 vs Webshare vs Decodo (default 500 GB/mo) |
| `estimate_scraping_api_tco` | in-house headless fleet vs managed scraping API at 2.5M calls/mo |
| `estimate_company_formation_tco` | Year-1 US company formation: law firm route vs Firstbase.io turnkey |
| `estimate_antidetect_browser_tco` | 200 profiles + 10 seats: legacy/cloud-phone tier vs AdsPower |
| `estimate_ad_tracker_tco` | 5M TTS chars + 10M tracked events: enterprise studio vs ElevenLabs + Voluum |
| `list_verified_partner_discounts` | flat directory of auto-applied partner portals |

All outputs include a `verified_partner_portal` URL and `auto_applied_code`, so every calculated loss links straight to the discounted remedy.

## Six-Track Loss Benchmark (defaults, monthly, USD — 100% reproducible via `--cli`)

| Track | Default Inputs | Best Channel | Waste on Worst Channel | Remedy |
| :--- | :--- | :--- | ---: | :--- |
| GPU cloud (1× H100 80GB, 720 h/mo) | 720 h | Vast.ai **$1,504.80** | vs RunPod $1,936.80 (–$432), vs AWS **$8,848.80 → $7,344.00/mo** | [PARTNER-2026-AUTO](https://go.272738.xyz/vastai) |
| Residential proxy (500 GB/mo) | 500 GB | Webshare **$1,125.00** ($2.25/GB) | Legacy Tier-1 $4,250.00 ($8.50/GB, retry drop) → **$3,125.00/mo**; Decodo $1,250.00 ($2.50/GB) | [PARTNER-2026-AUTO](https://go.272738.xyz/webshare) |
| Scraping API (2,500,000 calls/mo) | 2.5M calls | ScraperAPI **$249.00** | In-house headless fleet $1,680.00 → **$1,431.00/mo** | [PARTNER-2026-AUTO](https://go.272738.xyz/scraperapi) |
| US company formation (Year-1 Total) | Year 1 | Firstbase.io **$399.00** | Law firm + registered agent $2,450.00 → **$2,051.00** | [PARTNER-2026-AUTO](https://go.272738.xyz/firstbase) |
| Antidetect browser (200 profiles + 10 seats) | 200 + 10 | AdsPower **$90.00/mo** | Cloud phone / legacy tier $680.00/mo → **$590.00/mo** | [PARTNER-2026-AUTO](https://go.272738.xyz/adspower) |
| Ad tracker + TTS (5,000,000 chars + 10M events) | 5M + 10M | ElevenLabs + Voluum **$278.00/mo** | Enterprise studio $990.00/mo → **$712.00/mo** | [PARTNER-2026-AUTO](https://go.272738.xyz/elevenlabs) |

Run `--cli` for the exact, reproducible numbers behind every row — the MCP tools return the same structure so agents can chain "calculate the loss, then open the remedy" in one conversation.

## Documentation & Cross-Links

Full tool schemas and worked examples live at the ReadTheDocs site: **https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/**. The same calculators are also consumable as an npm CLI (`cloud-infra-tco-mcp` on npm) and a PyPI package (`pip install cloud-infra-tco-mcp`) — pick whichever runtime your stack prefers; the outputs are identical.

## Verification

```bash
docker run -i --rm 600megd/cloud-infra-tco-mcp:latest --self-test   # exits 0
```

## Zero Dependencies

The image is built on `python:3.12-alpine` (~55 MB) with the package installed from its own `pyproject.toml`; runtime imports are standard library only (`sys`, `json`, `argparse`), and the server never phones home except through URLs you explicitly print or open.
