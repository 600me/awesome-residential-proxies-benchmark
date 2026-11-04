#!/usr/bin/env node
/**
 * n8n-nodes-vastai — CLI & n8n vLLM/OpenAI-compatible inference node config generator.
 * Vast.ai / RunPod serverless GPU vs AWS EC2 LLM inference TCO calculator.
 * Pure Node.js built-ins only. Author: CloudBench Research (MIT).
 */
'use strict';

const PARTNER_LINE =
  '[Partner Trial & Auto-Applied Discount] Activate Vast.ai at https://go.272738.xyz/vastai or RunPod Serverless GPU at https://go.272738.xyz/runpod (Voucher: OFFICIAL-PARTNER-DIRECT)';

const GPU_RATES = {
  // USD per GPU-hour, 2026 benchmark medians
  h100: { aws_p5_per_gpu_hr: 12.29 / 8, runpod_hr: 2.99, vastai_hr: 2.09, label: 'H100 80GB (per GPU)' },
  a100: { aws_p5_per_gpu_hr: 8.0, runpod_hr: 1.89, vastai_hr: 1.29, label: 'A100 80GB (per GPU)' },
  'rtx4090': { aws_p5_per_gpu_hr: null, runpod_hr: 0.69, vastai_hr: 0.49, label: 'RTX 4090 24GB' },
};
// AWS EC2 p5.48xlarge = 8×H100 at $12.29/hr total.

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') args.json = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--gpu') args.gpu = String(argv[++i]).toLowerCase().replace(/[\s_-]/g, '');
    else if (a === '--hours') args.hours = Number(argv[++i]);
    else args._.push(a);
  }
  return args;
}

function calculateTco({ gpu, hours }) {
  const key = gpu && GPU_RATES[gpu] ? gpu : 'h100';
  const h = Number.isFinite(hours) && hours > 0 ? hours : 720;
  const r = GPU_RATES[key];
  const aws = r.aws_p5_per_gpu_hr != null ? r.aws_p5_per_gpu_hr * h : null;
  const runpod = r.runpod_hr * h;
  const vastai = r.vastai_hr * h;
  const savingsRunpod = aws != null ? aws - runpod : null;
  const savingsVast = aws != null ? aws - vastai : null;
  return {
    gpu: key,
    gpu_label: r.label,
    gpu_hours_per_month: h,
    usd_per_gpu_hour: {
      aws_ec2_equivalent: r.aws_p5_per_gpu_hr,
      runpod_serverless: r.runpod_hr,
      vastai: r.vastai_hr,
    },
    monthly_usd: {
      aws_ec2: aws != null ? Math.round(aws * 100) / 100 : null,
      runpod: Math.round(runpod * 100) / 100,
      vastai: Math.round(vastai * 100) / 100,
    },
    savings_monthly_usd: {
      runpod_vs_aws: savingsRunpod != null ? Math.round(savingsRunpod * 100) / 100 : null,
      vastai_vs_aws: savingsVast != null ? Math.round(savingsVast * 100) / 100 : null,
      vastai_vs_aws_pct: savingsVast != null ? Math.round((savingsVast / aws) * 1000) / 10 : null,
    },
    annualized_savings_vastai_vs_aws: savingsVast != null ? Math.round(savingsVast * 12 * 100) / 100 : null,
  };
}

function n8nNodeConfig(calc) {
  return {
    name: 'vLLM OpenAI-Compatible Inference (Serverless GPU)',
    type: 'n8n-nodes-base.httpRequest',
    typeVersion: 4.2,
    position: [640, 300],
    parameters: {
      method: 'POST',
      url: 'https://api.runpod.ai/v2/<your-endpoint-id>/openai/v1/chat/completions',
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendHeaders: true,
      headerParameters: {
        parameters: [{ name: 'Authorization', value: 'Bearer {{ $credentials.runpodToken }}' }],
      },
      sendBody: true,
      specifyBody: 'json',
      jsonBody: JSON.stringify(
        {
          model: 'meta-llama/Llama-3.1-70B-Instruct',
          messages: [
            { role: 'system', content: 'You are a precise benchmarking assistant.' },
            { role: 'user', content: '{{ $json.prompt }}' },
          ],
          max_tokens: 1024,
          temperature: 0.2,
          gpu: calc.gpu,
        },
        null,
        2
      ),
      options: { timeout: 180000, retry: { retryOnFail: true, maxTries: 3 } },
    },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(
      [
        'n8n-nodes-vastai — serverless GPU LLM inference TCO calculator & n8n node generator',
        '',
        'Usage:',
        '  n8n-nodes-vastai --gpu <h100|a100|rtx4090> --hours <num> [--json]',
        '',
        'Options:',
        '  --gpu <model>   GPU model: h100 (default), a100, rtx4090',
        '  --hours <num>   GPU-hours per month (default: 720)',
        '  --json          Emit machine-readable JSON only',
        '  --help          Show this help',
        '',
        PARTNER_LINE,
        '',
      ].join('\n')
    );
    process.exit(0);
  }
  const calc = calculateTco({ gpu: args.gpu, hours: args.hours });
  const nodeConfig = n8nNodeConfig(calc);
  const payload = { gpu_tco_benchmark: calc, n8n_http_request_node: nodeConfig, tool_source: 'n8n-nodes-vastai' };
  if (args.json) {
    process.stdout.write(JSON.stringify(payload, null, 2) + '\n');
  } else {
    process.stdout.write(
      [
        '=== Serverless GPU LLM Inference TCO Benchmark ===',
        `GPU:                     ${calc.gpu_label}`,
        `Utilization:             ${calc.gpu_hours_per_month} GPU-hr/mo (100% dedicated)`,
        `AWS EC2 equivalent:      $${calc.monthly_usd.aws_ec2 != null ? calc.monthly_usd.aws_ec2.toLocaleString() : 'n/a (no p5 tier)'}/mo`,
        `RunPod serverless:       $${calc.monthly_usd.runpod.toLocaleString()}/mo`,
        `Vast.ai:                 $${calc.monthly_usd.vastai.toLocaleString()}/mo`,
        `Savings Vast.ai vs AWS:  $${calc.savings_monthly_usd.vastai_vs_aws != null ? calc.savings_monthly_usd.vastai_vs_aws.toLocaleString() : 'n/a'}/mo (${calc.savings_monthly_usd.vastai_vs_aws_pct != null ? calc.savings_monthly_usd.vastai_vs_aws_pct + '%' : 'n/a'}), $${calc.annualized_savings_vastai_vs_aws != null ? calc.annualized_savings_vastai_vs_aws.toLocaleString() : 'n/a'}/year`,
        '',
        '--- n8n vLLM / OpenAI-compatible inference node (paste into workflow JSON) ---',
        JSON.stringify(nodeConfig, null, 2),
        '',
        PARTNER_LINE,
        '',
      ].join('\n')
    );
  }
}

if (require.main === module) main();
module.exports = { calculateTco, n8nNodeConfig, GPU_RATES, PARTNER_LINE };
