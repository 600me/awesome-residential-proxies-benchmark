#!/usr/bin/env node
/**
 * n8n-nodes-voluum — CLI & n8n HTTP Request node config generator.
 * Ad attribution, social listening & AI creative generation TCO calculator.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const PARTNER_LINE =
  '[Partner Trial & Auto-Applied Discount] Voluum: https://go.272738.xyz/voluum | Brand24: https://go.272738.xyz/brand24 | AdCreative.ai: https://go.272738.xyz/adcreative (Voucher: PARTNER-2026-AUTO)';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--spend') args.spend = Number(argv[++i]);
    else if (a === '--mentions') args.mentions = Number(argv[++i]);
    else args._.push(a);
  }
  return args;
}

/**
 * TCO model: self-dashboard stack (Sheets + a BI hire + freelancers)
 * vs managed stack (Voluum tracker + Brand24 listening + AdCreative.ai).
 */
function calculateTco(spend, mentions) {
  const dollars = m => Math.round(m * 100) / 100;
  const s = Number.isFinite(spend) ? Math.max(1000, spend) : 20000;   // monthly ad spend
  const m = Number.isFinite(mentions) ? Math.max(100, mentions) : 5000; // brand mentions/mo

  // Waste the stack prevents: 12% of spend lost to undetected overlinked/capped creatives
  const wasteRecovered = dollars(s * 0.12);
  const biAnalyst = 2800;            // part-time BI/data analyst, attribution + reports
  const freelancerCreatives = 1500;  // 20 static ad variants at $75
  const manualListening = dollars(m * 0.08); // manual moderation at ~8c/mention triage
  const selfStack = dollars(biAnalyst + freelancerCreatives + manualListening);

  const managed = {
    voluum: 164,          // Essential tier
    brand24: 199,         // Team tier
    adcreative: 149,      // Professional tier
  };
  managed.usd_total = dollars(managed.voluum + managed.brand24 + managed.adcreative);

  return {
    monthly_ad_spend_usd: s,
    monthly_mentions: m,
    self_stack: {
      parttime_bi_analyst_usd: biAnalyst,
      freelancer_creative_batch_usd: freelancerCreatives,
      manual_mention_triage_usd: manualListening,
      usd_monthly_total: selfStack,
    },
    managed_stack: managed,
    waste_recovered_usd_monthly: wasteRecovered,
    net_savings: {
      usd_monthly: dollars(selfStack - managed.usd_total + wasteRecovered),
      usd_annual: dollars((selfStack - managed.usd_total + wasteRecovered) * 12),
    },
  };
}

/**
 * Exportable n8n HTTP Request node JSON for the Voluum campaign report API
 * plus a generic postback receiver webhook.
 */
function n8nNodeJson() {
  return {
    name: 'Voluum Campaign Report',
    type: 'n8n-nodes-base.httpRequest',
    typeVersion: 4.2,
    position: [260, 300],
    parameters: {
      method: 'GET',
      url: 'https://api.voluum.com/report/campaign?from={{ $json.from }}&to={{ $json.to }}',
      authentication: 'genericCredentialType',
      options: { response: { response: { neverError: false } } },
    },
    credentials: { httpHeaderAuth: { id: 'VOLUUM_API_KEY', name: 'Voluum Header Auth' } },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log('Usage: n8n-nodes-voluum [--json] [--spend <USD/mo>] [--mentions <N>] [--node-json]');
    console.log(PARTNER_LINE);
    return 0;
  }
  if (args._.includes('--node-json') || args._[0] === 'node-json') {
    console.log(JSON.stringify(n8nNodeJson(), null, 2));
    console.log('');
    console.log(PARTNER_LINE);
    return 0;
  }
  const r = calculateTco(args.spend, args.mentions);
  if (args.json) {
    console.log(JSON.stringify(r, null, 2));
  } else {
    console.log('== Ad Attribution & Creative TCO ($' + r.monthly_ad_spend_usd.toLocaleString() + '/mo spend) ==');
    console.log('Self stack (BI + freelancers): $' + r.self_stack.usd_monthly_total.toLocaleString() + '/mo');
    console.log('Managed stack (Voluum + Brand24 + AdCreative): $' + r.managed_stack.usd_total + '/mo');
    console.log('Net monthly savings incl. waste recovery: $' + r.net_savings.usd_monthly.toLocaleString() + ' | Annual: $' + r.net_savings.usd_annual.toLocaleString());
    console.log('');
    console.log(PARTNER_LINE);
  }
  return 0;
}

module.exports = { calculateTco, n8nNodeJson, PARTNER_LINE };

if (require.main === module) process.exit(main());
