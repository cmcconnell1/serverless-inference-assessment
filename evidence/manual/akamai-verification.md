# Akamai manual verification

akamai.com returns 403 to scripted clients, so these facts were read from an interactive Chrome
session on 2026-09-29 03:46 UTC. Each capture file holds the URL, capture time, method, and the
full page text as rendered. Screenshots were not taken; the page text is the record.

| Item | Value in docs before check | Observed (verbatim) | Result | Capture |
| --- | --- | --- | --- | --- |
| RTX PRO 6000 hourly price | $3.00 (x1) | "RTX PRO 6000 Blackwell x1 $3.00", "x2 $6.00", "x4 $12.00", "x8 $24.00"; every row ends "Request access" | Match; add "Request access" | `akamai-pricing-20260929.txt` |
| RTX PRO 6000 regions | 20, "limited deployment availability" | "NVIDIA RTX PRO 6000 Blackwell Server Edition (limited deployment availability) Amsterdam, NL; Chennai, IN; Chicago, IL, US; Frankfurt, DE; Jakarta, ID; London, UK; Los Angeles, CA, US; Madrid, ES; Miami, FL, US; Mumbai, IN; Milan, IT; Newark, NJ, US; Osaka, JP; Paris, FR; Seattle, WA, US; Singapore, SG; Stockholm, SE; Tokyo, JP; Toronto, CA; Washington, DC, US." | Match (20) | `akamai-gpu-regions-20260929.txt` |
| Public per-token or serverless inference pricing | None found | Product page: "transparent pricing", "zero egress fees", feature list includes "Serverless functions"; no per-token, per-request, or per-second price. Pricing page: no token or inference line items. `/solutions/ai-inference` returns "Page Not Found" | Match: none published | `akamai-inference-cloud-product-20260929.txt`, `akamai-pricing-20260929.txt` |
| Serverless inference in development | Not in docs | Job posting: "owning reliability workstreams for Akamai's serverless inference platform ... GPU infrastructure, Kubernetes at scale, and AI inference workloads" | New fact | `akamai-serverless-inference-job-posting-20260929.txt` |
| Availability wording | Attributed to AI Grid | "Akamai Inference Cloud is available today for qualified enterprise customers." The sentence describes Inference Cloud, in the AI Grid release | Attribution fix | `akamai-ai-grid-press-release-20260929.txt` |
| Akamai cost-per-token claim | Not in docs | "Compared with H100 running similar workloads ... 28% lower cost per million tokens; Higher throughput (3,140 vs. 2,987 tokens/sec)" (1-card); "Nearly identical cost per token as H100/H200 class infrastructure" (2-card); "raw throughput starts to favor NVLink-based H100/H200 systems by roughly 30% to 50%" (4-card) | New fact; reconcile with docs 04a | `akamai-gpu-card-counts-blog-20260929.txt` |
| Search `site:akamai.com "per million tokens"` | n/a | Two blog posts (cost modeling, GPU card counts); no product price list | No per-token price | `akamai-search-per-million-tokens-20260929.txt` |
| Search `site:akamai.com "serverless inference"` | n/a | Glossary pages, a 2026-07-23 video on "roadmap investment in a serverless inference platform", job postings | Roadmap, not product | `akamai-search-serverless-inference-20260929.txt` |
