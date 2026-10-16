# 【刚性施工令｜无自由裁量执行工单：Chrome Web Store 自动提审】

## 一、唯一物理目标与路径
- **目标**：在 AI Chrome 开发者控制台（`https://chrome.google.com/webstore/devconsole/`）中，全自动完成扩展 `Proxy Fraud Checker` 的上传、商店元数据录入、隐私政策披露及提交审核（Submit for Review）。
- **物理路径与资产清单（100% 就地复用，严禁缺失）**：
  1. 上架 ZIP 包：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/extension/proxy-fraud-checker.zip`
  2. 1280x800 官方规格截图：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/extension/store-assets/screenshot-1280x800.png`
  3. 文本与描述真源：`/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark/extension/store-assets/STORE_LISTING.md`
  4. 官方隐私政策公开 URL：`https://proxy.mybskm.top/privacy.html`

---

## 二、表单刚性填充规范（1:1 严格对照，严禁自行发挥）
1. **商品信息（Store Listing）**：
   - **名称（Name）**：`Proxy Fraud Checker`
   - **简短说明（Summary）**：`Check your public IP, hosting/ISP signals and reported risk. Compare residential proxies when 403s waste your crawl budget.`
   - **详细说明（Description）**：完整填入 `STORE_LISTING.md` 中从 `Crawlers or multi-account workflows...` 到 `Terms applicable to your work.` 的正文。
   - **类别（Category）**：选择 `Developer Tools`（开发者工具）。
   - **屏幕截图（Screenshots）**：上传 `screenshot-1280x800.png`。
2. **隐私权规范（Privacy Practices）**：
   - **单一用途（Single Purpose）**：`Inspect public exit IP address, ASN, hosting/ISP signals and risk indicators on demand.`
   - **权限用途说明（Host Permission Justification）**：`Required solely to request public exit IP metadata and risk indicators from https://api.ipquery.io over secure HTTPS when the user opens the extension.`
   - **隐私政策网址（Privacy Policy URL）**：`https://proxy.mybskm.top/privacy.html`
   - **认证勾选**：勾选符合 Chrome Web Store 开发者政策声明（不收集 PII、不出售数据）。
3. **提交动作**：
   - 点击“提交审核”（Submit for review）。

---

## 三、客观验收指令（必须全部通过）
1. 控制台中显示商品状态变为 `Pending Review`（审核中）或已成功加入审核队列。
2. 退出码为 0，严禁设立 awaiting_human 假死锁。

---

## 四、执行验收（2026-10-16 19:32 Asia/Shanghai）
- [x] 使用 AI Chrome（CDP 9222）已有登录，保存非交易者声明。
- [x] 新建 Proxy Fraud Checker，上传指定 ZIP；商品 ID：`ogihjffhcilpepjkpdifmkloioocoajp`。
- [x] 名称、摘要沿用软件包；详细说明与 `STORE_LISTING.md` 正文逐字比对一致；类别为开发者工具，语言为英语。
- [x] 上传现有 128px 图标及指定 1280×800 截图。
- [x] 按指定原文填写单一用途、主机权限理由和隐私政策 URL；声明不使用远程代码，勾选三项数据使用承诺。表单明确将 IP 地址归入“位置”，据实际 IP 查询行为勾选该类别，未勾选个人身份信息。
- [x] 使用既有 Gmail 连接完成 `600megd@gmail.com` 发布者联系邮箱验证。
- [x] 点击提交审核；控制台确认“已将您的扩展程序提交送审”。保留通过审核后自动发布选项。
- [x] 刷新状态页后仍显示“状态：待审核”和“该草稿尚待审核。”，Pending Review 验收脚本退出码为 0。尚未审核通过或公开发布。

控制台：[商品状态](https://chrome.google.com/webstore/devconsole/dd87ba00-2592-4529-9a27-4d0651dabe4d/ogihjffhcilpepjkpdifmkloioocoajp/edit/status)

外部页面截图：[商店待审核](extension/store-assets/chrome-store-pending-review(商店待审核).png)
