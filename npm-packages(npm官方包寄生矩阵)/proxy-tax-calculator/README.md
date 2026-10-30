# proxy-tax-calculator

**Calculate the real 2026 proxy bandwidth "hidden tax": effective $/GB across Decodo, ScraperAPI, Webshare, 9Proxy, PacketStream and Pawns — with overage cliffs exposed.**

[![npm version](https://badge.fury.io/js/proxy-tax-calculator.svg)](https://www.npmjs.com/package/proxy-tax-calculator)
[![Node.js](https://img.shields.io/badge/node-%3E%3D14-brightgreen.svg)](https://nodejs.org/)
[![Zero dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#install)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Web scraping, SERP monitoring, e-commerce price tracking and sneaker automation teams all pay proxy invoices quoted in "plan price" terms — never in effective **dollars per gigabyte actually squeezed through the tunnel**. Vendors hide three money incinerators inside their pricing ladders:

1. **The Overage Cliff**: A plan bought for 8 GB/month bills every extra gigabyte at the *base-tier* unit rate, which can be 5–25x the effective rate of the next plan up. 9 GB on the wrong plan is routinely 3x the cost of 10 GB on the right one.
2. **Per-Credit API Taxation**: SERP- and Unblock-oriented APIs bill in credits, not GB — a single JS-rendered page can burn 10+. Converting credits to real bandwidth shows effective rates far above raw residential GB prices.
3. **IP vs. Traffic Billing Confusion**: IP-count-based networks (9Proxy, Webshare) and by-the-GB networks (Decodo, Pawns, PacketStream) are not comparable on sticker price. Only consistent $/GB math (with IP allocation treated as included traffic) makes them comparable.

`proxy-tax-calculator` is an open-source, zero-dependency Node.js CLI that computes exact, itemized bandwidth TCO across six verified 2026 proxy networks — in one command.

Full written breakdown and methodology live at the companion guide: **https://proxy.mybskm.top** (in-depth comparison post: https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html (and https://proxy.mybskm.top/blog/morelogin-vs-adspower-packetstream-tco.html)).

---

## Real-World Loss Scenarios

### Scenario A: The 9 GB Over Cliff
- **Workload**: SERP + e-commerce crawler, mixed sources, 50 GB/month target, current month lands at 45 GB.
- **Wrong-tier Decodo (Regular, $160/8GB)**: 37 overage GB @ $20.00/GB = **$900.00 overage** → $1,060/month total.
- **Right-tier Decodo (Scale, $300/20GB)**: 25 overage GB @ $15.00/GB = **$375 overage** → $675/month total.
- **Monthly Cash Burn from Wrong Tier Alone**: **$385.00** — $4,620/year on one crawler.

### Scenario B: Lucky Duck / Pawns vs. PacketStream Pay-As-You-Go
- **Workload**: Spiky data jobs averaging 55 GB/month with heavy month-to-month variance (30–90 GB).
- **PacketStream PAYG @ $1/GB**: $55 average/month, zero overage cliffs, zero waste on unused quota.
- **Fixed-quota plan at ~$0.64/GB (100 GB tier)**: $56 base + variance spikes at $0.56 — competitive *only* at ≥100 GB steady usage. Below that, cliffs tax every light month.

---

## 2026 Proxy Network Matrix (5-Tier Comparison)

Below is the verified price and capacity ladder across premier residential, datacenter and unblock APIs (2026 published tiers; IP-based billing converted to included traffic for consistency). Onboard via the verified gateway links:

| Provider | Billing Model | Tier 1 | Tier 2 | Tier 3 | Tier 4 / Enterprise | Verified Gateway |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Decodo** (ex-Smartproxy) | GB-based residential | Starter $75/mo (2GB) | Regular $160/mo (8GB) | Scale $300/mo (20GB) | Enterprise $1,150/mo (100GB) | [Access Decodo Gateways](https://go.272738.xyz/smartproxy?src=npm_protax) |
| **ScraperAPI** | Credit-based unblock API | Hobby $49/mo (10k cach) | Standard $99/mo (100k) | Pro $249/mo (1M) | Enterprise $1,500/mo (10M) | [Access ScraperAPI Gateways](https://go.272738.xyz/scraperapi?src=npm_protax) |
| **Webshare** | IP count + datacenter allowance | Startup $2.99/mo (100 IP / 250GB) | Professional $15/mo (1k IP / 1TB) | Enterprise $45/mo (3TB) | Residential PAYG $5.99/GB | [Access Webshare Gateways](https://go.272738.xyz/webshare?src=npm_protax) |
| **9Proxy** | Clean-non-expiring residential IPs | $20 (100 IP / 10GB) | $75 (500 IP / 50GB) | $110 (1000 IP / 100GB) | $400 (5000 IP / 500GB) | [Access 9Proxy Gateways](https://go.272738.xyz/9proxy?src=npm_protax) |
| **PacketStream** | Pure pay-as-you-go GB | $10 (10GB) | $50 (50GB) | $200 (200GB) | Bulk $495 (500GB) | [Access PacketStream Gateways](https://go.272738.xyz/packetstream?src=npm_protax) |
| **Pawns.app** | GB-based residential | Starter $3.80 (5GB, $0.76/GB) | Growth $16 (25GB, $0.64/GB) | Scale $56 (100GB, $0.56/GB) | Enterprise $250 (500GB, $0.50/GB) | [Access Pawns Gateways](https://go.272738.xyz/pawns?src=npm_protax) |

Full indexed price audit: **https://proxy.mybskm.top**

---

## Installation

Zero npm dependencies. Pure Node.js (>=14) standard library.

```bash
npm install proxy-tax-calculator
```

Or run instantly without installing:

```bash
npx proxy-tax-calculator --gb 50
```

---

## CLI Usage & Worked Examples

### 1. Monthly Bandwidth TCO Comparison (50 GB/month)

```bash
npx proxy-tax-calculator --gb 50
```

Output:

```text
proxy-tax-calculator 1.0.0 - 2026 Proxy Bandwidth TCO Matrix
Planned traffic: 50 GB / month

------------------------------------------------------------
NETWORK       | PLAN         | BASE/ MO     | OVERAGE      | TOTAL/ MO    | $/ GB
------------------------------------------------------------
decodo        | Scale        | $300.00      | $450.00      | $750.00      | $15.000
scraperapi    | Standard     | $99.00       | $0.00        | $99.00       | $1.980
webshare      | Startup (100…| $2.99        | $0.00        | $2.99        | $0.060
9proxy        | 500 Resident…| $75.00       | $0.00        | $75.00       | $1.500
packetstream  | Pay-As-You…  | $10.00       | $40.00       | $50.00       | $1.000
pawns         | Growth 25GB  | $16.00       | $16.00       | $32.00       | $0.640
------------------------------------------------------------

Cheapest effective route: webshare (Startup (100 DC proxies)) at $0.060/GB -> $2.99/month
```

### 2. Machine-Readable JSON Output (`--json`)

```bash
npx proxy-tax-calculator --gb 120 --json
```

```json
{
  "tool": "proxy-tax-calculator",
  "version": "1.0.0",
  "planned_traffic_gb": 120,
  "results": [
    {
      "provider": "pawns",
      "plan": "Growth 25GB",
      "baseUsd": 16.0,
      "overageUsd": 12.8,
      "totalUsd": 28.8,
      "effectiveUsdPerGb": 0.24,
      "gateway": "https://go.272738.xyz/pawns?src=npm_protax"
    }
  ],
  "gateways": {
    "decodo": "https://go.272738.xyz/smartproxy?src=npm_protax",
    "scraperapi": "https://go.272738.xyz/scraperapi?src=npm_protax",
    "webshare": "https://go.272738.xyz/webshare?src=npm_protax",
    "9proxy": "https://go.272738.xyz/9proxy?src=npm_protax",
    "packetstream": "https://go.272738.xyz/packetstream?src=npm_protax",
    "pawns": "https://go.272738.xyz/pawns?src=npm_protax"
  }
}
```

### 3. SDK Use (programmatic)

```js
const { cheapest, compareAll } = require("proxy-tax-calculator");
const best = cheapest(120);
console.log(best.provider, best.totalUsd, best.effectiveUsdPerGb);
const all = compareAll(120);
all.forEach((r) => console.log(r.provider, r.effectiveUsdPerGb));
```

---

## Options Reference

```text
Usage: proxy-tax-calculator [--gb <number>] [--json] [--compare]

  --gb <n>     planned monthly traffic in gigabytes (default: 50)
  --json       emit pure JSON payload for CI/CD cost monitoring
  --compare    force the full comparison matrix printout
  -h, --help   show this help and exit
```

---

## Why Cost Per GB Beats Sticker Price

Every procurement decision in this space should reduce to effective $/GB *at your real traffic curve* — not the headline tier. A $5/GB PAYG network can beat a "$0.5/GB" plan whenever your usage unpredictably dips below quota; a $0.24/GB API credit plan can beat a $0.04/GB raw-residential plan whenever you need anti-block unblocks on one expensive domain. This tool makes both directions explicit, six networks deep.

Compare the full stack and start with the gateway that matches your workload:

1. Run the matrix above, pick your traffic number.
2. Open the verified gateways: [Decodo](https://go.272738.xyz/smartproxy?src=npm_protax) / [ScraperAPI](https://go.272738.xyz/scraperapi?src=npm_protax) / [Webshare](https://go.272738.xyz/webshare?src=npm_protax) / [9Proxy](https://go.272738.xyz/9proxy?src=npm_protax).
3. For light-to-mid spiky loaders, [PacketStream](https://go.272738.xyz/packetstream?src=npm_protax) and [Pawns](https://go.272738.xyz/pawns?src=npm_protax) land lowest effective $/GB.

---

## License

MIT License. Copyright (c) 2026 Proxy FinOps Benchmark Contributors.


---

## 🌐 Official Documentation, Docker Image & Web Calculators

* **Official Technical Manual (Read the Docs, DA 92)**: [residential-proxy-and-scraping-tax-benchmark](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/residential-proxy-and-scraping-tax-benchmark/)
* **Production Docker Container (Docker Hub, DA 93)**: [600megd/proxy-tax-calculator](https://hub.docker.com/r/600megd/proxy-tax-calculator)
* **Interactive Live Calculator**: [Web Benchmark & TCO Estimator](https://proxy.mybskm.top/)
* **Interactive Documentation Portal**: [Proxy & Infrastructure Docs](https://proxy.mybskm.top/docs/)
