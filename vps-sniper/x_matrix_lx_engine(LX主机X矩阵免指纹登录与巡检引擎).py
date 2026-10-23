#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LX 主机 X 100 账号矩阵：代理巡检换 IP / 本地 SOCKS5 免密桥接 / Patchright 独立 Profile + 2FA 自动登录引擎。"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import select
import socket
import struct
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from urllib import request as urlrequest
from urllib import error as urlerror

# --------------------------------------------------------------------------------------
# 常量
# --------------------------------------------------------------------------------------

DEFAULT_EXCEL = "~/x-matrix-runtime(X矩阵运行器)/x_100_2fa_matrix_ready.xlsx"
DEFAULT_SHEET = "主表_100个带2FA账号"
DEFAULT_RUNTIME_ROOT = "~/x-matrix-runtime(X矩阵运行器)"

SYSTEM_LIB_DIR = "/home/kais/.local/sysroot/usr/lib/x86_64-linux-gnu"

WEBSHARE_REPLACE_URL = "https://proxy.webshare.io/api/v2/proxy/replace/"
EXIT_IP_URL = "https://ipv4.webshare.io/"
MAX_WORKERS = 16
CURL_TIMEOUT = 8

LOGIN_URL = "https://x.com/i/flow/login"
HOME_URL = "https://x.com/home"
COMPOSE_URL = "https://x.com/compose/post"

LOGGED_IN_SELECTORS = (
    '[data-testid="AppTabBar_Home_Link"]',
    '[data-testid="SideNav_AccountSwitcher_Button"]',
    '[data-testid="tweetTextarea_0"]',
    '[data-testid="AppTabBar_Profile_Link"]',
    '[data-testid="editProfileButton"]',
    '[aria-label="Account menu"]',
)

IPV4_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")


# --------------------------------------------------------------------------------------
# 基础工具 (日志脱敏 / 掩码 / 时间)
# --------------------------------------------------------------------------------------

def log(msg: str) -> None:
    """运行日志一律走 stderr, 便于 stdout 只输出 JSON 结果。"""
    sys.stderr.write("[x-matrix] %s\n" % msg)
    sys.stderr.flush()


def mask_ip(ip: str) -> str:
    """出口 IP 只保留首段与尾段, 避免完整 IP 落日志。"""
    if not ip or not IPV4_RE.match(ip):
        return "hidden"
    parts = ip.split(".")
    return "%s.%s.*.*" % (parts[0], parts[1])


def mask_proxy(proxy) -> str:
    """代理只显示 host:port, 口令永不出现。"""
    if not proxy:
        return "none"
    return "%s:%s" % (proxy[0], proxy[1])


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sleep_s(seconds: float) -> None:
    time.sleep(seconds)


def emit_json(payload) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


# --------------------------------------------------------------------------------------
# Excel 载入 (只读, 列名容错)
# --------------------------------------------------------------------------------------

def _norm(name: str) -> str:
    s = str(name).strip().lower()
    for ch in (" ", "-", "_", "\t", "（", "）", "(", ")", "：", ":", "*", "/"):
        s = s.replace(ch, "")
    return s


COLUMN_CANDIDATES = {
    "username": ("用户名", "username", "账号", "handle", "user", "screenname"),
    "password": ("密码", "password", "pass", "pwd"),
    "twofa": ("2fa秘钥", "2fa密钥", "2fa", "twofa", "totp", "totpsecret", "secret", "双重验证秘钥"),
    "cookie": ("cookie", "cookies", "cookie串", "cookie值"),
    "ua": ("useragent", "ua", "浏览器ua", "useragent字符串"),
    "viewport": ("窗口尺寸", "viewport", "windowsize", "分辨率", "尺寸"),
    "proxy": ("代理信息", "proxy", "代理", "socks5", "代理地址"),
    "email": ("emailaddress", "email", "邮箱", "邮件地址"),
    "profile": ("独立profile目录名", "profile", "profiledir", "profile目录", "目录名"),
    "group": ("cps赛道分组", "分组", "group", "赛道", "赛道分组"),
    "tier": ("矩阵层级", "层级", "tier", "level"),
}


def resolve_columns(df) -> dict:
    """把 Excel 实际列名映射成内部字段名, 支持精确 / 包含匹配。"""
    mapping = {}
    normalized = {_norm(c): c for c in df.columns}
    for field, candidates in COLUMN_CANDIDATES.items():
        hit = None
        for cand in candidates:
            key = _norm(cand)
            if key in normalized:
                hit = normalized[key]
                break
        if hit is None:
            for key, origin in normalized.items():
                if any(_norm(cand) in key or key in _norm(cand) for cand in candidates):
                    hit = origin
                    break
        if hit is not None:
            mapping[field] = hit
    return mapping


def load_matrix(excel_path: str, sheet_name: str):
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("缺少依赖 pandas: %s" % exc)

    path = Path(os.path.expanduser(excel_path))
    if not path.exists():
        raise SystemExit("Excel 不存在: %s" % path)

    # 只读读取, 任何情况下都不写回
    df = pd.read_excel(str(path), sheet_name=sheet_name, dtype=str, keep_default_na=False)
    if df.empty:
        raise SystemExit("Excel 为空: %s / %s" % (path, sheet_name))
    return df


def build_records(df) -> list:
    cols = resolve_columns(df)
    missing = [f for f in ("username", "password", "proxy") if f not in cols]
    if missing:
        raise SystemExit("Excel 缺少必需列: %s" % ", ".join(missing))

    records = []
    for idx, row in df.iterrows():
        rec = {"seq": len(records) + 1}
        for field in COLUMN_CANDIDATES:
            column = cols.get(field)
            value = "" if column is None else str(row.get(column, "") or "")
            rec[field] = value.strip()
        records.append(rec)
    return records


def parse_viewport(raw: str, default=(1440, 900)) -> dict:
    nums = re.findall(r"\d+", raw or "")
    if len(nums) >= 2:
        w, h = int(nums[0]), int(nums[1])
        if 600 <= w <= 4000 and 500 <= h <= 4000:
            return {"width": w, "height": h}
    return {"width": default[0], "height": default[1]}


def parse_proxy(raw: str):
    s = str(raw or "").strip()
    if not s or s.lower() in ("nan", "none", "null"):
        return None
    s = re.sub(r"^(?:socks5h?|socks4a?|https?)://", "", s, flags=re.IGNORECASE).strip()
    parts = s.split(":")
    if len(parts) < 4:
        return None
    host, port, user = parts[0].strip(), parts[1].strip(), parts[2]
    password = ":".join(parts[3:])
    try:
        port_i = int(port)
    except (TypeError, ValueError):
        return None
    if not host or not (0 < port_i < 65536):
        return None
    return host, port_i, user, password


def normalize_group(raw: str) -> str:
    s = str(raw or "").strip().upper()
    m = re.search(r"[ABCD]", s)
    return m.group(0) if m else "未分组"


def normalize_tier(raw: str) -> str:
    s = str(raw or "").strip().lower()
    m = re.search(r"[1-3]", s)
    return "Tier%s" % m.group(0) if m else "未分层"


# --------------------------------------------------------------------------------------
# 代理探测 (curl + 并发)
# --------------------------------------------------------------------------------------

def curl_probe(proxy, timeout: int = CURL_TIMEOUT):
    """用 curl 走 SOCKS5(带账密) 请求 ipv4.webshare.io, 返回出口 IP 或 None。"""
    if not proxy:
        return None
    host, port, user, password = proxy
    cmd = [
        "curl", "-sS", "-m", str(timeout),
        "--socks5-hostname", "%s:%s" % (host, port),
        "-U", "%s:%s" % (user, password),
        EXIT_IP_URL,
    ]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout + 6, check=False
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode != 0:
        return None
    lines = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
    if not lines:
        return None
    ip = lines[-1]
    return ip if IPV4_RE.match(ip) else None


def probe_with_retry(proxy):
    """第 1 次失败自动重试 1 次。"""
    if not proxy:
        return None
    ip = curl_probe(proxy)
    if ip:
        return ip
    return curl_probe(proxy)


def webshare_resolve_slot_ip(api_key: str, user_str: str, fallback_ip: str) -> str:
    """若代理为 Webshare 主干模式 (username 以 -N 结尾), 从 direct 列表解析第 N 个静态 IP。"""
    m = re.search(r"-(\d+)$", user_str or "")
    if not m:
        return fallback_ip
    slot_idx = int(m.group(1)) - 1
    req = urlrequest.Request(
        "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page_size=100",
        headers={"Authorization": "Token %s" % api_key},
    )
    try:
        with urlrequest.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
            results = data.get("results") if isinstance(data, dict) else data
            if isinstance(results, list) and 0 <= slot_idx < len(results):
                addr = results[slot_idx].get("proxy_address")
                if addr:
                    return str(addr)
    except Exception:
        pass
    return fallback_ip


def webshare_replace(api_key: str, proxy_ip: str, user_str: str = ""):
    """调用 Webshare v2 replace 接口, 仅返回 (status, 短响应摘要)。"""
    target_ip = webshare_resolve_slot_ip(api_key, user_str, proxy_ip)
    body = {
        "to_replace": {"type": "ip_address", "ip_addresses": [target_ip]},
        "replace_with": [{"type": "country", "country_code": "US", "count": 1}],
    }
    data = json.dumps(body).encode("utf-8")
    req = urlrequest.Request(
        WEBSHARE_REPLACE_URL,
        data=data,
        method="POST",
        headers={
            "Authorization": "Token %s" % api_key,
            "Content-Type": "application/json",
        },
    )
    try:
        with urlrequest.urlopen(req, timeout=30) as resp:
            return resp.status, (resp.read(400).decode("utf-8", "replace") or "")[:200]
    except urlerror.HTTPError as exc:
        return exc.code, (exc.read(400).decode("utf-8", "replace") or "")[:200]
    except (urlerror.URLError, OSError) as exc:
        return None, str(exc)[:200]


def cmd_check_proxies(args) -> int:
    df = load_matrix(args.excel, args.sheet)
    records = build_records(df)
    proxies = [parse_proxy(r["proxy"]) for r in records]
    total = len(records)

    results = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(probe_with_retry, p): i for i, p in enumerate(proxies)}
        for fut in as_completed(futures):
            idx = futures[fut]
            try:
                results[idx] = fut.result()
            except Exception:  # 单点异常不拖垮整批
                results[idx] = None

    ok_ips = [ip for ip in results.values() if ip]
    failed_indices = [i + 1 for i in range(total) if not results.get(i)]
    unique_ips = len(set(ok_ips))

    replaced, replace_errors = [], []
    api_key = (os.environ.get("WEBSHARE_API_KEY") or "").strip()
    want_replace = bool(api_key) or bool(args.auto_replace)
    if failed_indices and want_replace:
        if not api_key:
            replace_errors.append({"error": "WEBSHARE_API_KEY 缺失, 跳过自动替换"})
        else:
            for seq in failed_indices:
                proxy = proxies[seq - 1]
                if not proxy:
                    replace_errors.append({"seq": seq, "error": "代理信息格式非法"})
                    continue
                status, summary = webshare_replace(api_key, proxy[0], proxy[2])
                if status == 200:
                    replaced.append({"seq": seq, "proxy": mask_proxy(proxy)})
                else:
                    replace_errors.append(
                        {"seq": seq, "proxy": mask_proxy(proxy), "status": status,
                         "detail": summary}
                    )
            log("Webshare 替换完成: 成功 %d / 失败 %d" % (len(replaced), len(replace_errors)))

    payload = {
        "total": total,
        "ok": len(ok_ips),
        "unique_exit_ips": unique_ips,
        "failed": failed_indices,
        "replaced": replaced,
        "replace_errors": replace_errors[:20],
    }
    emit_json(payload)
    return 0


# --------------------------------------------------------------------------------------
# 本地 SOCKS5 免密桥接 (Chromium 不支持带账密 SOCKS5)
# --------------------------------------------------------------------------------------

def _recv_exact(sock, n: int, timeout: float = 30.0):
    sock.settimeout(timeout)
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


class Socks5AuthBridge:
    """127.0.0.1:<随机端口> 免密 SOCKS5 -> 上游 host:port + 用户名/密码认证。"""

    def __init__(self, up_host: str, up_port: int, up_user: str, up_pass: str):
        self.up_host = up_host
        self.up_port = int(up_port)
        self.up_user = up_user or ""
        self.up_pass = up_pass or ""
        self.port = 0
        self._srv = None
        self._stop = threading.Event()
        self._thread = None

    # -- 生命周期 ------------------------------------------------------------------
    def start(self) -> int:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 0))
        sock.listen(128)
        self._srv = sock
        self.port = sock.getsockname()[1]
        self._thread = threading.Thread(target=self._accept_loop, name="socks-bridge", daemon=True)
        self._thread.start()
        return self.port

    def stop(self) -> None:
        self._stop.set()
        try:
            if self._srv is not None:
                self._srv.close()
        except OSError:
            pass
        self._srv = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()
        return False

    # -- 接受连接 ------------------------------------------------------------------
    def _accept_loop(self) -> None:
        while not self._stop.is_set():
            try:
                client, _ = self._srv.accept()
            except (OSError, AttributeError):
                return
            threading.Thread(target=self._handle, args=(client,), daemon=True).start()

    # -- 单连接处理 ----------------------------------------------------------------
    def _handle(self, client) -> None:
        upstream = None
        try:
            client.settimeout(30)
            head = _recv_exact(client, 2)
            if not head or head[0] != 0x05:
                return
            nmethods = head[1]
            if nmethods:
                if not _recv_exact(client, nmethods):
                    return
            client.sendall(b"\x05\x00")  # 免密

            req = _recv_exact(client, 4)
            if not req or req[0] != 0x05 or req[1] != 0x01:  # 仅 CONNECT
                return
            atyp = req[3]
            if atyp == 0x01:
                raw = _recv_exact(client, 4)
                if not raw:
                    return
                host = socket.inet_ntoa(raw)
            elif atyp == 0x03:
                ln = _recv_exact(client, 1)
                if not ln:
                    return
                raw = _recv_exact(client, ln[0])
                if raw is None:
                    return
                host = raw.decode("utf-8", "replace")
            elif atyp == 0x04:
                raw = _recv_exact(client, 16)
                if not raw:
                    return
                host = socket.inet_ntop(socket.AF_INET6, raw)
            else:
                return
            port_raw = _recv_exact(client, 2)
            if not port_raw:
                return
            target_port = struct.unpack("!H", port_raw)[0]

            upstream = socket.create_connection((self.up_host, self.up_port), timeout=20)
            upstream.settimeout(20)

            # 上游认证握手: 仅支持 0x02 用户名/密码
            upstream.sendall(b"\x05\x01\x02")
            sel = _recv_exact(upstream, 2)
            if not sel or sel[1] == 0xFF:
                return
            if sel[1] == 0x02:
                user_b = self.up_user.encode("utf-8")
                pass_b = self.up_pass.encode("utf-8")
                upstream.sendall(
                    b"\x01" + bytes([len(user_b)]) + user_b + bytes([len(pass_b)]) + pass_b
                )
                ar = _recv_exact(upstream, 2)
                if not ar or ar[1] != 0x00:
                    return

            # 转发 CONNECT
            if atyp == 0x01:
                addr = b"\x01" + socket.inet_aton(host)
            elif atyp == 0x03:
                hb = host.encode("utf-8")
                addr = b"\x03" + bytes([len(hb)]) + hb
            else:
                addr = b"\x04" + socket.inet_pton(socket.AF_INET6, host)
            upstream.sendall(b"\x05\x01\x00" + addr + struct.pack("!H", target_port))

            rep = _recv_exact(upstream, 4)
            if not rep or rep[1] != 0x00:
                client.sendall(b"\x05\x01\x00\x01\x00\x00\x00\x00\x00\x00")
                return
            # 吃掉上游 BND.ADDR + BND.PORT
            if rep[3] == 0x01:
                _recv_exact(upstream, 6)
            elif rep[3] == 0x03:
                ln = _recv_exact(upstream, 1)
                if ln:
                    _recv_exact(upstream, ln[0] + 2)
            elif rep[3] == 0x04:
                _recv_exact(upstream, 18)

            client.sendall(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
            client.settimeout(None)
            upstream.settimeout(None)
            self._relay(client, upstream)
        except (OSError, ValueError, struct.error, IndexError):
            return
        finally:
            for sock in (client, upstream):
                if sock is None:
                    continue
                try:
                    sock.close()
                except OSError:
                    pass

    # -- 双向转发 ------------------------------------------------------------------
    def _relay(self, a, b) -> None:
        socks = [a, b]
        try:
            while not self._stop.is_set():
                readable, _, broken = select.select(socks, [], socks, 30)
                if broken:
                    return
                if not readable:
                    continue
                for src in readable:
                    try:
                        data = src.recv(65536)
                    except OSError:
                        return
                    if not data:
                        return
                    (b if src is a else a).sendall(data)
        except (OSError, ValueError):
            return


# --------------------------------------------------------------------------------------
# Patchright 浏览器公共部分
# --------------------------------------------------------------------------------------

def ensure_ld_library_path() -> None:
    current = os.environ.get("LD_LIBRARY_PATH", "")
    entries = [p for p in current.split(":") if p]
    if SYSTEM_LIB_DIR not in entries and os.path.isdir(SYSTEM_LIB_DIR):
        new_ld = SYSTEM_LIB_DIR + ((":" + current) if current else "")
        os.environ["LD_LIBRARY_PATH"] = new_ld
        if not os.environ.get("_LD_REEXEC") and os.path.isfile(sys.argv[0]):
            os.environ["_LD_REEXEC"] = "1"
            os.execvpe(sys.executable, [sys.executable] + sys.argv, os.environ)


def cookie_file(runtime_root: Path, seq: int) -> Path:
    return runtime_root / "cookies" / ("profile_%03d.json" % seq)


def state_file(runtime_root: Path) -> Path:
    return runtime_root / "state" / "accounts_state.json"


def profile_dir(runtime_root: Path, seq: int, raw_name: str) -> Path:
    name = (raw_name or "").strip()
    if not name:
        name = "profile_%03d" % seq
    candidate = Path(os.path.expanduser(name))
    if candidate.is_absolute():
        return candidate
    safe = re.sub(r"[^0-9A-Za-z_.\-]", "_", name)
    return runtime_root / "profiles" / safe


def load_state(runtime_root: Path) -> dict:
    path = state_file(runtime_root)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(runtime_root: Path, state: dict) -> None:
    path = state_file(runtime_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(str(tmp), str(path))


_CLEAN_COOKIE_FIELDS = ("name", "value", "domain", "path", "expires", "httpOnly", "secure", "sameSite")


def normalize_samesite(value):
    s = str(value or "").strip().lower()
    if s in ("strict", "s"):
        return "Strict"
    if s in ("lax", "d", ""):
        return "Lax"
    if s in ("none", "no_restriction", "no_restrictions", "n"):
        return "None"
    if s in ("unspecified", "u", "-1"):
        return "Lax"
    return "Lax"


def clean_cookies(raw_cookies) -> list:
    """只保留 Playwright 支持的字段, 并清理过期 Cookie。"""
    cleaned = []
    now = time.time()
    for item in raw_cookies or []:
        if not isinstance(item, dict):
            continue
        entry = {}
        for field in _CLEAN_COOKIE_FIELDS:
            if field in item:
                entry[field] = item[field]
        if not entry.get("name") or not entry.get("domain"):
            continue
        entry["path"] = entry.get("path") or "/"
        entry["httpOnly"] = bool(entry.get("httpOnly", False))
        entry["secure"] = bool(entry.get("secure", False))
        entry["sameSite"] = normalize_samesite(entry.get("sameSite"))
        expires = entry.get("expires", -1)
        try:
            expires = float(expires)
        except (TypeError, ValueError):
            expires = -1
        if expires > 0 and expires < now - 60:
            continue  # 丢弃已过期 Cookie, 避免 add_cookies 报错
        if expires <= 0:
            entry.pop("expires", None)
        else:
            entry["expires"] = expires
        if entry["sameSite"] == "None" and not entry["secure"]:
            entry["secure"] = True  # 浏览器强制 SameSite=None 必须 Secure
        cleaned.append(entry)
    return cleaned


def load_cookies_for_seq(rec: dict, runtime_root: Path) -> list:
    local = cookie_file(runtime_root, rec["seq"])
    if local.exists():
        try:
            data = json.loads(local.read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                return clean_cookies(data)
        except (json.JSONDecodeError, OSError):
            log("seq=%d 本地 Cookie 文件解析失败, 回退 Excel Cookie" % rec["seq"])

    raw = (rec.get("cookie") or "").strip()
    if raw.startswith("["):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return clean_cookies(parsed)
        except json.JSONDecodeError:
            log("seq=%d Excel Cookie 列不是合法 JSON, 跳过注入" % rec["seq"])
    return []


def inject_cookies(context, cookies: list) -> int:
    if not cookies:
        return 0
    try:
        context.add_cookies(cookies)
        return len(cookies)
    except Exception as exc:  # Cookie 不合规不应阻断登录流程
        log("Cookie 注入失败(已忽略, 改为纯密码登录): %s" % type(exc).__name__)
        return 0


FULL_CHROME_CANDIDATES = (
    Path(os.path.expanduser("~/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome")),
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/chromium-browser"),
    Path("/usr/bin/chromium"),
)


def find_chrome_executable() -> str | None:
    for cand in FULL_CHROME_CANDIDATES:
        if cand.exists() and os.access(str(cand), os.X_OK):
            return str(cand)
    return None


def launch_context(playwright, profile_path: Path, local_port: int, ua: str, viewport: dict):
    profile_path.mkdir(parents=True, exist_ok=True)
    chrome_bin = find_chrome_executable()
    clean_ua = re.sub(r"HeadlessChrome", "Chrome", ua or "").strip()
    if not clean_ua:
        clean_ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    kwargs = dict(
        user_data_dir=str(profile_path),
        headless=True,
        user_agent=clean_ua,
        proxy={"server": "socks5://127.0.0.1:%d" % local_port},
        viewport={"width": int(viewport["width"]), "height": int(viewport["height"])},
        locale="en-US",
        args=[
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
        ],
    )
    if chrome_bin:
        kwargs["executable_path"] = chrome_bin
    return playwright.chromium.launch_persistent_context(**kwargs)


def first_page(context):
    return context.pages[0] if context.pages else context.new_page()


def safe_goto(page, url: str, timeout: int = 35000) -> bool:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        return True
    except Exception as exc:
        log("打开 %s 失败: %s" % (url, type(exc).__name__))
        return False


def query_any(page, selectors):
    for sel in selectors:
        try:
            node = page.query_selector(sel)
            if node:
                return node
        except Exception:
            continue
    return None


def is_logged_in(page) -> bool:
    try:
        url = (page.url or "")
    except Exception:
        url = ""
    if "/login" in url or "/i/flow/login" in url or "/onboarding" in url:
        return False
    # 必须实际在 DOM 中检测到登录态专属组件，严禁仅看 URL 判定
    return query_any(page, LOGGED_IN_SELECTORS) is not None


def read_exit_ip(page):
    """访问 ipv4.webshare.io 读取出口 IP, 返回 (verified, ip)。"""
    if not safe_goto(page, EXIT_IP_URL, timeout=20000):
        return False, None
    try:
        body = (page.inner_text("body") or "").strip()
    except Exception:
        body = ""
    ip = ""
    for token in re.split(r"\s+", body):
        if IPV4_RE.match(token):
            ip = token
            break
    sleep_s(1.0)
    return (bool(ip), ip)


def totp_code(secret: str) -> str:
    import pyotp

    normalized = re.sub(r"\s+", "", secret or "")
    if not normalized:
        return ""
    return pyotp.TOTP(normalized).now()


def _wait_login_input(page, timeout: int):
    """等待用户名输入框, 覆盖 X 2026 最新 DOM 及全套选择器。"""
    selectors = (
        'input[name="username_or_email"]',
        'input[autocomplete~="username"]',
        'input[autocomplete*="username"]',
        'input[autocomplete="username"]',
        'input[name="text"]',
        'input[data-testid="ocfEnterTextTextInput"]',
        'input[type="text"]',
    )
    for index, sel in enumerate(selectors):
        try:
            page.wait_for_selector(sel, timeout=timeout if index == 0 else 1500)
        except Exception:
            continue
        node = page.query_selector(sel)
        if node:
            return node
    return None


def _is_twofa_challenge(page) -> bool:
    if query_any(page, ('input[name="password"]', 'input[type="password"]')) is not None:
        return False
    return query_any(
        page, (
            'input[data-testid="ocfEnterTextTextInput"]',
            'input[name="text"]',
            'input[autocomplete="one-time-code"]',
            'input[inputmode="numeric"]',
            'input[type="text"]',
        )
    ) is not None


def perform_login(page, rec: dict) -> str:
    """登录状态机, 返回 login_method 描述字符串。"""
    username = rec["username"]
    password = rec["password"]
    twofa = rec["twofa"]
    email = rec.get("email") or ""

    if not safe_goto(page, LOGIN_URL, timeout=35000):
        return "login_page_open_failed"
    sleep_s(2.0)

    user_input = _wait_login_input(page, 25000)
    if not user_input and safe_goto(page, LOGIN_URL, timeout=35000):
        sleep_s(2.0)  # 表单偶发未渲染时重载一次
        user_input = _wait_login_input(page, 15000)
    if not user_input:
        return "username_field_missing"
    user_input.fill(username)
    sleep_s(0.5)
    user_input.press("Enter")
    sleep_s(1.0)
    try:
        next_btn = page.query_selector('button:has-text("Next"), div[role="button"]:has-text("Next")')
        if next_btn and page.query_selector('input[name="password"]') is None:
            next_btn.click()
    except Exception:
        pass
    sleep_s(2.5)

    # 异常登录核验 (要求提供邮箱或手机号)
    try:
        challenge = page.query_selector('input[data-testid="ocfEnterTextTextInput"]')
        has_password = page.query_selector('input[name="password"]') is not None
        if challenge and not has_password:
            challenge.fill(email or username)
            challenge.press("Enter")
            sleep_s(3.0)
    except Exception:
        pass

    pw_input = None
    try:
        page.wait_for_selector('input[name="password"]', timeout=25000)
        pw_input = page.query_selector('input[name="password"]')
    except Exception:
        pw_input = None
    if not pw_input:
        return "password_field_missing"
    pw_input.fill(password)
    sleep_s(0.5)
    pw_input.press("Enter")
    sleep_s(1.0)
    try:
        login_btn = page.query_selector('button:has-text("Log in"), div[role="button"]:has-text("Log in")')
        if login_btn:
            login_btn.click()
    except Exception:
        pass
    sleep_s(4.0)

    twofa_used = False
    try:
        if _is_twofa_challenge(page):
            code = totp_code(twofa)
            field = query_any(
                page, ('input[data-testid="ocfEnterTextTextInput"]', 'input[name="text"]')
            )
            if field and code:
                field.fill(code)
                sleep_s(0.5)
                field.press("Enter")
                sleep_s(1.0)
                try:
                    next_btn = page.query_selector('button:has-text("Next"), div[role="button"]:has-text("Next"), button:has-text("Confirm")')
                    if next_btn:
                        next_btn.click()
                except Exception:
                    pass
                sleep_s(5.0)
                twofa_used = True
    except Exception:
        pass

    sleep_s(1.0)
    return "password+2fa" if twofa_used else "password"


def _open_browser_session(playwright, rec: dict, runtime_root: Path, viewport: dict):
    """启动 SOCKS 桥 + persistent context, 返回 (context, page, bridge)。"""
    proxy = parse_proxy(rec["proxy"])
    if not proxy:
        raise RuntimeError("seq=%d 代理信息非法" % rec["seq"])

    ensure_ld_library_path()
    bridge = Socks5AuthBridge(proxy[0], proxy[1], proxy[2], proxy[3])
    local_port = bridge.start()
    context = None
    try:
        context = launch_context(
            playwright,
            profile_dir(runtime_root, rec["seq"], rec.get("profile") or ""),
            local_port,
            rec.get("ua") or "",
            viewport,
        )
        page = first_page(context)
        return context, page, bridge
    except Exception:
        if context is not None:
            try:
                context.close()
            except Exception:
                pass
        bridge.stop()
        raise


def _record_state(runtime_root: Path, rec: dict, **fields) -> None:
    state = load_state(runtime_root)
    key = str(rec["seq"])
    entry = state.get(key) or {}
    entry.update(
        {
            "seq": rec["seq"],
            "username": rec["username"],
            "group": normalize_group(rec.get("group")),
            "tier": normalize_tier(rec.get("tier")),
            "updated_at": utcnow_iso(),
        }
    )
    entry.update(fields)
    state[key] = entry
    save_state(runtime_root, state)


def cmd_login_smoke(args) -> int:
    from patchright.sync_api import sync_playwright

    seq = int(args.seq)
    if not 1 <= seq <= 100:
        raise SystemExit("--seq 必须在 1..100")

    runtime_root = Path(os.path.expanduser(args.runtime_root))
    records = build_records(load_matrix(args.excel, args.sheet))
    rec = records[seq - 1]
    viewport = parse_viewport(rec.get("viewport") or "")

    result = {
        "seq": seq,
        "username": rec["username"],
        "group": normalize_group(rec.get("group")),
        "tier": normalize_tier(rec.get("tier")),
        "exit_ip_verified": False,
        "login_method": None,
        "logged_in": False,
        "final_url": None,
    }

    bridge = None
    context = None
    pw_ctx = None
    try:
        pw_ctx = sync_playwright().start()
        context, page, bridge = _open_browser_session(pw_ctx, rec, runtime_root, viewport)
        page.set_default_timeout(30000)

        cookies = load_cookies_for_seq(rec, runtime_root)
        injected = inject_cookies(context, cookies)

        verified, exit_ip = read_exit_ip(page)
        result["exit_ip_verified"] = verified
        if verified:
            log("seq=%d 出口 IP 验证通过 (%s)" % (seq, mask_ip(exit_ip)))

        if not safe_goto(page, HOME_URL, timeout=35000):
            result["login_method"] = "home_open_failed"
        else:
            sleep_s(4.0)
            if is_logged_in(page):
                result["login_method"] = "cookie" if injected else "existing_session"
            else:
                result["login_method"] = perform_login(page, rec)
                sleep_s(1.0)
                safe_goto(page, HOME_URL, timeout=35000)
                sleep_s(3.0)

        logged_in = is_logged_in(page)
        result["logged_in"] = logged_in
        result["final_url"] = (page.url or "")

        if logged_in:
            try:
                cookie_path = cookie_file(runtime_root, seq)
                cookie_path.parent.mkdir(parents=True, exist_ok=True)
                cookie_path.write_text(
                    json.dumps(context.cookies(), ensure_ascii=False), encoding="utf-8"
                )
            except Exception as exc:
                log("seq=%d 保存 Cookie 失败: %s" % (seq, type(exc).__name__))
            _record_state(
                runtime_root,
                rec,
                logged_in=True,
                login_method=result["login_method"],
                exit_ip_verified=result["exit_ip_verified"],
                final_url=result["final_url"],
            )
        else:
            _record_state(
                runtime_root,
                rec,
                logged_in=False,
                login_method=result["login_method"],
                exit_ip_verified=result["exit_ip_verified"],
                final_url=result["final_url"],
            )

        emit_json(result)
        return 0 if logged_in else 2
    finally:
        if context is not None:
            try:
                context.close()
            except Exception:
                pass
        if pw_ctx is not None:
            try:
                pw_ctx.stop()
            except Exception:
                pass
        if bridge is not None:
            bridge.stop()


# --------------------------------------------------------------------------------------
# 发推 / 回复
# --------------------------------------------------------------------------------------

def _fill_tweet_box(page, text: str, timeout: int = 20000) -> bool:
    try:
        page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=timeout)
        box = page.locator('[data-testid="tweetTextarea_0"]').first
        if not box:
            return False
        box.click()
        sleep_s(0.5)
        # 参照 us-server typeLikeHuman 模拟人类击键随机延迟
        for ch in text:
            page.keyboard.insert_text(ch)
            if ch in "。！？；：.!?;:":
                sleep_s(random.uniform(0.12, 0.28))
            elif ch in "，、,. ":
                sleep_s(random.uniform(0.05, 0.12))
            else:
                sleep_s(random.uniform(0.02, 0.06))
        sleep_s(0.8)
        typed = (box.inner_text() or "").strip()
        prefix = text[:15].strip()
        if prefix and prefix not in typed:
            log("文本输入预警: 前缀未在编辑框完全出现")
        return True
    except Exception as exc:
        log("输入推文失败: %s" % type(exc).__name__)
        return False


def _submit_tweet(page, timeout: int = 15000) -> bool:
    selectors = [
        '[data-testid="tweetButton"]',
        '[data-testid="tweetButtonInline"]',
        '[role="button"]:has-text("Post")',
        '[role="button"]:has-text("发帖")',
    ]
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            loc.wait_for(state="visible", timeout=timeout)
            aria_disabled = loc.get_attribute("aria-disabled")
            if aria_disabled == "true" or loc.is_disabled():
                continue
            loc.click()
            return True
        except Exception:
            continue
    return False


def _collect_own_status_ids(page, username: str) -> set:
    """发帖前收集已有推文 ID 集合，排除置顶推文与历史推文干扰 (移植自 us-server x_browser_base)"""
    ids = set()
    try:
        if safe_goto(page, f"https://x.com/{username}", timeout=35000):
            sleep_s(2.5)
            links = page.locator(f'a[href*="/{username}/status/"]')
            count = min(links.count(), 40)
            for i in range(count):
                href = links.nth(i).get_attribute("href") or ""
                m = re.search(r'/status/(\d+)', href)
                if m:
                    ids.add(m.group(1))
    except Exception as exc:
        log(f"预读已有推文 ID 列表异常: {exc}")
    return ids


def _find_latest_own_status(page, username: str, text_snippet: str, known_ids: set, max_attempts: int = 5) -> dict:
    """发帖后在个人主页定位新产生的推文 ID 与完整 URL，并核验正文 (移植自 us-server x_browser_base)"""
    pattern = re.compile(rf'/{username}/status/(\d+)')
    target_prefix = text_snippet[:15].lower().strip()
    for attempt in range(max_attempts):
        if safe_goto(page, f"https://x.com/{username}", timeout=35000):
            sleep_s(3.0 + attempt * 1.5)
            links = page.locator(f'a[href*="/{username}/status/"]')
            count = min(links.count(), 35)
            for i in range(count):
                href = links.nth(i).get_attribute("href") or ""
                m = pattern.search(href)
                if not m:
                    continue
                status_id = m.group(1)
                if status_id not in known_ids:
                    tweet_url = f"https://x.com/{username}/status/{status_id}"
                    try:
                        article = links.nth(i).locator("xpath=ancestor::article")
                        body = (article.inner_text(timeout=3000) or "").lower()
                        if not target_prefix or target_prefix in body:
                            return {"verified": True, "status_id": status_id, "tweet_url": tweet_url}
                    except Exception:
                        return {"verified": True, "status_id": status_id, "tweet_url": tweet_url}
        sleep_s(3.0)
    return {"verified": False, "status_id": None, "tweet_url": None}


def _latest_tweet_url(page, username: str):
    if not safe_goto(page, "https://x.com/%s" % username, timeout=35000):
        return None
    sleep_s(3.0)
    try:
        link = page.locator('article[data-testid="tweet"] a[href*="/status/"]').first
        href = link.get_attribute("href", timeout=10000)
    except Exception:
        href = None
    if not href:
        return None
    if href.startswith("/"):
        return "https://x.com" + href
    if href.startswith("http"):
        return href
    return None


def cmd_post(args) -> int:
    from patchright.sync_api import sync_playwright

    seq = int(args.seq)
    if not 1 <= seq <= 100:
        raise SystemExit("--seq 必须在 1..100")

    runtime_root = Path(os.path.expanduser(args.runtime_root))
    records = build_records(load_matrix(args.excel, args.sheet))
    rec = records[seq - 1]
    viewport = parse_viewport(rec.get("viewport") or "")

    result = {
        "seq": seq,
        "username": rec["username"],
        "action": "reply" if args.reply_url else "post",
        "exit_ip_verified": False,
        "logged_in": False,
        "submitted": False,
        "verified": False,
        "tweet_url": None,
        "status_id": None,
        "self_reply_submitted": False,
        "target_url": args.reply_url or COMPOSE_URL,
        "final_url": None,
    }

    bridge = None
    context = None
    pw_ctx = None
    try:
        pw_ctx = sync_playwright().start()
        context, page, bridge = _open_browser_session(pw_ctx, rec, runtime_root, viewport)
        page.set_default_timeout(30000)

        cookies = load_cookies_for_seq(rec, runtime_root)
        inject_cookies(context, cookies)

        verified, exit_ip = read_exit_ip(page)
        result["exit_ip_verified"] = verified
        if verified:
            log("seq=%d 出口 IP 验证通过 (%s)" % (seq, mask_ip(exit_ip)))

        safe_goto(page, HOME_URL, timeout=35000)
        sleep_s(4.0)
        logged_in = is_logged_in(page)
        if not logged_in:
            method = perform_login(page, rec)
            sleep_s(1.0)
            safe_goto(page, HOME_URL, timeout=35000)
            sleep_s(3.0)
            logged_in = is_logged_in(page)
            log("seq=%d 现场登录: %s -> logged_in=%s" % (seq, method, logged_in))
            if logged_in:
                try:
                    cookie_path = cookie_file(runtime_root, seq)
                    cookie_path.parent.mkdir(parents=True, exist_ok=True)
                    cookie_path.write_text(
                        json.dumps(context.cookies(), ensure_ascii=False), encoding="utf-8"
                    )
                except Exception:
                    pass
        result["logged_in"] = logged_in

        if logged_in:
            if args.reply_url:
                if safe_goto(page, args.reply_url, timeout=35000):
                    sleep_s(3.0)
                    if _fill_tweet_box(page, args.text):
                        result["submitted"] = _submit_tweet(page)
                        sleep_s(4.0)
            else:
                # 参照 us-server：发主帖前预先收集个人主页推文 ID，用于发帖后精准差量核验
                known_ids = _collect_own_status_ids(page, rec["username"])
                if safe_goto(page, COMPOSE_URL, timeout=35000):
                    sleep_s(3.0)
                    if _fill_tweet_box(page, args.text):
                        result["submitted"] = _submit_tweet(page)
                        sleep_s(6.0)

                # 真实外部回读核验
                if result["submitted"]:
                    verify = _find_latest_own_status(page, rec["username"], args.text, known_ids)
                    if verify["verified"]:
                        result["verified"] = True
                        result["tweet_url"] = verify["tweet_url"]
                        result["status_id"] = verify["status_id"]
                        result["target_url"] = verify["tweet_url"]
                        log("seq=%d 发帖真实验收成功: %s" % (seq, verify["tweet_url"]))
                    else:
                        log("seq=%d 提交成功但未回读到新推文 URL (可能是轻微延迟)" % seq)

                if result["submitted"] and args.self_reply:
                    target_reply_url = result.get("tweet_url") or _latest_tweet_url(page, rec["username"])
                    if target_reply_url:
                        result["target_url"] = target_reply_url
                        if safe_goto(page, target_reply_url, timeout=35000):
                            sleep_s(3.0)
                            if _fill_tweet_box(page, args.self_reply):
                                result["self_reply_submitted"] = _submit_tweet(page)
                                sleep_s(4.0)
                    else:
                        log("seq=%d 未定位到推文详情 URL, 跳过现场自评" % seq)

        result["final_url"] = page.url or ""
        _record_state(
            runtime_root,
            rec,
            logged_in=logged_in,
            exit_ip_verified=result["exit_ip_verified"],
            last_action=result["action"],
            last_action_submitted=bool(
                result["submitted"] or result["self_reply_submitted"]
            ),
            final_url=result["final_url"],
        )
        emit_json(result)
        return 0 if (result["submitted"] and (result.get("verified") or not args.reply_url)) else 3
    finally:
        if context is not None:
            try:
                context.close()
            except Exception:
                pass
        if pw_ctx is not None:
            try:
                pw_ctx.stop()
            except Exception:
                pass
        if bridge is not None:
            bridge.stop()


# --------------------------------------------------------------------------------------
# 状态统计
# --------------------------------------------------------------------------------------

def cmd_update_profile(args) -> int:
    from patchright.sync_api import sync_playwright

    seq = int(args.seq)
    if not 1 <= seq <= 100:
        raise SystemExit("--seq 必须在 1..100")

    runtime_root = Path(os.path.expanduser(args.runtime_root))
    records = build_records(load_matrix(args.excel, args.sheet))
    rec = records[seq - 1]
    viewport = parse_viewport(rec.get("viewport") or "")

    result = {
        "seq": seq,
        "username": rec["username"],
        "action": "update_profile",
        "name_target": args.name,
        "bio_target": args.bio,
        "name_updated": False,
        "bio_updated": False,
        "saved": False,
    }

    bridge = None
    context = None
    pw_ctx = None
    try:
        pw_ctx = sync_playwright().start()
        context, page, bridge = _open_browser_session(pw_ctx, rec, runtime_root, viewport)
        page.set_default_timeout(30000)

        cookies = load_cookies_for_seq(rec, runtime_root)
        inject_cookies(context, cookies)

        safe_goto(page, HOME_URL, timeout=35000)
        sleep_s(4.0)
        logged_in = is_logged_in(page)
        if not logged_in:
            method = perform_login(page, rec)
            sleep_s(1.0)
            safe_goto(page, HOME_URL, timeout=35000)
            sleep_s(3.0)
            logged_in = is_logged_in(page)
        if not logged_in:
            log("seq=%d 无法登录，放弃修改资料" % seq)
            emit_json(result)
            return 2

        profile_url = "https://x.com/%s" % rec["username"]
        safe_goto(page, profile_url, timeout=35000)
        sleep_s(3.0)

        edit_btn = None
        for sel in (
            '[data-testid="editProfileButton"]',
            'a[href*="/settings/profile"]',
            'div[role="button"]:has-text("Edit profile")',
            'div[role="button"]:has-text("编辑个人资料")',
        ):
            try:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=4000):
                    edit_btn = btn
                    break
            except Exception:
                continue

        if edit_btn:
            edit_btn.click()
            sleep_s(2.5)
        else:
            safe_goto(page, "https://x.com/settings/profile", timeout=35000)
            sleep_s(3.5)

        if args.name:
            for sel in (
                'input[name="displayName"]',
                'input[autocomplete="name"]',
                'label:has-text("Name") input',
            ):
                try:
                    inp = page.locator(sel).first
                    if inp.is_visible(timeout=3000):
                        inp.click()
                        sleep_s(0.3)
                        page.keyboard.press("Control+A")
                        page.keyboard.press("Backspace")
                        sleep_s(0.2)
                        inp.fill(args.name)
                        result["name_updated"] = True
                        sleep_s(0.5)
                        break
                except Exception:
                    continue

        if args.bio:
            for sel in (
                'textarea[name="description"]',
                'label:has-text("Bio") textarea',
            ):
                try:
                    inp = page.locator(sel).first
                    if inp.is_visible(timeout=3000):
                        inp.click()
                        sleep_s(0.3)
                        page.keyboard.press("Control+A")
                        page.keyboard.press("Backspace")
                        sleep_s(0.2)
                        inp.fill(args.bio)
                        result["bio_updated"] = True
                        sleep_s(0.5)
                        break
                except Exception:
                    continue

        for sel in (
            '[data-testid="Profile_Save_Button"]',
            'button:has-text("Save")',
            'div[role="button"]:has-text("Save")',
            'button:has-text("保存")',
        ):
            try:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=3000):
                    btn.click()
                    sleep_s(4.0)
                    result["saved"] = True
                    log("seq=%d 资料修改成功并已保存" % seq)
                    break
            except Exception:
                continue

        emit_json(result)
        return 0 if result["saved"] else 3
    finally:
        if context is not None:
            try:
                context.close()
            except Exception:
                pass
        if pw_ctx is not None:
            try:
                pw_ctx.stop()
            except Exception:
                pass
        if bridge is not None:
            bridge.stop()


def cmd_status(args) -> int:
    runtime_root = Path(os.path.expanduser(args.runtime_root))
    records = build_records(load_matrix(args.excel, args.sheet))
    state = load_state(runtime_root)

    groups = {"A": 0, "B": 0, "C": 0, "D": 0, "未分组": 0}
    tiers = {"Tier1": 0, "Tier2": 0, "Tier3": 0, "未分层": 0}
    for rec in records:
        groups[normalize_group(rec.get("group"))] = groups.get(
            normalize_group(rec.get("group")), 0
        ) + 1
        tiers[normalize_tier(rec.get("tier"))] = tiers.get(
            normalize_tier(rec.get("tier")), 0
        ) + 1

    verified = 0
    by_group_logged = {"A": 0, "B": 0, "C": 0, "D": 0, "未分组": 0}
    by_tier_logged = {"Tier1": 0, "Tier2": 0, "Tier3": 0, "未分层": 0}
    for rec in records:
        entry = state.get(str(rec["seq"]))
        if not isinstance(entry, dict) or not entry.get("logged_in"):
            continue
        verified += 1
        g = normalize_group(rec.get("group"))
        t = normalize_tier(rec.get("tier"))
        by_group_logged[g] = by_group_logged.get(g, 0) + 1
        by_tier_logged[t] = by_tier_logged.get(t, 0) + 1

    payload = {
        "total": len(records),
        "groups": groups,
        "tiers": tiers,
        "verified_logged_in": verified,
        "verified_by_group": by_group_logged,
        "verified_by_tier": by_tier_logged,
        "state_entries": len(state),
        "excel": str(Path(os.path.expanduser(args.excel))),
        "runtime_root": str(runtime_root),
    }
    emit_json(payload)
    return 0


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="LX 主机 X 矩阵(100 账号) 代理巡检 / SOCKS5 桥接 / Patchright 自动登录发推引擎"
    )
    parser.add_argument("--excel", default=os.environ.get("X_MATRIX_EXCEL", DEFAULT_EXCEL))
    parser.add_argument("--sheet", default=DEFAULT_SHEET)
    parser.add_argument(
        "--runtime-root", default=os.environ.get("X_MATRIX_RUNTIME", DEFAULT_RUNTIME_ROOT)
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check-proxies", help="并发检测全部代理出口 IP")
    p_check.add_argument(
        "--auto-replace",
        action="store_true",
        help="失败代理自动调 Webshare 替换 (需 WEBSHARE_API_KEY)",
    )
    p_check.set_defaults(func=cmd_check_proxies)

    p_login = sub.add_parser("login-smoke", help="单账号 Cookie 注入 + 2FA 自动登录冒烟")
    p_login.add_argument("--seq", type=int, required=True, help="账号序号 1..100")
    p_login.set_defaults(func=cmd_login_smoke)

    p_post = sub.add_parser("post", help="发推 / 回复 / 自评")
    p_post.add_argument("--seq", type=int, required=True, help="账号序号 1..100")
    p_post.add_argument("--text", required=True, help="推文内容")
    p_post.add_argument("--self-reply", default=None, help="发推后在自己首推下 1 楼自评")
    p_post.add_argument("--reply-url", default=None, help="回复指定推文 URL")
    p_post.set_defaults(func=cmd_post)

    p_prof = sub.add_parser("update-profile", help="修改显示名称与简介")
    p_prof.add_argument("--seq", type=int, required=True, help="账号序号 1..100")
    p_prof.add_argument("--name", default=None, help="新的显示名称 (Name)")
    p_prof.add_argument("--bio", default=None, help="新的个人简介 (Bio)")
    p_prof.set_defaults(func=cmd_update_profile)

    p_status = sub.add_parser("status", help="赛道 / 层级统计与已验证登录数")
    p_status.set_defaults(func=cmd_status)
    return parser


def main(argv=None) -> int:
    ensure_ld_library_path()
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except SystemExit:
        raise
    except Exception:
        log("执行失败:\n%s" % traceback.format_exc(limit=6))
        return 1


if __name__ == "__main__":
    sys.exit(main())
