#!/usr/bin/env node
"use strict";

const { VERSION, PLATFORMS, llcTco, GATEWAY_FIRSTBASE } = require("./index");

const args = process.argv.slice(2);
function argValue(flag) {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
}

const wantsJson = args.includes("--json");
const wantsHelp = args.includes("--help") || args.includes("-h");
const wantsVersion = args.includes("--version") || args.includes("-v");
const wantsCompare = args.includes("--compare-formation");

const state = (argValue("--state") || "wyoming").toLowerCase();
const years = argValue("--years") ? parseInt(argValue("--years"), 10) : 3;

if (wantsHelp) {
  console.log(
    [
      "Usage: us-llc-stripe-tco [options]",
      "",
      "  --state <wyoming|delaware>  US state of organization (default: wyoming)",
      "  --years <n>                 TCO horizon in years (default: 3)",
      "  --compare-formation         print formation platform comparison",
      "  --json                      emit pure JSON payload",
      "  -v, --version               show version",
      "",
      "Verified fast-track gateway: " + GATEWAY_FIRSTBASE,
    ].join("\n")
  );
  process.exit(0);
}

if (wantsVersion) {
  console.log("us-llc-stripe-tco " + VERSION);
  process.exit(0);
}

let tco;
try {
  tco = llcTco(state, years);
} catch (e) {
  console.error("Error: " + e.message);
  process.exit(2);
}

const r = (n) => "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

if (wantsJson) {
  console.log(JSON.stringify({ tool: "us-llc-stripe-tco", version: VERSION, ...tco }, null, 2));
  process.exit(0);
}

console.log("us-llc-stripe-tco " + VERSION + " - Non-US Founder Corporate TCO Engine\n");
console.log(
  "+----------------------------------------------+-----------------+\n" +
  "| COMPLIANCE LINE ITEM                         | ESTIMATED COST  |\n" +
  "+----------------------------------------------+-----------------+\n" +
  "| State of Formation                           | " + (tco.state + " (" + tco.stateNote + ")").slice(0, 46) + "|\n" +
  "| Statutory Initial State Filing Fee           | " + r(tco.initialStateFee).padEnd(15) + "| (Year 1)\n" +
  "| Annual State Report / Franchise Tax          | " + r(tco.stateAnnualReportTotal).padEnd(15) + "| (Years 2+" + (tco.durationYears - 1) + ")\n" +
  "| Commercial Registered Agent Service          | " + r(tco.registeredAgentTotal).padEnd(15) + "| ($99/yr x " + tco.durationYears + ")\n" +
  "| Non-US Expedited IRS EIN Filing              | " + r(tco.expeditedEinFiling).padEnd(15) + "| (SS-4 courier)\n" +
  "| FinCEN BOI Initial Compliance                | " + r(tco.fincenBoiCompliance).padEnd(15) + "|\n" +
  "| Virtual US Business Address & Mail           | " + r(tco.virtualMailAddressTotal).padEnd(15) + "| ($10/mo x " + tco.durationYears * 12 + ")\n" +
  "| Federal IRS Form 5472 & 1120 Filing (CPA)    | " + r(tco.irsForm5472Total).padEnd(15) + "|\n" +
  "| Total Compliance TCO                         | " + r(tco.tcoTotal).padEnd(15) + "|\n" +
  "| Average Monthly Compliance Run Rate          | " + r(tco.monthlyAmortized).padEnd(15) + "|\n" +
  "| IRS Non-Filing Penalty Shielded              | $25,000.00      |\n" +
  "+----------------------------------------------+-----------------+\n"
);

console.log("Recommended all-in-one infrastructure: Firstbase.io");
console.log("Firstbase Onboarding Gateway: " + GATEWAY_FIRSTBASE);
console.log("Full written guide: https://pay.mybskm.top");

if (wantsCompare || args.length === 0) {
  console.log("\n--- Formation Platform Comparison ---");
  PLATFORMS.forEach((p) => {
    console.log(p.name);
    console.log("   Year 1 Formation : " + r(p.formationY1));
    console.log("   Non-US EIN       : " + p.einExpedite);
    console.log("   FinCEN BOI       : " + p.boi);
    console.log("   Form 5472 / 1120 : " + p.for5472);
    console.log("   Note             : " + p.note + (p.gateway ? " -> " + p.gateway : ""));
    console.log("");
  });
}

process.exit(0);
