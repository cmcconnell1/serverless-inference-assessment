# 6. Methodology and Limits

## Scope

Three providers in scope: Baseten, DeepInfra, Nebius Token Factory. Akamai Cloud (Linode API v4,
Inference Cloud, AI Grid) is the baseline for the overlap analysis. Cut-off date for all facts:
2026-09-28, except the probe captures (2026-09-29 18:21 to 18:23 UTC) and the Akamai and Nebius pages that block scripted clients, read in a browser on
2026-09-29 and recorded in `evidence/manual/`. The source check also ran on 2026-09-29. Every row
in [docs 5](05-evidence-appendix.md) carries its own date.

## Method

| Step | What was done | Output |
| --- | --- | --- |
| Public document review | Vendor docs, pricing pages, changelogs, terms and SLA documents, engineering blogs, press releases, investor letters, GitHub organizations, third-party benchmarks | Source lists at the end of docs 1 to 4a |
| Unauthenticated probes | `scripts/probe_providers.sh`: GET, POST with no key and with a fixed invalid key, OPTIONS, HEAD, and `dig` against API, docs, marketing, and status hosts; public OpenAPI specs and catalog endpoints | `evidence/probes/` |
| Network ownership and timing | Same script: origin-ASN lookup of every resolved address (Team Cymru whois); nine `curl` timing samples per inference host and URL; SHA-256 of every body as received | `asn.txt`, `timing.txt`, `.meta` |
| Derivation | `scripts/summarize_probes.py`: incident statistics (windows end at capture time), catalog statistics, DNS and ASN fingerprints, OpenAPI path lists, chat-parameter diff against the OpenAI request schema, connection latency | `evidence/derived/` |
| Synthesis | Claims paired with contract text and observed data; verdicts assigned as Supported, Partially supported, Unsupported, or Not claimed | docs 1 to 5 |

## Reproduction

```bash
make evidence                            # probe (about 90 seconds, no credentials) and summarize
make report                              # rebuild the brief and full-report PDFs if an input changed
./scripts/probe_providers.sh --debug     # also writes a support bundle under /var/tmp/akamai-validation/
```

`dist/serverless-inference-assessment-full-report-chris-mcconnell.pdf` is a build artifact of `docs/*.md`,
`evidence/derived/*.md`, `evidence/manual/browser-checked-urls.tsv` and
`evidence/probes/*/*.meta` (cover date range), `CHANGELOG.md` (cover version), and
`scripts/build_report.sh` with `scripts/report/*`. Those
are prerequisites of the target, so editing any of them makes the next `make report`
rebuild the PDF, and `make rebuild-report` forces a build.
The brief, `dist/serverless-inference-assessment-brief-chris-mcconnell.pdf`, is built the same way
from `brief/*.md` with the same cover, version, and styling, and no evidence appendix.

All scripts accept `-h` or `--help`. JSON captures are stored with non-ASCII characters escaped
(`\uXXXX`), so parsed values match the response exactly; `body_sha256` in each `.meta` file hashes
the bytes as received.

## What was not tested

| Not tested | Reason | Effect on conclusions |
| --- | --- | --- |
| Authenticated requests, streaming chunk shapes, `usage` objects, tool-call streaming | No accounts were created and no spend was incurred, per the assessment brief | Streaming and usage conformance rows rely on vendor docs, marked as such |
| Cold-start timing | Requires a paid dedicated deployment scaled to zero | Cold-start verdicts rely on vendor docs, case studies, and status history |
| TTFT and throughput | Requires keys and a controlled load generator | Third-party benchmarks used, with caveats listed in docs 5 |
| Multi-vantage latency | Probes ran from one US host | `latency.md` measures connection phases from one location only; geography claims rely on llmlatency.dev |
| DeepInfra incident history | The DeepInfra status page is a custom Next.js site without a public incident API | DeepInfra availability rows use its 90-day component summary and aggregator snapshots |
| Incidents older than the 50 most recent | Statuspage public API returns 50 incidents | Baseten's 90-day window is complete (oldest returned 2026-05-26); Nebius (2026-02-18) and Linode (2026-04-24) windows are complete for 90 days |
| Nebius price page and catalog | JavaScript-rendered behind login | Prices taken from Nebius cookbooks, the public templates API, and third-party trackers, each dated |

## Known limits of the evidence

- Status-page minutes are vendor-declared and measure incident duration, not customer-visible
  error rate. "Availability if major minutes were full downtime" is a bound, not a measurement.
- Origin ASN identifies the announcing network, not the physical site. An anycast address (Google front end, Akamai edge) terminates near the client regardless of where the GPU runs.
- OpenAPI specs describe what a vendor documents, not necessarily what the server enforces.
- The DeepInfra live metric is two samples, 30 s apart, of a platform-wide counter.
- Artificial Analysis and OpenRouter numbers change daily; the values are snapshots with dates.

## AI use, tooling, and review process

An AI coding assistant was used for source research, script writing, and first drafts. Scope,
method, and conclusions were set by the author, and nothing was accepted without a check against
primary evidence.

The assistant was also used to review current public Akamai technical publications
([State of the Internet: Apps, APIs, and DDoS 2026](https://www.akamai.com/site/en/documents/state-of-the-internet/2026/app-api-ddos-security-report-2026.pdf),
[AI Inference Efficiency](https://www.akamai.com/site/en/documents/white-paper/ai-inference-efficiency.pdf))
so this report's format stays consistent with them. Only a structural convention was adopted: the
Key insights page in docs 00. No Akamai logo, brand colors, typefaces, or text were reused. Company
and product names identify what was assessed and remain trademarks of their owners.

Review steps:

- Audited the draft line by line against the assessment brief before any changes, and approved
  the fix plan first.
- Cross-checked every number in the docs against the raw captures, then did it again after
  editing. The second pass found 11 more errors.
- Checked every cited URL (203) and 26 key quotes and prices against the live pages with
  `make check-sources`; results in `evidence/derived/source-check.md`.
- Read Akamai pricing, region, and product pages from an interactive Chrome session, because the
  site blocks scripted access; page text and findings are in `evidence/manual/`.

What the checks changed:

- DeepInfra and Nebius run their own networks (AS16581, AS214415). The earlier Cogent and
  Hetzner attributions came from guessing by IP prefix and were wrong.
- A paraphrase of Baseten's docs had been shown as a quote. It was reworded.
- The first latency comparison timed endpoints doing different amounts of work. Re-measured on
  equal terms, Akamai's lead over the others mostly disappeared.
- NVIDIA's throughput data showed the RTX PRO 6000 can't match DeepInfra's per-token price at
  list rates. Recommendation 3 was rewritten around that.
