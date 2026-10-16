# 【刚性施工令｜无自由裁量执行工单：Phase 3 & Phase 4】

## 一、唯一物理目标与路径
在 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/` 内完整实现并交付 Phase 3（Chrome 极简扩展与打包）和 Phase 4（美西 VPS 意图狙击守护进程与部署配置）。

### 物理路径清单（严格收敛，严禁引入 npm 繁琐构建链或额外抽象层）：
1. **Phase 3（Chrome 极简扩展：`extension/`）**：
   - `extension/manifest.json`：Manifest V3 规范，权限仅限最小必要权限（如 `activeTab`, 访问公共 IP 查询 API）。
   - `extension/popup.html`：极简查询界面（展示当前 IP、类型 Hosting vs ISP、风险状态）。
   - `extension/popup.js`：原生纯 JS（无需构建），异步请求当前 IP 并解析类型，内嵌转化出口链接（指向 Smartproxy / Bright Data 等带参 Ref 占位符）。
   - `extension/popup.css`：现代深色/浅色极简商务科技质感样式。
   - `extension/icons/`：包含 16x16, 48x48, 128x128 像素的标准 PNG 图标（可用轻量纯 Python 脚本生成规范透明 PNG）。
   - `extension/store-assets/STORE_LISTING.md`：符合 Chrome Web Store 审核规范与商业三要素的英文上架说明（标题、简短描述、详细介绍、隐私合规声明）。
   - 打包产物：自动生成 `extension/proxy-fraud-checker.zip`（包含所有上架文件，可直接在 chrome://extensions 拖拽或上传商店）。

2. **Phase 4（美西 VPS 意图狙击守护进程：`vps-sniper/`）**：
   - `vps-sniper/sniper_daemon.py`：单文件 Python 脚本（纯标准库 `urllib`, `json`, `time`, `os`, `re`），零第三方外部依赖。
     - 支持 `--once` 和 `--dry-run` 模式：单次巡检并输出匹配到的高意图线索，退出码为 0。
     - 状态管理：单文件 `vps-sniper/state.json`，原子替换写入（`os.replace`），维护滚动 `seen_post_ids`（上限 500 条）。
     - 巡检节拍：默认 1800 秒（30分钟）加随机抖动，轻量巡检快退。
     - 容错机制：网络超时/解析失败记录日志并静默等待下一轮，绝不抛出未捕获异常退出。
   - `vps-sniper/proxy-sniper.service`：标准 systemd 配置文件（`Restart=on-failure`, `RestartSec=60`）。
   - `vps-sniper/deploy_us_server.sh`：一键部署到美西服务器（`96.9.225.9` / Tailscale `100.80.6.84`）的 Shell 脚本（使用现有 SSH / rsync，零繁琐流程）。

---

## 二、执行硬红线（违反直接判不及格）
1. **文案主权与商业常识三要素**：
   - Chrome 扩展弹窗与商店说明中，必须包含明确转化出口：“*爬虫/多账号频繁遭遇 403 阻断？推荐高纯度住宅代理（附专属优惠与基准测试）*”，直达 GitHub Benchmark 或带参链接。
   - 严禁擅自删改或弱化商业刺痛感。
2. **零构建黑洞（No Build Tools）**：
   - Chrome 扩展使用原生 Web 技术，禁止引入 webpack, vite, npm, node_modules 等重量级构建黑洞。
3. **零外部重依赖**：
   - `sniper_daemon.py` 必须使用 Python 标准库编写，在任何 Linux 环境下无需 `pip install` 即可直接通过 `python3 sniper_daemon.py` 运行。
4. **零等待人工假死锁**：
   - 所有代码必须自测通过，禁止输出 `awaiting_human`。

---

## 三、客观验收指令（必须全部通过）
1. **Phase 3 验收**：
   - 检查 `extension/manifest.json` 为合法的 JSON 且符合 Manifest V3 规范。
   - 检查 `extension/icons/icon16.png`, `icon48.png`, `icon128.png` 存在且为有效图片。
   - 检查打包文件 `extension/proxy-fraud-checker.zip` 成功生成且解压后文件完整。
2. **Phase 4 验收**：
   - `python3 -m py_compile vps-sniper/sniper_daemon.py`：语法无误，退出码为 0。
   - `python3 vps-sniper/sniper_daemon.py --dry-run`：单次模拟运行成功，输出匹配逻辑与状态更新，退出码为 0。
   - 检查 `vps-sniper/proxy-sniper.service` 与 `deploy_us_server.sh` 文件合法且具备可执行权限。

---

## 四、交付动作
- 严格按照上述规范在当前工程下创建 `extension/` 与 `vps-sniper/` 两个子目录，完成所有文件编写与打包。
- 执行全部客观验收指令，确认退出码均为 0 后结束，绝不输出“建议等待人工确认”。
