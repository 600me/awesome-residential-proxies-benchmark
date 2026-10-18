#!/usr/bin/env python3
"""Publish two canonical-bound technical articles to Dev.to.

    python3 devto-publisher.py --dry-run
    DEVTO_API_KEY=... python3 devto-publisher.py --post

The script uses only the Python 3 standard library.  ``--dry-run`` is fully
offline: it builds and validates both Markdown documents (including YAML
frontmatter), prints the metadata and the complete articles, and never opens a
network connection or touches ``published_articles.jsonl``.

``--post`` sends each article to the official Dev.to REST endpoint
``POST https://dev.to/api/articles`` with the ``api-key`` header and appends a
success receipt to ``published_articles.jsonl`` beside this file.  A run is
idempotent by canonical URL unless ``--force`` is supplied.  The API key is
read from ``DEVTO_API_KEY`` and is never written to output or the ledger.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "published_articles.jsonl"
API_URL = "https://dev.to/api/articles"
USER_AGENT = "kais-devto-publisher/1.0 (+https://scrape.mybskm.top/)"
UTM = "utm_source=devto&utm_medium=article"
MIN_WORDS = 1200
REQUIRED_FRONTMATTER = ("title", "published", "tags", "canonical_url", "series")


ARTICLE_ONE_BODY = r"""
The crawl finished at 06:00. The job log says 100,000 requests. The dataset has 68,000 usable rows, 22,000 challenge pages, and 10,000 timeouts. The invoice counts 100,000 requests plus every retry, every JavaScript render, and every premium-proxy attempt.

That gap between requests sent and pages usable is the 403 tax. It is invisible on a pricing page, and it is the number that decides whether a scraping API is cheap or expensive.

This is a cost-first teardown of the problem. I use the normalized plan inputs published on [scrape.mybskm.top](https://scrape.mybskm.top/?utm_source=devto&utm_medium=article&utm_campaign=scraping_api_benchmark), walk through the arithmetic, and then show a two-hour pilot that produces a better buying decision than any vendor comparison table.

## The invoice counts attempts, not answers

A scraping API is not a bandwidth pipe. It is a request orchestrator: it chooses an IP, opens a TLS session, may execute JavaScript, may solve or wait out a challenge, and may retry. Every one of those steps can consume a credit.

That is why two providers can both advertise "$49 per month" and produce very different bills. The useful unit is not the request. It is the **usable page**: a response that contains the fields your pipeline needs, at the time you need them.

A 200 response with a Cloudflare interstitial is a failure. A 403 with a valid cached copy may still be a success if your pipeline is allowed to use the cache. A timeout after 30 seconds may have consumed a credit even though it produced nothing. Your accounting has to follow the output, not the status code.

## A residential IP is not a Turnstile pass

Cloudflare, DataDome, and Akamai do not make a single decision. They combine signals:

- IP reputation and ASN type.
- TLS fingerprint and HTTP/2 settings.
- Header order and browser fingerprint.
- Cookie and challenge-token state.
- Request rate, navigation pattern, and mouse or keyboard behavior.

A residential IP helps with the first signal. It does not automatically produce a valid Turnstile token. Turnstile requires JavaScript execution in a browser-like environment, and that execution is usually billed at a higher credit multiplier. DataDome and Akamai apply similar layered checks.

This is the practical reason "just buy residential proxies" often disappoints. You can move the IP and still fail the browser and token checks. A managed scraping API bundles the browser, the proxy, and the retry logic, but it charges for all three.

## The credit multiplier is the real price list

The public calculator normalizes four providers to a common baseline. The inputs below were observed on 2026-10-17. They are planning baselines, not fresh vendor quotes, and the site explicitly labels them that way.

| API (baseline input) | Plan | Included credits | Cost / credit | 10k @ 1 credit | 10k @ 5 credits | 10k @ 25 credits |
|---|---:|---:|---:|---:|---:|---:|
| ZenRows | $49 | 250,000 | $0.000196 | $1.96 | $9.80 | $49.00 |
| ScrapingBee | $49 | 150,000 | $0.000327 | $3.27 | $16.33 | $81.67 |
| ScraperAPI | $49 | 100,000 | $0.000490 | $4.90 | $24.50 | $122.50 |
| Crawlbase | $29 | not specified | n/a | n/a | n/a | n/a |

The formula is simple:

```text
cost per request = plan price / included credits * credits per request
```

At one credit per request, the difference between the cheapest and most expensive normalized option is $2.94 per 10,000 requests. At 25 credits per request, it is $73.50. The multiplier, not the plan price, controls the spread.

Crawlbase is deliberately left as n/a. Its supplied baseline does not state the included paid request volume, so the $2.90 per 10,000 estimate cannot be converted into a per-credit rate. Treating it as comparable would be a spreadsheet error dressed up as analysis.

## Retry amplification: the line item finance never sees

Suppose you need 100,000 URLs. Thirty percent hit a challenge or a 403. A naive retry policy tries each failed URL three times. You now bill:

```text
70,000 non-challenged attempts + 30,000 challenged URLs * 3 attempts = 160,000 billed attempts
```

If every attempt costs one credit, the allocated cost at the normalized rates is:

| Billing assumption | Billed credits | ZenRows | ScrapingBee | ScraperAPI |
|---|---:|---:|---:|---:|
| 1 credit per attempt | 160,000 | $31.36 | $52.27 | $78.40 |
| 5 credits per challenged retry | 520,000 | $101.92 | $169.87 | $254.80 |

The second row is the important one. It assumes 70,000 clean requests at one credit and 30,000 challenged requests at three attempts times five credits. That is 520,000 credits for a job that "only" had 100,000 URLs.

These are allocated plan costs, not necessarily the provider's overage price. Overage rates can be higher, and plans may throttle or block before overage. The point is directional: a retry policy without a credit budget is an open-ended invoice.

## Cost per 1,000 usable pages

The metric to put in the budget is:

```text
cost per 1,000 usable pages =
  (cost per credit * credits per attempt) / usable yield * 1,000
```

Using the normalized rates and an explicit 70% yield assumption:

| API | $ / 1k attempts (1 credit) | $ / 1k usable at 70%, 1 credit | $ / 1k usable at 70%, 5 credits |
|---|---:|---:|---:|
| ZenRows | $0.196 | $0.280 | $1.400 |
| ScrapingBee | $0.327 | $0.467 | $2.333 |
| ScraperAPI | $0.490 | $0.700 | $3.500 |

Seventy percent is an assumption, not a measurement. It is there to make the arithmetic visible. If the supplied baseline success rates of 98.5%, 97.8%, and 96.5% held, the one-credit numbers would be $0.199, $0.334, and $0.508 per 1,000 usable pages. Those rates are supplied planning inputs, not independent target measurements, so your own pilot still decides.

The 5-credit column is the part most teams miss. A provider with a lower per-credit price can lose on a target that forces JavaScript rendering on every request. The opposite is also true: a provider with a higher per-credit price can win if it avoids retries and returns clean data on the first attempt.

## A two-hour pilot that beats any comparison table

You do not need a 10,000-request benchmark to make a good decision. You need a representative sample, a definition of usable, and honest accounting.

1. **Pick 200 URLs.** Stratify by template, not by random pages. Include the pages that produce the most revenue or the most support tickets.
2. **Define usable before you run.** A product page is usable only if the price, currency, and availability fields are present. A listing page is usable only if it returns the expected number of items. Hash the relevant fragment, not the whole HTML, so rotating ads do not create false negatives.
3. **Run three times.** Morning, midday, and evening in the target geography. Use the same session settings and the same timeout. Record status, latency, bytes, and credits consumed.
4. **Count retries as cost.** If your client retries three times, the pilot must record three attempts. Otherwise the result is a demo, not an economic measurement.
5. **Compute the useful number.** Cost per 1,000 usable pages, not cost per request. Add the engineering time spent on the integration.

A minimal standard-library probe looks like this:

```python
import hashlib
import json
import time
import urllib.request

TARGET = "https://example.com/product/123"
MARKER = "Add to cart"

def probe(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "cost-pilot/1.0"})
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        status = response.status
    return {
        "status": status,
        "seconds": round(time.perf_counter() - started, 3),
        "usable": MARKER.encode() in body,
        "sha256": hashlib.sha256(body).hexdigest()[:16],
    }

print(json.dumps(probe(TARGET)))
```

Run that through your provider's endpoint and through a direct baseline. The direct baseline tells you what the target does without a proxy. The provider result tells you what you are buying. If the direct baseline is already 95% usable, a managed API may still be worth it for maintenance and IP rotation, but you should price it as an operational convenience, not as a magic bypass.

## What I would do with a $49 budget

Start with the free trial, not the annual plan. Run the 200-URL pilot. Measure usable yield and credits per usable page. Then decide whether the problem is IP reputation, browser execution, or your own parser.

Three rules have saved me more money than any vendor comparison:

- **Cache before you crawl.** A page that has not changed does not need a new credit.
- **Use the official API when one exists.** It is usually cheaper, more stable, and less likely to trigger a challenge than scraping the HTML.
- **Set a retry budget.** If a URL fails three times, park it and alert. Infinite retries convert a temporary block into a permanent cost.

## The conclusion that survives contact with production

The cheapest scraping API is not the one with the lowest sticker price. It is the one with the lowest cost per usable page at your target, your geography, and your required freshness.

That number depends on three variables you control: the credit multiplier of the request mode, the yield of the target, and the retry policy. A provider that looks 60% cheaper per credit can be 2.5x more expensive per usable page once rendering is included. A provider that looks expensive can win if it returns clean data on the first attempt.

Run the arithmetic before you run the invoice. The calculator and the underlying baseline are public:

- **Scraping API cost calculator:** [scrape.mybskm.top](https://scrape.mybskm.top/?utm_source=devto&utm_medium=article&utm_campaign=scraping_api_benchmark)
- **Residential proxy economics:** [proxy.mybskm.top](https://proxy.mybskm.top/?utm_source=devto&utm_medium=article&utm_campaign=proxy_benchmark)
- **Methodology and data:** [GitHub repository](https://github.com/600me/awesome-web-scraping-apis-benchmark?utm_source=devto&utm_medium=article&utm_campaign=scraping_api_benchmark)

**Disclosure:** Some outbound links on this page are affiliate links. If you buy a service through them, I may earn a commission at no extra cost to you. The baseline figures are supplied planning inputs, not independently measured target results or current vendor quotes. Verify current pricing and terms with each provider before purchasing.

**Data note:** Normalized plan inputs observed 2026-10-17T12:39:14Z. Success rates and 10k estimates are supplied baselines, and performance was not independently measured. HTTP 200 is not proof of bypass success.
"""


ARTICLE_TWO_BODY = r"""
An eight-hour H100 fine-tune looks like a $21.52 line item at $2.69 per GPU-hour. Then you discover the cheapest listing is a two-GPU bundle, the dataset sits in storage for a week, the job checkpoints twice, and the instance is interrupted at hour six. The bill is not $21.52, and the headline rate was never the price.

This is a practical teardown of GPU cloud pricing using live catalogue rates observed on 2026-10-17. The point is not that one provider is always cheaper. The point is that the advertised GPU-hour is a component price, and your budget needs the fully loaded number.

## What the advertised rate includes

Most GPU marketplaces quote compute only:

- The GPU and its host memory.
- The container or VM while it is running.
- Sometimes local disk, sometimes not.
- Sometimes network, sometimes not.

Storage, egress, taxes, idle time, and restart overhead are usually separate. Multi-GPU offers may require you to rent the whole bundle even if your job can only use one GPU. Community or interruptible capacity may be cheaper because the inventory is not reserved and can disappear.

That is why a rate table is a starting point, not a budget. The useful unit is **cost per useful GPU-hour**: the total bill divided by the GPU-hours that actually produced work you can keep.

## What the market actually listed on 2026-10-17

The public GPU index samples RunPod's catalogue and Vast.ai's verified on-demand bundles. These are live catalogue observations, not negotiated quotes. Inventory is not guaranteed, and storage and network are extra.

| Provider | GPU | Tier | $ / GPU-hour | 100 GPU-hours | Bundle constraint |
|---|---|---|---:|---:|---|
| RunPod | H100 SXM 80GB | Community | $2.690 | $269.00 | Single GPU |
| RunPod | H100 SXM 80GB | Secure | $3.990 | $399.00 | Single GPU |
| Vast.ai | H100 SXM 80GB | Verified on-demand | $2.134 | $213.40 | 2-GPU bundle at $4.269/hour |
| RunPod | H100 PCIe 80GB | Community | $1.990 | $199.00 | Single GPU |
| RunPod | H100 PCIe 80GB | Secure | $2.890 | $289.00 | Single GPU |
| Vast.ai | H100 PCIe 80GB | Verified on-demand | $2.268 | $226.80 | 2-GPU bundle at $4.537/hour |
| RunPod | A100 80GB SXM | Community | $1.390 | $139.00 | Single GPU |
| RunPod | A100 80GB SXM | Secure | $1.790 | $179.00 | Single GPU |
| Vast.ai | A100 80GB SXM | Verified on-demand | $1.056 | $105.60 | Single GPU |
| RunPod | A100 80GB PCIe | Community | $1.190 | $119.00 | Single GPU |
| RunPod | A100 80GB PCIe | Secure | $1.790 | $179.00 | Single GPU |
| Vast.ai | A100 80GB PCIe | Verified on-demand | $1.001 | $100.10 | 2-GPU bundle at $2.002/hour |
| RunPod | RTX 4090 24GB | Community | $0.340 | $34.00 | Single GPU |
| RunPod | RTX 4090 24GB | Secure | $0.890 | $89.00 | Single GPU |
| Vast.ai | RTX 4090 24GB | Verified on-demand | $0.429 | $42.90 | 2-GPU bundle at $0.857/hour |

Two things stand out. First, the H100 SXM spread between the cheapest verified listing and the secure RunPod listing is $1.856 per GPU-hour, or 87% more for the secure tier. Second, the cheapest headline rate on the board is not always the cheapest job, because of the bundle minimum.

## The two-GPU minimum is a commitment

Take an eight-hour fine-tune that fits on one H100 SXM.

At RunPod's community rate, the compute cost is:

```text
8 hours * $2.69 = $21.52
```

At Vast.ai's H100 SXM rate, the listing is a two-GPU bundle at $4.269 per hour. If the job cannot use the second GPU, you still pay for it:

```text
8 hours * $4.269 = $34.15 for 16 GPU-hours
```

You paid for 16 GPU-hours to do 8 GPU-hours of useful work. The effective cost is $4.269 per useful GPU-hour, not $2.134. The bundle is only a discount if you can run two single-GPU jobs in parallel or split the workload across both cards.

That is the first rule of GPU shopping: **a two-GPU minimum is not a lower price, it is a larger commitment.** Compare the smallest rentable unit, not the per-GPU rate.

## Community versus Secure is not a 10% upsell

The tier names vary, but the trade-off is consistent: community or interruptible capacity is cheaper because the provider does not reserve it; secure or on-demand capacity costs more because it is isolated and more likely to stay up.

The observed premiums are large:

| GPU | Community / standard | Secure / reserved | Premium |
|---|---:|---:|---:|
| H100 SXM 80GB | $2.690 | $3.990 | +48.3% |
| A100 80GB SXM | $1.390 | $1.790 | +28.8% |
| RTX 4090 24GB | $0.340 | $0.890 | +161.8% |

A 48% premium on an H100 is $1.30 per GPU-hour. On a 100-hour job, that is $130. Whether it is worth it depends on what a lost hour costs you.

If the job checkpoints every 15 minutes and can resume automatically, community capacity can be a rational choice. If the job is a deadline-bound inference service or a multi-day training run without checkpointing, the secure tier may be cheaper than the recovery work. The premium buys availability and isolation, not necessarily raw speed.

## Utilization is the multiplier that never appears in the rate

You do not pay for useful GPU-hours. You pay for billed GPU-hours. If the GPU is waiting on data loading, a stuck download, or a serial preprocessing step, you still pay.

For 100 useful GPU-hours:

| Utilization | Billed GPU-hours | Vast.ai H100 SXM at $2.134 | RunPod Community H100 SXM at $2.690 |
|---:|---:|---:|---:|
| 100% | 100.0 | $213.40 | $269.00 |
| 80% | 125.0 | $266.75 | $336.25 |
| 60% | 166.7 | $355.67 | $448.33 |

At 60% utilization, the effective cost of a useful H100 SXM hour is $3.56 on the cheaper listing and $4.48 on the more expensive one. Neither number appears on the pricing page.

This is where data engineering matters more than GPU shopping. A fast NVMe path, a pre-tokenized dataset, and a loader that keeps the GPU fed can be worth more than a $0.50 rate difference. Measure tokens per second or images per second on your actual pipeline, not just the GPU model.

## What 100 GPU-hours actually cost

On paper, Vast.ai's H100 SXM listing is $55.60 cheaper than RunPod's community listing for 100 GPU-hours:

```text
$269.00 - $213.40 = $55.60
```

That is a 20.7% saving. Now add one operational incident. A 45-minute interruption at a $65 per hour engineering cost is $48.75. That single incident consumes 88% of the saving. Two incidents and the cheaper listing is more expensive.

The arithmetic is not an argument against the cheaper listing. It is an argument for checkpointing, monitoring, and a restart budget. If your job can tolerate interruption and you have automated recovery, the saving is real. If every failure requires a human, the saving is a subsidy for your future self.

Storage and egress can add smaller but real amounts. Using explicit assumptions of $0.10 per GB-month for storage and $0.05 per GB for egress, a 500GB dataset kept for seven days costs about $11.67, and 200GB of egress costs about $10.00. Those are illustrative rates, not quotes. The point is to put them in the model instead of discovering them on the invoice.

## The only number to put in the budget

Use this formula:

```text
effective $ / useful GPU-hour =
  (hourly rate * billed hours + storage + egress + restart cost)
  / useful GPU-hours
```

Example: 100 useful hours on the Vast.ai H100 SXM listing at 80% utilization.

```text
billed hours = 100 / 0.80 = 125
compute = 125 * $2.134 = $266.75
storage + egress + restart = $15 + $10 + $20 = $45
total = $311.75
effective rate = $311.75 / 100 = $3.12 per useful GPU-hour
```

The headline rate was $2.134. The budget number is $3.12, about 46% higher. Run the same calculation for the secure tier and for your own utilization. The ranking can change.

## A decision guide that survives real workloads

| Workload | Sensible first test | Why |
|---|---|---|
| Single 8-hour fine-tune | RunPod Community H100 SXM or A100 80GB | No bundle minimum; $21.52 or $11.12 for eight hours at observed rates |
| Long, checkpointable batch | Vast.ai verified on-demand | Lowest observed $/GPU-hour, but budget restarts and verify the bundle |
| Production inference | Secure or on-demand with capacity | Availability and isolation matter more than a $0.50 difference |
| Multi-GPU training | Compare bundle price and interconnect | A two-GPU bundle can fit, but verify NVLink and topology |
| Cost-sensitive small models | RTX 4090 24GB | Lowest $/hour, but 24GB VRAM is not an H100 substitute |

The RTX 4090 row is a reminder that the cheapest GPU-hour is not always the right GPU-hour. If the model does not fit in 24GB, a $0.34 rate is irrelevant. If it does fit, the same 100 GPU-hours cost $34 on RunPod Community versus $269 on H100 SXM. The workload decides.

## What I would do with a $200 budget

Do not start with 100 GPU-hours. Start with 20 to 40 GPU-hours on the smallest rentable unit that fits the model. Measure throughput, not just latency to first token. Checkpoint every 15 minutes. Log the cost per useful GPU-hour, including storage and egress.

Then compare the effective rate, not the advertised rate. A provider that is 20% cheaper per GPU-hour but interrupts twice as often may lose. A provider that is 20% more expensive but keeps the GPU fed may win.

The public index and the underlying observations are here:

- **GPU cloud price index:** [gpu.mybskm.top](https://gpu.mybskm.top/?utm_source=devto&utm_medium=article&utm_campaign=gpu_benchmark)
- **Pricing methodology:** [GitHub repository](https://github.com/600me/awesome-gpu-cloud-pricing-benchmark?utm_source=devto&utm_medium=article&utm_campaign=gpu_benchmark)
- **Scraping API cost calculator:** [scrape.mybskm.top](https://scrape.mybskm.top/?utm_source=devto&utm_medium=article&utm_campaign=scraping_api_benchmark)

**Disclosure:** Some outbound links on this page are affiliate links. If you buy a service through them, I may earn a commission at no extra cost to you. Rates are catalogue observations, not quotes, and inventory changes. Verify current pricing, storage, egress, and interruption policy with the provider before committing budget.

**Data note:** GPU rates observed 2026-10-17T12:50:44Z from RunPod's GraphQL catalogue and Vast.ai's bundles API. Secure and community availability is not guaranteed. Storage, network, taxes, and restart overhead are excluded from the headline rates.
"""


ARTICLES = [
    {
        "key": "scraping-api-403-tax",
        "title": "The 403 Tax: What Anti-Bot Protection Really Does to Your Scraping Bill",
        "description": (
            "A cost-first teardown of scraping APIs under Cloudflare and Turnstile "
            "pressure: credit multipliers, retry amplification, and the only metric "
            "that survives production."
        ),
        "tags": ["webscraping", "cloudflare", "python", "api"],
        "canonical_url": "https://scrape.mybskm.top/",
        "series": "Anti-Bot Economics",
        "body": ARTICLE_ONE_BODY.strip(),
    },
    {
        "key": "h100-rental-trap",
        "title": "The H100 Rental Trap: Why $2.13 per GPU-Hour Is Not the Price You Pay",
        "description": (
            "Live H100 and A100 catalogue rates, bundle minimums, utilization, and "
            "restart overhead: how to calculate the effective cost of a useful "
            "GPU-hour before you rent."
        ),
        "tags": ["gpu", "cloud", "machinelearning", "devops"],
        "canonical_url": "https://gpu.mybskm.top/",
        "series": "GPU Cloud Cost Notes",
        "body": ARTICLE_TWO_BODY.strip(),
    },
]


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


def build_markdown(article, published=False):
    """Build a Dev.to-compatible Markdown document with YAML frontmatter."""
    lines = [
        "---",
        "title: " + json.dumps(article["title"], ensure_ascii=False),
        "published: " + ("true" if published else "false"),
        "tags: " + json.dumps(article["tags"], ensure_ascii=False),
        "canonical_url: " + json.dumps(article["canonical_url"], ensure_ascii=False),
        "series: " + json.dumps(article["series"], ensure_ascii=False),
        "---",
        "",
        article["body"].strip(),
        "",
    ]
    return "\n".join(lines)


def parse_frontmatter(markdown):
    """Parse the small YAML subset this script emits, using JSON scalar rules."""
    if not markdown.startswith("---\n"):
        raise ValueError("missing opening frontmatter fence")
    end = markdown.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter fence")
    block = markdown[4:end]
    data = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError("malformed frontmatter line: " + line)
        key, raw = line.split(":", 1)
        key = key.strip()
        raw = raw.strip()
        if raw in ("true", "false", "null") or raw.startswith(('"', "[", "{")):
            data[key] = json.loads(raw)
        else:
            data[key] = raw
    return data, markdown[end + 5:]


def validate_article(article):
    """Raise ValueError unless the article is safe to publish as-is."""
    if not isinstance(article.get("title"), str) or not article["title"].strip():
        raise ValueError("article title is empty")
    if len(article["title"]) > 128:
        raise ValueError("article title is longer than 128 characters")
    if not isinstance(article.get("tags"), list) or not 1 <= len(article["tags"]) <= 4:
        raise ValueError("Dev.to requires 1-4 tags")
    for tag in article["tags"]:
        if not re.fullmatch(r"[a-z0-9]+", tag):
            raise ValueError("invalid Dev.to tag: " + repr(tag))
    if article["canonical_url"] not in (
        "https://scrape.mybskm.top/",
        "https://gpu.mybskm.top/",
    ):
        raise ValueError("unexpected canonical_url: " + article["canonical_url"])
    if not article.get("series"):
        raise ValueError("series is empty")
    if not article.get("description"):
        raise ValueError("description is empty")
    body = article["body"]
    if "REPLACE_ME" in body:
        raise ValueError("body contains REPLACE_ME")
    if "TODO" in body or "TBD" in body:
        raise ValueError("body contains an unfinished placeholder")
    if body.count(UTM) < 2:
        raise ValueError("body needs at least two Dev.to UTM links")
    if word_count(body) < MIN_WORDS:
        raise ValueError(
            "body is too short: %d words (minimum %d)"
            % (word_count(body), MIN_WORDS)
        )

    markdown = build_markdown(article, published=False)
    frontmatter, rendered_body = parse_frontmatter(markdown)
    for field in REQUIRED_FRONTMATTER:
        if field not in frontmatter:
            raise ValueError("frontmatter is missing " + field)
    if frontmatter["published"] is not False:
        raise ValueError("dry-run frontmatter must set published: false")
    if frontmatter["tags"] != article["tags"]:
        raise ValueError("frontmatter tags do not match the article")
    if frontmatter["canonical_url"] != article["canonical_url"]:
        raise ValueError("frontmatter canonical_url does not match the article")
    if frontmatter["title"] != article["title"]:
        raise ValueError("frontmatter title does not match the article")
    if frontmatter["series"] != article["series"]:
        raise ValueError("frontmatter series does not match the article")
    if rendered_body.strip() != body.strip():
        raise ValueError("frontmatter parser lost the body")
    return {
        "key": article["key"],
        "title": article["title"],
        "canonical_url": article["canonical_url"],
        "series": article["series"],
        "tags": article["tags"],
        "description": article["description"],
        "word_count": word_count(body),
        "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "frontmatter": frontmatter,
    }


def validate_all():
    if len(ARTICLES) != 2:
        raise ValueError("exactly two articles are required")
    seen = set()
    metadata = []
    for article in ARTICLES:
        if article["key"] in seen:
            raise ValueError("duplicate article key: " + article["key"])
        seen.add(article["key"])
        metadata.append(validate_article(article))
    if {item["canonical_url"] for item in metadata} != {
        "https://scrape.mybskm.top/",
        "https://gpu.mybskm.top/",
    }:
        raise ValueError("the two articles must bind different mybskm.top sites")
    return metadata


def read_ledger():
    if not LEDGER.exists():
        return []
    receipts = []
    with LEDGER.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                receipts.append(json.loads(line))
            except json.JSONDecodeError:
                print("warning: ignoring malformed ledger line", file=sys.stderr)
    return receipts


def append_receipt(receipt):
    with LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def post_article(article, api_key, force=False):
    """POST one article and return a receipt dict; raise on HTTP failure."""
    receipts = read_ledger()
    if not force and any(
        item.get("canonical_url") == article["canonical_url"]
        and item.get("status") == "published"
        for item in receipts
    ):
        print(
            "skip: already published for %s (use --force to override)"
            % article["canonical_url"],
            file=sys.stderr,
        )
        return None

    payload = {
        "article": {
            "title": article["title"],
            "published": True,
            "body_markdown": article["body"],
            "tags": article["tags"],
            "canonical_url": article["canonical_url"],
            "series": article["series"],
            "description": article["description"],
        }
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        status = response.status
        raw = response.read()
    data = json.loads(raw.decode("utf-8"))
    if status not in (200, 201):
        raise RuntimeError("unexpected Dev.to HTTP status: %d" % status)
    receipt = {
        "posted_at": now(),
        "status": "published",
        "http_status": status,
        "id": data.get("id"),
        "url": data.get("url"),
        "slug": data.get("slug"),
        "title": article["title"],
        "canonical_url": article["canonical_url"],
        "series": article["series"],
        "tags": article["tags"],
    }
    append_receipt(receipt)
    return receipt


def dry_run():
    metadata = validate_all()
    report = {
        "mode": "dry-run",
        "network_writes": False,
        "article_count": len(metadata),
        "utm": UTM,
        "articles": metadata,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    for index, article in enumerate(ARTICLES, 1):
        print("\n" + "=" * 78)
        print("ARTICLE %d/%d: %s" % (index, len(ARTICLES), article["title"]))
        print("=" * 78 + "\n")
        print(build_markdown(article, published=False))
    return 0


def post_all(force=False):
    metadata = validate_all()
    api_key = os.environ.get("DEVTO_API_KEY", "").strip()
    if not api_key:
        print(
            "DEVTO_API_KEY is not set; refusing to publish. "
            "Dry-run validation is available with --dry-run.",
            file=sys.stderr,
        )
        return 2
    print(
        json.dumps(
            {"mode": "post", "article_count": len(metadata), "utm": UTM},
            ensure_ascii=False,
        )
    )
    failures = 0
    for index, article in enumerate(ARTICLES, 1):
        try:
            receipt = post_article(article, api_key, force=force)
        except urllib.error.HTTPError as exc:
            detail = exc.read(2000).decode("utf-8", "replace")
            print(
                "post failed for %s: HTTP %s %s"
                % (article["key"], exc.code, detail),
                file=sys.stderr,
            )
            failures += 1
            continue
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            print(
                "post failed for %s: %s" % (article["key"], exc),
                file=sys.stderr,
            )
            failures += 1
            continue
        if receipt is None:
            continue
        print(
            json.dumps(
                {
                    "posted": receipt["title"],
                    "id": receipt["id"],
                    "url": receipt["url"],
                    "canonical_url": receipt["canonical_url"],
                },
                ensure_ascii=False,
            )
        )
        if index < len(ARTICLES):
            time.sleep(2)
    if failures:
        print("%d article(s) failed; see errors above" % failures, file=sys.stderr)
        return 1
    print("receipts: " + str(LEDGER))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build and publish two canonical-bound Dev.to articles."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="build and validate offline; print Markdown and metadata",
    )
    mode.add_argument(
        "--post",
        action="store_true",
        help="publish through the Dev.to API (requires DEVTO_API_KEY)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="repost even if the canonical URL already has a published receipt",
    )
    args = parser.parse_args(argv)
    try:
        if args.dry_run:
            return dry_run()
        return post_all(force=args.force)
    except ValueError as exc:
        print("validation failed: %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
