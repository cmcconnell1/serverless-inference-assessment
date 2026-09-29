# DeepInfra public catalog analysis

Source: unauthenticated GET https://api.deepinfra.com/models/list and
GET https://api.deepinfra.com/v1/openai/models, captured by the probe script.

Entries: 385 total in models/list, 231 active, 187 in the OpenAI-style models endpoint.

## Active models by type

| Type | Active |
| --- | --- |
| text-generation | 102 |
| text-to-image | 47 |
| embeddings | 28 |
| text-to-video | 24 |
| text-to-speech | 15 |
| automatic-speech-recognition | 8 |
| reranker | 4 |
| zero-shot-image-classification | 2 |
| text-to-music | 1 |

## Text generation: 102 active, 123 deprecated

### Declared quantization (active text generation)

| Quantization | Models |
| --- | --- |
| fp8 | 42 |
| None | 31 |
| fp4 | 17 |
| bfloat16 | 10 |
| fp16 | 2 |

### Partner (proxied third-party) models: 26 of 102 active text models

ByteDance/Seed-1.8, ByteDance/Seed-2.0-code, ByteDance/Seed-2.0-mini, ByteDance/Seed-2.0-pro, MiniMaxAI/MiniMax-M2.7-Turbo, Qwen/Qwen3-Max, Qwen/Qwen3-Max-Thinking, Qwen/Qwen3.7-Max, Qwen/Qwen3.8-Flash, Qwen/Qwen3.8-Max, anthropic/claude-fable-5, anthropic/claude-haiku-4-5, anthropic/claude-opus-4-7, anthropic/claude-opus-4-8, anthropic/claude-opus-5, anthropic/claude-opus-5-5, anthropic/claude-sonnet-4-6, anthropic/claude-sonnet-5, google/gemini-2.5-flash, google/gemini-2.5-pro, google/gemini-3.1-flash-lite, google/gemini-3.1-pro, google/gemini-3.5-flash, google/gemini-3.7-flash, google/gemma-4-31B-it-Ultra, openai/gpt-oss-120b-Ultra

### Capability tags (active text generation)

| Tag | Models |
| --- | --- |
| openai | 102 |
| json | 99 |
| tools | 93 |
| structured-output | 92 |
| cc-native | 75 |
| reasoning | 67 |
| flex | 59 |
| multimodal | 50 |
| non-reasoning | 37 |
| priority | 37 |
| no-free-anon | 27 |
| ocr | 23 |
| featured | 22 |
| can-disable-reasoning | 20 |
| input-video | 15 |
| input-audio | 11 |
| b200 | 5 |
| disable-penalty | 4 |
| batch | 1 |

### Pricing fields present (active text generation)

| Field | Models |
| --- | --- |
| cents_per_input_token | 102 |
| cents_per_output_token | 102 |
| type | 102 |
| rate_per_service_tier_flex | 59 |
| rate_per_input_token_cached | 51 |
| rate_per_service_tier_priority | 37 |
| discount | 7 |
| full | 7 |
| explicit_cache_granularity_tokens | 4 |
| rate_per_explicit_cache_write_token | 4 |
| short | 3 |

### Cached-input read multiplier (x input price): 51 of 102 active text models

Minimum 0.0084, median 0.2000, maximum 0.7000.

| Multiplier | Models |
| --- | --- |
| 0.0084 | 1 |
| 0.02 | 1 |
| 0.03 | 1 |
| 0.0318 | 1 |
| 0.05 | 1 |
| 0.0504 | 1 |
| 0.0769 | 2 |
| 0.1 | 2 |
| 0.1248 | 2 |
| 0.1333 | 1 |
| 0.1684 | 1 |
| 0.1842 | 1 |
| 0.1867 | 1 |
| 0.2 | 17 |
| 0.2222 | 2 |
| 0.25 | 5 |
| 0.2538 | 1 |
| 0.3333 | 1 |
| 0.3571 | 1 |
| 0.4889 | 1 |
| 0.5 | 3 |
| 0.52 | 1 |
| 0.55 | 1 |
| 0.5556 | 1 |
| 0.7 | 1 |

### Service tier multipliers (priority, flex)

| Priority x | Flex x | Models |
| --- | --- | --- |
| None | None | 43 |
| 1.5 | 0.8 | 37 |
| None | 0.8 | 22 |

### Newest 30 active text generation models by create_ts

| Added | Model | Quantization | Partner | Context | In $/M | Out $/M | Cached read x |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-09-25 | tencent/Hy4-preview | fp8 | False | 1048576 | 0.834 | 2.501 | 0.05035971 |
| 2026-09-23 | anthropic/claude-opus-5-5 | None | True | 1000000 | 4.000 | 20.000 | 0.05 |
| 2026-09-22 | XiaomiMiMo/MiMo-V2.6-Pro | fp8 | False | 1048576 | 0.430 | 0.870 | 0.00837209 |
| 2026-09-22 | XiaomiMiMo/MiMo-V2.6-Flash | fp8 | False | 1048576 | 0.140 | 0.280 | 0.02 |
| 2026-09-14 | Qwen/Qwen3.8-Flash | None | True | 1000000 | 0.113 | 0.382 | 0.12477876 |
| 2026-09-10 | deepseek-ai/DeepSeek-V4.1-Flash | fp8 | False | 1048576 | 0.200 | 0.600 | 0.03 |
| 2026-09-08 | inclusionAI/Ling-3.0-flash-VL | fp16 | False | 131072 | 0.060 | 0.180 | 0.2 |
| 2026-09-03 | inclusionAI/Ling-3.0-flash-Fin | fp4 | False | 262144 | 0.060 | 0.180 | 0.2 |
| 2026-09-03 | deepseek-ai/DeepSeek-V4-Flash-Vision-Exp | fp8 | False | 1048576 | 0.440 | 1.320 | 0.03181818 |
| 2026-08-28 | zai-org/GLM-5.3 | fp4 | False | 1048576 | 0.900 | 4.000 | 0.22222222 |
| 2026-08-26 | zai-org/GLM-5.3-Flash | fp4 | False | 1048576 | 0.150 | 0.500 | 0.2 |
| 2026-08-24 | ibm-granite/granite-4.2-30b | None | False | 131072 | 0.160 | 0.650 | 0.25 |
| 2026-08-24 | ibm-granite/granite-4.2-8b | None | False | 131072 | 0.060 | 0.250 | 0.25 |
| 2026-08-24 | ibm-granite/granite-4.2-3b | None | False | 131072 | 0.030 | 0.120 | 0.25 |
| 2026-08-17 | Qwen/Qwen3.8-27B | None | False | 262144 | 0.200 | 2.500 | 0.25 |
| 2026-08-14 | deepseek-ai/DeepSeek-V4-Pro-0813 | fp8 | False | 1048576 | 1.300 | 2.600 | 0.07692308 |
| 2026-08-14 | google/gemini-3.7-flash | None | True | 1000000 | 0.750 | 3.750 | None |
| 2026-08-12 | Qwen/Qwen3.8-2.4T-A95B | fp4 | False | 262144 | 2.000 | 6.000 | 0.1 |
| 2026-08-10 | meta-models/Muse-Glimmer-30B | None | False | 131072 | 0.300 | 1.200 | 0.13333333 |
| 2026-08-04 | inclusionAI/Ling-3.0-flash | None | False | 131072 | 0.060 | 0.180 | 0.2 |
| 2026-08-03 | nvidia/NVIDIA-Nemotron-3.5-Lightning | None | False | 262144 | 0.060 | 0.160 | 0.5 |
| 2026-08-03 | Qwen/Qwen3.8-Max | None | True | 256000 | 1.650 | 4.951 | 0.12484848 |
| 2026-07-31 | deepseek-ai/DeepSeek-V4-Flash-0731 | fp8 | False | 1048576 | 0.060 | 0.180 | 0.25 |
| 2026-07-31 | thinkingmachines/Inkling-Small | fp8 | False | 524288 | 0.450 | 1.200 | 0.22222222 |
| 2026-07-27 | moonshotai/Kimi-K3 | None | False | 1048576 | 2.850 | 14.250 | 0.1 |
| 2026-07-27 | openai/gpt-oss-120b-Ultra | fp8 | True | 131072 | 0.200 | 0.950 | None |
| 2026-07-27 | google/gemma-4-31B-it-Ultra | fp8 | True | 131072 | 0.270 | 0.760 | None |
| 2026-07-27 | anthropic/claude-opus-5 | None | True | 1000000 | 5.000 | 25.000 | None |
| 2026-07-21 | thinkingmachines/Inkling | fp8 | False | 524288 | 0.950 | 4.050 | 0.16842105 |
| 2026-07-07 | tencent/Hy3 | fp4 | False | 262144 | 0.130 | 0.530 | 0.25384615 |

### Flagship open-weight families (active text generation)

| Family | Count | Models |
| --- | --- | --- |
| DeepSeek | 10 | deepseek-ai/DeepSeek-R1-0528, deepseek-ai/DeepSeek-V3, deepseek-ai/DeepSeek-V3.1, deepseek-ai/DeepSeek-V3.2, deepseek-ai/DeepSeek-V4-Flash, deepseek-ai/DeepSeek-V4-Flash-0731, deepseek-ai/DeepSeek-V4-Flash-Vision-Exp, deepseek-ai/DeepSeek-V4-Pro, deepseek-ai/DeepSeek-V4-Pro-0813, deepseek-ai/DeepSeek-V4.1-Flash |
| Llama | 7 | NousResearch/Hermes-3-Llama-3.1-405B, NousResearch/Hermes-3-Llama-3.1-70B, meta-llama/Llama-3.3-70B-Instruct-Turbo, meta-llama/Llama-4-Scout-17B-16E-Instruct, meta-llama/Llama-Guard-4-12B, meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo, meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo |
| Qwen3 | 21 | Qwen/Qwen3-14B, Qwen/Qwen3-235B-A22B-Instruct-2507, Qwen/Qwen3-30B-A3B, Qwen/Qwen3-32B, Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo, Qwen/Qwen3-Max, Qwen/Qwen3-Max-Thinking, Qwen/Qwen3-Next-80B-A3B-Instruct, Qwen/Qwen3-VL-235B-A22B-Instruct, Qwen/Qwen3-VL-30B-A3B-Instruct, Qwen/Qwen3.5-27B, Qwen/Qwen3.5-35B-A3B, Qwen/Qwen3.5-397B-A17B, Qwen/Qwen3.5-9B, Qwen/Qwen3.6-27B, Qwen/Qwen3.6-35B-A3B, Qwen/Qwen3.7-Max, Qwen/Qwen3.8-2.4T-A95B, Qwen/Qwen3.8-27B, Qwen/Qwen3.8-Flash, Qwen/Qwen3.8-Max |
| gpt-oss | 4 | openai/gpt-oss-120b, openai/gpt-oss-120b-Turbo, openai/gpt-oss-120b-Ultra, openai/gpt-oss-20b |
| Kimi | 2 | moonshotai/Kimi-K2.6, moonshotai/Kimi-K3 |
| GLM | 5 | zai-org/GLM-4.6, zai-org/GLM-4.7, zai-org/GLM-5.2, zai-org/GLM-5.3, zai-org/GLM-5.3-Flash |
| gemma | 7 | google/gemma-3-12b-it, google/gemma-3-27b-it, google/gemma-3-4b-it, google/gemma-4-26B-A4B-it, google/gemma-4-31B-it, google/gemma-4-31B-it-Ultra, google/gemma-4-31B-it-turbo |
| Nemotron | 5 | nvidia/NVIDIA-Nemotron-3-Super-120B-A12B, nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B, nvidia/NVIDIA-Nemotron-3.5-Lightning, nvidia/Nemotron-3-Nano-30B-A3B, nvidia/Nemotron-Content-Safety-3.5 |
| Mistral | 3 | mistralai/Mistral-Nemo-Instruct-2407, mistralai/Mistral-Small-24B-Instruct-2501, mistralai/Mistral-Small-3.2-24B-Instruct-2506 |
| MiniMax | 2 | MiniMaxAI/MiniMax-M2.7-Turbo, MiniMaxAI/MiniMax-M3 |
| granite | 3 | ibm-granite/granite-4.2-30b, ibm-granite/granite-4.2-3b, ibm-granite/granite-4.2-8b |

Models tagged b200: deepseek-ai/DeepSeek-R1-0528, deepseek-ai/DeepSeek-V3, meta-llama/Llama-3.3-70B-Instruct-Turbo, meta-llama/Llama-4-Scout-17B-16E-Instruct, meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo

