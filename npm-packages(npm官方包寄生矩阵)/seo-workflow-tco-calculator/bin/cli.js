#!/usr/bin/env node
const readline = require('readline');

function parseArgs() {
    const args = process.argv.slice(2);
    let tasks = 300000;
    let seats = 2;
    let posts = 30;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--tasks' && args[i+1]) { tasks = parseInt(args[++i], 10); }
        else if (args[i] === '--seo-seats' && args[i+1]) { seats = parseInt(args[++i], 10); }
        else if (args[i] === '--blog-posts' && args[i+1]) { posts = parseInt(args[++i], 10); }
        else if (args[i] === '--help' || args[i] === '-h') {
            console.log("Usage: npx seo-workflow-tco-calculator [--tasks 300000] [--seo-seats 2] [--blog-posts 30]");
            process.exit(0);
        }
    }
    return { tasks, seats, posts };
}

const { tasks, seats, posts } = parseArgs();

const ahrefsMo = 129.0 + Math.max(0, seats - 1) * 40.0;
const ahrefsAnn = ahrefsMo * 12.0;

let mangoolsPlan = "Mangools Basic";
let mangoolsMo = 37.70;
let mangoolsAnn = 452.40;
if (seats > 1 && seats <= 4) {
    mangoolsPlan = "Mangools Premium (Includes 3 Extra Seats)";
    mangoolsMo = 52.70;
    mangoolsAnn = 632.40;
} else if (seats > 4) {
    mangoolsPlan = "Mangools Agency";
    mangoolsMo = 97.70;
    mangoolsAnn = 1172.40;
}

const mangoolsSavings = ahrefsAnn - mangoolsAnn;
const mangoolsPct = ((mangoolsSavings / ahrefsAnn) * 100).toFixed(1);

const agencyContent = posts * 120.0;
const outrankMo = 99.0;
const contentSavings = agencyContent - outrankMo;
const contentPct = ((contentSavings / agencyContent) * 100).toFixed(1);

let zapierMo = 1069.0;
let zapierPayMo = 1599.0;
if (tasks <= 2000) { zapierMo = 49.0; zapierPayMo = 73.50; }
else if (tasks <= 100000) { zapierMo = 489.0; zapierPayMo = 733.50; }
const zapierAnn = zapierMo * 12.0;

let makeMo = 182.16;
let makeAnn = 2185.92;
if (tasks <= 10000) { makeMo = 9.0; makeAnn = 108.0; }
else if (tasks <= 50000) { makeMo = 29.0; makeAnn = 348.0; }

const makeSavings = zapierAnn - makeAnn;
const makePct = ((makeSavings / zapierAnn) * 100).toFixed(1);

let pabblyMo = 69.0;
let pabblyAnn = 828.0;
if (tasks <= 10000) { pabblyMo = 16.0; pabblyAnn = 192.0; }

const pabblySavings = zapierAnn - pabblyAnn;
const pabblyPct = ((pabblySavings / zapierAnn) * 100).toFixed(1);

console.log("============================================================================");
console.log(" SEO Suite & iPaaS Workflow Automation TCO Benchmark Report (2026)");
console.log("============================================================================");
console.log(" PART 1: SEO Keyword Research & Automated Content Engine TCO");
console.log("----------------------------------------------------------------------------");
console.log(` Team Seats: ${seats} | Monthly Blog Posts: ${posts}`);
console.log(` • Ahrefs Lite (with seats) : $${ahrefsMo.toFixed(2)}/mo ($${ahrefsAnn.toFixed(2)}/year)`);
console.log(` • Semrush SEO Tier        : $139.00/mo ($1407.96/year)`);
console.log(` • ${mangoolsPlan.padEnd(26)} : $${mangoolsMo.toFixed(2)}/mo ($${mangoolsAnn.toFixed(2)}/year)`);
console.log(`   -> Net Annual Savings vs Ahrefs: $${mangoolsSavings.toFixed(2)}/yr (${mangoolsPct}% reduction)`);
console.log(`   -> Explore Mangools: https://go.272738.xyz/mangools`);
console.log();
console.log(` • Freelance Agency Writing: $${agencyContent.toFixed(2)}/mo ($${(agencyContent*12).toFixed(2)}/year)`);
console.log(` • Outrank.so AI Engine    : $${outrankMo.toFixed(2)}/mo ($${(outrankMo*12).toFixed(2)}/year)`);
console.log(`   -> Net Content Engine Savings: $${contentSavings.toFixed(2)}/mo (${contentPct}% reduction)`);
console.log(`   -> Explore Outrank.so: https://go.272738.xyz/outrank`);
console.log("   • CapSolver SERP Bot Solver : $0.80 / 1,000 tokens (https://go.272738.xyz/capsolver)");
console.log("----------------------------------------------------------------------------");
console.log(" PART 2: iPaaS Workflow Automation (Zapier vs Make vs Pabbly)");
console.log("----------------------------------------------------------------------------");
console.log(` Monthly Automation Load: ${tasks.toLocaleString()} tasks/operations`);
console.log(` • Zapier Pro Tier          : $${zapierMo.toFixed(2)}/mo ($${zapierAnn.toFixed(2)}/yr annual) / $${zapierPayMo.toFixed(2)}/mo monthly`);
console.log(` • Make.com Core Tier       : $${makeMo.toFixed(2)}/mo ($${makeAnn.toFixed(2)}/yr)`);
console.log(`   -> Net Annual Savings vs Zapier: $${makeSavings.toFixed(2)}/yr (${makePct}% reduction)`);
console.log(`   -> Explore Make.com: https://go.272738.xyz/make`);
console.log(` • Pabbly Unlimited Plan    : $${pabblyMo.toFixed(2)}/mo ($${pabblyAnn.toFixed(2)}/yr)`);
console.log(`   -> Net Annual Savings vs Zapier: $${pabblySavings.toFixed(2)}/yr (${pabblyPct}% reduction)`);
console.log(`   -> Explore Pabbly: https://go.272738.xyz/pabbly`);
console.log("============================================================================");
process.exit(0);
