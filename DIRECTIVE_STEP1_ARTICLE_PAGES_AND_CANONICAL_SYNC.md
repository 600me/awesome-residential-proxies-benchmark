# 【刚性施工令｜无自由裁量执行工单：站内独立文章页生成、Dev.to Canonical 同步修正与归因贯通】

## 一、物理交付定义与责任划分

本工单为纯底层工程与 SEO 地基修复任务，由 Worker 无条件、无自由裁量严格执行并逐项断言验收：

### 1. 【Scraping 站内文章页生成与部署】
- **本地路径**：`/Users/a600/project-workspaces(项目工作区)/kais-scraping-apis-benchmark/blog/403-tax.html`
- **内容来源**：提取自 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/devto-publisher.py` 中 `scraping-api-403-tax` 的完整 1,600+ 字硬核拆解长文。
- **页面规范**：
  - 纯静态单文件 HTML5，严禁外部构建依赖；采用与 `scrape.mybskm.top` 一致的高质感深色主题（Dark Theme）；
  - 完整保留全部数据表格（Markdown 表格转为原生自适应 HTML `<table>`）、代码块、算例公式与避坑架构；
  - 必须包含 Self-Canonical 标签：`<link rel="canonical" href="https://scrape.mybskm.top/blog/403-tax.html" />`；
  - 必须包含完整的 Article Schema（JSON-LD，包含 headline、description、author=600me、publisher=Scraping API Benchmark、datePublished、dateModified）；
  - 包含 OpenGraph / Twitter Cards 元数据；
  - CTA 按钮直链：`https://go.272738.xyz/scraperapi?utm_source=scrape_blog&utm_medium=article&utm_campaign=403_tax&src=article_403tax` 及 `https://go.272738.xyz/smartproxy?utm_source=scrape_blog&utm_medium=article&utm_campaign=403_tax&src=article_403tax`；
  - 显式标注 FTC 合规佣金披露（Affiliate Disclosure）；
  - 顶部/底部提供返回主看板链接：`[← Back to Live Scraping API Benchmark]`；
  - 在 `kais-scraping-apis-benchmark/index.html` 顶部增加醒目研报入口导航；
  - 在 `kais-scraping-apis-benchmark/sitemap.xml` 中追加该文章 URL；
  - 部署至美西 VPS：`us-server:/var/www/kais-scraping-benchmark/blog/403-tax.html`（并同步更新后的 `index.html` 与 `sitemap.xml`）。

### 2. 【GPU 站内文章页生成与部署】
- **本地路径**：`/Users/a600/project-workspaces(项目工作区)/kais-gpu-cloud-benchmark/blog/h100-rental-trap.html`
- **内容来源**：提取自 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/devto-publisher.py` 中 `h100-rental-trap` 的完整 1,600+ 字硬核拆解长文。
- **页面规范**：
  - 纯静态单文件 HTML5，采用与 `gpu.mybskm.top` 一致的高质感深色主题；
  - 完整保留所有显卡价格对比表、存储计费陷阱算例、NVLink 拓扑解析与断言；
  - 必须包含 Self-Canonical 标签：`<link rel="canonical" href="https://gpu.mybskm.top/blog/h100-rental-trap.html" />`；
  - 必须包含完整的 Article Schema（JSON-LD）；
  - CTA 按钮直链：`https://go.272738.xyz/runpod?utm_source=gpu_blog&utm_medium=article&utm_campaign=h100_trap&src=article_h100trap` 及 `https://go.272738.xyz/vastai?utm_source=gpu_blog&utm_medium=article&utm_campaign=h100_trap&src=article_h100trap`；
  - 显式标注 FTC 合规佣金披露；
  - 顶部/底部提供返回主看板及返回 `/calculator/` 链接；
  - 在 `kais-gpu-cloud-benchmark/index.html` 顶部增加醒目研报入口导航；
  - 在 `kais-gpu-cloud-benchmark/sitemap.xml` 中追加该文章 URL；
  - 部署至美西 VPS：`us-server:/var/www/kais-gpu-benchmark/blog/h100-rental-trap.html`（并同步更新后的 `index.html` 与 `sitemap.xml`）。

### 3. 【Dev.to 线上文章 Canonical 同步修正】
- 使用 Dev.to API Key（`dYpM4MXJTcvZxGhnus6ADsrU`），向 `PUT https://dev.to/api/articles/{id}` 发起更新请求：
  - 文章 1（ID 4872430）：设置 `canonical_url` = `https://scrape.mybskm.top/blog/403-tax.html`
  - 文章 2（ID 4872432）：设置 `canonical_url` = `https://gpu.mybskm.top/blog/h100-rental-trap.html`
- 断言 API 返回 HTTP 200，且返回数据中的 `canonical_url` 严格匹配新文章链接；
- 同步更新本地及远程 `/opt/kais-proxy-sniper/published_articles.jsonl`，确保账本幂等一致。

### 4. 【中继打通与客观断言验收】
- 编写并执行自动化测试脚本 `test_groundwork_verification.py`，必须覆盖：
  - 线上文章页 HTTP/2 200 验证；
  - 线上文章页 `<link rel="canonical">` 自身严格匹配断言；
  - 线上文章页 Schema Article JSON-LD 解析有效性断言；
  - Dev.to 公开网页源代码中的 `rel="canonical"` 指向站内文章页断言；
  - 中继带参 302 验证与 `/var/log/nginx/affiliate_relay.log` 日志落地验证；
- 全套测试退出码必须为 0，Git 提交并推送至对应远端仓库。
