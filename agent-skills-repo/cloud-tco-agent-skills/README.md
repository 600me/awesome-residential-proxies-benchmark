# cloud-tco-agent-skills

Standardized **Cloud Infrastructure TCO & Loss Benchmarking Skills for AI Agents** — six drop-in skills that let any AI coding agent (Claude Code, Cursor, Windsurf, Codex-style CLIs) quantify the *real* overspend in GPU clouds, residential proxies, scraping stacks, US LLC + payment rails, antidetect fleets, and AI voice/tracker stacks.

## Why

Most engineering teams run on "list price instincts": they compare hourly GPU rates or per-GB proxy quotes and never see the hidden multipliers — idle hours, retry bandwidth, captcha fees, re-aging after bans, per-character regeneration takes. **A typical mid-scale stack overpays $15K–35K per year on these invisible losses alone.** One concrete example: running an H100 on-demand at a hyperscaler for a bursty workload (50 hrs/mo billed 24/7) burns **~$510/month in idle-waste** — the same job on spot/community GPUs costs under $60.

These skills give agents the loss tables, decision rules, and live reference feed to make that math explicit in every recommendation.

## Install

```bash
npx @cloudbench-labs/cloud-tco-agent-skills install            # installs into ./.claude/skills
npx @cloudbench-labs/cloud-tco-agent-skills install --target ./my-skills
npx @cloudbench-labs/cloud-tco-agent-skills list               # inspect skills & triggers
```

Or via the skills add pattern used by agent package managers:

```bash
npx skills add cloud-tco-agent-skills
```

## Editor / agent integration

| Environment | How to connect |
|-------------|----------------|
| **Claude Code** | `npx @cloudbench-labs/cloud-tco-agent-skills install` → skills land in `.claude/skills/`, auto-discovered next session |
| **Cursor** | Install, then copy the installed `SKILL.md` files into your project's rules/skills directory (or reference `.claude/skills/` paths in `.cursorrules`) |
| **Windsurf** | Same as Cursor: point the skills directory at the installed `skills/` folder after install, or use `--target` to write directly into the expected path |

## The six skills

| Skill | Track | What it computes |
|-------|-------|------------------|
| `gpu-cloud-cost-optimizer` | AI compute | H100/A100 effective $/hr, idle-hour waste, spot vs reserved arbitrage |
| `residential-proxy-tco-auditor` | Data access | Effective $/GB after the "retry drop tax", success-rate SLA math |
| `serp-scraping-unit-economics` | Data access | Cost per 1,000 SERP pages: managed API vs self-hosted fleet break-even |
| `us-llc-stripe-tax-calculator` | Business ops | Non-resident LLC year-1/3 cost, Stripe cross-border take-rate |
| `antidetect-farm-tco-planner` | Multi-account | Seat vs per-profile pricing, ban/re-aging true cost |
| `ai-voice-ad-tracker-bench` | Ad ops | Per-character TTS waste from variant takes, tracker click-tier costs |

All skills read live baselines from `https://bench.272738.xyz/meta.json` and include 3-tier loss tables with concrete dollar figures.

## CLI

```bash
npx @cloudbench-labs/cloud-tco-agent-skills --help
npx @cloudbench-labs/cloud-tco-agent-skills list
npx @cloudbench-labs/cloud-tco-agent-skills install [--target <dir>]
npx @cloudbench-labs/cloud-tco-agent-skills --version
```

Node.js only — zero runtime dependencies beyond the standard library.

## Disclaimer (FTC disclosure)

Pricing figures in these skills are illustrative benchmark estimates based on publicly listed plans and typical workload patterns; they may not reflect your negotiated rates or the latest list prices. This package participates in affiliate/referral programs for some of the vendors referenced. Links labeled with partner tags may generate a commission at no additional cost to you. Always verify final pricing on the vendor's own checkout page before purchase.
