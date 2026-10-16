# 【刚性施工令｜无自由裁量执行工单：双域名上线与资产升级】

## 一、唯一物理目标与路径
DNS 已完成解析：
- `proxy.mybskm.top` ➔ `96.9.225.9`（美西服务器）
- `go.272738.xyz` ➔ `96.9.225.9`（美西服务器）

本工单目标：
1. 在 `us-server` 部署 `proxy.mybskm.top`（提供 Benchmark 静态展示与合规 `privacy.html`）并申请 SSL。
2. 在 `us-server` 部署 `go.272738.xyz`（提供全网防失效 301 跳转短链）并申请 SSL。
3. 将本地项目（`config/affiliates.yaml`、`README.md`、`extension/`）中的推广链接升级为 `https://go.272738.xyz/<vendor>`，隐私政策外链升级为 `https://proxy.mybskm.top/privacy.html`，并重新生成打包 ZIP。

---

## 二、执行硬红线（违反直接判不及格）
1. **平滑生效与零破坏**：
   - 严禁影响美西 VPS 现有的其他服务（如 `x1-proxy`、`taskfocus`、`emailguard` 等）。
   - Nginx 操作仅允许新增配置文件至 `/etc/nginx/sites-available/`，软链到 `sites-enabled/`，测试 `nginx -t` 通过后执行 `systemctl reload nginx`。
2. **Certbot 自动化非交互**：
   - 使用 `certbot --nginx -d <域名> --non-interactive --agree-tos -m 600megd@gmail.com --redirect` 自动签发并配置 HTTPS，严禁交互式挂起。
3. **文案三要素与合规声明**：
   - `proxy.mybskm.top/privacy.html` 必须完整渲染 `STORE_LISTING.md` 中的隐私政策条款，确保 Chrome Web Store 审核秒过。
4. **零等待人工假死锁**：
   - 远端 curl 测试与本地代码编译验证全部通过，退出码 0，严禁输出 `awaiting_human`。

---

## 三、客观验收指令（必须全部通过）
1. **远端 Nginx 配置与证书核验**：
   - `ssh us-server 'nginx -t'`：退出码必须为 0。
   - `curl -Is https://proxy.mybskm.top | grep "HTTP/"`：必须返回 `HTTP/2 200` 或 `HTTP/1.1 200`。
   - `curl -Is https://proxy.mybskm.top/privacy.html | grep "HTTP/"`：必须返回 `200`。
   - `curl -Is https://go.272738.xyz/smartproxy | grep -E "HTTP/|location:"`：必须返回 `301` 或 `302` 重定向。
2. **本地资产更新核验**：
   - `python3 -m py_compile probe_runner.py`：退出码为 0。
   - `python3 probe_runner.py --dry-run`：执行测试并成功注入 README，退出码为 0。
   - `unzip -t extension/proxy-fraud-checker.zip`：测试压缩包完整性，退出码为 0。

---

## 四、交付动作
- 编写部署脚本在 `us-server` 完成两个站点的 Nginx + SSL 配置与页面发布。
- 更新本地项目的相关链接与配置文件，执行 dry-run 与扩展重新打包。
- 执行上述全部验收指令，确认退出码均为 0 后结束。


## 执行与验收记录（2026-10-16 10:46 UTC）

- [x] 已执行 `./deploy-domains(双域名部署).sh`，退出码 0。新增 `/etc/nginx/sites-available/kais-proxy-benchmark`、`kais-proxy-links` 及对应 sites-enabled 软链；静态页面位于 `/var/www/kais-proxy-benchmark/`。
- [x] 两个域名分别通过指定的非交互 Certbot 命令完成签发；证书到期日均为 2027-01-14。复用现有 `snap.certbot.renew.timer`（active）。
- [x] `ssh us-server 'nginx -t'`：退出码 0。
- [x] `curl -Is https://proxy.mybskm.top | grep "HTTP/"`：退出码 0，HTTP/2 200。
- [x] `curl -Is https://proxy.mybskm.top/privacy.html | grep "HTTP/"`：退出码 0，HTTP/2 200。公网页面逐条比对 STORE_LISTING.md，七条原有隐私条款完整保留，并披露静态站点/短链正常连接元数据处理。
- [x] `curl -Is https://go.272738.xyz/smartproxy | grep -E "HTTP/|location:"`：退出码 0，HTTP/2 301，Location 保留原厂商目标及参数。
- [x] smartproxy、brightdata、apify、oxylabs 四条 HTTPS 短链均为 301；三个 HTTP 页面/短链入口均正确重定向至 HTTPS。
- [x] `python3 -m py_compile probe_runner.py`：退出码 0。
- [x] `python3 probe_runner.py --dry-run`：退出码 0，README 已注入真实直连结果与明确标记的厂商 MOCK 数据，静态展示已同步本轮结果。
- [x] config/affiliates.yaml、README、扩展 JS/HTML 与商店说明均升级至新域名；destination_url 保留原始跳转目标。
- [x] `unzip -t extension/proxy-fraud-checker.zip`：退出码 0，8 个文件完整；manifest.json 位于 ZIP 根目录，打包内容逐字节匹配本地源文件。
- [x] `node --check extension/popup.js`、部署脚本 Bash 语法检查：退出码 0。
- [x] 既有 Nginx 全局及其他站点配置 SHA-256 校验全部一致；nginx、kais-email-guard、us-h2-node、proxy-sniper 的进程 ID、启动时间及重启次数均未变化，服务均 active；仅执行 Nginx reload，未重启其他服务。部署临时目录已清理。
- 远端部署前备份：`/var/backups/kais-proxy-domains-20261016T104509Z/nginx-before.tar.gz`。
- 本地修改前备份：`/Users/a600/tmp(临时)/kais-proxy-domains-backup(部署前备份)-20261016T104339Z.tar.gz`。
- 事实边界：短链目标仍含未激活的 REPLACE_ME，优惠码仍为占位符；此次完成域名部署和打包，不代表联盟资格、Chrome Web Store 审核通过或收入。
