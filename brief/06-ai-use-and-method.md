# 6. AI Use and Method

## How AI was used

An AI coding assistant was used for source research, script writing, and first drafts. Scope,
method, and conclusions were set by the author, and nothing was accepted without a check against
primary evidence. The assistant was also used to review current public Akamai technical
publications so the report format stays consistent with them; only one structural convention was
adopted (the Key insights page), and no Akamai logo, brand colors, typefaces, or text were reused.

Review steps:

- Audited the draft line by line against the assessment brief before any changes.
- Cross-checked every number against the raw captures, then again after editing. The second pass
  found 11 more errors.
- Checked all 203 cited URLs and 26 key quotes and prices against the live pages.
- Read Akamai and Nebius pages that block scripted access in an interactive browser session.

What the checks changed:

- DeepInfra and Nebius run their own networks (AS16581, AS214415); earlier hosting attributions
  guessed from IP prefixes were wrong.
- A paraphrase of Baseten's docs had been shown as a quote and was reworded.
- The first latency comparison timed endpoints doing different amounts of work. Re-measured on
  equal terms, Akamai's lead mostly disappeared.
- NVIDIA throughput data showed the RTX PRO 6000 cannot match DeepInfra's per-token price at list
  rates; Recommendation 3 was rewritten around that.

## Method and limits

| Evidence | Limit |
| --- | --- |
| Unauthenticated probes of API, DNS, origin ASN, status pages, OpenAPI specs, and catalogs; reproducible with `make evidence` in about 90 seconds, no credentials | No accounts and no spend, per the brief: streaming and usage rows rely on vendor docs |
| Vendor documentation, contracts, SLA terms, pricing pages, engineering blogs | Cold-start timing not measured; verdicts rely on docs, case studies, and status history |
| Third-party benchmarks (Artificial Analysis, OpenRouter, llmlatency.dev) | TTFT and throughput are dated snapshots, not controlled measurements |
| Connection timing, nine samples per host | One US vantage point only |

Scope, reproduction steps, and what was not tested: [full report 6](../docs/06-methodology.md).
Capture index and key numeric facts: [full report 5](../docs/05-evidence-appendix.md).
