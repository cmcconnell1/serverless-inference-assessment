# 4. Strategic Output: PM Brief & SE Field Guide, Part A: Product Management Brief

Audience: Akamai Cloud product management for serverless AI inference. Date: 2026-09-29.
Competitor facts dated 2026-09-28, probe captures 2026-09-29; Akamai and Nebius price pages read in a browser on 2026-09-29.

## Starting position

| Fact | Source |
| --- | --- |
| No public per-token price list for Akamai serverless inference was found on akamai.com or techdocs as of 2026-09-29; a serverless inference platform is in development ("reliability workstreams for Akamai's serverless inference platform" in current job postings). Akamai Inference Cloud sells GPU hours (RTX PRO 6000 Blackwell at $3.00 per GPU-hour list, 96 GB GDDR7, 20 regions marked "limited deployment availability", every plan marked "Request access") plus a pre-configured Kubernetes stack (vLLM, KServe, NVIDIA Dynamo, NIM) on LKE | [A1][A2][A7] |
| AI Grid (2026-03-16) adds an orchestrator that routes on "cost per token, time-to-first-token, and throughput" across 4,400+ edge locations, with semantic caching on Akamai Functions. The same release states "Akamai Inference Cloud is available today for qualified enterprise customers" | [A3] |
| GPU capacity in the first 20 cities was "sold out" before general availability; a $500M replenishment lands mostly in early 2027 | [A4][A5] |
| The RTX PRO 6000 has no NVLink and 1,597 GB/s of memory bandwidth, 20% of a B200 and 48% of an H100 SXM; an 8-GPU server holds 768 GB. Trillion-parameter MoE models (Kimi K3 862B, Qwen3.8 2.4T) that headline competitor catalogs fit only at FP4 and only with PCIe-bound tensor parallelism | [A2][H3][H4][N1] |
| Competitors cluster on the same engines (vLLM, Dynamo) and the same API dialect (OpenAI). Differentiation is in transparency, routing geography, and pricing tiers, see [docs 2](02-technical-architecture-and-engine-mechanics.md) and [docs 3](03-developer-experience-dx-and-api-surface-evaluation.md) | [P-OPENAPI] |

The recommendations below assume a serverless product built on the existing RTX PRO 6000 fleet
and LKE, not on new HGX capacity.

## Recommendation 1: Ship a published serving contract per model, and an SLA that matches the marketing

### Problem observed

| Competitor gap | Evidence |
| --- | --- |
| Baseten markets "99.99% uptime out of the box" while its SLA is 99.9%, credits are capped at 40%, and 8 major incidents hit in 90 days | [B1][B2][P-STATUS] |
| DeepInfra has no SLA and no credits for serverless; individual model endpoints were down 8 h and 6 h in July; deprecated models are silently redirected to a different model | [D1][D2][D3] |
| Nebius removed 21 serverless SKUs in three months with no automatic reroute; serverless carries "no region guarantee"; ZDR disables speculative decoding without a price change | [N2][N3][N4] |
| Quantization and served context are disclosed inconsistently: 31 of DeepInfra's 102 active text models declare no precision; DeepInfra's own benchmark served DeepSeek V4 Pro at a 66k context on FP4 while the vendor ceiling is 1M | [P-CATALOG][D4] |

### Recommendation

Publish, per model and per region, a machine-readable serving contract in the `/v1/models`
response and on a public catalog endpoint: weights hash and revision, precision (weights and KV),
served context and output cap, engine and version, speculative decoding on or off, TTFT and
tokens-per-second targets at a stated concurrency, deprecation date with a guaranteed 30 day
notice, and the replacement policy (never silent). Pair it with a 99.9% monthly SLA that applies
to the serverless tier from day one, with per-model and per-region status components, and
credits that are automatic rather than claimed within 24 hours.

### Why Akamai can win this

Akamai already runs a Statuspage with 250 components grouped by region and service and publishes
`llms.txt` and an agent-skills index on techdocs, so the disclosure plumbing exists [P-STATUS][P-API].
The brand sells to enterprises that buy on contract terms; none of the three competitors does.

### Metric and risk

| Success metric | Risk |
| --- | --- |
| Every serverless model page shows all contract fields; SLA credits paid automatically; zero silent model substitutions in the first year | Publishing TTFT targets creates a public benchmark. Mitigate by stating concurrency and prompt length with each target and by starting with models whose numbers are strong on RTX PRO 6000 |

## Recommendation 2: Make routing geography the product: anycast ingress, region pinning, and priced prefix caching

### Problem observed

| Competitor gap | Evidence |
| --- | --- |
| Nebius serverless ingress is one European address; edge TTFB p50 is 100 ms from Germany and 217 ms from US Central | [P-DNS][N5] |
| DeepInfra ingress is US-only with no region parameter and no EU option; GDPR listed as "in progress" | [P-DNS][D5][D6] |
| Baseten offers `us` and `eu` pinning only, terminates at Google's front end, then hops to a GPU in another cloud; internal retries are exposed in a response header | [B3][B4][P-API] |
| Prefix caching is priced by Baseten (about 10% of input) and DeepInfra (0.2x read, explicit TTL) but not by Nebius, whose 31-vote request sits "In Review" | [B5][D7][N6] |
| KV-aware routing is Enterprise-only at Baseten and undocumented as a control at DeepInfra and Nebius | [B6][D8][N7] |

### Recommendation

1. Terminate the OpenAI-compatible endpoint on Akamai's anycast edge at every PoP, the same way
   `api.linode.com` already resolves through `akamaiedge.net` [P-DNS].
2. Add a `region` request field and `x-akamai-inference-region` response header. Default to
   nearest GPU region; honor pinning for residency (EU, US, UK, APAC) as a contractual commitment,
   which Nebius offers only on dedicated endpoints [N3].
3. Run NVIDIA Dynamo's KV-aware router across the 20 RTX PRO 6000 regions and make session affinity a
   documented header from day one, as Baseten does with `x-session-affinity` [B7].
4. Price cached input at 10% of input and offer explicit cache retention (5 minute and 1 hour
   TTL) with the same request fields DeepInfra uses (`prompt_cache_key`, `prompt_cache_options`),
   so agent frameworks already tuned for DeepInfra work unchanged [D7][P-OPENAPI].
5. Put the semantic cache from AI Grid in front of the KV cache at the edge, so identical prompts
   never reach a GPU [A3].

### Why Akamai can win this

DeepInfra terminates in one US /24 and Nebius at one NL address, each on its own network; Baseten rents Google's front end
and then hops to a GPU in whichever cloud has capacity. None of the three places GPUs by user
geography. Akamai's edge plus 20 RTX PRO 6000 regions (22 GPU-capable regions in the public
regions API) is a distribution advantage that engine parity cannot erase [P-REGIONS][A2][A3], but
only if the gateway runs at the edge: from a US vantage point, a minimal request to
`api.linode.com` returns its first byte in 164 ms against 106 ms for Baseten's Google front end,
mostly because the Linode API origin sits behind the edge [P-LAT]. Zero egress fees remove the cost
objection to multi-region replication [A1].

### Metric and risk

| Success metric | Risk |
| --- | --- |
| Edge TTFB p50 under 50 ms from the top 20 metros (today a minimal `api.linode.com` request measures 164 ms from one US vantage point [P-LAT]); TTFT on gpt-oss-120b within 2x of the Artificial Analysis leader (Baseten 0.19 s) as a hypothesis to validate on RTX PRO 6000 before it is published; cache hit rate above 60% on agent traffic | Cross-region KV routing adds a control-plane dependency. Mitigate by starting with region-local KV-aware routing and cross-region only for failover |

## Recommendation 3: Right-size the catalog to the RTX PRO fleet, price on the contract rather than on parity, and sell service tiers

### Problem observed

| Competitor gap | Evidence |
| --- | --- |
| Baseten's shared Model APIs cover 11 slugs and exclude Llama and Qwen; the deployable path needs a Python packaging tool and engine config | [B7][B8] |
| DeepInfra sells three tiers on the same weights (Flex 0.8x, standard, Priority 1.5x) plus batch at 0.8x, but hides batching controls and publishes no per-minute rate limits | [D9][D10][D11] |
| Nebius sells Fast and Base flavors, but the June notice removed six `-fast` serverless SKUs, its public catalog lists no `-fast` IDs today, and it does not publish the price delta or dedicated hourly rates | [N2][N8][N9] |

### Unit economics: cost per token, not cost per GPU-hour

A lower GPU-hour price does not mean a lower token price. The table divides each list GPU-hour
price by NVIDIA's published maximum output throughput per GPU for the same model and sequence
lengths (1,000 input and 1,000 output tokens). It is a cost floor at full batch utilization;
real serving runs below it.

| Model | GPU and list price | Output tokens/s per GPU | Cost per 1M output tokens | Source |
| --- | --- | --- | --- | --- |
| Llama 3.3 70B | Akamai RTX PRO 6000, $3.00/h | 1,724 (FP4) | $0.48 | [H1][A2] |
| Llama 3.3 70B | DeepInfra B200, $3.69/h | 6,920 (FP4) | $0.15 | [H1][D12] |
| Llama 3.3 70B | DeepInfra H100, $2.20/h | 2,209 (FP8) | $0.28 | [H1][D12] |
| Llama 3.3 70B | Baseten B200, $9.98/h | 6,920 (FP4) | $0.40 | [H1][B5] |
| Llama 3.3 70B | Nebius AI Cloud RTX PRO 6000, $1.80/h | 1,724 (FP4) | $0.29 | [H1][N10] |
| Llama 3.3 70B | Nebius AI Cloud H100, $3.85/h | 2,209 (FP8) | $0.48 | [H1][N10] |
| Llama 3.3 70B | Baseten H100, $6.50/h | 2,209 (FP8) | $0.82 | [H1][B5] |
| Qwen3 30B-A3B | Akamai RTX PRO 6000, $3.00/h | 9,938 (FP4) | $0.084 | [H1][A2] |
| Qwen3 30B-A3B | DeepInfra B200, $3.69/h | 26,971 (FP4) | $0.038 | [H1][D12] |

DeepInfra sells Llama 3.3 70B Turbo output at $0.32 per million tokens [P-CATALOG], below the
$0.48 floor an RTX PRO 6000 reaches at Akamai's own list price. MLPerf Inference v5.1 shows the
same ratio: an RTX PRO 6000 delivers about 0.26x the Llama 2 70B throughput of a B200 and 0.84x
that of an H100 [H2]. Akamai's internal GPU cost sits below list and is not public, so the break-even
is a number product management must compute; at list, price parity with DeepInfra on dense 70B
models loses money. The gap narrows on small-active-parameter MoE models (2.2x on Qwen3 30B-A3B
versus 3.2x on Llama 3.3 70B), which are bandwidth-light and suit GDDR7.

Akamai's own benchmark claim is consistent with this table once the comparison price is fixed. The
GPU card counts blog reports "28% lower cost per million tokens" and "higher throughput (3,140 vs.
2,987 tokens/sec)" for one RTX PRO 6000 against an H100, "nearly identical cost per token" at two
cards, and a 30% to 50% throughput advantage for NVLink H100/H200 systems at four cards [A6]. On
the throughput figures above, an RTX PRO 6000 at $3.00 matches Nebius's $3.85/h H100 and is
about 40% cheaper per token than Baseten's $6.50/h H100. The claim holds against typical H100
pricing; it does not hold against DeepInfra's $2.20/h H100 or any B200, and DeepInfra is the price
reference buyers in this segment use.

The same card is also cheaper elsewhere: Nebius AI Cloud lists the RTX PRO 6000 on demand at
$1.80 per GPU-hour, 40% below Akamai's $3.00, with spot capacity from $0.79 [N10]. Any Akamai
per-token price built on the RTX PRO 6000 competes with a Nebius cost floor on identical hardware.

### Recommendation

1. Catalog: launch with the 20B to 120B open-weight class where a single RTX PRO 6000 or a
   2 to 4 GPU slice serves at FP8 or NVFP4 without NVLink penalties: gpt-oss-120b and 20b, Qwen3.x
   27B to 35B, Gemma 4 31B, Nemotron 3 Nano, Super, and 3.5 Lightning, DeepSeek V4 Flash at NVFP4,
   Whisper, Qwen3 embeddings and rerankers. Add trillion-parameter MoE only on dedicated
   multi-node endpoints, and say so in the serving contract.
2. Tiers, not knobs: standard, flex (0.8x, bounded wait), priority (1.5x, protected admission),
   and batch (0.8x, 24 h) using DeepInfra's field names (`service_tier`, `fail_fast`) so switching
   costs a base URL change. Reserve engine-level configuration for dedicated endpoints on LKE.
3. API dialect: OpenAI chat and completions plus the Responses API (Nebius and DeepInfra have
   it, Baseten does not) and Anthropic Messages (Baseten and DeepInfra have it), with a public OpenAPI spec and a
   published conformance report against the OpenAI request schema, the same mechanical diff used
   in [docs 3](03-developer-experience-dx-and-api-surface-evaluation.md).
4. Portability as a feature: a documented "export to LKE" path that emits the vLLM and Dynamo
   manifests for the same model, so the serverless tier is an on-ramp to the GPU business rather
   than a lock-in. None of the three competitors offers a self-hosted exit for their per-token
   tier.
5. Pricing: do not lead with price on this fleet. Price near Nebius and Baseten (mid-pack) and
   sell the serving contract, region pinning, and edge routing as the reason to pay it. Reserve
   price-leader SKUs for small-active-parameter MoE models, where the RTX PRO 6000 gap to B200 is
   smallest, and revisit parity once HGX capacity from the replenishment lands.

### Why Akamai can win this

The fleet is already deployed in 20 regions and demand has outrun supply [A2][A4]. Its constraint
is memory bandwidth, not capacity per node, which is why the catalog leans on MoE models with few
active parameters and why the pitch is contract and geography rather than unit price. The Kubernetes
stack (vLLM, KServe, Dynamo) is the same one the competitors run, so the engineering risk is
integration, not research [A1].

### Metric and risk

| Success metric | Risk |
| --- | --- |
| Ten launch models live with contract fields; 30-day developer activation from sign-up to first paid token above 40%; at least one published third-party benchmark (Artificial Analysis) showing Akamai in the top three on TTFT for gpt-oss-120b | Catalog looks narrow next to DeepInfra's 102 models. Mitigate with the export-to-LKE path for long-tail models and by adding partner-proxied frontier models only if the serving contract can be honored for them |

## Sequencing

| Quarter | Deliverable | Dependency |
| --- | --- | --- |
| Q4 2026 | Serving contract schema, per-model status components, OpenAI-dialect gateway on the edge with `region` field, launch catalog of ten models in 3 GPU regions | Existing RTX PRO 6000 fleet, AI Grid orchestrator |
| Q1 2027 | Flex, priority, batch tiers; cached-input pricing and explicit retention; Prometheus export; public OpenAPI spec | Dynamo KV-aware routing per region |
| Q2 2027 | Responses API, Anthropic Messages, export-to-LKE, SLA credits automation; expand to all 20 RTX PRO regions as the replenishment lands | $500M capacity replenishment |

## Sources

Probe captures (this repository, 2026-09-29): [P-STATUS] [evidence/derived/status-incidents.md](../evidence/derived/status-incidents.md); [P-CATALOG] [evidence/derived/deepinfra-catalog.md](../evidence/derived/deepinfra-catalog.md); [P-DNS] [evidence/derived/dns-cdn.md](../evidence/derived/dns-cdn.md); [P-API] [evidence/derived/api-surface.md](../evidence/derived/api-surface.md); [P-OPENAPI] [evidence/derived/openapi-surface.md](../evidence/derived/openapi-surface.md); [P-REGIONS] [evidence/derived/akamai-regions.md](../evidence/derived/akamai-regions.md); [P-LAT] [evidence/derived/latency.md](../evidence/derived/latency.md).

Akamai:

- [A1] https://www.akamai.com/products/akamai-inference-cloud-platform
- [A2] https://techdocs.akamai.com/cloud-computing/docs/gpu-compute-instances and https://www.akamai.com/cloud/pricing/north-america
- [A3] https://www.akamai.com/newsroom/press-release/akamai-launches-ai-grid-intelligent-orchestration-for-distributed-inference-across-4400-edge-locations (2026-03-16)
- [A4] Akamai Q4 2025 earnings call, 2026-02-19, https://www.stockinsights.ai/us/AKAM/earnings-transcript/fy25-q4-a227
- [A5] Akamai Q2 2026 earnings call, 2026-08-06, https://www.fool.com/earnings/call-transcripts/2026/08/13/akamai-akam-q2-2026-earnings-call-transcript/
- [A6] Why GPU Card Counts Matter for Real AI Workloads, Akamai blog, https://www.akamai.com/blog/cloud/why-gpu-card-counts-matter-real-ai-workloads
- [A7] Akamai careers, Senior Site Reliability Engineer, https://jobs.akamai.com/en/sites/CX_1/job/2688

Akamai page captures read from an interactive browser on 2026-09-29: [evidence/manual/akamai-verification.md](../evidence/manual/akamai-verification.md).

Hardware and throughput:

- [H1] NVIDIA TensorRT-LLM performance overview (TRT-LLM 1.3.0rc28, updated 2026-09-21), output tokens per second per GPU, https://nvidia.github.io/TensorRT-LLM/latest/developer-guide/perf-overview.html
- [H2] MLPerf Inference v5.1 closed, Llama2-70B-99, per-GPU values divided from system totals: HPE DL380a 8x RTX PRO 6000 26,205.8 tok/s; NVIDIA 8x B200 101,527; Cisco 16x H100 62,351.6, https://mlcommons.org/2025/09/mlperf-inference-v5-1-results/ and https://github.com/mlcommons/inference_results_v5.1
- [H3] NVIDIA RTX PRO 6000 Blackwell Server Edition specifications, https://www.nvidia.com/en-us/data-center/rtx-pro-6000-blackwell-server-edition/
- [H4] NVIDIA DGX B200 and H100 specifications, https://www.nvidia.com/en-us/data-center/dgx-b200/ and https://www.nvidia.com/en-us/data-center/h100/

Baseten:

- [B1] https://www.baseten.co/
- [B2] https://www.baseten.co/service-level-agreement/
- [B3] https://docs.baseten.co/deployment/regional-deployments
- [B4] https://docs.baseten.co/deployment/autoscaling/request-lifecycle
- [B5] https://www.baseten.co/pricing/
- [B6] https://docs.baseten.co/engines/bis-llm/advanced-features
- [B7] https://docs.baseten.co/inference/model-apis/overview
- [B8] https://docs.baseten.co/reference/truss-configuration

DeepInfra:

- [D1] https://deepinfra.com/terms
- [D2] https://status.deepinfra.com/
- [D3] https://github.com/theopenco/llmgateway/pull/4222
- [D4] https://deepinfra.com/blog/deepseek-v4-pro-max-api-benchmarks-latency-throughput-cost
- [D5] https://deepinfra.com/privacy
- [D6] https://trust.deepinfra.com/compliance
- [D7] https://deepinfra.com/blog/prompt-cache-retention
- [D8] https://deepinfra.com/blog/deepinfra-nvidia-inference-stack
- [D9] https://deepinfra.com/blog/flex-service-tier
- [D10] https://deepinfra.com/blog/priority-service-tier
- [D11] https://docs.deepinfra.com/account/rate-limits
- [D12] https://deepinfra.com/pricing

Nebius:

- [N1] https://tokenfactory.nebius.com/endpoints
- [N2] https://docs.tokenfactory.nebius.com/june-2026-deprecation-notice.md and https://docs.tokenfactory.nebius.com/august-2026-deprecation-notice.md
- [N3] https://docs.tokenfactory.nebius.com/public-serverless.md
- [N4] https://docs.tokenfactory.nebius.com/legal/legal-quick-guide.md
- [N5] https://llmlatency.dev/provider/nebius
- [N6] https://ideas.nebius.com/p/support-impliciteexplicite-prompt-caching
- [N7] https://nebius.com/blog/posts/routing-is-the-difference-between-scaling-and-stalling
- [N8] https://docs.tokenfactory.nebius.com/ai-models-inference/overview
- [N9] https://tokenfactory.nebius.com/api/public/models_info
- [N10] Nebius AI Cloud GPU pricing, on-demand and spot, https://nebius.com/prices (2026-09-29)
