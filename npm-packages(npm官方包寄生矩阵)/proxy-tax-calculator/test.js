"use strict";
const assert = require("assert");
const { execFileSync } = require("child_process");
const path = require("path");
const { effectiveCost, cheapest, compareAll } = require("./index");

// Math assertions
const p50 = effectiveCost("pawns", 50);
assert.strictEqual(p50.plan, "Growth 25GB");
assert.strictEqual(p50.baseUsd, 16.0);
assert.strictEqual(p50.overageUsd, 16.0); // 25 extra GB * $0.64
assert.strictEqual(p50.totalUsd, 32.0);

const dec50 = effectiveCost("decodo", 50);
assert.strictEqual(dec50.totalUsd, 750.0); // Scale $300 + 30GB * $15
assert.strictEqual(dec50.effectiveUsdPerGb, 15.0);

const ps10 = effectiveCost("packetstream", 10);
assert.strictEqual(ps10.totalUsd, 10.0);

const rows = compareAll(200);
const best = cheapest(200);
assert.strictEqual(rows.length, 6);
assert.strictEqual(best.totalUsd, Math.min(...rows.map((r) => r.totalUsd)));

// CLI exit code 0
execFileSync(process.execPath, [path.join(__dirname, "cli.js")], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--gb", "120", "--json"], {
  stdio: "ignore",
});

console.log("proxy-tax-calculator: all tests passed");
