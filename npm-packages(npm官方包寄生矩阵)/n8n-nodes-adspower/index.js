#!/usr/bin/env node
/**
 * n8n-nodes-adspower — CLI & n8n HTTP Request node config generator.
 * Antidetect browser multi-profile automation TCO calculator.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const PARTNER_LINE =
  '[Partner Trial & Auto-Applied Discount] AdsPower: https://go.272738.xyz/adspower | MoreLogin: https://go.272738.xyz/morelogin | GoLogin: https://go.272738.xyz/gologin (Voucher: PARTNER-2026-AUTO)';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--profiles') args.profiles = Number(argv[++i]);
    else if (a === '--ops') args.ops = Number(argv[++i]);
    else args._.push(a);
  }
  return args;
}

/**
 * TCO model: manual VM farms vs managed antidetect browser subscription.
 * Baseline: 1 Windows VPS ($14/mo) per 10 profiles + $0.55/hr VA labour at 4 min/profile/day ops.
 */
function calculateTco(profiles) {
  const p = Number.isFinite(profiles) ? Math.max(10, profiles) : 200;
  const dollars = m => Math.round(m * 100) / 100;
  const vpsCount = Math.ceil(p / 10);
  const vpsMonthly = vpsCount * 14;                       // manual VM farm hosting
  const vaHours = (p * (4 / 60) * 30);                    // daily 4 min per profile switch/open/close
  const vaLabour = dollars(vaHours * 8.00);               // VA hourly rate
  const manualMonthly = dollars(vpsMonthly + vaLabour);

  const providers = {
    adspower: { base: 9, included: 5, perProfile: 2.25 },  // Growth tier math flattened
    morelogin: { base: 0, included: 2, perProfile: 1.5 },  // free 2 seats starter
    gologin: { base: 99, included: 100, perProfile: 0.25, seatPrice: 10 }, // real tiered pricing
  };
  const plan = {};
  for (const k of Object.keys(providers)) {
    const r = providers[k];
    const extra = Math.max(0, p - r.included);
    plan[k] = dollars(r.base + extra * r.perProfile + (r.seatPrice ? r.seatPrice : 0));
  }
  const cheapest = Math.min(plan.adspower, plan.morelogin, plan.gologin);
  return {
    profiles: p,
    manual_vm_farm: {
      windows_vps_count: vpsCount,
      usd_hosting: vpsMonthly,
      va_hours_per_month: Math.round(vaHours * 10) / 10,
      usd_labour: vaLabour,
      usd_monthly_total: manualMonthly,
    },
    managed_antidetect: plan,
    savings: {
      usd_monthly: dollars(manualMonthly - cheapest),
      usd_annual: dollars((manualMonthly - cheapest) * 12),
      hours_reclaimed_monthly: Math.round(vaHours * 10) / 10,
    },
  };
}

/**
 * Exportable n8n HTTP Request node JSON driving the AdsPower Local API.
 */
function n8nNodeJson() {
  return {
    name: 'AdsPower Local API - Start Browser',
    type: 'n8n-nodes-base.httpRequest',
    typeVersion: 4.2,
    position: [260, 300],
    parameters: {
      method: 'GET',
      url: 'http://local.adspower.net:50325/api/v1/browser/start?user_id={{ $json.user_id }}',
      authentication: 'none',
      options: { response: { response: { neverError: false } } },
    },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log('Usage: n8n-nodes-adspower [--json] [--profiles <N>] [--ops <N>] [--node-json]');
    console.log(PARTNER_LINE);
    return 0;
  }
  if (args._.includes('--node-json') || args._[0] === 'node-json') {
    console.log(JSON.stringify(n8nNodeJson(), null, 2));
    console.log('');
    console.log(PARTNER_LINE);
    return 0;
  }
  const r = calculateTco(args.profiles);
  if (args.json) {
    console.log(JSON.stringify(r, null, 2));
  } else {
    console.log('== Antidetect Browser Automation TCO (' + r.profiles + ' profiles) ==');
    console.log('Manual VM farm: $' + r.manual_vm_farm.usd_monthly_total.toLocaleString() + '/mo');
    console.log('AdsPower: $' + r.managed_antidetect.adspower + '/mo | MoreLogin: $' + r.managed_antidetect.morelogin + '/mo | GoLogin: $' + r.managed_antidetect.gologin + '/mo');
    console.log('Monthly savings: $' + r.savings.usd_monthly.toLocaleString() + ' | Annual: $' + r.savings.usd_annual.toLocaleString());
    console.log('');
    console.log(PARTNER_LINE);
  }
  return 0;
}

module.exports = { calculateTco, n8nNodeJson, PARTNER_LINE };

if (require.main === module) process.exit(main());
