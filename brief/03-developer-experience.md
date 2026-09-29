# 3. Developer Experience (DX) & API Surface Evaluation

## 3.1 API uniformity and OpenAI compatibility

| Element | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| Routes beyond chat | Anthropic Messages (beta); completions and embeddings on dedicated | Completions, embeddings, Responses, Anthropic Messages, files and batches | Completions, embeddings, Responses, rerank, fine-tuning |
| Chat schema versus OpenAI | No public schema | 31 parameters; 15 OpenAI parameters absent (`logit_bias`, `top_logprobs`, `parallel_tool_calls`); 11 extensions | 23 parameters; 13 absent (including `seed`); one extension (`extra_body`) |
| Error body | `{"error": "<string>"}`; 403 on a bad key where OpenAI returns 401 | OpenAI-shaped error object on the OpenAI route | FastAPI `{"detail": ...}` |
| Streaming | SSE `chat.completion.chunk`; usage chunk opt-in | SSE ending `data: [DONE]`; usage chunk on by default | SSE ending `data: [DONE]`; usage opt-in; reasoning under `reasoning` or `reasoning_content` |
| Custom headers | Full `x-ratelimit-*` set plus uncached-input split; `X-Baseten-Request-Id`; retry count header | No rate-limit or request-ID headers documented | Full `x-ratelimit-*` set plus dynamic-scale headers; `x-request-id` |
| Default `max_tokens` | 4,096 | Docs conflict: 16,384 or 65,536 | 8,192 |

An OpenAI SDK client works on all three for content and tool calls. Reasoning fields, error
bodies, and default output caps diverge, so a ported workload changes behavior unless
`max_tokens` is explicit. Error and header captures are unauthenticated; streaming rows come from
documentation. Detail: [full report 3.1](../docs/03-developer-experience-dx-and-api-surface-evaluation.md#31-api-uniformity-and-openai-compatibility).

## 3.2 Control plane versus data plane

| Dimension | Baseten | DeepInfra | Nebius Token Factory |
| --- | --- | --- | --- |
| CLI | Truss (packaging) plus Baseten CLI | `deepctl` (Rust) | None for inference |
| Deployment artifact | Truss `config.yaml` or a custom Docker image; weights from HF, S3, GCS, R2, Azure | Hugging Face repo ID plus GPU type; no custom container on serverless | Template plus flavor through the API; custom weights in beta |
| Management API | 160 paths; environments, rolling promotion, CI action | 140 paths | 37 paths |
| TTFT and tokens/s | Per deployment | Platform-wide only | Dedicated endpoints only |
| Queue delay | Async queue time and size | Not exposed | Not exposed |
| Metrics export | Prometheus (beta), OTLP, tracing | None | Prometheus federation |

Baseten is a control plane with engines attached; DeepInfra and Nebius are data planes with a
thin control surface. Only Baseten shows queue delay to the developer.

## 3.3 Architectural overlap with Akamai Cloud

| Layer | Shared lineage | Akamai Cloud |
| --- | --- | --- |
| Serving engine | vLLM at all three; NVIDIA Dynamo at Baseten and DeepInfra | vLLM, Dynamo, KServe, NIM on LKE: same engines |
| Orchestration | Kubernetes at Baseten and Nebius | LKE (Cilium) |
| API dialect | OpenAI at all three; FastAPI `{"detail"}` errors at DeepInfra and Nebius | Linode API uses `{"errors": [...]}` and capitalized `X-RateLimit-*` headers: no overlap |
| Ingress | No CDN at any of the three | Akamai edge on API, docs, and marketing hosts |
| Docs and status | Mintlify (Baseten, Nebius); Atlassian Statuspage (Baseten, Nebius) | ReadMe with `llms.txt`; Atlassian Statuspage |
| Hosting relationship | None found with Akamai or Linode | Not applicable |

Engine parity is free. The data plane must speak the OpenAI dialect while the control plane keeps
Linode conventions, and that seam must be documented. Ingress is where Akamai can lead, provided
the gateway runs at the edge. Lineage diagram and fingerprints:
[full report 3.3](../docs/03-developer-experience-dx-and-api-surface-evaluation.md#33-architectural-overlap-with-akamai-cloud).
