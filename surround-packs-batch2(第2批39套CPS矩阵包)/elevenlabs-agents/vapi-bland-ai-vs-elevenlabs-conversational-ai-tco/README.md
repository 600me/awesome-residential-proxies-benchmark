# Voice Agent TCO: ElevenLabs vs Vapi.ai and Bland AI

[![Evaluate ElevenLabs](https://img.shields.io/badge/ElevenLabs-evaluate-black)](https://is.gd/Dawnj5)
[![Python 3 standard library](https://img.shields.io/badge/Python-3-standard_library-blue)](https://is.gd/Dawnj5)
[![License MIT](https://img.shields.io/badge/License-MIT-green)](https://is.gd/Dawnj5)

## 1. The engineering problem and the invoice trap

A voice-agent invoice is often split across an orchestration platform, a speech provider, a transcription provider, an LLM, and a telephone carrier. Multiplying only the orchestration headline by connected minutes can leave most of the invoice invisible. Vapi.ai's historically advertised $0.05/minute platform fee is a useful anchor, but it does not by itself price a complete call. PlayHT is a speech layer that needs surrounding infrastructure; Bland AI's historically advertised $0.09/minute bundle needs its own inclusion and routing checks.

At 30,000 connected minutes, this repository's Vapi.ai stack totals $4,470/month versus $3,870 for the ElevenLabs scenario. That is **$600/month or $7,200/year** of avoidable spend if the chosen Vapi voice component really costs $0.06 per connected minute. Ignoring Vapi's assumed voice, STT, LLM, and carrier components would underbudget $2,970/month, or $35,640/year, against a $1,500 platform-only estimate. These are reproducible scenario losses, not evidence that every Vapi customer pays those amounts.

The same model puts Bland AI at $3,120/month: **ElevenLabs costs $750/month more** in that comparison. An integrated implementation may still justify a premium through voice quality or less engineering work, but that benefit must be measured separately. This calculator does not add invented productivity savings to make a preferred provider win.

**[Evaluate ElevenLabs for your voice-agent workload](https://is.gd/Dawnj5)** after replacing the assumptions with your own contract terms.

## 2. Historical prices and comparable technical boundaries

**Pricing provenance:** prepared offline on 2026-10-30 using remembered historical public pricing anchors. No live price pages or APIs were fetched. Historical anchors are identifiable vendor prices from earlier offers, not verified current quotations; packaging, limits, model eligibility, and availability may have changed. Every other rate below is explicitly a scenario input. Do not interpret the default totals as a current vendor quote or a measured benchmark. This independent project does not claim vendor sponsorship.

| Price or technical dimension | ElevenLabs | Vapi.ai stack | PlayHT stack | Bland AI |
|---|---|---|---|---|
| Product role | Integrated conversational agent | Agent orchestration + selected providers | Speech API + assumed external stack | Bundled conversational agent |
| Historical public anchor, USD | Agent usage from about $0.10/agent min | $0.05/connected min orchestration | Creator $39/month, 250,000 characters | About $0.09/connected min bundle |
| Platform/bundle used by calculator | $0.100/connected min | $0.050/connected min | $0.050/connected min assumed orchestration | $0.090/connected min |
| Voice cost used by calculator | Inside modeled agent rate | $0.060/connected min assumption | $0.120/generated min assumption | Inside modeled bundle |
| STT used by calculator | Inside modeled agent rate | $0.010/connected min assumption | $0.010/connected min assumption | Inside modeled bundle |
| LLM used by calculator | $0.015/connected min assumption | $0.015/connected min assumption | $0.015/connected min assumption | Inside modeled bundle assumption |
| Carrier used by calculator | $0.014/connected min assumption | $0.014/connected min assumption | $0.014/connected min assumption | $0.014/connected min assumption; verify inclusion |
| Output-speech denominator | Included in scenario | Voice assumption already normalized | 45% of connected minutes | Included in scenario |
| Streaming integration boundary | Agent session + playback | Agent transport + chosen speech adapter | TTS stream + custom agent transport | Agent session + playback |
| Interruption acceptance test | Measure playback clear + late frames | Measure across selected providers | Implement cancel + stale-frame guard | Measure playback clear + late frames |
| Measured latency in this repository | None | None | None | None |
| Effective modeled USD/connected min | $0.129 | $0.149 | $0.143 | $0.104 |
| Monthly total at 30,000 minutes | $3,870 | $4,470 | $4,290 | $3,120 |
| Annual difference versus ElevenLabs | Baseline | $7,200 more | $5,040 more | $9,000 less |


The historical PlayHT Creator anchor is not used as a production API entitlement. At an illustrative 900 characters per generated minute and 45% speech share, 30,000 connected minutes imply 12,150,000 characters. A 250,000-character studio allowance cannot simply be extrapolated into an unlimited conversational deployment. The calculator instead uses a clearly assumed generated-audio rate; obtain an actual API quote before treating it as a purchasing comparison.

The relevant purchasing unit is the connected call minute. Keep generated speech minutes separate from connected minutes and token-based inference. Collect at least one representative invoice per vendor and map each line to a component before changing defaults. An ElevenLabs agent-minute anchor is not the standalone Turbo TTS API price.

A break-even check is especially useful here: the non-voice Vapi scenario is $0.089 per connected minute, while the complete ElevenLabs scenario is $0.129. Vapi's voice component therefore breaks even at $0.040 per connected minute. A cheaper voice configuration reverses the displayed savings. Run `--vapi-tts-rate 0.02` to see that reversal instead of assuming the default ranking is universal.

**[Check ElevenLabs suitability and current commercial terms](https://is.gd/Dawnj5)** before committing traffic or a budget. The gateway is the only external action destination in this repository; badges are static images, not pricing sources.

## 3. Run the cost calculator locally

Python 3.8+ and its standard library are sufficient. There are no dependencies, credentials, API calls, network requests, or required arguments. Run from this repository directory:

```sh
python3 calculate_elevenlabs_agents_tco.py
python3 calculate_elevenlabs_agents_tco.py --help
python3 calculate_elevenlabs_agents_tco.py --tier scale --vapi-tts-rate 0.04
python3 calculate_elevenlabs_agents_tco.py --minutes 30000 --vapi-tts-rate 0.02 --json
```

Parameters and units:

| Parameter | Default | Meaning |
|---|---|---|
| `--tier starter / growth / scale` | `growth` | Workload presets: 5,000 / 30,000 / 120,000 connected minutes monthly; not vendor subscription tiers |
| `--minutes NUMBER` | Tier workload | Explicit connected-minute override, including zero |
| `--json` | Off | One parseable JSON object with costs, assumptions, annual deltas, and gateway |
| `--elevenlabs-rate NUMBER` | `0.10` | Modeled agent dollars per connected minute; LLM and carrier are separate |
| `--vapi-tts-rate NUMBER` | `0.06` | Voice dollars already normalized per connected minute |
| `--playht-tts-rate NUMBER` | `0.12` | Assumed dollars per generated audio minute |
| `--speech-share NUMBER` | `0.45` | Generated speech minutes / connected minutes; range 0 through 1 |
| `--bland-rate NUMBER` | `0.09` | Modeled bundled dollars per connected minute |
| `--llm-rate NUMBER` | `0.015` | Separate LLM assumption for ElevenLabs, Vapi.ai, and PlayHT stacks |
| `--telephony-rate NUMBER` | `0.014` | Shared carrier scenario dollars per connected minute |
| `--calls NUMBER` | `0` | Chargeable calls for the optional scenario fee |
| `--per-call-fee NUMBER` | `0` | Shared scenario dollars per chargeable call |
| `--latency-ms NUMBER` | `170` | Assumed first-audio time; displayed by the latency repository only |
| `--buffer-ms NUMBER` | `40` | Assumed playback-buffer delay for the latency budget |
| `--network-ms NUMBER` | `35` | Assumed transport delay for the latency budget |
| `--demo` | Off | Include the offline interruption trace; always included in the streaming repository |

Actual default terminal output captured from this repository's local script:

```text
$ python3 calculate_elevenlabs_agents_tco.py
OFFLINE ESTIMATE | USD | historical anchors + adjustable assumptions
Tier: growth; connected minutes/month: 30,000
+------------------+------------+------------+------------+------------+------------+------------+------------+
| Provider         | Platform $ | Voice $    | STT $      | LLM $      | Carrier $  | Call fee $ | Monthly $  |
+------------------+------------+------------+------------+------------+------------+------------+------------+
| ElevenLabs       |   3,000.00 |       0.00 |       0.00 |     450.00 |     420.00 |       0.00 |   3,870.00 |
| Vapi.ai stack    |   1,500.00 |   1,800.00 |     300.00 |     450.00 |     420.00 |       0.00 |   4,470.00 |
| PlayHT stack     |   1,500.00 |   1,620.00 |     300.00 |     450.00 |     420.00 |       0.00 |   4,290.00 |
| Bland AI         |   2,700.00 |       0.00 |       0.00 |       0.00 |     420.00 |       0.00 |   3,120.00 |
+------------------+------------+------------+------------+------------+------------+------------+------------+
Annual savings with ElevenLabs (negative = ElevenLabs costs more):
  vs Vapi.ai stack: $7,200.00/year
  vs PlayHT stack: $5,040.00/year
  vs Bland AI: $-9,000.00/year
Evaluate ElevenLabs and check current terms: https://is.gd/Dawnj5
```

For each provider, monthly cost is the sum of separately rounded component costs plus the optional call fee. Annual savings with ElevenLabs equals `(competitor monthly total - ElevenLabs monthly total) * 12`. Negative savings mean ElevenLabs costs more. PlayHT voice cost is `connected minutes * speech share * generated-minute rate`. Values are rounded to cents for planning, not settlement. Annual figures assume twelve identical months and no annual discount.

The model intentionally leaves out taxes, minimum commitments, free quotas, number rental, storage, staff time, and volume discounts. It assumes all components share the same connected-minute denominator except PlayHT output speech and optional call fees. Fixed Vapi orchestration ($0.05) and external-stack STT ($0.01) assumptions are visible in the script's `rates` dictionary; edit those local inputs when contracts differ. An actual contract may include LLM or carrier charges that this scenario separates, so remove duplicate charges before using totals. A trial measures quality; this arithmetic only estimates cost.

**[Start an ElevenLabs evaluation with your own rates](https://is.gd/Dawnj5)** and use the JSON output to keep the comparison reproducible.

## 4. Migration checklist and companion repositories

- [ ] Separate platform fees from pass-through model, transcription, voice, and carrier invoices.
- [ ] Reconcile connected minutes with billed minutes, minimum commitments, and concurrency charges.
- [ ] Replace the historical agent-minute anchor with the actual ElevenLabs offer and LLM policy.
- [ ] Export prompts, tool schemas, escalation rules, consent logic, and representative recordings.
- [ ] Replay equivalent calls against both systems and record task completion, transfers, and human corrections.
- [ ] Pilot a limited traffic cohort and retain the old route until quality and unit cost meet your thresholds.

Use the other repositories for the adjacent engineering questions:

- [playht-murf-vs-elevenlabs-turbo-v2-5-latency-bench](../playht-murf-vs-elevenlabs-turbo-v2-5-latency-bench)
- [ai-call-center-per-minute-telephony-cost-calculator](../ai-call-center-per-minute-telephony-cost-calculator)
- [websocket-streaming-tts-interruption-handling-demo](../websocket-streaming-tts-interruption-handling-demo)

Acceptance for this repository is local and reproducible: default execution exits 0, prints a complete ASCII component bill, reports annual dollar deltas, and includes the gateway. `--json` emits valid JSON instead of mixing text with structured data. Zero workload produces zero usage costs; negative or nonfinite numeric inputs are rejected. Neither the latency budget nor the interruption trace makes an external performance claim.

### Open-source license

MIT License. Copyright (c) 2026 Voice Agent Comparison Contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
