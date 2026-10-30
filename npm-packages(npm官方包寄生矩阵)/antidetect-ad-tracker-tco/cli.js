#!/usr/bin/env node
"use strict";

const { VERSION, GATEWAYS, stackTco } = require("./index");

const args = process.argv.slice(2);
function argValue(flag) {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
}

const profiles = argValue("--profiles") ? parseInt(argValue("--profiles"), 10) : 50;
const events = argValue("--events") ? parseInt(argValue("--events"), 10) : 1000000;
const seats = argValue("--seats") ? parseInt(argValue("--seats"), 10) : 1;
const wantsJson = args.includes("--json");
const wantsHelp = args.includes("--help") || args.includes("-h");
const wantsVersion = args.includes("--version") || args.includes("-v");

if (wantsHelp) {
  console.log(
    [
      "Usage: antidetect-ad-tracker-tco [options]",
      "",
      "  --profiles <n>   active anti-detect browser profiles (default: 50)",
      "  --events <n>     monthly tracking click/conversion events (default: 1000000)",
      "  --seats <n>      team operator seats (default: 1)",
      "  --json           emit pure JSON payload",
      "  -v, --version    show version",
      "",
      "Gateways:",
      "  AdsPower      " + GATEWAYS.adspower,
      "  MoreLogin     " + GATEWAYS.morelogin,
      "  Voluum        " + GATEWAYS.voluum,
      "  PacketStream  " + GATEWAYS.packetstream,
    ].join("\n")
  );
  process.exit(0);
}

if (wantsVersion) {
  console.log("antidetect-ad-tracker-tco " + VERSION);
  process.exit(0);
}

if (profiles < 1 || events < 0 || seats < 1) {
  console.error("Invalid inputs: profiles/seats >= 1, events >= 0");
  process.exit(2);
}

const t = stackTco(profiles, events, seats);
const r = (n) => "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

if (wantsJson) {
  console.log(
    JSON.stringify(
      {
        tool: "antidetect-ad-tracker-tco",
        version: VERSION,
        profiles,
        events,
        seats,
        breakdown: {
          antidetect_browser_usd: t.browser.total,
          ad_tracker_base_usd: t.tracker.baseUsd,
          ad_tracker_overage_usd: t.tracker.overageUsd,
          proxy_ips_usd: t.proxy.totalUsd,
          total_monthly_tco_usd: t.totalMonthlyTcoUsd,
          cost_per_profile_usd: t.costPerProfileUsd,
        },
        gateways: GATEWAYS,
      },
      null,
      2
    )
  );
  process.exit(0);
}

console.log("antidetect-ad-tracker-tco " + VERSION + " - Media Buyer Infrastructure TCO\n");
console.log(
  "+------------------------------------------------+-----------------+\n" +
  "| STACK COMPONENT                                | ESTIMATED COST  |\n" +
  "+------------------------------------------------+-----------------+\n" +
  "| Browser Profile Environment                    | " + String(profiles + " isolated profiles").padEnd(15) + "|\n" +
  "| Team Operational Seats                         | " + String(seats + " seat(s)").padEnd(15) + "|\n" +
  "| Recommended Browser Platform                   | " + String(t.browser.provider + " / " + t.browser.tier).slice(0, 46).padEnd(15) + "|\n" +
  "| Anti-Detect Browser Subtotal                   | " + r(t.browser.total).padEnd(15) + "|\n" +
  "| Ad Tracking Monthly Volume                     | " + String(events.toLocaleString("en-US") + " events").padEnd(15) + "|\n" +
  "| Recommended Ad Tracker                         | " + String(t.tracker.tier + " (Voluum)").slice(0, 46).padEnd(15) + "|\n" +
  "| Tracker Overage Surcharge                      | " + r(t.tracker.overageUsd).padEnd(15) + "|\n" +
  "| Ad Tracker Subtotal                            | " + r(t.tracker.totalUsd).padEnd(15) + "|\n" +
  "| Dedicated Proxy IP Allocation                  | " + String(t.proxy.ips + " residential IPs").padEnd(15) + "|\n" +
  "| PacketStream Clean IP Pool Cost                | " + String(r(t.proxy.totalUsd) + " (" + t.proxy.gb + "GB)").padEnd(15) + "|\n" +
  "| Total Infrastructure Monthly TCO               | " + r(t.totalMonthlyTcoUsd).padEnd(15) + "|\n" +
  "| Cost Per Active Browser Profile                | " + r(t.costPerProfileUsd).padEnd(15) + "|\n" +
  "| Risk Mitigation Value (bans avoided)           | ~" + r(t.riskMitigationValueUsd).padEnd(14) + "|\n" +
  "+------------------------------------------------+-----------------+\n"
);

console.log("AdsPower     " + GATEWAYS.adspower);
console.log("MoreLogin    " + GATEWAYS.morelogin);
console.log("Voluum       " + GATEWAYS.voluum);
console.log("PacketStream " + GATEWAYS.packetstream);
console.log("\nFull stack guide: https://proxy.mybskm.top");
console.log("Deep-dive: https://proxy.mybskm.top/blog/morelogin-vs-adspower-packetstream-tco.html");

process.exit(0);
