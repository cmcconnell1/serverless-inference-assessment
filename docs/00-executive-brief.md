# 0. Executive Brief

Serverless inference landscape: Baseten, DeepInfra, Nebius Token Factory. Facts dated 2026-09-28,
except probe captures (2026-09-29) and pages that block scripted clients, read in a browser on 2026-09-29.
Detail and sources: [docs 1](01-product-positioning-and-messaging-audit.md) to
[docs 6](06-methodology.md). A short companion brief,
`serverless-inference-assessment-brief-chris-mcconnell.pdf`, answers each deliverable in short
form; this report holds the evidence and detail.

## Key insights

- **The engine layer is commoditized: all 3 competitors serve on open engines, and all 3 run vLLM.**
  - Baseten and DeepInfra run vLLM, SGLang, TensorRT-LLM, and NVIDIA Dynamo; Nebius runs vLLM in
    production, with TensorRT-LLM in at least one proof of concept. All sit behind an
    OpenAI-compatible API, and Akamai's own LKE stack already offers vLLM and NVIDIA Dynamo
    ([docs 3](03-developer-experience-dx-and-api-surface-evaluation.md)).
  - Differentiation sits in what is disclosed, where requests land, and how capacity is priced
    ([docs 2](02-technical-architecture-and-engine-mechanics.md)).
- **Marketing outruns contracts: Baseten markets 99.99% uptime against a 99.9% SLA.**
  - DeepInfra markets "reliable" with no SLA.
  - Nebius markets sub-second TTFT that third-party data does not show on its serverless tier
    ([docs 1](01-product-positioning-and-messaging-audit.md)).
- **None of the 3 places GPUs by user geography.**
  - DeepInfra answers from one /24 on its own network in the US.
  - Nebius answers from a single address on its own network in NL.
  - Baseten rents Google's front end, then hops to whichever cloud has capacity.
- **Akamai's opening is a published serving contract plus geography-aware routing, but the edge
  advantage is not automatic: 164 ms to first byte against 106 ms for Baseten.**
  - From one US vantage point, a minimal request to `api.linode.com` returns its first byte in
    164 ms, against 106 ms for Baseten's Google front end and 465 ms for Nebius
    ([latency](../evidence/derived/latency.md)).

## Competitor snapshot

| | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Sells | Inference engineering depth and multi-cloud capacity | Lowest list price on owned GPUs | Owned EU capacity, fine-tune and serve |
| Buyer | ML platform lead at an AI-native scale-up | Developer optimizing cost per token | Regulated or EU enterprise |
| Strength | Fastest shared-API TTFT (0.19 s, gpt-oss-120b); deepest engine controls | Priced prefix caching, three service tiers, fullest public API spec | 99.9% SLA on dedicated; EU residency on dedicated |
| Exploitable gap | 99.99% marketed versus 99.9% contracted; 8 major incidents in 90 days | No SLA, no EU region, 31 of 102 models with undeclared precision | Serverless has no region guarantee; OpenRouter uptime 91 to 97% |

## Recommendations for Akamai ([docs 4a](04a-strategic-output-product-management-brief.md))

1. **Publish a serving contract per model** (precision, served context, engine, TTFT target at a
   stated concurrency, deprecation notice) and a 99.9% SLA on the serverless tier from launch.
2. **Make routing geography the product**: OpenAI-compatible gateway at the edge, region pinning
   for residency, KV-aware routing, and priced prefix caching compatible with DeepInfra's fields.
3. **Size the catalog to the RTX PRO 6000 fleet** (20B to 120B class, MoE models with few active
   parameters), sell service tiers instead of engine knobs, and offer an export path to LKE. Do
   not lead with price: at list rates an RTX PRO 6000 produces a 70B-class token for about $0.48
   per million against about $0.15 on DeepInfra's B200s, and Nebius lists the same RTX PRO 6000 at $1.80 per GPU-hour against Akamai's $3.00. Price
   mid-pack and sell the contract.

## Evidence base

- Unauthenticated probes of each provider's API, DNS, origin ASN, status page, OpenAPI spec, and
  connection timing, reproducible with `make evidence` ([docs 6](06-methodology.md)).
- Vendor documentation, contracts, and pricing pages. All 203 cited URLs were checked for
  reachability on 2026-09-29, and 26 load-bearing quotes and prices were checked against the
  live pages.
- Third-party benchmarks (Artificial Analysis, OpenRouter, llmlatency.dev) used with their caveats
  ([docs 5](05-evidence-appendix.md)).
