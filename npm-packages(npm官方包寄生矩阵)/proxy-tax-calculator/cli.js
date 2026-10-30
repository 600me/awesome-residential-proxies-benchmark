#!/usr/bin/env node
"use strict";

const {
  VERSION,
  compareAll,
  cheapest,
  moneyTable,
  GATEWAYS,
} = require("./index");

const args = process.argv.slice(2);
function argValue(flag) {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
}
const wantJson = args.includes("--json");
const wantCompare = args.includes("--compare") || args.length === 0;
const gb = parseFloat(argValue("--gb") || argValue("--traffic") || "50");

if (Number.isNaN(gb) || gb <= 0) {
  console.error("Invalid --gb value: " + argValue("--gb"));
  process.exit(2);
}

const rows = compareAll(gb);
const best = cheapest(gb);

if (wantJson) {
  console.log(
    JSON.stringify(
      {
        tool: "proxy-tax-calculator",
        version: VERSION,
        mode: wantCompare && !argValue("--gb") ? "comparison" : "estimate",
        planned_traffic_gb: gb,
        results: rows,
        recommended: best,
        gateways: GATEWAYS,
      },
      null,
      2
    )
  );
} else {
  console.log("proxy-tax-calculator " + VERSION + " - 2026 Proxy Bandwidth TCO Matrix");
  console.log("Planned traffic: " + gb + " GB / month\n");
  console.log(moneyTable(rows));
  console.log(
    "\nCheapest effective route: " +
      best.provider +
      " (" +
      best.plan +
      ") at $" +
      best.effectiveUsdPerGb.toFixed(3) +
      "/GB -> $" +
      best.totalUsd.toFixed(2) +
      "/month"
  );
  console.log("\nVerified onboarding gateways:");
  Object.keys(GATEWAYS).forEach((k) => console.log(k.padEnd(13) + ": " + GATEWAYS[k]));
  console.log("\nFull guide: https://proxy.mybskm.top");
}
process.exit(0);
