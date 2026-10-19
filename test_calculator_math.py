#!/usr/bin/env python3
"""Offline assertions for the proxy calculator and the shipped SEO assets.

Two independent things are certified here:

1. The pure JS core embedded in ``web/calculator/index.html`` is extracted and
   re-executed through Node against a from-scratch Python implementation of the
   same sticky-session model, so the shipped page cannot silently drift from the
   published arithmetic (including the three worked tiers in the blog article).
2. Every shipped HTML page carries a self-referencing canonical plus a valid
   JSON-LD block of the documented @type, and both sitemaps list the URLs the
   release contract requires.

No third-party packages: standard library plus the Node binary already present
on the host.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
GPU_ROOT = ROOT.parent / "kais-gpu-cloud-benchmark"

CALC = WEB / "calculator" / "index.html"
HOME = WEB / "index.html"
BLOG_INDEX = WEB / "blog" / "index.html"
ARTICLE = WEB / "blog" / "residential-proxy-sticky-session-guide.html"
SITEMAP = WEB / "sitemap.xml"
GPU_SITEMAP = GPU_ROOT / "sitemap.xml"

DAYS = 30
MIN_ARTICLE_WORDS = 1600

_PASSED = 0


def check(condition: bool, message: str) -> None:
    global _PASSED
    if not condition:
        raise AssertionError(message)
    _PASSED += 1
    print(f"PASS  {message}")


def close(actual: float, expected: float, tol: float = 1e-6) -> bool:
    return abs(float(actual) - float(expected)) <= tol


def strategy(inp: dict, hazard_pct: float) -> dict:
    hazard = min(max(hazard_pct, 0.0), 99.0) / 100.0
    survive = max(1.0 - hazard, 0.01)
    step_runs = inp["steps"] / survive
    flow_kb = step_runs * inp["kb"]
    attempts_per_session_per_day = (inp["hours"] * 60) / inp["duration"]
    monthly_attempts = inp["concurrency"] * attempts_per_session_per_day * DAYS
    monthly_kb = monthly_attempts * flow_kb
    monthly_gb = monthly_kb / (1024 * 1024)
    monthly_cost = monthly_gb * inp["price"]
    completed = monthly_attempts * survive
    return {
        "hazard": hazard,
        "rerun_loss": hazard / survive,
        "step_runs": step_runs,
        "flow_kb": flow_kb,
        "monthly_attempts": monthly_attempts,
        "monthly_gb": monthly_gb,
        "monthly_cost": monthly_cost,
        "completed": completed,
        "cost_per_flow": monthly_cost / completed if completed else 0.0,
    }


def compute(case: dict) -> dict:
    inp = {
        "concurrency": _num(case, "concurrency", 1.0),
        "duration": _num(case, "duration", 10.0),
        "steps": _num(case, "steps", 1.0),
        "price": _num(case, "price", 1.0),
        "kb": _num(case, "kb", 180.0),
        "hours": _num(case, "hours", 24.0),
    }
    sticky = strategy(inp, case["dropRate"])
    rotation = strategy(inp, case["rotationFailure"])
    return {
        "input": inp,
        "sticky": sticky,
        "rotation": rotation,
        "delta_cost": rotation["monthly_cost"] - sticky["monthly_cost"],
        "delta_cost_pct": ((rotation["monthly_cost"] - sticky["monthly_cost"]) / sticky["monthly_cost"]
                           if sticky["monthly_cost"] else 0.0),
    }


def _num(case: dict, name: str, fallback: float) -> float:
    value = case.get(name, fallback)
    return float(fallback if value is None else value)


NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync(process.argv[1], 'utf8');
const match = html.match(/<script id="calc-core">([\s\S]*?)<\/script>/);
if (!match) { console.error('missing calc-core script'); process.exit(2); }
const context = {console};
vm.createContext(context);
vm.runInContext(match[1], context);
const C = context.PROXY_STICKY_CALC;
if (!C) { console.error('PROXY_STICKY_CALC not exported'); process.exit(3); }
const cases = JSON.parse(process.argv[2]);
const out = cases.map(function (item) {
  const r = C.compute(item);
  return {
    sticky: {
      rerun_loss: r.sticky.rerunLossRate,
      step_runs: r.sticky.stepRuns,
      flow_kb: r.sticky.flowKb,
      monthly_gb: r.sticky.monthlyGb,
      monthly_cost: r.sticky.monthlyCost,
      completed: r.sticky.completedFlows,
      cost_per_flow: r.sticky.costPerCompletedFlow
    },
    rotation: {
      rerun_loss: r.rotation.rerunLossRate,
      step_runs: r.rotation.stepRuns,
      flow_kb: r.rotation.flowKb,
      monthly_gb: r.rotation.monthlyGb,
      monthly_cost: r.rotation.monthlyCost,
      completed: r.rotation.completedFlows,
      cost_per_flow: r.rotation.costPerCompletedFlow
    },
    delta_cost: r.delta.cost,
    delta_cost_pct: r.delta.costPct
  };
});
process.stdout.write(JSON.stringify(out));
"""


def run_js_cases(cases: list[dict]) -> list[dict]:
    try:
        proc = subprocess.run(
            ["node", "-e", NODE_HARNESS, str(CALC), json.dumps(cases)],
            capture_output=True, text=True, timeout=30,
        )
    except FileNotFoundError as exc:  # pragma: no cover
        raise AssertionError("Node.js is required for the JS/Python cross-check") from exc
    check(proc.returncode == 0, f"calculator JS core evaluates cleanly (node exit {proc.returncode})")
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.strip())
    return json.loads(proc.stdout)


def assert_case(case: dict, ref: dict, js: dict, label: str) -> None:
    for lane in ("sticky", "rotation"):
        for field in ("rerun_loss", "step_runs", "flow_kb", "monthly_gb",
                      "monthly_cost", "completed", "cost_per_flow"):
            check(close(js[lane][field], ref[lane][field], 1e-6),
                  f"{label}: JS {lane}.{field} matches Python ({ref[lane][field]:.4f})")
    check(close(js["delta_cost"], ref["delta_cost"], 1e-6),
          f"{label}: JS delta cost matches Python ({ref['delta_cost']:.2f})")
    check(close(js["delta_cost_pct"], ref["delta_cost_pct"], 1e-9),
          f"{label}: JS delta percent matches Python ({ref['delta_cost_pct']:.4%})")


def extract_json_ld(path: Path) -> list[dict]:
    html = path.read_text(encoding="utf-8")
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.IGNORECASE | re.DOTALL)
    parsed = []
    for block in blocks:
        parsed.append(json.loads(block))
    return parsed


CASES = [
    {"label": "tier A light checkout",
     "concurrency": 10, "duration": 5, "dropRate": 6, "steps": 10,
     "price": 4, "kb": 150, "hours": 24, "rotationFailure": 35},
    {"label": "tier B login + cart",
     "concurrency": 40, "duration": 10, "dropRate": 8, "steps": 12,
     "price": 4, "kb": 180, "hours": 24, "rotationFailure": 35},
    {"label": "tier C long dashboard",
     "concurrency": 120, "duration": 15, "dropRate": 12, "steps": 20,
     "price": 4, "kb": 260, "hours": 24, "rotationFailure": 35},
    {"label": "zero-drop sanity",
     "concurrency": 5, "duration": 30, "dropRate": 0, "steps": 4,
     "price": 2.5, "kb": 100, "hours": 8, "rotationFailure": 0},
]


def main() -> int:
    print("== Proxy calculator math & SEO asset assertions ==")

    for path in (CALC, HOME, BLOG_INDEX, ARTICLE, SITEMAP, GPU_SITEMAP):
        check(path.is_file(), f"asset exists: {path.relative_to(ROOT.parent)}")

    # ---- Python model bands / published tier numbers --------------------
    refs = [compute(case) for case in CASES]

    tier_a, tier_b, tier_c, sanity = refs
    check(130.0 <= tier_a["sticky"]["monthly_gb"] <= 133.0,
          f"tier A sticky burns ~131 GB/month ({tier_a['sticky']['monthly_gb']:.1f})")
    check(520.0 <= tier_a["sticky"]["monthly_cost"] <= 532.0,
          f"tier A sticky costs ~$526/month ({tier_a['sticky']['monthly_cost']:.2f})")
    check(close(tier_a["sticky"]["rerun_loss"], 0.0638297872, 1e-9),
          "tier A re-run loss is exactly 6% / 94% = 6.3830%")

    check(385.0 <= tier_b["sticky"]["monthly_gb"] <= 389.0,
          f"tier B sticky burns ~387 GB/month ({tier_b['sticky']['monthly_gb']:.1f})")
    check(1540.0 <= tier_b["sticky"]["monthly_cost"] <= 1555.0,
          f"tier B sticky costs ~$1,548/month ({tier_b['sticky']['monthly_cost']:.2f})")
    check(545.0 <= tier_b["rotation"]["monthly_gb"] <= 550.0,
          f"tier B rotation burns ~548 GB/month ({tier_b['rotation']['monthly_gb']:.1f})")
    check(2180.0 <= tier_b["rotation"]["monthly_cost"] <= 2200.0,
          f"tier B rotation costs ~$2,190/month ({tier_b['rotation']['monthly_cost']:.2f})")
    check(close(tier_b["rotation"]["rerun_loss"], 0.35 / 0.65, 1e-9),
          "tier B rotation loss is exactly 35% / 65% = 53.8462%")
    check(0.40 <= tier_b["delta_cost_pct"] <= 0.43,
          f"tier B rotation is ~41% more expensive ({tier_b['delta_cost_pct']:.2%})")
    check(close(tier_b["sticky"]["step_runs"], 12 / 0.92, 1e-9),
          "tier B sticky needs exactly 13.0435 step runs per flow")

    check(1940.0 <= tier_c["sticky"]["monthly_gb"] <= 1955.0,
          f"tier C sticky burns ~1,948 GB/month ({tier_c['sticky']['monthly_gb']:.1f})")
    check(7780.0 <= tier_c["sticky"]["monthly_cost"] <= 7800.0,
          f"tier C sticky costs ~$7,790/month ({tier_c['sticky']['monthly_cost']:.2f})")

    check(close(sanity["sticky"]["rerun_loss"], 0.0, 1e-12),
          "a 0% drop rate produces a 0% re-run loss rate")
    check(close(sanity["sticky"]["step_runs"], 4.0, 1e-12),
          "a 0% drop rate consumes exactly the configured steps per flow")

    # ---- JS / Python cross-check ----------------------------------------
    js_results = run_js_cases(CASES)
    check(len(js_results) == len(CASES), "JS core returned one result per case")
    for case, ref, js in zip(CASES, refs, js_results):
        assert_case(case, ref, js, case["label"])

    # ---- Canonical + JSON-LD -------------------------------------------
    canonical_expectations = {
        HOME: ("https://proxy.mybskm.top/", "WebApplication"),
        CALC: ("https://proxy.mybskm.top/calculator/", "WebApplication"),
        BLOG_INDEX: ("https://proxy.mybskm.top/blog/", "CollectionPage"),
        ARTICLE: ("https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html", "Article"),
    }
    for path, (canonical, ld_type) in canonical_expectations.items():
        html = path.read_text(encoding="utf-8")
        check(f'<link rel="canonical" href="{canonical}">' in html,
              f"{path.name}: self-referencing canonical is {canonical}")
        blocks = extract_json_ld(path)
        check(bool(blocks), f"{path.name}: contains at least one JSON-LD block")
        types = {block.get("@type") for block in blocks}
        check(ld_type in types, f"{path.name}: JSON-LD declares @type {ld_type} ({sorted(types)})")
        for block in blocks:
            check(block.get("@context") == "https://schema.org",
                  f"{path.name}: JSON-LD @context is schema.org")

    article_html = ARTICLE.read_text(encoding="utf-8")
    article_text = re.sub(r"<[^>]+>", " ", article_html.split("<main", 1)[-1])
    word_count = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", article_text))
    check(word_count >= MIN_ARTICLE_WORDS,
          f"article body has {word_count} English words (>= {MIN_ARTICLE_WORDS})")
    for token in ('rel="sponsored noopener"', "https://proxy.mybskm.top/calculator/",
                  "src=article_sticky_guide", "curl_cffi", "cf_clearance"):
        check(token in article_html, f"article contains required token: {token}")

    # ---- Sitemaps --------------------------------------------------------
    proxy_map = SITEMAP.read_text(encoding="utf-8")
    for loc in ("https://proxy.mybskm.top/",
                "https://proxy.mybskm.top/privacy.html",
                "https://proxy.mybskm.top/calculator/",
                "https://proxy.mybskm.top/blog/",
                "https://proxy.mybskm.top/blog/residential-proxy-sticky-session-guide.html"):
        check(loc in proxy_map, f"proxy sitemap lists {loc}")

    gpu_map = GPU_SITEMAP.read_text(encoding="utf-8")
    check("https://gpu.mybskm.top/calculator/" in gpu_map,
          "gpu sitemap lists https://gpu.mybskm.top/calculator/")

    # ---- IndexNow broadcaster -------------------------------------------
    broadcaster = ROOT / "indexnow-broadcast(IndexNow广播).py"
    check(broadcaster.is_file(), "IndexNow broadcaster still exists after the rewrite")
    source = broadcaster.read_text(encoding="utf-8")
    for token in ("api.indexnow.org/indexnow", "sitemap.xml", "proxy.mybskm.top",
                  "gpu.mybskm.top", "pay.mybskm.top", "scrape.mybskm.top"):
        check(token in source, f"broadcaster references {token}")

    print(f"\n{_PASSED} assertions passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"\nFAIL  {error}", file=sys.stderr)
        raise SystemExit(1)
