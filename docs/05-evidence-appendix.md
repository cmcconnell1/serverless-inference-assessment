# 5. Evidence Appendix

Two classes of evidence back the analysis: first-hand captures produced by the scripts in this
repository, and public documents fetched on 2026-09-28, with pages that block scripted clients
read in a browser on 2026-09-29. The per-document source lists sit at the
end of [docs 1](01-product-positioning-and-messaging-audit.md), [docs 2](02-technical-architecture-and-engine-mechanics.md),
[docs 3](03-developer-experience-dx-and-api-surface-evaluation.md), and [docs 4a](04a-strategic-output-product-management-brief.md). This appendix indexes the
captures and consolidates the numeric facts the battlecard depends on.

## Capture index

| Capture | Command | What it shows |
| --- | --- | --- |
| `evidence/probes/<provider>/{models,noauth,badkey,options,notfound}.{headers,body,meta}` | `scripts/probe_providers.sh` | HTTP status, error body, and headers for unauthenticated and invalid-key requests on the OpenAI-compatible route of each provider |
| `evidence/probes/baseten/openapi.body` | GET `https://api.baseten.co/v1/spec` | Baseten management API specification, 160 paths |
| `evidence/probes/deepinfra/openapi.body` | GET `https://api.deepinfra.com/openapi.json` | DeepInfra full API specification, 140 paths |
| `evidence/probes/nebius/openapi.body` | GET `https://api.studio.nebius.com/openapi.json` | Nebius inference API specification, 37 paths, version `20260928-144ca2fd4` |
| `evidence/probes/akamai/openapi.body` | GET raw `linode/linode-api-docs` `openapi.json` | Linode API v4.215.0 specification, 308 paths |
| `evidence/probes/deepinfra/public_models.body` | GET `https://api.deepinfra.com/models/list` | 385 catalog entries with quantization, deprecation, replacement, partner flag, tier pricing |
| `evidence/probes/deepinfra/models.body` | GET `https://api.deepinfra.com/v1/openai/models` | 187 OpenAI-style model objects with metadata |
| `evidence/probes/deepinfra/live_metrics.body` | GET `https://api.deepinfra.com/v1/metrics/live` | Platform-wide tokens/s, TTFT, requests/s |
| `evidence/probes/nebius/dedicated_templates.body` | GET `https://api.tokenfactory.nebius.com/v0/dedicated_endpoints/templates` | 43 templates, 48 flavors, quantization and GPU by region |
| `evidence/probes/{baseten,nebius,akamai}/status{,_incidents}.body` | Statuspage `summary.json` and `incidents.json` | Components and the 50 most recent incidents |
| `evidence/probes/akamai/regions.body` | GET `https://api.linode.com/v4/regions` | 33 regions with capability flags |
| `evidence/probes/akamai/{llms_txt,agent_skills}.body` | GET techdocs `llms.txt` and `.well-known/agent-skills/index.json` | Machine-readable docs discovery on Akamai techdocs |
| `evidence/probes/<provider>/dns.txt` | `dig` A, AAAA, CNAME | Resolution chains for API, docs, marketing, and status hosts |
| `evidence/probes/<provider>/asn.txt` | `whois -h whois.cymru.com " -v <ip>"` | Origin ASN and registrant for every resolved address |
| `evidence/probes/<provider>/timing.txt` | `curl -w` timing variables, 9 samples per URL | DNS, TCP connect, TLS, and TTFB per inference host from one vantage point |
| `evidence/probes/<provider>/*.meta` `body_sha256` | `shasum -a 256` at capture | Hash of each body as received, before character normalization |
| `evidence/derived/*.md` | `scripts/summarize_probes.py` | Tables derived from the captures above |

## Key numeric facts

| Fact | Value | Date | Source |
| --- | --- | --- | --- |
| Baseten incidents, last 90 days | 35 (27 minor, 8 major) | 2026-09-29 | status.baseten.co incidents API, [derived](../evidence/derived/status-incidents.md) |
| Baseten Model APIs major-incident minutes, 90 days | 299 | 2026-09-29 | same |
| Baseten contractual SLA | 99.9% monthly, 40% credit cap | 2025-09-15 document | https://www.baseten.co/service-level-agreement/ |
| Baseten marketed uptime | 99.99% | 2026-09-28 | https://www.baseten.co/ |
| Baseten Series F | $1.5B, up to $13B valuation | 2026-06-22 | https://www.baseten.co/blog/announcing-our-series-f/ |
| Baseten H100 and B200 dedicated | $6.50/h and $9.98/h (from per-minute list) | 2026-09-28 | https://www.baseten.co/pricing/ |
| Baseten GLM-5.3 Model API | $1.40 in, $0.14 cached, $4.40 out per 1M | 2026-09-28 | same |
| DeepInfra active text models, deprecated, partner-proxied | 102, 123, 26 | 2026-09-29 | `/models/list`, [derived](../evidence/derived/deepinfra-catalog.md) |
| DeepInfra quantization declared (active text) | fp8 42, fp4 17, bf16 10, fp16 2, none 31 | 2026-09-29 | same |
| DeepInfra service tiers | Flex 0.8x, Priority 1.5x, batch 0.8x | 2026-06 to 07 | blogs cited in docs 2; catalog `rate_per_service_tier_*` |
| DeepInfra explicit cache write | 1.25x (5 min), 2.0x (1 h); granularity 1,024 tokens (GLM-5.2, DeepSeek V4 Flash), 1,536 (Kimi K3), 8,192 (Nemotron 3 Ultra) | 2026-08-05 | catalog `rate_per_explicit_cache_write_token` |
| DeepInfra live platform TTFT | 0.417 s and 0.421 s (about 4,200 req/s, 39.7M tok/s) | 2026-09-29 18:21:52 and 18:22:22 UTC | `/v1/metrics/live`, two samples 30 s apart |
| DeepInfra B200 and B300 | $3.69/h and $4.89/h | 2026-09-28 | https://deepinfra.com/pricing |
| DeepInfra Series B | $107M | 2026-05-04 | https://deepinfra.com/blog/deepinfra-series-b |
| DeepInfra data centers | 8 US plus Toronto | 2026-07-08 | GlobeNewswire release cited in docs 2 |
| Nebius Statuspage components and groups | 161 components, 7 region groups | 2026-09-29 | status.nebius.com summary API |
| Nebius incidents titled Token Factory | 8 between 2026-02-18 and 2026-07-01 (12 when counted by component tag, latest 2026-08-19) | 2026-09-29 | status.nebius.com incidents API |
| Nebius dedicated templates | 43 templates; flavors fp8 33, fp16 8, fp4 4, int4 2, bf16 1 | 2026-09-29 | templates capture, [derived](../evidence/derived/openapi-surface.md) |
| Nebius GPU by region (templates) | H200 in us-central1 (41 flavors), H100 in eu-north1 (20), L40S in eu-north1 (6) | 2026-09-29 | same |
| Nebius edge TTFB p50 | 100 ms Germany, 217 ms US Central, 446 ms Sao Paulo, 513 ms Tokyo | 2026-09-28 | https://llmlatency.dev/provider/nebius |
| Nebius OpenRouter 30-day uptime | 96.94% gpt-oss-120b; 91.38% Qwen3-235B | 2026-09-28 | OpenRouter endpoints API |
| Nebius serverless SKUs removed | 11 (June 22) plus 10 (Aug 31) | 2026 | deprecation notices |
| Nebius Q2 2026 revenue and AI cloud ARR | $582.3M and $3.0B | 2026-08-12 | Q2 2026 shareholder letter |
| Akamai RTX PRO 6000 | $3.00/GPU-h list (x1; x2 $6.00, x4 $12.00, x8 $24.00), 96 GB GDDR7, 20 regions ("limited deployment availability"), all plans "Request access" | 2026-09-29 browser capture, [manual](../evidence/manual/akamai-verification.md) | https://www.akamai.com/cloud/pricing/north-america (blocks scripted clients) and https://techdocs.akamai.com/cloud-computing/docs/gpu-compute-instances |
| Nebius AI Cloud on-demand GPU-hour | RTX PRO 6000 $1.80; H100 $3.85 ($4.50 second column); B200 $7.15 | 2026-09-29 | https://nebius.com/prices |
| Output tokens/s per GPU, Llama 3.3 70B, 1000/1000 | RTX PRO 6000 1,724 (FP4); B200 6,920 (FP4); H100 2,209 (FP8) | 2026-09-21 | https://nvidia.github.io/TensorRT-LLM/latest/developer-guide/perf-overview.html |
| Akamai regions with GPU capability | 22 of 33 | 2026-09-29 | `/v4/regions` capture, [derived](../evidence/derived/akamai-regions.md) |
| Inference ingress origin ASN | Baseten AS396982 (Google Cloud); DeepInfra AS16581 (own); Nebius AS214415 (own, NL); Akamai AS20940 | 2026-09-29 | `asn.txt`, [derived](../evidence/derived/dns-cdn.md) |
| Connection TTFB p50, unknown route, one US vantage point | Baseten 106 ms, DeepInfra 112 ms, `api.linode.com` 164 ms, Nebius 465 ms | 2026-09-29 18:21 to 18:23 UTC | `timing.txt`, [derived](../evidence/derived/latency.md) |
| Akamai edge locations | 4,400+ | 2026-03-16 | AI Grid press release |
| Artificial Analysis gpt-oss-120b TTFT | Baseten 0.19 s, DeepInfra 0.69 s, Nebius 0.94 s | 2026-09-28 | https://artificialanalysis.ai/models/gpt-oss-120b/providers |
| Paired GLM 5.3 Flash test, e2e p50 | Baseten 331 ms, DeepInfra 1,827 ms, Nebius 1,451 ms | 2026-09-03 | https://github.com/openbenchmarks-labs/inference |
| Availability budgets | 99.99% = 4.4 min per 30 days; 99.9% = 43.8 min | constant | https://uptime.is/99.99 |

## Observed header and error-body fingerprints

| Provider | Route | Status | Body | Distinguishing headers |
| --- | --- | --- | --- | --- |
| Baseten | POST chat, no key | 401 | `{"error":"please check the api-key you provided"}` | `via: 1.1 google`, `alt-svc: h3` |
| Baseten | POST chat, bad key | 403 | same | same |
| Baseten | GET unknown route | 405 | empty | same |
| Baseten | GET management, no key | 403 | `{"code": "PERMISSION_DENIED", "message": "Authorization error"}` | `server: gunicorn` |
| DeepInfra | POST chat, no key | 401 | `{"error":{"message":"missing API key","type":"invalid_request_error","param":null,"code":"invalid_api_key"}}` | `server: uvicorn`, `www-authenticate: Bearer` |
| DeepInfra | POST native inference, no key | 401 | `{"detail":"missing API key"}` | same |
| DeepInfra | GET unknown route | 404 | `{"detail":"Not Found"}` | `server: uvicorn` only |
| Nebius | POST chat, no key | 401 | `{"detail":"Couldn't authenticate. Reason: token is not present"}` | `x-request-id`, `access-control-allow-origin: *`, `vary: Origin` |
| Nebius | POST chat, bad key | 401 | `{"detail":"Couldn't authenticate. Reason: Unable authenticate"}` | same |
| Nebius | GET `/docs` | 200 | Swagger UI page referencing fastapi.tiangolo.com | same |
| Akamai (Linode) | GET profile, no key | 401 | `{"errors": [{"reason": "Invalid Token"}]}` | `Retry-After: 60`, `access-control-allow-origin: *` |
| Akamai (Linode) | GET unknown route | 404 | `{"errors": [{"reason": "Not found"}]}` | `access-control-allow-origin: *`; no `Retry-After` or rate-limit headers |
| Akamai (techdocs) | HEAD docs | 301 | none | `link: rel="api-catalog"`, `rel="agent-skills"`, `x-ratelimit-limit: 100` |
| Akamai (www) | HEAD marketing | 403 to a scripted client | HTML | `X-Akam-SW-Version`, `akaas_production` cookie, mPulse `expect-ct` |

## Third-party sources and their caveats

| Source | Used for | Caveat |
| --- | --- | --- |
| Artificial Analysis provider pages | TTFT, throughput, blended price | 10k-token default input; reasoning-model "latency" includes thinking; provider coverage varies by model |
| openbenchmarks-labs/inference | Paired-request latency and failure rate | Single model (GLM 5.3 Flash), concurrency 1, 600 requests |
| OpenRouter endpoints API | 30-day uptime per provider endpoint | Reflects OpenRouter's traffic and health checks only |
| llmlatency.dev | Edge TTFB by region | Network-only measurement; no inference |
| CheckUpstream, StatusGator | Impact-declared uptime | Aggregators of vendor-declared status; not independent monitoring |
| Vendor blogs quoting competitor numbers (DeepInfra benchmarks, Spheron) | Cross-checks only | Flagged as competitor-authored wherever cited |
