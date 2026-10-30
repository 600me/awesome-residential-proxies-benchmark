"use strict";
const assert = require("assert");
const { execFileSync } = require("child_process");
const path = require("path");
const { gpuTco, mediaTco, voiceCost, videoCost, GPUS } = require("./index");

// GPU math: h100 @ 300 hours
const g = gpuTco("h100", 300);
assert.strictEqual(g.nominalCost, 747.0);
assert.strictEqual(g.coldStartCost, 22.41);
assert.strictEqual(g.effectiveOnDemandTco, 769.41);
assert.strictEqual(g.spotBaseCost, 387.0);
assert.strictEqual(g.spotPenalty, 58.05);
assert.strictEqual(g.effectiveSpotTco, 445.05);
assert(g.netSavingsUsd > 300);

// a100: rate 1.64 * 120 = 196.8, cold 5.9
const a = gpuTco("a100", 120);
assert.strictEqual(a.nominalCost, 196.8);
assert.strictEqual(a.effectiveOnDemandTco, 202.7);

// Voice: 500k chars -> Pro tier $99 quota, 0 overage
const v = voiceCost(500000);
assert.strictEqual(v.tierName, "Pro");
assert.strictEqual(v.totalUsd, 99.0);

// Video: 60 mins -> Team 30 base $89 + 30 overage @ $5 = $164
const vid = videoCost(60);
assert.strictEqual(vid.tierName, "Team");
assert.strictEqual(vid.baseUsd, 89);
assert.strictEqual(vid.overageUsd, 75);
assert.strictEqual(vid.totalUsd, 164.0);

// Media combined
const m = mediaTco(500000, 60);
assert.strictEqual(m.totalMonthlyTcoUsd, 263.0);

// All GPU models exist
["h100", "a100", "rtx5090", "rtx4090"].forEach((k) => assert(GPUS[k]));

// CLI exits 0 in markdown and JSON modes
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--gpu", "h100", "--hours", "300"], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--gpu", "a100", "--hours", "120", "--json"], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--voice-chars", "500000", "--video-mins", "60"], { stdio: "ignore" });
execFileSync(process.execPath, [path.join(__dirname, "cli.js"), "--help"], { stdio: "ignore" });

console.log("llm-gpu-cost-estimator: all tests passed");
