"use strict";
const assert = require("assert");
const { execFileSync } = require("child_process");
const path = require("path");
const { llcTco, STATES } = require("./index");

// Wyoming 3-year: 102 + 62*2 + 99*3 + 200 + 50 + 10*36 + 500*3 = 2633
const wy = llcTco("wyoming", 3);
assert.strictEqual(wy.initialStateFee, 102);
assert.strictEqual(wy.stateAnnualReportTotal, 124);
assert.strictEqual(wy.registeredAgentTotal, 297);
assert.strictEqual(wy.virtualMailAddressTotal, 360);
assert.strictEqual(wy.irsForm5472Total, 1500);
assert.strictEqual(wy.tcoTotal, 2633);
assert.strictEqual(wy.monthlyAmortized, 73.14);

// Delaware 3-year: 110 + 300*2 + 297 + 200 + 50 + 360 + 1500 = 3117
const de = llcTco("delaware", 3);
assert.strictEqual(de.tcoTotal, 3117);
assert.strictEqual(de.monthlyAmortized, 86.58);

// 1-year horizon and bad state handling
assert.strictEqual(llcTco("wyoming", 1).stateAnnualReportTotal, 0);
assert.throws(() => llcTco("nevada", 3));
assert.throws(() => llcTco("wyoming", 0));
assert.throws(() => llcTco("wyoming", 2.5));

// CLI exit codes
execFileSync(process.execPath, [path.join(__dirname, "cli.js")], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--state", "delaware", "--years", "3"], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--state", "wyoming", "--years", "3", "--json"], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--compare-formation"], { stdio: "ignore" });
try { execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--state", "nevada"], { stdio: "ignore" }); assert.fail("nevada should exit nonzero"); } catch (_) {}

console.log("us-llc-stripe-tco: all tests passed");
