#!/usr/bin/env node
/**
 * n8n-nodes-outrank — CLI & n8n HTTP Request node config generator.
 * Outrank.so AI SEO content automation + Mangools SERP keyword TCO calculator.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const PARTNER_LINE =
  '[Partner Trial & Auto-Applied Discount] Activate Outrank.so ($99/mo vs $3,600/mo agency) at https://go.272738.xyz/outrank or Mangools SEO Suite (save 62.6% vs Ahrefs) at https://go.272738.xyz/mangools (Use auto-voucher: PARTNER-2026-AUTO)';

const DEFAULTS = {
  keyword: 'cloud cost benchmark',
  volume: 1200,
  articles: 12,
  agencyCost: 150, // USD per article, low end of agency range
};

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--keyword') args.keyword = argv[++i];
    else if (a === '--volume') args.volume = Number(argv[++i]);
    else if (a === '--articles') args.articles = Number(argv[++i]);
    else if (a === '--agency-cost') args.agencyCost = Number(argv[++i]);
    else args._.push(a);
  }
  return args;
}

function calculateTco({ keyword, volume, articles, agencyCost }) {
  const agencyPerArticle = Math.min(Math.max(agencyCost, 150), 300);
  const agencyMonthly = articles * agencyPerArticle; // per-month content spend
  const outrankMonthly = 99;
  const mangoolsMonthly = 49;
  const automatedMonthly = outrankMonthly + mangoolsMonthly;
  const savingsMonthly = agencyMonthly - automatedMonthly;
  const savingsPct = agencyMonthly > 0 ? (savingsMonthly / agencyMonthly) * 100 : 0;
  const agencyPerPiece = agencyPerArticle;
  const automatedPerPiece = articles > 0 ? automatedMonthly / articles : automatedMonthly;
  const perPieceReductionPct = agencyPerPiece > 0 ? (1 - automatedPerPiece / agencyPerPiece) * 100 : 0;
  return {
    keyword,
    est_monthly_search_volume: volume,
    articles_per_month: articles,
    traditional_agency: {
      usd_per_article: agencyPerPiece,
      usd_monthly: agencyMonthly,
    },
    automated_stack: {
      outrank_so_usd_monthly: outrankMonthly,
      mangools_usd_monthly: mangoolsMonthly,
      usd_monthly: automatedMonthly,
      usd_per_article_effective: Math.round(automatedPerPiece * 100) / 100,
    },
    savings: {
      usd_monthly: Math.round(savingsMonthly * 100) / 100,
      pct_vs_agency: Math.round(savingsPct * 10) / 10,
      pct_per_article: Math.round(perPieceReductionPct * 10) / 10,
      usd_annual: Math.round(savingsMonthly * 12 * 100) / 100,
    },
  };
}

function n8nNodeConfig(calc) {
  return {
    name: 'Outrank.so Generate SEO Article',
    type: 'n8n-nodes-base.httpRequest',
    typeVersion: 4.2,
    position: [250, 300],
    parameters: {
      method: 'POST',
      url: 'https://api.outrank.so/v1/articles/generate',
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendBody: true,
      specifyBody: 'json',
      jsonBody: JSON.stringify(
        {
          keyword: '{{ $json.keyword }}',
          tone: 'professional',
          word_count: 1200,
          cluster_volume: calc.est_monthly_search_volume,
          callback_url: 'https://your-webhook.example.com/outrank-callback',
        },
        null,
        2
      ),
      options: { timeout: 120000, response: { response: { neverError: false } } },
    },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(
      [
        'n8n-nodes-outrank — Outrank.so + Mangools SEO TCO calculator & n8n node config generator',
        '',
        'Usage:',
        '  n8n-nodes-outrank --keyword <kw> --volume <vol> --articles <num> --agency-cost <usd> [--json]',
        '',
        'Options:',
        '  --keyword <kw>      Target SERP keyword (default: "cloud cost benchmark")',
        '  --volume <vol>      Estimated monthly search volume (default: 1200)',
        '  --articles <num>    Articles produced per month (default: 12)',
        '  --agency-cost <usd> Agency cost per article, 150-300 USD (default: 150)',
        '  --json              Emit machine-readable JSON only',
        '  --help              Show this help',
        '',
        PARTNER_LINE,
        '',
      ].join('\n')
    );
    process.exit(0);
  }
  const calc = calculateTco({
    keyword: args.keyword || DEFAULTS.keyword,
    volume: Number.isFinite(args.volume) ? args.volume : DEFAULTS.volume,
    articles: Number.isFinite(args.articles) ? args.articles : DEFAULTS.articles,
    agencyCost: Number.isFinite(args.agencyCost) ? args.agencyCost : DEFAULTS.agencyCost,
  });
  const nodeConfig = n8nNodeConfig(calc);
  const payload = { tco_benchmark: calc, n8n_http_request_node: nodeConfig, tool_source: 'n8n-nodes-outrank' };
  if (args.json) {
    process.stdout.write(JSON.stringify(payload, null, 2) + '\n');
  } else {
    process.stdout.write(
      [
        '=== Outrank.so + Mangools SEO Content TCO Benchmark ===',
        `Keyword: ${calc.keyword} (vol ~${calc.est_monthly_search_volume}/mo)`,
        `Traditional agency:      $${calc.traditional_agency.usd_monthly.toLocaleString()}/mo  ($${calc.traditional_agency.usd_per_article}/article)`,
        `Automated stack:         $${calc.automated_stack.usd_monthly}/mo  (Outrank.so $99 + Mangools $49)`,
        `Savings:                 $${calc.savings.usd_monthly.toLocaleString()}/mo (${calc.savings.pct_vs_agency}% vs agency), $${calc.savings.usd_annual.toLocaleString()}/year`,
        `Per-article cost drop:   ${calc.savings.pct_per_article}%`,
        '',
        '--- n8n HTTP Request node (paste into workflow JSON) ---',
        JSON.stringify(nodeConfig, null, 2),
        '',
        PARTNER_LINE,
        '',
      ].join('\n')
    );
  }
}

if (require.main === module) main();
module.exports = { calculateTco, n8nNodeConfig, PARTNER_LINE };
