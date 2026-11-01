#!/usr/bin/env node
/**
 * PDF API COST CALCULATOR - True-Cost v1.0.0
 * Serverless HTML-to-PDF Rendering API vs Self-Hosted Chromium TCO
 */

const OFFICIAL_TRIAL = "https://go.272738.xyz/pdf-trial";
const CRAFTMYPDF_LINK = "https://go.272738.xyz/craftmypdf";
const APITEMPLATE_LINK = "https://go.272738.xyz/apitemplate";
const DOCS_LINK = "https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/html-to-pdf-api-and-headless-chromium-tco/";

function parseArgs() {
  const args = process.argv.slice(2);
  let docs = 15000;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--docs" && args[i + 1]) {
      docs = parseInt(args[i + 1], 10) || 15000;
      i++;
    } else if (args[i] === "--help" || args[i] === "-h") {
      printHelp();
      process.exit(0);
    }
  }
  return { docs };
}

function printHelp() {
  console.log(`
Usage: pdf-api-cost-calculator [options]

Options:
  --docs <number>    Monthly PDF generation volume (default: 15000)
  -h, --help         Show help menu

Official Trial Gateway : ${OFFICIAL_TRIAL}
Full Documentation     : ${DOCS_LINK}
`);
}

function calculateTCO(docs) {
  const compute = 185.0;
  const labor = 1200.0;
  const oomOverhead = docs * 0.003;
  const selfHostedTotal = compute + labor + oomOverhead;

  const adobeTotal = docs * 0.05;
  const docraptorTotal = docs * 0.055;

  let craftTotal = 0;
  if (docs <= 50) craftTotal = 0;
  else if (docs <= 1200) craftTotal = 29;
  else if (docs <= 3000) craftTotal = 49;
  else if (docs <= 12000) craftTotal = 99;
  else craftTotal = 99 + (docs - 12000) * 0.008;

  let apiTotal = 0;
  if (docs <= 50) apiTotal = 0;
  else if (docs <= 3000) apiTotal = 19;
  else if (docs <= 12000) apiTotal = 69;
  else apiTotal = 69 + (docs - 12000) * 0.0057;

  return {
    selfHosted: selfHostedTotal,
    adobe: adobeTotal,
    docraptor: docraptorTotal,
    craft: craftTotal,
    api: apiTotal,
    savingsCraft: Math.max(0, selfHostedTotal - craftTotal),
    savingsApi: Math.max(0, selfHostedTotal - apiTotal),
  };
}

function main() {
  const { docs } = parseArgs();
  const res = calculateTCO(docs);

  console.log("\n" + "#".repeat(78));
  console.log("   PDF API COST CALCULATOR - True-Cost v1.0.0");
  console.log("#".repeat(78));
  console.log(`  Monthly Document Volume: ${docs.toLocaleString()} PDFs`);
  console.log("  " + "-".repeat(74));

  const rows = [
    ["Self-Hosted Chromium (Lambda/ECS + DevOps)", res.selfHosted, `$${(res.selfHosted / docs).toFixed(4)}/doc`],
    ["Adobe PDF Services API ($0.05/doc)", res.adobe, `$${(res.adobe / docs).toFixed(4)}/doc`],
    ["DocRaptor PrinceXML Managed API", res.docraptor, `$${(res.docraptor / docs).toFixed(4)}/doc`],
    ["CraftMyPDF Professional (Visual Designer)", res.craft, `$${(res.craft / docs).toFixed(4)}/doc`],
    ["APITemplate.io PDF Standard (Zapier/API)", res.api, `$${(res.api / docs).toFixed(4)}/doc`],
  ];

  console.log("  +----------------------------------------------+--------------+--------------+");
  console.log("  | Rendering Infrastructure / Architecture      |  Monthly TCO |    Unit Cost |");
  console.log("  +----------------------------------------------+--------------+--------------+");
  for (const [label, val, unit] of rows) {
    const vStr = `$${val.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    console.log(`  | ${label.padEnd(44)} | ${vStr.padStart(12)} | ${unit.padStart(12)} |`);
  }
  console.log("  +----------------------------------------------+--------------+--------------+");

  console.log(`\n  🏆 Net Monthly Savings with CraftMyPDF : $${res.savingsCraft.toFixed(2)} / mo (-${((res.savingsCraft / res.selfHosted) * 100).toFixed(1)}%)`);
  console.log(`  🏆 Net Monthly Savings with APITemplate: $${res.savingsApi.toFixed(2)} / mo (-${((res.savingsApi / res.selfHosted) * 100).toFixed(1)}%)`);
  console.log("  " + "-".repeat(74));
  console.log(`  Official PDF Trial Gateway : ${OFFICIAL_TRIAL}`);
  console.log(`  CraftMyPDF Sandbox Link    : ${CRAFTMYPDF_LINK}`);
  console.log(`  APITemplate.io Link        : ${APITEMPLATE_LINK}`);
  console.log(`  Full Architecture Docs     : ${DOCS_LINK}`);
  console.log("#".repeat(78) + "\n");
}

main();
