# 战线 6 底层工兵【刚性施工令】(Worker Directive for GLM-5.3-Flash)

你是战线 6 的纯底层工兵（Worker），负责执行以下 4 项明确的工程与部署动作。请按照严格的操作步骤执行，完成后向主脑汇报每一步的客观执行结果（退出码、HTTP 状态、关键证据）。严禁二次规划，严禁推翻文案，严禁设立等待人类指令假死锁。

---

### 任务 1：提拔 `lx-server` 72h 自动发仓队列前 10 槽位为真佣金品牌

1. 通过 SSH 登录 `lx-server`，进入 `/home/kais/gt-matrix-runtime(GitHub矩阵运行器)/`。
2. 备份账本：
   ```bash
   ssh lx-server "cp /home/kais/gt-matrix-runtime\(GitHub矩阵运行器\)/account_lifecycle_ledger\(账号生命周期状态账本\).json /home/kais/gt-matrix-runtime\(GitHub矩阵运行器\)/account_lifecycle_ledger\(账号生命周期状态账本\).json.bak_track6_pre"
   ```
3. 在 `account_lifecycle_ledger(账号生命周期状态账本).json` 中，定位所有 `lifecycle_stage == 'WARMING_UP_PENDING_WASH_AND_DEPLOY'` 的账号，并按 `eligible_wash_at` 从早到晚排序：
   - 保持前 7 个待发账号不变（`traumaticproc` -> `elevenlabs`, `open-houd` -> `elevenlabs-dubbing`, `waterymalnu` -> `adspower`, `thosemedicat` -> `9proxy`, `lonegymnasti` -> `scraperapi-ecommerce`, `monita77` -> `voluum`, `peruth8room` -> `pawns`）。
   - 将紧随其后的第 8、9、10 个待发账号修改为：
     - `lou-concrak` (`2026-10-31T02:43Z`): `assigned_brand_pack` 改为 `"heygen"`
     - `paltrybehest` (`2026-10-31T07:31Z`): `assigned_brand_pack` 改为 `"morelogin"`
     - `nippybedroom` (`2026-10-31T07:31Z`): `assigned_brand_pack` 改为 `"packetstream"`
   - 将原本占位的 `brand24` 赋给 `xonne87`（原本排为 `packetstream`），将原本的 `gologin` 赋给 `famouspoem` 或 `silverfine`（末尾重复槽位）。
4. 运行 Python 脚本验证修改后的账本：
   - 确保前 10 个即将在 72h 后发射的账号其 `assigned_brand_pack` 分别为 10 个独立真佣金品牌包（`elevenlabs`, `elevenlabs-dubbing`, `adspower`, `9proxy`, `scraperapi-ecommerce`, `voluum`, `pawns`, `heygen`, `morelogin`, `packetstream`），达成 100% 锁定真佣金。
   - 确保 JSON 格式合法无语法错误，权限为 600。

---

### 任务 2：白帽门户 `proxy.mybskm.top` 14 品牌网关卡片部署与 GitHub 同步

1. 确认本地 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/web/index.html` 中的 `#infrastructure-gateways` 区域已包含全部 14 张品牌卡片（已由主脑写入，含 PacketStream、MoreLogin、HeyGen）。
2. 同步更新部署至 `us-server`：
   ```bash
   rsync -avz -e ssh /Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/web/ us-server:/var/www/kais-proxy-benchmark/
   ```
3. 将本地变更提交并推送到 GitHub 生产仓库 `600me/awesome-residential-proxies-benchmark`：
   ```bash
   cd "/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark"
   git status
   git add web/index.html README.md generate_hf_dataset.py hf-space-mirror/ hf-dataset-mirror/ coupon-parasite-pages/ vps-sniper/
   git commit -m "feat(track6): full 14-brand matrix convergence (PacketStream, MoreLogin, HeyGen) across portal, HF space, and dataset"
   git push origin main
   ```
4. 实测公开站点 `https://proxy.mybskm.top/`：
   - `curl -sL https://proxy.mybskm.top/` 验证 HTTP 200，并检查包含 `PacketStream`、`MoreLogin`、`HeyGen` 关键字且无 `Not configured` 占位符。

---

### 任务 3：升级 Hugging Face Space 与 Dataset 至 14 大品牌并部署上线

1. 运行 `generate_hf_dataset.py` 确保本地数据集已完全生成 14 品牌版：
   ```bash
   python3 "/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/generate_hf_dataset.py"
   ```
   检查 CSV 行数确为 15（1 标题 + 14 行数据）。
2. 运行 Hugging Face 生产部署脚本：
   ```bash
   python3 "/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/scripts/deploy_hf_and_gist_matrix.py"
   ```
   该脚本会将 `hf-space-mirror` 推送到 Space `600me/llm-gpu-cost-calculator`，将 `hf-dataset-mirror` 推送到 Dataset `600me/developer-coupons-breakdown`。
3. 验证线上 Hugging Face 端点：
   - Space: `https://huggingface.co/spaces/600me/llm-gpu-cost-calculator` (HTTP 200)
   - Dataset: `https://huggingface.co/datasets/600me/developer-coupons-breakdown` (HTTP 200)

---

### 任务 4：调用 Dev.to API 发布 2 篇新增高转化长文 + 验证 14 套 Gist 生产包

1. 运行 Dev.to 自动发布脚本：
   ```bash
   python3 "/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/devto_publish_track6.py" --post
   ```
   确认文章 09（HeyGen vs Synthesia）与文章 10（MoreLogin vs AdsPower）发布成功，记录返回的 Dev.to 公开 URL 和 slug。
2. 检查 `vps-sniper/published_articles.jsonl`，确认 2 篇新文章已成功追加回执，且状态为 `published`。
3. 对新发布的 2 个 Dev.to 公开 URL 进行 curl 验证，确保 HTTP 200 且页面正常展示。
4. 运行 14 套 Gist 生产包验证脚本：
   ```bash
   python3 "/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/coupon-parasite-pages(优惠码寄生截流页)/expand-gists(扩铺Gist与验收).py"
   ```
   检查 `coupon-parasite-pages(优惠码寄生截流页)/expansion-verification(扩铺与报告验收).json`，确保 14 套生产包全量覆盖、所有文档词数均 $\ge 400$（实际 $\ge 450$）、所有 Python 精算脚本执行退出码为 0。

---

完成后请输出完整的执行日志与各项客观指标（退出码、HTTP 状态、公开 URL），供独立审计官进行对抗审查！
