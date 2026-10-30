#!/usr/bin/env node
"use strict";

const { VERSION, GATEWAYS, gpuTco, mediaTco, lineTable } = require("./index");

const args = process.argv.slice(2);
function argValue(flag) {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
}
const wantsJson = args.includes("--json");
const wantsHelp = args.includes("--help") || args.includes("-h");
const wantsVersion = args.includes("--version");
const wantsVersion2 = args.includes("-v");

const GPU_ALIASES = ["h100", "a100", "rtx5090", "rtx4090"];
const gpu = argValue("--gpu") || (args.length === 0 ? "h100" : null);
const hours = argValue("--hours") ? parseFloat(argValue("--hours")) : null;
const voiceChars = argValue("--voice-chars") ? parseInt(argValue("--voice-chars"), 10) : null;
const videoMins = argValue("--video-mins") ? parseFloat(argValue("--video-mins")) : null;

if (wantsHelp) {
  console.log(
    [
      "Usage: llm-gpu-cost-estimator [options]",
      "",
      "  --gpu <h100|a100|rtx5090|rtx4090>  GPU model to benchmark",
      "  --hours <n>                        compute runtime hours",
      "  --voice-chars <n>                  ElevenLabs voice synthesis characters / month",
      "  --video-mins <n>                   HeyGen avatar video minutes / month",
      "  --json                             emit pure JSON payload",
      "  -v, --version                      show version",
      "",
      "Gateways:",
      "  RunPod       " + GATEWAYS.runpod,
      "  Vast.ai      " + GATEWAYS.vastai,
      "  ElevenLabs   " + GATEWAYS.elevenlabs,
      "  HeyGen       " + GATEWAYS.heygen,
    ].join("\n")
  );
  process.exit(0);
}

if (wantsVersion || wantsVersion2) {
  console.log("llm-gpu-cost-estimator " + VERSION);
  process.exit(0);
}

if (gpu && !GPU_ALIASES.includes(gpu)) {
  console.error("Unknown --gpu: " + gpu + " (choose h100 | a100 | rtx5090 | rtx4090)");
  process.exit(2);
}

// Compute mode: either GPU TCO or generative media TCO
const doGpu = gpu && (hours !== null || !voiceChars && !videoMins);
const doMedia = voiceChars !== null || videoMins !== null;

if (doGpu) {
  const g = gpuTco(gpu, hours !== null ? hours : 100);
  if (wantsJson) {
    console.log(
      JSON.stringify(
        {
          tool: "llm-gpu-cost-estimator",
          version: VERSION,
          mode: "compute",
          gpu_model: g.gpuName,
          hours: g.hours,
          nominal_rate_per_hour: g.nominalRatePerHour,
          nominal_cost: g.nominalCost,
          cold_start_cost: g.coldStartCost,
          effective_ondemand_tco: g.effectiveOnDemandTco,
          spot_rate_per_hour: g.spotRatePerHour,
          spot_base_cost: g.spotBaseCost,
          spot_penalty: g.spotPenalty,
          effective_spot_tco: g.effectiveSpotTco,
          net_savings_usd: g.netSavingsUsd,
          savings_percentage: g.savingsPct,
          gateways: { runpod: GATEWAYS.runpod, vastai: GATEWAYS.vastai },
        },
        null,
        2
      )
    );
  } else {
    console.log("llm-gpu-cost-estimator " + VERSION + " - AI Compute TCO Engine\n");
    console.log(
      lineTable("METRIC                       | VALUE", [
        ["GPU Architecture", g.gpuName],
        ["Compute Duration", g.hours + " hours"],
        ["Base On-Demand Rate", "$" + g.nominalRatePerHour.toFixed(2) + " / hour"],
        ["Nominal Compute Cost", "$" + g.nominalCost.toFixed(2)],
        ["Cold-Start Overhead (3%)", "$" + g.coldStartCost.toFixed(2)],
        ["Effective On-Demand TCO", "$" + g.effectiveOnDemandTco.toFixed(2)],
        ["Spot Base Cost", "$" + g.spotBaseCost.toFixed(2) + " ($" + g.spotRatePerHour.toFixed(2) + "/hr)"],
        ["Spot Interruption Penalty", "$" + g.spotPenalty.toFixed(2) + " (15% restart)"],
        ["Effective Spot TCO", "$" + g.effectiveSpotTco.toFixed(2)],
        ["Spot Net Savings", "$" + g.netSavingsUsd.toFixed(2) + " (" + g.savingsPct + "%)"],
      ])
    );
    console.log(
      "\nRecommended providers:\n  On-Demand  -> RunPod  " + GATEWAYS.runpod + "\n  Spot       -> Vast.ai " + GATEWAYS.vastai
    );
    console.log("\nFull guide: https://gpu.mybskm.top");
  }
}

if (doMedia) {
  const m = mediaTco(voiceChars !== null ? voiceChars : 0, videoMins !== null ? videoMins : 0);
  if (wantsJson) {
    console.log(
      JSON.stringify(
        {
          tool: "llm-gpu-cost-estimator",
          version: VERSION,
          mode: "media",
          voice_chars: voiceChars,
          video_minutes: videoMins,
          breakdown: m,
          gateways: { elevenlabs: GATEWAYS.elevenlabs, heygen: GATEWAYS.heygen },
        },
        null,
        2
      )
    );
  } else {
    console.log("\nllm-gpu-cost-estimator " + VERSION + " - Generative Media Production TCO\n");
    console.log(
      lineTable("METRIC                       | VALUE", [
        ["Voice Volume (Chars)", voiceChars === null ? "n/a" : voiceChars.toLocaleString("en-US") + " chars"],
        ["ElevenLabs Tier Reqd", m.voice.tierName + " (base $" + m.voice.baseUsd + ")"],
        ["Voice Synthesis Cost", "$" + m.voice.totalUsd.toFixed(2)],
        ["Video Avatar Volume", videoMins === null ? "n/a" : videoMins + " minutes"],
        ["HeyGen Tier Reqd", m.video.tierName + " (base $" + m.video.baseUsd + ")"],
        ["Video Synthesis Cost", "$" + m.video.totalUsd.toFixed(2)],
        ["Total Media Pipeline TCO", "$" + m.totalMonthlyTcoUsd.toFixed(2) + " / month"],
        ["Per Finished AV Minute", m.perFinishedMinuteUsd === null ? "n/a" : "$" + m.perFinishedMinuteUsd],
      ])
    );
    console.log(
      "\nElevenLabs " + GATEWAYS.elevenlabs + "\nHeyGen     " + GATEWAYS.heygen
    );
    console.log("\nVoice vs video deep-dive: https://gpu.mybskm.top/blog/heygen-vs-synthesia-elevenlabs.html");
  }
}

process.exit(0);
