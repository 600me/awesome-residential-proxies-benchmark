"use strict";

/** proxy-tax-calculator: zero-dependency 2026 proxy bandwidth TCO engine. */

const VERSION = "1.0.0";

const GATEWAYS = {
  decodo: "https://go.272738.xyz/smartproxy?src=npm_protax",
  scraperapi: "https://go.272738.xyz/scraperapi?src=npm_protax",
  webshare: "https://go.272738.xyz/webshare?src=npm_protax",
  "9proxy": "https://go.272738.xyz/9proxy?src=npm_protax",
  packetstream: "https://go.272738.xyz/packetstream?src=npm_protax",
  pawns: "https://go.272738.xyz/pawns?src=npm_protax",
};

// 2026 verified plan ladders: [label, includedTrafficGb, monthlyUsd, overageUsdPerGb]
const PLANS = {
  decodo: [
    ["Starter", 2, 75, 37.5],
    ["Regular", 8, 160, 20.0],
    ["Scale", 20, 300, 15.0],
    ["Enterprise", 100, 1150, 11.5],
  ],
  scraperapi: [
    ["Hobby", 10, 49, 4.9],
    ["Standard", 100, 99, 0.99],
    ["Pro", 1000, 249, 0.249],
    ["Enterprise", 10000, 1500, 0.15],
  ],
  webshare: [
    ["Startup (100 DC proxies)", 250, 2.99, 5.99],
    ["Professional (1k DC proxies)", 1000, 15, 5.49],
    ["Enterprise (Dedicated bandwidth)", 3000, 45, 4.99],
    ["Residential Pay-As-You-Go", 1, 0, 5.99],
  ],
  "9proxy": [
    ["100 Clean Residential IPs", 10, 20, 2.0],
    ["500 Residential IPs", 50, 75, 1.5],
    ["1000 Clean Residential IPs", 100, 110, 1.1],
    ["5000 Enterprise IPs", 500, 400, 0.8],
  ],
  packetstream: [
    ["Pay-As-You-Go 10GB", 10, 10, 1.0],
    ["Pay-As-You-Go 50GB", 50, 50, 1.0],
    ["Pay-As-You-Go 200GB", 200, 200, 1.0],
    ["Bulk 500GB", 500, 495, 0.99],
  ],
  pawns: [
    ["Starter 5GB", 5, 3.8, 0.76],
    ["Growth 25GB", 25, 16.0, 0.64],
    ["Scale 100GB", 100, 56.0, 0.56],
    ["Enterprise 500GB", 500, 250.0, 0.5],
  ],
};

function effectiveCost(provider, gb) {
  if (!PLANS[provider]) throw new Error("unknown provider: " + provider);
  // Evaluate every tier as base + overage at its cliff rate, then pick cheapest total.
  let tier = null;
  let bestTotal = Infinity;
  PLANS[provider].forEach((t) => {
    const over = Math.max(0, gb - t[1]) * t[3];
    if (t[2] + over < bestTotal) {
      bestTotal = t[2] + over;
      tier = t;
    }
  });
  const overageGb = Math.max(0, gb - tier[1]);
  const overage = overageGb * tier[3];
  const total = tier[2] + overage;
  return {
    provider,
    plan: tier[0],
    includedGb: tier[1],
    baseUsd: tier[2],
    overageUsd: Math.round(overage * 100) / 100,
    totalUsd: Math.round(total * 100) / 100,
    effectiveUsdPerGb: Math.round((total / Math.max(gb, 0.001)) * 1000) / 1000,
    gateway: GATEWAYS[provider],
  };
}

function compareAll(gb) {
  return Object.keys(PLANS).map((p) => effectiveCost(p, gb));
}

function cheapest(gb) {
  return compareAll(gb).reduce((a, b) => (b.totalUsd < a.totalUsd ? b : a));
}

function moneyTable(rows) {
  const width = 14;
  const line = (cells) => cells.map((c) => String(c).padEnd(width)).join("| ").trimEnd();
  const sep = "-".repeat(width * 6 + 8);
  const out = [sep, line(["NETWORK", "PLAN", "BASE/ MO", "OVERAGE", "TOTAL/ MO", "$/ GB"]), sep];
  rows.forEach((r) =>
    out.push(
      line([
        r.provider,
        r.plan.slice(0, 14),
        "$" + r.baseUsd.toFixed(2),
        "$" + r.overageUsd.toFixed(2),
        "$" + r.totalUsd.toFixed(2),
        "$" + r.effectiveUsdPerGb.toFixed(3),
      ])
    )
  );
  out.push(sep);
  return out.join("\n");
}

module.exports = {
  VERSION,
  GATEWAYS,
  PLANS,
  effectiveCost,
  compareAll,
  cheapest,
  moneyTable,
};
