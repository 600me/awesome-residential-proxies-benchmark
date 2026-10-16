# 【刚性施工令｜无自由裁量执行工单】

## 一、唯一物理目标与路径
- **目标**：在 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/` 内完整初始化 B2B 住宅代理与爬虫基建 CPS 开源评测仓库的核心资产（Phase 1 交付物），包括单文件异步测速探针、具备商业三要素的高转化 README.md、GitHub Actions 周更 CI 工作流及配置文件。
- **物理路径（严格限于以下 5 个文件，严禁多建任何抽象层/中间件/冗余文件）**：
  1. `probe_runner.py`：单文件异步探测与结果渲染脚本（仅依赖 `aiohttp`）。
  2. `README.md`：高权重 GitHub Benchmark 文档（附带 `<!-- BENCHMARK:START -->` 自动渲染标记）。
  3. `.github/workflows/benchmark.yml`：GitHub Actions 每周三定时测速并自动 Push 工作流。
  4. `requirements.txt`：仅声明 `aiohttp`。
  5. `config/affiliates.yaml`：各厂商测速配置模板与 Referral 占位符。

---

## 二、执行硬红线（违反直接判不及格）
1. **文案主权与商业常识三要素**：
   - 严禁将 `README.md` 简化为干瘪的 API 调试日志或单调代码文档！
   - 必须包含商业三要素：
     - 【痛点痛击】：直击开发者爬虫被 Cloudflare 403 阻断、大量垃圾机房 IP 浪费高额带宽费的真实生产损失；
     - 【金额与成本算例】：给出劣质机房代理（高损耗率）vs 高纯度住宅代理在 100GB 电商/社媒抓取下的实际有效单价算例；
     - 【对比大表与明确行动出口】：包含 Smartproxy、Bright Data、Apify、Oxylabs 的实测对比表格，保留带参链接跳转出口与独家 Promo Code 占位符。
2. **零等待人工假死锁**：
   - 所有客观代码必须立即编写完成并通过自测，严禁输出 `awaiting_human`、严禁以“等用户提供代理”为借口不完成脚本编写。
3. **最简物理路径与单文件原则**：
   - 探针逻辑全部收敛在 `probe_runner.py` 内，禁止拆分出 `models/`、`utils/`、`service/` 等过度工程模块。
4. **容错即数据原则**：
   - 单家代理连接超时（10s）、HTTP 403/503 一律捕获为该厂商的客观测试结果（标记为 `Failed / Timeout`），绝不让脚本抛出未捕获异常导致退出码非 0。

---

## 三、代码与技术实现刚性规范

### 1. `probe_runner.py` 核心要求：
- 纯 Python 3 异步架构，使用 `aiohttp`。
- 测试指标覆盖：连通成功率（Success Rate）、首包/响应延迟（Latency ms）、IP 类型检测（ISP 住宅 vs Hosting 机房，通过免费公共接口解析 ASN / Hosting 属性，限频时优雅退回）、HTTP 状态码。
- 支持 `--dry-run` 参数：在未配置真实代理账号时，直接运行直连测试与 Mock 渲染，验证表格生成逻辑，退出码必须为 0。
- 结果输出机制：运行后读取当前 `README.md`，精准定位 `<!-- BENCHMARK:START -->` 和 `<!-- BENCHMARK:END -->` 标签，将最新的 Markdown 表格与测试时间戳替换注入，原子写回文件。

### 2. `.github/workflows/benchmark.yml` 核心要求：
- 触发方式：每周三 `03:00 UTC` 定时触发 + `workflow_dispatch` 手动触发。
- 权限：`permissions: contents: write`。
- 流程：Checkout 代码 -> 安装 python 与 aiohttp -> 运行 `python probe_runner.py` -> 检查 `git diff`，若有变更则使用 `GITHUB_TOKEN` 执行 `git commit -m "chore(benchmark): weekly live test update [skip ci]"` 并 `git push`；无变化则静默退出。

---

## 四、客观验收指令（必须全部通过）
1. `python3 -m py_compile probe_runner.py`：语法检查，退出码为 0。
2. `python3 probe_runner.py --dry-run`：执行测试并成功注入 README，退出码为 0。
3. 检查 `README.md`：包含痛点、算例、对比表、`<!-- BENCHMARK:START -->` 标记且已被成功渲染填入数据。
4. 检查 `.github/workflows/benchmark.yml`：语法合法。

---

## 五、交付动作
- 严格按照上述规范在当前目录完成全部 5 个文件的编写。
- 运行客观验收命令，确认退出码全部为 0 后结束，绝不输出“建议等待人工确认”。
