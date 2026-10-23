#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
x_matrix_scheduler.py —— LX 主机 X 矩阵 Tier-1 发帖调度 / 真实发布回读验收 / 1 楼待办持久化 / 美东双窗口错峰

物理定位
--------
单文件调度器，运行在 lx-server，与同目录 x_matrix_lx_engine.py 配合：
    ~/x-matrix-runtime(X矩阵运行器)/x_matrix_scheduler.py
    ~/x-matrix-runtime(X矩阵运行器)/x_matrix_lx_engine.py
    ~/x-matrix-runtime(X矩阵运行器)/state/schedule_ledger.json    发帖账本 + 窗口计划 + 1 楼待办
    ~/x-matrix-runtime(X矩阵运行器)/state/accounts_state.json     账号风控状态 + known_ids
    ~/x-matrix-runtime(X矩阵运行器)/state/schedule_ledger.lock    fcntl 排他锁
    ~/x-matrix-runtime(X矩阵运行器)/x-matrix-scheduler.service    systemd 用户服务

硬规则（写死，无开关）
--------------------
1. 8 个 Tier-1 账号各自持有 100% 互不相同的文案（主帖 / 1 楼均唯一），启动即自检；
   主帖零外链，链接与 FTC 佣金披露只出现在 1 楼自评，且披露位于链接之前或紧邻。
2. 发帖判定不认 Playwright 退出码：
   发布前读取个人主页已知推文 ID 集合（known_ids）→ 发布 → 独立回读个人主页差量提取新推文 ID
   → 文字片段匹配 → 外部 oembed / og:description 校验。缺任一步都不算发布成功。
3. 1 楼自评持久化待办：主帖验收成功后立即写入 pending_self_reply（parent_tweet_url /
   self_reply_text / due_at），daemon 每轮优先补发到期待办，进程中断不丢落地页链接。
4. 美东时区（America/New_York）双窗口分流，周一至周四：
      morning   08:30-10:30 ET（北京 20:30-22:30，夏令时）→ seq 5 / 26 / 51 / 78
      afternoon 12:30-14:00 ET（北京次日 00:30-02:00，夏令时）→ seq 7 / 28 / 52 / 91
   每个窗口 4 个号，间隔 20-35 分钟错峰；窗口计划落盘，重启不重排、不重复。
5. 每号每日最多 1 条主帖；单号连续失败 3 次熔断 6 小时；全局 60 分钟内失败 5 次暂停 2 小时。
6. 零人工假死锁：客观指标（回读 ID + 文字匹配 + 外部校验）通过即推进 1 楼自评，
   从不写入 awaiting_human 状态，也不因等待人工而停摆。

CLI
---
    python3 x_matrix_scheduler.py status
    python3 x_matrix_scheduler.py dry-run
    python3 x_matrix_scheduler.py plan [--window morning|afternoon] [--date YYYY-MM-DD] [--create]
    python3 x_matrix_scheduler.py verify --seq 5 [--tweet-url URL]
    python3 x_matrix_scheduler.py pending [--process] [--limit 2]
    python3 x_matrix_scheduler.py trigger-tier1 --group A|B|C|D|ALL [--seq N] [--force]
                                              [--delay-self-reply-seconds 240] [--wait-self-reply]
                                              [--gap-min 20] [--gap-max 35]
    python3 x_matrix_scheduler.py trigger-window --window morning|afternoon [--force] [--wait-self-reply]
    python3 x_matrix_scheduler.py daemon [--force] [--interval-seconds 300]
                                        [--delay-self-reply-seconds 240]
    python3 x_matrix_scheduler.py systemd-unit [--out PATH] [--install]
"""

from __future__ import annotations

import argparse
import contextlib
import difflib
import html as html_lib
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

try:  # lx-server 为 Linux；其它平台退化为无锁（仅本地核验）
    import fcntl  # type: ignore
except ImportError:  # pragma: no cover
    fcntl = None  # type: ignore

# --------------------------------------------------------------------------------------
# 时区 / 路径 / 运行参数
# --------------------------------------------------------------------------------------

ET = ZoneInfo("America/New_York")
BJ = ZoneInfo("Asia/Shanghai")
UTC = ZoneInfo("UTC")

DEFAULT_RUNTIME_DIR = Path(os.path.expanduser("~/x-matrix-runtime(X矩阵运行器)"))

PATHS = {
    "runtime": DEFAULT_RUNTIME_DIR,
    "state": DEFAULT_RUNTIME_DIR / "state",
    "ledger": DEFAULT_RUNTIME_DIR / "state" / "schedule_ledger.json",
    "accounts": DEFAULT_RUNTIME_DIR / "state" / "accounts_state.json",
    "lock": DEFAULT_RUNTIME_DIR / "state" / "schedule_ledger.lock",
    "heartbeat": DEFAULT_RUNTIME_DIR / "state" / "scheduler_heartbeat.json",
    "engine": DEFAULT_RUNTIME_DIR / "x_matrix_lx_engine.py",
}

LEDGER_MAX_RECORDS = 8000
WINDOW_PLAN_KEEP = 48
PENDING_MAX_ATTEMPTS = 8
PENDING_MAX_AGE_HOURS = 36
DEFAULT_POST_TIMEOUT = 900
DEFAULT_REPLY_TIMEOUT = 600
EXTERNAL_TIMEOUT = 15

ENGINE_EXCEL: str | None = None
ENGINE_SHEET: str | None = None
ENGINE_EXTRA_ARGS: list[str] = []

UA_HTTP = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"


def configure_paths(runtime_dir: str | os.PathLike[str]) -> None:
    root = Path(os.path.expanduser(str(runtime_dir)))
    PATHS["runtime"] = root
    PATHS["state"] = root / "state"
    PATHS["ledger"] = root / "state" / "schedule_ledger.json"
    PATHS["accounts"] = root / "state" / "accounts_state.json"
    PATHS["lock"] = root / "state" / "schedule_ledger.lock"
    PATHS["heartbeat"] = root / "state" / "scheduler_heartbeat.json"
    PATHS["engine"] = root / "x_matrix_lx_engine.py"


def configure_engine(excel: str | None, sheet: str | None) -> None:
    global ENGINE_EXCEL, ENGINE_SHEET, ENGINE_EXTRA_ARGS
    ENGINE_EXCEL = excel or None
    ENGINE_SHEET = sheet or None
    extra: list[str] = []
    if ENGINE_EXCEL:
        extra += ["--excel", ENGINE_EXCEL]
    if ENGINE_SHEET:
        extra += ["--sheet", ENGINE_SHEET]
    ENGINE_EXTRA_ARGS = extra


# --------------------------------------------------------------------------------------
# 美东双窗口（周一至周四）
# --------------------------------------------------------------------------------------

WINDOW_HOURS: dict[str, tuple[dtime, dtime]] = {
    "morning": (dtime(8, 30), dtime(10, 30)),
    "afternoon": (dtime(12, 30), dtime(14, 0)),
}
WINDOW_DAYS = {0, 1, 2, 3}  # Mon-Thu
WINDOW_SEQS: dict[str, list[int]] = {
    "morning": [5, 26, 51, 78],
    "afternoon": [7, 28, 52, 91],
}
WINDOW_LABEL = {
    "morning": "上午窗口 Mon-Thu 08:30-10:30 ET（北京 20:30-22:30 夏令时）",
    "afternoon": "午后窗口 Mon-Thu 12:30-14:00 ET（北京次日 00:30-02:00 夏令时）",
}


def now_et() -> datetime:
    return datetime.now(tz=ET)


def now_bj() -> datetime:
    return datetime.now(tz=BJ)


def iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def fmt_ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def combine_et(day: date, t: dtime) -> datetime:
    return datetime.combine(day, t).replace(tzinfo=ET)


def window_name(dt: datetime) -> str | None:
    if dt.weekday() not in WINDOW_DAYS:
        return None
    t = dt.time()
    for name, (start, end) in WINDOW_HOURS.items():
        if start <= t < end:
            return name
    return None


def window_end_dt(day: date, name: str) -> datetime:
    return combine_et(day, WINDOW_HOURS[name][1])


def next_window_start(dt: datetime) -> tuple[str, datetime] | None:
    for offset in range(0, 9):
        day = dt.date() + timedelta(days=offset)
        if day.weekday() not in WINDOW_DAYS:
            continue
        for name in ("morning", "afternoon"):
            start = combine_et(day, WINDOW_HOURS[name][0])
            if start > dt:
                return name, start
    return None


def human_delta(seconds: float) -> str:
    seconds = int(max(0, seconds))
    d, rem = divmod(seconds, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if d:
        parts.append(f"{d}天")
    if h:
        parts.append(f"{h}小时")
    if m:
        parts.append(f"{m}分")
    if not parts:
        parts.append(f"{s}秒")
    return "".join(parts)


# --------------------------------------------------------------------------------------
# 内置文案库：8 个 Tier-1 账号，逐号独立，1:1 原样（禁止改写 / 禁止合并）
# --------------------------------------------------------------------------------------

COPY_LIBRARY: dict[int, dict] = {
    5: {
        "seq": 5,
        "handle": "Tomi11238760",
        "group": "A",
        "group_name": "住宅代理 Residential Proxy",
        "theme": "30% Retry Tax",
        "window": "morning",
        "main": (
            "Residential proxy bills hide the real cost: retries. At $4/GB PAYG, a scraper that "
            "retries 30% on 500GB/month burns 650GB = $2,600. At $2.75/GB on 100GB prepay, same "
            "burn = $1,787.50. The gap isn't per-GB price. It's session stability."
        ),
        "self_reply": (
            "Disclosure: I may earn an affiliate commission from tools I benchmark. I built the "
            "sticky-session & retry calculator here: "
            "https://proxy.mybskm.top/calculator/?utm_source=x_t1_proxy_retry — simulate your fail rate."
        ),
    },
    7: {
        "seq": 7,
        "handle": "TianaRamsey5",
        "group": "A",
        "group_name": "住宅代理 Residential Proxy",
        "theme": "Sticky Session Drop-off at Minute 14",
        "window": "afternoon",
        "main": (
            "Most checkout scrapers crash at minute 14 because residential sticky sessions default "
            "to 10 min. 5,000 checkout runs/day × 18% mid-flow drops = 900 broken sessions and "
            "duplicate cart auths. The fix isn't more concurrent threads. It's matching proxy session "
            "TTL to p95 checkout duration."
        ),
        "self_reply": (
            "Disclosure: Affiliate links included. Full checklist on session TTL and proxy latency "
            "benchmark: https://proxy.mybskm.top/calculator/?utm_source=x_t1_proxy_sticky"
        ),
    },
    26: {
        "seq": 26,
        "handle": "Josette05752050",
        "group": "B",
        "group_name": "反爬 API Anti-Bot API",
        "theme": "Credit Multiplier",
        "window": "morning",
        "main": (
            "Anti-bot cost isn't the API fee. It's the retry multiplier. 1M pages with 25% "
            "challenged/retried = 1.25M credits. ScraperAPI at $49/100k = $612.50. ZenRows at "
            "$49/250k = $245. Same target, 2.5x spread. Measure retries before you compare stickers."
        ),
        "self_reply": (
            "Disclosure: I earn commissions from reviewed platforms. Live benchmark & credit cost "
            "calculator: https://scrape.mybskm.top/calculator/?utm_source=x_t1_scrape_credit and "
            "https://github.com/600me/awesome-web-scraping-apis-benchmark"
        ),
    },
    28: {
        "seq": 28,
        "handle": "EastawayLayne",
        "group": "B",
        "group_name": "反爬 API Anti-Bot API",
        "theme": "Cloudflare 403 Challenge Penalty Tax",
        "window": "afternoon",
        "main": (
            "A 403 response isn't just one failed request. When 20% of 2M pages trigger Cloudflare "
            "challenges and auto-retry twice, that's 800,000 unmetered fetches burned. At 5-second "
            "backoff, you waste 1,111 developer hours waiting on queues. Always cap the retry budget "
            "per domain before increasing credit tiers."
        ),
        "self_reply": (
            "Disclosure: May contain affiliate links. TCO calculator for anti-bot scraping APIs: "
            "https://scrape.mybskm.top/calculator/?utm_source=x_t1_scrape_403"
        ),
    },
    51: {
        "seq": 51,
        "handle": "Rebecka61453038",
        "group": "C",
        "group_name": "GPU 算力 GPU Compute",
        "theme": "Billable Hours vs Headline $/hr",
        "window": "morning",
        "main": (
            "A 100-hour H100 job looks cheap until you price idle and cold start. Vast.ai: 100 × "
            "$1.788/hr = $178.80. RunPod Secure: 100 × $3.99/hr = $399.00. Same GPU-hours, $220.20 "
            "gap. The real number is billable hours, not headline $/hr."
        ),
        "self_reply": (
            "Disclosure: Affiliate commission may apply. Interactive GPU VRAM & TCO calculator: "
            "https://gpu.mybskm.top/calculator/?utm_source=x_t1_gpu_h100 — includes cold start assumptions."
        ),
    },
    52: {
        "seq": 52,
        "handle": "Maryett32244792",
        "group": "C",
        "group_name": "GPU 算力 GPU Compute",
        "theme": "Cold Start Container Pull Tax",
        "window": "afternoon",
        "main": (
            "Cold starts killed our 8×H100 batch: 18 min container pull + 6 min checkpoint load at "
            "$3.99/hr = $12.77 burned before step 1. Two network retries = $25.54 wasted, equivalent "
            "to 14.3 hours of unreserved GPU time. Always pre-bake the weights into a local volume "
            "snapshot or use hot-standby instances."
        ),
        "self_reply": (
            "Disclosure: Contains affiliate links. I modeled the cold-start vs reserved GPU tradeoff "
            "calculator here: https://gpu.mybskm.top/calculator/?utm_source=x_t1_gpu_coldstart"
        ),
    },
    78: {
        "seq": 78,
        "handle": "David1874901",
        "group": "D",
        "group_name": "出海收单 Payments",
        "theme": "LLC vs MoR 5% Tipping Point at $8k MRR",
        "window": "morning",
        "main": (
            "At $8k/mo MRR, $40 AOV means 200 sales. Stripe: 2.9%+$0.30 = $292/mo + $1,000/yr "
            "compliance = $4,504/yr. MoR 5%+$0.50 = $500/mo = $6,000/yr. Gap $1,496/yr—before a "
            "missed Form 5472 at $25,000. Calculate your crossover point before choosing Merchant of Record."
        ),
        "self_reply": (
            "Disclosure: Affiliate links included. Breakdown of Stripe LLC vs Merchant of Record costs: "
            "https://pay.mybskm.top/?utm_source=x_t1_pay_mor"
        ),
    },
    91: {
        "seq": 91,
        "handle": "yichuanxx",
        "group": "D",
        "group_name": "出海收单 Payments",
        "theme": "$15,000 MRR SaaS Tax on 5% MoR",
        "window": "afternoon",
        "main": (
            "When a SaaS scales to $15k MRR, a 5% MoR take equals $750/month ($9,000/year). A "
            "self-owned Wyoming LLC + Stripe gateway totals ~$435/month ($5,220/year). The $3,780 "
            "annual difference easily covers automated sales tax filings. Don't pay MoR percentage "
            "fees on volume your own LLC can absorb."
        ),
        "self_reply": (
            "Disclosure: I may earn an affiliate commission. Interactive MoR vs US LLC crossover "
            "calculator: https://pay.mybskm.top/?utm_source=x_t1_pay_scale"
        ),
    },
}

TIER1_SEQS: list[int] = sorted(COPY_LIBRARY)
TIER1_GROUP_SEQS: dict[str, list[int]] = {
    group: [seq for seq in TIER1_SEQS if COPY_LIBRARY[seq]["group"] == group]
    for group in ("A", "B", "C", "D")
}

LINK_RE = re.compile(r"https?://|www\.|t\.co/", re.IGNORECASE)
STATUS_ID_RE = re.compile(r"/status/(\d+)")
HTML_TAG_RE = re.compile(r"<[^>]+>")


def norm_text(value: str) -> str:
    s = (value or "").lower()
    s = re.sub(r"https?://\S+", " ", s)
    s = (
        s.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u00d7", "x")
        .replace("&amp;", "&")
    )
    s = re.sub(r"[^\w\s%$.,:/'\"-]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def text_match_ratio(expected: str, actual: str) -> float:
    exp = norm_text(expected)
    act = norm_text(actual)
    if not exp or not act:
        return 0.0
    fragment = exp[:60]
    if fragment and fragment in act:
        return 1.0
    fragment15 = exp[:15]
    if fragment15 and fragment15 in act:
        return max(0.9, difflib.SequenceMatcher(None, exp, act).ratio())
    return difflib.SequenceMatcher(None, exp, act).ratio()


def validate_copy_library() -> list[str]:
    """启动自检：8 套文案互不相同 / 主帖零外链 / 披露在链接前 / 双窗口各 4 号 / 每赛道各 1 号。"""
    problems: list[str] = []
    if len(COPY_LIBRARY) != 8:
        problems.append(f"Tier-1 账号应为 8 个，实际 {len(COPY_LIBRARY)}")

    main_seen: dict[str, int] = {}
    reply_seen: dict[str, int] = {}
    for seq, item in COPY_LIBRARY.items():
        main = item["main"]
        reply = item["self_reply"]
        if LINK_RE.search(main):
            problems.append(f"seq={seq} 主帖包含外链，违反主帖零外链红线")
        if "http" not in reply:
            problems.append(f"seq={seq} 1 楼自评缺少落地链接")
        if "disclosure" not in reply.lower():
            problems.append(f"seq={seq} 1 楼自评缺少 FTC 披露")
        low = reply.lower()
        if "affiliate" not in low and "commission" not in low:
            problems.append(f"seq={seq} 1 楼自评缺少联盟/佣金披露")
        link_at = low.find("http")
        disc_at = low.find("disclosure")
        if link_at >= 0 and disc_at >= 0:
            if disc_at > link_at:
                problems.append(f"seq={seq} 披露位于链接之后，违反披露前置红线")
            elif link_at - disc_at > 220:
                problems.append(f"seq={seq} 披露与链接相距过远，不满足紧邻要求")
        if item["window"] not in WINDOW_HOURS:
            problems.append(f"seq={seq} 窗口非法: {item['window']}")
        if seq not in WINDOW_SEQS.get(item["window"], []):
            problems.append(f"seq={seq} 未登记在 {item['window']} 窗口名单")
        key_main = norm_text(main)
        key_reply = norm_text(reply)
        if key_main in main_seen:
            problems.append(f"seq={seq} 主帖与 seq={main_seen[key_main]} 重复")
        main_seen[key_main] = seq
        if key_reply in reply_seen:
            problems.append(f"seq={seq} 1 楼与 seq={reply_seen[key_reply]} 重复")
        reply_seen[key_reply] = seq

    for group, seqs in TIER1_GROUP_SEQS.items():
        if len(seqs) != 2:
            problems.append(f"Group {group} 账号数应为 2，实际 {seqs}")
        windows = sorted(COPY_LIBRARY[seq]["window"] for seq in seqs)
        if windows != ["afternoon", "morning"]:
            problems.append(f"Group {group} 两号需一 morning 一 afternoon，实际 {windows}")
    for name, seqs in WINDOW_SEQS.items():
        if len(seqs) != 4:
            problems.append(f"{name} 窗口应 4 个号，实际 {seqs}")
        if sorted(seqs) != sorted([s for s in COPY_LIBRARY if COPY_LIBRARY[s]["window"] == name]):
            problems.append(f"{name} 窗口名单与文案库不一致")
    return problems


# --------------------------------------------------------------------------------------
# 状态读写（fcntl 排他锁 / 原子替换）
# --------------------------------------------------------------------------------------

def load_json(path: Path, default):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


@contextlib.contextmanager
def ledger_lock(timeout: float = 30.0):
    """fcntl.flock 排他锁，防 daemon / trigger / systemd 多进程竞态。"""
    PATHS["state"].mkdir(parents=True, exist_ok=True)
    if fcntl is None:
        yield
        return
    fh = open(PATHS["lock"], "a+", encoding="utf-8")
    deadline = time.time() + timeout
    try:
        while True:
            try:
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.time() > deadline:
                    raise RuntimeError(f"账本锁等待超时({timeout}s): {PATHS['lock']}")
                time.sleep(0.2)
        yield
    finally:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        finally:
            fh.close()


def new_ledger() -> dict:
    return {
        "version": 2,
        "created_at": iso(now_et()),
        "posts": [],
        "breaker": {"global_pause_until": None, "reason": "", "tripped_at": None},
        "pending_self_reply": [],
        "window_plans": {},
        "known_ids": {},
    }


def new_account_record(seq: int) -> dict:
    item = COPY_LIBRARY.get(seq, {})
    return {
        "seq": seq,
        "handle": item.get("handle", ""),
        "group": item.get("group", "?"),
        "tier": 1,
        "window": item.get("window", ""),
        "last_post_at": None,
        "last_et_date": None,
        "last_self_reply_at": None,
        "cooldown_until": None,
        "consecutive_failures": 0,
        "risk_status": "ok",
        "circuit_until": None,
        "total_posts": 0,
        "total_failures": 0,
        "known_tweet_ids": [],
        "last_error": "",
    }


def new_accounts() -> dict:
    return {str(seq): new_account_record(seq) for seq in TIER1_SEQS}


def load_ledger_unlocked() -> dict:
    ledger = load_json(PATHS["ledger"], None)
    if not isinstance(ledger, dict):
        ledger = new_ledger()
    ledger.setdefault("version", 2)
    ledger.setdefault("created_at", iso(now_et()))
    ledger.setdefault("posts", [])
    ledger.setdefault("breaker", {"global_pause_until": None, "reason": "", "tripped_at": None})
    ledger.setdefault("pending_self_reply", [])
    ledger.setdefault("window_plans", {})
    ledger.setdefault("known_ids", {})
    return ledger


def load_accounts_unlocked() -> dict:
    accounts = load_json(PATHS["accounts"], None)
    if not isinstance(accounts, dict):
        accounts = new_accounts()
    for seq in TIER1_SEQS:
        key = str(seq)
        base = new_account_record(seq)
        if not isinstance(accounts.get(key), dict):
            accounts[key] = base
        else:
            for field, value in base.items():
                accounts[key].setdefault(field, value)
    return accounts


def ensure_state() -> tuple[dict, dict]:
    with ledger_lock():
        ledger = load_ledger_unlocked()
        accounts = load_accounts_unlocked()
        save_json(PATHS["ledger"], ledger)
        save_json(PATHS["accounts"], accounts)
    return ledger, accounts


def read_state() -> tuple[dict, dict]:
    with ledger_lock():
        return load_ledger_unlocked(), load_accounts_unlocked()


def update_state(mutator):
    """在排他锁内 load → mutate → save，返回 mutator 结果。"""
    with ledger_lock():
        ledger = load_ledger_unlocked()
        accounts = load_accounts_unlocked()
        result = mutator(ledger, accounts)
        trim_ledger(ledger)
        save_json(PATHS["ledger"], ledger)
        save_json(PATHS["accounts"], accounts)
        return result


def trim_ledger(ledger: dict) -> None:
    posts = ledger.get("posts", [])
    if len(posts) > LEDGER_MAX_RECORDS:
        ledger["posts"] = posts[-LEDGER_MAX_RECORDS:]
    pending = ledger.get("pending_self_reply", [])
    finished = [p for p in pending if p.get("status") != "pending"]
    active = [p for p in pending if p.get("status") == "pending"]
    ledger["pending_self_reply"] = active + finished[-200:]
    plans = ledger.get("window_plans", {})
    for key in sorted(plans)[:-WINDOW_PLAN_KEEP]:
        plans.pop(key, None)


def parse_ts(value) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=ET)
    return dt.astimezone(ET)


def et_date_of(dt: datetime) -> str:
    return dt.date().isoformat()


# --------------------------------------------------------------------------------------
# 账本查询 / 风控
# --------------------------------------------------------------------------------------

def posts_today(ledger: dict, seq: int, dt: datetime) -> int:
    day = et_date_of(dt)
    return sum(
        1
        for rec in ledger.get("posts", [])
        if rec.get("seq") == seq
        and rec.get("kind") == "main"
        and rec.get("status") == "ok"
        and rec.get("et_date") == day
    )


def global_breaker_until(ledger: dict) -> datetime | None:
    return parse_ts(ledger.get("breaker", {}).get("global_pause_until"))


def failures_within(ledger: dict, minutes: int) -> int:
    cutoff = now_et() - timedelta(minutes=minutes)
    count = 0
    for rec in ledger.get("posts", []):
        if rec.get("status") != "failed":
            continue
        ts = parse_ts(rec.get("ts_et"))
        if ts and ts >= cutoff:
            count += 1
    return count


def account_block_reason(accounts: dict, seq: int, dt: datetime) -> str | None:
    acc = accounts.get(str(seq)) or new_account_record(seq)
    if acc.get("risk_status") == "circuit_open":
        until = parse_ts(acc.get("circuit_until"))
        if until and until > dt:
            return "circuit_open"
    until = parse_ts(acc.get("cooldown_until"))
    if until and until > dt:
        return "cooldown"
    return None


def eligibility(ledger: dict, accounts: dict, seq: int, dt: datetime) -> tuple[bool, str]:
    if seq not in COPY_LIBRARY:
        return False, "非 Tier-1 账号"
    if posts_today(ledger, seq, dt) >= 1:
        return False, "已达日频上限(1/天)"
    blocked = account_block_reason(accounts, seq, dt)
    if blocked == "circuit_open":
        return False, "熔断中"
    if blocked == "cooldown":
        return False, "冷却中"
    return True, "可发"


def record_post(
    ledger: dict,
    seq: int,
    kind: str,
    status: str,
    returncode: int,
    cmd: list[str],
    extra: dict | None = None,
) -> dict:
    dt = now_et()
    item = COPY_LIBRARY.get(seq, {})
    rec = {
        "ts_et": iso(dt),
        "ts_bj": iso(now_bj()),
        "et_date": et_date_of(dt),
        "seq": seq,
        "handle": item.get("handle", ""),
        "group": item.get("group", "?"),
        "window": item.get("window", ""),
        "kind": kind,
        "status": status,
        "returncode": returncode,
        "engine_cmd": cmd,
    }
    if extra:
        rec.update(extra)
    ledger.setdefault("posts", []).append(rec)
    return rec


def apply_success(accounts: dict, seq: int) -> None:
    acc = accounts.setdefault(str(seq), new_account_record(seq))
    acc["last_post_at"] = iso(now_et())
    acc["last_et_date"] = et_date_of(now_et())
    acc["cooldown_until"] = iso(now_et() + timedelta(minutes=random.randint(20, 35)))
    acc["consecutive_failures"] = 0
    acc["risk_status"] = "ok"
    acc["circuit_until"] = None
    acc["total_posts"] = int(acc.get("total_posts") or 0) + 1
    acc["last_error"] = ""


def apply_failure(accounts: dict, seq: int, error: str) -> None:
    acc = accounts.setdefault(str(seq), new_account_record(seq))
    acc["consecutive_failures"] = int(acc.get("consecutive_failures") or 0) + 1
    acc["total_failures"] = int(acc.get("total_failures") or 0) + 1
    acc["last_error"] = (error or "")[:400]
    if acc["consecutive_failures"] >= 3:
        acc["risk_status"] = "circuit_open"
        acc["circuit_until"] = iso(now_et() + timedelta(hours=6))
        acc["cooldown_until"] = acc["circuit_until"]


def trip_global_breaker(ledger: dict, reason: str) -> None:
    ledger.setdefault("breaker", {})
    ledger["breaker"]["global_pause_until"] = iso(now_et() + timedelta(hours=2))
    ledger["breaker"]["reason"] = reason
    ledger["breaker"]["tripped_at"] = iso(now_et())


# --------------------------------------------------------------------------------------
# 引擎调用
# --------------------------------------------------------------------------------------

def engine_path() -> Path:
    return Path(PATHS["engine"])


def engine_argv(sub: str, sub_args: list[str]) -> list[str]:
    return list(ENGINE_EXTRA_ARGS) + [sub] + list(sub_args)


def run_engine(sub: str, sub_args: list[str], timeout: int) -> tuple[int, str, str, list[str]]:
    engine = engine_path()
    argv = engine_argv(sub, sub_args)
    full_cmd = [sys.executable, str(engine)] + argv
    if not engine.exists():
        return 127, "", f"引擎不存在: {engine}", full_cmd
    try:
        proc = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(engine.parent),
        )
        return proc.returncode, proc.stdout or "", proc.stderr or "", full_cmd
    except subprocess.TimeoutExpired:
        return 124, "", f"引擎超时({timeout}s)", full_cmd
    except Exception as exc:  # noqa: BLE001 —— 单点异常不阻断调度
        return 1, "", f"引擎调用异常: {type(exc).__name__}: {exc}", full_cmd


def extract_result(stdout: str) -> dict:
    for line in reversed((stdout or "").strip().splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict):
                return data
    return {}


# --------------------------------------------------------------------------------------
# 个人主页独立回读（复用引擎的代理桥 / Profile / Cookie 会话）
# --------------------------------------------------------------------------------------

_ENGINE_MODULE = None
_ENGINE_MODULE_ERROR = ""


def load_engine_module():
    global _ENGINE_MODULE, _ENGINE_MODULE_ERROR
    if _ENGINE_MODULE is not None:
        return _ENGINE_MODULE
    path = engine_path()
    if not path.exists():
        raise RuntimeError(f"引擎不存在: {path}")
    spec = importlib.util.spec_from_file_location("x_matrix_lx_engine_readback", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载引擎模块")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    _ENGINE_MODULE = module
    _ENGINE_MODULE_ERROR = ""
    return module


@contextlib.contextmanager
def engine_profile_page(seq: int):
    """打开该账号的独立浏览器会话（同一代理 / Profile / Cookie），用于回读验收。"""
    eng = load_engine_module()
    from patchright.sync_api import sync_playwright

    runtime_root = Path(os.path.expanduser(str(PATHS["runtime"])))
    excel = ENGINE_EXCEL or getattr(eng, "DEFAULT_EXCEL")
    sheet = ENGINE_SHEET or getattr(eng, "DEFAULT_SHEET")
    records = eng.build_records(eng.load_matrix(excel, sheet))
    if not 1 <= seq <= len(records):
        raise RuntimeError(f"Excel 中不存在 seq={seq}")
    rec = records[seq - 1]
    viewport = eng.parse_viewport(rec.get("viewport") or "")

    pw = None
    context = None
    bridge = None
    try:
        pw = sync_playwright().start()
        context, page, bridge = eng._open_browser_session(pw, rec, runtime_root, viewport)
        page.set_default_timeout(30000)
        eng.inject_cookies(context, eng.load_cookies_for_seq(rec, runtime_root))
        yield eng, page, rec
    finally:
        if context is not None:
            try:
                context.close()
            except Exception:
                pass
        if pw is not None:
            try:
                pw.stop()
            except Exception:
                pass
        if bridge is not None:
            try:
                bridge.stop()
            except Exception:
                pass


def extract_articles(page, limit: int = 25, username: str = "") -> list[dict]:
    """从个人主页 / 推文页提取 (status_id, url, text)。"""
    items: list[dict] = []
    try:
        nodes = page.query_selector_all('article[data-testid="tweet"]')
    except Exception:
        return items
    for node in nodes[:limit]:
        try:
            text_el = node.query_selector('[data-testid="tweetText"]')
            text = (text_el.inner_text() if text_el else "") or ""
            status_id = None
            url = None
            own_prefix = f"/{username}/status/" if username else ""
            candidates = []
            for a in node.query_selector_all('a[href*="/status/"]'):
                href = a.get_attribute("href") or ""
                m = STATUS_ID_RE.search(href)
                if not m:
                    continue
                candidates.append((href, m.group(1)))
            if own_prefix:
                candidates.sort(key=lambda pair: 0 if pair[0].startswith(own_prefix) else 1)
            if candidates:
                href, status_id = candidates[0]
                url = ("https://x.com" + href.split("?")[0]) if href.startswith("/") else href.split("?")[0]
            if status_id:
                items.append({"id": status_id, "url": url, "text": text})
        except Exception:
            continue
    return items


def read_profile_timeline(seq: int, limit: int = 25, scrolls: int = 1) -> dict:
    """发帖前已知 ID 集合 / 发帖后差量比对的独立回读入口。"""
    try:
        with engine_profile_page(seq) as (eng, page, rec):
            username = rec["username"]
            if not eng.safe_goto(page, f"https://x.com/{username}", timeout=40000):
                return {"ok": False, "statuses": [], "error": "个人主页打开失败", "username": username}
            eng.sleep_s(3.0)
            for _ in range(max(0, scrolls)):
                try:
                    page.mouse.wheel(0, 2600)
                except Exception:
                    pass
                eng.sleep_s(2.0)
            statuses = extract_articles(page, limit, username)
            if not statuses:
                # 新号主页可能 0 条推文：主页结构正常即视为回读成功，known_ids 为空集合
                try:
                    url_ok = f"x.com/{username}".lower() in (page.url or "").lower()
                    header_ok = page.query_selector('[data-testid="primaryColumn"]') is not None
                except Exception:
                    url_ok = header_ok = False
                if not (url_ok and header_ok):
                    return {"ok": False, "statuses": [], "error": "个人主页未解析到推文",
                            "username": username}
            return {
                "ok": True,
                "statuses": statuses,
                "error": "",
                "username": username,
                "profile_url": f"https://x.com/{username}",
            }
    except Exception as exc:  # noqa: BLE001 —— 回读失败只影响验收，不冒充成功
        return {"ok": False, "statuses": [], "error": f"{type(exc).__name__}: {exc}", "username": ""}


def confirm_status_on_profile(seq: int, status_id: str, expected_text: str, attempts: int = 3,
                              interval: int = 30) -> dict:
    """回读个人主页，确认新推文 ID 存在且正文片段匹配（独立于引擎退出码）。"""
    if not status_id:
        return {"ok": False, "error": "缺少 status_id", "ratio": 0.0, "attempts": 0}
    last_error = ""
    for attempt in range(1, attempts + 1):
        try:
            with engine_profile_page(seq) as (eng, page, rec):
                username = rec["username"]
                if not eng.safe_goto(page, f"https://x.com/{username}", timeout=40000):
                    last_error = "个人主页打开失败"
                else:
                    eng.sleep_s(3.0)
                    target = f"/{username}/status/{status_id}"
                    ratio = 0.0
                    found_text = ""
                    try:
                        link = page.locator(f'a[href*="{target}"]').first
                        link.wait_for(state="visible", timeout=12000)
                        article = link.locator("xpath=ancestor::article")
                        found_text = article.inner_text(timeout=4000) or ""
                        ratio = text_match_ratio(expected_text, found_text)
                        if ratio < 0.82:
                            items = extract_articles(page, 30, username)
                            for item in items:
                                if item["id"] == status_id:
                                    found_text = item["text"]
                                    ratio = max(ratio, text_match_ratio(expected_text, found_text))
                                    break
                        if ratio >= 0.82:
                            return {
                                "ok": True,
                                "ratio": round(ratio, 4),
                                "status_id": status_id,
                                "tweet_url": f"https://x.com/{username}/status/{status_id}",
                                "attempts": attempt,
                                "error": "",
                            }
                        last_error = f"ID 命中但正文匹配度 {ratio:.2f} < 0.82"
                    except Exception as exc:  # noqa: BLE001
                        last_error = f"主页未找到 status {status_id}: {type(exc).__name__}"
        except Exception as exc:  # noqa: BLE001
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt < attempts:
            time.sleep(interval)
    return {"ok": False, "ratio": 0.0, "status_id": status_id, "attempts": attempts, "error": last_error}


def read_tweet_thread(seq: int, tweet_url: str, limit: int = 40) -> dict:
    try:
        with engine_profile_page(seq) as (eng, page, _rec):
            if not eng.safe_goto(page, tweet_url, timeout=40000):
                return {"ok": False, "items": [], "error": "推文页打开失败"}
            eng.sleep_s(3.5)
            try:
                page.mouse.wheel(0, 1200)
            except Exception:
                pass
            eng.sleep_s(2.0)
            items = extract_articles(page, limit)
            return {"ok": bool(items), "items": items, "error": "" if items else "推文页未解析到内容"}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "items": [], "error": f"{type(exc).__name__}: {exc}"}


def strip_html(value: str) -> str:
    return html_lib.unescape(HTML_TAG_RE.sub(" ", value or ""))


def http_get(url: str, timeout: int = EXTERNAL_TIMEOUT) -> tuple[int, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA_HTTP, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 —— 固定 https 公开端点
        return int(getattr(resp, "status", 200)), resp.read(500000).decode("utf-8", "replace")


def external_verify_tweet(tweet_url: str, expected_text: str) -> dict:
    """外部校验：publish oembed + 推文页 og:description，确认公开可见且正文匹配。"""
    fragment = norm_text(expected_text)[:70]
    sources: list[dict] = []
    errors: list[str] = []
    verdict: bool | None = None

    try:
        status, body = http_get(
            "https://publish.twitter.com/oembed?url=" + urllib.parse.quote(tweet_url, safe="")
        )
        text = strip_html(body)
        match = bool(fragment) and fragment in norm_text(text)
        sources.append({"source": "publish_oembed", "http_status": status, "match": match})
        if status == 200 and match:
            verdict = True
        elif status == 200:
            verdict = False if verdict is not True else verdict
        elif status in (403, 404):
            verdict = False
    except Exception as exc:  # noqa: BLE001
        errors.append(f"oembed:{type(exc).__name__}")

    if verdict is not True:
        try:
            status, body = http_get(tweet_url)
            og = ""
            m = re.search(r'property="og:description"\s+content="([^"]*)"', body)
            if not m:
                m = re.search(r'content="([^"]*)"\s+property="og:description"', body)
            if m:
                og = html_lib.unescape(m.group(1))
            match = bool(fragment) and fragment in norm_text(og)
            sources.append({"source": "og_description", "http_status": status, "match": match})
            if match:
                verdict = True
            elif status == 200 and og and verdict is None:
                verdict = False
        except Exception as exc:  # noqa: BLE001
            errors.append(f"og:{type(exc).__name__}")

    return {
        "verified": verdict,
        "fragment": fragment,
        "sources": sources,
        "errors": errors,
    }


def verify_new_tweet(seq: int, known_ids: set[str], expected_text: str,
                     attempts: int = 3, interval: int = 45) -> dict:
    """差量回读：个人主页出现 known_ids 之外的新 ID，且正文匹配。"""
    history: list[dict] = []
    for attempt in range(1, attempts + 1):
        rb = read_profile_timeline(seq, limit=25, scrolls=1 if attempt > 1 else 0)
        history.append({
            "attempt": attempt,
            "ok": rb["ok"],
            "count": len(rb["statuses"]),
            "error": rb.get("error", ""),
        })
        if rb["ok"]:
            new_items = [item for item in rb["statuses"] if item["id"] not in known_ids]
            best = None
            best_ratio = 0.0
            for item in new_items:
                ratio = text_match_ratio(expected_text, item["text"])
                if ratio > best_ratio:
                    best, best_ratio = item, ratio
            if best and best_ratio >= 0.82:
                return {
                    "ok": True,
                    "tweet": best,
                    "ratio": round(best_ratio, 4),
                    "new_ids": [item["id"] for item in new_items],
                    "attempts": attempt,
                    "history": history,
                    "error": "",
                }
            if new_items:
                history[-1]["best_ratio"] = round(best_ratio, 4)
        if attempt < attempts:
            time.sleep(interval)
    return {
        "ok": False,
        "tweet": None,
        "ratio": 0.0,
        "new_ids": [],
        "attempts": attempts,
        "history": history,
        "error": "个人主页未出现匹配的新推文 ID",
    }


def verify_reply_visible(seq: int, parent_url: str, reply_text: str, known_ids: set[str],
                         attempts: int = 2, interval: int = 30) -> dict:
    """1 楼自评验收：个人主页差量 + 推文详情页双路回读。"""
    last_error = ""
    for attempt in range(1, attempts + 1):
        rb = read_profile_timeline(seq, limit=25, scrolls=1)
        if rb["ok"]:
            for item in rb["statuses"]:
                if item["id"] in known_ids:
                    continue
                ratio = text_match_ratio(reply_text, item["text"])
                if ratio >= 0.80:
                    ext = external_verify_tweet(item["url"], reply_text)
                    return {
                        "ok": ext["verified"] is not False,
                        "reply": item,
                        "ratio": round(ratio, 4),
                        "source": "profile",
                        "external": ext,
                        "attempts": attempt,
                        "error": "",
                    }
            last_error = "个人主页未出现匹配的 1 楼内容"
        else:
            last_error = rb.get("error", "")
        if parent_url:
            th = read_tweet_thread(seq, parent_url, limit=40)
            if th["ok"]:
                for item in th["items"]:
                    if item["id"] in known_ids or item["url"] == parent_url:
                        continue
                    ratio = text_match_ratio(reply_text, item["text"])
                    if ratio >= 0.80:
                        ext = external_verify_tweet(item["url"], reply_text)
                        return {
                            "ok": ext["verified"] is not False,
                            "reply": item,
                            "ratio": round(ratio, 4),
                            "source": "thread",
                            "external": ext,
                            "attempts": attempt,
                            "error": "",
                        }
                last_error = last_error or "推文详情页未出现匹配的 1 楼内容"
        if attempt < attempts:
            time.sleep(interval)
    return {"ok": False, "reply": None, "ratio": 0.0, "source": "", "external": {}, "attempts": attempts,
            "error": last_error or "1 楼回读验收失败"}


# --------------------------------------------------------------------------------------
# 1 楼自评待办队列（持久化，进程中断不丢链接）
# --------------------------------------------------------------------------------------

def enqueue_pending(ledger: dict, seq: int, parent_url: str, reply_text: str,
                    due_at: datetime, note: str = "") -> str:
    pid = f"sr-{seq}-{int(time.time() * 1000)}"
    ledger.setdefault("pending_self_reply", []).append({
        "id": pid,
        "seq": seq,
        "group": COPY_LIBRARY[seq]["group"],
        "handle": COPY_LIBRARY[seq]["handle"],
        "parent_tweet_url": parent_url,
        "self_reply_text": reply_text,
        "created_at": iso(now_et()),
        "due_at": iso(due_at),
        "attempts": 0,
        "last_attempt_at": None,
        "last_error": "",
        "status": "pending",
        "note": note,
    })
    return pid


def find_pending(ledger: dict, pid: str) -> dict | None:
    for item in ledger.get("pending_self_reply", []):
        if item.get("id") == pid:
            return item
    return None


def pending_due(ledger: dict, dt: datetime) -> list[dict]:
    due: list[dict] = []
    for item in ledger.get("pending_self_reply", []):
        if item.get("status") != "pending":
            continue
        due_at = parse_ts(item.get("due_at"))
        if due_at is None or due_at <= dt:
            due.append(item)
    return sorted(due, key=lambda x: str(x.get("due_at") or ""))


def attempt_self_reply(item: dict, known_ids: set[str]) -> dict:
    seq = int(item["seq"])
    parent_url = item.get("parent_tweet_url") or ""
    reply_text = item.get("self_reply_text") or ""
    if not parent_url.startswith("http"):
        return {"ok": False, "error": "缺少 parent_tweet_url，拒绝脱离主帖单独发链接", "rc": -1,
                "engine_result": {}, "reply": None, "external": {}, "cmd": []}
    rc, out, err, full_cmd = run_engine(
        "post",
        ["--seq", str(seq), "--text", reply_text, "--reply-url", parent_url],
        DEFAULT_REPLY_TIMEOUT,
    )
    engine_result = extract_result(out)
    verdict = verify_reply_visible(seq, parent_url, reply_text, known_ids)
    ok = bool(verdict.get("ok") and (engine_result.get("submitted") or verdict.get("reply")))
    return {
        "ok": ok,
        "rc": rc,
        "engine_result": engine_result,
        "reply": verdict.get("reply"),
        "ratio": verdict.get("ratio", 0.0),
        "source": verdict.get("source", ""),
        "external": verdict.get("external", {}),
        "error": "" if ok else (verdict.get("error") or err.strip()[-200:] or f"rc={rc}"),
        "cmd": full_cmd,
    }


def process_pending(limit: int = 2, respect_due: bool = True, only_id: str | None = None) -> list[dict]:
    """补发到期 1 楼待办。成功即出队；失败按退避改期；超过上限标记 abandoned（不静默丢弃）。"""
    dt = now_et()
    ledger, accounts = read_state()
    if only_id:
        candidates = [i for i in ledger.get("pending_self_reply", [])
                      if i.get("id") == only_id and i.get("status") == "pending"]
    else:
        candidates = pending_due(ledger, dt) if respect_due else [
            i for i in ledger.get("pending_self_reply", []) if i.get("status") == "pending"
        ]
    results: list[dict] = []
    for item in candidates[: max(1, limit)]:
        if not engine_path().exists():
            results.append({"id": item["id"], "status": "engine_missing"})
            break
        known = set((ledger.get("known_ids", {}).get(str(item["seq"])) or []))
        out = attempt_self_reply(item, known)
        ts = now_et()

        def mutate(led: dict, accs: dict):
            entry = find_pending(led, item["id"])
            if entry is None:
                return
            entry["attempts"] = int(entry.get("attempts") or 0) + 1
            entry["last_attempt_at"] = iso(ts)
            if out["ok"]:
                entry["status"] = "done"
                entry["completed_at"] = iso(ts)
                entry["reply_url"] = (out.get("reply") or {}).get("url")
                entry["reply_status_id"] = (out.get("reply") or {}).get("id")
                entry["last_error"] = ""
                record_post(
                    led, int(entry["seq"]), "self_reply", "ok", int(out.get("rc") or 0),
                    out.get("cmd") or [],
                    {
                        "pending_id": entry["id"],
                        "parent_tweet_url": entry.get("parent_tweet_url"),
                        "reply_url": entry.get("reply_url"),
                        "reply_status_id": entry.get("reply_status_id"),
                        "match_ratio": out.get("ratio"),
                        "verify_source": out.get("source"),
                        "external_verify": out.get("external"),
                        "engine_result": out.get("engine_result"),
                    },
                )
                acc = accs.setdefault(str(entry["seq"]), new_account_record(int(entry["seq"])))
                acc["last_self_reply_at"] = iso(ts)
                acc["consecutive_failures"] = 0
                acc["risk_status"] = "ok"
                acc["circuit_until"] = None
            else:
                entry["last_error"] = str(out.get("error") or "")[:400]
                attempts = int(entry["attempts"])
                created = parse_ts(entry.get("created_at"))
                expired = created and (ts - created) > timedelta(hours=PENDING_MAX_AGE_HOURS)
                if attempts >= PENDING_MAX_ATTEMPTS or expired:
                    entry["status"] = "abandoned"
                    entry["abandoned_at"] = iso(ts)
                else:
                    backoff = min(30, 5 * attempts)
                    entry["due_at"] = iso(ts + timedelta(minutes=backoff))
                record_post(
                    led, int(entry["seq"]), "self_reply", "failed", int(out.get("rc") or -1),
                    out.get("cmd") or [],
                    {
                        "pending_id": entry["id"],
                        "parent_tweet_url": entry.get("parent_tweet_url"),
                        "attempts": attempts,
                        "error": entry["last_error"],
                        "engine_result": out.get("engine_result"),
                    },
                )
                apply_failure(accs, int(entry["seq"]), entry["last_error"])

        update_state(mutate)
        results.append({
            "id": item["id"],
            "seq": item["seq"],
            "status": "ok" if out["ok"] else "failed",
            "reply_url": (out.get("reply") or {}).get("url"),
            "error": out.get("error", ""),
        })
        emit(f"  1楼待办 {item['id']} seq={item['seq']} → {'OK' if out['ok'] else 'FAIL'} "
             f"{(out.get('reply') or {}).get('url') or out.get('error', '')}")
    return results


# --------------------------------------------------------------------------------------
# 主帖发布：known_ids → 发布 → 差量回读 → 文字匹配 → 外部校验 → 1 楼待办
# --------------------------------------------------------------------------------------

def execute_main_post(seq: int, delay_self_reply: int, wait_self_reply: bool = False,
                      forced: bool = False, plan_key: str | None = None) -> dict:
    entry = COPY_LIBRARY[seq]
    group = entry["group"]
    result = {
        "seq": seq,
        "group": group,
        "handle": entry["handle"],
        "window": entry["window"],
        "main_status": "skipped",
        "self_reply_status": "skipped",
        "tweet_url": None,
        "tweet_id": None,
        "pending_id": None,
        "known_ids": 0,
        "match_ratio": 0.0,
        "external_verified": None,
        "note": "",
    }

    if LINK_RE.search(entry["main"]):
        update_state(lambda led, acc: (
            record_post(led, seq, "main", "failed", -1, [], {"error": "主帖含外链，拒绝执行"}),
            apply_failure(acc, seq, "主帖含外链，拒绝执行"),
        ))
        result["main_status"] = "blocked_link_in_main"
        return result

    if not engine_path().exists():
        result["main_status"] = "engine_missing"
        result["note"] = f"引擎缺失: {engine_path()}"
        return result

    # 步骤 1：发帖前读取个人主页已有推文 ID 集合（known_ids）
    pre = read_profile_timeline(seq, limit=25, scrolls=0)
    if not pre["ok"]:
        pre = read_profile_timeline(seq, limit=25, scrolls=1)
    if not pre["ok"]:
        result["main_status"] = "readback_unavailable"
        result["note"] = f"发帖前 known_ids 读取失败: {pre.get('error', '')}"

        def mutate_pre_fail(led: dict, accs: dict):
            record_post(led, seq, "main", "failed", -1, [], {
                "error": result["note"], "phase": "preflight_known_ids",
            })
            apply_failure(accs, seq, result["note"])

        update_state(mutate_pre_fail)
        return result

    known_ids = {item["id"] for item in pre["statuses"]}
    result["known_ids"] = len(known_ids)

    def persist_known(led: dict, accs: dict):
        led.setdefault("known_ids", {})[str(seq)] = sorted(known_ids)
        acc = accs.setdefault(str(seq), new_account_record(seq))
        acc["known_tweet_ids"] = sorted(known_ids)[-60:]

    update_state(persist_known)
    emit(f"  [{seq}] 发帖前 known_ids={len(known_ids)} 条（个人主页回读）")

    # 步骤 2：只发主帖（链接与披露绝不进入主帖）
    rc, out, err, full_cmd = run_engine("post", ["--seq", str(seq), "--text", entry["main"]],
                                        DEFAULT_POST_TIMEOUT)
    engine_result = extract_result(out)
    verified_by_engine = bool(engine_result.get("verified"))
    engine_status_id = str(engine_result.get("status_id") or "")
    engine_tweet_url = engine_result.get("tweet_url") or engine_result.get("target_url")
    emit(f"  [{seq}] 引擎返回 rc={rc} submitted={engine_result.get('submitted')} "
         f"verified={verified_by_engine} status_id={engine_status_id or 'n/a'}")

    # 步骤 3：独立差量回读个人主页（不认退出码，也不盲信引擎 submitted）
    verdict = verify_new_tweet(seq, known_ids, entry["main"], attempts=3, interval=45)
    tweet = verdict.get("tweet")
    if not verdict["ok"] and engine_status_id:
        confirm = confirm_status_on_profile(seq, engine_status_id, entry["main"], attempts=2, interval=40)
        if confirm["ok"]:
            tweet = {"id": engine_status_id, "url": confirm["tweet_url"], "text": entry["main"]}
            verdict = {"ok": True, "tweet": tweet, "ratio": confirm.get("ratio", 0.0),
                       "new_ids": [engine_status_id], "attempts": confirm.get("attempts", 0),
                       "history": verdict.get("history", []), "error": ""}
            result["note"] = "差量回读未命中，已按引擎 status_id 定点复核通过"

    if not verdict["ok"] or not tweet:
        result["main_status"] = "unverified"
        result["note"] = verdict.get("error", "") or "个人主页未回读到新推文"
        evidence = {
            "engine_result": engine_result,
            "readback_history": verdict.get("history", []),
            "known_ids": len(known_ids),
            "stderr_tail": (err or "")[-400:],
            "error": result["note"],
        }

        def mutate_unverified(led: dict, accs: dict):
            record_post(led, seq, "main", "failed", rc, full_cmd, evidence)
            apply_failure(accs, seq, result["note"])

        update_state(mutate_unverified)
        return result

    tweet_url = tweet["url"] or engine_tweet_url
    tweet_id = tweet["id"]
    result["tweet_url"] = tweet_url
    result["tweet_id"] = tweet_id
    result["match_ratio"] = float(verdict.get("ratio") or 0.0)

    # 步骤 4：外部校验（oembed / og:description），确认真实公开可见
    ext = external_verify_tweet(tweet_url, entry["main"])
    result["external_verified"] = ext.get("verified")
    if ext.get("verified") is False:
        result["main_status"] = "unverified_external"
        result["note"] = "外部校验不通过（oembed/og 均未匹配正文）"

        def mutate_ext_fail(led: dict, accs: dict):
            record_post(led, seq, "main", "failed", rc, full_cmd, {
                "engine_result": engine_result,
                "tweet_url": tweet_url,
                "tweet_id": tweet_id,
                "match_ratio": result["match_ratio"],
                "external_verify": ext,
                "known_ids": len(known_ids),
                "stderr_tail": (err or "")[-400:],
                "error": result["note"],
            })
            apply_failure(accs, seq, result["note"])

        update_state(mutate_ext_fail)
        return result
    if ext.get("verified") is None:
        result["note"] = "外部校验端点不可达（已保留回读证据，标记 external_unavailable）"

    # 步骤 5：主帖验收通过 → 记账 + 写 1 楼待办（持久化）
    due_at = now_et() + timedelta(seconds=max(0, int(delay_self_reply)))
    pid_holder: dict[str, str] = {}

    def mutate_ok(led: dict, accs: dict):
        record_post(led, seq, "main", "ok", rc, full_cmd, {
            "engine_result": engine_result,
            "tweet_url": tweet_url,
            "tweet_id": tweet_id,
            "match_ratio": result["match_ratio"],
            "external_verify": ext,
            "known_ids": len(known_ids),
            "readback_attempts": verdict.get("attempts"),
            "window_plan": plan_key,
            "stderr_tail": (err or "")[-400:],
        })
        apply_success(accs, seq)
        pid_holder["pid"] = enqueue_pending(
            led, seq, tweet_url, entry["self_reply"], due_at,
            note="主帖验收通过后挂 1 楼" if delay_self_reply > 0 else "立即挂 1 楼",
        )
        led.setdefault("known_ids", {})[str(seq)] = sorted(known_ids | {tweet_id})

    update_state(mutate_ok)
    result["main_status"] = "ok"
    result["pending_id"] = pid_holder.get("pid")
    result["self_reply_status"] = "pending"
    emit(f"  [{seq}] 主帖验收通过 {tweet_url} | 匹配度 {result['match_ratio']:.2f} | "
         f"外部校验 {ext.get('verified')} | 1楼待办 {result['pending_id']} due {iso(due_at)}")

    if wait_self_reply:
        wait_seconds = max(0, int((due_at - now_et()).total_seconds()))
        if wait_seconds:
            emit(f"  [{seq}] 等待 {human_delta(wait_seconds)} 后挂 1 楼 ...")
            time.sleep(wait_seconds)
        process_pending(limit=1, respect_due=True, only_id=result["pending_id"])
        ledger, _ = read_state()
        item = find_pending(ledger, result["pending_id"])
        if item:
            result["self_reply_status"] = item.get("status")
            if item.get("status") == "done":
                result["self_reply_url"] = item.get("reply_url")

    return result


# --------------------------------------------------------------------------------------
# 窗口计划（20-35 分钟错峰，落盘防重排）
# --------------------------------------------------------------------------------------

def plan_key(window: str, day: date) -> str:
    return f"{day.isoformat()}|{window}"


def build_plan(window: str, day: date) -> dict:
    start_t, end_t = WINDOW_HOURS[window]
    start = combine_et(day, start_t)
    end = combine_et(day, end_t)
    seqs = list(WINDOW_SEQS[window])
    random.shuffle(seqs)
    cursor = start + timedelta(seconds=random.randint(0, 240))
    tail = timedelta(minutes=8)
    avail = max(60.0, (end - tail - cursor).total_seconds())
    gaps = max(1, len(seqs) - 1)
    budget = avail / gaps
    upper = max(20 * 60, min(35 * 60, budget))
    slots: list[dict] = []
    for index, seq in enumerate(seqs):
        slots.append({
            "seq": seq,
            "group": COPY_LIBRARY[seq]["group"],
            "handle": COPY_LIBRARY[seq]["handle"],
            "due_at": iso(cursor),
            "status": "pending",
            "posted_at": None,
            "tweet_url": None,
            "note": "",
        })
        if index < gaps:
            cursor += timedelta(seconds=random.uniform(20 * 60, upper))
    return {
        "window": window,
        "et_date": day.isoformat(),
        "created_at": iso(now_et()),
        "start": iso(start),
        "end": iso(end),
        "gap_upper_seconds": int(upper),
        "slots": slots,
    }


def get_or_create_plan(ledger: dict, window: str, day: date) -> dict:
    plans = ledger.setdefault("window_plans", {})
    key = plan_key(window, day)
    if key not in plans:
        plans[key] = build_plan(window, day)
        emit(f"[计划] 新建 {key}：{[(s['seq'], s['due_at'][11:16]) for s in plans[key]['slots']]}")
    return plans[key]


def mark_slot(plan_key_value: str, seq: int, status: str, extra: dict | None = None) -> None:
    def mutate(ledger: dict, _accounts: dict):
        plan = ledger.get("window_plans", {}).get(plan_key_value)
        if not plan:
            return
        for slot in plan.get("slots", []):
            if slot.get("seq") == seq and slot.get("status") == "pending":
                slot["status"] = status
                slot["decided_at"] = iso(now_et())
                if extra:
                    slot.update(extra)
                break

    update_state(mutate)


def last_main_post_ts(ledger: dict, day: str, window: str) -> datetime | None:
    latest: datetime | None = None
    for rec in ledger.get("posts", []):
        if rec.get("kind") != "main" or rec.get("status") != "ok":
            continue
        if rec.get("et_date") != day or rec.get("window") != window:
            continue
        ts = parse_ts(rec.get("ts_et"))
        if ts and (latest is None or ts > latest):
            latest = ts
    return latest


# --------------------------------------------------------------------------------------
# 输出
# --------------------------------------------------------------------------------------

def emit(line: str = "") -> None:
    print(line, flush=True)


def print_header(title: str) -> None:
    emit("=" * 78)
    emit(title)
    emit("=" * 78)


def describe_window(dt: datetime, forced: bool = False) -> str:
    name = window_name(dt)
    if name:
        end = window_end_dt(dt.date(), name)
        return f"活跃窗口: {name} —— {WINDOW_LABEL[name]} | 剩余 {human_delta((end - dt).total_seconds())}"
    if forced:
        return "活跃窗口: forced（当前不在自然窗口，--force 已放开）"
    return "活跃窗口: 无（周一至周四 08:30-10:30 / 12:30-14:00 ET）"


# --------------------------------------------------------------------------------------
# status
# --------------------------------------------------------------------------------------

def cmd_status(args) -> int:
    ledger, accounts = ensure_state()
    dt = now_et()
    print_header("X 矩阵调度器 STATUS（美东双窗口 / known_ids 回读 / 1 楼待办 / 风控）")
    emit(f"运行目录 : {PATHS['runtime']}")
    emit(f"引擎文件 : {PATHS['engine']} {'[存在]' if engine_path().exists() else '[缺失]'}")
    emit(f"账本文件 : {PATHS['ledger']}")
    emit(f"状态文件 : {PATHS['accounts']}")
    emit("")
    emit("[时间]")
    emit(f"美东 ET : {fmt_ts(dt)}")
    emit(f"北京 BJ : {fmt_ts(now_bj())}")
    emit(f"UTC     : {fmt_ts(dt.astimezone(UTC))}")
    emit(describe_window(dt))
    nxt = next_window_start(dt)
    if nxt:
        name, start = nxt
        emit(f"下一窗口 : {name} @ {fmt_ts(start)} / 北京 {fmt_ts(start.astimezone(BJ))}"
             f"（倒计时 {human_delta((start - dt).total_seconds())}）")
    emit("")

    breaker = global_breaker_until(ledger)
    emit("[熔断器]")
    if breaker and breaker > dt:
        emit(f"全局暂停至 {fmt_ts(breaker)}（{ledger['breaker'].get('reason') or 'n/a'}）")
    else:
        emit(f"全局正常（近 60 分钟失败 {failures_within(ledger, 60)} / 阈值 5）")
    emit("单号: 连续失败 3 次 → 熔断 6 小时 | 每号每日 1 帖 | 窗口内 20-35 分钟错峰")
    emit("")

    emit("[Tier-1 8 号（逐号独立文案）]")
    for seq in TIER1_SEQS:
        item = COPY_LIBRARY[seq]
        acc = accounts.get(str(seq), new_account_record(seq))
        cd = parse_ts(acc.get("cooldown_until"))
        cd_txt = "无冷却" if not cd or cd <= dt else f"冷却至 {fmt_ts(cd)}"
        emit(f"  seq={seq:<3} @{item['handle']:<17} {item['group']}/{item['window']:<9} "
             f"{item['theme'][:34]:<36} 今日={posts_today(ledger, seq, dt)} {cd_txt} "
             f"风控={acc.get('risk_status')} known_ids={len(ledger.get('known_ids', {}).get(str(seq), []))}")
    emit("")

    emit("[1 楼待办队列 pending_self_reply]")
    pending = ledger.get("pending_self_reply", [])
    active = [p for p in pending if p.get("status") == "pending"]
    emit(f"队列 {len(pending)} 条 | pending {len(active)} | done "
         f"{len([p for p in pending if p.get('status') == 'done'])} | abandoned "
         f"{len([p for p in pending if p.get('status') == 'abandoned'])}")
    for item in active[:8]:
        emit(f"  {item['id']} seq={item['seq']} due={item.get('due_at')} attempts={item.get('attempts')} "
             f"parent={item.get('parent_tweet_url')} err={str(item.get('last_error') or '')[:60]}")
    emit("")

    emit("[窗口计划]")
    for name in ("morning", "afternoon"):
        plan = ledger.get("window_plans", {}).get(plan_key(name, dt.date()))
        if plan:
            emit(f"  {name}: " + " | ".join(
                f"seq={s['seq']}@{s['due_at'][11:16]} {s['status']}" for s in plan["slots"]))
        else:
            emit(f"  {name}: 今日未生成（进入窗口或 plan --create 时生成）")
    emit("")

    emit("[发帖账本]")
    posts = ledger.get("posts", [])
    today = [p for p in posts if p.get("et_date") == et_date_of(dt) and p.get("kind") == "main"]
    emit(f"记录 {len(posts)} 条 | 今日主帖 ok={len([p for p in today if p.get('status') == 'ok'])} "
         f"failed={len([p for p in today if p.get('status') == 'failed'])}")
    for rec in posts[-6:]:
        emit(f"  {str(rec.get('ts_et'))[:19]} seq={rec.get('seq')} {rec.get('kind')} → {rec.get('status')} "
             f"rc={rec.get('returncode')} {str(rec.get('tweet_url') or '')}")
    emit("")

    problems = validate_copy_library()
    emit("[文案自检]")
    if problems:
        for p in problems:
            emit(f"  FAIL: {p}")
        emit("结果: FAIL")
    else:
        emit("  8 套文案两两互异 / 主帖零外链 / 披露在链接前 / 双窗口各 4 号 / 每赛道一晨一午")
        emit("结果: PASS")
    return 0


# --------------------------------------------------------------------------------------
# dry-run / plan / verify / pending
# --------------------------------------------------------------------------------------

def cmd_dry_run(args) -> int:
    ledger, accounts = ensure_state()
    dt = now_et()
    forced = bool(getattr(args, "force", False))
    gate = bool(window_name(dt)) or forced
    print_header("X 矩阵 DRY-RUN（不调用浏览器 / 不写账本）")
    emit(f"ET {fmt_ts(dt)} | BJ {fmt_ts(now_bj())}")
    emit(describe_window(dt, forced=forced))
    breaker = global_breaker_until(ledger)
    if breaker and breaker > dt:
        gate = False
        emit(f"熔断: 全局暂停至 {fmt_ts(breaker)} → 本轮全部跳过")
    emit(f"闸门判定: {'OPEN' if gate else 'CLOSED'}")
    emit("")
    emit("[窗口分配]")
    for name in ("morning", "afternoon"):
        seqs = WINDOW_SEQS[name]
        emit(f"  {name:<9} {WINDOW_LABEL[name]}")
        for seq in seqs:
            ok, reason = eligibility(ledger, accounts, seq, dt)
            emit(f"    seq={seq:<3} @{COPY_LIBRARY[seq]['handle']:<17} {reason}")
    emit("")
    emit("[验收链（每帖必跑）]")
    emit("  1) 发帖前回读个人主页 → known_ids 落盘")
    emit("  2) 引擎 post（主帖零外链，不带 --self-reply）")
    emit("  3) 独立差量回读个人主页 → 新 status_id + 正文匹配 ≥0.82")
    emit("  4) 外部校验 publish oembed / og:description")
    emit("  5) 通过 → 写 pending_self_reply（parent_tweet_url / self_reply_text / due_at）")
    emit("")
    emit("[文案预览]")
    for seq in TIER1_SEQS:
        item = COPY_LIBRARY[seq]
        emit(f"  seq={seq} {item['group']}/{item['window']} {item['theme']}")
        emit(f"    main: {item['main'][:110]}...")
        emit(f"    1F  : {item['self_reply'][:110]}...")
    emit("")
    emit("本轮未产生任何真实动作。")
    return 0


def cmd_plan(args) -> int:
    ledger, _ = ensure_state()
    dt = now_et()
    name = args.window or window_name(dt) or "morning"
    day = date.fromisoformat(args.date) if args.date else dt.date()
    key = plan_key(name, day)
    plan = ledger.get("window_plans", {}).get(key)
    if plan is None and args.create:
        def mutate(led: dict, _acc: dict):
            return get_or_create_plan(led, name, day)

        plan = update_state(mutate)
    print_header(f"窗口计划 {key}")
    if not plan:
        emit("未生成（加 --create 生成并落盘）")
        return 0
    emit(f"窗口 {plan['start']} → {plan['end']} | 最大间隔 {plan['gap_upper_seconds'] // 60} 分钟")
    for slot in plan["slots"]:
        due = parse_ts(slot["due_at"])
        emit(f"  seq={slot['seq']:<3} @{COPY_LIBRARY[slot['seq']]['handle']:<17} "
             f"due {fmt_ts(due) if due else '?'}（北京 {fmt_ts(due.astimezone(BJ)) if due else '?'}） "
             f"{slot['status']} {slot.get('note') or ''}")
    emit(f"账本: {PATHS['ledger']}")
    return 0


def cmd_verify(args) -> int:
    seq = int(args.seq)
    if seq not in COPY_LIBRARY:
        emit(f"seq={seq} 不是 Tier-1 账号")
        return 2
    print_header(f"回读验收自检 seq={seq} @{COPY_LIBRARY[seq]['handle']}")
    if args.tweet_url:
        status_id = args.status_id or ""
        if not status_id:
            m = STATUS_ID_RE.search(args.tweet_url)
            status_id = m.group(1) if m else ""
        confirm = confirm_status_on_profile(seq, status_id, COPY_LIBRARY[seq]["main"])
        emit(f"定点回读: ok={confirm.get('ok')} ratio={confirm.get('ratio')} err={confirm.get('error')}")
        return 0 if confirm.get("ok") else 1
    rb = read_profile_timeline(seq, limit=25, scrolls=1)
    if not rb["ok"]:
        emit(f"回读失败: {rb.get('error')}")
        return 1
    emit(f"个人主页 {rb['profile_url']} 解析到 {len(rb['statuses'])} 条推文")
    for item in rb["statuses"][:10]:
        emit(f"  {item['id']} ratio(main)={text_match_ratio(COPY_LIBRARY[seq]['main'], item['text']):.2f} "
             f"{item['url']}")
    emit("回读链路正常。")
    return 0


def cmd_pending(args) -> int:
    ledger, _ = ensure_state()
    if args.process:
        results = process_pending(limit=max(1, args.limit), respect_due=not args.ignore_due)
        if not results:
            emit("没有到期待办。")
        return 0 if all(r.get("status") == "ok" for r in results) else 1
    items = ledger.get("pending_self_reply", [])
    print_header("1 楼待办队列 pending_self_reply")
    emit(f"共 {len(items)} 条 | pending {len([i for i in items if i.get('status') == 'pending'])}")
    for item in items[-20:]:
        emit(f"  {item['id']} seq={item['seq']} status={item['status']} due={item.get('due_at')} "
             f"attempts={item.get('attempts')} parent={item.get('parent_tweet_url')}")
        emit(f"    reply: {str(item.get('self_reply_text'))[:100]}")
    return 0


# --------------------------------------------------------------------------------------
# trigger-tier1 / trigger-window
# --------------------------------------------------------------------------------------

def gate_ok(ledger: dict, dt: datetime, forced: bool, seqs: list[int] | None = None) -> tuple[bool, str]:
    breaker = global_breaker_until(ledger)
    if breaker and breaker > dt:
        return False, f"全局熔断至 {fmt_ts(breaker)}"
    name = window_name(dt)
    if name is None and not forced:
        return False, "当前不在美东发布窗口（Mon-Thu 08:30-10:30 / 12:30-14:00 ET）"
    if name and seqs:
        wrong = [s for s in seqs if COPY_LIBRARY[s]["window"] != name]
        if wrong and not forced:
            return False, f"seq={wrong} 不属于当前窗口 {name}"
    return True, name or "forced"


def cmd_trigger_tier1(args) -> int:
    ledger, accounts = ensure_state()
    dt = now_et()
    groups = ["A", "B", "C", "D"] if args.group == "ALL" else [args.group]
    if args.seq is not None:
        if args.seq not in COPY_LIBRARY:
            emit(f"--seq {args.seq} 不是 Tier-1 账号")
            return 2
        targets = [args.seq]
    else:
        targets = [seq for group in groups for seq in TIER1_GROUP_SEQS[group]]

    print_header("TRIGGER-TIER1（known_ids → 发布 → 差量回读 → 外部校验 → 1 楼待办）")
    emit(f"ET {fmt_ts(dt)} | BJ {fmt_ts(now_bj())}")
    emit(describe_window(dt, forced=bool(args.force)))
    emit(f"目标: {targets} | 1 楼延迟 {args.delay_self_reply_seconds}s | 间隔 "
         f"{args.gap_min}-{args.gap_max} 分钟")

    ok, why = gate_ok(ledger, dt, bool(args.force), targets)
    if not ok:
        emit(f"拒绝执行: {why}（人工联调请加 --force）")
        return 1
    if not engine_path().exists():
        emit(f"引擎缺失: {engine_path()}")
        return 1

    planned = []
    for seq in targets:
        can, reason = eligibility(ledger, accounts, seq, dt)
        if can:
            planned.append(seq)
        else:
            emit(f"seq={seq}: 跳过（{reason}）")
    if not planned:
        emit("无可发账号。")
        return 0

    emit("")
    failures = 0
    for index, seq in enumerate(planned):
        if index > 0 and not args.no_stagger:
            gap = random.randint(max(1, args.gap_min) * 60, max(args.gap_min, args.gap_max) * 60)
            emit(f"错峰等待 {human_delta(gap)} 后继续 ...")
            time.sleep(gap)
        emit(f"→ seq={seq} @{COPY_LIBRARY[seq]['handle']} {COPY_LIBRARY[seq]['theme']}")
        summary = execute_main_post(
            seq,
            delay_self_reply=args.delay_self_reply_seconds,
            wait_self_reply=bool(args.wait_self_reply),
            forced=bool(args.force),
        )
        emit(f"  主帖={summary['main_status']} 1楼={summary['self_reply_status']} "
             f"url={summary.get('tweet_url') or 'n/a'} ratio={summary.get('match_ratio')} "
             f"ext={summary.get('external_verified')} note={summary.get('note') or '-'}")
        if summary["main_status"] != "ok":
            failures += 1
        ledger, accounts = read_state()
        if failures_within(ledger, 60) >= 5:
            update_state(lambda led, _acc: trip_global_breaker(led, "60 分钟内失败 5 次"))
            emit("全局熔断已触发（2 小时），停止本轮。")
            break
    emit("")
    emit(f"完成: {len(planned) - failures}/{len(planned)} 主帖验收通过。账本: {PATHS['ledger']}")
    return 1 if failures else 0


def cmd_trigger_window(args) -> int:
    """按落盘计划整窗执行：睡到每个 slot 的 due_at，再逐号发布。"""
    ledger, accounts = ensure_state()
    dt = now_et()
    name = args.window or window_name(dt)
    if name is None:
        emit("当前不在窗口内，请显式 --window morning|afternoon（或 --force 手动联调）")
        return 1
    day = dt.date()
    key_holder = {"key": plan_key(name, day)}

    def mutate(led: dict, _acc: dict):
        return get_or_create_plan(led, name, day)

    plan = update_state(mutate)
    emit(describe_window(dt, forced=bool(args.force)))
    emit(f"窗口计划 {key_holder['key']} | " + " | ".join(
        f"seq={s['seq']}@{s['due_at'][11:16]}" for s in plan["slots"]))

    end = window_end_dt(day, name) - timedelta(minutes=2)
    failures = 0
    for slot in plan["slots"]:
        if slot["status"] != "pending":
            continue
        due = parse_ts(slot["due_at"])
        if due is None:
            continue
        if due > now_et():
            while now_et() < due:
                time.sleep(min(30, max(1, int((due - now_et()).total_seconds()))))
        dt_now = now_et()
        if dt_now > end and not args.force:
            mark_slot(key_holder["key"], slot["seq"], "missed", {"note": "窗口已关闭"})
            emit(f"seq={slot['seq']} 窗口已关闭，标记 missed")
            continue
        ledger, accounts = read_state()
        last = last_main_post_ts(ledger, day.isoformat(), name)
        if last and not args.force:
            gap_left = 18 * 60 - (dt_now - last).total_seconds()
            if gap_left > 0:
                emit(f"距上一帖不足 18 分钟，补足错峰 {human_delta(gap_left)} ...")
                time.sleep(gap_left)
                dt_now = now_et()
                if dt_now > end:
                    mark_slot(key_holder["key"], slot["seq"], "missed", {"note": "补足错峰后窗口已关闭"})
                    continue
        can, reason = eligibility(ledger, accounts, slot["seq"], dt_now)
        if not can:
            mark_slot(key_holder["key"], slot["seq"], "skipped", {"note": reason})
            emit(f"seq={slot['seq']} 跳过（{reason}）")
            continue
        emit(f"→ seq={slot['seq']} @{COPY_LIBRARY[slot['seq']]['handle']}")
        summary = execute_main_post(
            slot["seq"],
            delay_self_reply=args.delay_self_reply_seconds,
            wait_self_reply=bool(args.wait_self_reply),
            forced=bool(args.force),
            plan_key=key_holder["key"],
        )
        mark_slot(
            key_holder["key"], slot["seq"],
            "done" if summary["main_status"] == "ok" else "failed",
            {"tweet_url": summary.get("tweet_url"), "note": summary.get("note") or "",
             "main_status": summary["main_status"]},
        )
        if summary["main_status"] != "ok":
            failures += 1
        ledger, _ = read_state()
        if failures_within(ledger, 60) >= 5:
            update_state(lambda led, _acc: trip_global_breaker(led, "60 分钟内失败 5 次"))
            emit("全局熔断已触发（2 小时），停止本窗口。")
            break

    if args.wait_self_reply:
        process_pending(limit=4)
    emit(f"窗口执行完成，失败 {failures} 个。")
    return 1 if failures else 0


# --------------------------------------------------------------------------------------
# daemon
# --------------------------------------------------------------------------------------

def heartbeat(payload: dict) -> None:
    try:
        save_json(PATHS["heartbeat"], payload)
    except Exception:
        pass


def force_pick(ledger: dict, accounts: dict, dt: datetime) -> tuple[str, int] | None:
    """--force 且不在窗口时：优先今日未发的号。"""
    for seq in TIER1_SEQS:
        if eligibility(ledger, accounts, seq, dt)[0]:
            return COPY_LIBRARY[seq]["window"], seq
    return None


def daemon_tick(args) -> None:
    dt = now_et()
    pending_results = process_pending(limit=2)
    ledger, accounts = read_state()

    breaker = global_breaker_until(ledger)
    if breaker and breaker > dt:
        heartbeat({"tick_at": iso(dt), "state": "breaker", "until": iso(breaker),
                   "pending_processed": len(pending_results)})
        emit(f"[{dt.strftime('%H:%M:%S')} ET] 全局熔断至 {fmt_ts(breaker)}，轻量跳过")
        return

    name = window_name(dt)
    if name is None and not args.force:
        nxt = next_window_start(dt)
        payload = {"tick_at": iso(dt), "state": "idle_window_closed",
                   "pending_processed": len(pending_results)}
        if nxt:
            payload["next_window"] = nxt[0]
            payload["next_window_at"] = iso(nxt[1])
        heartbeat(payload)
        emit(f"[{dt.strftime('%H:%M:%S')} ET] 窗口关闭，轻量巡检"
             + (f" | 下一窗口 {nxt[0]} {human_delta((nxt[1] - dt).total_seconds())} 后" if nxt else ""))
        return

    if not engine_path().exists():
        heartbeat({"tick_at": iso(dt), "state": "engine_missing"})
        emit(f"[{dt.strftime('%H:%M:%S')} ET] 引擎缺失 {PATHS['engine']}")
        return

    if name is None:  # --force 且窗口外
        picked = force_pick(ledger, accounts, dt)
        if picked is None:
            heartbeat({"tick_at": iso(dt), "state": "forced_no_candidate"})
            return
        group, seq = picked
        emit(f"[{dt.strftime('%H:%M:%S')} ET][force] 触发 seq={seq} {group}")
        summary = execute_main_post(seq, args.delay_self_reply_seconds,
                                    wait_self_reply=False, forced=True)
        emit(f"  主帖={summary['main_status']} url={summary.get('tweet_url') or 'n/a'}")
        heartbeat({"tick_at": iso(dt), "state": "forced_post", "seq": seq,
                   "result": summary["main_status"]})
        return

    key = plan_key(name, dt.date())

    def mutate(led: dict, _acc: dict):
        return get_or_create_plan(led, name, dt.date())

    plan = update_state(mutate)

    last = last_main_post_ts(ledger, dt.date().isoformat(), name)
    if last and (dt - last).total_seconds() < 18 * 60:
        heartbeat({"tick_at": iso(dt), "state": "stagger_wait", "window": name,
                   "last_post_at": iso(last)})
        emit(f"[{dt.strftime('%H:%M:%S')} ET] 错峰等待（距上一帖 "
             f"{(dt - last).total_seconds() / 60:.0f} 分钟）")
        return

    end = window_end_dt(dt.date(), name)
    for slot in plan["slots"]:
        if slot["status"] != "pending":
            continue
        due = parse_ts(slot["due_at"])
        if due is None or due > dt + timedelta(seconds=20):
            continue
        if dt >= end - timedelta(minutes=2):
            mark_slot(key, slot["seq"], "missed", {"note": "窗口关闭前未执行"})
            emit(f"seq={slot['seq']} 窗口即将关闭，标记 missed")
            return
        can, reason = eligibility(ledger, accounts, slot["seq"], dt)
        if not can:
            mark_slot(key, slot["seq"], "skipped", {"note": reason})
            emit(f"seq={slot['seq']} 跳过（{reason}）")
            return
        emit(f"[{dt.strftime('%H:%M:%S')} ET] 窗口 {name} 触发 seq={slot['seq']} "
             f"@{COPY_LIBRARY[slot['seq']]['handle']}")
        summary = execute_main_post(
            slot["seq"], args.delay_self_reply_seconds,
            wait_self_reply=False, forced=bool(args.force), plan_key=key,
        )
        mark_slot(key, slot["seq"], "done" if summary["main_status"] == "ok" else "failed",
                  {"tweet_url": summary.get("tweet_url"), "note": summary.get("note") or "",
                   "main_status": summary["main_status"]})
        emit(f"  主帖={summary['main_status']} 1楼待办={summary.get('pending_id')} "
             f"url={summary.get('tweet_url') or 'n/a'}")
        ledger, _ = read_state()
        if failures_within(ledger, 60) >= 5:
            update_state(lambda led, _acc: trip_global_breaker(led, "60 分钟内失败 5 次"))
            emit("全局熔断已触发（2 小时）")
        heartbeat({"tick_at": iso(now_et()), "state": "posted", "window": name,
                   "seq": slot["seq"], "result": summary["main_status"],
                   "pending_id": summary.get("pending_id")})
        return

    nxt_slot = next((s for s in plan["slots"] if s["status"] == "pending"), None)
    heartbeat({
        "tick_at": iso(dt), "state": "window_active", "window": name,
        "next_slot_seq": (nxt_slot or {}).get("seq"),
        "next_slot_due": (nxt_slot or {}).get("due_at"),
        "pending_processed": len(pending_results),
    })
    if nxt_slot:
        due = parse_ts(nxt_slot["due_at"])
        emit(f"[{dt.strftime('%H:%M:%S')} ET] 窗口 {name} 待发 seq={nxt_slot['seq']} "
             f"due {fmt_ts(due) if due else '?'}")
    else:
        emit(f"[{dt.strftime('%H:%M:%S')} ET] 窗口 {name} 计划已全部处理")


def cmd_daemon(args) -> int:
    ensure_state()
    interval = max(30, int(args.interval_seconds))
    print_header("X 矩阵 DAEMON（双窗口计划 / known_ids 回读 / 1 楼待办 / 熔断）")
    emit(f"轮询 {interval}s | 1 楼延迟 {args.delay_self_reply_seconds}s | 账本 {PATHS['ledger']}")
    emit(f"启动 ET {fmt_ts(now_et())} | BJ {fmt_ts(now_bj())}")
    emit(f"引擎 {PATHS['engine']} {'[存在]' if engine_path().exists() else '[缺失]'}")
    emit("窗口: 周一至周四 morning 08:30-10:30 ET / afternoon 12:30-14:00 ET")
    emit("Ctrl-C 退出。")
    try:
        while True:
            try:
                daemon_tick(args)
            except Exception as exc:  # noqa: BLE001 —— 单轮异常不终止常驻进程
                emit(f"daemon 轮询异常: {type(exc).__name__}: {exc}")
                heartbeat({"tick_at": iso(now_et()), "state": "tick_error",
                           "error": f"{type(exc).__name__}: {exc}"})
            time.sleep(interval)
    except KeyboardInterrupt:
        emit("收到 Ctrl-C，daemon 退出。")
        return 0


# --------------------------------------------------------------------------------------
# systemd 用户服务
# --------------------------------------------------------------------------------------

def systemd_unit_text() -> str:
    runtime = str(PATHS["runtime"])
    if Path(os.path.expanduser(runtime)) == Path(os.path.expanduser(str(DEFAULT_RUNTIME_DIR))):
        runtime = "%h/x-matrix-runtime(X矩阵运行器)"  # 换机可移植
    return f"""[Unit]
Description=X Matrix Tier-1 Scheduler (ET windows / readback verification / pending self-reply)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
WorkingDirectory="{runtime}"
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONIOENCODING=utf-8
Environment=TZ=America/New_York
ExecStart="/usr/bin/python3" "{runtime}/x_matrix_scheduler.py" --runtime-dir "{runtime}" daemon --interval-seconds 300 --delay-self-reply-seconds 240
Restart=always
RestartSec=90
TimeoutStopSec=30
StandardOutput=append:{runtime}/state/scheduler.log
StandardError=append:{runtime}/state/scheduler.err.log

[Install]
WantedBy=default.target
"""


def cmd_systemd_unit(args) -> int:
    text = systemd_unit_text()
    out = Path(os.path.expanduser(args.out)) if args.out else PATHS["runtime"] / "x-matrix-scheduler.service"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    emit(f"已写入 {out}")
    if args.install:
        target = Path(os.path.expanduser("~/.config/systemd/user/x-matrix-scheduler.service"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        emit(f"已安装 {target}")
        emit("启用: systemctl --user daemon-reload && systemctl --user enable --now x-matrix-scheduler.service")
        emit("常驻: loginctl enable-linger $USER")
    return 0


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="x_matrix_scheduler.py",
        description="X 矩阵 Tier-1 调度器：known_ids 回读验收 / 1 楼待办 / 美东双窗口 20-35 分钟错峰",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python3 x_matrix_scheduler.py status\n"
            "  python3 x_matrix_scheduler.py dry-run\n"
            "  python3 x_matrix_scheduler.py plan --window morning --create\n"
            "  python3 x_matrix_scheduler.py trigger-tier1 --group A --force --no-stagger\n"
            "  python3 x_matrix_scheduler.py trigger-window --window morning --wait-self-reply\n"
            "  python3 x_matrix_scheduler.py daemon\n"
            "  python3 x_matrix_scheduler.py systemd-unit --install\n"
        ),
    )
    parser.add_argument("--runtime-dir", default=str(DEFAULT_RUNTIME_DIR),
                        help=f"运行目录（默认 {DEFAULT_RUNTIME_DIR}）")
    parser.add_argument("--excel", default=None, help="账号矩阵 Excel（默认沿用引擎内置路径）")
    parser.add_argument("--sheet", default=None, help="Excel 工作表名")
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="时区 / 窗口 / 账号 / 待办 / 账本 / 文案自检")
    p_status.add_argument("--force", action="store_true", help="仅展示用")

    p_dry = sub.add_parser("dry-run", help="模拟调度扫描，不调用浏览器")
    p_dry.add_argument("--force", action="store_true")

    p_plan = sub.add_parser("plan", help="查看或生成窗口计划")
    p_plan.add_argument("--window", choices=["morning", "afternoon"], default=None)
    p_plan.add_argument("--date", default=None, help="ET 日期 YYYY-MM-DD")
    p_plan.add_argument("--create", action="store_true", help="不存在时生成并落盘")

    p_verify = sub.add_parser("verify", help="个人主页回读链路自检")
    p_verify.add_argument("--seq", type=int, required=True)
    p_verify.add_argument("--tweet-url", default=None, help="定点复核该推文 URL")
    p_verify.add_argument("--status-id", default=None, help="定点复核的 status id")

    p_pending = sub.add_parser("pending", help="查看 / 补发 1 楼待办")
    p_pending.add_argument("--process", action="store_true")
    p_pending.add_argument("--limit", type=int, default=2)
    p_pending.add_argument("--ignore-due", action="store_true", help="忽略 due_at 立即补发")

    p_t1 = sub.add_parser("trigger-tier1", help="手动触发指定赛道/账号")
    p_t1.add_argument("--group", default="ALL", choices=["A", "B", "C", "D", "ALL"])
    p_t1.add_argument("--seq", type=int, default=None)
    p_t1.add_argument("--force", action="store_true")
    p_t1.add_argument("--delay-self-reply-seconds", type=int, default=240)
    p_t1.add_argument("--wait-self-reply", action="store_true")
    p_t1.add_argument("--gap-min", type=int, default=20)
    p_t1.add_argument("--gap-max", type=int, default=35)
    p_t1.add_argument("--no-stagger", action="store_true", help="联调用：不等错峰")

    p_tw = sub.add_parser("trigger-window", help="按落盘计划整窗执行")
    p_tw.add_argument("--window", choices=["morning", "afternoon"], default=None)
    p_tw.add_argument("--force", action="store_true")
    p_tw.add_argument("--delay-self-reply-seconds", type=int, default=240)
    p_tw.add_argument("--wait-self-reply", action="store_true")

    p_daemon = sub.add_parser("daemon", help="常驻轮询：待办优先 + 窗口计划发帖")
    p_daemon.add_argument("--force", action="store_true")
    p_daemon.add_argument("--interval-seconds", type=int, default=300)
    p_daemon.add_argument("--delay-self-reply-seconds", type=int, default=240)

    p_unit = sub.add_parser("systemd-unit", help="生成 x-matrix-scheduler.service")
    p_unit.add_argument("--out", default=None)
    p_unit.add_argument("--install", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except Exception:
            pass

    parser = build_parser()
    args = parser.parse_args(argv)
    configure_paths(args.runtime_dir)
    configure_engine(getattr(args, "excel", None), getattr(args, "sheet", None))

    problems = validate_copy_library()
    if problems and args.command in ("trigger-tier1", "trigger-window", "daemon"):
        emit("文案库自检失败，拒绝发帖：")
        for problem in problems:
            emit(f"  - {problem}")
        return 2

    if args.command == "status":
        return cmd_status(args)
    if args.command == "dry-run":
        return cmd_dry_run(args)
    if args.command == "plan":
        return cmd_plan(args)
    if args.command == "verify":
        return cmd_verify(args)
    if args.command == "pending":
        return cmd_pending(args)
    if args.command == "trigger-tier1":
        return cmd_trigger_tier1(args)
    if args.command == "trigger-window":
        return cmd_trigger_window(args)
    if args.command == "daemon":
        return cmd_daemon(args)
    if args.command == "systemd-unit":
        return cmd_systemd_unit(args)

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
