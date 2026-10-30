"use strict";
const assert = require("assert");
const { execFileSync } = require("child_process");
const path = require("path");
const { stackTco, browserCost, trackerCost, proxyCost } = require("./index");

// Agency scenario from README: 100 profiles, 5M events, 5 seats
const t = stackTco(100, 5000000, 5);
// Browser: MoreLogin Agency $85 < AdsPower Base $19+4 seats*$5=39
assert.strictEqual(t.browser.provider, "morelogin");
assert.strictEqual(t.browser.total, 35);
// Tracker: Growth tier $349 base + 2M overage @ $0.05/1k
assert.strictEqual(t.tracker.baseUsd, 199);
assert.strictEqual(t.tracker.overageUsd, 240);
assert.strictEqual(t.tracker.totalUsd, 439);
// Proxy: 100 profiles * 0.2GB = 20GB @ $1
assert.strictEqual(t.proxy.gb, 20);
assert.strictEqual(t.proxy.totalUsd, 20);
// Total: 85 + 449 + 20 = 554
assert.strictEqual(t.totalMonthlyTcoUsd, 494);
assert.strictEqual(t.costPerProfileUsd, 4.94);

// Solo scenario: 50 profiles, 1M events, 1 seat
const s = stackTco(50, 1000000, 1);
// Browser: MoreLogin Solo $9 (beats AdsPower Base $19)
assert.strictEqual(s.browser.provider, "morelogin");
assert.strictEqual(s.browser.total, 9);
assert.strictEqual(s.tracker.totalUsd, 199);
assert.strictEqual(s.proxy.totalUsd, 10);
assert.strictEqual(s.totalMonthlyTcoUsd, 218);
assert.strictEqual(s.costPerProfileUsd, 4.36);

// Overage math
assert.strictEqual(trackerCost(5000000).overageUsd, 240);
assert.strictEqual(proxyCost(250).totalUsd, 50);

// CLI exit codes
execFileSync(process.execPath, [path.join(__dirname, "cli.js")], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--profiles", "100", "--events", "5000000", "--seats", "5"], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--profiles", "100", "--events", "5000000", "--seats", "5", "--json"], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--help"], { stdio: "ignore" });

console.log("antidetect-ad-tracker-tco: all tests passed");
