#!/usr/bin/env node
/**
 * n8n-nodes-webshare — CLI & n8n proxy-rotation HTTP Request node config generator.
 * Webshare / Decodo residential proxy retry-loss ("block tax") calculator.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const PARTNER_LINE =
  '[Partner Trial & Auto-Applied Discount] Activate Webshare (10 Free Proxies + $1.80/GB) at https://go.272738.xyz/webshare, Decodo ($2.20/GB) at https://go.272738.xyz/decodo, ScraperAPI (Unblocker) at https://go.272738.xyz/scraperapi, CapSolver at https://go.272738.xyz/capsolver (Voucher: PARTNER-2026-AUTO)';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--requests') args.requests = Number(argv[++i]);
    else if (a === '--block-rate') args.blockRate = Number(argv[++i]);
    else args._.push(a);
  }
  return args;
}

/**
 * Retry amplification: with per-request block rate p, expected total requests
 * per successful fetch = 1/(1-p). This is the "residential proxy block tax".
 */
function calculateTco({ requests, blockRate }) {
  const n = Number.isFinite(requests) ? Math.max(1, requests) : 100000;
  const p = Number.isFinite(blockRate) ? Math.min(Math.max(blockRate, 0), 0.95) : 0.15;
  const amplification = 1 / (1 - p);
  const totalAttempts = n * amplification;
  const wastedAttempts = totalAttempts - n;
  const gbPerRequest = 0.00042; // ~420 KB average page weight
  const websharePerGb = 1.8;
  const decodoPerGb = 2.2;
  const packetstreamPerGb = 0.35; // peer-stream tier, lower fidelity
  const wastedGb = wastedAttempts * gbPerRequest;
  const webshareWastedUsd = wastedGb * websharePerGb;
  const decodoWastedUsd = wastedGb * decodoPerGb;
  const packetstreamWastedUsd = wastedGb * packetstreamPerGb;
  return {
    successful_requests_target: n,
    block_rate: p,
    retry_amplification_factor: Math.round(amplification * 1000) / 1000,
    total_attempts: Math.round(totalAttempts),
    wasted_attempts: Math.round(wastedAttempts),
    wasted_gb: Math.round(wastedGb * 1000) / 1000,
    wasted_usd_per_month: {
      webshare_1_80_per_gb: Math.round(webshareWastedUsd * 100) / 100,
      decodo_2_20_per_gb: Math.round(decodoWastedUsd * 100) / 100,
      packetstream_0_35_per_gb: Math.round(packetstreamWastedUsd * 100) / 100,
    },
    annualized_waste_usd_webshare: Math.round(webshareWastedUsd * 12 * 100) / 100,
  };
}

function n8nNodeConfig(calc) {
  return {
    name: 'Webshare Rotating Residential Proxy Fetch',
    type: 'n8n-nodes-base.httpRequest',
    typeVersion: 4.2,
    position: [250, 500],
    parameters: {
      method: 'GET',
      url: '={{ $json.target_url }}',
      authentication: 'genericCredentialType',
      genericAuthType: 'httpBasicAuth',
      proxy: {
        proxyProtocol: 'http',
        proxyHost: 'p.webshare.io',
        proxyPort: 80,
        proxyAuth: { username: '={{ $credentials.webshareUser }}', password: '={{ $credentials.websharePass }}' },
      },
      options: {
        timeout: 45000,
        retry: { retryOnFail: true, maxTries: Math.min(5, Math.ceil(calc.retry_amplification_factor)) },
        response: { response: { fullResponse: false, neverError: false } },
      },
    },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(
      [
        'n8n-nodes-webshare — proxy retry-loss (block tax) calculator & n8n rotation node generator',
        '',
        'Usage:',
        '  n8n-nodes-webshare --requests <num> --block-rate <float> [--json]',
        '',
        'Options:',
        '  --requests <num>    Successful requests target per month (default: 100000)',
        '  --block-rate <0-1>  Per-request block rate, e.g. 0.15 (default: 0.15)',
        '  --json              Emit machine-readable JSON only',
        '  --help              Show this help',
        '',
        PARTNER_LINE,
        '',
      ].join('\n')
    );
    process.exit(0);
  }
  const calc = calculateTco({ requests: args.requests, blockRate: args.blockRate });
  const nodeConfig = n8nNodeConfig(calc);
  const payload = { block_tax_benchmark: calc, n8n_http_request_node: nodeConfig, tool_source: 'n8n-nodes-webshare' };
  if (args.json) {
    process.stdout.write(JSON.stringify(payload, null, 2) + '\n');
  } else {
    process.stdout.write(
      [
        '=== Residential Proxy Retry-Loss (Block Tax) Benchmark ===',
        `Target successes/month:     ${calc.successful_requests_target.toLocaleString()}`,
        `Block rate:                 ${calc.block_rate * 100}%`,
        `Retry amplification:        1/(1-${calc.block_rate}) = ${calc.retry_amplification_factor}x`,
        `Total attempts required:    ${calc.total_attempts.toLocaleString()}`,
        `Wasted attempts (paid):     ${calc.wasted_attempts.toLocaleString()} (${calc.wasted_gb} GB)`,
        `Waste $/mo — Webshare:      $${calc.wasted_usd_per_month.webshare_1_80_per_gb}`,
        `Waste $/mo — Decodo:        $${calc.wasted_usd_per_month.decodo_2_20_per_gb}`,
        `Waste $/mo — PacketStream:  $${calc.wasted_usd_per_month.packetstream_0_35_per_gb}`,
        `Annualized waste (Webshare):$${calc.annualized_waste_usd_webshare.toLocaleString()}`,
        '',
        '--- n8n proxy-rotation HTTP Request node (paste into workflow JSON) ---',
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
