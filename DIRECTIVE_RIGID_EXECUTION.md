# 【刚性施工令｜无自由裁量执行工单：Phase 3 扩展提审与 Phase 4 联盟审批及无人值守落地】

## 一、唯一物理目标与路径
在 `/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/` 及相关阵地下，以纯底层工兵（Worker）身份无条件完成工序 2 剩余的 Phase 3 与 Phase 4 落地，并通过全部客观指标验收：
1. **Phase 3（Chrome 扩展提审资产准备与验证）**：
   - 验证 `extension/proxy-fraud-checker.zip` 解压结构完整（包含 Manifest V3、popup.html/js/css、icons 及 STORE_LISTING.md）；
   - 验证隐私政策页面公网 HTTP 200 存活；
   - 验证商店文案符合商业三要素（读者痛点 + 算例 + 带参转化出口）。
2. **Phase 4（CPS 联盟审批收网与无人值守守护进程）**：
   - 编写并执行单文件轻量巡检脚本 `affiliate-health-check(联盟巡检).py`（纯 Python 3 标准库，无外部依赖）：
     - 校验现有已激活的 5 大中继链接（Smartproxy, Firstbase, RunPod, Vast.ai, ScraperAPI）公网 302 跳转带参正常；
     - 检查 Gmail/已获批状态，若无新获批直接毫秒级快退（退出码 0），杜绝高频空转；
   - 验收美西 VPS 线上 `proxy-sniper.service` 守护进程（运行状态、日志、自愈能力）；
3. **交接单全量落盘更新**：
   - 严格将客观事实（命令退出码、HTTP 状态码、已激活参数）回填至 `/Users/a600/handoff/task-cps-traffic-acquisition-pipeline(CPS矩阵公域截流与主动获客).md`。

---

## 二、执行硬红线（坚决杜绝过度防守与画蛇添足，违反直接判不及格）
1. **严禁防御性过度工程**：
   - 严禁擅自拆分 `seen_post_ids` 搞所谓的“待办队列数据库/中间状态层”；
   - 严禁引入 `sd_notify` 心跳协议等冗余通信机制，标准 systemd `Restart=on-failure` 即足够；
   - 严禁为每个源设计多维退避状态机，保持单源超时 10s 快速跳过的最简物理路径；
   - 严禁回头推翻已在美西 VPS 上全量上线且 HTTP 200 的四大站交互计算器代码。
2. **零等待人工假死锁（No `awaiting_human`）**：
   - 非实际扣款付费、非本人税务/实名验证的一切常规工序，一律全自动执行，严禁以“待人类审批”为由设立假死锁停滞。
3. **就地物理复用铁律**：
   - 复用现有美西 VPS（`us-server`）、现有 `go.272738.xyz` Nginx 配置、现有密码库 `ai-pass`。严禁引入 npm 构建黑洞或外部重依赖。

---

## 三、客观验收指令（必须全部退出码为 0）
1. `unzip -t extension/proxy-fraud-checker.zip`：无错误，退出码 0。
2. `curl -Is https://proxy.mybskm.top/privacy.html | grep -E "HTTP/.*200"`：返回 200 OK。
3. `python3 "affiliate-health-check(联盟巡检).py"`：成功输出 5 大已激活厂商 302 验证通过，未激活厂商快退，退出码 0。
4. `ssh us-server 'systemctl is-active proxy-sniper.service'`：返回 `active`，退出码 0。
5. 检查 `/Users/a600/handoff/task-cps-traffic-acquisition-pipeline(CPS矩阵公域截流与主动获客).md` 成功更新 Phase 3 与 Phase 4 记录。

---

## 四、交付指令
立即无条件按上述要求执行并完成验收，执行完毕后输出客观验收回执，绝不二次规划或推翻共识。
