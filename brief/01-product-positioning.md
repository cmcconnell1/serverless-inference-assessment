# 1. Product Positioning & Messaging Audit

## 1.1 Market narrative

| Vector | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Tagline | "Inference is everything" | "AI Inference: FAST, SIMPLE, RELIABLE, LOW-COST" | "Run open models at production scale" |
| Core frame | Inference engineering company: runtime, control plane (Truss, environments), and capacity brokered across 18 clouds and 87 clusters | Price and ownership company: owned GPUs in nine colocation sites, "from GPU hardware to API layer" | Vertically integrated neocloud: inference layer on Nebius-owned data centers, fine-tune and serve on one platform |
| Lead product | Dedicated Inference per GPU-minute; per-token Model APIs added May 2025 | Serverless per-token APIs | Serverless per-token plus Dedicated Endpoints (GA 2026-02-26) |
| Proof points | Named logos (Notion, Cursor, Writer), day-0 launches | Price tables, "close to five trillion tokens a week", OpenRouter supply share | Prosus "up to 26x cost reductions", Revolut, Sword Health |
| Where it is thin | "Cross-cloud high availability", yet 17 of 35 incidents in 90 days name a single cluster, region, cloud, or upstream | "Reliable" with no SLA; terms promise "commercially reasonable efforts" | "Production scale" serverless carries "no region guarantee"; the 99.9% SLA covers dedicated only |

Baseten sells engineering depth, DeepInfra sells unit price, Nebius sells owned capacity and
European residency. None sells proximity to the end user, the vector an edge network can own.

## 1.2 Target personas

| Dimension | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Economic buyer | VP Engineering or Head of ML Platform at an AI-native scale-up with revenue tied to latency | Founder or lead engineer at a token-volume product (agents, chat, aggregators) | Head of AI Platform or CTO at a European or regulated enterprise |
| Hands-on user | ML engineer comfortable with Truss and engine configuration | Application developer who swaps a base URL in the OpenAI SDK | Application developer (serverless); platform engineer (dedicated, post-training) |
| Buying trigger | Latency SLO on a custom or fine-tuned model | Bill shock on a closed-model API | Data residency mandate; fine-tune and serve on one platform |
| Deal blocker to exploit | Price: H100 $6.50/h, B200 $9.98/h list | No SLA, no EU region, no custom containers on serverless | Serverless is EU-anchored with no region guarantee |

## 1.3 Claims versus reality

| Claim | Baseten | DeepInfra | Nebius |
| --- | --- | --- | --- |
| "Instant" cold starts | **Partially supported.** "Blazing-fast cold starts", but the cold-start docs give no latency figure; about 10 s for small cached models, unquantified for 70B+; wake-up minutes billed | **Not claimed.** Warm shared pool; contention becomes a 429 or a Flex wait of up to 10 minutes instead of a cold start | **Unsupported for serverless.** Claim is "sub-second responses for interactive agents" (Fast flavor), but six serverless `-fast` SKUs were removed in June; holds only on dedicated endpoints with min replicas above zero |
| "99.99% availability" | **Unsupported.** Marketed 99.99%, contracted 99.9% with credits capped at 40%. Model APIs logged 299 major-incident minutes in 90 days against a 13 minute 99.99% budget | **Not claimed numerically.** No SLA; single-model outages of 8 h and 6 h in July with no remedy | **Partially supported.** 99.9% SLA on dedicated only, and only under contract; OpenRouter 30-day serverless uptime 91.4% to 96.9% |
| "Sub-second TTFT" | **Supported on TTFT, not on throughput.** Claim is "fastest runtime available": 0.19 s on gpt-oss-120b, fastest of the three; mid-pack on throughput (10 of 18) | **Holds on average, fails at the tail.** 0.69 s on gpt-oss-120b; p99 17 s in a paired test | **Unsupported.** 0.94 s on gpt-oss-120b, 0.99 to 2.33 s on reasoning models; 217 ms edge TTFB from US Central before inference starts |

TTFT figures are Artificial Analysis (10k-token input; reasoning-model figures include thinking
time, so they are an upper bound) and a 600-request paired test; edge TTFB is llmlatency.dev. Verbatim
claims, contract text, and incident data: [full report 1.3](../docs/01-product-positioning-and-messaging-audit.md#13-claims-versus-reality).
