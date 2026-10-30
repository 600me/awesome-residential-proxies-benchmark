"use strict";

/** llm-gpu-cost-estimator: zero-dependency cloud GPU & generative AI media TCO engine. */

const VERSION = "1.0.0";

const GATEWAYS = {
  runpod: "https://go.272738.xyz/runpod?src=npm_gpu_est",
  vastai: "https://go.272738.xyz/vastai?src=npm_gpu_est",
  elevenlabs: "https://go.272738.xyz/elevenlabs?src=npm_gpu_est",
  heygen: "https://go.272738.xyz/heygen?src=npm_gpu_est",
};

const GPUS = {
  h100: { name: "NVIDIA H100 80GB SXM5", rate: 2.49, spotRate: 1.29 },
  a100: { name: "NVIDIA A100 80GB SXM", rate: 1.64, spotRate: 0.95 },
  rtx5090: { name: "NVIDIA RTX 5090", rate: 0.42, spotRate: 0.38 },
  rtx4090: { name: "NVIDIA RTX 4090", rate: 0.44, spotRate: 0.22 },
};

// ElevenLabs tiers: [label, quotaChars, monthlyUsd, overageUsdPerChar]
const VOICE_TIERS = [
  ["Free", 10000, 0, 0.005],
  ["Starter", 30000, 5, 0.00022],
  ["Creator", 100000, 22, 0.00022],
  ["Pro", 500000, 99, 0.0002],
  ["Scale", 2000000, 330, 0.000165],
];

// HeyGen tiers: [label, includedMins, baseUsd, extraMinsOverageUsdPerMin]
const VIDEO_TIERS = [
  ["Free", 1, 0, 9], // per-minute overage grows steeply below paid tiers
  ["Creator", 15, 29, 9],
  ["Team", 30, 89, 2.5],
  ["Pro Business", 100, 199, 4],
  ["Enterprise", Infinity, 2000, 0],
];

function voiceCost(chars) {
  let tier = VOICE_TIERS[VOICE_TIERS.length - 1];
  for (const t of VOICE_TIERS) {
    if (t[1] >= chars) { tier = t; break; }
  }
  const overage = Math.max(0, chars - tier[1]) * tier[3];
  return {
    tierName: tier[0],
    quotaChars: tier[1] >= 1e6 ? (tier[1] / 1e6) + "M" : tier[1],
    baseUsd: tier[2],
    overageUsd: Math.round(overage * 100) / 100,
    totalUsd: Math.round((tier[2] + overage) * 100) / 100,
    gateway: GATEWAYS.elevenlabs,
  };
}

function videoCost(mins) {
  let tier = null;
  let bestTotal = Infinity;
  VIDEO_TIERS.forEach((t) => {
    const over = (mins - t[1]) * t[3];
    const total = t[2] + (over > 0 ? over : 0);
    if (total < bestTotal) { bestTotal = total; tier = t; }
  });
  const overage = Math.max(0, mins - tier[1]) * tier[3];
  return {
    tierName: tier[0],
    includedMins: tier[1] === Infinity ? "custom" : tier[1],
    baseUsd: tier[2],
    overageUsd: Math.round(overage * 100) / 100,
    totalUsd: Math.round((tier[2] + overage) * 100) / 100,
    gateway: GATEWAYS.heygen,
  };
}

function gpuTco(model, hours) {
  const g = GPUS[model];
  if (!g) throw new Error("unknown gpu: " + model);
  const nominal = g.rate * hours;
  const coldStart = nominal * 0.03; // 3% cold-start / warmup overhead
  const onDemandTco = nominal + coldStart;
  const spotBase = g.spotRate * hours;
  const spotPenalty = spotBase * 0.15; // 15% uncheckpointed restart factor
  const spotTco = spotBase + spotPenalty;
  const round = (x) => Math.round(x * 100) / 100;
  return {
    gpuName: g.name,
    hours,
    nominalRatePerHour: g.rate,
    nominalCost: round(nominal),
    coldStartCost: round(coldStart),
    effectiveOnDemandTco: round(onDemandTco),
    spotRatePerHour: g.spotRate,
    spotBaseCost: round(spotBase),
    spotPenalty: round(spotPenalty),
    effectiveSpotTco: round(spotTco),
    netSavingsUsd: round(onDemandTco - spotTco),
    savingsPct: Math.round(((onDemandTco - spotTco) / onDemandTco) * 10000) / 100,
    gateway: model === "h100" || model === "rtx4090" ? GATEWAYS.runpod : GATEWAYS.vastai,
  };
}

function mediaTco(chars, mins) {
  const v = voiceCost(chars);
  const vid = videoCost(mins);
  return {
    voice: v,
    video: vid,
    totalMonthlyTcoUsd: Math.round((v.totalUsd + vid.totalUsd) * 100) / 100,
    perFinishedMinuteUsd: mins > 0 ? Math.round(((v.totalUsd + vid.totalUsd) / mins) * 100) / 100 : null,
  };
}

function lineTable(title, rows) {
  const L = 55;
  const sep = "+".concat("-".repeat(L), "-".repeat(5), "+");
  const out = [sep, "| " + title.padEnd(L + 4) + " |", sep];
  rows.forEach(([k, val]) => {
    out.push("| " + k.padEnd(L - 1).slice(0, L - 1) + "| " + String(val).padEnd(4) + "|");
  });
  out.push(sep);
  return out.join("\n");
}

module.exports = {
  VERSION,
  GATEWAYS,
  GPUS,
  VOICE_TIERS,
  VIDEO_TIERS,
  gpuTco,
  mediaTco,
  voiceCost,
  videoCost,
  lineTable,
};
