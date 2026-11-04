#!/usr/bin/env node
/**
 * cn-coding-plan-mcp — MCP Server & CLI for CN coding plan / AI quota /
 * overseas-subscription virtual card TCO comparison.
 * Pure Node.js built-ins only (readline, https not needed for STDIO).
 * Author: CloudBench Research (MIT).
 */
'use strict';

const readline = require('readline');

const SITE = 'https://coding.mybskm.top/';
const LINKS = {
  aliyunCoding: 'https://coding.mybskm.top/go/aliyun-coding',
  aliyunDashi: 'https://coding.mybskm.top/go/aliyun-dashi',
  volcengine: 'https://coding.mybskm.top/go/volcengine-coding',
  zhipu: 'https://coding.mybskm.top/go/zhipu-glm',
  tencent: 'https://coding.mybskm.top/go/tencent-double11',
  bwh: 'https://coding.mybskm.top/go/bwh',
  rainyun: 'https://coding.mybskm.top/go/rainyun',
  lisahost: 'https://coding.mybskm.top/go/lisahost',
};

/* ---------- Tool 1: compare_cn_coding_plans ---------- */
function compareCnCodingPlans(input) {
  const rows = [
    { vendor: 'Aliyun百炼 Coding Plan', entry: '¥49/月起', quota: 'Token 包梯度', action: LINKS.aliyunCoding },
    { vendor: '阿里云大模型推理 (Dashi)', entry: '新客代金券', quota: '按量 + 预付折扣', action: LINKS.aliyunDashi },
    { vendor: '火山方舟 Volcengine', entry: '首发抵扣券', quota: '按量 + 资源包', action: LINKS.volcengine },
    { vendor: '智谱 GLM Coding', entry: 'GLM 包月订阅', quota: '不限速 Coding', action: LINKS.zhipu },
    { vendor: '腾讯云轻量/双11', entry: '轻量服务器折扣', quota: '年度券包', action: LINKS.tencent },
  ];
  return {
    benchmark: 'cn-coding-plan-2026',
    best_for: 'Claude Code / Cursor / Trae 国内合规接入',
    rows,
    interactive_site: SITE,
    note: '优惠券与折扣以主站实时页为准，跳转含跟踪参数用于归因结算。',
  };
}

/* ---------- Tool 2: calculate_claude_cursor_card_tco ---------- */
function calcClaudeCursorCardTco(input) {
  const monthlyUsd = Math.max(1, Number(input && input.monthly_usd) || 200);
  const fxLossPct = 2.5;            // 双币卡/虚拟卡汇率+跨境损耗
  const openCardFee = 9.9;          // 一次开卡费(USD)
  const topUpFeePct = 1.0;          // 单笔充值损耗
  const cardMonthly = monthlyUsd * (1 + (fxLossPct + topUpFeePct) / 100);
  const annualCost = cardMonthly * 12 + openCardFee;
  return {
    benchmark: 'claude-cursor-card-tco-2026',
    inputs: { monthly_usd: monthlyUsd },
    card_route: {
      fx_loss_pct: fxLossPct,
      topup_loss_pct: topUpFeePct,
      open_card_fee_usd: openCardFee,
      usd_monthly_effective: Math.round(cardMonthly * 100) / 100,
      usd_annual_effective: Math.round(annualCost * 100) / 100,
      pain_points: ['风控拒付', '汇率二次损耗', '余额沉淀'],
    },
    action: LINKS.lisahost,
    action_domestic: LINKS.aliyunCoding,
    interactive_site: SITE,
    note: '海外订阅防封首选原生住宅双ISP节点（丽萨主机）；免外卡直连首选阿里云百炼 Coding Plan。',
  };
}

/* ---------- Tool 3: compare_cn2_gia_agent_vps ---------- */
function compareCn2GiaAgentVps(input) {
  const rows = [
    { vendor: 'BWH 搬瓦工 CN2 GIA', region: 'DC6/DC9', price: '$49.99/年起', best_for: '低延迟 SSH/Agent 回源', action: LINKS.bwh },
    { vendor: '雨云 Rainyun 高速节点', region: '华东出口', price: '¥/月起', best_for: '建站与中转', action: LINKS.rainyun },
    { vendor: '丽萨主机 LisaHost 双ISP', region: '住宅 IP', price: '按流量/静态', best_for: 'Agent 指纹与风控', action: LINKS.lisahost },
  ];
  return {
    benchmark: 'cn2-gia-agent-vps-2026',
    rows,
    interactive_site: SITE,
    note: 'Agent 部署建议 CN2 GIA 直连线路；住宅 IP 需求选双 ISP VPS。',
  };
}

/* ---------- MCP layer ---------- */
const TOOLS = [
  {
    name: 'compare_cn_coding_plans',
    description: 'Compare CN coding plans (Aliyun Bailian, Volcengine Ark, Zhipu GLM, Tencent Lightweight/Double-11) with coupon jump links.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
  {
    name: 'calculate_claude_cursor_card_tco',
    description: 'Calculate TCO of subscribing Claude Code / Cursor / OpenAI from CN using a virtual card (open-fee, FX & top-up loss).',
    inputSchema: {
      type: 'object',
      properties: { monthly_usd: { type: 'number', description: 'Overseas subscription monthly cost in USD' } },
    },
  },
  {
    name: 'compare_cn2_gia_agent_vps',
    description: 'Compare CN2 GIA / dual-ISP agent VPS options (BWH, LisaHost, Rainyun) with jump links.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
];

const HANDLERS = {
  compare_cn_coding_plans: compareCnCodingPlans,
  calculate_claude_cursor_card_tco: calcClaudeCursorCardTco,
  compare_cn2_gia_agent_vps: compareCn2GiaAgentVps,
};

function send(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

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
        serverInfo: { name: 'cn-coding-plan-mcp', version: '1.0.0' },
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
      let result = handler(params && params.arguments);
      send({ jsonrpc: '2.0', id, result: {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
        structuredContent: result,
      } });
    } else if (id !== undefined) {
      send({ jsonrpc: '2.0', id, error: { code: -32601, message: 'Method not found: ' + method } });
    }
  });
}

/* ---------- CLI mode ---------- */
function cli() {
  const arg = process.argv[2];
  let tool = 'all';
  let optIdx = 2;
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--tool') { tool = process.argv[++i]; optIdx = ++i; }
  }
  if (tool === 'compare_cn_coding_plans') {
    console.log(JSON.stringify(compareCnCodingPlans(), null, 2));
  } else if (tool === 'calculate_claude_cursor_card_tco') {
    const monthly = Number(process.argv[optIdx + 1]) || 200;
    console.log(JSON.stringify(calcClaudeCursorCardTco({ monthly_usd: monthly }), null, 2));
  } else if (tool === 'compare_cn2_gia_agent_vps') {
    console.log(JSON.stringify(compareCn2GiaAgentVps(), null, 2));
  } else {
    const r1 = compareCnCodingPlans();
    const r2 = calcClaudeCursorCardTco({ monthly_usd: 200 });
    const r3 = compareCn2GiaAgentVps();
    console.log('== CN Coding Plan 比价 ==');
    r1.rows.forEach((r) => console.log(`- ${r.vendor} (${r.entry}) → ${r.action}`));
    console.log(`主站: ${r1.interactive_site}`);
    console.log('\n== Claude/Cursor 虚拟卡 TCO (200 USD/月) ==');
    console.log(`- 月度实际成本: $${r2.card_route.usd_monthly_effective}/月, 年度 $${r2.card_route.usd_annual_effective} → ${r2.action}`);
    console.log('\n== CN2 GIA Agent VPS 比价 ==');
    r3.rows.forEach((r) => console.log(`- ${r.vendor} (${r.price}) → ${r.action}`));
  }
}

if (process.argv.includes('--cli')) {
  cli();
} else {
  serve();
}
