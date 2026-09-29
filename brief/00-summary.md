# 0. Summary

Serverless inference landscape: Baseten, DeepInfra, Nebius Token Factory. This brief answers each
assessment deliverable in the order asked. The companion full report,
`serverless-inference-assessment-full-report-chris-mcconnell.pdf`, holds the evidence, citations,
method, and extended tables; section numbers in this brief match it (the full
report's section 5 is its evidence appendix). Facts dated 2026-09-28,
except probe captures (2026-09-29) and pages that block scripted clients, read in a browser on
2026-09-29.

## Key insights

- **The engine layer is commoditized: all 3 competitors serve on open engines, and all 3 run vLLM.**
  - Baseten and DeepInfra run vLLM, SGLang, TensorRT-LLM, and NVIDIA Dynamo; Nebius runs vLLM in
    production. All sit behind an OpenAI-compatible API, and Akamai's LKE stack already offers
    vLLM and NVIDIA Dynamo.
  - Differentiation sits in what is disclosed, where requests land, and how capacity is priced.
- **Marketing outruns contracts: Baseten markets 99.99% uptime against a 99.9% SLA.**
  - DeepInfra markets "reliable" with no SLA.
  - Nebius markets sub-second TTFT that third-party data does not show on its serverless tier.
- **None of the 3 places GPUs by user geography.**
  - DeepInfra answers from one /24 on its own network in the US.
  - Nebius answers from a single address on its own network in NL.
  - Baseten rents Google's front end, then hops to whichever cloud has capacity.
- **Akamai's opening is a published serving contract plus geography-aware routing, but the edge
  advantage is not automatic: 164 ms to first byte against 106 ms for Baseten.**
  - From one US vantage point, a minimal request to `api.linode.com` returns its first byte in
    164 ms, against 106 ms for Baseten's Google front end and 465 ms for Nebius.

## Competitor snapshot

| | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Sells | Inference engineering depth and multi-cloud capacity | Lowest list price on owned GPUs | Owned EU capacity, fine-tune and serve |
| Buyer | ML platform lead at an AI-native scale-up | Developer optimizing cost per token | Regulated or EU enterprise |
| Strength | Fastest shared-API TTFT (0.19 s, gpt-oss-120b); deepest engine controls | Priced prefix caching, three service tiers, fullest public API spec | 99.9% SLA on dedicated; EU residency on dedicated |
| Exploitable gap | 99.99% marketed versus 99.9% contracted; 8 major incidents in 90 days | No SLA, no EU region, 31 of 102 models with undeclared precision | Serverless has no region guarantee; OpenRouter uptime 91 to 97% |

## Recommendations for Akamai

1. **Publish a serving contract per model** (precision, served context, engine, TTFT target at a
   stated concurrency, deprecation notice) and a 99.9% SLA on the serverless tier from launch.
2. **Make routing geography the product**: OpenAI-compatible gateway at the edge, region pinning
   for residency, KV-aware routing, and priced prefix caching compatible with DeepInfra's fields.
3. **Size the catalog to the RTX PRO 6000 fleet**, sell service tiers instead of engine knobs,
   price mid-pack rather than at parity, and offer an export path to LKE.

Detail in [section 4A](04a-product-management-brief.md). Evidence base: unauthenticated probes of each provider's API, DNS,
origin ASN, status page, and OpenAPI spec; vendor documentation, contracts, and pricing pages
(203 cited URLs checked on 2026-09-29); third-party benchmarks used with stated caveats.
