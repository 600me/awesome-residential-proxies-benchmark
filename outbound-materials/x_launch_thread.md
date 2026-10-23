# X / Twitter 首发工程 Thread — `@VerlieK88056`

> 物料版本：`launch_thread_v1`｜生成日期 2026-10-23
> 机器可读版本：`x_launch_thread.json`（含加权字数、断言来源与复算式）
> 结构依据：X 现行分发逻辑——**主推文 0 外链防降权，全部直达链接放第 1 条自我回复**。

---

## 发布结构

| # | 角色 | 外链 | 加权长度 / 280 | 目的 |
|---:|---|---|---:|---|
| 1 | 主推文 | 无 | 253 | 反直觉数字对比，制造停留与引用 |
| 2 | 线程回复 | 无 | 249 | 方法论：403 重试税三行公式 + CLI 输出 |
| 3 | 线程回复 | 无 | 254 | 数据覆盖面：4 个基准数据集 |
| 4 | 自我回复（转化出口） | 5 个（4 计算器 + GitHub） | 273 | 直达链接汇总 + 透明披露 |

> 加权长度规则：CJK 计 2、其它计 1、URL 一律计 23（t.co 包装）。全部 ≤280，无需拆分。

---

## Tweet 1 — 主推文（0 外链）

```text
"Vast is 25% cheaper than RunPod" is true on paper: H100 samples $2.01 vs $2.69/GPU-hr (-25.3%).

Then I priced one 4090 for a 1-GPU job. Vast's verified offer is a 2-card bundle: $0.858/h. RunPod: $0.34/h.

+152%.

Per-GPU-hour is not the billing unit.
```

**为什么这条能跑**：先承认一个广为流传的正确结论（-25.3%），再用同一份数据把它推翻（+152%）。没有链接，读者不会因为"这是广告"而划走；数字给的是比例而不是"省很多钱"这种空话。

**数字来源与复算**（详见 JSON 的 `claim_sources`）：
- H100：`(2.69 − 2.01) / 2.69 = 25.28%`
- 4090 单卡：Vast `$0.429/GPU-hr` 且 `bundle=2` → `0.429 × 2 = 0.858`；`(0.858 − 0.34) / 0.34 = 152.4%`
- 抽样时间 2026-10-18，页面：<https://gpu.mybskm.top/calculator/>

---

## Tweet 2 — CLI 逻辑与输出格式

```text
The 403 tax in 3 lines:

usable = 200s whose body contains your marker
effective $/1k = nominal / usable_rate
$0.49/1k @70% usable = $0.70 (1.43x). @40% = $1.225 (2.5x).

`check-proxy-tax --url ... --marker ... --json` prints that, stdlib only, MIT.
```

**说明**：三行公式就是 CLI 的全部核心逻辑（`usable_pct` / `effective_cost_per_1k` / `tax_multiplier`）。真实输出示例（`example.com`, 20 次采样, 100% 可用）：

```json
{"usable_count": 20, "blocked_count": 0, "usable_pct": 100.0,
 "effective_cost_per_1k": 0.49, "tax_multiplier": 1.0,
 "cost_status": "finite", "status_counts": {"200": 20}, "exit_code": 0}
```

---

## Tweet 3 — 4 大基准的数据覆盖

```text
What the numbers sit on:

- proxies: 9 policy dims from public pricing pages, 0 unverified cells
- scraping API vs DIY TCO
- GPU: weights+KV+CUDA x1.15, 5 card classes, 2 providers
- payments: MoR 5% vs US LLC+Stripe breakeven

No 'contact sales' inputs.
```

**覆盖范围**（每条都对应一个公开可访问的页面，便于被引用与 fact-check）：
1. 住宅代理：9 个采购维度（入口价、计费粒度、最低充值、试用、退款、地理/ASN、KYC、粘性会话窗口、适用场景）+ 实时探测表；
2. 抓取 API：自建 vs 托管 TCO，含重试放大与 credit 倍率；
3. GPU：显存模型（权重 + KV cache + CUDA context）×1.15 安全余量，5 类卡（4090/L40S/A100/H100/H200）× 2 家供应商；
4. 支付：MoR 5% vs 美国 LLC + Stripe，平衡点随卡构成/FX 变化。

---

## Tweet 4 — 自我回复（转化出口）

```text
Links, all free, no signup:

Proxies/403 tax: https://proxy.mybskm.top/calculator/?utm_source=x_thread
Scraping API TCO: https://scrape.mybskm.top/calculator/?utm_source=x_thread
GPU: https://gpu.mybskm.top/calculator/?utm_source=x_thread
Payments: https://pay.mybskm.top/?utm_source=x_thread

Code: https://github.com/600me/check-proxy-tax

Disclosure: some vendor links are affiliate; numbers don't change.
```

**UTM**：4 个计算器统一 `?utm_source=x_thread`，便于在 `traffic_audit` 里单独归因这条线程的点击；GitHub 链接不加 UTM（保持仓库链接干净）。

---

## 发布前硬检查

- [ ] Tweet 1 内**不含任何** `http`/`github.com`/`go.272738.xyz`（含隐藏换行内的链接）
- [ ] 顺序 1 → 2 → 3 → 4，第 4 条挂在第 1 条下面（self-reply），不新开线程
- [ ] 全部 4 条加权长度 ≤280（当前 253 / 249 / 254 / 273）
- [ ] 披露句保留（"some vendor links are affiliate; numbers don't change."）
- [ ] 不出现未复算数字；如需新增数字，先跑 `claim_sources[*].reproduce` 的算式
- [ ] 发布后 24h 内记录：展示量、链接点击、GitHub 访客，写回 `vps-sniper/traffic_audit_report.json` 对应渠道

## 已知限制（不要对外宣称）

- 抽样价是**某一时刻的公开抽样**，不是厂商报价或购买承诺；GPU 页面明确写了 storage/network/tax/idle 另计。
- 线程里的"effective $/1k"是**采样估计**，不是全量统计；样本量默认 20 次，做采购决策需要多时段、多出口复测。
- 本线程是内容物料，不代表已发布、已产生曝光或已产生佣金。
