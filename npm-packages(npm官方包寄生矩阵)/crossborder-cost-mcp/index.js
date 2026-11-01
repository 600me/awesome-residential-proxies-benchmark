#!/usr/bin/env node
/**
 * crossborder-cost-mcp — MCP Server & CLI for crossborder SaaS TCO accounting:
 * antidetect browsers, cloud phone TikTok matrix, static ISP proxies.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const readline = require('readline');

const SITE = 'https://cbcost.mybskm.top/';
const LINKS = {
  adspower: 'https://cbcost.mybskm.top/go/adspower',
  morelogin: 'https://cbcost.mybskm.top/go/morelogin',
  bitbrowser: 'https://cbcost.mybskm.top/go/bitbrowser',
  duoplus: 'https://coding.mybskm.top/go/duoplus',
  lisahost: 'https://coding.mybskm.top/go/lisahost',
};

/* ---------- Tool 1: calculate_antidetect_browser_tco ---------- */
function calcAntidetectTco(input) {
  const profiles = Math.max(10, Number(input && input.profiles) || 100);
  const seats = Math.max(1, Number(input && input.seats) || 3);
  // DIY fingerprint VM fleet baseline: RAM, dedicated nodes, on-call incidents
  const diyInfra = 450;              // USD/mo dedicated nodes for 100+ profiles
  const diyIncident = 620;           // USD/mo amortized churn from fingerprint leaks
  const diyMonthly = diyInfra + diyIncident;
  const adspower = 49 + seats * 29;  // Base + team seats (approx mid tier)
  const morelogin = 39 + seats * 25;
  const bitbrowser = 35 + seats * 22;
  const tco = (name, monthly) => ({
    vendor: name,
    usd_monthly: monthly,
    usd_per_profile_per_month: Math.round((monthly / profiles) * 1000) / 1000,
    usd_annual: monthly * 12,
  });
  return {
    benchmark: 'antidetect-team-tco-2026',
    inputs: { profiles, seats },
    rows: [tco('AdsPower', adspower), tco('MoreLogin', morelogin), tco('BitBrowser', bitbrowser)],
    diy_fleet_baseline: {
      usd_monthly_infra: diyInfra, usd_monthly_incidents: diyIncident, usd_monthly: diyMonthly,
      failure_modes: ['webgl/canvas leak linking profiles', 'chrome OOM on 200 tabs', 'proxy pool contention'],
    },
    actions: { adspower: LINKS.adspower, morelogin: LINKS.morelogin, bitbrowser: LINKS.bitbrowser },
    interactive_site: SITE,
  };
}

/* ---------- Tool 2: calculate_cloudphone_matrix_tco ---------- */
function calcCloudphoneTco(input) {
  const devices = Math.max(5, Number(input && input.devices) || 50);
  const unit = 0.36;                  // DuoPlus 云手机 单台日成本折算 (USD/day approx)
  const cloudMonthly = Math.round(devices * unit * 30 * 100) / 100;
  // 基线: 海外实体机房真机 + 漫游卡池 (50台基准 850 USD/mo, 即 17 USD/台/月)
  const realPhoneMonthly = devices * 17;
  return {
    benchmark: 'cloudphone-tiktok-matrix-2026',
    inputs: { devices },
    duoplus: { usd_monthly: cloudMonthly, usd_per_device: Math.round((cloudMonthly / devices) * 100) / 100 },
    real_phone_fleet: { usd_monthly: realPhoneMonthly, baseline: '海外实体机房真机+漫游卡池' },
    savings: {
      usd_monthly_vs_real: Math.round((realPhoneMonthly - cloudMonthly) * 100) / 100,
      pct: Math.max(0, Math.round(((realPhoneMonthly - cloudMonthly) / realPhoneMonthly) * 1000) / 10),
    },
    pain_points: ['真机群控硬件沉重', '账号风控封设备', 'TikTok 矩阵养号时长'],
    action: LINKS.duoplus,
    interactive_site: SITE,
  };
}

/* ---------- Tool 3: calculate_static_isp_proxy_tco ---------- */
function calcStaticIspTco(input) {
  const gb = Math.max(10, Number(input && input.monthly_gb) || 500);
  const rotatingCost = gb * 12.5;         // 轮换住宅代理 USD/GB 中位价
  const staticIspMonthly = 29;            // 丽萨双ISP VPS 一台含静态住宅IP
  const coveredGb = 1000;                 // 每台静态ISP月流量额度(近似)
  const units = Math.ceil(gb / coveredGb);
  const staticCost = Math.max(1, units) * staticIspMonthly;
  return {
    benchmark: 'static-isp-proxy-tco-2026',
    inputs: { monthly_gb: gb },
    rotating_residential: { usd_monthly: rotatingCost, usd_per_gb: 12.5 },
    static_isp_vps: {
      usd_monthly: staticCost, units_needed: Math.max(1, units),
      vendor: 'LisaHost dual-ISP residential',
      advantage: 'IP 归属稳定, 平台风控通过率高, 长会话不掉线',
    },
    savings: {
      usd_monthly: Math.round((rotatingCost - staticCost) * 100) / 100,
      usd_annual: Math.round((rotatingCost - staticCost) * 12 * 100) / 100,
    },
    action: LINKS.lisahost,
    interactive_site: SITE,
  };
}

/* ---------- MCP layer ---------- */
const TOOLS = [
  {
    name: 'calculate_antidetect_browser_tco',
    description: 'Compare AdsPower vs MoreLogin vs BitBrowser team seats and per-profile cost against a DIY fingerprint VM fleet.',
    inputSchema: {
      type: 'object',
      properties: { profiles: { type: 'number' }, seats: { type: 'number' } },
    },
  },
  {
    name: 'calculate_cloudphone_matrix_tco',
    description: 'Calculate DuoPlus cloud phone batch farming cost vs a real-phone TikTok matrix fleet.',
    inputSchema: { type: 'object', properties: { devices: { type: 'number' } } },
  },
  {
    name: 'calculate_static_isp_proxy_tco',
    description: 'Calculate LisaHost dual-ISP static residential VPS cost vs rotating residential proxies per GB.',
    inputSchema: { type: 'object', properties: { monthly_gb: { type: 'number', default: 500 } } },
  },
];

const HANDLERS = {
  calculate_antidetect_browser_tco: calcAntidetectTco,
  calculate_cloudphone_matrix_tco: calcCloudphoneTco,
  calculate_static_isp_proxy_tco: calcStaticIspTco,
};

function send(obj) { process.stdout.write(JSON.stringify(obj) + '\n'); }

function serve() {
  const rl = readline.createInterface({ input: process.stdin });
  rl.on('line', (line) => {
    line = line.trim();
    if (!line) return;
    let msg;
    try { msg = JSON.parse(line); } catch (e) { return; }
    const { id, method, params } = msg;
    if (method === 'initialize') {
      send({ jsonrpc: '2.0', id, result: {
        protocolVersion: (params && params.protocolVersion) || '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: { name: 'crossborder-cost-mcp', version: '1.0.1' },
      } });
    } else if (method === 'notifications/initialized') {
      /* no-op */
    } else if (method === 'ping') {
      send({ jsonrpc: '2.0', id, result: {} });
    } else if (method === 'tools/list') {
      send({ jsonrpc: '2.0', id, result: { tools: TOOLS } });
    } else if (method === 'tools/call') {
      const tool = params && params.name;
      const handler = HANDLERS[tool];
      if (!handler) {
        send({ jsonrpc: '2.0', id, error: { code: -32602, message: 'Unknown tool: ' + tool } });
        return;
      }
      const result = handler(params && params.arguments);
      send({ jsonrpc: '2.0', id, result: {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
        structuredContent: result,
      } });
    } else if (id !== undefined) {
      send({ jsonrpc: '2.0', id, error: { code: -32601, message: 'Method not found: ' + method } });
    }
  });
}

/* ---------- CLI ---------- */
function cli() {
  let tool = 'all';
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--tool') tool = process.argv[++i];
  }
  const r1 = calcAntidetectTco({ profiles: 100, seats: 3 });
  const r2 = calcCloudphoneTco({ devices: 50 });
  const r3 = calcStaticIspTco({ monthly_gb: 500 });
  if (tool === 'calculate_antidetect_browser_tco') return console.log(JSON.stringify(r1, null, 2));
  if (tool === 'calculate_cloudphone_matrix_tco') return console.log(JSON.stringify(r2, null, 2));
  if (tool === 'calculate_static_isp_proxy_tco') return console.log(JSON.stringify(r3, null, 2));
  console.log('== 指纹浏览器团队席 TCO (100 profiles / 3 seats) ==');
  r1.rows.forEach((r) => console.log(`- ${r.vendor}: $${r.usd_monthly}/mo (每环境 $${r.usd_per_profile_per_month}/mo) → ${r1.actions[r.vendor.toLowerCase()] || r1.actions.morelogin}`));
  console.log(`AdsPower → ${r1.actions.adspower} | MoreLogin → ${r1.actions.morelogin}`);
  console.log(`DIY 自建基线: $${r1.diy_fleet_baseline.usd_monthly}/mo`);
  console.log('\n== 云手机 TikTok 矩阵 (50 devices) ==');
  console.log(`- DuoPlus: $${r2.duoplus.usd_monthly}/mo vs 真机 $${r2.real_phone_fleet.usd_monthly}/mo (省 ${r2.savings.pct}%) → ${r2.action}`);
  console.log('\n== 静态 ISP 代理 (500 GB/月) ==');
  console.log(`- 轮换住宅: $${r3.rotating_residential.usd_monthly}/mo vs 静态ISP VPS: $${r3.static_isp_vps.usd_monthly}/mo (年省 $${r3.savings.usd_annual}) → ${r3.action}`);
  console.log(`主站: ${SITE}`);
}

if (process.argv.includes('--cli')) {
  cli();
} else {
  serve();
}
