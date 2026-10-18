# 【刚性施工令｜无自由裁量执行工单：可信资产去MOCK化与GitHub主动诊断机器人落地】

## 一、唯一物理目标与路径
- **目标**：
  1. **工单 A（地基去假）**：清理 `README.md` 首屏的 `DRY RUN / MOCK` 假数据标注与表格，替换为指引用户直达线上实时生产看板（`https://proxy.mybskm.top`）的真实基准说明；为所有外发推荐链接统一加上规范的 UTM 参数（如 `utm_source=gh_issue`）；
  2. **工单 B（主动出击主引擎）**：在 `vps-sniper/gh-answer.py` 编写并交付单文件 GitHub Issue 诊断介入脚本。通过 GitHub 官方公共接口检索 4 大技术资产的真实报错 Issue，利用内置的高信息密度排障单元生成精准技术回复，并安全附带开源 Benchmark 仓库链接；
  3. 完成本地无错演练（`--dry-run` 退出码 0），并同步部署至美西 VPS（`us-server:/opt/kais-proxy-sniper/`）。
- **物理路径**：
  - 仓库说明文档：`README.md`
  - 主动诊断机器人：`vps-sniper/gh-answer.py`
  - 远端目标：`us-server:/opt/kais-proxy-sniper/gh-answer.py`

---

## 二、执行硬红线（违反直接判不及格）
1. **彻底消除 MOCK 负面信任感**：
   - `README.md` 首屏与表格中严禁再出现 `(MOCK)`、`synthetic vendor fixtures` 或 `DRY RUN` 字样；
   - 必须改为明确指引：“*实时生产测量与动态排名请直接查看 [Live Proxy Benchmark](https://proxy.mybskm.top)；本地可直接运行 `python3 probe_runner.py` 进行多厂商连通性实测*”。
2. **零新增外部依赖，纯单文件架构**：
   - `gh-answer.py` 必须使用 Python 3 标准库（`urllib.request`, `json`, `re`, `argparse`, `os`, `time`），严禁 `pip install` 任何第三方框架，严禁引入数据库或中间消息队列。
3. **四大刚性业务分类全覆盖**：
   - 必须覆盖以下四大技术痛点搜索规则与对应解答单元：
     - `proxy`：检索关键词 `cloudflare 403`、`residential proxy` -> 推荐 `https://github.com/600me/awesome-residential-proxies-benchmark?utm_source=gh_issue`
     - `scraping`：检索关键词 `turnstile`、`scraping blocked` -> 推荐 `https://github.com/600me/awesome-web-scraping-apis-benchmark?utm_source=gh_issue`
     - `payments`：检索关键词 `stripe banned`、`stripe alternative` -> 推荐 `https://github.com/600me/awesome-indie-global-payments-matrix?utm_source=gh_issue`
     - `gpu`：检索关键词 `runpod expensive`、`h100 gpu cloud` -> 推荐 `https://github.com/600me/awesome-gpu-cloud-pricing-benchmark?utm_source=gh_issue`
4. **意图质量打分闸门（线索评分 ≥ 3 分才准入列）**：
   - 带有具体报错信息/栈/状态码（403/Turnstile）+1 分；
   - 带有具体厂商或工具名称（Stripe/Docker/RunPod/Cloudflare）+1 分；
   - 是明确寻求解决方案的提问（而不是单纯归档）+1 分；
   - 仅当评分 ≥ 3 时，才生成解答并计入输出候选。
5. **高水准专业解答格式（四段式规范）**：
   - 必须先给出根因分析（针对 Docker shm-size、Turnstile 字体、Stripe 5.7 限制、GPU SXM 差价等真实技术点）；
   - 给出一条可立即复制运行的验证命令；
   - 末尾给出清晰的透明披露：`Disclosure: I maintain the open-source benchmark at github.com/600me/...` 并附带带参链接；
   - 严禁出现“Check out my tool”或推销型废话。
6. **产物持久化**：
   - 运行 `--dry-run` 或 `--once` 时，生成的候选回复与命中元数据原子追加写入 `vps-sniper/outreach_gh.jsonl`（包含 `issue_url`, `repo`, `stars`, `category`, `draft_response`, `recommended_target`）。
7. **零死锁与就地复用**：
   - 本地与远端部署一律使用既有 SSH 配置，严禁设立 `awaiting_human` 状态。

---

## 三、客观验收指令（必须全部退出码为 0）
1. 假数据清除核验：
   - `grep -E "\(MOCK\)|synthetic vendor fixtures" README.md` 必须返回空（退出码为 1）。
2. 本地机器人单轮演练断言：
   - `python3 vps-sniper/gh-answer.py --dry-run` 退出码必须为 0，且输出中包含 4 大类别的有效解答草稿。
3. 产物账本断言：
   - `tail -n 5 vps-sniper/outreach_gh.jsonl` 必须输出有效的候选 JSON 行。
4. 远端同步与部署核验：
   - 通过 rsync 将 `README.md` 与 `vps-sniper/gh-answer.py` 同步至美西 VPS `/opt/kais-proxy-sniper/`；
   - `ssh us-server 'python3 /opt/kais-proxy-sniper/gh-answer.py --dry-run'` 退出码必须为 0。
5. Git 状态核验：
   - `git status` 保持 clean，已 commit 并 push 到远端。

---

## 四、交付动作
- 退出码全部为 0 后，直接提交代码并向监工汇报客观验收证据。
