# 【刚性施工令｜无自由裁量执行工单：PyPI 极简诊断工具 `check-proxy-tax` 编写与开源矩阵就绪】

## 一、物理交付定义与责任划分

本工单为 CPS 主动进攻矩阵核心武器【A + C 咬合】的落地上线任务，由 Worker 无条件、无自由裁量严格执行并逐项断言验收：

### 1. 【CLI 工具仓库与纯标准库实现】
- **仓库根目录**：`/Users/a600/project-workspaces(项目工作区)/check-proxy-tax`
- **核心逻辑**：单文件纯 Python 3 标准库（`urllib.request`, `concurrent.futures`, `json`, `argparse`, `time`, `statistics`），零外部依赖，秒级安装与运行。
- **命令行功能规格**：
  - `check-proxy-tax --url <URL> [--requests 20] [--marker "STRING"] [--price-per-1k 0.49] [--proxy "http://..."] [--concurrency 4] [--timeout 10] [--json]`
  - 对目标执行并发采样探测；
  - 精确判定：HTTP 200 且 body 包含指定 marker（若提供）记为可用成功（Usable Success），遇 403/429/5xx、超时或 marker 缺失记为阻断（Blocked/Failed）；
  - 核心算例：
    - `usable_pct = (usable_count / total_requests) * 100`
    - `effective_cost_per_1k = nominal_price / (usable_pct / 100)`（若 usable 为 0 则标记为 Infinite）
    - `tax_multiplier = effective_cost_per_1k / nominal_price`
    - 统计 p50 / p95 响应耗时与总传输字节数；
  - 终端输出：高质感清晰 ASCII 诊断表，末尾附带客观基准链接：
    `Benchmark & provider matrix: https://scrape.mybskm.top/?utm_source=cli&utm_content=check-proxy-tax`
  - `--json` 选项：输出纯 JSON 格式给 CI/CD 自动化流水线消费；
  - `--help` 与 README 显式包含 FTC 佣金披露：`FTC Disclosure: Benchmark links may include affiliate tracking.`；
- **标准包结构**：
  - `pyproject.toml`（配置标准 entrypoint：`check-proxy-tax = "check_proxy_tax.cli:main"`，支持 `pip install .`）
  - `LICENSE`（MIT License，Author: Kais / 600me）
  - `README.md`（地道英文，包含痛点背景 "The 403 Tax"、快速上手、参数表、CI 示例、算例解释及基准链接）

### 2. 【离线测试套件编写】
- **测试文件**：`test_cli.py`
- 采用 `unittest`，内置轻量本地 `http.server` Mock 服务测试：
  - 正常 200 且匹配 marker 测试；
  - 403 阻断与 marker 缺失测试；
  - 有效成本算例与倍数测试；
  - `--json` 格式与字段断言测试；
  - 退出码与 `--help` 测试；
- 测试断言必须 100% 通过，退出码必须为 0。

### 3. 【GitHub 独立开源仓库建立与推送】
- 利用 `~/.secrets(密钥)/github-token(GitHub全权限个人访问令牌).env` 中的 `GITHUB_TOKEN`，通过 GitHub REST API 在 `600me` 账号下创建公开仓库：
  - 仓库名：`check-proxy-tax`
  - 描述：`CLI tool to audit real proxy costs, 403 blowout multipliers, and effective price per 1,000 usable requests.`
  - 设为 Public，MIT 开源协议；
- 初始化本地 git，关联 `git@github.com:600me/check-proxy-tax.git` 或带 Token 的 HTTPS 远端，推送 `main` 分支；
- 确保 `curl -s -I "https://github.com/600me/check-proxy-tax" | grep -q "200"` 退出码为 0。

### 4. 【Awesome Lists 提交物料（Awesome PR Package）】
- 在 `awesome-pr-proposals/` 目录下生成两份高质量 PR 提案文档：
  - `01-awesome-web-scraping.md`：目标仓库为 `lorien/awesome-web-scraping`（或其他高星抓取清单），给出精确插入位置（如 Network/Proxy 类别）、PR 标题、提交说明与客观工具描述；
  - `02-awesome-python-testing.md`：目标仓库为通用 Python/测试工具清单；
- 强调“开源轻量排错工具”，严禁营销导流词，确保符合 GitHub 社区维护者审美。

### 5. 【客观验收指令（必须全部退出码为 0）】
- 编写客观验收脚本 `verify_step2_cli.py`：
  - `python3 -m unittest test_cli.py` 退出码 0；
  - `python3 -m check_proxy_tax.cli --help` 退出码 0；
  - GitHub 仓库公开访问 HTTP 200；
  - Git status 保持 clean，与 `origin/main` 保持同步。
