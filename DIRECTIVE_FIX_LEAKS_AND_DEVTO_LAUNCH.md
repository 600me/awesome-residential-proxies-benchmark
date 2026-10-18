# 【刚性施工令｜无自由裁量执行工单：302中继堵漏与Dev.to自动化发文引擎落地】

## 一、物理目标与交付定义
- **目标**：
  1. **【堵漏先行】开启 302 中继点击日志 + 清理 13 个 REPLACE_ME 坏链**：
     - 修改美西 VPS `/etc/nginx/sites-available/kais-proxy-links`，废除 `access_log off;`，增加独立中继日志：
       ```nginx
       log_format relay_fmt '$time_iso8601 $status $request_uri $http_referer "$http_user_agent" $remote_addr';
       access_log /var/log/nginx/affiliate_relay.log relay_fmt;
       ```
     - 彻底清理 13 个包含 `?ref=REPLACE_ME` 的死链接：未获批的厂商直链其官方首页（保留 UTM 追踪参数，去除假 ref 参数），确保老外点击绝不出现钓鱼或坏链特征；
     - 校验配置并平滑重载：`nginx -t && systemctl reload nginx`；实测触发一次请求，确保 `/var/log/nginx/affiliate_relay.log` 有真实写入。
  2. **【SEO急救】修复 `scrape.mybskm.top/robots.txt` 404**：
     - 在 `/var/www/kais-scraping-benchmark/robots.txt` 创建标准 robots 文件：
       ```
       User-agent: *
       Allow: /
       Sitemap: https://scrape.mybskm.top/sitemap.xml
       ```
     - 核验 `curl -sI https://scrape.mybskm.top/robots.txt` 必须返回 `HTTP 200`。
  3. **【开辟 P0 战线】编写单文件 `vps-sniper/devto-publisher.py`**：
     - 纯 Python 3 标准库（`urllib.request`, `json`, `os`, `argparse`, `time`, `re`），零 pip 依赖；
     - 对接 Dev.to 官方 REST API（`POST https://dev.to/api/articles`，Header `api-key`）；
     - 支持生成 2 篇核心真实数据拆解长文（分别绑定 `canonical_url: https://scrape.mybskm.top/` 和 `https://gpu.mybskm.top/`）；
     - 文末包含高价值客观结论与带 UTM 专属链接（`utm_source=devto&utm_medium=article`）；
     - 支持 `--dry-run` 离线校验生成；支持 `--post` 真实发布，发帖回执追加写入 `published_articles.jsonl`；
  4. **同步美西 VPS 与客观验收**：
     - 同步脚本至 `us-server:/opt/kais-proxy-sniper/devto-publisher.py`（chmod 755，属主 `proxy-sniper`）；
     - 执行客观指令断言，确认全部退出码为 0，git commit 与 git push。

---

## 二、代码与配置执行硬红线（违反直接判不及格）
1. **中继日志不可丢失**：
   - `access_log /var/log/nginx/affiliate_relay.log relay_fmt;` 必须生效，严禁保留 `access_log off;`；
2. **严禁在公网留下 REPLACE_ME**：
   - 检查 nginx 配置文件与静态网页，严禁再有任何可点击的 `REPLACE_ME` 字符串；
3. **零新增第三方库**：
   - `devto-publisher.py` 必须使用标准库完成 HTTP 请求与 JSON 解析；
4. **Dev.to 规范与 Canonical 绑定**：
   - 生成的每篇文章必须包含合法 frontmatter（title, published, tags, canonical_url, series）；
   - `canonical_url` 必须正确指回对应的 mybskm.top 站点，确保外站 SEO 权重 100% 反哺主站；
5. **--dry-run 100% 离线通过**：
   - 运行 `--dry-run` 时不发起外部网络写操作，输出结构化 Markdown 与文章元数据，退出码必须为 0。

---

## 三、客观验收指令（必须全部退出码为 0）
1. 302 中继日志实测：
   - `curl -s -I "https://go.272738.xyz/smartproxy"` 后，`ssh us-server 'grep -q "smartproxy" /var/log/nginx/affiliate_relay.log'` 退出码必须为 0；
2. REPLACE_ME 根治核验：
   - `ssh us-server 'grep "REPLACE_ME" /etc/nginx/sites-available/kais-proxy-links'` 必须返回空（退出码为 1）；
3. robots.txt 存活核验：
   - `curl -s -I "https://scrape.mybskm.top/robots.txt" | grep -q "200"` 退出码必须为 0；
4. 本地与远端发布器演练：
   - `python3 /Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/vps-sniper/devto-publisher.py --dry-run` 退出码必须为 0；
   - `ssh us-server 'python3 /opt/kais-proxy-sniper/devto-publisher.py --dry-run'` 退出码必须为 0；
5. Git 状态核验：
   - 仓库保持 clean，已 commit 并 push 到远端。
