# 4. Strategic Output: PM Brief & SE Field Guide, Part B: Solutions Engineering Battlecard

For technical prospect conversations. Facts dated 2026-09-28, probe captures 2026-09-29; re-check prices before quoting.
Sources are in [docs 1 to 3](01-product-positioning-and-messaging-audit.md) and [evidence/derived](../evidence/derived/).

## Reference table (assessment template)

| Evaluation Vector | Baseten | DeepInfra | Nebius (Token Factory) |
| :---- | :---- | :---- | :---- |
| **Pricing Model** | Two lines. Model APIs per token: GLM-5.3 $1.40 in / $4.40 out, cached input at 10%; gpt-oss-120b $0.10 / $0.50; Kimi K3 $3.00 / $15.00. Dedicated per GPU-minute: H100 $6.50/h, B200 $9.98/h; wake-up minutes billed; scale-to-zero default. Basic, Pro, Enterprise plans; SLA 99.9% with 40% credit cap | Per token, price leader: gpt-oss-120b $0.037 / $0.17; DeepSeek V4 Flash 0731 $0.06 / $0.18 with cache read at 0.25x; Llama 3.3 70B Turbo $0.10 / $0.32. Three tiers on the same weights: Flex 0.8x, standard, Priority 1.5x; batch 0.8x. Dedicated per GPU-hour: H100 $2.20, B200 $3.69, B300 $4.89. Card required, no free tier, no SLA | Per token, mid-pack: gpt-oss-120b $0.15 / $0.60; Kimi K3 $3.00 / $15.00; DeepSeek V4 Flash 0731 $0.14 / $0.28. Fast and Base flavors, delta unpublished. No cached-input discount. Batch at 50% off base. Dedicated endpoints per GPU-hour, per-minute granularity, rate card behind login; cloud H100 $3.85/h rising to $4.50 on 2026-10-01. $1 trial credit; 99.9% SLA on dedicated only |
| **Cold-Start Strategy** | Scale-to-zero with billable wake-up. Baseten Delivery Network caches weights on node NVMe, in-cluster peer cache, mirrored origin; image streaming; torch compile cache; `min_replica` warm floor; scheduled autoscaling. No published cold-start seconds (the cold-start docs page gives no latency figures); sync requests park up to 1,200 s | No cold start exposed to the caller. Shared warm pools for the catalog; contention handled by 429, `fail_fast`, Flex waits up to 10 minutes, or Priority admission. Low-usage models are deprecated and silently redirected. Dedicated deployments may scale to zero (`min_instances: 0`) | Serverless: shared "Global" pool, no cold-start statement, no region guarantee. Dedicated: "initial deployment can take several minutes", scale above min replicas "not guaranteed indefinitely", stopping may release unrecoverable capacity; keep `min_replicas` at 1 or more to avoid cold starts |
| **Primary Sweet Spot (Use case and ideal customer)** | Latency-sensitive custom or fine-tuned models at AI-native scale-ups (code completion, clinical dictation, TTS). Buyer wants engine control (TensorRT-LLM builder, speculative decoding, KV-aware routing) and multi-cloud failover without running Kubernetes | Highest-volume, lowest-price open-weight tokens for agents, chat, and aggregators. Buyer swaps a base URL in the OpenAI SDK, accepts FP4 and US-only processing, and needs no contract. Also the default supplier behind OpenRouter | European or regulated enterprises that need EU residency, a fine-tune-and-serve loop on one platform, and dedicated Blackwell capacity from an owner-operator. Buyer signs a DPA and a reserved-capacity contract |
| **Key Technical Limitation** | Cost and opacity of the shared tier: 11 Model API slugs (no Llama, no Qwen); advanced engine features (KV-aware routing, disaggregation, token autoscaling) are Enterprise-only; region pinning is `us` or `eu` only; marketing 99.99% versus contractual 99.9%; inference error body is a bare string, not the OpenAI error object | No SLA, no EU region, no custom containers on serverless, no engine controls, no per-minute rate limits published, no request-ID header. Aggressive FP4 with 31 of 102 models undeclared; served context can be far below the model ceiling; silent deprecation redirects | Serverless has no region guarantee, no cached-input pricing, no speech, and no `-fast` SKU in the public catalog after the June removals, 21 serverless SKUs removed in three months; ZDR disables speculative decoding; dedicated H200 is us-central1 only and H100 is eu-north1 only; observability and TTFT metrics exist only on dedicated; OpenRouter 30-day uptime 96.9% (gpt-oss-120b) and 91.4% (Qwen3-235B) |

## One-line positioning for live calls

| Vector | Baseten | DeepInfra | Nebius (Token Factory) |
| --- | --- | --- | --- |
| Pricing Model | Premium: per token on 11 shared models, per GPU-minute on dedicated at 2 to 3x DeepInfra list | Cheapest list price; tiers (Flex 0.8x, Priority 1.5x) on the same weights | Mid-priced per token; no cached-input discount; dedicated rate card behind login |
| Cold-Start Strategy | Scale to zero, cached weights, no published seconds, wake-up is billed | No cold start; queues and 429s instead | Shared pool with no statement; dedicated needs `min_replicas` of 1 or more |
| Sweet spot | Custom or fine-tuned models where latency is revenue | Highest-volume, lowest-cost open-weight tokens | EU residency plus fine-tune and serve on owned GPUs |
| Key limitation | Enterprise-only engine features; 99.99% marketed, 99.9% contracted | No SLA, no EU region, FP4 often undeclared | Serverless has no region guarantee; OpenRouter uptime 91 to 97% |

## Extended rows

| Vector | Baseten | DeepInfra | Nebius (Token Factory) |
| --- | --- | --- | --- |
| Engines | TensorRT-LLM (Engine Builder), vLLM and SGLang (BIS-LLM), BEI, Dynamo, custom C++ gRPC server | vLLM, SGLang, TensorRT-LLM, Dynamo; own forks | vLLM with EAGLE-3; TensorRT-LLM POC; Groq 3 LPX subset |
| Quantization disclosure | User-selected per deployment | Per model in public catalog; 41% fp8, 17% fp4, 30% undeclared | Per dedicated template; 69% fp8; serverless per `/v1/models?verbose=true` |
| Regions | 18 clouds, 87 clusters; pin `us` or `eu`; EU, UK, AU environments via support | 8 US sites plus Toronto; no region choice | Serverless global (EU ingress); dedicated eu-north1, eu-west1, us-central1 |
| Ingress fingerprint (captured) | `via: 1.1 google`; management on AWS | FastAPI on uvicorn, own ASN (AS16581), one /24 | FastAPI, own ASN (AS214415), single NL-registered address |
| OpenAI conformance | Error body non-conformant; 403 on bad key | Best of three on the OpenAI route; Responses API first seen 2026-09-29; chat schema drops `top_logprobs`, `logit_bias`, `parallel_tool_calls` | Adds Responses API and rerank; drops `seed`; FastAPI error bodies |
| Rate-limit headers | Full OpenAI set plus uncached-input split | None documented | Full OpenAI set plus dynamic-scale headers |
| Observability | TTFT, TPS, queue, KV hit, replicas; Prometheus, OTLP, tracing | Platform-wide live metrics; usage and cost APIs; no per-request TTFT | Dedicated only: TTFT, TPS, KV hit, error rate; Prometheus federation |
| Custom model path | Truss config or custom Docker server; weights from HF, S3, GCS, R2, Azure | Hugging Face repo ID only; container only on GPU rentals | Template plus flavor; custom weights in beta on request |
| Status page | 6 product components; 35 incidents in 90 days | Per-model components; no incident API | 161 components by region; Token Factory per region; 8 incidents titled Token Factory, Feb 18 to Jul 1 |
| Retention | Inputs and outputs not stored; KV in GPU memory only | Zero retention by contract | Retains inputs for speculative decoding unless ZDR is enabled |

## Landmines: what a prospect will hear from each vendor, and the counter

| If the prospect says | Reply with |
| --- | --- |
| "Baseten has four nines out of the box" | The published SLA is 99.9%, credits are capped at 40%, and the status API shows 8 major incidents in 90 days. Ask for the SLA document and the per-model status history |
| "Baseten is the fastest" | True on TTFT for shared APIs (0.19 s on gpt-oss-120b). Ask what the same workload costs: H100 $6.50/h and B200 $9.98/h on dedicated, and Kimi K3 at $15 per million output tokens |
| "DeepInfra is the cheapest" | True on list price. Ask which precision is served (FP4 on many flagships), what context is actually served, and what the remedy is when a model endpoint is down for eight hours with no SLA |
| "DeepInfra is OpenAI compatible" | Best of the three on the OpenAI route, and still missing `top_logprobs`, `logit_bias`, `parallel_tool_calls` on chat completions, request-ID headers, and rate-limit headers. Ask for the OpenAPI spec and run the diff |
| "Nebius is EU-sovereign" | True for dedicated endpoints. Serverless is "Global" with "no region guarantee", and enabling zero retention disables speculative decoding. Ask which tier the quote is for |
| "Nebius has sub-second TTFT" | Third-party data shows 0.94 s on gpt-oss-120b and 1 to 2.3 s on reasoning models; US Central edge TTFB alone is 217 ms. Ask for a measured TTFT from the prospect's region |

## Traps to set: questions that expose gaps across all three

1. Ask for the served context length, output cap, precision, and engine of a model. Nebius
   publishes precision, context, and a tokens-per-second figure; none of the three publishes the
   output cap and engine alongside them on the serverless tier.
2. Ask for measured TTFT from the cities where the prospect's users sit. No competitor terminates
   at the edge or publishes geography-specific latency.
3. Ask what happens to live traffic when a model is deprecated. DeepInfra redirects silently,
   Nebius does not reroute, Baseten gave 12 days notice on six APIs.
4. Ask whether a region can be pinned with a residency commitment on the per-token tier. Only
   Baseten offers `us` or `eu`; Nebius requires dedicated; DeepInfra has no option.
5. Ask for the export path to self-host the same serving configuration. None of the three
   provides manifests; Akamai can with LKE.
