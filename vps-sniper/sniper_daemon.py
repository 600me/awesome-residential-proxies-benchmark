#!/usr/bin/env python3
"""Read public matrix intent leads; persist matches, never post or send messages.

python3 sniper_daemon.py --once       # one real public-feed inspection
python3 sniper_daemon.py --dry-run    # offline fixtures + atomic temp-state check
python3 sniper_daemon.py              # 1800s + 0..180s jitter between rounds

State and matched_leads.jsonl live beside this file. Deployment preserves both.
stdout is JSONL, captured by systemd's journal. Dry-run uses temporary files.
Sources: Reddit JSON (public RSS fallback) + Hacker News Algolia API.
--source URL may be repeated to override either public JSON feed format.
Public feeds may deny unauthenticated access; errors are logged, never bypassed.
"""

import argparse
import html
import json
import os
import random
import re
import tempfile
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
LEADS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "matched_leads.jsonl")
USER_AGENT = "linux:kais-matrix-intent-monitor:v2.0 (read-only public feed; contact: https://proxy.mybskm.top/)"
DEFAULT_SOURCES = (
    "https://hn.algolia.com/api/v1/search_by_date?query=proxy&tags=(story,comment)&hitsPerPage=50",
    "https://hn.algolia.com/api/v1/search_by_date?query=gpu+cloud&tags=(story,comment)&hitsPerPage=50",
    "https://hn.algolia.com/api/v1/search_by_date?query=stripe+banned&tags=(story,comment)&hitsPerPage=50",
    "https://hn.algolia.com/api/v1/search_by_date?query=scraping+cloudflare&tags=(story,comment)&hitsPerPage=50",
    "https://www.reddit.com/r/webscraping/new.json?limit=50&raw_json=1",
)
MAX_SEEN = 500
MAX_BYTES = 2 * 1024 * 1024
PATTERNS = {
    "pain": re.compile(r"\b(?:403|429|cloudflare|block(?:ed|ing|s)?|bann?ed|captcha|rate[- ]?limit(?:ed|ing)?|fail(?:ed|ing|ure)?|timeouts?|expensive|cost(?:s|ly)?|pricing|unavailable|suspend(?:ed)?|reject(?:ed)?|shut down)\b", re.I),
    "buying_intent": re.compile(r"\b(?:recommend(?:ation|ations)?|looking for|need(?:s|ed)?|best|alternatives?|providers?|buy|budget|switch(?:ing)?|suggest(?:ion|ions)?|anyone|how (?:can|do|to)|help)\b", re.I),
}
CATEGORY_PATTERNS = {
    "proxy": re.compile(r"\b(?:prox(?:y|ies)|multi[- ]?accounts?)\b", re.I),
    "gpu": re.compile(r"\b(?:gpus?|cuda|runpod|vast\.?ai|cloud compute|(?:model|llm) inference)\b", re.I),
    "payments": re.compile(r"\b(?:stripe|paypal|payments?|payouts?|merchant accounts?|payment processors?|paddle|lemonsqueezy)\b", re.I),
    "scraping": re.compile(r"\b(?:scrap(?:e|er|ers|ing)|crawl(?:er|ers|ing)?|apify|scraperapi)\b", re.I),
}
RECOMMENDED_TARGETS = {
    "proxy": "https://proxy.mybskm.top/",
    "gpu": "https://gpu.mybskm.top/",
    "payments": "https://pay.mybskm.top/",
    "scraping": "https://scrape.mybskm.top/",
}


def log(event, **fields):
    print(json.dumps({"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      "event": event, **fields}, ensure_ascii=False), flush=True)


def normalize_seen(values):
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise ValueError("seen_post_ids must be a list of strings")
    # Keep the latest occurrence of an ID in order, capped at 500.
    return list(dict.fromkeys(reversed(values)))[::-1][-MAX_SEEN:]


def load_state(path):
    try:
        with open(path, encoding="utf-8") as stream:
            state = json.load(stream)
        if not isinstance(state, dict):
            raise ValueError("state must be an object")
        state["seen_post_ids"] = normalize_seen(state.get("seen_post_ids", []))
        return state
    except FileNotFoundError:
        return {"seen_post_ids": []}
    except (OSError, ValueError, TypeError) as error:
        log("state_error", error=str(error), action="skip round; preserve existing state")
        return None


def save_state(path, state):
    state = {**state, "seen_post_ids": normalize_seen(state["seen_post_ids"])}
    # Same directory guarantees os.replace stays on the same filesystem.
    fd, temporary = tempfile.mkstemp(prefix=".state-", suffix=".tmp", dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def fetch_bytes(source):
    request = urllib.request.Request(source, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json, application/atom+xml;q=0.9",
    })
    with urllib.request.urlopen(request, timeout=10) as response:
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("feed exceeds 2 MiB")
    return raw


def parse_reddit_rss(raw):
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(raw)
    if root.tag != "{http://www.w3.org/2005/Atom}feed":
        raise ValueError("invalid Reddit Atom feed")
    posts = []
    for entry in root.findall("atom:entry", namespace):
        post_id = entry.findtext("atom:id", default="", namespaces=namespace)
        if not re.fullmatch(r"t3_[A-Za-z0-9]+", post_id):
            raise ValueError("invalid Reddit Atom post ID")
        content = entry.findtext("atom:content", default="", namespaces=namespace)
        posts.append({"id": post_id[3:], "platform": "reddit",
                      "title": entry.findtext("atom:title", default="", namespaces=namespace),
                      "selftext": html.unescape(re.sub(r"<[^>]+>", " ", content))})
    return posts


def fetch_posts(source):
    try:
        raw = fetch_bytes(source)
    except urllib.error.HTTPError as error:
        # Reddit's public Atom endpoint can remain available when JSON is denied.
        # One ordinary RSS request per round; never retry/bypass a denied RSS feed.
        if error.code != 403 or not re.match(r"https://www\.reddit\.com/r/[A-Za-z0-9_]+/new\.json(?:\?|$)", source):
            raise
        fallback = source.split("/new.json", 1)[0] + "/.rss"
        posts = parse_reddit_rss(fetch_bytes(fallback))
        log("source_fallback", source=source, http_status=403, fallback=fallback,
            fallback_status=200, posts=len(posts))
        return posts
    payload = json.loads(raw)
    if "hits" in payload:
        if not isinstance(payload["hits"], list):
            raise ValueError("invalid Hacker News hits")
        posts = []
        for hit in payload["hits"]:
            post_id = hit["objectID"]
            if not isinstance(post_id, str) or not post_id.isdigit():
                raise ValueError("invalid Hacker News item ID")
            body = (hit.get("story_text") or "") + "\n" + (hit.get("comment_text") or "")
            posts.append({"id": post_id, "platform": "hackernews",
                          "title": hit.get("title") or hit.get("story_title") or "Hacker News discussion",
                          "selftext": html.unescape(re.sub(r"<[^>]+>", " ", body))})
        return posts
    children = payload["data"]["children"]
    if not isinstance(children, list):
        raise ValueError("invalid feed children")
    posts = []
    for child in children:
        post = child["data"]
        if not isinstance(post, dict) or not isinstance(post.get("id"), str):
            raise ValueError("invalid post")
        if not re.fullmatch(r"[A-Za-z0-9_]+", post["id"]):
            raise ValueError("invalid post ID")
        posts.append(post)
    return posts


def match_post(post):
    if post.get("stickied") or post.get("removed_by_category"):
        return None
    title, body = post.get("title", ""), post.get("selftext", "")
    if not isinstance(title, str) or not isinstance(body, str):
        return None
    text = title + "\n" + body
    evidence = {name: pattern.search(text) for name, pattern in PATTERNS.items()}
    categories = {name: match.group(0) for name, pattern in CATEGORY_PATTERNS.items()
                  if (match := pattern.search(text))}
    if categories and all(evidence.values()):
        category = next(iter(categories))
        return {"category": category, "categories": list(categories),
                "recommended_target": RECOMMENDED_TARGETS[category],
                "evidence": {**{name: match.group(0) for name, match in evidence.items()},
                             "categories": categories}}
    return None


def load_lead_ids(path):
    try:
        with open(path, encoding="utf-8") as stream:
            return {json.loads(line)["post_id"] for line in stream if line.strip()}
    except FileNotFoundError:
        return set()


def append_lead(path, lead):
    # One O_APPEND write keeps a complete JSON line contiguous on the VPS filesystem.
    # Persist before stdout/state; the ledger also deduplicates after a state crash.
    record = (json.dumps(lead, ensure_ascii=False) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        original_size = os.fstat(fd).st_size
        if os.write(fd, record) != len(record):
            os.ftruncate(fd, original_size)
            raise OSError("incomplete lead append")
        os.fsync(fd)
    finally:
        os.close(fd)


def inspect_round(sources, state_path=STATE_PATH, fixture_posts=None, leads_path=LEADS_PATH):
    state = load_state(state_path)
    if state is None:
        return
    seen = list(state["seen_post_ids"])
    seen_set = set(seen)
    lead_ids = load_lead_ids(leads_path)
    checked, matched, errors = 0, 0, 0
    for source in sources:
        try:
            posts = fixture_posts if fixture_posts is not None else fetch_posts(source)
            # Both default feeds return newest first; evict oldest IDs first.
            for post in reversed(posts):
                platform = post.get("platform", "reddit")
                post_id = platform + ":" + post["id"]
                if post_id in seen_set:
                    continue
                checked += 1
                evidence = match_post(post)
                if evidence and post_id not in lead_ids:
                    lead = {"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "event": "lead", "post_id": post_id, "title": post["title"],
                            "url": ("https://news.ycombinator.com/item?id=" + post["id"] if platform == "hackernews"
                                    else "https://www.reddit.com/comments/" + post["id"] + "/"),
                            "source": source, **evidence, "dry_run": fixture_posts is not None}
                    append_lead(leads_path, lead)
                    lead_ids.add(post_id)
                    print(json.dumps(lead, ensure_ascii=False), flush=True)
                    matched += 1
                seen.append(post_id)
                seen_set.add(post_id)
        except Exception as error:
            # One failed feed must not prevent the other feeds or the next round.
            errors += 1
            log("source_error", source=source, error=str(error), retry="next round")
    state["seen_post_ids"] = normalize_seen(seen)
    state["last_checked_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    state["last_round"] = {"checked": checked, "matched": matched, "source_errors": errors}
    save_state(state_path, state)
    if fixture_posts is not None:
        log("state_update", path="temporary dry-run state", atomic_replace=True,
            seen_count=len(state["seen_post_ids"]), **state["last_round"])
    elif errors or checked or matched:
        log("round", seen_count=len(state["seen_post_ids"]), **state["last_round"])


def dry_run():
    posts = [
        {"id": "demo_high", "title": "Scraper blocked by Cloudflare 403; need residential proxy recommendations", "selftext": "100GB monthly budget"},
        {"id": "demo_gpu", "title": "GPU cloud too expensive; need an alternative provider", "selftext": "CUDA model inference"},
        {"id": "demo_pay", "title": "Stripe banned my merchant account; looking for payment alternatives", "selftext": ""},
        {"id": "demo_scrape", "title": "Scraping blocked by Cloudflare; need a scraping API recommendation", "selftext": ""},
        {"id": "demo_low", "title": "My Python scraper tutorial", "selftext": "Learning JSON"},
        {"id": "demo_other", "title": "Need the best laptop recommendation", "selftext": ""},
        {"id": "demo_proxy", "title": "Need an OpenCode proxy; provider blocking model requests", "selftext": ""},
        {"id": "demo_sticky", "title": "Need GPU cloud alternatives; costs too high", "selftext": "", "stickied": True},
    ]
    log("dry_run", rules={key: pattern.pattern for key, pattern in PATTERNS.items()},
        categories={key: pattern.pattern for key, pattern in CATEGORY_PATTERNS.items()},
        policy="category + pain + intent required; offline fixtures; production files unchanged")
    with tempfile.TemporaryDirectory(prefix="proxy-sniper-dry-") as directory:
        path = os.path.join(directory, "state.json")
        leads_path = os.path.join(directory, "matched_leads.jsonl")
        inspect_round(["fixture://reddit"], path, posts, leads_path)
        first = load_state(path)
        assert first["last_round"] == {"checked": 8, "matched": 5, "source_errors": 0}
        with open(leads_path, encoding="utf-8") as stream:
            leads = [json.loads(line) for line in stream]
        assert {lead["category"] for lead in leads} == set(CATEGORY_PATTERNS)
        assert all(lead["recommended_target"] == RECOMMENDED_TARGETS[lead["category"]] for lead in leads)
        assert next(lead for lead in leads if lead["post_id"] == "reddit:demo_high")["categories"] == ["proxy", "scraping"]
        inspect_round(["fixture://reddit"], path, posts, leads_path)
        assert load_state(path)["last_round"]["matched"] == 0
        # A crash after ledger fsync but before saving seen IDs must not duplicate.
        save_state(path, {"seen_post_ids": []})
        inspect_round(["fixture://reddit"], path, posts, leads_path)
        assert load_state(path)["last_round"]["matched"] == 0
        with open(leads_path, encoding="utf-8") as stream:
            assert len(stream.readlines()) == 5
        # Atom fallback preserves the same Reddit ID and plain-text matching.
        atom = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <id>t3_rss123</id><title>Need scraping help</title>
          <content type="html">&lt;p&gt;Cloudflare blocked my scraper&lt;/p&gt;</content>
        </entry></feed>'''
        rss_post = parse_reddit_rss(atom)[0]
        assert rss_post["id"] == "rss123"
        assert match_post(rss_post)["category"] == "scraping"
        save_state(path, {"seen_post_ids": ["reddit:test_" + str(index) for index in range(600)]})
        assert len(load_state(path)["seen_post_ids"]) == MAX_SEEN
    log("dry_run_pass", categories=4, matching=True, deduplication=True, atomic_state=True,
        atomic_lead_append=True, restart_deduplication=True, reddit_rss=True, rolling_limit=MAX_SEEN)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--once", action="store_true", help="inspect real feeds once, then exit")
    parser.add_argument("--dry-run", action="store_true", help="one offline simulation; production state unchanged")
    parser.add_argument("--source", action="append", help="public Reddit or HN Algolia JSON URL; repeat to override defaults")
    parser.add_argument("--interval", type=int, default=1800, help="seconds between rounds (default: 1800)")
    args = parser.parse_args()
    if args.interval < 1:
        parser.error("--interval must be positive")
    if args.dry_run:
        dry_run()
        return 0
    while True:
        try:
            inspect_round(args.source or DEFAULT_SOURCES)
        except Exception as error:
            log("round_error", error=str(error), retry="next round")
        if args.once:
            return 0
        time.sleep(args.interval + random.uniform(0, args.interval * 0.1))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        pass
