You bought residential bandwidth. You configured the gateway. You rotated the exit IP on every request, exactly as the marketing page promised. And you still get `403 Forbidden` after the third call in a sequence.

That is not one bug. It is three independent failure layers stacked on top of each other, and the price of the second layer never appears on the invoice: the **re-run tax**. A residential IP that dies halfway through a login or checkout invalidates every trust cookie bound to it, so all the steps you already paid for are replayed from zero. This article separates the three layers, shows the arithmetic behind the tax, and gives you the exact `curl` commands to prove which layer is biting you.

Everything below is reproducible with the open-source auditor in [github.com/600me/check-proxy-tax](https://github.com/600me/check-proxy-tax) and the [sticky-session loss calculator](https://proxy.mybskm.top/calculator/).

## Layer 1 — ASN reputation: "residential" is not a binary

A site never sees the word "residential". It sees an IP, and the IP resolves to an autonomous system. Anti-bot vendors score that ASN on historical abuse signals, hosting-vs-consumer classification, and how many other tenants are already hammering the same destination from the same block. Two things follow, and both are easy to forget:

- A freshly assigned residential IP on a heavily abused ASN can score worse than an old, quiet datacenter IP.
- A "residential" pool is shared. The IP you were handed ten seconds ago may have been handed to four other crawlers this hour. Reputation is a property of the neighbourhood, not of your account.

This is why the honest first step is to measure your *own* egress before you blame the vendor. On 2026-10-19 the un-proxied audit host on this benchmark resolved to `144.34.225.53`, AS25820 (IT7 Networks / Cluster Logic), a hosting-class network. It returned 100% HTTP 200 against `api.ipify.org` at a median 890 ms total (596 ms of that was TLS). That is a healthy network and a poor bot score at the same time — which is exactly why "it works against a health-check endpoint" tells you nothing about a protected target.

## Layer 2 — Session binding: why a mid-flow IP drop is expensive

Most protected flows are stateful. You solve a challenge, receive a token such as `cf_clearance`, and the edge binds that token to the tuple of IP address, TLS fingerprint and user agent that solved it. Send that cookie from a different exit IP and the edge does not politely refresh it — it rejects the session and may raise the difficulty of the next challenge.

A rotating strategy therefore does not rotate "safely". It rotates into a state where the token you just earned is already invalid, which is why pipelines that look fine on request #1 collapse at request #3. Sticky sessions exist to break that logic: hold one exit IP for the whole flow so the token survives its own TTL.

### What "sticky" actually means per vendor

The window is not a marketing detail; it is the single number that decides whether a 15-minute checkout flow can finish at all. From the vendors' own published documentation (verified October 2026):

| Vendor | Documented sticky window | Practical implication |
|---|---|---|
| Smartproxy (Decodo) | 1–1440 min, default 10 min | Configurable per session ID; long flows are possible if you set the window explicitly. |
| Bright Data | up to 30 min | Enough for checkout and most login flows; residential access itself needs KYC. |
| Oxylabs | up to 24 h | The longest documented window; aimed at corporate, KYC-gated accounts. |
| Apify Residential | ~30 min per `session` ID | Convenient if your actors already run inside Apify. |

Notice what is *not* in that table: success rate. A window is a contract about time. Whether the IP actually survives the window is a property of the pool on the day, and the only way to know is to measure it.

## Layer 3 — JA3 / JA4: the fingerprint that travels with you

Even with a clean ASN and a live sticky session, a request can still be flagged before it is read, because TLS clients announce themselves. The ClientHello advertises cipher suites, extensions, elliptic curves and their order; hashed, that becomes a JA3 (and now JA4) fingerprint. Python's default `requests`/`urllib` stack produces a fingerprint that differs from any real browser, and a site protecting a login endpoint can reject it on sight.

The fix is not another proxy. It is a client that presents a browser-shaped handshake — `curl_cffi`, which mirrors real Chrome/Firefox/Safari TLS signatures, or a browser automation session. Combine a matching fingerprint with a stable residential IP and the two layers stop fighting each other.

## The re-run tax: a three-tier worked example

Here is the arithmetic that surprises most teams. Let `p` be the probability that a sticky IP drops before the flow completes. The number of times a flow must be executed is geometric, so `expected step runs = steps / (1 - p)` and the pure waste ratio is `p / (1 - p)`. Bandwidth is metered on every byte, including the bytes inside a flow that never finished. The table below assumes a fully-loaded per-GB rate of $4.00, 24 active hours a day and 30 days a month.

| Tier | Concurrency | Flow | Steps | Drop rate | Re-run loss | Real GB / month | Monthly cost |
|---|---|---|---|---|---|---|---|
| A · light checkout | 10 | 5 min | 10 | 6% | 6.4% | 132 GB | $526 |
| B · login + cart | 40 | 10 min | 12 | 8% | 8.7% | 387 GB | $1,548 |
| C · long dashboard | 120 | 15 min | 20 | 12% | 13.6% | 1,948 GB | $7,790 |

Now run the same tier B workload with forced per-request rotation and a 35% challenge-failure rate. Because a clearance token can never follow a new IP, every step is effectively cold: `18.46` step executions per completed flow, a **53.8%** re-run loss rate, **548 GB** consumed and **$2,190** per month — roughly **41% more** than the sticky configuration for exactly the same number of completed flows. That difference is not a discount you negotiate. It is traffic you burned on flows that died.

| Same tier-B workload | Step runs / flow | Re-run loss | Real GB / month | Monthly cost |
|---|---|---|---|---|
| Sticky session (8% drop, 10 min window) | 13.04 | 8.7% | 387 GB | $1,548 |
| Per-request rotation (35% challenge failure) | 18.46 | 53.8% | 548 GB | $2,190 |
| **Difference** | +5.42 | +45.1 pts | +161 GB | +$643 |

You can reproduce every one of those numbers, with your own workload, in the [sticky-session & concurrency-loss calculator](https://proxy.mybskm.top/calculator/). The only inputs are concurrency, flow duration, drop rate, steps per flow and price per GB.

## Diagnosing it yourself: five commands

Before you buy anything, prove which layer is failing. These run locally and cost nothing. Replace `USER:PASS@HOST:PORT` with a gateway you are authorised to use.

### 1. Generic HTTP status through the proxy

```bash
curl -sS -o /dev/null -w 'http=%{http_code} connect=%{time_connect}s tls=%{time_appconnect}s total=%{time_total}s\n' \
  --proxy 'http://USER:PASS@HOST:PORT' \
  'https://api.ipify.org?format=json'
```

### 2. Prove the exit IP and its ASN class

```bash
curl -sS --proxy 'http://USER:PASS@HOST:PORT' 'https://api.ipify.org?format=json'; echo
# then classify the IP that came back:
curl -sS 'https://api.ipapi.is/?q=THAT_IP' | python3 -m json.tool | head -40
```

### 3. Confirm one sticky IP survives a full flow window

```bash
# Decodo-style sticky session: fix session_id + session_time, then sample twice.
for i in 1 2 3; do
  curl -sS --proxy 'http://USER-session-abc123-sessionduration-10:PASS@HOST:PORT' \
    'https://api.ipify.org?format=json'; echo
done
# Stable across all three responses = the window held. Three different IPs = it did not.
```

### 4. Compare a browser TLS fingerprint against the default client

```bash
python3 -m pip install curl_cffi
python3 - <<'PY'
from curl_cffi import requests
for impersonate in ("chrome", "safari"):
    r = requests.get("https://api.ipify.org?format=json",
                     impersonate=impersonate, timeout=15)
    print(impersonate, r.status_code, r.text)
PY
```

If `curl_cffi` clears a target that plain `requests` fails, your problem is Layer 3, and a bigger proxy bill will not fix it.

### 5. Measure the drop rate instead of guessing it

```python
import os, statistics, time
from curl_cffi import requests

proxy = "http://USER-session-abc123-sessionduration-15:PASS@HOST:PORT"
ips, lat = [], []
for _ in range(20):
    t = time.perf_counter()
    r = requests.get("https://api.ipify.org?format=json", proxies={"https": proxy},
                     impersonate="chrome", timeout=15)
    lat.append((time.perf_counter() - t) * 1000)
    if r.status_code == 200:
        ips.append(r.json()["ip"])

print("requests:", len(lat), "ok:", len(ips), "unique exits:", len(set(ips)),
      "median ms:", round(statistics.median(lat), 1))
print("empirical drop signal:", 1 - len(ips) / len(lat))
```

That whole script is the core of the CLI in [github.com/600me/check-proxy-tax](https://github.com/600me/check-proxy-tax), which extends it to compute the re-run tax and the monthly ceiling from your own logs.

Feed the observed number into the calculator and you have a defensible monthly budget instead of a vendor slide.

## ASN economics: when residential is genuinely overkill

There is a fourth option that no affiliate program will ever recommend, because it pays nobody: don't buy residential bandwidth at all. A well-behaved `curl_cffi` client on a free Cloudflare WARP or IPv6 egress will clear a large class of targets — public APIs, documentation mirrors, price pages without aggressive bot management — at zero marginal cost. Our own table lists it explicitly as a **$0 commission anchor** and it is recommended for workloads under roughly 1,000 requests a day where a rotating consumer ASN buys you nothing.

> **Decision rule:** pay for residential IPs when you need at least one of rotating consumer ASNs, precise geo-targeting, or a sticky session that holds trust across a multi-step flow. If your workload is small, JA3-sensitive but not ASN-sensitive, the free baseline is not a compromise — it is the correct engineering answer.

## The short version

1. **ASN reputation** decides whether your IP is trusted before the request is even read. Measure your own egress first.
2. **Session binding** decides whether the trust token survives. A mid-flow IP drop voids the token and forces a full replay.
3. **JA3/JA4** decides whether the client looks like a browser. A browser-shaped handshake is not optional on protected endpoints.
4. **The re-run tax** is the number to budget: at an 8% drop rate it is 8.7% overhead; under forced rotation with a 35% challenge failure it is 53.8%.
5. **Sticky windows are contractual.** Check the documented maximum before you design a 15-minute flow — across vendors it ranges from ~30 minutes to 24 hours.

## Put your own numbers in

The [calculator](https://proxy.mybskm.top/calculator/) turns five inputs into the re-run loss rate, the real GB you burn and the monthly bill — sticky versus rotation. Then, if the arithmetic says residential is worth it, check the vendor's self-serve entry price against the nine-dimension matrix on the home page.

- **[Open the sticky-session calculator →](https://proxy.mybskm.top/calculator/)**
- **[Run the open-source auditor: github.com/600me/check-proxy-tax →](https://github.com/600me/check-proxy-tax)**
- **[Try Smartproxy (Decodo) residential — 100 MB trial ↗](https://go.272738.xyz/smartproxy?src=devto_sticky_guide)**

*Further reading on this site: the [9-dimension public commercial & policy matrix](https://proxy.mybskm.top/#matrix) and the [live probe telemetry](https://proxy.mybskm.top/#telemetry). Sister projects: [the 403 tax on scraping APIs](https://scrape.mybskm.top/blog/403-tax.html) and [the H100 rental trap](https://gpu.mybskm.top/blog/h100-rental-trap.html).*

**FTC affiliate disclosure:** this article contains affiliate links. If you buy a residential proxy plan after clicking the Smartproxy (Decodo) link, we may earn a commission at no extra cost to you. Nothing in the analysis, the arithmetic or the ordering of the tables depends on that. The open-source `curl_cffi` baseline it recommends earns us nothing, and the diagnostic commands run on your machines, not ours.
