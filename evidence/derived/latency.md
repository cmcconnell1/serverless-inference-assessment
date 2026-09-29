# Connection-phase latency

Source: timing.txt per provider, written by the probe script. Each row is an
unauthenticated GET that returns before any inference, so the numbers measure DNS,
TCP connect, TLS handshake, and gateway time-to-first-byte from one vantage point.
They are a floor under TTFT from that location, not a TTFT measurement.
Compare hosts on the unknown-route rows: each returns an error with minimal server work.
The model and region list rows include the time to build a full response body.

Vantage: unspecified (timezone MDT).

| Provider | URL | Remote IP | Samples | HTTP | Connect p50 (ms) | TLS done p50 (ms) | TTFB p50 (ms) | TTFB min to max (ms) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| akamai | https://api.linode.com/v4/this-route-does-not-exist | 23.211.124.199 | 9 | 404 | 36 | 71 | 164 | 139 to 232 |
| akamai | https://api.linode.com/v4/regions | 23.211.124.199 | 9 | 200 | 36 | 71 | 385 | 367 to 509 |
| baseten | https://inference.baseten.co/v1/this-route-does-not-exist | 35.244.129.243 | 9 | 405 | 23 | 46 | 106 | 98 to 117 |
| baseten | https://inference.baseten.co/v1/models | 35.244.129.243 | 9 | 401 | 22 | 44 | 105 | 95 to 115 |
| deepinfra | https://api.deepinfra.com/v1/openai/this-route-does-not-exist | 38.101.151.16 | 9 | 404 | 36 | 74 | 112 | 108 to 477 |
| deepinfra | https://api.deepinfra.com/v1/openai/models | 38.101.151.16 | 9 | 200 | 36 | 74 | 209 | 197 to 802 |
| nebius | https://api.tokenfactory.nebius.com/v1/this-route-does-not-exist | 213.239.161.19 | 9 | 404 | 142 | 285 | 465 | 464 to 467 |
| nebius | https://api.tokenfactory.nebius.com/v1/models | 213.239.161.19 | 9 | 401 | 142 | 286 | 427 | 422 to 429 |
