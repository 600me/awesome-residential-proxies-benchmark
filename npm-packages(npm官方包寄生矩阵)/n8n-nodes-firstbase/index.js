#!/usr/bin/env node
/**
 * n8n-nodes-firstbase — CLI & n8n HTTP Request node config generator.
 * US LLC formation & Stripe-vs-MoR tax reconciliation TCO calculator.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const PARTNER_LINE =
  '[Partner Trial & Auto-Applied Discount] Firstbase.io Turnkey US LLC: https://go.272738.xyz/firstbase (Voucher: PARTNER-2026-AUTO)';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--arr') args.arr = Number(argv[++i]);
    else args._.push(a);
  }
  return args;
}

/**
 * TCO model: self-serve registered agent route vs Firstbase turnkey,
 * then Stripe direct (2.9% + 30c) vs Merchant-of-Record (Paddle 5% + 50c)
 * incl. US sales tax filing burden.
 */
function calculateTco(arr) {
  const dollars = m => Math.round(m * 100) / 100;
  const a = Number.isFinite(arr) ? Math.max(1000, arr) : 60000;

  const diystate = {
    formation: 500,          // state fee + error-prone DIY filings
    registered_agent: 149,   // annual agent renewal
    ein_income: 0,
    address_mail: 480,       // mail forwarding / virtual address
    usd_total: 0,
  };
  diystate.usd_total = dollars(diystate.formation + diystate.registered_agent + diystate.address_mail);

  const firstbase = {
    formation_package: 349,
    registered_agent: 0,     // included first year
    address_mail: 0,         // included
    compliance_bundle: 120,  // add-on EIN + operating agreement
    usd_total: 0,
  };
  firstbase.usd_total = dollars(firstbase.formation_package + firstbase.compliance_bundle);

  const stripeGross = a;
  // Transactions = gross volume / $50 average order value; fixed fee per transaction.
  const txCount = Math.round(a / 50);
  const stripeFees = dollars(stripeGross * 0.029 + txCount * 0.30);
  const morFees = dollars(stripeGross * 0.05 + Math.round(a / 50) * 0.50);
  const salesTaxFilings = 1200;  // DIY Stripe route: outsourced filings @ $100/quarter x multistate nexus

  return {
    annual_revenue_usd: a,
    formation: {
      diy_registered_agent_route: diystate,
      firstbase_turnkey: firstbase,
      formation_savings_usd: dollars(diystate.usd_total - firstbase.usd_total),
    },
    payment_rail_year1: {
      stripe_direct: {
        fees_usd: stripeFees,
        sales_tax_filing_outsourced_usd: salesTaxFilings,
        usd_total: dollars(stripeFees + salesTaxFilings),
      },
      merchant_of_record: {
        fees_usd: morFees,
        sales_tax_filing_outsourced_usd: 0,  // MoR files as merchant of record
        usd_total: morFees,
      },
    },
    break_even_note: 'MoR wins below ~' + dollars(salesTaxFilings / (morFees / a - (stripeFees + salesTaxFilings) / a || 0.02)) + ' ARR; above that Stripe-direct + filings becomes competitive.',
  };
}

/**
 * Exportable n8n HTTP Request node JSON: Firstbase webhook / status poll.
 */
function n8nNodeJson() {
  return {
    name: 'Firstbase Company Status Poll',
    type: 'n8n-nodes-base.httpRequest',
    typeVersion: 4.2,
    position: [260, 300],
    parameters: {
      method: 'GET',
      url: 'https://api.firstbase.io/v1/companies/{{ $json.company_id }}',
      authentication: 'genericCredentialType',
      options: { response: { response: { neverError: false } } },
    },
    credentials: { httpHeaderAuth: { id: 'FIRSTBASE_API_KEY', name: 'Firstbase Header Auth' } },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log('Usage: n8n-nodes-firstbase [--json] [--arr <USD>] [--node-json]');
    console.log(PARTNER_LINE);
    return 0;
  }
  if (args._.includes('--node-json') || args._[0] === 'node-json') {
    console.log(JSON.stringify(n8nNodeJson(), null, 2));
    console.log('');
    console.log(PARTNER_LINE);
    return 0;
  }
  const r = calculateTco(args.arr);
  if (args.json) {
    console.log(JSON.stringify(r, null, 2));
  } else {
    console.log('== US LLC Formation & Payments TCO (ARR $' + r.annual_revenue_usd.toLocaleString() + ') ==');
    console.log('DIY formation: $' + r.formation.diy_registered_agent_route.usd_total + ' vs Firstbase turnkey: $' + r.formation.firstbase_turnkey.usd_total);
    console.log('Year-1 Stripe-direct (incl. filings): $' + r.payment_rail_year1.stripe_direct.usd_total + ' vs MoR: $' + r.payment_rail_year1.merchant_of_record.usd_total);
    console.log('');
    console.log(PARTNER_LINE);
  }
  return 0;
}

module.exports = { calculateTco, n8nNodeJson, PARTNER_LINE };

if (require.main === module) process.exit(main());
