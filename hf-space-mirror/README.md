---
title: Residential Proxy Sticky Session & cf_clearance Loss Calculator
emoji: 🌐
colorFrom: blue
colorTo: indigo
sdk: static
app_file: index.html
pinned: false
license: mit
short_description: Price the re-run tax when sticky proxy IPs drop mid-flow
---

# Residential Proxy Sticky Session & `cf_clearance` Loss Calculator

A single-file, zero-dependency Static Space for the question that decides a residential proxy bill:
**what does one completed flow actually cost after premature IP drops and invalidated `cf_clearance`
tokens?**

An invoice is priced per gigabyte. A crawler is paid in flows that finish. When a sticky residential
IP disappears halfway through a login or a checkout, the `cf_clearance` token bound to that IP no
longer matches the new exit IP, so every completed step is replayed from zero — and every replayed
byte is still metered.

## What it computes

- **Expected step runs:** `steps / (1 - drop_rate)` — with a per-flow drop probability, a flow needs
  a geometric number of attempts and only the last one completes.
- **Re-run loss rate:** `drop_rate / (1 - drop_rate)` — the share of step executions that are pure
  waste.
- **Real traffic per flow:** `steps / (1 - drop_rate) × payload` — what the vendor meters, including
  the bytes inside flows that never finished.
- **Monthly attempts:** `concurrency × (active_minutes / session_duration) × 30`.
- **Monthly ledger for two strategies:** sticky sessions versus forced per-request rotation, each
  with its own hazard rate, real GB, total cost, completed flows and **cost per completed flow**.
- **The crossover:** the delta panel states when rotation is actually cheaper, which is exactly the
  case long flows on an unreliable pool hide.

All inputs — concurrency, session duration, drop rate, steps per flow, nominal `$ / GB`, payload per
step, active hours and rotation challenge-failure rate — recompute live in the browser. Three presets
(checkout 3 min, login + cart 10 min, dashboard 30 min) cover the common shapes.

## Why static

`sdk: static` serves this Space as plain HTML/CSS/JS: no container, no Python server, no cold start.
`index.html` is the complete page, with no external scripts, stylesheets, fonts or tracking pixels.
The page is byte-identical to the tool published at
`https://proxy.mybskm.top/calculator/` apart from the affiliate attribution parameter.

## Files

- `index.html` — the complete calculator, styles and vanilla JavaScript.
- `README.md` — this Space card and static SDK metadata.

## Links

- Main-site calculator: https://proxy.mybskm.top/calculator/
- Live matrix and telemetry: https://proxy.mybskm.top/
- The sticky-session deep dive: https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html
- CLI audit (`check-proxy-tax`): https://github.com/600me/check-proxy-tax

## The four Hugging Face Static Spaces in this matrix

1. [GPU Fit & Cost Calculator](https://huggingface.co/spaces/600me/llm-gpu-cost-calculator) — VRAM sizing, NVLink topology and GPU rental TCO.
2. [LLM/RAG Web Scraping TCO Calculator](https://huggingface.co/spaces/600me/rag-web-scraping-cost-calculator) — cost per 1,000 clean Markdown pages.
3. **This Space** — residential proxy sticky-session and `cf_clearance` re-run economics.
4. [MoR vs US LLC + Stripe Breakeven Calculator](https://huggingface.co/spaces/600me/ai-saas-stripe-vs-mor-tax-calculator) — the cross-border SaaS payment model.

Full-size sites: [gpu.mybskm.top](https://gpu.mybskm.top/) · [scrape.mybskm.top](https://scrape.mybskm.top/) · [proxy.mybskm.top](https://proxy.mybskm.top/) · [pay.mybskm.top](https://pay.mybskm.top/)

## Disclosure and scope

The Smartproxy (Decodo) button is an affiliate link (`src=hf_space_proxy_calc`). We may earn a
commission at no additional cost to the visitor, and the commission does not change any formula,
default or recommendation — the arithmetic is published on the page and independently cross-checked
against a Python implementation (`test_calculator_math.py`).

Model output is planning arithmetic, not a vendor quote, a measured benchmark or a guarantee of
success rate. Providers set their own prices, pool terms, session windows and concurrency limits;
confirm live pricing and policy before buying.
