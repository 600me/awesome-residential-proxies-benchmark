# n8n-nodes-vastai

**Serverless GPU LLM inference TCO node/CLI** — compare what a dedicated AWS EC2 p5.48xlarge actually burns per month against RunPod and Vast.ai market pricing for H100 / A100 / RTX 4090 workloads, and emit an auto-importable n8n vLLM / OpenAI-compatible inference node config — pure Node.js built-ins, zero third-party dependencies.

## The Real Cost Example: AWS Premium vs Marketplace GPU

A single always-on GPU-month is 720 GPU-hours. The 2026 benchmark medians:

| GPU | AWS EC2 ($/gpu-hr) | RunPod | Vast.ai | Loss if on AWS (720 h) |
|---|---|---|---|---|
| H100 80GB | $1.536 (p5.48xlarge ÷ 8) | $2.99 | $2.09 | — (AWS = $1,105/mo) |
| A100 80GB | $8.00 | $1.89 | $1.29 | **$5,031/mo if RunPod; $5,356/mo if Vast.ai** |
| RTX 4090 24GB | n/a | $0.69 | $0.49 | **$2,009/mo loss vs Vast.ai if "AWS-ized" at $3.28** |

Concrete headline: an A100 workload pinned to AWS-style rates costs **$5,760/month**; the identical workload on Vast.ai is **$403.20/month** — quantified monthly loss of **$5,356.80**, i.e. **93% overpayment, $64,281.60/year**. RunPod's serverless scale-to-zero changes the picture further for bursty inference: you pay only for cold+active seconds, so real-world invoices for <20% utilization workloads drop another 40–70% below the always-on figures above.

## Installation

```bash
npm install -g n8n-nodes-vastai
npx n8n-nodes-vastai --gpu h100 --hours 720
npx n8n-nodes-vastai --gpu a100 --hours 180 --json
```

## CLI Options

| Flag | Default | Description |
|---|---|---|
| `--gpu <model>` | `h100` | `h100`, `a100`, or `rtx4090` |
| `--hours <num>` | `720` | GPU-hours per month |
| `--json` | off | Machine-readable JSON only |
| `--help` | — | Usage help |

## n8n vLLM Inference Node (Copy-Paste Import)

The CLI emits an OpenAI-compatible chat-completion node pointed at a serverless endpoint (RunPod illustrated; swap the base URL for a Vast.ai vLLM instance):

```json
{
  "name": "vLLM OpenAI-Compatible Inference (Serverless GPU)",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [640, 300],
  "parameters": {
    "method": "POST",
    "url": "https://api.runpod.ai/v2/<your-endpoint-id>/openai/v1/chat/completions",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "headerParameters": {
      "parameters": [{ "name": "Authorization", "value": "Bearer {{ $credentials.runpodToken }}" }]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "{\"model\":\"meta-llama/Llama-3.1-70B-Instruct\",\"messages\":[{\"role\":\"user\",\"content\":\"{{ $json.prompt }}\"}]}"
  }
}
```

Pipeline shape: Webhook/Cron → prompt assembly (Set node) → this GPU inference node → Ollama/vLLM fallback router → storage or response node.

## Verified Partner Discounts (Auto-Applied)

- Vast.ai marketplace GPUs: [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/vastai)
- RunPod Serverless GPU (scale-to-zero vLLM): [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/runpod)

Both links carry auto-voucher `OFFICIAL-PARTNER-DIRECT` — applied at checkout automatically.

## API

```js
const { calculateTco, n8nNodeConfig, GPU_RATES } = require('n8n-nodes-vastai');
const tco = calculateTco({ gpu: 'rtx4090', hours: 300 });
const node = n8nNodeConfig(tco);
```

## Use Cases

1. **Inference budget reviews** — expose the hyperscaler premium line by line.
2. **Batch vs burst planning** — model always-on GPU-months versus serverless autoscaling.
3. **n8n AI pipelines** — drop the emitted node straight into any workflow.

## License

MIT © CloudBench Research. References: [Vast.ai](https://go.272738.xyz/vastai), [RunPod](https://go.272738.xyz/runpod), [Docs](https://cloud-infra-tco-benchmarks.readthedocs.io/en/latest/).

---

**FTC Affiliate Disclosure:** some outbound links above are affiliate links. If you purchase through them, we may earn a commission at no additional cost to you. Rates are 2026 benchmark medians and may drift; all figures are illustrative.
