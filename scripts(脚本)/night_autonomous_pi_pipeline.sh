#!/usr/bin/env bash
# Nighttime Autonomous Pi Pipeline (GLM-5.3-Flash Worker + DeepSeek-v4.1-Flash Auditor)
# Runs completely detached via nohup while Kais sleeps:
#   - Uses 0 Antigravity Gemini quota
#   - Productively consumes cc-switch-open-code-go (GLM-5.3-Flash & DeepSeek-v4.1-Flash) quota
#   - Each pi step is wrapped with perl alarm hard-timeout so it can never hang indefinitely.

set -u
WORKSPACE="/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark"
LOG_DIR="$WORKSPACE/logs"
mkdir -p "$LOG_DIR" "$WORKSPACE/npm-packages(npm官方包寄生矩阵)" "$WORKSPACE/reports(报告)" "$WORKSPACE/validation(验证)"
MAIN_LOG="$LOG_DIR/night_pi_pipeline_20261029.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$MAIN_LOG"
}

run_with_timeout() {
    local timeout_sec="$1"
    shift
    perl -e 'alarm shift; exec @ARGV' "$timeout_sec" "$@"
}

log "=== NIGHT AUTONOMOUS PI PIPELINE STARTED ==="

# ---------------------------------------------------------------------------
# STAGE 1: GLM-5.3-Flash Deep CPS Target Deconstruction & Verification
# ---------------------------------------------------------------------------
STAGE1_PROMPT_FILE="/tmp/night_stage1_glm53_prompt.txt"
cat > "$STAGE1_PROMPT_FILE" <<'EOF'
你是海外 CPS 矩阵项目的夜间情报深挖工兵（GLM-5.3-Flash）。
请读取 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/reports(报告)/night-cps-competitor-mining-result(夜间dd全网CPS同行掘金数据).json`，并结合你自己的 Python 并发探测脚本（可直接请求公网网页与 GitHub/npm/网页搜索），完成以下【刚性施工任务】：

1. 【剔除噪音并深挖 Top 10 免审/秒批高佣新 CPS 猎物】：
   - 从夜间 `dd-lan` 抓到的 90 个外部域名，以及同类的【开发者刚需耗材/工具赛道】（重点方向：① 验证码自动打码如 CapMonster Cloud / 2Captcha / Anti-Captcha / CapSolver；② 爬虫/自动化无头浏览器云如 ZenRows / ScrapingBee / Browserbase / Steel；③ AI SEO 与冷启动外贸工具如 Outrank.so / Instantly.ai / Smartlead；④ 海外开发者高客单 API/GPU/虚拟卡/量化基础设施），筛选出 **10 个拥有真实公開 Affiliate / Partner 返佣计划（优先走 PartnerStack、Rewardful、FirstPromoter、Tapfiliate、Impact 或自带秒批后台）** 的高价值 CPS 商家（必须排除我们已有的 14 个品牌：decodo, scraperapi, firstbase, vastai, runpod, elevenlabs, adspower, 9proxy, voluum, pawns, webshare, packetstream, morelogin, heygen）。
   - 必须写一个并发 Python 脚本实测这 10 个商家的官网及 Affiliate 申请页 URL，确认全部返回 HTTP 200，并提取其真实返佣比例（如 20%~30% recurring）、归因周期、使用的是哪家联盟追踪系统（如 Rewardful/FirstPromoter/自建）、以及最适合在 npm/PyPI/GitHub 截流的高意向关键词（如 `2captcha pricing calculator`、`capmonster coupon code`）。

2. 【落盘完整的结构化报告与 JSON 数据】：
   - 将实测核验通过的 Top 10 新 CPS 猎物写入：
     `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/reports(报告)/night-glm53-top10-new-cps-targets(夜间GLM5.3深挖Top10新CPS猎物报告).md`
   - 同时将对应的机器可读 JSON（含 `merchant_name`, `domain`, `affiliate_signup_url`, `http_status`, `commission_rate`, `affiliate_network`, `approval_type`, `parasite_keywords`）写入：
     `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/reports(报告)/night-glm53-top10-new-cps-targets(夜间GLM5.3深挖Top10新CPS猎物数据).json`
   - 注意：严禁编造 URL，所有入选的 `affiliate_signup_url` 必须经你现场运行 Python 脚本实测 HTTP 200！请将网络探测合并进 1~2 个并发 Python 脚本中高效执行。
EOF

log "[Stage 1] Launching GLM-5.3-Flash for Top 10 New CPS Target Deep-Dive..."
cd "$WORKSPACE"
run_with_timeout 900 /usr/local/bin/pi --provider cc-switch-open-code-go --model glm-5.3-flash --tools read,write,edit,bash -p "$(cat "$STAGE1_PROMPT_FILE")" >> "$MAIN_LOG" 2>&1
log "[Stage 1] Finished with exit code $?"

# ---------------------------------------------------------------------------
# STAGE 2: GLM-5.3-Flash Pre-Production of 4 Official npmjs.com Packages (14 Brands)
# ---------------------------------------------------------------------------
STAGE2_PROMPT_FILE="/tmp/night_stage2_glm53_npm_prompt.txt"
cat > "$STAGE2_PROMPT_FILE" <<'EOF'
你是海外 CPS 矩阵项目的夜间工程预生产工兵（GLM-5.3-Flash）。
请参考 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/pypi-packages(PyPI官方包寄生矩阵)/` 下已发布的 4 个 Python 官方包的高转化文案结构与 14 大品牌价格数据，在 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/npm-packages(npm官方包寄生矩阵)/` 目录下完整预生产 4 个零依赖、可直接发布到 `npmjs.com` 的 Node.js CLI & SDK 官方包：

1. 【4 个 npm 包目录与包名规范】：
   - 包 1：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/npm-packages(npm官方包寄生矩阵)/proxy-tax-calculator/`
     - `package.json` `name`: `"proxy-tax-calculator"`, `version`: `"1.0.0"`
     - 覆盖品牌：Decodo (`https://go.272738.xyz/smartproxy`), ScraperAPI (`https://go.272738.xyz/scraperapi`), Webshare (`https://go.272738.xyz/webshare`), 9Proxy (`https://go.272738.xyz/9proxy`), PacketStream (`https://go.272738.xyz/packetstream`), Pawns (`https://go.272738.xyz/pawns`)
   - 包 2：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/npm-packages(npm官方包寄生矩阵)/llm-gpu-cost-estimator/`
     - `package.json` `name`: `"llm-gpu-cost-estimator"`, `version`: `"1.0.0"`
     - 覆盖品牌：RunPod (`https://go.272738.xyz/runpod`), Vast.ai (`https://go.272738.xyz/vastai`), ElevenLabs (`https://go.272738.xyz/elevenlabs`), HeyGen (`https://go.272738.xyz/heygen`)
   - 包 3：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/npm-packages(npm官方包寄生矩阵)/us-llc-stripe-tco/`
     - `package.json` `name`: `"us-llc-stripe-tco"`, `version`: `"1.0.0"`
     - 覆盖品牌：Firstbase (`https://go.272738.xyz/firstbase`) vs Stripe Atlas / Doola 3年 TCO 对比
   - 包 4：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/npm-packages(npm官方包寄生矩阵)/antidetect-ad-tracker-tco/`
     - `package.json` `name`: `"antidetect-ad-tracker-tco"`, `version`: `"1.0.0"`
     - 覆盖品牌：AdsPower (`https://go.272738.xyz/adspower`), MoreLogin (`https://go.272738.xyz/morelogin`), Voluum (`https://go.272738.xyz/voluum`), PacketStream (`https://go.272738.xyz/packetstream`)

2. 【每个 npm 包必须包含的 4 个核心文件与硬指标】：
   - `package.json`：含 `name`, `version`, `description`, `main`: `"index.js"`, `bin`, `scripts`: `{"test": "node test.js"}`, `keywords`（不少于 10 个高意向商业搜索词）, `license`: `"MIT"`, `repository`, `homepage`（指向对应白帽站 `https://proxy.mybskm.top` / `https://gpu.mybskm.top` / `https://pay.mybskm.top`）。
   - `index.js` 与 `cli.js`（带 `#!/usr/bin/env node`）：真实可运行的 Node.js 2026 TCO 精算函数与命令行表格输出工具，支持 `--json` 与默认 Markdown/ASCII 对比表输出。
   - `test.js`：真实断言测试脚本，验证 `index.js` 计算结果与 `cli.js` 执行退出码为 `0`。
   - `README.md`：**必须直接复用 `pypi-packages(PyPI官方包寄生矩阵)` 中已由 Gemini 撰写的同主题高转化正文与 5 档官方套餐价格表**（仅将安装与调用示例从 `pip install` / `python` 替换为 `npx <pkg>` / `npm install <pkg>`，并额外挂上我们刚发的白帽站 Blog Canonical 链接 `https://gpu.mybskm.top/blog/heygen-vs-synthesia-elevenlabs.html` 与 `https://proxy.mybskm.top/blog/morelogin-vs-adspower-packetstream-tco.html` 以加速 Google 爬虫收录！）。
   - 每个 `README.md` 词数必须 >= 500 词，包含完整价格对比表、具体美元损失算例、至少 4 处指向 `https://go.272738.xyz/...` 的独立 CTA，且 **0 处** `"No checkout-verified code"` / `"Were paid benchmarks run"` 等劝退免责废话！

3. 【本地自测】：
   - 写完后，在全部 4 个包目录下运行 `node cli.js` 与 `npm test`，确保 100% 退出码为 0！
EOF

log "[Stage 2] Launching GLM-5.3-Flash for 4 npm Packages Pre-Production..."
run_with_timeout 900 /usr/local/bin/pi --provider cc-switch-open-code-go --model glm-5.3-flash --tools read,write,edit,bash -p "$(cat "$STAGE2_PROMPT_FILE")" >> "$MAIN_LOG" 2>&1
log "[Stage 2] Finished with exit code $?"

# ---------------------------------------------------------------------------
# STAGE 3: DeepSeek-v4.1-Flash Independent Adversarial Audit (<= 12 rounds)
# ---------------------------------------------------------------------------
STAGE3_PROMPT_FILE="/tmp/night_stage3_ds41_audit_prompt.txt"
cat > "$STAGE3_PROMPT_FILE" <<'EOF'
你是海外 CPS 矩阵项目的独立对抗实测审核官（DeepSeek-v4.1-Flash）。
【防百轮空转与极速审计硬约束】：请将所有文件检查、Node.js 脚本运行测试、词数统计、违禁词正则扫描与公网 HTTP 状态码探测合并编写为 **1~2 个并发 Python 脚本** 一次性执行完毕，严禁零碎单步敲 sed/grep/curl！本次审计总工具调用次数严格限制在 **12 轮以内**！

请对今晚 `GLM-5.3-Flash` 完成的两项产出执行 100% 全量实测验收：
1. 【审计目标 A：Top 10 新 CPS 猎物深挖报告】：
   - 检查 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/reports(报告)/night-glm53-top10-new-cps-targets(夜间GLM5.3深挖Top10新CPS猎物报告).md` 与 `.json` 是否存在且满 10 个独立新商家（不含已有 14 品牌）。
   - 用并发 Python 脚本现场请求 JSON 中全部 10 个商家的 `affiliate_signup_url`（带浏览器 User-Agent），核验实际 HTTP 状态码是否为 200。

2. 【审计目标 B：4 个 `npmjs.com` 预生产官方包】：
   - 检查 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/npm-packages(npm官方包寄生矩阵)/` 下 4 个包（`proxy-tax-calculator`, `llm-gpu-cost-estimator`, `us-llc-stripe-tco`, `antidetect-ad-tracker-tco`）。
   - 核验每个包的 `package.json`, `index.js`, `cli.js`, `test.js`, `README.md` 是否齐全。
   - 现场执行每个包的 `node cli.js` 与 `node test.js`，确认退出码全部为 0。
   - 核验每个包 `README.md` 词数 >= 500 词、含完整价格表、含 >= 4 处 `https://go.272738.xyz/` 短链 CTA、含新增白帽站 Blog Canonical 互链、且 0 处违禁自宫免责词（如 `No checkout-verified code`）。
   - 并发实测 `README.md` 中所有 `https://go.272738.xyz/...` 短链均返回 301/302 且最终落地页 HTTP 200。

3. 【落盘独立审计报告】：
   - 将完整实测结果写入：
     `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/validation(验证)/AUDIT_2026-10-30_night_npm_and_cps_targets(夜间npm包预生产与新CPS猎物独立审计).md`
   - 若全部达标，在报告末尾明确输出 `FINAL VERDICT: PASS`；若有未达标项，明确列出具体 FAIL 项。
EOF

log "[Stage 3] Launching DeepSeek-v4.1-Flash for Independent Audit (<=12 rounds)..."
run_with_timeout 600 /usr/local/bin/pi --provider cc-switch-open-code-go --model deepseek-v4.1-flash --tools read,bash -p "$(cat "$STAGE3_PROMPT_FILE")" >> "$MAIN_LOG" 2>&1
log "[Stage 3] Finished with exit code $?"

# ---------------------------------------------------------------------------
# STAGE 4: Auto-Remediation Loop if Audit did not PASS
# ---------------------------------------------------------------------------
AUDIT_FILE="$WORKSPACE/validation(验证)/AUDIT_2026-10-30_night_npm_and_cps_targets(夜间npm包预生产与新CPS猎物独立审计).md"
if [[ -f "$AUDIT_FILE" ]] && grep -qi "FAIL" "$AUDIT_FILE" && ! grep -qi "FINAL VERDICT: PASS" "$AUDIT_FILE"; then
    log "[Stage 4] Audit reported FAIL items. Launching GLM-5.3-Flash auto-remediation..."
    run_with_timeout 600 /usr/local/bin/pi --provider cc-switch-open-code-go --model glm-5.3-flash --tools read,write,edit,bash -p "请读取 $AUDIT_FILE 中指出的所有 FAIL 项，逐项修复代码、README 或新 CPS 猎物链接，并在修复后运行自测确认 100% 通过。" >> "$MAIN_LOG" 2>&1
    log "[Stage 4] Running DeepSeek-v4.1-Flash Delta Re-Audit (<=5 rounds)..."
    run_with_timeout 360 /usr/local/bin/pi --provider cc-switch-open-code-go --model deepseek-v4.1-flash --tools read,bash -p "请读取 $AUDIT_FILE 刚才的 FAIL 项，仅针对被修复项执行定点复测（Delta Check，工具调用严格限制在 5 轮以内），确认修复后将最新结论追加更新至 $AUDIT_FILE。" >> "$MAIN_LOG" 2>&1
fi

log "=== NIGHT AUTONOMOUS PI PIPELINE COMPLETED ==="
