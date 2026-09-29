# 2. Technical Architecture & Engine Mechanics

## 2.1 Model comparison and availability

| Measure | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Serverless catalog | 11 Model API slugs (DeepSeek V4, GLM 5.x, Kimi K3, Nemotron 3 Ultra, gpt-oss-120b); Llama and Qwen only in the deployable library | 102 active text models, 385 entries across all modalities; 26 partner-proxied models, mostly closed (Claude, Gemini, Qwen Max, Seed) | About 25 text models after 21 SKUs were removed in three months; 43 dedicated templates |
| Latest models | Day-0: DeepSeek V4 Pro 0813 (2026-08-13), Kimi K3 (2026-07-27), GLM-5.3 | Hy4-preview (2026-09-25), MiMo V2.6 (2026-09-22), DeepSeek V4.1 Flash (2026-09-10) | Day-one: Kimi K3, GLM-5.2, MiniMax M3, Nemotron 3 Ultra |
| Deprecation | Six Model APIs retired with 12 days notice | At least one week notice; requests silently forwarded to a replacement model | No automatic reroute |
| Precision disclosure | User-selected per deployment | Per model; 31 of 102 active text models undeclared | Per template flavor, plus tokens/s per flavor |
| How models are marketed | Day-0 launch speed and named logos; "Fast" SKUs at 1.5x price | Price and breadth; Priority and Flex badges | Curated frontier models on owned capacity |
| Customer use cases named | Code completion (Cursor, Zed), clinical documentation (Abridge), voice and TTS (Speechify) | Agent platforms, OpenRouter supply, long-horizon coding | Coding agents, AI search, fraud and risk (Revolut), digital health (Sword Health) |

All three carry the current frontier open-weight families (DeepSeek V4, Kimi K3, GLM 5.x) and
announce day-0 or day-one launches. They differ in breadth (DeepInfra) and in catalog
stability (Nebius removed 21 SKUs; DeepInfra redirects silently).

## 2.2 Execution engines and runtimes

| | Baseten | DeepInfra | Nebius |
| --- | --- | --- | --- |
| Engines in production | TensorRT-LLM (Engine Builder), vLLM and SGLang (BIS-LLM), NVIDIA Dynamo; custom containers | vLLM for most of the catalog, SGLang, TensorRT-LLM, Dynamo | vLLM; TensorRT-LLM in a proof of concept; LMCache for long context |
| Proprietary layer | Custom C++ gRPC server replacing Triton; BEI embeddings | Maintained forks of vLLM, TensorRT-LLM, SGLang, Dynamo | Cache-aware router; EAGLE-3 speculator training |
| Batching exposed to the developer | Engine knobs on dedicated: `max_batch_size` (default 256), `max_num_tokens`, scheduler policy, chunked prefill | None on serverless; sold as tiers: Flex 0.8x (bounded wait), Priority 1.5x, `fail_fast` | None on serverless; "Fast" flavor means smaller batches and more compute |

All three serve on engines built on continuous (in-flight) batching; none uses static batching
on shared tiers. The operating point between throughput and
per-request speed is the product decision. Baseten exposes it as configuration, DeepInfra and
Nebius sell it as a price tier. TGI, named in the brief, is no longer live: Hugging Face archived
it on 2026-03-21, and none of the three uses it for managed serving. Full detail and lineage diagram:
[full report 2.2](../docs/02-technical-architecture-and-engine-mechanics.md#22-execution-engines-and-runtimes).

## 2.3 Memory and KV cache management

| Technique | Baseten | DeepInfra | Nebius |
| --- | --- | --- | --- |
| Paged KV cache (PagedAttention) | Documented, with configuration keys and host offload | Implied by its vLLM and TensorRT-LLM forks | Implied by vLLM |
| Prefix caching | Documented; Model APIs bill cached input at about 10% of input; `x-session-affinity` keeps a session on one replica | Documented and priced: cache reads on 51 of 102 models, explicit TTL of 5 minutes or 1 hour | No cached-input price; `cached_tokens` returned; feature request "In Review" |
| KV-aware routing | Dynamo router, Enterprise plan only | Dynamo (engineering blog) | Custom cache-aware router: 95% cache hit versus 62% under Kubernetes ClusterIP |
| Speculative decoding | Eagle, MTP, NGram by configuration | Not documented | Used by the Fast flavor; zero data retention disables it |
| Quantization | FP8; FP4 on B200 | FP4 "all-in"; served context can drop | FP8 default; FP4 and INT4 for some models |

DeepInfra has turned the KV cache into a priced, programmable resource. Nebius couples a privacy
setting to a performance feature, so regulated buyers choose between residency and speed.

## 2.4 Routing and multi-region topology

| Provider | Ingress (probe captures) | Region control | TTFB p50, US vantage |
| --- | --- | --- | --- |
| Baseten | Google global front end, then a hop to a GPU in one of 18 clouds | `us` or `eu` pinning | 106 ms |
| DeepInfra | 14 addresses in one /24 on its own network (AS16581), US | None; eight US sites plus Toronto | 112 ms |
| Nebius | One NL-registered address on its own network (AS214415) | Serverless "no region guarantee"; dedicated region by contract | 465 ms |
| Akamai Cloud (baseline) | `api.linode.com` on the Akamai edge | 33 core regions; RTX PRO 6000 in 20 | 164 ms |

TTFB is a minimal unauthenticated request to an unknown route: a floor under TTFT, not a TTFT
measurement. None of the three places GPUs by user geography. Nebius pays a transatlantic round
trip from the US; DeepInfra pays the reverse for European and Asian users. Akamai trails Google's
front end by 58 ms: 25 ms in connection setup, the rest after TLS, consistent with the
edge-to-origin hop. The edge advantage therefore exists only if the inference gateway runs at the
edge. Request-path diagram and per-phase timings:
[full report 2.4](../docs/02-technical-architecture-and-engine-mechanics.md#24-routing-and-multi-region-topology).
