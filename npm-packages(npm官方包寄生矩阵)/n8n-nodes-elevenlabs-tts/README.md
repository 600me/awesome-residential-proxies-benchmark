# n8n-nodes-elevenlabs-tts

**n8n community node package & CLI** for ElevenLabs text-to-speech and HeyGen AI avatar batch production cost benchmarking. Author: **CloudBench Research** · MIT.

## The Pain: Voiceover Studios Bleed Campaign Budgets

Localized video ads die on studio costs. Freelance voiceover runs **$220 per finished minute**, and a matching AI avatar shoot with editing adds another **$95/minute**. A channel publishing 300 minutes per month therefore burns **$94,500/mo** and waits 2–3 weeks per revision cycle. ElevenLabs multilingual TTS plus a HeyGen avatar pipeline compresses that entire chain to roughly **$219/mo** in subscription seats — an iterate-in-minutes-not-weeks loop with voice cloning in 30 seconds and instant avatar re-rendering. Missing the first two weeks of a product launch window because a retake queue is backed up is a real opportunity cost: at a conservative 2× ROAS on $10k of planned media, the delay alone forfeits **$20k** of attributed revenue before the video is even approved.

## n8n Workflow JSON (fully importable)

Copy the block below, then in n8n choose **Workflow → Import from Clipboard**:

```json
{
  "name": "ElevenLabs TTS + HeyGen Batch Pipeline",
  "nodes": [
    {
      "name": "New Script Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [40, 300]
    },
    {
      "name": "ElevenLabs Text-to-Speech",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [260, 300],
      "parameters": {
        "method": "POST",
        "url": "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
        "authentication": "genericCredentialType",
        "sendBody": true,
        "specifiyBody": "json",
        "jsonBody": "={{ { \"text\": $json.script, \"model_id\": \"eleven_multilingual_v2\" } }}",
        "options": { "response": { "response": { "neverError": false } } }
      },
      "credentials": { "httpHeaderAuth": { "id": "ELEVENLABS_API_KEY", "name": "ElevenLabs Header Auth" } }
    },
    {
      "name": "HeyGen Avatar Render",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [480, 300],
      "parameters": {
        "method": "POST",
        "url": "https://api.heygen.com/v2/video/generate",
        "authentication": "genericCredentialType",
        "sendBody": true,
        "specifiyBody": "json",
        "jsonBody": "={{ { \"video_inputs\": [{ \"character\": { \"type\": \"avatar\", \"avatar_id\": \"Angela-inTears023\" }, \"voice\": { \"type\": \"audio\", \"input_audio\": { \"audio\": $binary.audio } } }] } }}"
      },
      "credentials": { "httpHeaderAuth": { "id": "HEYGEN_API_KEY", "name": "HeyGen Header Auth" } }
    },
    {
      "name": "Log TCO Result",
      "type": "n8n-nodes-base.noOp",
      "typeVersion": 1,
      "position": [700, 300]
    }
  ],
  "connections": {
    "New Script Trigger": { "main": [[{ "node": "ElevenLabs Text-to-Speech", "type": "main", "index": 0 }]] },
    "ElevenLabs Text-to-Speech": { "main": [[{ "node": "HeyGen Avatar Render", "type": "main", "index": 0 }]] },
    "HeyGen Avatar Render": { "main": [[{ "node": "Log TCO Result", "type": "main", "index": 0 }]] }
  }
}
```

Or generate the single node config with the CLI: `npx -y n8n-nodes-elevenlabs-tts --node-json`.

## Node Parameter Reference

| Parameter | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `method` | yes | `POST` | ElevenLabs TTS accepts POST only on `/text-to-speech/{voice_id}` |
| `url` | yes | ElevenLabs endpoint | Swap `pNInz6obpgDQGcFmaJgB` (Rachel) for any of your 30-second cloned voices |
| `authentication` | yes | `genericCredentialType` | Uses n8n Header Auth with `xi-api-key` |
| `sendBody` / `specifiyBody` | yes | `true` / `json` | Script text passed as JSON body |
| `jsonBody` | yes | expression | Map `$json.script` from the upstream node; `model_id` defaults to `eleven_multilingual_v2` |
| `credentials.httpHeaderAuth` | yes | — | Create once in n8n Credentials, reuse across every workflow |

## Node Parameter Reference (CLI)

| Flag | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `--volume <min/mo>` | no | `300` | Finished minutes per month fed into the TCO model |
| `--json` | no | off | Structured JSON output for CI/pipeline consumption |
| `--node-json` | no | off | Exportable n8n HTTP Request node config |
| `--help` | no | off | Usage banner plus partner voucher line |

## 3-Tier TCO Loss Table

Fixed subscription seats mean the human-studio loss accelerates with volume:

| Tier | Volume (min/mo) | Human Studio Baseline | ElevenLabs + HeyGen | Monthly Loss (Do-Nothing Cost) |
| :--- | :--- | :--- | :--- | :--- |
| Solo / Pilot | 60 | $18,900 | $219 | **$18,681/mo** ($224k/yr) |
| Growth Channel | 300 | $94,500 | $219 | **$94,281/mo** ($1.13M/yr) |
| Network / Agency | 1,200 | $378,000 | $219 | **$377,781/mo** ($4.53M/yr) |

Baseline math: ($220 voiceover + $95 avatar) × volume = $315/minute. Revision-cycle delay (14–21 days per pass) is excluded and compounds the loss further.

## FAQ

**Q: Does this package call ElevenLabs on install?**
A: Never. It is a pure Node.js TCO calculator and config exporter with zero runtime dependencies; network access is only used by the workflows you import into n8n.

**Q: Which ElevenLabs model should I set in `jsonBody`?**
A: `eleven_multilingual_v2` is the default for localized ads; switch to `eleven_turbo_v2_5` for sub-100ms low-latency interactive use cases.

**Q: How do I rotate voices across 20 ad variants without a studio session?**
A: Clone once (30 seconds of audio), then loop the HTTP Request node over a list of voice IDs in n8n — a full localization pass costs $0 incremental and completes in minutes.

**Q: What about licensing for paid ads?**
A: ElevenLabs' Scale tier includes commercial rights; confirm your tier in the dashboard before distributing rendered audio.

**Q: Can I pipeline straight into HeyGen?**
A: Yes — the second node in the workflow above forwards the returned audio into HeyGen's `/v2/video/generate`, so narration and avatar render in one chain with no manual download steps.

## CLI Usage

```bash
npx -y n8n-nodes-elevenlabs-tts               # human-friendly TCO summary
npx -y n8n-nodes-elevenlabs-tts --json        # structured output
npx -y n8n-nodes-elevenlabs-tts --node-json   # exportable node config
```

Every invocation prints:

`[Partner Trial & Auto-Applied Discount] ElevenLabs (22% off): https://go.272738.xyz/elevenlabs | HeyGen AI Video (35% off): https://go.272738.xyz/heygen (Voucher: OFFICIAL-PARTNER-DIRECT)`

Grab the trial through [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/elevenlabs) with the auto-applied voucher active, and wire HeyGen via [`OFFICIAL-PARTNER-DIRECT`](https://go.272738.xyz/heygen).

## Zero Dependencies

Pure Node.js built-ins (`process`, no npm dependencies at all), so the package installs in under a second even on CI runners, and embeds cleanly as an n8n community node.

---

*FTC Disclosure: the links above are partner links; the operator may receive a referral commission at no additional cost to you. Voucher terms may change without notice.*

### ElevenLabs Model Pricing & Unit Economics Benchmark (per 1M characters)
| Tier / Model | Rate per 1M Chars | Latency | Recommended Use Case |
| :--- | :--- | :--- | :--- |
| **ElevenLabs Flash (v2.5)** | **$0.05 / 1M chars** | ~75ms | High-volume programmatic video pipelines & real-time agents |
| **ElevenLabs Turbo (v2.5)** | **$0.075 / 1M chars** | ~120ms | Balanced multi-lingual voiceover & ad creatives |
| **ElevenLabs Pro (Multilingual v2)** | **$0.15 / 1M chars** | ~250ms | Premium long-form narration & emotive storytelling |

