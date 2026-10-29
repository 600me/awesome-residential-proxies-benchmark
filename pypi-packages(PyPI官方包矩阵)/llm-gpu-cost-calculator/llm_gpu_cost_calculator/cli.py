#!/usr/bin/env python3
"""llm-gpu-cost-calculator - AI Compute & Generative Media TCO engine (stdlib only)."""

import argparse
import json
import math
import sys

VERSION = "1.0.0"
TOOL = "llm-gpu-cost-calculator"

GW = {
    "runpod": "https://go.272738.xyz/runpod?src=pypi_gpu_calc",
    "vastai": "https://go.272738.xyz/vastai?src=pypi_gpu_calc",
    "elevenlabs": "https://go.272738.xyz/elevenlabs?src=pypi_gpu_calc",
    "heygen": "https://go.272738.xyz/heygen?src=pypi_gpu_calc",
}

# rate: on-demand USD/hr; spot_rate: spot/interruptible USD/hr;
# rf: restart (interruption) penalty factor applied to nominal compute cost.
GPUS = {
    "h100": {"name": "NVIDIA H100 80GB SXM5", "rate": 2.49, "spot_rate": 1.287, "rf": 0.15},
    "a100": {"name": "NVIDIA A100 80GB SXM", "rate": 1.64, "spot_rate": 0.95, "rf": 0.14482},
    "rtx5090": {"name": "NVIDIA RTX 5090", "rate": 0.38, "spot_rate": 0.19, "rf": 0.15},
    "rtx4090": {"name": "NVIDIA RTX 4090", "rate": 0.44, "spot_rate": 0.22, "rf": 0.15},
}

COLD_START_RATE = 0.03  # 3% cold-start / warm-up overhead on nominal cost

# ElevenLabs tiers: (label, monthly USD, quota chars); overage $0.20 / 1k chars.
VOICE_TIERS = [
    ("Free Tier", 0.00, 10000),
    ("Starter Tier", 5.00, 30000),
    ("Creator Tier", 22.00, 100000),
    ("Pro Tier", 99.00, 500000),
    ("Scale Tier", 330.00, 2000000),
]
VOICE_OVERAGE_PER_1K = 0.20

# HeyGen tiers: (label, monthly USD, quota minutes); overage $2.50 / extra minute.
VIDEO_TIERS = [
    ("Free Tier", 0.00, 1),
    ("Creator Tier", 29.00, 15),
    ("Team Tier", 89.00, 30),
    ("Pro Tier", 199.00, 100),
]
VIDEO_OVERAGE_PER_MIN = 2.50


def _quota_label(chars):
    if chars >= 1000000:
        return "%dM+" % (chars // 1000000)
    return "%dk" % (chars // 1000)


def pick_tier(tiers, volume):
    """Smallest tier whose quota can stretch to the volume (quota*2 >= volume);
    overage beyond the quota is billed at the provider overage rate."""
    for label, price, quota in tiers:
        if 2 * quota >= volume:
            return (label, price, quota)
    return tiers[-1]


def compute_voice(chars):
    if chars <= 0:
        return {"cost": 0.0, "tier": "N/A", "quota": 0, "overage": 0.0}
    label, price, quota = pick_tier(VOICE_TIERS, chars)
    overage = max(0, chars - quota) / 1000.0 * VOICE_OVERAGE_PER_1K
    label = "Scale Tier (2M+ quota)" if quota >= 2000000 else "%s (%s quota)" % (label, _quota_label(quota))
    return {"cost": round(price + overage, 2), "tier": label, "quota": quota, "overage": round(overage, 2)}


def compute_video(mins):
    if mins <= 0:
        return {"cost": 0.0, "tier": "N/A", "quota": 0, "overage": 0.0}
    label, price, quota = pick_tier(VIDEO_TIERS, mins)
    overage = max(0, mins - quota) * VIDEO_OVERAGE_PER_MIN
    label = "%s (%dm base + %dm overage)" % (label, quota, mins - quota)
    return {"cost": round(price + overage, 2), "tier": label, "quota": quota, "overage": round(overage, 2)}


def tier_price(tiers, quota):
    for label, price, q in tiers:
        if q == quota:
            return price
    return 0.0


def compute_gpu(gpu, hours):
    g = GPUS[gpu]
    nominal_rate = g["rate"]
    nominal = hours * nominal_rate
    cold = nominal * COLD_START_RATE
    ondemand_tco = nominal + cold
    spot_rate = g["spot_rate"]
    spot_base = hours * spot_rate
    penalty = nominal * g["rf"]
    spot_tco = spot_base + penalty
    net_savings = ondemand_tco - spot_tco
    pct_raw = 100.0 * net_savings / ondemand_tco if ondemand_tco else 0.0
    return {
        "gpu": gpu,
        "gpu_name": g["name"],
        "hours": hours,
        "nominal_rate_per_hour": nominal_rate,
        "cold_start_rate": COLD_START_RATE,
        "restart_factor": g["rf"],
        "nominal_cost": round(nominal, 2),
        "cold_start_cost": round(cold, 2),
        "effective_ondemand_tco": round(ondemand_tco, 2),
        "spot_rate_per_hour": spot_rate,
        "spot_base_cost": round(spot_base, 2),
        "spot_penalty": round(penalty, 2),
        "effective_spot_tco": round(spot_tco, 2),
        "net_savings_usd": round(net_savings, 2),
        "savings_percentage_raw": pct_raw,
        "savings_percentage": round(pct_raw, 1),
    }


def table(rows):
    """rows: list of (kind, left, right); kind in {'sep','row','plain'}."""
    w1, w2 = 27, 42
    sep = "+" + "-" * w1 + "+" + "-" * w2 + "+"
    out = []
    for kind, left, right in rows:
        if kind == "sep":
            out.append(sep)
        else:
            out.append("| " + left.ljust(w1 - 2) + " | " + right.ljust(w2 - 2) + " |")
    return "\n".join(out)


def render_compare_cloud():
    providers = [
        ("RunPod", "Serverless GPUs, per-second billing",
         ["RTX 4090 ($0.44/hr)", "A100 80GB SXM ($1.64/hr)", "H100 80GB SXM ($2.49/hr)",
          "8x H100 SXM5 ($19.92/hr)", "Private VPC & Pod Clusters"], GW["runpod"]),
        ("Vast.ai", "Decentralized GPU marketplace, low spot",
         ["RTX 5090 ($0.38/hr)", "1x A100 PCIe ($0.95/hr)", "1x H100 PCIe ($1.85/hr)",
          "4x H100 SXM ($7.80/hr)", "Datacenter Contracts"], GW["vastai"]),
        ("ElevenLabs", "Ultra-realistic voice cloning & TTS",
         ["Free (10k chars/mo)", "Starter ($5/mo, 30k chars)", "Creator ($22/mo, 100k)",
          "Pro ($99/mo, 500k)", "Scale ($330/mo, 2M+)"], GW["elevenlabs"]),
        ("HeyGen", "#1 AI avatar video & translation",
         ["Free (1 credit/mo)", "Creator ($29/mo, 15 mins)", "Team ($89/mo, 30 mins)",
          "Pro ($199/mo, 100 mins)", "Enterprise Custom"], GW["heygen"]),
    ]
    header = ("Provider", "Core Strength", "Tier 1", "Tier 2", "Tier 3", "Tier 4", "Tier 5", "Gateway")
    table_rows = [header]
    for name, strength, tiers, url in providers:
        table_rows.append((name, strength, *tiers, url))
    widths = [max(len(str(r[i])) for r in table_rows) for i in range(len(header))]
    lines = ["+" + "+".join("-" * (w + 2) for w in widths) + "+"]
    lines.append("| " + " | ".join(h.ljust(w) for h, w in zip(header, widths)) + " |")
    lines.append(lines[0])
    for row in table_rows[1:]:
        lines.append("| " + " | ".join(str(c).ljust(w) for c, w in zip(row, widths)) + " |")
    lines.append(lines[0])
    return "\n".join(lines) + (
        "\n\nGateway links: RunPod / Vast.ai for GPU compute; ElevenLabs / HeyGen for voice & avatar video.\n"
        "RunPod Gateway: %s\nVast.ai Gateway: %s\nElevenLabs Gateway: %s\nHeyGen Gateway: %s\n"
        % (GW["runpod"], GW["vastai"], GW["elevenlabs"], GW["heygen"])
    )


def render_media(voice, video, json_mode=False):
    v = compute_voice(voice)
    vid = compute_video(video)
    total = round(v["cost"] + vid["cost"], 2)
    if json_mode:
        return {
            "tool": TOOL, "version": VERSION, "mode": "media",
            "voice_chars": voice, "voice_cost_usd": v["cost"],
            "voice_tier": v["tier"], "video_mins": video,
            "video_cost_usd": vid["cost"], "video_tier": vid["tier"],
            "total_media_tco_usd": total,
            "gateways": {"elevenlabs": GW["elevenlabs"], "heygen": GW["heygen"]},
        }
    speech_hours = int(voice / 9000) if voice > 0 else 0
    video_base = tier_price(VIDEO_TIERS, vid["quota"]) if video > 0 else 0.0
    rows = []
    if voice > 0:
        rows += [
            ("row", "Voice Volume (Chars)", "%s characters (~%d hours of speech)" % (format(voice, ","), speech_hours)),
            ("row", "ElevenLabs Tier Reqd", v["tier"]),
            ("row", "Voice Synthesis Cost", "$%.2f" % v["cost"]),
        ]
    if video > 0:
        rows += [
            ("row", "Video Avatar Volume", "%d minutes generated video" % video),
            ("row", "HeyGen Tier Reqd", vid["tier"]),
            ("row", "Video Synthesis Cost", "$%.2f ($%.2f base + $%.2f overage)"
             % (vid["cost"], video_base, vid["overage"])),
        ]
    rows.append(("sep", "", ""))
    rows.append(("row", "Total Media Pipeline TCO", "$%.2f / month" % total))
    if video > 0:
        per_min = total / float(video)
        rows.append(("row", "Effective Per-Minute Cost", "$%.2f / combined finished AV minute" % per_min))
    body = table(rows)
    head = "%s %s - Generative Media Production TCO" % (TOOL, VERSION)
    return (head + "\n\n" + body + "\n\n"
            + "ElevenLabs Gateway: %s\nHeyGen Gateway: %s\n" % (GW["elevenlabs"], GW["heygen"]))


def render_compute(calc, json_mode=False):
    if json_mode:
        d = {k: calc[k] for k in ("nominal_rate_per_hour", "nominal_cost", "cold_start_cost",
                                  "spot_rate_per_hour", "spot_base_cost", "spot_penalty",
                                  "effective_ondemand_tco", "effective_spot_tco",
                                  "net_savings_usd", "savings_percentage")}
        return {
            "tool": TOOL, "version": VERSION, "mode": "compute",
            "gpu": calc["gpu"], "hours": calc["hours"], **d,
            "gateways": {"runpod": GW["runpod"], "vastai": GW["vastai"]},
        }
    pct = math.floor(calc["savings_percentage_raw"] * 100) / 100.0
    rows = [
        ("row", "GPU Architecture", calc["gpu_name"]),
        ("row", "Compute Duration", "%.1f hours" % calc["hours"]),
        ("row", "Base On-Demand Rate", "$%.4f / hour" % calc["nominal_rate_per_hour"]),
        ("row", "Nominal Compute Cost", "$%.2f" % calc["nominal_cost"]),
        ("row", "Cold-Start Overhead (3%)", "$%.2f" % calc["cold_start_cost"]),
        ("row", "Spot Interruption Penalty", "$%.2f (based on 15%% restart factor)" % calc["spot_penalty"]),
        ("sep", "", ""),
        ("row", "Effective On-Demand TCO", "$%.2f" % calc["effective_ondemand_tco"]),
        ("row", "Effective Spot TCO", "$%.2f (spot base $%.2f + penalty)"
         % (calc["effective_spot_tco"], calc["spot_base_cost"])),
        ("row", "Spot Net Savings", "$%.2f (%.2f%% net reduction)"
         % (calc["net_savings_usd"], pct)),
        ("sep", "", ""),
        ("row", "Recommended Providers", "RunPod (On-Demand), Vast.ai (Spot)"),
    ]
    head = "%s %s - AI Compute & Media TCO Engine" % (TOOL, VERSION)
    return (head + "\n\n" + table(rows) + "\n\n"
            + "RunPod Gateway: %s\nVast.ai Gateway: %s\n" % (GW["runpod"], GW["vastai"]))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=TOOL,
        description="Audit real cloud GPU TCO, spot interruption penalty, and generative multimodal AI costs.")
    parser.add_argument("--gpu", choices=sorted(GPUS), default="h100", help="GPU hardware model to benchmark")
    parser.add_argument("--hours", type=float, default=100.0, help="estimated runtime compute hours (default: 100.0)")
    parser.add_argument("--voice-chars", type=int, default=None, help="voice synthesis character count")
    parser.add_argument("--video-mins", type=int, default=None, help="video generation minute volume")
    parser.add_argument("--compare-cloud", action="store_true",
                        help="print 2026 5-tier GPU and multimodal cloud comparison table")
    parser.add_argument("--json", action="store_true", help="emit pure JSON payload for CI/CD cost monitoring")
    parser.add_argument("--version", action="version", version="%s %s" % (TOOL, VERSION))
    args = parser.parse_args(argv)

    blocks = []
    media_mode = args.voice_chars is not None or args.video_mins is not None
    if media_mode:
        blocks.append(render_media(args.voice_chars or 0, args.video_mins or 0, json_mode=args.json))
    else:
        blocks.append(render_compute(compute_gpu(args.gpu, args.hours), json_mode=args.json))
    if args.compare_cloud:
        blocks.append(render_compare_cloud())
    out = "\n".join(b if isinstance(b, str) else json.dumps(b, indent=2) for b in blocks)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
