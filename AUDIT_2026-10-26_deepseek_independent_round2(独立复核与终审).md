# 第二轮独立复核与终审（DeepSeek v4.1）

复核时间：2026-10-26。方法：不采信工兵自述，全部条目由审计方重新跑命令、重新发 HTTP 请求、并自建破坏性变异测试验证护栏是否真咬。

## 0. 终审结论（一句话）

**内容层 P0 已解除，执行层 P0 未解除。** 同意放行「整改后的拆解报告 + NodeSeek 稿」作为高质量合规资产；**不同意**放行 Reddit 回复包进入执行（无账号、无版规、无节奏），X 草案维持 FAIL（UTM 与披露未整改）。

| 轨道 | 上轮 | 本轮终审 | 依据 |
|---|---|---|---|
| 一：拆解报告 | WARN | **PASS（内部研究资产）** | 3 处笔误已改且经活体复核；双联盟跳转已独立验证 200 |
| 二：Reddit 12 条靶标 | FAIL | **内容 PASS / 执行 BLOCK** | 供应商子版与商业 UTM 全清；但无 Reddit 身份、无版规与节奏字段 |
| 三：NodeSeek 稿 | WARN | **PASS（条件：发布前核账号等级）** | 节点指引 + 透明披露齐备，链接全部 200 |
| 四：X 12 条草案 | WARN | **FAIL（未整改）** | 11/12 仍带 `utm_source=x_hijack_reply`，0/12 含联盟披露 |
| 整包 | 不得作为触达包 | **维持** | `full_task_satisfied=false` 状态正确，不得以 exit 0 冒充达成 |

## 1. 审计方独立复现的事实（不是听来的）

| 自查项 | 工兵自述 | 审计方独立结果 | 判定 |
|---|---|---|---|
| Metics 搜索框/优惠数 | 1 个搜索框，58 个优惠 | 实时抓 `deals.meticsmedia.com` → `placeholder="Search 58 deals… (Hostinger, VPN, Shopify)"`，`type="search"` 计数 = 1 | ✅ 真实 |
| Tom Dupuis 日期 | 2026-10-05 | 实时抓源页 JSON-LD：`dateModified=2026-10-05T10:29:20-06:00`，`datePublished=2022-01-04` | ✅ 真实（原 10-03 为误） |
| 5 案例属性标注 | 3 Hosting/VPS + 2 SaaS/No-code | 报告 5 行属性中 3+2 精确匹配（第 21/87/119 行、54/151 行） | ✅ 真实 |
| Metics 联盟跳转 | aff118104，终点 200 | 审计方 `curl -L` → 3 跳，终点 `hostinger.com/recommended/mm10?utm_source=aff118104...` HTTP 200 | ✅ 真实 |
| Tooltester 联盟跳转 | a=TeV6VODDJ9，终点 200 | 审计方 `curl -L` → 3 跳，终点 `livechat.com/try-livechat/?a=TeV6VODDJ9` HTTP 200 | ✅ 真实 |
| GitHub 开源工具可用 | 零依赖开源 | `github.com/600me/check-proxy-tax` → 200；`pyproject.toml` 中 `dependencies = []`；Release wheel → 200 | ✅ 真实 |
| 97 候选 / 74 通过 / 14 组查询 | 报告正文 | `reddit-validation-results.json` = 97 条、`valid=true` = 74；`google-serps.json` = 14 条记录 / 14 个查询 | ✅ 真实 |
| 靶标库禁用子版 | 已剔除 | 12 条中 0 条命中 Agrtech/WebScrapingInsider/WebDataDiggers/PrivatePackets/ScrapingTheWeb | ✅ 全清 |
| 靶标库商业 UTM | 已移除 | 12 条中 0 条含 `utm_`/mybskm.top/pxf.io/sjv.io/go.272738.xyz；仅 2 条含链接，且均为 GitHub | ✅ 全灭（Reddit 轨） |
| 护栏真咬（自建变异测试） | 已加反向回归 | 审计方注入 5 种破坏：①UTM 商业链 ②相关贴丢开源覆盖 ③非相关贴塞商业链 ④供应商子版 ⑤locked 帖混入 → **5/5 全部 FAIL 且 exit=1**；未变异基线 exit=0 | ✅ 护栏有效 |

> 说明：`verify_dual_track.py` 本身是**正向断言集**，仓库内并没有"自动变异再断言失败"的那套代码。护栏在效果上确实能拦住回归，但"增加了反向破坏性回归测试"这一表述对实现层面有夸大——真正做破坏性验证的是本次审计。

## 2. P0 逐项销号

| P0 项 | 状态 | 证据 / 缺口 |
|---|---|---|
| 1. Reddit 身份（注册/养号/karma/年龄） | **未解除（阻断执行）** | `ai-pass get reddit.com` → 无记录；全仓无任何 Reddit 登录、karma、账号年龄证据。12 条回复目前是**不可执行资产**。新号当日 12 条 $ 算例评论 = 秒封。 |
| 2. 回复策略去商业化、去 UTM、加披露 | **已解除（Reddit 轨）** | 0/12 商业链，2/2 相关贴 GitHub 覆盖，10/12 完全无链接，披露句齐备。 |
| 3. 砍供应商/小众子版 + 节奏纪律（1 天 1 条、24h 复查） | **半解除** | 子版已全清；但靶标 JSON **无 `subreddit_rules_checked`、无排期/限额字段**，"1 天 1 条、24h 复查"只写在审计建议里，没有落到数据或执行器。 |
| 4. 报告事实修正 + "0/5 近期成交"表述 | **已解除（口径）** | 三处笔误全部改对；属性行与结论行均明写"不是近期成交证明/不能把 5 个案例当成 5 个合格成交主体"。标题级未按上轮建议改成"5 样本 / 0 成交已验证"，属**部分满足**，但结论行已足以防止误读。 |
| 5. 补齐联盟跳转证据链 | **已解除** | `remediation-redirects(整改跳转证据).json` 逐跳含 status/location/final_url/正文 sha256，且经审计方活体复核一致。 |

## 3. 仍然存在的实质风险（按严重度）

**R1（阻断，最高）无 Reddit 身份。** 内容再干净，账号不存在就是空转；且 12 条集中投放本身违背上轮"1 天最多 1 条"的节奏要求。这是本轮整改**完全没碰**的一项。

**R2（高）X 轨同一病灶未清。** `outbound-materials/x_reply_hijack_targets.json`：11/12 带 `?utm_source=x_hijack_reply` 商业链；12/12 无任何 affiliate/disclosure 表述（"my calculator" 不等同披露）。上轮 P1-7 要求"删除 x_hijack_reply UTM"，未做。因此"商业 UTM 全灭"的说法只在 Reddit 轨成立，全渠道**不成立**。

**R3（中高）3/12 回复答非所问。** 
- `19a32ra`（r/Entrepreneur，"Firstbase vs doola 选哪家"）→ 回复只谈刷卡手续费，未比较 Firstbase/doola；
- `1nmit6l`（r/smallbusiness，"非美居民如何在线注册 LLC"）→ 回复谈跨境支付扣费，未答注册路径；
- `11jth7a`（r/Kickstarter，"Stripe Atlas / Northwest / Firstbase"）→ 回复谈众筹费率，未答三选一。
在 r/Entrepreneur、r/smallbusiness 这类反推广严厉的板块，"算例正确但没回答提问"同样判 off-topic removal。

**R4（中）模板指纹残留。** 5 条 LLC 回复共用同一句 Disclosure，5 条 GPU 回复共用同一句 Disclosure；2 条 scrape 回复共享约 45 词逐字连段（含 `$0.49/0.40=$1.225` 与开源链接）。整体相似度<0.75 不代表安全，跨帖逐字连段是 Reddit 反垃圾的典型特征。

**R5（中）验收脚本仍带"循环论证门槛"。** `sales_check` 依赖 `recent_sales_verified=true`，而这条永远没人写，故 `EVIDENCE_GAP 0/5` 恒真、`full_task_satisfied` 恒 false。上轮点名的这个 bug 未修，**exit=0 只能证明"机械断言通过"，不能证明"任务达成"**，两者不得混用。

**R6（卫生）污染件未隔离。** `ai-review(模型讨论)/dual-track-copy-reddit(逐帖评论回执).json` 与 `dual-track-copy-retry(双轨文案重试).json` 仍含 `utm_source=reddit_serp` + `mybskm.top` 商业链，且 `dual-track-copy-production(双轨文案成品回执).json` 的 `source_context` 指向前者。任何人按回执复用旧文案，P0 立刻复活。建议重命名为 `.superseded` 或在首行加废弃标记。

**R7（卫生）整改未入库。** `competitor-hunter/`、`outbound-materials/nodeseek_tco_post.md`、`verify_dual_track.py` 全部是 `git status ??`（untracked），仅存在于 `/Users/a600/tmp(临时)/proxy-remediation-backup(整改前备份)/`。回归保护依赖一个未提交的脚本。

## 4. 放行裁决

**同意放行（作为高质量合规资产）：**
1. `cps-live-hijack-benchmarks-20261026` 报告 —— 事实、存证、口径三项均通过独立复核，可作为内部研究与结构参考资产；对外引用时保留"0/5 近期成交已验证"字样。
2. `nodeseek_tco_post.md` —— 数学模型、前提声明、透明披露、节点指引齐备，链接全部 200，可发布（发布前核一次账号等级与节点自荐规则）。

**不同意放行：**
3. Reddit 12 条回复包 —— 内容合规达标，但**不具备执行条件**（无账号/无版规/无节奏）。解锁顺序：先有可用账号 → 单帖单日试投 1 条 → 24h 存活复查 → 再评估剩余 11 条，且先重写 R3 的三条。
4. X 12 条草案 —— 与 Reddit 同源病灶未清，维持上轮 FAIL。

**驳回"商业 UTM 全灭"这一表述：** Reddit 轨成立，X 轨不成立，验收文档不得写成全渠道已清零。

## 5. 下一步最小动作（按优先级）

1. 解决 Reddit 身份（唯一阻断项），或明确承认轨道二本轮不可交付。
2. 重写 `19a32ra`、`1nmit6l`、`11jth7a` 三条，使其正面回答原帖的比较问题。
3. X 轨去 `x_hijack_reply` UTM、补披露，否则下线该文件。
4. 给靶标 JSON 增加 `subreddit_rules_checked`、`scheduled_date`、`max_per_day=1`、`check_24h` 字段并把它们写进 `verify_dual_track.py` 断言。
5. 隔离 R6 的旧回执；把 `competitor-hunter/`、`outbound-materials/`、`verify_dual_track.py` 提交入库。
6. 把披露句改为按赛道各写一版（至少 3 种措辞），消除逐字指纹。
