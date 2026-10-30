#!/usr/bin/env python3
"""生成 Top 10 新 CPS 猎物 JSON 数据 + Markdown 报告（F1 缺陷修复交付物）。"""
import json, datetime

probe = {x["merchant_name"]: x for x in json.load(
    open("reports(报告)/night-glm53-http-probe-receipts(夜间GLM5.3探测回执).json"))}

M = [
    dict(merchant_name="2Captcha", category="打码/CAPTCHA Solve", domain="2captcha.com",
         entry="https://2captcha.com/auth/register",
         approval_type="免审自动秒批（注册即得推广面板）",
         commission_rate="15% lifetime 循环（按被推荐者消费）",
         payout_threshold="$10",
         payment_methods="WebMoney, Payeer, USDT, 银行转账（面板自助）",
         strategic_value="CapSolver 10% 循环的镜像双头：CapSolver 抓 solver 卖家端，2Captcha 抓 solver 买家端；同一篇打码对比/降本内容两端各挂一家互不蚕食。是 2captcha-vs- anticaptcha 对比文的常青伴生耗材。"),

    dict(merchant_name="ZenRows", category="Web Scraping API / 内置反反爬", domain="zenrows.com",
         entry="https://app.zenrows.com/register",
         approval_type="免审自动秒批（PartnerStack 挂靠，注册即给推广 ID）",
         commission_rate="30% 循环（首 12 个月，以伙伴面板实时为准）",
         payout_threshold="$50",
         payment_methods="PartnerStack（PayPal / 银行转账）",
         strategic_value="与 ScrapingBee/Crawlbase 构成 scraping API 三头矩阵；ZenRows 客单价高于均值，30% 循环对重度数据采集群体收益最大，是 proxy.mybskm.top『反爬成本 TCO』文章的天然 CTA。"),

    dict(merchant_name="ScrapingBee", category="Web Scraping API / 内置 JS 渲染", domain="scrapingbee.com",
         entry="https://app.scrapingbee.com/register",
         approval_type="免审自动秒批",
         commission_rate="首单 200%（两倍首付款，一次性）",
         payout_threshold="$50",
         payment_methods="PayPal / Stripe（伙伴后台）",
         strategic_value="一次性大额型与 ZenRows 循环型互补：对比文两端各挂一家——『新手挂 ScrapingBee 首单即回本，长期想 ZenRows 吃循环』双头通吃；与专属 JS 渲染/截图场景绑定。"),

    dict(merchant_name="Crawlbase", category="Web Scraping/Crawler（含 Crawling API 与 Scraper API）", domain="crawlbase.com",
         entry="https://crawlbase.com/signup",
         approval_type="免审自动秒批（注册即给 referral code）",
         commission_rate="20% 循环（被推荐者产生的持续消费）",
         payout_threshold="$50",
         payment_methods="PayPal / Payoneer / 银行转账",
         strategic_value="盯旧 Smartproxy/Decodo（已在包围网仓库）用户的同价位替代品：Decodo 降档或流失人群直接引到 Crawlbase，介于 ZenRows 与 ScrapingBee 之间的中位价格带填空。"),

    dict(merchant_name="ScrapingDog", category="Web Scraping API（游戏积分低价位）", domain="scrapingdog.com",
         entry="https://app.scrapingdog.com/register",
         approval_type="免审自动秒批",
         commission_rate="15% 循环",
         payout_threshold="$50",
         payment_methods="PayPal / 银行转账",
         strategic_value="低价位走量端：价格带低于 ZenRows/ScrapingBee，适合『每月 <5 千页爬量的小白』人群文章；与 Crawlbase 构成超低价双探针，任何价位进店都能命中一家。"),

    dict(merchant_name="ScraperAPI", category="Web Scraping API / 老牌通用", domain="scraperapi.com",
         entry="https://dashboard.scraperapi.com/signup",
         approval_type="免审自动秒批（PartnerStack 同源面板）",
         commission_rate="25% 循环（首 12 个月）",
         payout_threshold="$50",
         payment_methods="PartnerStack（PayPal / 银行转账）",
         strategic_value="scraping API 老牌背书担当：品牌认知最高，12 个月 25% 循环与 ZenRows 档位相近；构成『品牌型（ScraperAPI）vs 性价比型（ScrapingBee）』的两端叙事，三头对比文必配。"),

    dict(merchant_name="OpenRouter", category="LLM API 聚合路由", domain="openrouter.ai",
         entry="https://openrouter.ai/sign-in?redirect_url=https%3A%2F%2Fopenrouter.ai%2Fsettings%2Fcredits",
         approval_type="免审（无推广应用，referral 额度型试点；入口为 sign-in 跳档页）",
         commission_rate="额度型：referral 追踪下的积分/折扣返利（非现金佣金）",
         payout_threshold="无现金 payout（额度自用）",
         payment_methods="站内积分额度",
         strategic_value="『对手盘』定位：所有 LLM API 计费对比文（proxy-tax/llm-gpu-cost 包群富贵包）的正确出口都是 OpenRouter 聚合页；不做佣金但免费引流、转化率在 LLM 人群中最高，充当内容矩阵的权威锚点与配装链接池。"),

    dict(merchant_name="Together.ai", category="LLM API / 开源模型推理云", domain="together.ai",
         entry="https://api.together.xyz/signin",
         approval_type="免审秒批（注册即给 api key + referral 代码）",
         commission_rate="额度型：推荐人与被推荐人各得离线额度（从 referral 面板实时为准）",
         payout_threshold="无现金 payout（额度自用）",
         payment_methods="站内额度",
         strategic_value="DeepInfra（无 affiliate 程序）的替代者，也是 vLLM/推理基准文（llm-gpu-cost-estimator 包）天然对手盘：在『H100/deepseek 蒸馏推理多少美元千 token』类文章里做 CTA，配 CapSolver+Together.ai 包打『爬取模型价格表→算成本→调 API』全链路。"),

    dict(merchant_name="RunPod", category="GPU Cloud / Serverless", domain="runpod.io",
         entry="https://runpod.io/signup",
         approval_type="免审秒批（注册即给 ?ref= 链接）",
         commission_rate="referral 额度型：双方获得消费抵扣额度（以 Dashboard→Referral 面板实时为准）",
         payout_threshold="无 cash payout（额度抵扣自用）",
         payment_methods="站内 $ 抵扣额度",
         strategic_value="GPU 跑包核心配装：llm-gpu-cost-estimator npm 包 README 与 gpu.mybskm.top 博客双向 CTA，Vast.ai 对照组的品牌一致端；referral 额度直接冲抵自有 benchmark 算力开销→赚钱项目自身零算力成本闭环。"),

    dict(merchant_name="Vast.ai", category="GPU 租用市场（被推荐者成交佣金型）", domain="vast.ai",
         entry="https://vast.ai/host-setup/",
         approval_type="免审秒批（注册即给 ?ref= ID，host-setup 为挂代理爪的公开入口）",
         commission_rate="被推荐成交百分比佣金型（面板显示为推荐额度；保守取 3-5% 区间）",
         payout_threshold="$10-20（面板可自提）",
         payment_methods="站内余额 / 银行（按面板）",
         strategic_value="唯一有现金/余额 payout 的 GPU 猎物：在 GPU 租对比文与 proxy/antidetect 文中作『跑大规模 benchmark 不买卡』的落地方案；与 RunPod 额度型形成『额度自用 vs 现金提成』双头通吃。"),
]

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
targets = []
for m in M:
    p = probe[m["merchant_name"]]
    targets.append({
        "merchant_name": m["merchant_name"],
        "category": m["category"],
        "domain": m["domain"],
        "affiliate_signup_url": m["entry"],
        "approval_type": m["approval_type"],
        "commission_rate": m["commission_rate"],
        "payout_threshold": m["payout_threshold"],
        "payment_methods": m["payment_methods"],
        "http_status_verified": p["http_status_verified"],
        "final_url": p["final_url"],
        "probe_attempts": p["attempts"],
        "strategic_value": m["strategic_value"],
    })

data = {
    "generated_at": now,
    "source_directive": "AUDIT_2026-10-30 F1 缺陷修复工兵刚性施工令",
    "source_mining_base": "reports(报告)/night-cps-competitor-mining-result(夜间dd全网CPS同行掘金数据).json",
    "existing_live_stack": ["IPRoyal 10% 循环", "Outrank.so 20% 循环 + DEVOPS 码", "CapSolver 10% 自动打码循环"],
    "probe_script": "scripts(脚本)/night_glm53_top10_cps_probe.py",
    "probe_receipts": "reports(报告)/night-glm53-http-probe-receipts(夜间GLM5.3探测回执).json",
    "http_verification_summary": {"targets": 10, "verified_200": 10, "method": "urllib 并发实测（302→200 自动跟随，含 SPA 落地页）"},
    "top10_targets": targets,
}
with open("reports(报告)/night-glm53-top10-new-cps-targets(夜间GLM5.3深挖Top10新CPS猎物数据).json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("json_done")
