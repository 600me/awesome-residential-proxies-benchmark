# 【刚性施工令｜无自由裁量执行工单：DeepSeek 大模型动态接入与 GitHub 主动发帖闭环】

## 一、物理目标与交付定义
- **目标**：
  1. **大模型动态答题大脑接入**：升级 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/gh-answer.py`，接入 DeepSeek API（模型 `deepseek-chat`）。当检测到有效报错 Issue（评分 ≥ 3）时，由 DeepSeek 针对具体的报错日志与提问动态生成 100% 定制的四段式硬核排障解答；若网络或 API 异常，优雅降级为既有专家静态模板（零中断死锁）；
  2. **扣动发帖扳机（--post）**：支持读取 `GITHUB_TOKEN`，增加 `--post` 参数。对通过门禁且未回帖过的公开 Issue，通过 GitHub 官方 REST API（`POST /repos/{owner}/{repo}/issues/{issue_number}/comments`）完成真实回帖，并记录回执与 URL 到 `outreach_gh.jsonl`；
  3. **凭据安全入库与 VPS 同步**：
     - 本地读取 `/Users/a600/.secrets(密钥)/github-token(GitHub发帖令牌).env` 与 `/Users/a600/.secrets(密钥)/deepseek-api(深度求索API).env`；
     - 同步至美西 VPS：`/opt/kais-proxy-sniper/github-token.env` 与 `/opt/kais-proxy-sniper/deepseek.env`（权限 `600`，属主 `proxy-sniper`）；
  4. **美西 VPS 定时巡检出击脚本**：
     - 在远端创建 `/opt/kais-proxy-sniper/run_daily_outreach.sh`，每天运行一次 `--once --post --limit 3`；
     - 在 `proxy-sniper` 用户下配置 crontab（每天固定一次，严禁高频泛滥）；
  5. **客观验收与 Git 交付**：本地与美西 VPS 执行 `--dry-run` 与 Token 核验，确认退出码全部为 0，推送远端仓库。

---

## 二、模型更新机制说明（必须写入代码与注释）
- **官方别名指针机制**：DeepSeek 官方 API 中的 `deepseek-chat` 是持久别名（Permanent Alias Pointer）。当官方升级 V3、V3.5 或后续更新时，后端会自动指向最新生产模型，无需人工更改模型编号；
- **配置覆盖兜底**：代码同时读取环境变量 `DEEPSEEK_MODEL`（默认值为 `deepseek-chat`），确保未来若需要显式锁定特定模型时单行环境变量即可生效。

---

## 三、代码实现硬红线（违反直接判不及格）
1. **纯单文件，零新增第三方库**：
   - 必须使用 Python 3 标准库（`urllib.request`, `json`, `os`, `re`, `time`, `argparse`），严禁 `pip install` 任何外部库（如 requests/openai/aiohttp）；
2. **AI 生成与降级双保险**：
   - 动态调用 `https://api.deepseek.com/chat/completions` 时，超时时间设为 6 秒；
   - 若未配置 `DEEPSEEK_API_KEY` 或 API 报错超时，无缝回退到既有专家模板，绝不阻塞流程；
3. **回帖安全防封门禁**：
   - 目标仓库 Stars ≥ 50；Issue 处于 open 状态且 14 天内有更新；
   - 排除 `600me` 自己的仓库（避免在自己项目下刷帖）；
   - 严格去重：已在 `outreach_gh.jsonl` 中标记为 `posted: true` 的 Issue 绝对不二次发送；
   - 单次运行发帖上限不得超过 `--limit`（默认 2，最大 5），每次发帖之间随机休眠 3~7 秒；
4. **账本记录完备性**：
   - 发帖成功后，在 `outreach_gh.jsonl` 中记录 `posted: true`, `comment_url: <url>`, `comment_id: <id>`, `post_time: <iso_time>`；
5. **--dry-run 完全离线**：
   - 运行 `--dry-run` 时保持 100% 离线测试，覆盖 4 大分类，不发起任何真实外部写操作，退出码必须为 0。

---

## 四、客观验收指令（必须全部退出码为 0）
1. 本地演练验收：
   - `python3 /Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/gh-answer.py --dry-run` 退出码必须为 0；
2. 美西 VPS 凭据与权限核验：
   - `ssh us-server 'head -c 10 /opt/kais-proxy-sniper/github-token.env && head -c 10 /opt/kais-proxy-sniper/deepseek.env'` 成功输出且退出码为 0；
3. 美西 VPS 官方 Token 权限核验：
   - `ssh us-server 'curl -s -H "Authorization: token $(grep GITHUB_TOKEN /opt/kais-proxy-sniper/github-token.env | cut -d= -f2)" https://api.github.com/user | grep -q "\"login\": \"600me\""'` 退出码必须为 0；
4. 美西 VPS 部署演练核验：
   - `ssh us-server 'python3 /opt/kais-proxy-sniper/gh-answer.py --dry-run'` 退出码必须为 0；
5. Git 状态核验：
   - 仓库 status 保持 clean，已 commit 并 push 到远端。
