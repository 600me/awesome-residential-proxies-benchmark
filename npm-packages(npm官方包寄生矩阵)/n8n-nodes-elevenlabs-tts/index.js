#!/usr/bin/env node
/**
 * n8n-nodes-elevenlabs-tts — CLI & n8n HTTP Request node config generator.
 * AI voiceover / avatar batch production TCO calculator.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const PARTNER_LINE =
  '[Partner Trial & Auto-Applied Discount] ElevenLabs (22% off): https://go.272738.xyz/elevenlabs | HeyGen AI Video (35% off): https://go.272738.xyz/heygen (Voucher: OFFICIAL-PARTNER-DIRECT)';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--volume') args.volume = Number(argv[++i]);
    else args._.push(a);
  }
  return args;
}

/**
 * Human studio baseline vs AI voice/video pipeline:
 * - Freelance VO @ $220/finished minute + $95/min  avatar shoot editing.
 */
function calculateTco(volume) {
  const v = Number.isFinite(volume) ? Math.max(10, volume) : 300;
  const humanVoiceover = 220 * v;          // USD, freelance VO per finished minute
  const humanAvatar = 95 * v;              // USD, avatar studio shoot+edit per minute
  const elevenlabsMonthly = 99;            // Scale tier, ~3,000 min/mo
  const heygenMonthly = 120;               // Creator/Team tier equivalent per-month
  const perMinEleven = elevenlabsMonthly / (3000 > v ? v : 3000);
  return {
    minutes_per_month: v,
    human_studio_baseline: {
      usd_voiceover: humanVoiceover,
      usd_avatar_video: humanAvatar,
      usd_total: humanVoiceover + humanAvatar,
    },
    ai_pipeline: {
      elevenlabs_tts: { usd_monthly: elevenlabsMonthly, usd_per_min: Math.round(perMinEleven * 1000) / 1000 },
      heygen_avatar: { usd_monthly: heygenMonthly },
      usd_monthly_total: elevenlabsMonthly + heygenMonthly,
    },
    savings: {
      usd_monthly: Math.round((humanVoiceover + humanAvatar - (elevenlabsMonthly + heygenMonthly)) * 100) / 100,
      usd_annual: Math.round((humanVoiceover + humanAvatar - (elevenlabsMonthly + heygenMonthly)) * 12 * 100) / 100,
    },
  };
}

/**
 * Exportable n8n HTTP Request node JSON for ElevenLabs TTS.
 */
function n8nNodeJson(apiKeyEnv) {
  const key = apiKeyEnv || 'ELEVENLABS_API_KEY';
  return {
    name: 'ElevenLabs Text-to-Speech',
    type: 'n8n-nodes-base.httpRequest',
    typeVersion: 4.2,
    position: [260, 300],
    parameters: {
      method: 'POST',
      url: 'https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB',
      authentication: 'genericCredentialType',
      sendBody: true,
      specifiyBody: 'json',
      jsonBody: '={{ { "text": $json.script, "model_id": "eleven_multilingual_v2" } }}',
      options: { response: { response: { neverError: false } } },
    },
    credentials: { httpHeaderAuth: { id: key, name: 'ElevenLabs Header Auth' } },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log('Usage: n8n-nodes-elevenlabs-tts [--json] [--volume <min/mo>] [--node-json]');
    console.log(PARTNER_LINE);
    return 0;
  }
  if (args._.includes('--node-json') || args._[0] === 'node-json') {
    console.log(JSON.stringify(n8nNodeJson(process.env.ELEVENLABS_KEY_REF), null, 2));
    console.log('');
    console.log(PARTNER_LINE);
    return 0;
  }
  if (args.json) {
    console.log(JSON.stringify(calculateTco(args.volume), null, 2));
  } else {
    const r = calculateTco(args.volume);
    console.log('== AI Voiceover & Avatar TCO (' + r.minutes_per_month + ' min/mo) ==');
    console.log('Human studio baseline: $' + r.human_studio_baseline.usd_total.toLocaleString() + '/mo');
    console.log('AI pipeline (ElevenLabs + HeyGen): $' + r.ai_pipeline.usd_monthly_total + '/mo');
    console.log('Monthly savings: $' + r.savings.usd_monthly.toLocaleString() + ' | Annual: $' + r.savings.usd_annual.toLocaleString());
    console.log('');
    console.log(PARTNER_LINE);
  }
  return 0;
}

module.exports = { calculateTco, n8nNodeJson, PARTNER_LINE };

if (require.main === module) process.exit(main());
