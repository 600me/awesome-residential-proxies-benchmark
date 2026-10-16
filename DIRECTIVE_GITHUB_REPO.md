# 【刚性施工令｜无自由裁量执行工单：GitHub 仓库关联与主页跳转】

## 一、唯一物理目标与路径
- **目标**：Kais 明确指出 Codex 已链接了 GitHub 仓库。请利用既有的 GitHub 连接凭据/通道，将当前项目（`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark`）推送到远端 GitHub 仓库（命名为 `awesome-residential-proxies-benchmark`），并将真实 GitHub 开源主页 URL 完整更新回官网导航与本地代码。
- **物理路径**：
  - 本地 Git 仓库：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/`
  - 官网主页：`web/index.html` 及美西服务器 `/var/www/kais-proxy-benchmark/index.html`
  - 项目主页：`README.md`

---

## 二、执行硬红线（违反直接判不及格）
1. **就地复用既有 GitHub 凭据**：
   - 检查已有的 GitHub 凭据、认证、或已链接的仓库配置，完成远端仓库的创建/关联与 `git push -u origin main`。
   - 严禁要求 Kais 输入账号密码。
2. **闭环更新跳转链接**：
   - 成功推送到 GitHub 后，获取真实的仓库地址（例如 `https://github.com/<owner>/awesome-residential-proxies-benchmark`）。
   - 将 `web/index.html` 右上角导航按钮恢复为 `<a href="<真实GitHub仓库地址>" target="_blank" rel="noopener noreferrer" class="nav-btn">GitHub Repo ↗</a>`。
   - 同步通过 rsync 更新到美西服务器 `/var/www/kais-proxy-benchmark/index.html`。
3. **零等待人工假死锁**：
   - 只要客观指标（Git 远端存在、push 成功、curl 校验通过）满足，直接完成，严禁输出 `awaiting_human`。

---

## 三、客观验收指令（必须全部通过）
1. `git remote -v`：必须输出已关联的有效 GitHub origin。
2. `git status`：本地与远端分支保持同步，clean。
3. 远端检查：`curl -Is <真实GitHub仓库地址> | head -n 5`，确认仓库已公开可访问。
4. 官网检查：`curl -s https://proxy.mybskm.top | grep "GitHub Repo"`，确认按钮已指向真实 GitHub 仓库。

---

## 四、交付动作
- 执行上述全部动作与客观验收命令，退出码全部为 0 后结束。
