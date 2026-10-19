### 600me — Cost Engineering for Cloud, GPU, Scraping and Cross-Border SaaS

Independent, reproducible cost research. Every tool below is **free, zero-signup and runs
arithmetic in your browser or your terminal** — no account, no email wall, no "request a demo".

The premise is simple: vendor price lists are quoted in units your business does not actually buy
(GPU-hours, gigabytes, requests, MoR percentage). These calculators and CLIs convert them into the
unit you do buy — **cost per usable GPU-hour, per 1,000 clean pages, per completed flow, per
retained dollar**.

---

## 🧮 Interactive Engineering Calculators (Zero-Signup, Open Formulas)

Every formula is visible on the page. Nothing is uploaded; all math runs client-side.

| Calculator | What it prices | Hosted | Dataset |
|---|---|---|---|
| 🖥️ **LLM VRAM & GPU Cloud True TCO Calculator** | Weights + KV cache (GQA/MLA), NVLink vs PCIe topology, card-count rounding, RunPod/Vast.ai bundle billing → **cost per useful GPU-hour** | [gpu.mybskm.top/calculator](https://gpu.mybskm.top/calculator/?utm_source=gh_profile) · [HF Space](https://huggingface.co/spaces/600me/llm-gpu-cost-calculator) | [HF Dataset](https://huggingface.co/datasets/600me/gpu-cloud-h100-a100-pricing-benchmark) |
| 🕷️ **LLM/RAG Web Scraping & Anti-Bot True TCO Calculator** | `1/(1-block_rate)` retry amplification, challenge-page bandwidth bloat, Chromium render cost, managed-credit tiers → **$ per 1,000 clean Markdown pages** | [scrape.mybskm.top/calculator](https://scrape.mybskm.top/calculator/?utm_source=gh_profile) · [HF Space](https://huggingface.co/spaces/600me/rag-web-scraping-cost-calculator) | [HF Dataset](https://huggingface.co/datasets/600me/web-scraping-anti-bot-api-benchmark) |
| 🌐 **Residential Proxy Sticky Session & `cf_clearance` Loss Calculator** | Premature sticky-IP drops invalidating `cf_clearance`, geometric re-run tax, real GB burned → **sticky sessions vs per-request rotation, monthly** | [proxy.mybskm.top/calculator](https://proxy.mybskm.top/calculator/?utm_source=gh_profile) · [HF Space](https://huggingface.co/spaces/600me/residential-proxy-sticky-session-calculator) | [HF Dataset](https://huggingface.co/datasets/600me/residential-proxy-commercial-policy-matrix) |
| 💳 **Non-US Indie SaaS: MoR (Paddle/LS) vs US LLC + Stripe Breakeven** | 5% Merchant-of-Record drag vs Wyoming/Delaware franchise tax, registered agent, Form 5472 exposure → **at which MRR the LLC wins** | [pay.mybskm.top](https://pay.mybskm.top/?utm_source=gh_profile) · [HF Space](https://huggingface.co/spaces/600me/ai-saas-stripe-vs-mor-tax-calculator) | [HF Dataset](https://huggingface.co/datasets/600me/global-saas-mor-vs-us-llc-fee-matrix) |

---

## 📊 Public Benchmark Datasets (HuggingFace, MIT-licensed, viewer-ready)

Every model above also ships as a machine-readable dataset with a documented schema, so you can audit
or re-run the arithmetic instead of trusting a screenshot. CSV + JSONL, 10–252 rows each, rendered by
the HuggingFace Dataset Viewer.

| Dataset | What is inside | Rows |
|---|---|---|
| [`gpu-cloud-h100-a100-pricing-benchmark`](https://huggingface.co/datasets/600me/gpu-cloud-h100-a100-pricing-benchmark) | RunPod / Vast.ai / Lambda / CoreWeave / AWS / GCP / Azure list rates for H100 SXM & PCIe, A100 80GB, L40S, RTX 4090 + cold-start, NVMe and 85%-utilisation effective cost per useful GPU-hour | 28 |
| [`web-scraping-anti-bot-api-benchmark`](https://huggingface.co/datasets/600me/web-scraping-anti-bot-api-benchmark) | ScraperAPI, ZenRows, ScrapingBee, Crawlbase, Bright Data, Smartproxy residential and self-hosted Playwright: JS/premium credit multipliers, block rates, retry amplification, $/1k clean pages (measured + hard-target stress) | 14 |
| [`residential-proxy-commercial-policy-matrix`](https://huggingface.co/datasets/600me/residential-proxy-commercial-policy-matrix) | 9-dimension commercial matrix for Smartproxy (Decodo), Bright Data, Oxylabs, IPRoyal, SOAX, Webshare and the free `curl_cffi + WARP` baseline, plus sticky-session re-run tax across 3 flow shapes | 21 |
| [`global-saas-mor-vs-us-llc-fee-matrix`](https://huggingface.co/datasets/600me/global-saas-mor-vs-us-llc-fee-matrix) | Paddle / Lemon Squeezy 5% + $0.50 vs US LLC + Stripe 2.9% + intl/FX surcharges across $1k–$50k MRR, $15–$99 AOV and 3 card mixes, with 3-year net retained and Firstbase / Atlas / Doola entity costs | 252 |

Usage:

```bash
pip install datasets
python3 -c "from datasets import load_dataset; print(load_dataset('600me/residential-proxy-commercial-policy-matrix', split='train')[:3])"
```

---

## 🛠 Open-Source CLI & Reproducible Benchmarks

| Repository | What it does |
|---|---|
| [`600me/check-proxy-tax`](https://github.com/600me/check-proxy-tax) | Zero-dependency Python CLI (stdlib only). Fires a concurrent burst at one URL, classifies every response as usable or blocked, and reports usable rate, p50/p95 latency, bytes transferred and **effective cost per 1,000 usable requests** — the retry tax plus bandwidth amplification your invoice never shows. |
| [`600me/awesome-web-scraping-apis-benchmark`](https://github.com/600me/awesome-web-scraping-apis-benchmark) | Cloudflare/Turnstile bypass and cost benchmark across managed scraping APIs: credit multipliers, render surcharges, and the only metric that survives production. |
| [`600me/awesome-residential-proxies-benchmark`](https://github.com/600me/awesome-residential-proxies-benchmark) | 9-dimension commercial policy and sticky-session telemetry matrix — session TTL, pool transparency, pricing granularity, concurrency limits, refund terms. |
| [`600me/awesome-gpu-cloud-pricing-benchmark`](https://github.com/600me/awesome-gpu-cloud-pricing-benchmark) | Daily H100/A100 SXM vs PCIe pricing and hidden-cost tracker: egress, NVMe, cold-start pre-pull, bundle minimums. |
| [`600me/awesome-indie-global-payments-matrix`](https://github.com/600me/awesome-indie-global-payments-matrix) | Cross-border SaaS payment and US LLC compliance math for non-US founders, with the full 3-year cost ledger. |

---

## 📉 Deep Engineering Teardowns & A-vs-B Cost Audits (2026)

Long-form, arithmetic-first research. Each page shows the full cost model, the crossover point, and
where the "cheap" option stops being cheap.

**GPU & LLM inference**
- [The H100 Rental Trap: Why $2.13 per GPU-Hour Is Not the Price You Pay](https://gpu.mybskm.top/blog/h100-rental-trap.html?utm_source=gh_profile) — catalogue rate vs effective cost of a *useful* GPU-hour after bundle minimums, utilization gaps and restart overhead.
- [RunPod vs Vast.ai (2026): Real H100 & A100 Effective Cost After Cold-Start, NVMe Storage & Bandwidth Billing](https://gpu.mybskm.top/blog/runpod-vs-vastai-h100-a100.html?utm_source=gh_profile) — a 150 GB two-hour test costs 63% more on the "25% cheaper" marketplace; a 24/7 node flips back above 5.4 TB/month.

**Scraping & anti-bot**
- [The 403 Tax: What Anti-Bot Protection Really Does to Your Scraping Bill](https://scrape.mybskm.top/blog/403-tax.html?utm_source=gh_profile) — credit multipliers, retry amplification, and the metric that survives production.
- [Smartproxy (Decodo) vs ScraperAPI (2026): Raw Residential Pool vs Managed Anti-Bot Unblocker TCO](https://scrape.mybskm.top/blog/smartproxy-vs-scraperapi.html?utm_source=gh_profile) — $3.50/GB vs $299/month are not competing products; three worked scenarios plus the 30-line hybrid router.
- [The $0.49 Proxy Illusion: How a 200-Line CLI Exposes Real Scraping Costs](https://scrape.mybskm.top/blog/proxy-cost-audit.html?utm_source=gh_profile) — instrumenting a real burst to convert advertised price into cost per usable page.
- [Why Rotating Residential Proxies Still Get 403s: Sticky Session TTL, JA3 Fingerprints and ASN Economics](https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html?utm_source=gh_profile) — a rotating IP is not a trusted IP; how clearance binding creates the re-run tax.

**Cross-border payments & compliance**
- [The 5% MoR Illusion: Exact US LLC + Stripe Breakeven for Non-US SaaS Founders (2026)](https://pay.mybskm.top/blog/mor-vs-us-llc-breakeven.html?utm_source=gh_profile) — break-even at $3,205 / $5,376 / $15,152 MRR across three real card mixes, compliance bill included.
- [Firstbase vs Stripe Atlas vs Doola (2026): True 3-Year US LLC Cost for Non-US Founders](https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html?utm_source=gh_profile) — formation fee is not the price: $876 vs $1,600 vs $6,177 over three years, plus the $25,000 Form 5472 penalty exposure.

---

### Method & disclosure

- **Reproducible by design.** Static HTML + vanilla JS, or a single stdlib-only Python module. Read the source, re-run the numbers, argue with the arithmetic.
- **Vendor-neutral arithmetic.** Calculators include links to commercial providers, some of which are affiliate links. Commission never changes a formula, a default or a recommendation — the models are also published as standalone HTML and JSON you can audit.
- **Planning models, not quotes.** Published rates are snapshots and can change; verify live pricing with the provider before you commit money. Model output is arithmetic, not a measured benchmark or a guarantee.
