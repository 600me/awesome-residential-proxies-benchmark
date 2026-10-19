# 【刚性施工令｜无自由裁量执行工单：ABC 联合推进——Awesome PR 提交、Dev.to 第 3 篇实战发布与全矩阵中继巡检】

## 一、物理交付定义与责任划分

本工单由 Worker 无条件、无自由裁量严格按 A、B、C 三大工序逐步推进并逐项断言验收：

### 1. 【工序 A：开源 PR 外链渗透——提交 awesome-python-testing】
- **目标仓库**：[`cleder/awesome-python-testing`](https://github.com/cleder/awesome-python-testing)（默认分支为 `main`）
- **认证凭证**：读取 `~/.secrets(密钥)/github-token(GitHub全权限个人访问令牌).env` 中的 `GITHUB_TOKEN`
- **执行动作**：
  1. 调用 GitHub API（`POST /repos/cleder/awesome-python-testing/forks`）将目标仓库 Fork 到 `600me/awesome-python-testing`；
  2. 在 Fork 仓库创建新分支 `add-check-proxy-tax`；
  3. 修改 `README.md`：在 `## Tools`（约第 258 行）正下方、`CrossHair`（约第 260 行）之前，精准插入单行：
     `- [check-proxy-tax](https://github.com/600me/check-proxy-tax) - CLI that samples a URL concurrently and reports usable-response rate, latency, and effective cost per 1,000 usable requests.`
     （严格遵守字母排序，且保持文件末尾单个换行符）；
  4. 提交更改并推送至 `600me/awesome-python-testing:add-check-proxy-tax`；
  5. 调用 GitHub API（`POST /repos/cleder/awesome-python-testing/pulls`）向 upstream 的 `main` 分支提交 PR：
     - Title: `Add check-proxy-tax to Tools`
     - Body: 提取自 `/Users/a600/project-workspaces(项目工作区)/check-proxy-tax/awesome-pr-proposals/02-awesome-python-testing.md` 中的标准 PR 正文；
  6. 断言 API 返回 HTTP 201，记录 PR 链接并验证 `curl -sI <PR_URL>` 返回 HTTP 200。

### 2. 【工序 B：技术长文双重导流——Dev.to 第 3 篇硬核实战发布与站内文章页对齐】
- **文章选题**：`The $0.49 Proxy Illusion: How a 200-Line CLI Exposes Real Scraping Costs`
- **文章规格**：1,600+ 词地道英文硬核技术长文，结合 `check-proxy-tax` 命令行实测与真实反爬场景，拆解标称价格与有效千次成本的断层；
- **链接与归因配置**：
  - 开源工具：`https://github.com/600me/check-proxy-tax`
  - 研报母页：`https://scrape.mybskm.top/blog/403-tax.html`
  - 榜单主站：`https://scrape.mybskm.top/?utm_source=devto&utm_medium=article&utm_campaign=proxy_audit_cli&src=devto_cli`
  - 带参中继与 FTC 披露：
    `https://go.272738.xyz/scraperapi?utm_source=devto&utm_medium=article&utm_campaign=proxy_audit_cli&src=devto_cli` 及
    `https://go.272738.xyz/smartproxy?utm_source=devto&utm_medium=article&utm_campaign=proxy_audit_cli&src=devto_cli`；
- **站内独立页同步**：
  - 本地生成：`/Users/a600/project-workspaces(项目工作区)/kais-scraping-apis-benchmark/blog/proxy-cost-audit.html`（自包含 Dark Theme、Self-Canonical、Article JSON-LD、FTC 披露、返回主站导航）；
  - 更新主站 `index.html` 导航与 `sitemap.xml`；
  - 部署至 VPS：`us-server:/var/www/kais-scraping-benchmark/blog/proxy-cost-audit.html`（及更新的 index 与 sitemap）；
  - 验证 `curl -sI https://scrape.mybskm.top/blog/proxy-cost-audit.html` 返回 HTTP/2 200；
- **Dev.to 发布与 Canonical 绑定**：
  - 使用 Dev.to API Key 发布文章，指定 `canonical_url: https://scrape.mybskm.top/blog/proxy-cost-audit.html`；
  - 断言 API 返回 HTTP 201，记录新文章 ID 与公开 URL；
  - 更新本地及远端 `/opt/kais-proxy-sniper/published_articles.jsonl`。

### 3. 【工序 C：流量与归因全息巡检——美西 VPS Nginx 真实点击日志分析与 302 健康巡检】
- **执行动作**：
  1. 远程读取美西 VPS `/var/log/nginx/affiliate_relay.log` 与 `/var/log/nginx/access.log`；
  2. 运行本地 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/affiliate-health-check(联盟巡检).py`，确保 5 大活跃联盟中继（Smartproxy、Firstbase、RunPod、Vast.ai、ScraperAPI）全部返回 302 且下游归因参数有效；
  3. 统计全周期点击数据：总请求量、302 跳转量、按路由分布、带参（`src=`）分布、Bot 扫描过滤与真人访问溯源；
  4. 将结构化巡检结果写入 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/traffic_audit_report.json`。

### 4. 【客观验收断言（必须全部退出码为 0）】
- 编写综合验收脚本 `verify_step_abc.py`：
  - 工序 A：PR 在 GitHub 存在且状态为 `open`；
  - 工序 B：站内新研报页 HTTP 200，Dev.to 新文章 HTTP 200 且源码 canonical 严格指向站内页；
  - 工序 C：5 条 302 中继健康，流量报告成功生成且字段完备；
  - 所有涉及的 Git 仓库保持 clean 并与 `origin/main` 保持同步。
