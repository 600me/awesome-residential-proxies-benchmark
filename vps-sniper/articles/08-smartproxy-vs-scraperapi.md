On the sticker, a residential proxy pool looks like a rounding error next to a managed scraping API. On the invoice, the pool costs **3.9×** more for the same 250,000 rendered pages behind Cloudflare — and **35% less** for a million lightweight JSON pages. Same two vendors, opposite winners.

*Affiliate disclosure (FTC): this article contains affiliate links for Smartproxy (now Decodo) and ScraperAPI. If you buy a plan through them, I may earn a commission at no extra cost to you. Both links carry the same commission, both providers win a scenario below, and neither changes a single number in the tables. Prices are the vendors' published list prices captured on 2026-10-19, not quotes. Verify current pricing before purchasing.*

## The fork in the road: two products, two invoices

Every architecture review about scraping infrastructure reaches the same fork, and it is usually argued badly. One engineer wants to buy residential bandwidth from Smartproxy (Decodo) and drive it with `curl_cffi` or Playwright. Another wants to point a single HTTP call at ScraperAPI and let someone else own the anti-bot problem. Both are called "the scraping vendor", and the argument ends up comparing a per-gigabyte number against a per-month number — which is not a comparison at all.

The two products are not substitutes. One is a **transport**: 115M+ real-user IPs across 195+ locations, billed by the gigabyte, with the client, the fingerprint, the retry policy and the challenge logic entirely your problem. The other is a **service**: you hand it a URL, it returns HTML, and the pool, the browser, the CAPTCHA handling and the retry loop are inside a black box you rent by the credit.

| Dimension | Raw residential pool (Smartproxy / Decodo) | Managed unblocker (ScraperAPI) |
|---|---|---|
| **Billing unit** | Gigabyte of proxied traffic. Published tiers run $4.00/GB pay-as-you-go down to $2.00/GB at 1 TB; $3.50/GB at 10 GB, $2.75/GB at 100 GB. | API credit. Standard page 1 credit; Amazon 5, Google/Bing 25, LinkedIn 30; a Cloudflare/DataDome/PerimeterX bypass adds 10 credits per request. |
| **Published plan ladder** | 3 GB at $3.75/GB ($11.25) through 100 GB at $2.75/GB ($275); enterprise from 250 GB. | Hobby $49 / 100k, Startup $149 / 1M, Business $299 / 3M, Scaling $475 / 5M, then $975 and $1,975 tiers, then linear pay-as-you-go. |
| **What you must build** | HTTP client, TLS impersonation, session/sticky handling, retry and backoff, challenge detection, parser, and the monitoring that tells you a pool went bad. | One HTTP GET to an endpoint. Your code is a URL builder plus a parser. |
| **Who pays for a failure** | You do. A blocked request still moved bytes, and bytes are the meter. | The vendor absorbs the retry loop inside the credit model; credits are consumed per delivered request rather than per attempt. |
| **Marginal cost of one more page** | Near zero if the page is small and unprotected. This is the pool's whole advantage. | One credit (or 5, or 11). Linear and predictable, but never free. |
| **Marginal cost of one more *hard* page** | Steep and non-linear: retries inflate bandwidth, JS rendering inflates payload 2.4×, every failure is billed. | Bounded by the multiplier. A Cloudflare page costs 10 credits whether it took one attempt or six. |
| **Where the bill hides** | Engineering hours, render containers, and traffic burned on requests that never returned usable data. | Tier cliffs and credit multipliers. A workload at 1.05M credits pays $299, not a prorated $156. |

Read that table again and the argument dissolves. The pool is cheaper per byte and infinitely more expensive per engineer-hour. The unblocker is expensive per byte and free per engineer-hour. Which wins is a function of your block rate, your payload size, and what an hour of your team's time is worth.

## The cost model on both sides

I use the same model that ships in the public [true-cost calculator](https://scrape.mybskm.top/calculator/), so every number below is reproducible by moving the sliders.

```text
retry_multiplier      = 1 / (1 - block_rate)
bandwidth_factor      = 1 + (block_rate / (1 - block_rate)) * 0.35
js_payload_multiplier = (1 - js_share) + js_share * 2.4
avg_kb_per_page       = html_kb * js_payload_multiplier * bandwidth_factor
real_gb               = pages * avg_kb_per_page / 1,048,576
proxy_cost            = real_gb * price_per_gb
compute_cost          = pages * js_share / 100,000 * $18
engineering_cost      = hours_per_month * $75
DIY_total             = proxy_cost + compute_cost + engineering_cost
```

Two constants carry most of the argument. The **0.35** is the share of a challenge response still billed as bandwidth: you paid to be told no. The **2.4×** is the payload inflation of a headless render once scripts, fonts, images and XHR are counted — a 250 KB page becomes roughly 600 KB of metered traffic.

On the managed side it is a credit count and a tier lookup:

```text
credits = pages * ((1 - js_share) * 1 + js_share * 5)
cost    = tier_for(credits)   # 49 / 149 / 299 / 475 / ... / linear
```

The 5-credit JS multiplier is the calculator's planning assumption, not a vendor quote. ScraperAPI's own documentation puts a plain page at 1 credit and a Cloudflare/DataDome bypass at +10, so 5 is conservative for a rendering-heavy mix and optimistic for a protected one. Every table below states which multiplier it used.

## Scenario 1 — 1M lightweight pages/month, low block rate: the pool wins

A JSON or thin-HTML workload: product feeds, public APIs with an HTML fallback, documentation mirrors. 40 KB per page, 8% first-attempt block rate, 5% of pages needing a render, 30 minutes a month of maintenance, residential at the $3.50/GB ten-gigabyte tier.

| Line item | Smartproxy (Decodo) + `curl_cffi` | ScraperAPI |
|---|---|---|
| Pages / month | 1,000,000 | 1,000,000 |
| Billed attempts (8% block ⇒ 1.087×) | 1,086,957 | n/a — retries inside the API |
| Metered traffic (1.07× JS × 1.030× retry) | 42.1 GB | not metered |
| Bandwidth at $3.50/GB | $147.21 | — |
| Render compute (5% × $18/100k) | $9.00 | inside credits |
| Engineering (0.5 h × $75) | $37.50 | — |
| Credits consumed | — | 1,200,000 |
| Plan required | — | Business $299 |
| **Monthly total** | **$193.71** | $299.00 |
| **Cost per 1,000 pages** | **$0.194** | $0.299 |

The pool is **35% cheaper** here, and the gap widens at volume, because bandwidth has a real volume curve and credits do not. At the 100 GB tier ($2.75/GB) the same workload lands at **$162.16**; at a $0.49/GB third-party reseller quote — the sticker analysed in the [$0.49/GB proxy illusion teardown](https://scrape.mybskm.top/blog/proxy-cost-audit.html), which is not a Decodo list price — it lands at **$67.11**, or 78% below the managed bill.

Note the asymmetry that makes this scenario decisive. Even at *zero* maintenance hours and zero rendering, ScraperAPI cannot beat $0.149 per 1,000 pages on the Startup tier, and a 1M-page workload with any JS share at all tips over the 1M-credit cliff into the $299 tier — exactly where the pool's advantage stops being marginal. The managed product has no volume curve to fall down; the residential pool does.

**Where this breaks.** Push the block rate to **68.7%** and the DIY total crosses $299 at this page size, because bandwidth alone doubles. Push the HTML to 60 KB and the pool bill rises to **$267.31** — still cheaper than $299, but the margin is now a single engineer-hour. And the moment your targets answer with Turnstile instead of a page, the block rate is not 8%, it is 35% or worse, and you are in scenario 2.

## Scenario 2 — 250k pages/month, >30% block rate, heavy headless rendering: the unblocker wins

The workload that produces the argument in the first place: e-commerce price grids and SERP pages behind Cloudflare with Turnstile on the search path. 250 KB of HTML, 35% of first attempts blocked, 80% of pages needing a real browser, and eight engineering hours a month — about two hours a week — on fingerprint drift, selector repair and pool triage.

| Line item | Smartproxy (Decodo) + Playwright | ScraperAPI |
|---|---|---|
| Pages / month | 250,000 | 250,000 |
| Billed attempts (35% block ⇒ 1.538×) | 384,615 | n/a |
| Avg KB per page (2.12× JS × 1.188× retry) | 629.9 KB | not metered |
| Metered traffic | 150.2 GB | not metered |
| Bandwidth at $3.50/GB | $525.62 | — |
| Render compute (80% × $18/100k) | $36.00 | inside credits |
| Engineering (8 h × $75) | $600.00 | — |
| Credits consumed | — | 1,050,000 |
| Plan required | — | Business $299 |
| **Monthly total** | $1,161.62 | **$299.00** |
| **Cost per 1,000 pages** | $4.65 | **$1.196** |

The managed API is **74% cheaper**. Three multipliers did it, and none is a discount:

- **Retry amplification.** A 35% block rate means 1.538 billed attempts per usable page, and on a residential meter the failures are paid in bytes just like the successes.
- **Payload inflation.** Headless rendering multiplies metered traffic by 2.12× at an 80% JS share. You are paying residential prices for fonts, images and analytics beacons you will never parse.
- **Engineering.** Eight hours a month at $75 is $600 — more than the entire managed plan. This is the line item that never appears in the DIY column of a vendor comparison, and it is usually the decisive one.

Sensitivity matters more than the headline. Drop maintenance to two hours a month and DIY falls to $711.62: still 2.4× the managed bill, still losing. Raise it to eight hours a *week* (34.7 h/month) and DIY reaches $3,164.12 — 10.6× the managed bill. Drop the block rate to 20% and the pool still costs $1,116.96 at these page sizes, because bandwidth — not retries — dominates once rendering is involved. The only way this flips back is a much cheaper per-GB rate or a much smaller rendered payload, and neither is under your control at a protected target.

**Where this breaks.** Credit multipliers: if every one of those 250k pages sits behind Cloudflare, the real bill is not 5 credits per rendered page but 11 (1 standard + 10 bypass). That is 2.75M credits — still inside the $299 Business tier's 3M allowance, but one more multiplier notch (12+ credits per page) puts you at 3M+ and the next plan is $475. Second, freshness: a managed API's cache and retry behaviour is not yours to tune, so a workload needing a guaranteed cold fetch at a specific second may not be serviceable at any credit count.

## Scenario 3 — the hybrid fallback pattern that beats both

This is the pattern most teams converge on after paying for both mistakes once. Route **every request through the cheap path first**, and escalate only the ones that actually fail. The pool handles the 95% of traffic that never needed a bypass; the managed API handles the 5% that did.

Model: 1,000,000 pages a month, of which 950,000 are light (40 KB, 5% block, no rendering) and 50,000 are hard (140 KB, 45% block, 90% rendering). Half an hour of operations on each leg.

| Architecture | Light leg | Hard leg | Credits | Monthly total | Per 1,000 |
|---|---|---|---|---|---|
| All managed (ScraperAPI) | — | all 1M pages | 1,180,000 | $299.00 | $0.299 |
| All DIY (pool only) | $166.68 | $113.53 | — | $280.21 | $0.280 |
| **Hybrid: pool first, escalate the 5%** | **$166.68** | $49.00 (230k credits) | 230,000 | **$215.68** | **$0.216** |

The hybrid is 28% cheaper than all-managed and 23% cheaper than all-DIY. The reason is mechanical: the hard leg consumes only 230,000 credits, which fits the $49 Hobby tier, while pushing that same traffic through the pool costs $113.53 in bandwidth plus the engineering hours to keep a render farm alive. The cheap leg never touches a credit, so it never pushes you over a tier cliff.

That advantage has an expiry condition worth stating plainly: the escalation logic is itself code you maintain. The hybrid only wins while the glue costs less than **1.11 engineer-hours a month** — that is the entire margin against the $299 all-managed bill. If you have to touch the router every week, the saving evaporates and managed-everything was the correct answer.

### The 30-line router, Python standard library only

This is the whole pattern — thirty non-blank lines, standard library only. It tries the residential pool, inspects the response for the two signals that mean "this was not a page" (a challenge status code or a challenge marker in a small body), and escalates exactly those requests to the managed API.

```python
import json, os, sys, urllib.error, urllib.parse, urllib.request

PROXY, SCRAPE = os.environ["RESI_PROXY_URL"], os.environ["SCRAPERAPI_KEY"]
MARKERS = ("cf-chl", "turnstile", "Just a moment", "captcha-delivery")
CHALLENGE_STATUS = {403, 429, 503}

def _get(url, proxy=None, timeout=30):
    handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy} if proxy else {})
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.build_opener(handler).open(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")

def fetch(url):
    """Residential pool first; escalate only when the answer was not a page."""
    try:
        status, body = _get(url, proxy=PROXY)
        if status not in CHALLENGE_STATUS and not (
                len(body) < 20000 and any(m in body for m in MARKERS)):
            return body, "residential"
    except (urllib.error.URLError, TimeoutError):
        pass                              # a proxy failure is itself an escalation
    endpoint = ("https://api.scraperapi.com/?api_key=%s&url=%s"
                % (SCRAPE, urllib.parse.quote(url, safe="")))
    status, body = _get(endpoint)
    if status != 200: raise RuntimeError("%s: HTTP %s on both paths" % (url, status))
    return body, "managed"

if __name__ == "__main__":
    for target in sys.argv[1:]:
        page, path = fetch(target)
        print(json.dumps({"url": target, "path": path, "bytes": len(page)}))
```

One note on using it in anger: `urllib` presents a Python TLS fingerprint, which is precisely the failure mode described in the [sticky-session and JA3 teardown](https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html). In production swap `_get` for `curl_cffi.requests.get(..., impersonate="chrome")` and the escalation rate drops immediately. Measure the escalation rate before and after — that single number tells you whether you are paying for the managed API out of necessity or out of a client bug.

## The decision rule, in one paragraph

Buy the pool when the payload is small, the block rate is under roughly 10%, and someone already owns the client — the arithmetic gives you a 2–4× cost advantage that survives volume growth. Buy the managed unblocker when rendering is unavoidable, more than a third of your targets answer with a challenge, and the engineering time to keep a stealth stack alive is a real line item on someone's calendar. Buy *both* when the traffic is mixed, because the hybrid routes the cheap majority through the cheap meter and confines the expensive product to the requests that actually need it — and check the escalation rate monthly, since that percentage is the only input that decides whether the hybrid still pays for itself.

None of this is a prediction about your success rate. It is arithmetic over four numbers you can measure this week: pages per month, average HTML size, first-attempt block rate, and the JS share of your targets. Get those four right and the vendor question answers itself.

## Measure it yourself, then decide

- **[Scraping true-cost calculator →](https://scrape.mybskm.top/calculator/)**
- **[Sticky-session and concurrency-loss calculator →](https://proxy.mybskm.top/calculator/)**
- **[Hugging Face mirror →](https://huggingface.co/spaces/600me/rag-web-scraping-cost-calculator)**
- **[Open-source CLI, zero dependencies →](https://github.com/600me/check-proxy-tax)**
- **[Read the full teardown with every table and source note →](https://scrape.mybskm.top/blog/smartproxy-vs-scraperapi.html)**

## Try the path your arithmetic chose

Both links below carry the same commission and both providers win a scenario above. Pick with the tables, not with the discounts.

- **[Smartproxy (Decodo) residential ↗](https://go.272738.xyz/smartproxy?src=devto_smartproxy_scraperapi)**
- **[ScraperAPI managed unblocker ↗](https://go.272738.xyz/scraperapi?src=devto_smartproxy_scraperapi)**

*Affiliate links: a commission may be paid at no extra cost to you. Prices are dated list observations, not quotes; verify current terms before buying.*

## Method and sources

**Vendor prices.** Residential tiers and the plan ladder were read from Decodo's residential pricing page on 2026-10-19 (HTTP 200): $4.00/GB pay-as-you-go, $3.75/GB at 3 GB, $3.50/GB at 10 GB, $3.25/GB at 25 GB, $3.00/GB at 50 GB, $2.75/GB at 100 GB, enterprise from $2.50/GB at 250 GB to $2.00/GB at 1 TB. ScraperAPI's plans and credit rules were read from its pricing page the same day (HTTP 200): Hobby $49 / 100,000 credits, Startup $149 / 1,000,000, Business $299 / 3,000,000, Scaling $475 / 5,000,000, plus the published multipliers — 1 credit standard, 5 Amazon, 25 Google and Bing, 30 LinkedIn, and +10 when a Cloudflare, DataDome or PerimeterX bypass is applied.

**Model constants.** The retry, bandwidth, payload and tier formulas are the ones shipped in the public calculator; the 0.35 challenge-bandwidth share, the 2.4× JS payload multiplier, $18 per 100,000 renders and $75 per engineer-hour are documented planning assumptions on that page, not vendor figures. The 5-credit JS assumption on the managed side is the calculator's and is the assumption most likely to understate a fully protected workload — the +10 bypass multiplier is the vendor's own number and should replace it when your targets are all behind Cloudflare.

**What this article does not claim.** No success rate, latency or bypass result here was measured on a live target. The dollar figures are multiplications of published list prices by the stated quantities and assumptions; nothing is a quote, a promotion, or a guarantee. HTTP 200 from a vendor is not proof that a bypass works on your site. Change any input and the tables change; the method does not.

*Related research: [The 403 Tax](https://scrape.mybskm.top/blog/403-tax.html) on credit multipliers, [the $0.49/GB proxy illusion](https://scrape.mybskm.top/blog/proxy-cost-audit.html) on effective cost, and [RunPod vs Vast.ai](https://gpu.mybskm.top/blog/runpod-vs-vastai-h100-a100.html) for the same effective-cost method applied to GPU hours.*
