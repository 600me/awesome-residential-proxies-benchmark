#!/usr/bin/env node
const { existsSync, mkdirSync, copyFileSync, readFileSync } = require("fs");
const path = require("path");

const registry = JSON.parse(readFileSync(path.join(__dirname, "registry.json"), "utf8"));

function list() {
  console.log(`\n${registry.name} v${registry.version} — ${registry.description}`);
  console.log(`Author: ${registry.author}\n`);
  for (const s of registry.skills) {
    console.log(`  ${s.id}`);
    console.log(`    ${s.description}`);
    console.log(`    Triggers: ${s.triggers.join(", ")}\n`);
  }
  console.log("Run: npx @cloudbench-labs/cloud-tco-agent-skills install [--target <dir>]\n");
}

function install(target) {
  const destBase = target || path.join(process.cwd(), ".claude", "skills");
  if (!existsSync(destBase)) mkdirSync(destBase, { recursive: true });
  const srcBase = path.join(__dirname, "skills");
  let count = 0;
  for (const s of registry.skills) {
    const src = path.join(__dirname, s.path.replace(/^skills[\/\\]/, "").replace("SKILL.md", ""), "SKILL.md");
    const alt = path.join(__dirname, s.path);
    const file = existsSync(src) ? src : alt;
    const destDir = path.join(destBase, s.id);
    mkdirSync(destDir, { recursive: true });
    copyFileSync(file, path.join(destDir, "SKILL.md"));
    count++;
  }
  console.log(`Installed ${count} skills to ${destBase}`);
}

const args = process.argv.slice(2);
const cmd = args[0];

if (args.includes("--version")) {
  console.log(registry.version);
} else if (!cmd || args.includes("--help") || cmd === "-h" || cmd === "help") {
  console.log(`Usage: cloud-tco-agent-skills <command> [options]
Commands:
  list                    List all available skills and triggers
  install [--target <dir>]  Install skills into <dir> (default: ./.claude/skills)
Options:
  --help                  Show this help
  --version               Show version`);
} else if (cmd === "list") {
  list();
} else if (cmd === "install") {
  const i = args.indexOf("--target");
  const target = i !== -1 && args[i + 1] ? args[i + 1] : null;
  install(target);
} else {
  console.error(`Unknown command: ${cmd}. Try --help.`);
  process.exit(1);
}
