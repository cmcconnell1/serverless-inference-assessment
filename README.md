# Serverless Inference Assessment: Baseten, DeepInfra, Nebius Token Factory
Prepared by Chris McConnell.

Facts dated 2026-09-28, except probe captures (2026-09-29) and pages that block scripted clients, read in a browser on 2026-09-29.

Two PDFs, same design, built from this repository with `make report`:

| PDF | Content |
| --- | --- |
| [Brief](dist/serverless-inference-assessment-brief-chris-mcconnell.pdf) | Each deliverable answered in short form, the completed battlecard, and the AI-use summary; cites full-report sections for detail. Source: `brief/` |
| [Full report](dist/serverless-inference-assessment-full-report-chris-mcconnell.pdf) | Complete analysis, citations, evidence appendix, and methodology. Source: `docs/` |

## Summary

- All three competitors run open engines (vLLM at all three; Baseten and DeepInfra also SGLang,
  TensorRT-LLM, and NVIDIA Dynamo) and speak the same OpenAI dialect. Differentiation sits in transparency, routing geography,
  and pricing tiers, not in the engine.
- Baseten sells inference engineering depth: exposed engine knobs, 18-cloud capacity brokering,
  fastest shared-API TTFT (0.19 s on gpt-oss-120b), and premium prices. Its marketed 99.99% uptime
  is one order of magnitude above its 99.9% contractual SLA, and the status API shows 8 major
  incidents in 90 days.
- DeepInfra sells the lowest list price on owned GPUs and its own network (AS16581), three
  service tiers on the same weights, and the most complete public API surface (OpenAPI spec,
  per-model quantization, live metrics). It carries no SLA, no EU region, and serves 17 of 102
  active text models at FP4 with 31 undeclared.
- Nebius Token Factory sells owned European capacity, a fine-tune-and-serve loop, and a 99.9% SLA
  on dedicated endpoints. Serverless answers from one NL-registered address with "no region
  guarantee", has no cached-input pricing, lost 21 SKUs in three months, and shows 91 to 97%
  uptime on OpenRouter.
- No public Akamai per-token price list was found; job postings show a serverless inference
  platform in development. The RTX PRO 6000 fleet ($3.00 per GPU-hour list, request access, 20 regions, 96 GB per card, no NVLink) reaches about 0.25x B200 throughput, so at list
  price its cost per token sits above DeepInfra's retail price on dense 70B models. The
  recommendation is to compete on a published serving contract and edge routing with region
  pinning, price mid-pack rather than at parity, and offer an export path to LKE.

## Related project: inference-bench

This repository analyzes existing evidence and runs no inference workloads.
[inference-bench](https://github.com/cmcconnell1/inference-bench) runs the benchmark itself
and analyzes its own results.

| | This repository | [inference-bench](https://github.com/cmcconnell1/inference-bench) |
| --- | --- | --- |
| Method | Analyzes public evidence: HTTP and DNS probes, status pages, model catalogs, published third-party benchmarks | Provisions an Akamai Cloud GPU instance with Terraform, drives each serving engine with guidellm at fixed concurrency, then analyzes the results |
| Compares | Providers: Baseten, DeepInfra, Nebius Token Factory, against Akamai Cloud | Serving engines: vLLM, SGLang, TGI, Ollama, llama.cpp, NVIDIA NIM |
| Output | Assessment docs and one PDF report | Latency, throughput, 1 Hz GPU telemetry, and cost per 1M output tokens per run, plus a Markdown report with charts |
| Cost to run | None; no credentials | GPU hours on a Linode account (default RTX 4000 Ada, $0.52/h) |

The cost-per-token figures in [docs 4a](docs/04a-strategic-output-product-management-brief.md) rest on
NVIDIA-published throughput. inference-bench is the harness to measure that on Akamai GPUs. It is
validated offline (2026-09-27) but not yet run against a live account, so no measured results feed
this assessment.

## Documents

| Document | Assessment deliverable |
| --- | --- |
| [0. Executive Brief](docs/00-executive-brief.md) | Key insights, competitor snapshot, recommendations, evidence base |
| [1. Product Positioning & Messaging Audit](docs/01-product-positioning-and-messaging-audit.md) | Market narrative, target personas, claims versus reality |
| [2. Technical Architecture & Engine Mechanics](docs/02-technical-architecture-and-engine-mechanics.md) | Model catalog, availability, and marketing; engines, batching mechanics, TGI status; memory and KV cache; routing, ASN, and measured latency |
| [3. Developer Experience (DX) & API Surface Evaluation](docs/03-developer-experience-dx-and-api-surface-evaluation.md) | OpenAI conformance, streaming format, SDKs, default runtime settings, control plane versus data plane, architectural overlap with Akamai Cloud |
| [4. Strategic Output, Part A: Product Management Brief](docs/04a-strategic-output-product-management-brief.md) | Three roadmap recommendations with evidence, cost-per-token economics, metrics, risks, and sequencing |
| [4. Strategic Output, Part B: Solutions Engineering Battlecard](docs/04b-strategic-output-solutions-engineering-battlecard.md) | Completed template table, one-line positioning, extended rows, landmines, and traps |
| [5. Evidence Appendix](docs/05-evidence-appendix.md) | Capture index, key numeric facts, header fingerprints, third-party caveats |
| [6. Methodology and Limits](docs/06-methodology.md) | Scope, method, reproduction, what was not tested, [AI use, tooling, and review process](docs/06-methodology.md#ai-use-tooling-and-review-process) |

## Evidence

Everything under `evidence/` was produced by the scripts below with no credentials and no spend.

| Path | Content |
| --- | --- |
| [evidence/probes/](evidence/README.md) | Raw HTTP headers, bodies, status-page JSON, OpenAPI specs, catalog endpoints, DNS chains, origin ASNs, and connection timings for Baseten, DeepInfra, Nebius, and Akamai |
| [evidence/derived/api-surface.md](evidence/derived/api-surface.md) | Status codes, error bodies, and headers per probe |
| [evidence/derived/dns-cdn.md](evidence/derived/dns-cdn.md) | Resolution chains, origin ASN, and hosting fingerprints |
| [evidence/derived/latency.md](evidence/derived/latency.md) | DNS, TCP, TLS, and TTFB per inference host from one vantage point |
| [evidence/derived/status-incidents.md](evidence/derived/status-incidents.md) | Components and 30 and 90 day incident statistics |
| [evidence/derived/deepinfra-catalog.md](evidence/derived/deepinfra-catalog.md) | Quantization, freshness, partner models, tier and cache pricing |
| [evidence/derived/openapi-surface.md](evidence/derived/openapi-surface.md) | Path lists, chat-parameter diff versus OpenAI, Nebius templates |
| [evidence/derived/akamai-regions.md](evidence/derived/akamai-regions.md) | Linode regions with GPU and Kubernetes capability |
| [evidence/derived/source-check.md](evidence/derived/source-check.md) | Reachability of every cited URL and presence of key quotes on the live pages |
| [evidence/manual/akamai-verification.md](evidence/manual/akamai-verification.md) | Browser checks of Akamai facts the site blocks from scripts |

## Build and reproduce

```bash
make help        # list targets
make evidence    # probe providers (about 90 seconds, network) and regenerate derived tables
make summarize   # regenerate derived tables from existing captures (offline)
make check-sources  # check cited URLs and key quotes against live pages (network)
make report      # rebuild the brief and the full report, each only if its inputs changed
make rebuild-report  # rebuild both PDFs unconditionally
```

Both PDFs are build artifacts, not source files. `make report` rebuilds each one only when one
of its inputs is newer than the PDF; otherwise it prints that both are up to date. Run
`make all` to regenerate the derived tables from the captures and then rebuild both PDFs.
`./scripts/build_report.sh --variant brief` or `--variant full` builds one directly.

Inputs checked by `make report` (`BRIEF_SRC`, `REPORT_SRC`, and `COMMON_SRC` in the `Makefile`):

| Input | PDF | Role |
| --- | --- | --- |
| `brief/[0-9][0-9]*.md` | Brief | Chapters, in file-name order |
| `docs/[0-9][0-9]*.md` | Full report | Chapters, in file-name order |
| `evidence/derived/*.md` | Full report | Evidence tables |
| `evidence/manual/browser-checked-urls.tsv`, `evidence/probes/*/*.meta`, `evidence/derived/source-check.md` | Both | Cover evidence date range |
| `CHANGELOG.md` | Both | Cover version (first `## [x.y.z]` heading) |
| `scripts/build_report.sh`, `scripts/report/*`, `scripts/report/fonts/*` | Both | Assembly, pandoc filters, stylesheet, fonts, PDF metadata |

Files not checked, because the PDF build does not read them: `README.md`,
`evidence/README.md`, `evidence/quote-checks.tsv`, `evidence/manual/*.txt`,
`evidence/manual/akamai-verification.md`, the `Makefile`, and the probe, summary, and
source-check scripts. Editing these never triggers a rebuild.

Force a clean rebuild regardless of timestamps:

```bash
make rebuild-report     # run the build script directly
make -B report          # treat every input as changed
make clean report       # delete dist/, then build

stat -f '%Sm %N' dist/*.pdf   # confirm the PDF timestamp (macOS; GNU: stat -c '%y %n')
make -q dist/serverless-inference-assessment-full-report-chris-mcconnell.pdf; echo $?   # 0: up to date, 1: stale
```

`make` reads files from disk. An edit left unsaved in an editor does not trigger a rebuild.

Each script accepts `-h` for usage and `--debug` for a support bundle under `/var/tmp/akamai-validation/`.

| Requirement | Used by |
| --- | --- |
| bash, curl, dig, whois, shasum, Python 3.9+ (standard library only) | `scripts/probe_providers.sh`, `scripts/summarize_probes.py` |
| pandoc 3.x, mermaid-cli (`mmdc`), Google Chrome or Chromium, uv | `scripts/build_report.sh` (uv runs pikepdf 10.15.0 to number the contents and rewrite PDF metadata) |

## Repository layout

```
README.md
CHANGELOG.md
Makefile
brief/                Brief chapters: deliverables 1 to 4B in short form, AI use and method
docs/                 Full report: deliverables 0 to 4b plus appendix and methodology
evidence/probes/      Raw captures, one directory per provider
evidence/derived/     Tables generated from the captures
scripts/              probe_providers.sh, summarize_probes.py, check_sources.py, build_report.sh
scripts/report/       Assembly, pandoc filters, print stylesheet, TOC page numbers, PDF metadata rewrite
scripts/report/fonts/ IBM Plex Sans and Mono (SIL OFL 1.1, license in OFL.txt), embedded in the PDF
dist/                 Built PDFs: brief and full report
```
