# 4A. Strategic Output: Product Management Brief

Starting position: no public per-token price list for Akamai serverless inference was found; job
postings show a serverless inference platform in development. Akamai Inference Cloud sells the
RTX PRO 6000 Blackwell at $3.00 per GPU-hour list in 20 regions (request access), with vLLM,
KServe, NVIDIA Dynamo, and NIM on LKE. The card has no NVLink and 20% of a B200's memory
bandwidth. Capacity in the first 20 cities sold out; a $500M replenishment lands mostly in early
2027. The recommendations assume the existing fleet and LKE.

## Recommendation 1: Publish a serving contract per model, and an SLA that matches the marketing

- **Problem:** Baseten markets 99.99% against a 99.9% SLA. DeepInfra has no SLA and silently redirects deprecated models. Nebius removed 21 serverless SKUs in three months without rerouting. 31 of DeepInfra's 102 active text models declare no precision.
- **Action:** Publish per model and region, in `/v1/models` and a public catalog: weights revision, precision (weights and KV), served context and output cap, engine and version, speculative decoding on or off, TTFT and tokens/s targets at a stated concurrency, 30-day deprecation notice, never-silent replacement. Pair with a 99.9% monthly SLA on serverless from day one, per-model status components, automatic credits.
- **Why Akamai wins:** The disclosure plumbing exists: a 250-component Statuspage and `llms.txt` on techdocs. Akamai sells to enterprises that buy on contract terms; none of the three does.
- **Metric:** Every model page carries all contract fields; automatic SLA credits; zero silent substitutions in year one.

## Recommendation 2: Make routing geography the product

- **Problem:** Nebius serverless answers from one European address (217 ms edge TTFB from US Central). DeepInfra is US-only with no EU option. Baseten pins only `us` or `eu`, then hops to a GPU in another cloud. KV-aware routing is Enterprise-only at Baseten; Nebius has no cached-input price.
- **Action:** Terminate the OpenAI-compatible endpoint on the anycast edge. Add a `region` request field and a region response header; honor pinning (EU, US, UK, APAC) contractually. Run Dynamo KV-aware routing across the RTX PRO 6000 regions with a documented session-affinity header. Price cached input at 10% of input with DeepInfra's field names (`prompt_cache_key`, `prompt_cache_options`). Put the AI Grid semantic cache in front of the KV cache.
- **Why Akamai wins:** 4,400+ edge PoPs and 20 GPU regions; zero egress fees remove the cost objection to multi-region replication. Only if the gateway runs at the edge: today `api.linode.com` returns first byte in 164 ms against Baseten's 106 ms.
- **Metric:** Edge TTFB p50 under 50 ms from the top 20 metros; cache hit rate above 60% on agent traffic.

## Recommendation 3: Size the catalog to the RTX PRO fleet, sell tiers, and price on the contract

- **Problem:** At list price the RTX PRO 6000 cannot match DeepInfra per token on dense 70B models (table below), and Nebius lists the same card at $1.80 per GPU-hour.
- **Action:** Launch with the 20B to 120B class that fits one to four cards at FP8 or NVFP4 (gpt-oss-120b and 20b, Qwen3.x 27B to 35B, Gemma 4 31B, Nemotron 3 Nano, Super, and 3.5 Lightning, DeepSeek V4 Flash, Whisper, embeddings). Sell standard, flex (0.8x), priority (1.5x), and batch (0.8x) tiers with DeepInfra's field names. Ship OpenAI chat, Responses, and Anthropic Messages with a public OpenAPI spec and conformance report. Offer an export-to-LKE path. Price mid-pack; reserve price-leader SKUs for small-active-parameter MoE models.
- **Why Akamai wins:** The fleet is deployed in 20 regions and demand has outrun supply. The stack matches the competitors', so the risk is integration, not research. No competitor offers a self-hosted exit from its per-token tier.
- **Metric:** Ten launch models with contract fields; sign-up to first paid token above 40% in 30 days; top-three TTFT on gpt-oss-120b in a published third-party benchmark.

Cost floor per 1M output tokens, Llama 3.3 70B, list GPU-hour price divided by NVIDIA-published
maximum throughput (1,000 input and 1,000 output tokens):

| GPU and list price | Cost per 1M output tokens |
| --- | --- |
| Akamai RTX PRO 6000, $3.00/h | $0.48 |
| Nebius AI Cloud RTX PRO 6000, $1.80/h | $0.29 |
| DeepInfra H100, $2.20/h | $0.28 |
| DeepInfra B200, $3.69/h | $0.15 |
| DeepInfra retail price, Llama 3.3 70B Turbo output | $0.32 |

The gap narrows on small-active-parameter MoE models (2.2x on Qwen3 30B-A3B against 3.2x on
Llama 3.3 70B), which suit GDDR7. Sequencing: contract schema, edge gateway, and ten models in
Q4 2026; tiers and cached-input pricing in Q1 2027; Responses API, Anthropic Messages, and
export-to-LKE in Q2 2027. Problem evidence, risks, and the full unit-economics table:
[full report 4, Part A](../docs/04a-strategic-output-product-management-brief.md).
