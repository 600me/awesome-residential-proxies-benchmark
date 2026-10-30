# 夜间 `dd-lan` 事件 2：已上线 51 个 CPS 资产全量存活、SEO `noindex` 排雷与搜索引擎收录摸底报告
- **启动时间**: `2026-10-29T15:53:33.355033+00:00`
- **完成时间**: `2026-10-29T15:54:01.056261+00:00`
- **检测资产总数**: **57 个**（5 白帽站 + 5 深度 Blog + 4 PyPI 官方包 + 2 HF 资产 + 10 Dev.to 文章 + 25 GitHub 仓）
- **HTTP 200 存活率**: **56 / 57**
- **发现致命 `noindex` 标签数**: **2**（0 为最佳）
- **已捕获外部搜索引擎（Bing）收录信号数**: **57 / 57**

## 一、全部 51 个线上资产逐项体检明细
| 类别 | 资产名称 | HTTP | 耗时(ms) | `noindex` | 页面内转化/互链数 | 搜索收录信号 | URL |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `devto` | `devto:049-proxy-illusion` | 200 | 2497 | Clean | 7 | YES | https://dev.to/600me/the-049-proxy-illusion-how-a-200-line-cli-exposes-real-scraping-costs-5008 |
| `devto` | `devto:403-tax` | 200 | 1896 | Clean | 5 | YES | https://dev.to/600me/the-403-tax-what-anti-bot-protection-really-does-to-your-scraping-bill-50g7 |
| `devto` | `devto:5-mor-illusion` | 200 | 3234 | Clean | 13 | YES | https://dev.to/600me/the-5-mor-illusion-exact-us-llc-stripe-breakeven-for-non-us-saas-founders-2026-1h2l |
| `devto` | `devto:firstbase-vs-atlas` | 200 | 1787 | Clean | 12 | YES | https://dev.to/600me/firstbase-vs-stripe-atlas-vs-doola-2026-true-3-year-us-llc-registered-agent-irs-form-5472-3fcd |
| `devto` | `devto:h100-rental-trap` | 200 | 1771 | Clean | 6 | YES | https://dev.to/600me/the-h100-rental-trap-why-213-per-gpu-hour-is-not-the-price-you-pay-do7 |
| `devto` | `devto:heygen-vs-synthesia` | 200 | 1522 | WARN_NOINDEX | 14 | YES | https://dev.to/600me/heygen-vs-synthesia-elevenlabs-in-2026-ai-video-avatar-dubbing-localization-unit-economics-1gb |
| `devto` | `devto:morelogin-vs-adspower` | 200 | 2601 | WARN_NOINDEX | 22 | YES | https://dev.to/600me/morelogin-cloud-phone-vs-adspower-packetstream-1gb-residential-proxy-stack-100-account-matrix-i5b |
| `devto` | `devto:runpod-vs-vastai` | 200 | 5518 | Clean | 7 | YES | https://dev.to/600me/runpod-vs-vastai-2026-real-h100-a100-effective-cost-after-cold-start-nvme-storage--1ei1 |
| `devto` | `devto:smartproxy-vs-scraperapi` | 200 | 2116 | Clean | 13 | YES | https://dev.to/600me/smartproxy-decodo-vs-scraperapi-2026-raw-residential-proxy-pool-vs-managed-anti-bot-unblocker-5402 |
| `devto` | `devto:sticky-session-ttl` | 200 | 1630 | Clean | 11 | YES | https://dev.to/600me/why-rotating-residential-proxies-still-get-403s-sticky-session-ttl-ja3-fingerprints-and-asn-4g3n |
| `github_main` | `600me/awesome-residential-proxies-benchmark` | 200 | 4109 | Clean | 80 | YES | https://github.com/600me/awesome-residential-proxies-benchmark |
| `github_main` | `600me/check-proxy-tax` | 200 | 2686 | Clean | 22 | YES | https://github.com/600me/check-proxy-tax |
| `github_main` | `600me/decodo-smartproxy-pricing-coupons` | 200 | 2513 | Clean | 8 | YES | https://github.com/600me/decodo-smartproxy-pricing-coupons |
| `github_main` | `600me/firstbase-promo-code-pricing` | 200 | 2512 | Clean | 8 | YES | https://github.com/600me/firstbase-promo-code-pricing |
| `github_main` | `600me/runpod-gpu-pricing-coupons` | 200 | 2473 | Clean | 8 | YES | https://github.com/600me/runpod-gpu-pricing-coupons |
| `github_main` | `600me/scraperapi-pricing-coupons` | 200 | 2388 | Clean | 8 | YES | https://github.com/600me/scraperapi-pricing-coupons |
| `github_main` | `600me/vastai-gpu-pricing-coupons` | 200 | 2703 | Clean | 8 | YES | https://github.com/600me/vastai-gpu-pricing-coupons |
| `github_matrix` | `constantconv/doola-pricing-vs-firstbase` | 200 | 2609 | Clean | 8 | YES | https://github.com/constantconv/doola-pricing-vs-firstbase |
| `github_matrix` | `constantconv/firstbase-coupon-code-pricing` | 200 | 2505 | Clean | 8 | YES | https://github.com/constantconv/firstbase-coupon-code-pricing |
| `github_matrix` | `constantconv/non-us-founder-llc-annual-cost` | 200 | 2520 | Clean | 8 | YES | https://github.com/constantconv/non-us-founder-llc-annual-cost |
| `github_matrix` | `constantconv/stripe-atlas-vs-firstbase-costs` | 200 | 2233 | Clean | 8 | YES | https://github.com/constantconv/stripe-atlas-vs-firstbase-costs |
| `github_matrix` | `dnoddieva/aws-p5-vs-vastai-h100-pricing` | 200 | 6917 | Clean | 8 | YES | https://github.com/dnoddieva/aws-p5-vs-vastai-h100-pricing |
| `github_matrix` | `dnoddieva/runpod-vs-vastai-gpu-rental-costs` | 200 | 2370 | Clean | 8 | YES | https://github.com/dnoddieva/runpod-vs-vastai-gpu-rental-costs |
| `github_matrix` | `dnoddieva/spot-instance-gpu-training-budget` | 200 | 2114 | Clean | 8 | YES | https://github.com/dnoddieva/spot-instance-gpu-training-budget |
| `github_matrix` | `dnoddieva/vastai-promo-code-credit-guide` | 200 | 2125 | Clean | 8 | YES | https://github.com/dnoddieva/vastai-promo-code-credit-guide |
| `github_matrix` | `mistyparticle/brightdata-vs-webshare-pricing` | 200 | 2187 | Clean | 8 | YES | https://github.com/mistyparticle/brightdata-vs-webshare-pricing |
| `github_matrix` | `mistyparticle/rotating-residential-proxy-bandwidth-calculator` | 200 | 2595 | Clean | 8 | YES | https://github.com/mistyparticle/rotating-residential-proxy-bandwidth-calculator |
| `github_matrix` | `mistyparticle/smartproxy-vs-webshare-cost-comparison` | 200 | 3006 | Clean | 8 | YES | https://github.com/mistyparticle/smartproxy-vs-webshare-cost-comparison |
| `github_matrix` | `mistyparticle/webshare-coupon-code-pricing-guide` | 200 | 3945 | Clean | 8 | YES | https://github.com/mistyparticle/webshare-coupon-code-pricing-guide |
| `github_matrix` | `pierrewheffert/lambda-labs-vs-runpod-h100-costs` | 200 | 2238 | Clean | 8 | YES | https://github.com/pierrewheffert/lambda-labs-vs-runpod-h100-costs |
| `github_matrix` | `pierrewheffert/llm-inference-gpu-hourly-calculator` | 200 | 2224 | Clean | 8 | YES | https://github.com/pierrewheffert/llm-inference-gpu-hourly-calculator |
| `github_matrix` | `pierrewheffert/runpod-coupon-pricing-guide` | 200 | 3251 | Clean | 8 | YES | https://github.com/pierrewheffert/runpod-coupon-pricing-guide |
| `github_matrix` | `pierrewheffert/vastai-vs-runpod-serverless-pricing` | 200 | 2283 | Clean | 8 | YES | https://github.com/pierrewheffert/vastai-vs-runpod-serverless-pricing |
| `github_matrix` | `unfitjewell/scraperapi-coupon-code-breakdown` | 200 | 2366 | Clean | 8 | YES | https://github.com/unfitjewell/scraperapi-coupon-code-breakdown |
| `github_matrix` | `unfitjewell/scrapingbee-vs-scraperapi-pricing` | 200 | 2420 | Clean | 8 | YES | https://github.com/unfitjewell/scrapingbee-vs-scraperapi-pricing |
| `github_matrix` | `unfitjewell/web-scraping-api-cost-comparison` | 200 | 5219 | Clean | 8 | YES | https://github.com/unfitjewell/web-scraping-api-cost-comparison |
| `github_matrix` | `unfitjewell/zenrows-vs-scraperapi-pricing` | 200 | 3539 | Clean | 8 | YES | https://github.com/unfitjewell/zenrows-vs-scraperapi-pricing |
| `github_matrix` | `vainship/brightdata-pricing-vs-decodo` | 200 | 2372 | Clean | 8 | YES | https://github.com/vainship/brightdata-pricing-vs-decodo |
| `github_matrix` | `vainship/decodo-coupon-pricing-breakdown` | 200 | 2549 | Clean | 8 | YES | https://github.com/vainship/decodo-coupon-pricing-breakdown |
| `github_matrix` | `vainship/oxylabs-pricing-vs-decodo` | 200 | 2497 | Clean | 8 | YES | https://github.com/vainship/oxylabs-pricing-vs-decodo |
| `github_matrix` | `vainship/residential-proxy-scraping-costs` | 200 | 2722 | Clean | 8 | YES | https://github.com/vainship/residential-proxy-scraping-costs |
| `huggingface` | `HF Dataset: developer-coupons-breakdown` | 200 | 2672 | Clean | 14 | YES | https://huggingface.co/datasets/600me/developer-coupons-breakdown |
| `huggingface` | `HF Space: llm-gpu-cost-calculator` | 200 | 2628 | Clean | 0 | YES | https://huggingface.co/spaces/600me/llm-gpu-cost-calculator |
| `pypi` | `ad-tracker-antidetect-tco` | 200 | 2442 | Clean | 0 | YES | https://pypi.org/project/ad-tracker-antidetect-tco/ |
| `pypi` | `check-proxy-tax` | 200 | 1532 | Clean | 0 | YES | https://pypi.org/project/check-proxy-tax/ |
| `pypi` | `llm-gpu-cost-calculator` | 200 | 2449 | Clean | 0 | YES | https://pypi.org/project/llm-gpu-cost-calculator/ |
| `pypi` | `us-llc-compliance-tco` | 200 | 2257 | Clean | 0 | YES | https://pypi.org/project/us-llc-compliance-tco/ |
| `whitehat_blog` | `blog:firstbase-vs-atlas` | 200 | 1992 | Clean | 10 | YES | https://pay.mybskm.top/blog/firstbase-vs-stripe-atlas-vs-doola.html |
| `whitehat_blog` | `blog:heygen-vs-synthesia` | 200 | 8332 | Clean | 18 | YES | https://gpu.mybskm.top/blog/heygen-vs-synthesia-elevenlabs.html |
| `whitehat_blog` | `blog:morelogin-vs-adspower` | 200 | 2974 | Clean | 25 | YES | https://proxy.mybskm.top/blog/morelogin-vs-adspower-packetstream-tco.html |
| `whitehat_blog` | `blog:runpod-vs-vastai` | 0 | 16060 | Clean | 0 | YES | https://gpu.mybskm.top/blog/runpod-vs-vastai-h100-a100.html |
| `whitehat_blog` | `blog:smartproxy-vs-scraperapi` | 200 | 15887 | Clean | 14 | YES | https://scrape.mybskm.top/blog/smartproxy-vs-scraperapi.html |
| `whitehat_site` | `esim.mybskm.top` | 200 | 12608 | Clean | 8 | YES | https://esim.mybskm.top/ |
| `whitehat_site` | `gpu.mybskm.top` | 200 | 17583 | Clean | 22 | YES | https://gpu.mybskm.top/ |
| `whitehat_site` | `pay.mybskm.top` | 200 | 1625 | Clean | 2 | YES | https://pay.mybskm.top/ |
| `whitehat_site` | `proxy.mybskm.top` | 200 | 1866 | Clean | 14 | YES | https://proxy.mybskm.top/ |
| `whitehat_site` | `scrape.mybskm.top` | 200 | 24632 | Clean | 0 | YES | https://scrape.mybskm.top/ |
