---
license: mit
task_categories:
  - tabular-classification
language:
  - en
tags:
  - residential-proxy
  - proxy-pricing
  - smartproxy
  - bright-data
  - oxylabs
  - iproyal
  - soax
  - webshare
  - sticky-session
  - tco
  - benchmark
size_categories:
  - n<1K
pretty_name: "Residential Proxy 9-Dimension Commercial Policy & Sticky-Session Loss Matrix (2026)"
---

# Residential Proxy 9-Dimension Commercial Policy & Sticky-Session Loss Matrix (2026)

Per-GB list price is the least useful number in a proxy contract. This dataset records nine commercial
dimensions per vendor plus the **sticky-session re-run tax** across three realistic flow shapes.

## Files

| File | Rows | Description |
|---|---|---|
| `data/residential_proxy_9d_matrix_2026.csv` | 21 | 7 providers x 3 flow scenarios |
| `data/residential_proxy_9d_matrix_2026.jsonl` | 21 | Same records as newline-delimited JSON |

## The nine dimensions

1. Entry PAYG USD/GB
2. Volume price at 100 GB
3. Billing granularity
4. Minimum deposit
5. Free trial
6. Refund window (days)
7. Pool size (millions of IPs) and country coverage
8. KYC friction
9. Sticky-session window (max + default minutes)

## Schema

| Column | Type | Meaning |
|---|---|---|
| `provider` | string | Vendor, incl. the free `curl_cffi + WARP` baseline |
| `entry_usd_per_gb` | float | Cheapest advertised PAYG rate |
| `volume_100gb_usd_per_gb` | float | Effective rate at 100 GB |
| `min_deposit_usd` | float | Cash needed to start |
| `refund_window_days` | int | Self-serve refund window, 0 = none published |
| `kyc_required` | string | Account friction before traffic flows |
| `sticky_max_minutes` | int | Longest documented session hold |
| `scenario` | string | `checkout_3min`, `login_cart_10min`, `dashboard_30min` |
| `hazard_pct` | float | Probability the flow must restart before completing |
| `rerun_loss_pct` | float | `h*(1-h)`-normalised re-run tax |
| `billable_gb_per_clean_gb` | float | `1/(1-h)` traffic amplification |
| `effective_usd_per_gb` | float | `volume_price * billable_gb_per_clean_gb` |
| `cost_per_100_clean_gb_usd` | float | Cost of 100 GB of *clean* traffic |

## Method

```
survive       = 1 - hazard
rerun_loss    = hazard / survive
billable_mult = 1 / survive
effective_gbp = 100gb_price * billable_mult
```

A dropped sticky IP invalidates `cf_clearance`, so the whole multi-step flow is re-run; a rotating IP
carries a fixed challenge failure rate instead. Neither is free, and the crossover is scenario-specific.

## Summary table (3-minute checkout flow)

| Provider | Entry $/GB | 100 GB $/GB | KYC | Trial | Sticky max | Effective $/GB |
|---|---|---|---|---|---|---|
| Smartproxy (Decodo) | $4.00 | $2.75 | none | 3 days / 100 MB | 1440 | $2.93 |
| Bright Data | $8.00 | $3.50 | manual company KYC | 7 days / $2 credit | 30 | $3.72 |
| Oxylabs | $6.00 | $5.00 | mandatory KYC | $5 welcome credit | 1440 | $5.32 |
| IPRoyal | $7.00 | $5.25 | none | none | 1440 | $5.59 |
| SOAX | $5.00 | $3.00 | none | Sandbox account | 1440 | $3.19 |
| Webshare | $3.50 | $2.75 | none | 1 GB / 10 proxies free | 30 | $2.93 |
| curl_cffi + Cloudflare WARP | $0.00 | $0.00 | none | permanently free | 0 | $0.00 |

Cost of 100 GB of clean traffic in the checkout scenario: **$0.00** for the best-priced vendor versus
**$558.51** for the most expensive — banding that never appears on a per-GB price page.

## Use the calculator and mirror

- [Interactive calculator](https://proxy.mybskm.top/calculator/?utm_source=hf_dataset_proxy)
- [Benchmark site](https://proxy.mybskm.top/?utm_source=hf_dataset_proxy)
- [HuggingFace Space](https://huggingface.co/spaces/600me/residential-proxy-sticky-session-calculator)

**Deep dive**
- [Why rotating residential proxies still get 403s: sticky TTL, JA3 and ASN economics](https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html)
- [Research blog index](https://proxy.mybskm.top/blog/)


## The 4-calculator / 4-Space / 4-Dataset matrix

**Online calculators**
- [GPU cloud true TCO](https://gpu.mybskm.top/calculator/?utm_source=hf_dataset_matrix)
- [Scraping / anti-bot TCO](https://scrape.mybskm.top/calculator/?utm_source=hf_dataset_matrix)
- [Residential proxy sticky-session loss](https://proxy.mybskm.top/calculator/?utm_source=hf_dataset_matrix)
- [MoR vs US LLC breakeven](https://pay.mybskm.top/?utm_source=hf_dataset_matrix)

**HuggingFace Static Spaces**
- [gpu-cloud-h100-a100-pricing-benchmark](https://huggingface.co/spaces/600me/llm-gpu-cost-calculator)
- [web-scraping-anti-bot-api-benchmark](https://huggingface.co/spaces/600me/rag-web-scraping-cost-calculator)
- [residential-proxy-commercial-policy-matrix](https://huggingface.co/spaces/600me/residential-proxy-sticky-session-calculator)
- [global-saas-mor-vs-us-llc-fee-matrix](https://huggingface.co/spaces/600me/ai-saas-stripe-vs-mor-tax-calculator)

**HuggingFace Datasets**
- [gpu-cloud-h100-a100-pricing-benchmark](https://huggingface.co/datasets/600me/gpu-cloud-h100-a100-pricing-benchmark)
- [web-scraping-anti-bot-api-benchmark](https://huggingface.co/datasets/600me/web-scraping-anti-bot-api-benchmark)
- [residential-proxy-commercial-policy-matrix](https://huggingface.co/datasets/600me/residential-proxy-commercial-policy-matrix)  ← this dataset
- [global-saas-mor-vs-us-llc-fee-matrix](https://huggingface.co/datasets/600me/global-saas-mor-vs-us-llc-fee-matrix)


## Transparency & FTC affiliate disclosure

This dataset is published by the independent cost-research project at mybskm.top. Some outbound vendor links are affiliate links: if you open one and later buy, we may earn a commission at no extra cost to you. Commissions never change the measured numbers, the formula, or which vendor wins a scenario, and the free open-source baseline is included on purpose because it pays us nothing. Every price is a vendor-published list rate captured on the `observed_at` date; prices, trials, KYC rules and refund terms change without notice. Nothing here is a quote, a guarantee of eligibility, tax or legal advice, or a promise of results. Verify current pricing and terms with the vendor before purchasing.
