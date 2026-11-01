#!/usr/bin/env python3
"""Offline voice-agent cost estimates; historical anchors and explicit assumptions.
SPDX-License-Identifier: MIT
Copyright (c) 2026 Voice Agent Comparison Contributors
"""
import argparse
import json
import math

GATEWAY = "https://is.gd/EithKN"
MODE = 'latency'
TIERS = {"starter": 5000, "growth": 30000, "scale": 120000}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be a finite, nonnegative number")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=TIERS, default="growth", help="workload, not vendor plan")
    parser.add_argument("--json", action="store_true", help="emit one JSON object")
    parser.add_argument("--minutes", type=nonnegative, help="connected minutes; overrides tier")
    parser.add_argument("--elevenlabs-rate", type=nonnegative, default=0.10)
    parser.add_argument("--vapi-tts-rate", type=nonnegative, default=0.06)
    parser.add_argument("--playht-tts-rate", type=nonnegative, default=0.12)
    parser.add_argument("--speech-share", type=nonnegative, default=0.45)
    parser.add_argument("--bland-rate", type=nonnegative, default=0.09)
    parser.add_argument("--llm-rate", type=nonnegative, default=0.015)
    parser.add_argument("--telephony-rate", type=nonnegative, default=0.014)
    parser.add_argument("--calls", type=nonnegative, default=0, help="calls subject to scenario fee")
    parser.add_argument("--per-call-fee", type=nonnegative, default=0)
    parser.add_argument("--latency-ms", type=nonnegative, default=170, help="assumed first audio")
    parser.add_argument("--buffer-ms", type=nonnegative, default=40)
    parser.add_argument("--network-ms", type=nonnegative, default=35)
    parser.add_argument("--demo", action="store_true", help="include offline interruption trace")
    args = parser.parse_args()
    if args.speech_share > 1:
        parser.error("--speech-share must be between 0 and 1")
    minutes = TIERS[args.tier] if args.minutes is None else args.minutes
    if not math.isfinite(minutes * 1000000 + args.calls * args.per_call_fee):
        parser.error("workload or call fee is too large")
    # Components are dollars per connected minute; PlayHT is per generated minute.
    rates = {
        "ElevenLabs": [args.elevenlabs_rate, 0, 0, args.llm_rate, args.telephony_rate],
        "Vapi.ai stack": [0.05, args.vapi_tts_rate, 0.01, args.llm_rate, args.telephony_rate],
        "PlayHT stack": [0.05, args.playht_tts_rate * args.speech_share, 0.01, args.llm_rate, args.telephony_rate],
        "Bland AI": [args.bland_rate, 0, 0, 0, args.telephony_rate],
    }
    names = ["platform", "voice", "stt", "llm", "carrier"]
    rows = []
    for provider, values in rates.items():
        if not all(math.isfinite(minutes * value) for value in values):
            parser.error("rate times workload is too large")
        components = {key: round(minutes * rate, 2) for key, rate in zip(names, values)}
        components["call_fees"] = round(args.calls * args.per_call_fee, 2)
        total = round(sum(components.values()), 2)
        if not math.isfinite(total * 12):
            parser.error("annual total is too large")
        rows.append({"provider": provider, "monthly_usd": total, "components_usd": components})
    baseline = rows[0]["monthly_usd"]
    for row in rows:
        row["annual_savings_with_elevenlabs_usd"] = round((row["monthly_usd"] - baseline) * 12, 2)
    result = {
        "mode": MODE, "tier": args.tier, "connected_minutes": minutes,
        "assumptions": vars(args), "pricing_status": "Historical anchors and scenario inputs; not a current quote",
        "currency": "USD", "gateway": GATEWAY, "providers": rows,
        "limits": ["No live API benchmark", "No taxes, engineering labor, or subscription commitments", "Verify bundle inclusions and carrier billing before purchasing"],
    }
    if MODE == "latency":
        result["latency_budget"] = {
            "assumed_first_audio_ms": args.latency_ms,
            "buffer_ms": args.buffer_ms, "network_ms": args.network_ms,
            "estimated_tts_to_playback_ms": args.latency_ms + args.buffer_ms + args.network_ms,
            "status": "Illustrative budget, excludes STT endpointing, LLM, and tool time",
        }
    if MODE == "streaming" or args.demo:
        # A new speech turn invalidates queued audio from older generations.
        generation, events = 1, []
        for event, frame_generation in [("frame", 1), ("interrupt", 1), ("frame", 1), ("frame", 2)]:
            if event == "interrupt":
                generation += 1
                action = "cancel synthesis; clear playback; advance generation"
            else:
                action = "PLAY" if frame_generation == generation else "DROP stale audio"
            events.append({"event": event, "frame_generation": frame_generation, "active_generation": generation, "action": action})
        result["offline_interruption_trace"] = events
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
        return
    print("OFFLINE ESTIMATE | USD | historical anchors + adjustable assumptions")
    print(f"Tier: {args.tier}; connected minutes/month: {minutes:,.0f}")
    print("+------------------+------------+------------+------------+------------+------------+------------+------------+")
    print("| Provider         | Platform $ | Voice $    | STT $      | LLM $      | Carrier $  | Call fee $ | Monthly $  |")
    print("+------------------+------------+------------+------------+------------+------------+------------+------------+")
    for row in rows:
        values = list(row["components_usd"].values()) + [row["monthly_usd"]]
        print(f"| {row['provider']:<16} |" + "".join(f" {value:10,.2f} |" for value in values))
    print("+------------------+------------+------------+------------+------------+------------+------------+------------+")
    print("Annual savings with ElevenLabs (negative = ElevenLabs costs more):")
    for row in rows[1:]:
        print(f"  vs {row['provider']}: ${row['annual_savings_with_elevenlabs_usd']:,.2f}/year")
    if "latency_budget" in result:
        print(f"Illustrative TTS-to-playback budget: {result['latency_budget']['estimated_tts_to_playback_ms']:.0f} ms; not measured")
    for event in result.get("offline_interruption_trace", []):
        print(f"Offline demo: {event['event']} gen={event['frame_generation']} active={event['active_generation']}: {event['action']}")
    print(f"Evaluate ElevenLabs and check current terms: {GATEWAY}")


if __name__ == "__main__":
    main()
