# DNS and CDN fingerprints

Resolved with dig at capture time. Network owner comes from an origin-ASN lookup
(Team Cymru whois, asn.txt). CDN and hosting labels come from the CNAME chain.
Where no ASN record exists, an address-prefix heuristic is used and marked as such.

| Provider | Host | Chain | Addresses | Origin ASN | Hosting fingerprint |
| --- | --- | --- | --- | --- | --- |
| akamai | api.linode.com | loadbal-api.rin1.linode.com -> api.linode.com.edgekey.net -> e26254.dsca.akamaiedge.net | 2 IPv4, 23.211.124.199 to 23.211.124.208 | AS20940 AKAMAI-ASN1 - Akamai International B.V., NL (US) | Akamai edge (edgekey/akamaiedge) |
| akamai | techdocs.akamai.com | techdocs.akamai.com.edgekey.net -> e185847.dscx.akamaiedge.net | 2 IPv4, 23.45.123.41 to 23.45.123.42 | AS20940 AKAMAI-ASN1 - Akamai International B.V., NL (US) | Akamai edge (edgekey/akamaiedge) |
| akamai | www.akamai.com | www.akamai.com.edgekey.net | 2 IPv4, 23.45.123.5 to 23.45.123.37 | AS20940 AKAMAI-ASN1 - Akamai International B.V., NL (US) | Akamai edge (edgekey/akamaiedge) |
| akamai | status.linode.com | 8dn0wstr1chc.stspg-customer.com | 4 IPv4, 108.138.94.17 to 108.138.94.107 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | Atlassian Statuspage (CloudFront) |
| baseten | inference.baseten.co | (direct A record) | 1 IPv4: 35.244.129.243 | AS396982 GOOGLE-CLOUD-PLATFORM - Google LLC, US (US) | none |
| baseten | api.baseten.co | (direct A record) | 3 IPv4, 16.145.45.198 to 44.226.28.245 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | none |
| baseten | docs.baseten.co | cname.vercel-dns.com | 2 IPv4, 66.33.60.130 to 76.76.21.61 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | Vercel (Next.js hosting) |
| baseten | www.baseten.co | cname.vercel-dns.com | 2 IPv4, 66.33.60.129 to 76.76.21.22 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | Vercel (Next.js hosting) |
| baseten | status.baseten.co | 8dp3vkb2h71c.stspg-customer.com | 4 IPv4, 143.204.160.2 to 143.204.160.96 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | Atlassian Statuspage (CloudFront) |
| deepinfra | api.deepinfra.com | (direct A record) | 14 IPv4, 38.101.151.13 to 38.101.151.30 | AS16581 DEEPINFRA-01 - Deep Infra Inc., US (US) | none |
| deepinfra | deepinfra.com | (direct A record) | 1 IPv4: 76.76.21.21 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | none |
| deepinfra | status.deepinfra.com | (direct A record) | 1 IPv4: 100.50.38.141 | AS14618 AMAZON-AES - Amazon.com, Inc., US (US) | none |
| nebius | api.studio.nebius.com | (direct A record) | 1 IPv4: 213.239.161.19 | AS214415 NebiusPA10 - Nebius B.V., NL (NL) | none |
| nebius | api.tokenfactory.nebius.com | (direct A record) | 1 IPv4: 213.239.161.19 | AS214415 NebiusPA10 - Nebius B.V., NL (NL) | none |
| nebius | docs.tokenfactory.nebius.com | cname.mintlify-dns.com -> cname.vercel-dns.com | 2 IPv4, 66.33.60.130 to 76.76.21.61 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | Mintlify docs (on Vercel); Vercel (Next.js hosting) |
| nebius | nebius.com | (direct A record) | 1 IPv4: 150.171.110.151 | AS8075 MICROSOFT-CORP-MSN-AS-BLOCK - Microsoft Corporation, US (US) | none |
| nebius | status.nebius.com | qtd87qzrvchh.stspg-customer.com | 4 IPv4, 52.85.129.52 to 52.85.129.111 | AS16509 AMAZON-02 - Amazon.com, Inc., US (US) | Atlassian Statuspage (CloudFront) |
