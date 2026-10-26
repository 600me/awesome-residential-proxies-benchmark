# Pi DeepSeek v4.1 独立对抗审计报告

审计对象：`kais-proxy-cps-benchmark` 的【海外 CPS 活体同行反查 + Google 高排老帖截流双轨执行】交付物  
审计时间：2026-10-26（UTC）  
审计方式：独立复跑机械验收 + 20 条 Reddit 活体复核 + 5 个案例活体复核 + 源码/证据链审阅 + 账号与隔离检查  
审计立场：不采信工兵自述，只采信可复现的外部事实；商业结论与工程结论分开评级。

## 0. 总评

| 维度 | 评级 | 一句话结论 |
|---|---|---|
| 1. 同行真实性与防自嗨 | **PASS（真实性）/ WARN（同类性与证据链）/ FAIL（30 天出单 KPI）** | 5 个案例真实、5/5 推广链路可复核；但它们是泛联盟站长，不是 proxy CPS 同行；30 天出单为 0/5，诚实标记成立但证明方法薄弱。 |
| 2. 搜索流量靶标未锁性与质量 | **PASS（未锁性）/ PASS（排名取证）/ FAIL（靶标质量与可执行性）** | 20/20 帖活体 `archived=false, locked=false`；但 7/20 帖龄超过一年、7/20 落在 ≤9k 订阅的小众/供应商子版，20/20 回复导向商业计算器、0/20 导向开源工具，封禁风险高。 |
| 3. 社区与社媒物料合规 | **PASS（NodeSeek 技术内容）/ WARN（社区合规）/ WARN（X 可执行性）** | CLI 真实可用、公式正确、免责完整；但 NodeSeek 未定节点/未核版规，X 12 条是无目标推文的模板，11/12 为商业链接，重复度高。 |
| 4. 生产环境与安全隔离 | **PASS（主隔离）/ WARN（会话与标签卫生）** | 未碰个人 Chrome、未改生产调度、未付费；但用已登录 Google 会话跑 14 组 SERP 触发异常流量页，审计时 AI Chrome 仍有 32 个标签（含 Reddit/NodeSeek）。 |
| 5. 机械化验收脚本 | **WARN** | 退出 0 与 `full_task_satisfied=false` 的表述是诚实的；但检查以结构/快照为主，不能发现跑题、死链、版规、账号与封禁风险，且 sales 门槛是硬编码的永远 false。 |

**总裁决：轨道一（拆解报告）可在修正后作为内部研究使用；轨道二（20 条 Reddit 回复）不具备放行条件，立即阻断；轨道三（NodeSeek）与轨道四（X）仅可有条件小规模试投。整包不得被当作“可执行触达包”或“变现证明”。**

---

## 1. 审计方法与独立复核

我实际执行了以下独立核验，而不是只读工兵的自述：

1. 复跑 `verify_dual_track.py`：4 项 PASS，`EVIDENCE_GAP recent sales: 0 of 5`，`full_task_satisfied=false`，进程退出码 0。
2. 通过 AI Chrome（`127.0.0.1:9222`）对 20 个 Reddit 帖子逐条拉取活体 `.json`：20/20 帖子存在、`archived=false`、`locked=false`、`removed_by_category=null`，score/num_comments 与靶标 JSON 完全一致（例：`1u92g15` 7 分/26 评论；`1lphbw3` 1209 分/131 评论）。
3. 对 5 个案例逐页发起 HTTP 请求：5/5 返回 200；并独立复核了 5/5 的联盟链路（见 2.1）。
4. 用 CDP 以 1440×1000 视口重测 Metics 的 H1：`x=334, y=186.07, w=772, h=114.03, font-size=52.8px, font-family=Inter...`，与报告像素表**逐项一致**；同时测得页面只有 **1 个**搜索输入框。
5. 下载并安装 `check-proxy-tax-1.0.0-py3-none-any.whl`：无 `Requires-Dist`，`--help` 退出 0，对 `example.com` 的 5 次探针实际返回 `usable_pct=100, effective_cost_per_1k=0.49`。
6. 检查 4 个计算器页面：均 HTTP 200；无 `googletag/adsbygoogle/doubleclick` 等广告脚本；页面含 `Affiliate` 披露与 `ref=` 联盟链接。
7. 检查账号与隔离：Reddit 未登录（`/api/v1/me.json` 无 `name` 字段；`ai-pass` 无 reddit.com 记录）；NodeSeek/X 有账号记录；AI Chrome 与个人 Chrome 为两个独立进程；LaunchAgent 未新增/未改动；`vps-sniper/traffic_audit_report.json` 的 mtime 为 10-25 20:13，早于本任务（10-26 20:41 起），不归因于本任务。

---

## 2. 维度一：同行真实性与防自嗨

### 2.1 真实性与独立性：PASS

5 个案例全部是真实在线主体，且推广链路可独立复核：

| 案例 | 主体性质 | 活体结果 | 联盟链路复核 |
|---|---|---|---|
| Metics Media | YouTube 独立创作者 + 自有 deals 站 | 200 | `meticsmedia.com/hostinger-deal-websitebuilder` → `hostinger.com/recommended/mm10?...aff118104...`（本次实测） |
| Robert Brandl / Tooltester | 独立评测公司（非个人） | 200 | `/out/livechat` → `livechat.com/try-livechat/?a=TeV6VODDJ9...`（本次实测） |
| Tom Dupuis / OnlineMediaMasters | 个人站长 | 200 | 页面内 `a_aid=onlinemediamasters`（存档证据可见） |
| Tony Teaches Tech | 个人技术创作者 | 200 | `blog.ttt.do/VerpexVPS` → `clients.verpex.com/aff/?a_aid=ttt...`（存档证据可见） |
| Abhinand PS / Emerging Tech Daily | 个人博主 | 200 | `base44.pxf.io/c/3540428/2049275/25619`（存档证据可见） |

- 最终 5 个案例中**没有** Hostinger/LiveChat 等品牌官方号，也**没有** Forbes/CNN 等巨型媒体；报告对 Craylor、Medium The Digital Goldmine、Gist scumola、Substack Jennifer Leach 的剔除理由基本成立。
- 但“彻底剔除”是**结果**，不是被记录的筛选过程：自动化反查脚本的 28 条候选里，20 条是 Reddit 403 噪声，日志显示 `with_fingerprints` 仅 0→2；5 个案例主要是人工补采。报告没有区分“脚本发现”与“人工补采”，容易被误读为系统化反查的产出。

**评级：真实性 PASS；独立性 PASS（Tooltester 是公司而非个人，属“独立团队”，可接受）。**

### 2.2 “同行”同类性：WARN

5 个案例是**泛联盟 publishers**，不是 proxy CPS 同行：

- Hostinger、ScalaHosting、Verpex 属于 hosting/VPS，与代理买家的预算场景部分重叠；
- LiveChat、Base44 与 proxy CPS 无直接关系；
- 报告用“同行”“对标”描述它们，容易让读者以为这是同一赛道的竞争研究。更准确的标签是“独立联盟站的结构参考样本”。

这不算造假，但属于**范畴混淆**；如果下一阶段据此推导“proxy CPS 的可行打法”，会高估可迁移性。

### 2.3 证据链完整性：WARN

- Metics 的联盟跳转在存档 `offer-checks.json` 中记录为 `HTTP 406 Not Acceptable`，候选 JSON 的 `affiliate_links` 为空；Tooltester 的候选记录同样没有联盟链接。两者是我在本次审计中用浏览器 UA 活体重测才确认的。**报告宣称“推广可核验”，但存档证据本身不能复现这两条。**
- 报告存在两处可核实的事实错误：
  1. “58 个优惠搜索框”——实际是 **1 个**搜索框，placeholder 为 “Search 58 deals…”，58 是优惠数量。CDP 实测 `input[type=search]` 数量为 1，截图也可见。该错误直接污染了“1:1 结构/像素参考执行表”。
  2. Tom Dupuis 文章日期写成“2026-10-03”，页面实际显示 “Updated on: October 5, 2026”。
- 像素表本身是真实的（Metics 逐项复核一致），截图也是真实页面；问题在**文字描述**而非测量数据。

### 2.4 “近期 30 天真实出单”：FAIL（KPI）但 EVIDENCE_GAP 诚实性 PASS

- 报告明确写“5 个最近 30 天正在出单的硬指标未通过”“不能把 5 个案例数量当成 5 个合格成交主体”，`full_task_satisfied=false`，**没有伪造订单、佣金或到账截图**。这一点应肯定：这是本次交付中最可信的部分。
- 但“0/5”的证明方法很薄：
  - `write_benchmark_report(写入实证拆解报告).py` 第 23 行对 5 个案例统一写入 `sales_verified=False, recent_sales_verified=False`，销售结论是**手写常量**，不是由检索结果推导；
  - 反查日志没有“income report / September 2026 / monthly earnings”一类查询，未系统性寻找公开的近期收入披露；
  - `verify_dual_track.py` 的 `sales_check` 只接受结构化 `recent_sales_verified=true` 记录，而报告脚本从不生成该记录，因此该门槛**天然永远为 false**；这更像“正确的结论 + 循环论证的门槛”，而不是一次真实的 30 天销量测量。
- 就本案 5 个主体而言，公开证据确实不足以证明 30 天成交：Tooltester 是“9 年 300+ 订阅”的历史案例；Tom 是 2026 年“$150k/year”自述 + 往年黑五 $14k；其余只有活跃链接/内容更新。**联盟佣金是私有数据，外部无法逐单核验**，所以“证据缺口”是结构性真实，不是假死锁。
- 需要纠正一处措辞：Tom 的 `$150k/year` 是 **2026 年当前自述**，不完全是“历史数字”；报告把它与黑五 $14k 一起归为历史，略嫌粗糙。但它仍不是 30 天逐单成交，结论不变。

**评级：诚实性 PASS；方法 WARN；30 天出单 KPI FAIL（0/5）。**

### 2.5 防自嗨结论

报告主动写明“不能用 5 个案例数量冒充 5 个合格成交主体”，这在同类交付里是罕见的自律；但它仍然把“5 个真实公开推广案例”放在标题级结论，读者容易只记住“5 个案例”。建议把标题改为“5 个真实联盟站结构样本；0 个近期成交已验证”，并把“近期成交”单独做成一张红字限制表。

---

## 3. 维度二：搜索流量靶标的未锁性与质量

### 3.1 `archived==false` / `locked==false`：PASS

- 20/20 活体复核通过；帖子 ID、score、评论数、subreddit、created_utc 与存档一致；没有 `removed_by_category`。
- 14 组 Google 查询、140 条结果、97 个唯一 Reddit 候选、74 个通过 JSON 校验，与报告数字一致；SERP 截图、查询 URL、UTC 时间、JSON 哈希齐全。
- 我抽查了 `best residential proxy for scraping reddit` 的 SERP 截图：确为真实 Google 结果页，#1 就是 `r/WebScrapingInsider` 的 6 个月前帖子，排名记录可信；页脚显示“结果并非个性化定制”，说明 `pws=0` 生效。
- 小瑕疵：SERP 截图是中文界面/中文标题（浏览器或 Google 的翻译呈现），而 `page_text` 是英文；两者指向同一结果集，但截图不是 `hl=en` 原始英文页面的字面记录，报告应注明“截图经翻译呈现”。

**评级：未锁性 PASS；排名取证 PASS。**

### 3.2 靶标质量：FAIL

“Google 高排”在此处被误当成“高流量”。实际数据：

- **帖龄**：中位数 272 天；7/20 超过 365 天，4/20 超过 540 天，最老 1329 天（约 3.6 年）。对 1–3 年前的老帖追加评论，曝光极低。
- **互动量**：2 条 0 分，5 条 ≤4 分；4 条评论 ≤10；最低 3 条评论。多数帖子不是活跃讨论。
- **社区规模/性质**：7/20 落在 ≤9k 订阅的小众或供应商子版：
  - `r/Agrtech`：112 订阅，简介即“AGR Technology 官方子版”——在**供应商自己的子版**里推竞品工具，几乎必删；
  - `r/WebScrapingInsider`：5,029 订阅，SERP 文本显示由 ScrapeOps CEO 参与运营，是**供应商/竞品社区**；3/20 靶标在此；
  - `r/WebDataDiggers`：1,379 订阅；`r/PrivatePackets`：8,809 订阅（2/20）；`r/llc_life`：19,537 订阅但 `restrict_posting=true`。
  - 大版确有 `r/Entrepreneur`、`r/smallbusiness`、`r/LocalLLaMA`、`r/webdev` 等，但 `r/webdev` 的靶标是一条 2025-07 的 Cloudflare 新闻帖（1209 分/131 评论），商业回复会被淹没且违反其 self-promo 规则。
- **没有搜索量数据**：14 个查询都是长尾词（含 “reddit”），没有 Ahrefs/Semrush/Google Keyword Planner 的量级；排名 1–3 不等于有流量。
- **选择逻辑有偏**：脚本按 `(是否旧 ID, google_rank, -num_comments)` 排序取每赛道前 5，没有“子版质量、帖龄、是否供应商社区、是否允许推广”的门槛。

**评级：质量 FAIL；这是轨道二最实质的失败，不是“未锁”问题。**

### 3.3 商业三要素：机械 PASS，实质 FAIL

机械层面，20/20 都有“痛点句 + 美元数字 + 链接”，`verify_dual_track.py` 的 `'$' in reply` 与 `utm_source` 检查通过。但实质层面：

- **行动出口不是“无广告中转页/开源工具”**：20/20 回复全部指向 `pay/proxy/scrape/gpu.mybskm.top` 四个商业计算器域名，**0/20** 指向 `github.com/600me/check-proxy-tax`；计算器页含 `ref=` 联盟链接。也就是说，每条回复本质上是**带联盟链接的商业导流**，不是“开源工具分享”。
- **部分回复跑题**：
  - `19a32ra` 问 “Firstbase vs doola 哪个 LLC 服务好”，回复谈的是支付处理费，没有回答 Firstbase/doola 的选择；
  - `1lphbw3` 是 Cloudflare “pay per crawl” 新闻，回复谈 per-crawl 授权费预算，相关性弱；
  - `11jth7a` 问 Stripe Atlas/northwest/firstbase，回复谈众筹费率；
  - `1qnry6h` 问“如何绕过 Cloudflare”，回复直接说“不要找绕过方法，比较自建 vs API”，等于不回答原问题。
- **模板化明显**：20 条结构高度一致（“When/For/Choosing... Hypothetical... I maintain this tool... (may contain affiliate links)”），没有引用原帖的具体供应商、具体问题或 OP 的具体场景；Jaccard 相似度均值 0.25、最高 0.49，虽非逐字复制，但同一骨架足以被 Reddit 识别为模板推广。
- **UTM 自曝战术**：20/20 使用 `utm_source=reddit_serp`，X 用 `utm_source=x_hijack_reply`。公开 URL 里出现 “hijack/截流” 标签，既不利于品牌，也容易被版主/平台当作操纵证据。

**评级：三要素机械 PASS；行动出口 FAIL；逐帖定制 WARN（偏 FAIL）。**

### 3.4 封禁/SPAM 风险：FAIL（高）

- **没有 Reddit 身份**：`/api/v1/me.json` 返回未登录（只有 `features`，无 `name`）；`ai-pass get reddit.com` 无记录。这意味着 20 条回复目前**无法执行**。新注册账号立刻发 20 条带商业链接的评论，基本等于主动触发 shadowban/版务删除。
- **链接模式**：同一账号、短时间内、4 个自有域名、20 条近似模板、带 UTM、带 “may contain affiliate links”——这是 Reddit spam filter 的典型特征；后果不仅是删评，还可能**域名被全局拉黑**，连带损伤 4 个计算器站与 GitHub 项目。
- **社区规则**：`r/webdev`、`r/smallbusiness`、`r/LocalLLaMA`、`r/ollama` 等都有明确的 self-promo/低质推广限制；`r/Agrtech` 是供应商官方子版；`r/WebScrapingInsider` 是竞品运营的社区。报告只写了“archived/locked=false 不保证发言资格或版规”，但没有把“无账号、无 karma、无版规核验”列为阻断条件。
- **老帖评论的可见性**：Reddit 默认按 “best” 排序，老帖的新评论很难出现在顶部；即使不被删，实际点击/转化期望也很低。

**评级：封禁风险 FAIL；轨道二不具备执行条件。**

---

## 4. 维度三：社区与社媒物料合规

### 4.1 NodeSeek 发布稿：技术 PASS，社区 WARN

技术侧我独立验证：

- wheel 实际 11,489 字节，`Requires-Dist` 为空，真零依赖；`--help` 退出 0；`--url example.com --requests 5 --marker "Example Domain" --price-per-1k 0.49 --json` 实际返回 `usable_pct=100, effective_cost_per_1k=0.49`，说明稿件里的 CLI 示例不是纸面命令。
- 公式与算例正确：`0.49/0.40=1.225`，即标称价的 2.5 倍、高出 150%；“成功率 0% 时成本趋近无穷”也成立。
- 4 个计算器均 200；无广告脚本；页面含 `Affiliate` 披露；稿件有“无广告不等于无商业化”“报价非实时承诺”“LLC/MoR 不构成法律/税务建议、不保证收单”三段免责——符合技术论坛对“先给方法、再谈商业”的基本要求。

社区侧的风险：

- 稿件**没有指定 NodeSeek 节点**；审计时 AI Chrome 打开着 `categories/info`（情报/新闻节点）标签，而这篇是工具分享/自荐，放到情报节点属于跑题，正确节点应是“分享/技术”类。该标签无法确定性归因于本任务，但能说明“节点选择”没有被记录和核验。
- NodeSeek 的版规/节点约束未在交付中核验；按技术论坛通例，推广、联盟链接与低等级账号发链需要更高门槛，不能默认放行。账号虽有记录，但**等级/注册时长/是否被限制未核验**；`ai-pass` 里还有两条 NodeSeek 记录（用户名制与邮箱制各一条），存在重复/混用风险。
- 稿件本质是“开源 CLI + 4 个自有计算器（含联盟链接）”的自荐；即使技术内容合格，也要按“推广帖”预期管理，不能假设版务会放行。

**评级：技术 PASS；社区合规 WARN（可条件试投，不可默认放行）。**

### 4.2 X 矩阵评论区草稿：WARN（作为“草稿”合格，作为“执行包”不合格）

- 12 条草稿的痛点选得准：GPU 闲置/存储、reserved vs on-demand、代理重试税、自建 vs API、LLC vs MoR；数字算例我逐条复算，**全部正确**（如 8 卡×$2.5×125h=$2.5k；0.49/0.4=1.225；100k 成功@25%通过=400k 计费=$400）。
- 但：
  - **没有目标推文**：JSON 只有 `id/lane/trigger/reply`，没有 `target_url` 或 tweet ID；“trigger”是场景描述，不是真实推文。它不能被直接执行，只能作为“待定位”的模板。
  - **11/12 导向商业计算器**，仅 1 条导向 GitHub；“my calculator” 重复出现，容易被视为广告。
  - **UTM `x_hijack_reply`** 公开暴露“截流”意图；应改为中性来源，如 `utm_source=x_reply`。
  - **重复度/自动化风险**：12 条同一骨架、同一域名组，若在短时间内集中回复，符合 X 对 “aggressive/repetitive replies + links” 的 spam 判定特征；X 的自动化规则也要求通过 API 或人工节奏，不能脚本群发。
- 作为“草稿”它诚实（报告明确说“是模板，未伪装成已经定位的真实推文”），但作为“矩阵执行包”它缺少最关键的目标层。

**评级：WARN；先补真实目标推文与 1:1 语境，再谈执行。**

---

## 5. 维度四：生产环境与安全隔离

### 5.1 通过项

- **个人 Chrome 未被触碰**：自动化连接 `127.0.0.1:9222`，进程使用 `--user-data-dir=/Users/a600/.ai-chrome`；个人 Chrome 是另一个无调试端口的进程。符合“AI Chrome 独立实例”的要求。
- **生产调度未被改动**：`~/Library/LaunchAgents` 无新增/改动；`vps-sniper/traffic_audit_report.json` 的 mtime 为 10-25 20:13，早于本任务；本任务只改了 `README.md` 并新增 `competitor-hunter/`、`outbound-materials/` 两个文件与 `verify_dual_track.py`。没有 cron/LaunchAgent 被改写。
- **未产生付费**：没有下单、充值、订阅、API 付费调用；没有使用付费数据源。
- **未发送社区消息**：没有 NodeSeek/X/Reddit 发布记录；报告也明确“本轮未发布”。
- **证据未含会话凭据**：Reddit 证据只保存公开字段，未见 `modhash`/`reddit_session`/cookie 值；出现的邮箱是作者公开联系方式（如 `helloabhinandpsblog@gmail.com`、`affiliate@scalahosting.com`），不属于敏感凭据。
- **脚本标签关闭**：两个采集脚本都在 `finally: await page.close()` 中关闭页面，代码层面符合“用完即关”。

### 5.2 警告项

- **使用已登录 Google 会话做 SERP 抓取**：截图右上角可见 Google 账号头像；14 组查询 + 后续指纹查询触发了 Google 异常流量页（报告也承认）。这不一定封号，但会污染 AI Chrome 的 Google 会话，后续登录/搜索更容易遇到验证码。建议：SERP 抓取用未登录上下文或独立 profile，限制频率，出现验证码立即停。
- **标签卫生**：审计时 AI Chrome 有 32 个标签（现为 28 个），含 `reddit.com/?feed=home` 与 NodeSeek 页面；无法确定是否全部由本任务打开，但与本任务的研究路径部分吻合。脚本标签确实关闭了，**手工巡检标签没有确定性清理**，与“用完即关”的纪律不完全一致。
- **报告落位**：报告放在 `kais-business-findings` 根目录，而该目录的 README 规定“正式推荐只经 `recommend.py` 写入”。报告自称“不是新增生意推荐”，所以不是硬违规；但一份 19KB 的研究报告放在发现索引根目录，容易被误读为正式发现。建议移到项目文档目录，或在 findings 里只留一行链接。

**评级：主隔离 PASS；会话/标签卫生 WARN。**

---

## 6. 机械化验收脚本评估：WARN

`verify_dual_track.py` 的优点是**边界诚实**：它把“机械断言通过”与“商业指标通过”分开，明确输出 `full_task_satisfied=false`，没有把 exit 0 伪装成任务完成。这一点应保留。

但它不能支撑“交付合格”的结论：

1. **快照而非活体**：Reddit 检查读的是已保存的 `reddit-*.json` 与哈希，不重新请求 Reddit；如果证据是旧快照或伪造的，脚本无法发现（本次是我用 CDP 活体重验才排除）。
2. **语义缺失**：`'$' in reply`、`utm_source`/GitHub 字符串、45 词长度，不能判断回复是否回答原帖、是否跑题、是否是模板、是否会被版规删除。
3. **无链接存活检查**：不检查 4 个计算器/GitHub 是否 200；本次我手工验证了，但脚本没有。
4. **无账号/版规检查**：不检查 Reddit 是否登录、karma/年龄、子版是否允许推广、是否供应商社区。
5. **sales 门槛循环**：`sales_check` 只认 `recent_sales_verified=true` 的结构化记录，而报告脚本硬编码 false；因此 `sales=0` 是必然结果，不是测量结果。
6. **`EVIDENCE_GAP` 标签恒打印**：即使未来 `sales=5`，这行仍会打印 “EVIDENCE_GAP recent sales: 5 of 5 required”，属于表述 bug。
7. **`report_check` 只数标题**：`## 案例 N：` ≥5 且包含关键词就算通过，不能发现“58 个搜索框”这类事实错误。
8. **`scripts_check` 只做 AST**：检查 `max_workers=16`、`timeout=8` 字符串，不运行采集器，不能证明采集逻辑正确。
9. **`materials_check` 是字符串断言**：NodeSeek 稿件包含 `0.49/1.225` 等字样即通过，不能证明稿件可发布、节点正确、账号有权限。

**评级：WARN；可作为“结构完整性”回归测试，不能作为商业/执行验收。**

---

## 7. 风险矩阵

| 风险 | 触发条件 | 影响 | 等级 |
|---|---|---|---|
| Reddit 账号封禁/ shadowban | 新账号短时间发 20 条带链接模板 | 触达归零，申诉成本高 | **极高** |
| 4 个自有域名被 Reddit 拉黑 | 同上，链接集中在 4 个域名 | 计算器站与 GitHub 项目连带受损 | **极高** |
| 供应商子版/竞品社区删帖 | `r/Agrtech`、`r/WebScrapingInsider` 等 | 单帖归零，账号被 mod 标记 | 高 |
| Google 账号被加验证/限流 | 已登录会话高频 SERP 抓取 | AI Chrome 的 Google 能力下降 | 中高 |
| NodeSeek 删帖/降权 | 节点错误、低等级账号发联盟链接 | 社区信誉受损 | 中 |
| X 账号被限流/标记 spam | 12 条重复模板 + 商业链接集中回复 | 账号权重下降 | 中高 |
| 低流量浪费时间 | 老帖 + 长尾词 + 评论区 | 有排名、无点击、无转化 | 高 |
| “exit 0/5 案例/20 活帖”被误读为可执行 | 交付摘要与机械验收 | 团队误判进度，继续投入 | 中高 |

---

## 8. 整改清单

### P0（任何发布前必须完成）

1. **停止 20 条 Reddit 回复的直接执行**：当前无 Reddit 账号，先解决身份（注册/养号/ karma/年龄），否则一切回复都是空转。
2. **重写回复策略**：去掉 20/20 的商业计算器链接；优先“无链接的实质回答”，其次 GitHub 开源工具链接；如必须带链接，去掉 `utm_source=reddit_serp`，保留 “I maintain this / may contain affiliate links” 披露。
3. **砍掉 7/20 供应商/小众子版**：`r/Agrtech`（官方子版）、`r/WebScrapingInsider`（竞品运营）、`r/WebDataDiggers`、`r/PrivatePackets` 不建议投；保留 3–5 条大版真实提问帖，逐帖重写，1 天最多 1 条，发布后 24h 检查是否被删/被踩。
4. **修正报告事实**：
   - “58 个优惠搜索框” → “1 个搜索框，可检索 58 个优惠”；
   - Tom 日期 2026-10-03 → 2026-10-05；
   - “5 个同行” → “5 个独立联盟站结构样本；其中 3 个 hosting/VPS、2 个非 proxy 赛道”；
   - 标题级结论加“0/5 近期成交已验证”。
5. **补齐证据链**：把 Metics 的 `aff118104` 跳转、Tooltester 的 `a=TeV6VODDJ9` 跳转写入 `offer-checks.json`，否则“推广可核验”在存档层面不可复现。

### P1（下一阶段执行前）

6. **NodeSeek**：先核账号等级/注册时长/版规，选“分享/技术”节点；只发 1 篇；正文保留 GitHub 与计算器链接但明确“维护者+联盟披露”；若版规禁止联盟链接，改为 GitHub-only。
7. **X**：先找 10–20 条真实目标推文，按 1:1 语境重写；删除 `x_hijack_reply` UTM；每天 2–3 条，不脚本群发；没有目标推文就暂缓。
8. **验收脚本升级**：
   - 对每个 CTA 做实时 HTTP 200/最终 URL 检查；
   - 对每条回复做“是否回答原帖/是否含具体实体/是否跑题”的人工或模型评分；
   - 检查子版规则、账号登录/karma、是否供应商社区；
   - 把 `recent_sales` 改为“近期活跃代理指标”（最近内容更新、链接存活、公开收入披露），并明确它不是 30 天成交；
   - 修掉 `EVIDENCE_GAP` 恒打印的 bug。

### P2（卫生）

9. 把报告移到项目文档目录，或从 findings 只链接；清理 AI Chrome 残留标签；SERP 抓取改用未登录/独立 profile 并限速；保留本次审计的活体复核记录。

---

## 9. 放行结论

| 轨道 | 结论 | 条件 |
|---|---|---|
| 轨道一：拆解报告 | **内部研究可用（WARN）** | 修正 58 搜索框、Tom 日期、“同行”措辞、5/5 KPI 表述；补 Metics/Tooltester 联盟证据；不得对外发布为“同行实证” |
| 轨道二：20 条 Reddit 回复 | **FAIL，禁止放行** | 无 Reddit 身份；20/20 商业链接；7/20 供应商/小众子版；模板化；封禁与域名拉黑风险极高。需按 P0 重做后重新审计 |
| 轨道三：NodeSeek 稿 | **条件放行（WARN）** | 先核节点/版规/账号等级；只发 1 篇；保留披露；接受可能被删 |
| 轨道四：X 草案 | **条件放行（WARN）** | 先补真实目标推文；1:1 重写；去 “hijack” UTM；限速；否则暂缓 |
| 整包 | **不得作为“可执行触达包/变现证明”** | `full_task_satisfied=false` 是正确状态；当前只能作为内部研究与草稿 |

**一句话：这份交付最值得肯定的是“不伪造 30 天出单”和“证据哈希/截图/SERP 可复核”；最不能放行的是“无 Reddit 身份 + 20 条商业链接模板 + 供应商社区靶标”的组合。轨道一修完可用；轨道二必须回炉；轨道三/四只能小规模试投。**

---

## 10. 关键证据索引

- 机械验收：`verify_dual_track.py` → `mechanical_passed=true, recent_sales_verified=0, full_task_satisfied=false, exit=0`
- 活体 Reddit：20/20 `archived=false, locked=false`；score/comments 与 `serp_unarchived_reddit_targets(Google首页未锁帖靶标).json` 一致
- 活体案例：5/5 HTTP 200；联盟链路 5/5 可复核
- 像素复核：Metics H1 `334 / 186.07 / 772×114.03 / 52.8px / Inter`，与报告一致
- 结构错误：Metics 页面 `input[type=search]` 数量 = 1，placeholder “Search 58 deals…”
- CLI：wheel 11,489 bytes，无 Requires-Dist，`--help` 退出 0，实探 `example.com` 5/5 可用
- 账号：Reddit 未登录（`/api/v1/me.json` 无 name；`ai-pass` 无记录）；NodeSeek/X 有记录
- 隔离：AI Chrome `9222` + `~/.ai-chrome`；个人 Chrome 独立；LaunchAgent 未改；`traffic_audit_report.json` mtime 10-25 20:13（早于任务）
- 标签：AI Chrome 32 tabs，含 Reddit/NodeSeek；脚本均 `finally: page.close()`
