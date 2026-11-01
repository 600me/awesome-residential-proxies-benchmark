# PDF API Cost Calculator — Serverless HTML-to-PDF Rendering API vs Self-Hosted Headless Chromium TCO

[![npm](https://img.shields.io/npm/v/pdf-api-cost-calculator.svg)](https://www.npmjs.com/package/pdf-api-cost-calculator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/Docs-ReadTheDocs-blue.svg)](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/html-to-pdf-api-and-headless-chromium-tco/)
[![Docker Hub](https://img.shields.io/badge/Docker-600megd%2Fpdf--api--cost--calculator-blue.svg)](https://hub.docker.com/r/600megd/pdf-api-cost-calculator)
[![Gateway](https://img.shields.io/badge/Trial-Gateway-success.svg)](https://go.272738.xyz/pdf-trial)

A command-line tool and benchmarking framework to calculate the Total Cost of Ownership (TCO) of document generation architectures. Compares self-hosted Headless Chromium / Puppeteer clusters against managed document generation APIs including CraftMyPDF, APITemplate.io, DocRaptor, and Adobe PDF Services.

---

## ⚡ Quick Start

```bash
# Run directly via npx (zero installation required)
npx pdf-api-cost-calculator --docs 15000

# Install globally
npm install -g pdf-api-cost-calculator
pdf-api-cost-calculator --docs 15000
```

---

## 💸 Why Self-Hosting Puppeteer / Chromium Is an Anti-Pattern

1. **Chromium Memory Leaks**: Renders leak 80–250 MB per job. Node.js worker pools crash under high-concurrency billing cycles.
2. **Cold Starts in Lambda**: AWS Lambda 1024MB–2048MB runtimes require 3–8s cold starts; missing OS fonts cause tofu boxes.
3. **DevOps Overhead**: 12+ hours/month spent maintaining font packages, Chromium dependencies, and headless sandbox CVEs ($1,200/mo eng drag).

---

## 📊 2026 Production Unit Economics (15,000 Documents / Month)

| Solution | Rate Card Tier | Effective Cost (15k docs) | Labor & Maintenance | Total TCO |
| :--- | :--- | :--- | :--- | :--- |
| **Self-Hosted AWS Lambda/ECS** | Pay-as-you-go compute | \$185 / mo | 12 hrs (\$1,200 / mo) | **\$1,435 / mo** |
| **Adobe PDF Services API** | \$0.05 / doc | \$750 / mo | 0.5 hr (\$50 / mo) | **\$800 / mo** |
| **DocRaptor PrinceXML** | \$0.055 / doc | \$825 / mo | 0.5 hr (\$50 / mo) | **\$875 / mo** |
| **CraftMyPDF Professional** | **\$99 / mo** (12k docs included) | **\$123 / mo** | 0.5 hr (\$50 / mo) | **\$173 / mo (Save \$1,262)** |
| **APITemplate.io PDF Standard** | **\$69 / mo** (12k docs included) | **\$87 / mo** | 0.5 hr (\$50 / mo) | **\$137 / mo (Save \$1,298)** |

---

## 🔗 Cross-Platform Ecosystem & Live Benchmarks

- **Documentation**: [HTML-to-PDF API vs Headless Chromium TCO Guide](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/html-to-pdf-api-and-headless-chromium-tco/)
- **Docker Hub Container**: [600megd/pdf-api-cost-calculator](https://hub.docker.com/r/600megd/pdf-api-cost-calculator)
- **PyPI Package Index**: [pdf-api-cost-calculator on PyPI](https://pypi.org/project/pdf-api-cost-calculator/)
- **Official Gateway**: [Verify PDF API Trial & Sandbox](https://go.272738.xyz/pdf-trial)
- **CraftMyPDF Sandbox**: [50 Free Documents per Month](https://go.272738.xyz/craftmypdf)
- **APITemplate.io Portal**: [3,000 Free Credits](https://go.272738.xyz/apitemplate)
