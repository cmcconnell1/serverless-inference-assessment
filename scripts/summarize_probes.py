#!/usr/bin/env python3
"""summarize_probes.py

Derive citable evidence tables from the raw captures written by
scripts/probe_providers.sh. Reads evidence/probes/<provider>/* and writes
Markdown tables to evidence/derived/. Read-only against the network; no
HTTP calls are made here.

Outputs (evidence/derived/):
  api-surface.md        HTTP status, error schema and server fingerprints per probe
  dns-cdn.md            DNS chain and CDN or hosting fingerprint per hostname
  status-incidents.md   Status page components and incident statistics (30d, 90d)
  deepinfra-catalog.md  DeepInfra public catalog: quantization, freshness, pricing
  akamai-regions.md     Linode regions with GPU and LKE capability flags
  openapi-surface.md    Public OpenAPI specs: paths, chat parameter diff vs OpenAI, Nebius templates
  latency.md            Connection-phase timings (DNS, TCP, TLS, TTFB) per inference host

Incident windows are measured back from the capture time recorded in each
status_incidents.meta, not from the time this script runs, so re-running it
later reproduces the same numbers.

Usage: summarize_probes.py [-h] [-v] [--debug] [--probes DIR] [--out DIR]
"""

import argparse
import collections
import ipaddress
import json
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import tarfile
from datetime import datetime, timedelta, timezone

TOOL = "summarize_probes"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
PROBES = os.path.join(ROOT, "evidence", "probes")
OUT = os.path.join(ROOT, "evidence", "derived")
INTERESTING_HDRS = (
    "server", "via", "x-vercel-id", "x-vercel-cache", "cf-cache-status", "cf-ray",
    "www-authenticate", "retry-after", "x-ratelimit-limit", "x-ratelimit-remaining",
    "access-control-allow-origin", "access-control-allow-methods", "x-akam-sw-version",
    "x-request-id", "x-session-affinity", "alt-svc", "content-type", "link",
)
REF = {"99.99": 4.38, "99.95": 21.9, "99.9": 43.8, "99.5": 219.0}  # minutes per 30 days


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def read(path, default=""):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return default


def parse_meta(path):
    meta = {}
    for line in read(path).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def parse_headers(path):
    hdrs = {}
    for line in read(path).splitlines():
        if ":" in line and not line.startswith("HTTP/"):
            k, v = line.split(":", 1)
            hdrs.setdefault(k.strip().lower(), v.strip())
    return hdrs


ASCII_MAP = {
    "\u2014": ",", "\u2013": ",", "\u2011": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"',
    "\u201d": '"', "\u2026": "...", "\u00a0": " ", "\u00b7": "-", "\u25cf": "-", "\u2122": "(TM)",
    "\u3001": ",",
}


def ascii_clean(text):
    """Rewrite typographic substitutes to ASCII and drop format, symbol, and private-use characters.

    Letters in any script and the registered sign are kept; everything else outside ASCII is
    normalized so derived tables never carry hidden or decorative characters.
    """
    out = []
    for ch in str(text):
        if ord(ch) < 128:
            out.append(ch)
        elif ch in ASCII_MAP:
            out.append(ASCII_MAP[ch])
        elif ch.isalpha() or ch == "\u00ae":
            out.append(ch)
        # any other non-ASCII symbol, emoji, or format character is dropped
    return "".join(out)


def load_asn(prov):
    """Map IP to 'AS<n> <name>' from asn.txt (Team Cymru verbose whois lines)."""
    table = {}
    for line in read(os.path.join(PROBES, prov, "asn.txt")).splitlines():
        parts = [x.strip() for x in line.split("|")]
        if len(parts) >= 7 and parts[0].isdigit():
            table[parts[1]] = f"AS{parts[0]} {parts[6]} ({parts[3]})"
    return table


def capture_time(prov, probe):
    meta = parse_meta(os.path.join(PROBES, prov, probe + ".meta"))
    if meta.get("captured_utc"):
        return ts(meta["captured_utc"])
    return datetime.now(timezone.utc)


def md_escape(s):
    return ascii_clean(s).replace("|", "\\|").replace("\n", " ")


def ranked(counter):
    """Counter items by count descending, ties by key, so equal counts never reorder between runs."""
    return sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))


def api_surface(providers, verbose):
    rows = ["# API surface captures", "",
            "Generated from evidence/probes by scripts/summarize_probes.py. All requests were",
            "unauthenticated; the badkey probe sent a fixed invalid bearer token.", "",
            "| Provider | Probe | Method | URL | HTTP | Body (first 160 chars) | Notable headers |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for prov in providers:
        d = os.path.join(PROBES, prov)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".meta"):
                continue
            name = fn[:-5]
            meta = parse_meta(os.path.join(d, fn))
            hdrs = parse_headers(os.path.join(d, name + ".headers"))
            body = read(os.path.join(d, name + ".body")).strip()
            if body.startswith("<!DOCTYPE") or body.startswith("<html"):
                body = "(HTML page)"
            body = re.sub(r"\s+", " ", body)[:160]
            keep = [f"{k}: {v[:60]}" for k, v in hdrs.items() if k in INTERESTING_HDRS]
            rows.append("| %s | %s | %s | %s | %s | `%s` | %s |" % (
                prov, name, meta.get("method", ""), md_escape(meta.get("url", "")),
                meta.get("http_code", ""), md_escape(body) if body else "(empty)",
                md_escape("; ".join(keep))))
            if verbose:
                print(f"[api] {prov}/{name} -> {meta.get('http_code')}")
    return "\n".join(rows) + "\n"


def dns_cdn(providers, verbose):
    rows = ["# DNS and CDN fingerprints", "",
            "Resolved with dig at capture time. Network owner comes from an origin-ASN lookup",
            "(Team Cymru whois, asn.txt). CDN and hosting labels come from the CNAME chain.",
            "Where no ASN record exists, an address-prefix heuristic is used and marked as such.", "",
            "| Provider | Host | Chain | Addresses | Origin ASN | Hosting fingerprint |",
            "| --- | --- | --- | --- | --- | --- |"]
    fingerprints = [
        (r"akamaiedge\.net|edgekey\.net", "Akamai edge (edgekey/akamaiedge)"),
        (r"vercel-dns\.com", "Vercel (Next.js hosting)"),
        (r"mintlify-dns\.com", "Mintlify docs (on Vercel)"),
        (r"stspg-customer\.com", "Atlassian Statuspage (CloudFront)"),
        (r"cloudfront\.net", "Amazon CloudFront"),
        (r"cloudflare", "Cloudflare"),
    ]
    ip_hints = [
        (r"^35\.(19[0-9]|2[0-4][0-9])\.", "Google Cloud IP range"),
        (r"^34\.(2(0[8-9]|1[0-9]|2[0-3]))\.|^44\.|^54\.|^52\.|^3\.", "AWS IP range"),
        (r"^38\.101\.", "Cogent-announced range (self-hosted or colocation)"),
        (r"^213\.239\.", "Hetzner-announced range (EU, self-hosted or colocation)"),
        (r"^76\.76\.21\.|^66\.33\.60\.", "Vercel anycast"),
        (r"^150\.171\.", "Microsoft Azure Front Door range"),
        (r"^23\.|^2600:1405:", "Akamai edge IP range"),
    ]
    for prov in providers:
        asn = load_asn(prov)
        txt = read(os.path.join(PROBES, prov, "dns.txt"))
        for block in txt.split("== ")[1:]:
            host, _, body = block.partition(" ==")
            lines = [l for l in body.strip().splitlines() if l.strip()]
            cnames = []
            ips = []
            for l in lines:
                parts = l.split()
                if len(parts) >= 5 and parts[3] == "CNAME":
                    cnames.append(parts[4].rstrip("."))
                elif len(parts) >= 5 and parts[3] in ("A", "AAAA"):
                    ips.append(parts[4])
            chain = " -> ".join(dict.fromkeys(cnames)) if cnames else "(direct A record)"
            inf = set()
            for pat, label in fingerprints:
                if re.search(pat, " ".join(cnames)):
                    inf.add(label)
            owners = set()
            for ip in ips:
                if ip in asn:
                    owners.add(asn[ip])
                    continue
                for pat, label in ip_hints:
                    if re.search(pat, ip):
                        owners.add(label + " (prefix heuristic)")
            # Sorted: resolvers rotate A-record order, which would change the range on every run.
            v4 = sorted((ip for ip in set(ips) if ":" not in ip), key=ipaddress.ip_address)
            addr = f"{len(v4)} IPv4" + (f": {v4[0]}" if len(v4) == 1 else f", {v4[0]} to {v4[-1]}" if v4 else "")
            rows.append("| %s | %s | %s | %s | %s | %s |" % (
                prov, host, md_escape(chain), addr, md_escape("; ".join(sorted(owners)) or "unknown"),
                "; ".join(sorted(inf)) or "none"))
            if verbose:
                print(f"[dns] {prov}/{host}: {sorted(inf)}")
    return "\n".join(rows) + "\n"


def status_incidents(providers, verbose):
    out = ["# Status page components and incident statistics", "",
           "Source: Atlassian Statuspage summary.json and incidents.json captured by the probe",
           "script (DeepInfra does not expose a Statuspage API; see api-surface.md).", "",
           "Incident minutes are start to resolved as posted by the provider. Statuspage returns",
           "the 50 most recent incidents, so a 90 day window may be truncated where noted.",
           "Windows end at the capture time of incidents.json. An incident tagged on several",
           "components with the same name (for example one per region) counts once per name.",
           "Reference downtime budgets per 30 days: 99.99% = 4.4 min, 99.95% = 21.9 min,",
           "99.9% = 43.8 min, 99.5% = 219 min.", ""]
    for prov in providers:
        sp = os.path.join(PROBES, prov, "status.body")
        ip = os.path.join(PROBES, prov, "status_incidents.body")
        if not (os.path.exists(sp) and os.path.exists(ip)):
            continue
        try:
            s = json.loads(read(sp))
            inc = json.loads(read(ip))["incidents"]
        except (ValueError, KeyError):
            out.append(f"## {prov}: no Statuspage JSON\n\nNo Statuspage JSON available.\n")
            continue
        page = s["page"]
        groups = {c["id"]: c["name"] for c in s["components"] if c.get("group")}
        leaf = [c for c in s["components"] if not c.get("group")]
        out.append(f"## {prov}: {page['name']} ({page['url']})\n")
        out.append(f"Components: {len(s['components'])} total, {len(groups)} groups, {len(leaf)} leaf. "
                   f"Page updated {page['updated_at']}.\n")
        if groups:
            out.append("Groups: " + ", ".join(groups.values()) + "\n")
        names = collections.Counter(c["name"] for c in leaf)
        out.append("Leaf component names: " + ", ".join(f"{n} (x{k})" if k > 1 else n for n, k in sorted(names.items())) + "\n")
        now = capture_time(prov, "status_incidents")
        oldest = min(i["created_at"] for i in inc) if inc else "n/a"
        out.append(f"Incidents returned: {len(inc)} (oldest {oldest[:10]}). Window end: {now.isoformat()[:19]}Z.\n")
        for days in (30, 90):
            cut = now - timedelta(days=days)
            rec = [i for i in inc if ts(i["created_at"]) >= cut]
            truncated = len(inc) >= 50 and ts(oldest) > cut
            resolved = [i for i in rec if i.get("resolved_at")]
            total = sum(max(0.0, (ts(i["resolved_at"]) - ts(i["started_at"] or i["created_at"])).total_seconds() / 60) for i in resolved)
            impacts = collections.Counter(i["impact"] for i in rec)
            out.append(f"### Last {days} days{' (window truncated by 50-incident API limit)' if truncated else ''}\n")
            out.append(f"Incidents: {len(rec)} ({', '.join(f'{k}: {v}' for k, v in sorted(impacts.items()))}). "
                       f"Resolved incident-minutes summed across incidents: {total:.0f}.\n")
            bycomp = collections.defaultdict(lambda: [0, 0.0, 0, 0.0])
            for i in resolved:
                dur = max(0.0, (ts(i["resolved_at"]) - ts(i["started_at"] or i["created_at"])).total_seconds() / 60)
                names = sorted(set(c["name"] for c in (i.get("components") or [])) or {"(no component tagged)"})
                for name in names:
                    v = bycomp[name]
                    v[0] += 1
                    v[1] += dur
                    if i["impact"] in ("major", "critical"):
                        v[2] += 1
                        v[3] += dur
            out.append("| Component | Incidents | Minutes | Major incidents | Major minutes | Availability if major minutes were full downtime |")
            out.append("| --- | --- | --- | --- | --- | --- |")
            for c, v in sorted(bycomp.items(), key=lambda kv: (-kv[1][1], kv[0]))[:25]:
                avail = 100 - v[3] / (days * 24 * 60) * 100
                out.append(f"| {md_escape(c)} | {v[0]} | {v[1]:.0f} | {v[2]} | {v[3]:.0f} | {avail:.3f}% |")
            out.append("")
        out.append("### Incident log (most recent 50)\n")
        out.append("| Created (UTC) | Impact | Minutes | Components | Title |")
        out.append("| --- | --- | --- | --- | --- |")
        for i in inc:
            dur = (ts(i["resolved_at"]) - ts(i["started_at"] or i["created_at"])).total_seconds() / 60 if i.get("resolved_at") else float("nan")
            comps = ", ".join(sorted(set(c["name"] for c in i.get("components", []))))
            if len(comps) > 70:
                comps = comps[:67] + "..."
            out.append(f"| {i['created_at'][:16]} | {i['impact']} | {dur:.0f} | {md_escape(comps)} | {md_escape(i['name'][:110])} |")
        out.append("")
        if verbose:
            print(f"[status] {prov}: {len(inc)} incidents")
    return "\n".join(out) + "\n"


def deepinfra_catalog(verbose):
    p = os.path.join(PROBES, "deepinfra", "public_models.body")
    q = os.path.join(PROBES, "deepinfra", "models.body")
    if not os.path.exists(p):
        return "# DeepInfra catalog\n\nNo capture found.\n"
    d = json.loads(read(p))
    o = json.loads(read(q))["data"] if os.path.exists(q) else []
    act = [m for m in d if not m.get("deprecated")]
    tg = [m for m in act if m["type"] == "text-generation"]
    dep_tg = [m for m in d if m.get("deprecated") and m["type"] == "text-generation"]
    out = ["# DeepInfra public catalog analysis", "",
           "Source: unauthenticated GET https://api.deepinfra.com/models/list and",
           "GET https://api.deepinfra.com/v1/openai/models, captured by the probe script.", "",
           f"Entries: {len(d)} total in models/list, {len(act)} active, {len(o)} in the OpenAI-style models endpoint.", "",
           "## Active models by type", "", "| Type | Active |", "| --- | --- |"]
    for t, n in ranked(collections.Counter(m["type"] for m in act)):
        out.append(f"| {t} | {n} |")
    out += ["", f"## Text generation: {len(tg)} active, {len(dep_tg)} deprecated", "",
            "### Declared quantization (active text generation)", "", "| Quantization | Models |", "| --- | --- |"]
    for qn, n in ranked(collections.Counter(str(m.get("quantization")) for m in tg)):
        out.append(f"| {qn} | {n} |")
    partner = [m for m in tg if m.get("is_partner")]
    out += ["", f"### Partner (proxied third-party) models: {len(partner)} of {len(tg)} active text models", "",
            ", ".join(sorted(m["model_name"] for m in partner)), "",
            "### Capability tags (active text generation)", "", "| Tag | Models |", "| --- | --- |"]
    for t, n in ranked(collections.Counter(t for m in tg for t in (m.get("tags") or []))):
        out.append(f"| {t} | {n} |")
    out += ["", "### Pricing fields present (active text generation)", "", "| Field | Models |", "| --- | --- |"]
    fields = collections.Counter(k for m in tg for k, v in (m.get("pricing") or {}).items() if v not in (None, {}, []))
    for k, n in ranked(fields):
        out.append(f"| {k} | {n} |")
    cached = [m["pricing"]["rate_per_input_token_cached"] for m in tg
              if (m.get("pricing") or {}).get("rate_per_input_token_cached") is not None]
    if cached:
        dist = collections.Counter(round(x, 4) for x in cached)
        out += ["", f"### Cached-input read multiplier (x input price): {len(cached)} of {len(tg)} active text models", "",
                f"Minimum {min(cached):.4f}, median {statistics.median(cached):.4f}, maximum {max(cached):.4f}.", "",
                "| Multiplier | Models |", "| --- | --- |"]
        for k, n in sorted(dist.items()):
            out.append(f"| {k} | {n} |")
    tiers = collections.Counter((m["pricing"].get("rate_per_service_tier_priority"), m["pricing"].get("rate_per_service_tier_flex")) for m in tg)
    out += ["", "### Service tier multipliers (priority, flex)", "", "| Priority x | Flex x | Models |", "| --- | --- | --- |"]
    for (pr, fl), n in ranked(tiers):
        out.append(f"| {pr} | {fl} | {n} |")
    out += ["", "### Newest 30 active text generation models by create_ts", "",
            "| Added | Model | Quantization | Partner | Context | In $/M | Out $/M | Cached read x |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for m in sorted(tg, key=lambda m: (m["create_ts"], m["model_name"]), reverse=True)[:30]:
        pr = m.get("pricing") or {}
        cin = pr.get("cents_per_input_token")
        cout = pr.get("cents_per_output_token")
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            m["create_ts"][:10], m["model_name"], m.get("quantization"), m.get("is_partner"), m.get("max_tokens"),
            f"{cin * 1e6 / 100:.3f}" if cin is not None else "", f"{cout * 1e6 / 100:.3f}" if cout is not None else "",
            pr.get("rate_per_input_token_cached")))
    out += ["", "### Flagship open-weight families (active text generation)", "", "| Family | Count | Models |", "| --- | --- | --- |"]
    for key in ["DeepSeek", "Llama", "Qwen3", "gpt-oss", "Kimi", "GLM", "gemma", "Nemotron", "Mistral", "MiniMax", "granite"]:
        names = sorted(m["model_name"] for m in tg if key.lower() in m["model_name"].lower())
        out.append(f"| {key} | {len(names)} | {md_escape(', '.join(names))} |")
    b200 = sorted(m["model_name"] for m in tg if "b200" in (m.get("tags") or []))
    out += ["", f"Models tagged b200: {', '.join(b200) or 'none'}", ""]
    if verbose:
        print(f"[deepinfra] {len(tg)} active text models")
    return "\n".join(out) + "\n"


def akamai_regions(verbose):
    p = os.path.join(PROBES, "akamai", "regions.body")
    if not os.path.exists(p):
        return "# Akamai Cloud regions\n\nNo capture found.\n"
    d = json.loads(read(p))["data"]
    gpu = [r for r in d if "GPU Linodes" in r["capabilities"]]
    out = ["# Akamai Cloud (Linode API v4) regions", "",
           "Source: unauthenticated GET https://api.linode.com/v4/regions captured by the probe script.", "",
           f"Regions: {len(d)}. Regions advertising the GPU Linodes capability: {len(gpu)}.", "",
           "| Region | Label | Country | Site type | GPU Linodes | Kubernetes | NETINT VPU | Placement Group |",
           "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sorted(d, key=lambda r: r["id"]):
        c = r["capabilities"]
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["id"], r["label"], r["country"], r.get("site_type", ""),
            "yes" if "GPU Linodes" in c else "", "yes" if "Kubernetes" in c else "",
            "yes" if "NETINT Quadra T1U" in c else "", "yes" if "Placement Group" in c else ""))
    out += ["", "All capability strings seen: " + ", ".join(sorted(set(x for r in d for x in r["capabilities"]))), ""]
    if verbose:
        print(f"[akamai] {len(d)} regions, {len(gpu)} with GPU")
    return "\n".join(out) + "\n"


OPENAI_CHAT_PARAMS = {
    "messages", "model", "audio", "frequency_penalty", "logit_bias", "logprobs", "max_completion_tokens",
    "max_tokens", "metadata", "modalities", "n", "parallel_tool_calls", "prediction", "presence_penalty",
    "prompt_cache_key", "prompt_cache_retention", "reasoning_effort", "response_format", "safety_identifier",
    "seed", "service_tier", "stop", "store", "stream", "stream_options", "temperature", "tool_choice", "tools",
    "top_logprobs", "top_p", "user", "verbosity", "web_search_options", "function_call", "functions",
}


def _resolve(spec, node, depth=0):
    if isinstance(node, dict) and "$ref" in node and depth < 8:
        cur = spec
        for part in node["$ref"].split("/")[1:]:
            cur = cur[part]
        return _resolve(spec, cur, depth + 1)
    return node


def _props(spec, schema, depth=0):
    schema = _resolve(spec, schema, depth)
    out = {}
    if not isinstance(schema, dict) or depth > 8:
        return out
    for key in ("allOf", "anyOf", "oneOf"):
        for sub in schema.get(key) or []:
            out.update(_props(spec, sub, depth + 1))
    for k, v in (schema.get("properties") or {}).items():
        v = _resolve(spec, v)
        out[k] = (v.get("description") or "")[:100].replace("\n", " ")
    return out


def _body_schema(spec, path, method="post"):
    op = spec["paths"].get(path, {}).get(method, {})
    content = (op.get("requestBody") or {}).get("content") or {}
    for ct in ("application/json", "*/*"):
        if ct in content:
            return content[ct].get("schema", {})
    return next(iter(content.values()))["schema"] if content else {}


def openapi_surface(verbose):
    out = ["# Public OpenAPI specifications", "",
           "Captured unauthenticated by the probe script. Path counts and parameter diffs are computed",
           "mechanically from each specification; descriptions are quoted from the spec.", ""]
    specs = [
        ("Baseten management API", "baseten/openapi.body", None),
        ("DeepInfra API", "deepinfra/openapi.body", "/v1/chat/completions"),
        ("Nebius Token Factory inference API", "nebius/openapi.body", "/v1/chat/completions"),
        ("Akamai Cloud (Linode API v4)", "akamai/openapi.body", None),
    ]
    loaded = {}
    for label, rel, chat in specs:
        path = os.path.join(PROBES, rel)
        try:
            spec = json.loads(read(path))
            assert "paths" in spec
        except (ValueError, AssertionError):
            out.append(f"## {label}\n\nNo specification captured.\n")
            continue
        loaded[label] = spec
        paths = spec["paths"]
        ops = sum(1 for v in paths.values() for m in v if m in ("get", "post", "put", "patch", "delete"))
        tags = collections.Counter(t for v in paths.values() for m, op in v.items()
                                   if isinstance(op, dict) for t in op.get("tags", []))
        sec = list((spec.get("components", {}).get("securitySchemes") or {}).keys())
        out.append(f"## {label}\n")
        out.append(f"Title: {spec['info'].get('title')}; version: {spec['info'].get('version')}; "
                   f"OpenAPI {spec.get('openapi')}; servers: {', '.join(s.get('url', '') for s in spec.get('servers', []))}.\n")
        out.append(f"Paths: {len(paths)}; operations: {ops}; security schemes: {', '.join(sec) or 'none declared'}.\n")
        if tags:
            out.append("Tags by operation count: " + ", ".join(f"{t} ({n})" for t, n in ranked(tags)) + "\n")
        out.append("<details><summary>Path list</summary>\n")
        out.append("| Methods | Path |")
        out.append("| --- | --- |")
        for pth, v in paths.items():
            ms = ",".join(m.upper() for m in v if m in ("get", "post", "put", "patch", "delete"))
            out.append(f"| {ms} | `{pth}` |")
        out.append("\n</details>\n")
        if chat and chat in paths:
            ps = _props(spec, _body_schema(spec, chat))
            extra = sorted(set(ps) - OPENAI_CHAT_PARAMS)
            missing = sorted(OPENAI_CHAT_PARAMS - set(ps))
            out.append(f"### Chat completions request schema vs OpenAI ({chat})\n")
            out.append(f"Declared parameters: {len(ps)}. Present OpenAI parameters: {len(set(ps) & OPENAI_CHAT_PARAMS)}.\n")
            out.append("Parameters beyond the OpenAI schema:\n")
            out.append("| Parameter | Description (from spec) |")
            out.append("| --- | --- |")
            for k in extra:
                out.append(f"| `{k}` | {md_escape(ps[k])} |")
            out.append("")
            out.append("OpenAI parameters absent from the schema: " + ", ".join(f"`{m}`" for m in missing) + "\n")
            op = paths[chat].get("post", {})
            codes = {c: (r.get("description") or "")[:60] for c, r in (op.get("responses") or {}).items()}
            out.append("Documented response codes: " + ", ".join(f"{c} ({d})" if d else c for c, d in codes.items()) + "\n")
        if verbose:
            print(f"[openapi] {label}: {len(paths)} paths")
    tpl = os.path.join(PROBES, "nebius", "dedicated_templates.body")
    if os.path.exists(tpl):
        try:
            d = json.loads(read(tpl))
            items = d.get("data") or d.get("templates") or d.get("items") or []
            if isinstance(d, list):
                items = d
        except ValueError:
            items = []
        if items:
            out.append("## Nebius dedicated endpoint templates (public GET /v0/dedicated_endpoints/templates)\n")
            out.append(f"Templates: {len(items)}. Types: " + ", ".join(
                f"{t} ({n})" for t, n in ranked(collections.Counter(i.get("type") for i in items))) + "\n")
            q = collections.Counter()
            gpu_region = collections.Counter()
            rows = []
            for it in items:
                for fname, fl in (it.get("flavors") or {}).items():
                    q[str(fl.get("quantization"))] += 1
                    gcs = ((fl.get("available_configurations") or {}).get("gpu_configurations") or {})
                    for g, cfg in gcs.items():
                        for r in cfg.get("allowed_regions", []):
                            gpu_region[(g, r)] += 1
                    rows.append((it.get("name"), fname, fl.get("quantization"),
                                 ", ".join(f"{g}@{'/'.join(c.get('allowed_regions', []))}" for g, c in gcs.items()),
                                 max((c.get("max_replicas_allowed") or 0) for c in gcs.values()) if gcs else "",
                                 (it.get("metadata") or {}).get("context_window_k")))
            out.append("Flavor quantization: " + ", ".join(f"{k} ({n})" for k, n in ranked(q)) + "\n")
            out.append("GPU type by region (flavor count): " + ", ".join(
                f"{g} in {r} ({n})" for (g, r), n in sorted(gpu_region.items())) + "\n")
            out.append("| Model | Flavor | Quantization | GPU types at regions | Max replicas | Context (K) |")
            out.append("| --- | --- | --- | --- | --- | --- |")
            for r in sorted(rows):
                out.append("| " + " | ".join(md_escape(x) for x in r) + " |")
            out.append("")
    return "\n".join(out) + "\n"


def latency(providers, verbose):
    out = ["# Connection-phase latency", "",
           "Source: timing.txt per provider, written by the probe script. Each row is an",
           "unauthenticated GET that returns before any inference, so the numbers measure DNS,",
           "TCP connect, TLS handshake, and gateway time-to-first-byte from one vantage point.",
           "They are a floor under TTFT from that location, not a TTFT measurement.",
           "Compare hosts on the unknown-route rows: each returns an error with minimal server work.",
           "The model and region list rows include the time to build a full response body.", ""]
    rows = ["| Provider | URL | Remote IP | Samples | HTTP | Connect p50 (ms) | TLS done p50 (ms) | TTFB p50 (ms) | TTFB min to max (ms) |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    vantage = set()
    for prov in providers:
        txt = read(os.path.join(PROBES, prov, "timing.txt"))
        if not txt:
            continue
        samples = collections.defaultdict(list)
        for line in txt.splitlines():
            if line.startswith("# vantage:"):
                vantage.add(line.split(":", 1)[1].strip())
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 9:
                samples[parts[0]].append(parts)
        for url, ss in samples.items():
            ms = lambda idx: [float(s[idx]) * 1000 for s in ss]
            ttfb = ms(6)
            rows.append("| %s | %s | %s | %d | %s | %.0f | %.0f | %.0f | %.0f to %.0f |" % (
                prov, md_escape(url), ss[-1][8], len(ss), ",".join(sorted(set(s[2] for s in ss))),
                statistics.median(ms(4)), statistics.median(ms(5)), statistics.median(ttfb), min(ttfb), max(ttfb)))
            if verbose:
                print(f"[latency] {prov} {url}: ttfb p50 {statistics.median(ttfb):.0f} ms")
    out.append("Vantage: " + ("; ".join(sorted(vantage)) or "not recorded") + ".")
    out.append("")
    return "\n".join(out + rows) + "\n"


def write_debug_bundle(args):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bdir = f"/var/tmp/akamai-validation/{TOOL}-{stamp}"
    os.makedirs(bdir, exist_ok=True)
    shutil.copytree(args.probes, os.path.join(bdir, "probes"), dirs_exist_ok=True)
    shutil.copytree(args.out, os.path.join(bdir, "derived"), dirs_exist_ok=True)
    redact = re.compile(r"(TOKEN|SECRET|PASSWORD|KEY)", re.I)
    env = "\n".join(f"{k}=[REDACTED]" if redact.search(k) else f"{k}={v}" for k, v in sorted(os.environ.items()))
    with open(os.path.join(bdir, "environment.txt"), "w") as f:
        f.write(f"host_os: {platform.platform()}\npython: {sys.version.split()[0]}\ntool: {TOOL}.py\n"
                f"invocation: {' '.join(sys.argv)}\nutc: {datetime.now(timezone.utc).isoformat()}\n\n"
                f"environment (redacted):\n{env}\n")
    with open(os.path.join(bdir, "manifest.txt"), "w") as f:
        f.write("manifest.txt     This file.\nenvironment.txt  Host, interpreter, invocation, redacted environment.\n"
                "probes/          Input captures.\nderived/         Output Markdown tables.\n")
    tgz = f"/var/tmp/akamai-validation/{TOOL}-{stamp}.tgz"
    with tarfile.open(tgz, "w:gz") as t:
        t.add(bdir, arcname=os.path.basename(bdir))
    print(f"DEBUG BUNDLE: {bdir}")
    print(f"DEBUG BUNDLE TAR: {tgz}")


def main():
    global PROBES
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true", help="print per-item progress")
    ap.add_argument("--debug", action="store_true",
                    help="write a support bundle to /var/tmp/akamai-validation/ and print its location last")
    ap.add_argument("--probes", default=PROBES, help="input directory (default: evidence/probes)")
    ap.add_argument("--out", default=OUT, help="output directory (default: evidence/derived)")
    args = ap.parse_args()
    PROBES = args.probes
    providers = sorted(p for p in os.listdir(PROBES) if os.path.isdir(os.path.join(PROBES, p)))
    os.makedirs(args.out, exist_ok=True)
    outputs = {
        "api-surface.md": api_surface(providers, args.verbose),
        "dns-cdn.md": dns_cdn(providers, args.verbose),
        "status-incidents.md": status_incidents(providers, args.verbose),
        "deepinfra-catalog.md": deepinfra_catalog(args.verbose),
        "akamai-regions.md": akamai_regions(args.verbose),
        "openapi-surface.md": openapi_surface(args.verbose),
        "latency.md": latency(providers, args.verbose),
    }
    for fn, content in outputs.items():
        path = os.path.join(args.out, fn)
        # Leave unchanged tables untouched so their mtimes do not mark the
        # report stale for make.
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                if f.read() == content:
                    print(f"unchanged {path}")
                    continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote {path}")
    if args.debug:
        write_debug_bundle(args)


if __name__ == "__main__":
    main()
