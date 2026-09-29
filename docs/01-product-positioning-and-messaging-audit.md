# 1. Product Positioning & Messaging Audit

Scope: Baseten, DeepInfra, and Nebius Token Factory as of 2026-09-28. Every marketing quote is
verbatim from the vendor page cited. Every counter-fact is from a contractual document, a status
page API, a third-party benchmark, or a capture in [evidence/derived](../evidence/derived/).

## 1.1 Market narrative

| Vector | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Tagline | "Inference is everything" [B1] | "AI Inference: FAST, SIMPLE, RELIABLE, LOW-COST" [D1] | "Run open models at production scale" [N1] |
| One-line value prop | "The fastest model runtimes, cross-cloud high availability, and seamless developer workflows" [B1] | "Scale to trillions of tokens without breaking the bank" [D1] | "OpenAI-compatible API to start fast. Dedicated GPUs, post-training, and workload optimization when you scale" [N2] |
| Core frame | Inference engineering company. Sells a runtime (Baseten Inference Stack), a control plane (Truss, environments), and capacity brokered across 18 clouds and 87 clusters [B2] | Price and ownership company. "Built DeepInfra from the ground up, from GPU hardware to API layer"; owned GPUs in nine colocation sites [D2][D3] | Vertically integrated neocloud. Token Factory is the inference layer on Nebius-owned data centers; "serves the full workload lifecycle on one platform" [N3] |
| Lead product | Dedicated Inference (per GPU-minute). Model APIs (per token) added May 2025 as a second line [B3][P-STATUS] | Serverless per-token APIs. Dedicated GPU-hour deployments and DeepCluster are secondary [D4] | Serverless per-token plus Dedicated Endpoints (GA 2026-02-26) with fine-tuning and Data Lab [N4] |
| Proof points used | Named logos (Notion, Cursor, Writer, Vercel), case-study multipliers ("2-3x lower latency"), day-0 launches [B1][B4] | Price tables, "close to five trillion tokens a week", OpenRouter supply share [D5][D6] | Prosus "up to 26x cost reductions", Revolut, Sword Health P99 "over 20 seconds to under 12", SemiAnalysis quote on ODM chassis TCO [N1][N5] |
| Capital position | Series F, $1.5B at up to $13B valuation, 2026-06-22 [B2] | Series B, $107M, 2026-05-04; NVIDIA and Supermicro investors [D3] | Parent NASDAQ: NBIS, Q2 2026 revenue $582.3M, AI cloud ARR $3.0B; Eigen AI acquisition about $643M for inference R&D [N6][N7] |
| Where the narrative is thin | "Cross-cloud high availability" is sold as a feature, yet 17 of 35 incidents in the last 90 days name a single cluster, region, cloud, or upstream provider in the title [P-STATUS] | "Reliable" carries no SLA of any kind; the terms promise "commercially reasonable efforts" and cap liability at six months of fees [D7] | "Production scale" for serverless carries a "no region guarantee" caveat and a 99% best-effort tier; the 99.9% SLA applies to dedicated endpoints only [N8][N9] |

Read across the three: Baseten sells engineering depth, DeepInfra sells unit price, Nebius sells
owned capacity and European residency. None of the three sells proximity to the end user, which is
the vector an edge network can own.

## 1.2 Target personas

| Dimension | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Economic buyer | VP Engineering or Head of ML Platform at an AI-native scale-up with revenue tied to model latency (Notion, Cursor, Writer, Abridge) [B1] | Founder or lead engineer at a token-volume-driven product (agents, chat, aggregators); DeepStart targets companies "founded in the last 2 years" with $250K to $10M raised [D8] | Head of AI Platform or CTO at a European or regulated enterprise (Revolut, Sword Health, Prosus) and frontier-adjacent labs needing owned GPU capacity [N1] |
| Hands-on user | ML engineer comfortable with a Python packaging tool (Truss), engine configuration, and rolling deployments [B5] | Application developer who swaps a base URL in the OpenAI SDK and never touches infrastructure [D9] | Application developer for serverless; platform engineer for dedicated endpoints and post-training [N10] |
| Entry motion | Product-led: deploy from the model library, then upgrade to Pro or Enterprise for KV-aware routing, disaggregation, and regional environments [B6] | Product-led: card on file, no free tier, pay per token; enterprise via DeepCluster (256 to 5,000 GPUs) [D10][D11] | Product-led with $1 trial credit; enterprise via sales for reserved capacity, SLA, custom DPA [N11][N9] |
| Buying trigger | Latency SLO on a custom or fine-tuned model that shared APIs cannot meet | Bill shock on a closed-model API; need the cheapest open-weight token | Data residency mandate; desire to fine-tune and serve on the same platform |
| Deal blocker to exploit | Price: H100 at $6.50 per hour and B200 at $9.98 per hour on list [B7] | No SLA, no EU region, no custom containers on serverless [D7][D12][D13] | Serverless is EU-anchored and region-free; US users see roughly twice the edge latency of German users [N12] |

## 1.3 Claims versus reality

### Claim: "instant" or "blazing-fast" cold starts

| Provider | Verbatim claim | What the documentation commits to | Independent evidence | Verdict |
| --- | --- | --- | --- | --- |
| Baseten | "blazing-fast cold starts" (homepage) [B1] | The cold-start page gives no latency figures. Sync requests park for up to 1,200 s then return 500. Wake-up minutes are billable. Weight transfer via the Baseten Delivery Network is "2-3x faster" with no absolute figure [B8][B9][B10] | Model-cache docs cite SDXL "just under 10 seconds"; NVIDIA case study cites "5-10 seconds"; competitor claims 30 to 90 s for large models; status page logged "Slower than usual scale-ups for B200s" on 2026-07-31 [B11][B12][B13][P-STATUS] | Partially supported. Fast for cached small models; unquantified for 70B+ and priced while warming |
| DeepInfra | No cold-start claim on current site. Docs: "no idle GPU time, no minimums" [D9] | Serverless models are kept warm in a shared pool; contention is handled by 429, Flex waits of up to 10 minutes, and Priority admission at 1.5x price [D14][D15] | Founder statement from 2023: cold start "under 10 s". Live platform TTFT captured at 0.42 s across all traffic [D16][P-LIVE] | Not claimed. The design substitutes queueing for cold starts, so the risk is a 429 or a 10 minute Flex wait rather than a slow first token |
| Nebius | "sub-second responses for interactive agents" for the Fast flavor [N13] | Serverless: no cold-start statement. Dedicated: "initial deployment can take several minutes"; scaling above minimum replicas "is not guaranteed indefinitely" [N14][N15] | The June 2026 deprecation removed six `-fast` serverless SKUs (the August notice removed ten base SKUs and no `-fast` ones), so the tier the claim describes is now thin [N16][N17] | Unsupported for serverless. Applies only to dedicated endpoints with min replicas above zero |

### Claim: "99.99% availability"

Reference: 99.99% allows 4.4 minutes of downtime per 30 days; 99.9% allows 43.8 minutes.

| Provider | Verbatim claim | Contract | Observed (status page API, last 90 days to 2026-09-29) | Verdict |
| --- | --- | --- | --- | --- |
| Baseten | "99.99% uptime out of the box" (homepage); "Four nines of uptime" (Model APIs page) [B1][B3] | Published SLA is 99.9% monthly, "commercially reasonable measures", credits capped at 40% of monthly fees, claims within 24 hours, upstream provider outages excluded [B14] | 35 incidents (8 major). Model APIs: 12 incidents, 4 major totalling 299 minutes. Dedicated Inference: 17 incidents, 4 major totalling 86 minutes. Third-party monitor: 99.691% of the last 30 days with no declared impact [P-STATUS][B15] | Unsupported. Marketing is one order of magnitude above the contract, and posted major-incident minutes alone exceed the 90-day 99.99% budget (13 minutes) by more than 20x for Model APIs |
| DeepInfra | "RELIABLE" (homepage) [D1] | No SLA for serverless. DeepCluster page cites "99.982% uptime SLA", which is the Tier 3 colocation figure [D7][D11] | Status page reports API "100% over 88.8 of 90 days measured"; model-level outages of 8h01m and 6h19m on 2026-07-25 and 07-26 (gemma-4-31B-it-turbo); OpenRouter registry flagged a DeepInfra endpoint at 1% uptime in September [D17][D18] | Not claimed numerically. Platform API uptime is high; individual model endpoints fail for hours without a contractual remedy |
| Nebius | "99.9% SLA" (dedicated); "Best-effort 99% availability" (Starter) [N9] | Docs: "Self-service dedicated endpoints do not include a formal SLA unless covered by contract"; historical success "approximately 99.9%" [N15] | 8 incidents titled Token Factory between 2026-02-18 and 2026-07-01 including two of roughly one day (batch inference, Data Lab). OpenRouter 30-day uptime: gpt-oss-120b 96.94%, Qwen3-235B 91.38% and "Degraded" [P-STATUS][N18] | Partially supported. The claim is honest about tiers, but serverless observed availability on OpenRouter sits well below 99% |

### Claim: "sub-second Time-To-First-Token"

Artificial Analysis figures use a 10k-token input and, for reasoning models, count thinking time,
so they are an upper bound on pure TTFT. Same-model comparison where all three are listed:

| Model | Baseten | DeepInfra | Nebius | Source |
| --- | --- | --- | --- | --- |
| gpt-oss-120b TTFT | 0.19 s | 0.69 s | 0.94 s | [T1] |
| gpt-oss-120b output tokens/s | 267 | 333 | 252 | [T1] |
| DeepSeek V4 Pro output tokens/s | 163 | listed, price $0.59 blended | 208 | [T2] |
| GLM 5.3 Flash end-to-end p50 (600 paired requests, concurrency 1) | 331 ms | 1,827 ms | 1,451 ms | [T3] |
| GLM 5.3 Flash operational failures | 0.00% | 4.00% | 14.83% | [T3] |

| Provider | Verbatim claim | Verdict |
| --- | --- | --- |
| Baseten | "fastest runtime available" (Model APIs page) [B3] | Supported on TTFT for shared APIs (fastest TTFT on gpt-oss-120b, lowest p50 in the paired test). Not supported on throughput, where it ranks mid-pack (10 of 18 on gpt-oss-120b) [T1] |
| DeepInfra | Live homepage counter, no fixed claim; blog claims "three speed tiers on the same weights" [D5] | Platform-wide TTFT captured live at 0.42 s [P-LIVE]. Per-model TTFT on shared endpoints is 0.5 to 0.9 s for non-reasoning models, so "sub-second" holds on average and fails at p99 (17 s in the paired test) [T3] |
| Nebius | "sub-second time-to-first-token, validated by internal and third-party benchmarks" [N13] | Unsupported on third-party data: 0.94 s on gpt-oss-120b and 0.99 to 2.33 s across reasoning models; edge TTFB from US Central is 217 ms before any inference work begins [T1][N12] |

## 1.4 Messaging gaps an edge provider can exploit

1. None of the three publishes a complete per-model serving contract (quantization, served
   context, output cap, engine, TTFT target, deprecation policy). Nebius comes closest: its public
   `models_info` endpoint lists quantization, context window, and a tokens-per-second figure per
   flavor, but no engine, TTFT, or output cap, and 21 serverless SKUs were removed in three months
   without automatic rerouting [N19][N16][N17]. DeepInfra discloses quantization per model but 31
   of 102 active text models carry no declaration [P-CATALOG]. Baseten discloses neither on its
   model pages.
2. None of the three sells latency by geography. Nebius is EU-anchored, DeepInfra is US-only with
   Toronto, Baseten offers `us` and `eu` pinning only [B16][D12][N12].
3. Marketing uptime and contractual uptime diverge by one order of magnitude in allowed downtime
   at Baseten and are absent at DeepInfra. A published SLA with per-model status components would be
   differentiated on its own.

## Sources

Probe captures (this repository):

- [P-STATUS] [evidence/derived/status-incidents.md](../evidence/derived/status-incidents.md), from `status.baseten.co`, `status.nebius.com`, and `status.linode.com` Statuspage APIs, 2026-09-29.
- [P-LIVE] `evidence/probes/deepinfra/live_metrics.body` and `live_metrics_2.body`, unauthenticated GET `https://api.deepinfra.com/v1/metrics/live`, two samples 30 s apart at 2026-09-29 18:21:52 and 18:22:22 UTC: `time_to_first_token` 0.417 s and 0.421 s, about 4,200 requests/s, 39.7M tokens/s.
- [P-CATALOG] [evidence/derived/deepinfra-catalog.md](../evidence/derived/deepinfra-catalog.md), from `GET https://api.deepinfra.com/models/list`, 2026-09-29.

Baseten:

- [B1] https://www.baseten.co/
- [B2] https://www.baseten.co/blog/announcing-our-series-f/ (2026-06-22)
- [B3] https://www.baseten.co/products/model-apis/
- [B4] https://www.baseten.co/resources/customers/
- [B5] https://docs.baseten.co/reference/truss-configuration
- [B6] https://docs.baseten.co/engines/bis-llm/advanced-features
- [B7] https://www.baseten.co/pricing/
- [B8] https://docs.baseten.co/deployment/autoscaling/cold-starts
- [B9] https://docs.baseten.co/deployment/autoscaling/request-lifecycle
- [B10] https://www.baseten.co/blog/baseten-delivery-network-fast-cold-starts-big-models/ (2026-03-19)
- [B11] https://docs.baseten.co/development/model/model-cache
- [B12] https://www.nvidia.com/en-us/case-studies/baseten
- [B13] https://www.spheron.network/blog/baseten-alternatives/ (competitor source)
- [B14] https://www.baseten.co/service-level-agreement/
- [B15] https://checkupstream.com/status/baseten
- [B16] https://docs.baseten.co/deployment/regional-deployments (2026-09-10)

DeepInfra:

- [D1] https://deepinfra.com/
- [D2] https://deepinfra.com/about
- [D3] https://deepinfra.com/blog/deepinfra-series-b (2026-05-04)
- [D4] https://docs.deepinfra.com/private-models/custom-llms
- [D5] https://deepinfra.com/blog/best-open-source-llm-api-providers (2026-09-14)
- [D6] https://openrouter.ai/provider/deepinfra
- [D7] https://deepinfra.com/terms (effective 2026-08-17)
- [D8] https://deepinfra.com/deepstart
- [D9] https://docs.deepinfra.com/
- [D10] https://deepinfra.com/pricing
- [D11] https://deepinfra.com/deepcluster
- [D12] https://deepinfra.com/privacy (2026-08-15)
- [D13] https://docs.deepinfra.com/gpu-instances/overview
- [D14] https://deepinfra.com/blog/priority-service-tier (2026-06-29)
- [D15] https://deepinfra.com/blog/flex-service-tier (2026-07-14)
- [D16] https://news.ycombinator.com/item?id=34874029 (2023-02-24)
- [D17] https://status.deepinfra.com/
- [D18] https://github.com/Parametrix-insurance/openrouter-uptime

Nebius:

- [N1] https://nebius.com/services/token-factory
- [N2] https://dev.nebius.com/token-factory
- [N3] Nebius Q2 2026 shareholder letter, https://assets.nebius.com/assets/a6ecfd85-a6cb-4967-8ef7-9a25bd261f9c/SHLQ226.pdf (2026-08-12)
- [N4] https://nebius.com/blog/posts/dedicated-endpoints-and-custom-weights-hub (2026-02-26)
- [N5] https://nebius.com/customer-stories/swordhealth (2026-04-09)
- [N6] https://en.wikipedia.org/wiki/Nebius_Group
- [N7] https://nebius.com/newsroom/nebius-agrees-to-acquire-eigen-ai-strengthening-nebius-token-factory-as-a-frontier-inference-platform (2026-05-01)
- [N8] https://docs.tokenfactory.nebius.com/public-serverless.md
- [N9] https://nebius.com/services/token-factory/enterprise-grade-inference
- [N10] https://docs.tokenfactory.nebius.com/ai-models-inference/dedicated-endpoints/overview.md
- [N11] https://docs.tokenfactory.nebius.com/other-capabilities/billing-new.md
- [N12] https://llmlatency.dev/provider/nebius (2026-09-28)
- [N13] https://nebius.com/services/token-factory/inference-service
- [N14] https://docs.tokenfactory.nebius.com/ai-models-inference/dedicated-endpoints/deploy-api.md
- [N15] https://docs.tokenfactory.nebius.com/ai-models-inference/dedicated-endpoints/capacity-and-scaling
- [N16] https://docs.tokenfactory.nebius.com/june-2026-deprecation-notice.md
- [N17] https://docs.tokenfactory.nebius.com/august-2026-deprecation-notice.md
- [N18] https://openrouter.ai/api/v1/models/openai/gpt-oss-120b/endpoints and https://openrouter.ai/api/v1/models/qwen/qwen3-235b-a22b-2507/endpoints (2026-09-28)
- [N19] https://tokenfactory.nebius.com/api/public/models_info (2026-09-28)

Third-party benchmarks:

- [T1] https://artificialanalysis.ai/models/gpt-oss-120b/providers
- [T2] https://artificialanalysis.ai/models/deepseek-v4-pro/providers
- [T3] https://github.com/openbenchmarks-labs/inference (GLM 5.3 Flash, reviewed 2026-09-03)
