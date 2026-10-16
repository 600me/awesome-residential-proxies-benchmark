#!/usr/bin/env python3
"""Read public intent leads; print matches, never post or send messages.

python3 sniper_daemon.py --once       # one real public-feed inspection
python3 sniper_daemon.py --dry-run    # offline fixtures + atomic temp-state check
python3 sniper_daemon.py              # 1800s + 0..180s jitter between rounds

State lives beside this file. Deployment preserves it. stdout is JSONL, captured
by systemd's journal. Dry-run uses a temporary file, not production seen IDs.
Sources: Reddit JSON + Hacker News Algolia API (https://hn.algolia.com/api).
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
import urllib.request


STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
DEFAULT_SOURCES = (
    "https://www.reddit.com/r/webscraping/new.json?limit=50&raw_json=1",
    "https://hn.algolia.com/api/v1/search_by_date?query=proxy&tags=(story,comment)&hitsPerPage=50",
)
MAX_SEEN = 500
MAX_BYTES = 2 * 1024 * 1024
PATTERNS = {
    "workload": re.compile(r"\b(?:scrap(?:e|er|ers|ing)|crawl(?:er|ers|ing)?|multi[- ]?accounts?|(?:residential|rotating)\s+prox(?:y|ies))\b", re.I),
    "pain": re.compile(r"\b(?:403|429|cloudflare|block(?:ed|ing|s)?|bann?ed|captcha|rate[- ]?limit(?:ed|ing)?|fail(?:ed|ing|ure)?|timeouts?)\b", re.I),
    "buying_intent": re.compile(r"\b(?:recommend(?:ation|ations)?|looking for|need|best|alternative|provider|buy|budget|residential|switch(?:ing)?)\b", re.I),
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


def fetch_posts(source):
    request = urllib.request.Request(source, headers={
        "User-Agent": "kais-proxy-intent-monitor/1.0 (public read-only feed)",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(request, timeout=10) as response:
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("feed exceeds 2 MiB")
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
    if all(evidence.values()):
        return {name: match.group(0) for name, match in evidence.items()}
    return None


def inspect_round(sources, state_path=STATE_PATH, fixture_posts=None):
    state = load_state(state_path)
    if state is None:
        return
    seen = list(state["seen_post_ids"])
    seen_set = set(seen)
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
                if evidence:
                    log("lead", post_id=post_id, title=post["title"],
                        url=("https://news.ycombinator.com/item?id=" + post["id"] if platform == "hackernews"
                             else "https://www.reddit.com/comments/" + post["id"] + "/"),
                        evidence=evidence, dry_run=fixture_posts is not None)
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
        {"id": "demo_low", "title": "My Python scraper tutorial", "selftext": "Learning JSON"},
        {"id": "demo_other", "title": "Need the best laptop recommendation", "selftext": ""},
        {"id": "demo_proxy", "title": "Need an OpenCode proxy; provider blocking model requests", "selftext": ""},
    ]
    log("dry_run", rules={key: pattern.pattern for key, pattern in PATTERNS.items()},
        policy="all three signals required; offline fixtures; production state unchanged")
    with tempfile.TemporaryDirectory(prefix="proxy-sniper-dry-") as directory:
        path = os.path.join(directory, "state.json")
        inspect_round(["fixture://reddit"], path, posts)
        first = load_state(path)
        assert first["last_round"] == {"checked": 4, "matched": 1, "source_errors": 0}
        inspect_round(["fixture://reddit"], path, posts)
        assert load_state(path)["last_round"]["matched"] == 0
        save_state(path, {"seen_post_ids": ["reddit:test_" + str(index) for index in range(600)]})
        assert len(load_state(path)["seen_post_ids"]) == MAX_SEEN
    log("dry_run_pass", matching=True, deduplication=True, atomic_state=True, rolling_limit=MAX_SEEN)


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
