# 【刚性施工令｜无自由裁量执行工单：美西 VPS 部署】

## 一、唯一物理目标与路径
- **目标**：将 `vps-sniper/` 中的意图狙击守护进程成功部署到美西闲置服务器 `us-server`（公网 `96.9.225.9` / 主机名 `super-bite`），配置为 systemd 后台常驻守护进程并立即启动生效。
- **物理路径**：
  - 部署脚本：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/deploy_us_server.sh`
  - 远端工作目录：`/opt/kais-proxy-sniper/`
  - 远端服务定义：`/etc/systemd/system/proxy-sniper.service`

---

## 二、执行硬红线（违反直接判不及格）
1. **就地复用既有连接凭据**：
   - 本机 `~/.ssh/config` 中已存在验证可用的 `Host us-server` 配置（使用既有私钥）。
   - 部署脚本必须支持优先尝试使用 `us-server` 目标别名进行连接与部署，严禁因 IP 无法直接匹配 HostKey 导致认证失败，严禁请求人工输入密码。
2. **零破坏与状态隔离**：
   - 仅传输 `sniper_daemon.py` 与 `proxy-sniper.service`，严禁覆盖远端未来产生的生产 `state.json`；
   - 严禁影响或重启美西 VPS 上的现有其他系统服务。
3. **零等待人工假死锁**：
   - 部署全流程必须全自动闭环，远端拉起服务后必须通过确定性脚本确认服务处于 active 状态，退出码 0，严禁输出 `awaiting_human`。

---

## 三、客观验收指令（必须全部通过）
1. 本地执行部署命令：`./vps-sniper/deploy_us_server.sh`，退出码必须为 0。
2. 远端服务存活核验：`ssh us-server 'systemctl is-active proxy-sniper.service'`，退出码必须为 0（输出 `active`）。
3. 远端日志核验：`ssh us-server 'journalctl -u proxy-sniper.service -n 5 --no-pager'`，确认有初始化日志输出。

---

## 四、交付动作
- 适配 `deploy_us_server.sh` 使其优先支持 `us-server` SSH 别名与既有密钥。
- 真实执行远端部署，完成上述验收断言，退出码全部为 0 后结束。

---

## 执行记录（2026-10-16 10:32 UTC）
- [x] `deploy_us_server.sh` 默认优先使用 `us-server` 别名及既有 SSH 配置，并兼容本机 rsync 2.6.9。
- [x] `./vps-sniper/deploy_us_server.sh`：退出码 0，实际部署至 `super-bite` 的 `/opt/kais-proxy-sniper/`。
- [x] `ssh us-server 'systemctl is-active proxy-sniper.service'`：退出码 0，输出 `active`。
- [x] `ssh us-server 'journalctl -u proxy-sniper.service -n 5 --no-pager'`：退出码 0，包含服务启动及首轮运行日志。
- 服务已启用开机启动，验收时 `NRestarts=0`；仅传输指定两个文件，未上传本地 `state.json`，未重启其他服务。
- 首轮生产状态已生成：检查 50 条、匹配 0 条、来源错误 1 次。Reddit 返回 HTTP 403，守护进程记录错误并按既有节拍下轮重试；该来源当前不可用，不作为抓取成功记录。
