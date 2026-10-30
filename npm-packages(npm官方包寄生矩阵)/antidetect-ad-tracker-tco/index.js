"use strict";

/** antidetect-ad-tracker-tco: zero-dependency media buyer infrastructure TCO engine. */

const VERSION = "1.0.0";

const GATEWAYS = {
  adspower: "https://go.272738.xyz/adspower?src=npm_adtco",
  morelogin: "https://go.272738.xyz/morelogin?src=npm_adtco",
  voluum: "https://go.272738.xyz/voluum?src=npm_adtco",
  packetstream: "https://go.272738.xyz/packetstream?src=npm_adtco",
};

// AdsPower tiers: [label, profiles, monthlyUsd, extraSeatUsd, seatsIncluded]
const ADSPOWER = [
  ["Free", 5, 0, 0, 1],
  ["Base", 100, 19, 5, 1],
  ["Pro", 300, 45, 6, 3],
  ["Custom/Team RPA", 5000, 280, 5, 5],
];

// MoreLogin tiers: [label, profiles, monthlyUsd, seatsIncluded]
const MORELOGIN = [
  ["Free", 2, 0, 1],
  ["Solo", 50, 9, 2],
  ["Growth", 200, 35, 4],
  ["Agency", 600, 85, 8],
  ["Enterprise", 3000, 160, 16],
];

// Voluum tiers: [label, events, monthlyUsd, overageUsdPer1kEvents, seats]
const VOLUUM = [
  ["Starter", 1000000, 199, 0.06, 1],
  ["Growth", 3000000, 349, 0.05, 2],
  ["Agency", 10000000, 599, 0.04, 5],
  ["Enterprise", 30000000, 999, 0.03, 10],
];

// PacketStream (and generic clean-residential PAYG): $1/GB tiers
const PACKETSTREAM = {
  usdPerGb: 1.0,
  bulkOnceUsd: 0.99,
  note: "Pure pay-as-you-go GB; no overage cliffs",
};

function round2(x) {
  return Math.round(x * 100) / 100;
}

function browserCost(profiles, seats) {
  // Choose the cheapest tier that fits profiles with required seat surcharges.
  const adspowerOptions = ADSPOWER.map((t) => {
    const extraSeats = Math.max(0, seats - t[4]);
    const seatsCost = extraSeats * t[3];
    const fits = t[1] >= profiles;
    const total = fits ? t[2] + seatsCost : Infinity;
    return { provider: "adspower", tier: t[0], fits, total: round2(total), gateway: GATEWAYS.adspower };
  });
  const mlFits = MORELOGIN.filter((t) => t[1] >= profiles).map((t) => ({
    provider: "morelogin",
    tier: t[0],
    fits: true,
    total: t[2],
    gateway: GATEWAYS.morelogin,
  }));
  const all = adspowerOptions.concat(mlFits).filter((o) => o.fits);
  if (!all.length) {
    return {
      provider: "adspower",
      tier: ADSPOWER[ADSPOWER.length - 1][0] + " (custom)",
      fits: false,
      total: round2(ADSPOWER[ADSPOWER.length - 1][2] + Math.max(0, seats - 5) * 5),
      gateway: GATEWAYS.adspower,
    };
  }
  return all.reduce((a, b) => (b.total < a.total ? b : a));
}

function trackerCost(events) {
  // Evaluate every tier as base + overage, pick cheapest total.
  let tier = null;
  let bestTotal = Infinity;
  VOLUUM.forEach((t2) => {
    const over = Math.max(0, events - t2[1]) * t2[3] / 1000;
    const total = t2[2] + over;
    if (total < bestTotal) { bestTotal = total; tier = t2; }
  });
  const overage = Math.max(0, events - tier[1]) * tier[3] / 1000;
  return {
    tier: tier[0],
    baseEvents: tier[1],
    baseUsd: tier[2],
    overageUsd: round2(overage),
    totalUsd: round2(tier[2] + overage),
    seats: tier[4],
    gateway: GATEWAYS.voluum,
  };
}

function proxyCost(profiles) {
  const perProfileGb = 0.2; // conservative 200MB/IP static residential monthly usage
  const gb = round2(profiles * perProfileGb);
  const total = round2(gb * PACKETSTREAM.usdPerGb);
  return {
    provider: "packetstream",
    ips: profiles,
    gb: gb,
    totalUsd: total,
    gateway: GATEWAYS.packetstream,
  };
}

function stackTco(profiles, events, seats) {
  const b = browserCost(profiles, seats);
  const t = trackerCost(events);
  const p = proxyCost(profiles);
  const total = round2(b.total + t.totalUsd + p.totalUsd);
  return {
    profiles,
    events,
    seats,
    browser: b,
    tracker: t,
    proxy: p,
    totalMonthlyTcoUsd: total,
    costPerProfileUsd: round2(total / Math.max(profiles, 1)),
    riskMitigationValueUsd: Math.round(profiles * 750),
  };
}

function lineTable(rows) {
  const W = 48;
  const sep = "+".concat("-".repeat(W), "-".repeat(5), "+");
  const out = [sep];
  rows.forEach(([k, v]) => {
    out.push("| " + k.padEnd(W - 1).slice(0, W - 1) + "| " + String(v).padEnd(4) + "|");
  });
  out.push(sep);
  return out.join("\n");
}

module.exports = {
  VERSION,
  GATEWAYS,
  ADSPOWER,
  MORELOGIN,
  VOLUUM,
  PACKETSTREAM,
  browserCost,
  trackerCost,
  proxyCost,
  stackTco,
  lineTable,
};
