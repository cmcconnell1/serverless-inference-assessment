#!/usr/bin/env bash
# probe_providers.sh
#
# Unauthenticated, read-only HTTP and DNS probes against public serverless
# inference API endpoints. Captures response headers, error schemas, public
# model listings, status-page summaries, and CDN/DNS fingerprints as static
# evidence for the competitive assessment. No accounts, no API keys, no spend.
#
# Outputs: evidence/probes/<provider>/<probe>.headers, .body, .meta
#          evidence/probes/<provider>/dns.txt, asn.txt, timing.txt
#
# Usage: probe_providers.sh [-h|--help] [-v|--verbose] [--debug] [-o DIR]
#                           [-p PROVIDER[,PROVIDER...]] [--vantage LABEL]

set -u

TOOL_NAME="probe_providers"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUT_DIR="${REPO_ROOT}/evidence/probes"
VERBOSE=0
DEBUG=0
PROVIDERS="baseten,deepinfra,nebius,akamai"
CURL_TIMEOUT=20
TIMING_SAMPLES=9
LIVE_METRICS_GAP=30
VANTAGE="unspecified (timezone $(date +%Z))"
UA="ci-assessment-probe/1.0 (read-only; unauthenticated)"
INVALID_KEY="sk-invalid-0000000000000000"

usage() {
  cat <<USAGE
${TOOL_NAME}.sh: capture public API evidence from serverless inference providers.

Usage:
  ${TOOL_NAME}.sh [options]

Options:
  -h, --help            Show this help and exit.
  -v, --verbose         Print each probe and HTTP status to the screen.
  -o, --out DIR         Output directory (default: evidence/probes under repo root).
  -p, --providers LIST  Comma-separated subset of: baseten,deepinfra,nebius,akamai.
  --vantage LABEL       Free-text location of the probing host, recorded in
                        timing.txt (default: unspecified plus local timezone).
  --debug               Write a self-contained support bundle to
                        /var/tmp/akamai-validation/${TOOL_NAME}-<UTC>/ plus a .tgz, and print
                        DEBUG BUNDLE lines last. Implies full capture. Distinct
                        from --verbose.

Probes per provider (all unauthenticated):
  models          GET  <api>/v1/models (or provider public model list)
  openapi         GET  public OpenAPI specs and API catalogs where published
  noauth          POST <api>/v1/chat/completions with no Authorization header
  badkey          POST <api>/v1/chat/completions with an invalid bearer token
  options         OPTIONS <api>/v1/chat/completions (CORS surface)
  status          GET  status page summary JSON when the provider uses Statuspage
  docs_head       HEAD docs site (CDN and server headers)
  dns             dig CNAME/A for api and docs hosts
  asn             Team Cymru whois lookup of every resolved address (origin ASN)
  timing          ${TIMING_SAMPLES} samples of DNS, TCP connect, TLS, and time-to-first-byte
                  per inference host: an unknown route (minimal server work, the
                  like-for-like comparison) and the model or region list

Each .meta file records body_sha256 of the bytes as received. JSON bodies are
then re-serialized with non-ASCII characters escaped (\\uXXXX), which keeps every
value identical when parsed and leaves the stored file pure ASCII.

Secrets: the script sends only a fixed, obviously invalid token. Any environment
variable whose name matches TOKEN, SECRET, PASSWORD, or KEY is redacted in the
debug bundle.
USAGE
}

log() { printf '%s\n' "$*" >&2; }
vlog() { [ "${VERBOSE}" -eq 1 ] && log "$@"; return 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    -v|--verbose) VERBOSE=1 ;;
    --debug) DEBUG=1; VERBOSE=1 ;;
    -o|--out) OUT_DIR="$2"; shift ;;
    -p|--providers) PROVIDERS="$2"; shift ;;
    --vantage) VANTAGE="$2"; shift ;;
    *) log "Unknown option: $1"; usage; exit 2 ;;
  esac
  shift
done

for bin in curl dig whois shasum python3; do
  command -v "$bin" >/dev/null 2>&1 || { log "Missing dependency: $bin"; exit 3; }
done

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "${OUT_DIR}"
RUN_LOG="${OUT_DIR}/run-${STAMP}.log"
: > "${RUN_LOG}"

# ascii_json FILE: if FILE parses as JSON, rewrite it with every non-ASCII
# character as a \uXXXX escape. Values are unchanged when parsed; the file
# becomes pure ASCII, so later character normalization cannot alter it.
ascii_json() {
  python3 - "$1" <<'PY'
import json, sys
path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
except (ValueError, UnicodeDecodeError):
    print("raw")
    sys.exit(0)
with open(path, "w", encoding="ascii") as f:
    json.dump(data, f, ensure_ascii=True)
print("json, non-ASCII escaped as \\uXXXX")
PY
}

# capture NAME PROVIDER METHOD URL [extra curl args...]
capture() {
  local name="$1" prov="$2" method="$3" url="$4"; shift 4
  local dir="${OUT_DIR}/${prov}"
  mkdir -p "${dir}"
  local hdr="${dir}/${name}.headers" body="${dir}/${name}.body" meta="${dir}/${name}.meta"
  local code
  code="$(curl -sS -o "${body}" -D "${hdr}" -w '%{http_code}' \
      -X "${method}" --max-time "${CURL_TIMEOUT}" -A "${UA}" "$@" "${url}" 2>>"${RUN_LOG}")" || code="000"
  {
    echo "provider: ${prov}"
    echo "probe: ${name}"
    echo "method: ${method}"
    echo "url: ${url}"
    echo "http_code: ${code}"
    echo "captured_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "body_bytes: $(wc -c < "${body}" | tr -d ' ')"
    echo "body_sha256: $(shasum -a 256 "${body}" | cut -d' ' -f1)"
    echo "body_encoding: $(ascii_json "${body}")"
  } > "${meta}"
  vlog "[${prov}] ${name} ${method} ${url} -> ${code}"
  printf '%s %s %s %s -> %s\n' "${prov}" "${name}" "${method}" "${url}" "${code}" >> "${RUN_LOG}"
}

dns_capture() {
  local prov="$1"; shift
  local dir="${OUT_DIR}/${prov}"
  mkdir -p "${dir}"
  local out="${dir}/dns.txt"
  : > "${out}"
  for host in "$@"; do
    {
      echo "== ${host} =="
      dig +noall +answer "${host}" A
      dig +noall +answer "${host}" AAAA
      dig +noall +answer "${host}" CNAME
      echo
    } >> "${out}" 2>>"${RUN_LOG}"
  done
  vlog "[${prov}] dns -> ${out}"
  asn_capture "${prov}"
}

# asn_capture PROVIDER: origin ASN for every A/AAAA address in dns.txt.
asn_capture() {
  local prov="$1"
  local dir="${OUT_DIR}/${prov}"
  local out="${dir}/asn.txt"
  : > "${out}"
  awk '$4=="A" || $4=="AAAA" {print $5}' "${dir}/dns.txt" | sort -u | while read -r ip; do
    whois -h whois.cymru.com " -v ${ip}" 2>>"${RUN_LOG}" | tail -n 1 >> "${out}"
  done
  vlog "[${prov}] asn -> ${out}"
}

# timing_capture PROVIDER URL...: connection-phase timings, no inference work.
timing_capture() {
  local prov="$1"; shift
  local dir="${OUT_DIR}/${prov}"
  mkdir -p "${dir}"
  local out="${dir}/timing.txt"
  {
    echo "# vantage: ${VANTAGE}"
    echo "# captured_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "# columns: url sample http_code dns_s connect_s tls_s ttfb_s total_s remote_ip"
  } > "${out}"
  local url i
  for url in "$@"; do
    for i in $(seq 1 "${TIMING_SAMPLES}"); do
      curl -sS -o /dev/null --max-time "${CURL_TIMEOUT}" -A "${UA}" \
        -w "${url} ${i} %{http_code} %{time_namelookup} %{time_connect} %{time_appconnect} %{time_starttransfer} %{time_total} %{remote_ip}\n" \
        "${url}" >> "${out}" 2>>"${RUN_LOG}"
    done
  done
  vlog "[${prov}] timing -> ${out}"
}

CHAT_BODY='{"model":"probe-model","messages":[{"role":"user","content":"ping"}],"max_tokens":1}'
JSON_HDR="Content-Type: application/json"

probe_openai_surface() {
  # PROVIDER BASE_URL
  local prov="$1" base="$2"
  capture models   "${prov}" GET     "${base}/models"
  capture noauth   "${prov}" POST    "${base}/chat/completions" -H "${JSON_HDR}" --data "${CHAT_BODY}"
  capture badkey   "${prov}" POST    "${base}/chat/completions" -H "${JSON_HDR}" -H "Authorization: Bearer ${INVALID_KEY}" --data "${CHAT_BODY}"
  capture options  "${prov}" OPTIONS "${base}/chat/completions" -H "Origin: https://example.com" -H "Access-Control-Request-Method: POST"
  capture notfound "${prov}" GET     "${base}/this-route-does-not-exist"
}

probe_baseten() {
  probe_openai_surface baseten "https://inference.baseten.co/v1"
  capture mgmt_noauth baseten GET "https://api.baseten.co/v1/models"
  capture openapi baseten GET "https://api.baseten.co/v1/spec"
  capture inference_openapi baseten GET "https://inference.baseten.co/openapi.json"
  capture inference_docs baseten GET "https://inference.baseten.co/docs"
  capture status baseten GET "https://status.baseten.co/api/v2/summary.json"
  capture status_incidents baseten GET "https://status.baseten.co/api/v2/incidents.json"
  capture docs_head baseten HEAD "https://docs.baseten.co/" -I
  capture www_head baseten HEAD "https://www.baseten.co/" -I
  dns_capture baseten inference.baseten.co api.baseten.co docs.baseten.co www.baseten.co status.baseten.co
  timing_capture baseten "https://inference.baseten.co/v1/this-route-does-not-exist" "https://inference.baseten.co/v1/models"
}

probe_deepinfra() {
  probe_openai_surface deepinfra "https://api.deepinfra.com/v1/openai"
  capture public_models deepinfra GET "https://api.deepinfra.com/models/list"
  capture openapi deepinfra GET "https://api.deepinfra.com/openapi.json"
  capture live_metrics deepinfra GET "https://api.deepinfra.com/v1/metrics/live"
  sleep "${LIVE_METRICS_GAP}"
  capture live_metrics_2 deepinfra GET "https://api.deepinfra.com/v1/metrics/live"
  capture native_noauth deepinfra POST "https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3.1-8B-Instruct" -H "${JSON_HDR}" --data '{"input":"ping"}'
  capture status deepinfra GET "https://status.deepinfra.com/api/v2/summary.json"
  capture status_incidents deepinfra GET "https://status.deepinfra.com/api/v2/incidents.json"
  capture docs_head deepinfra HEAD "https://deepinfra.com/docs" -I
  capture www_head deepinfra HEAD "https://deepinfra.com/" -I
  dns_capture deepinfra api.deepinfra.com deepinfra.com status.deepinfra.com
  timing_capture deepinfra "https://api.deepinfra.com/v1/openai/this-route-does-not-exist" "https://api.deepinfra.com/v1/openai/models"
}

probe_nebius() {
  probe_openai_surface nebius "https://api.studio.nebius.com/v1"
  probe_openai_surface nebius_tf "https://api.tokenfactory.nebius.com/v1"
  capture openapi nebius GET "https://api.studio.nebius.com/openapi.json"
  capture dedicated_templates nebius GET "https://api.tokenfactory.nebius.com/v0/dedicated_endpoints/templates"
  capture openapi_tf nebius GET "https://api.tokenfactory.nebius.com/openapi.json"
  capture fastapi_docs nebius GET "https://api.studio.nebius.com/docs"
  capture status nebius GET "https://status.nebius.com/api/v2/summary.json"
  capture status_incidents nebius GET "https://status.nebius.com/api/v2/incidents.json"
  capture docs_head nebius HEAD "https://docs.tokenfactory.nebius.com/" -I
  capture docs_head_legacy nebius HEAD "https://docs.nebius.com/studio/inference" -I
  capture www_head nebius HEAD "https://nebius.com/token-factory" -I
  dns_capture nebius api.studio.nebius.com api.tokenfactory.nebius.com docs.tokenfactory.nebius.com nebius.com status.nebius.com
  timing_capture nebius "https://api.tokenfactory.nebius.com/v1/this-route-does-not-exist" "https://api.tokenfactory.nebius.com/v1/models"
}

probe_akamai() {
  capture regions akamai GET "https://api.linode.com/v4/regions"
  capture noauth akamai GET "https://api.linode.com/v4/profile"
  capture badkey akamai GET "https://api.linode.com/v4/profile" -H "Authorization: Bearer ${INVALID_KEY}"
  capture notfound akamai GET "https://api.linode.com/v4/this-route-does-not-exist"
  capture options akamai OPTIONS "https://api.linode.com/v4/profile" -H "Origin: https://example.com" -H "Access-Control-Request-Method: GET"
  capture api_catalog akamai GET "https://techdocs.akamai.com/cloud-computing/.well-known/api-catalog"
  capture agent_skills akamai GET "https://techdocs.akamai.com/cloud-computing/.well-known/agent-skills/index.json"
  capture llms_txt akamai GET "https://techdocs.akamai.com/cloud-computing/llms.txt"
  capture openapi akamai GET "https://raw.githubusercontent.com/linode/linode-api-docs/development/openapi.json"
  capture status akamai GET "https://status.linode.com/api/v2/summary.json"
  capture status_incidents akamai GET "https://status.linode.com/api/v2/incidents.json"
  capture docs_head akamai HEAD "https://techdocs.akamai.com/cloud-computing/docs" -I
  capture www_head akamai HEAD "https://www.akamai.com/products/cloud-computing-services" -I
  capture inference_head akamai HEAD "https://www.akamai.com/solutions/ai-inference" -I
  dns_capture akamai api.linode.com techdocs.akamai.com www.akamai.com status.linode.com
  timing_capture akamai "https://api.linode.com/v4/this-route-does-not-exist" "https://api.linode.com/v4/regions"
}

IFS=',' read -r -a PROV_ARR <<< "${PROVIDERS}"
for p in "${PROV_ARR[@]}"; do
  case "$p" in
    baseten)   probe_baseten ;;
    deepinfra) probe_deepinfra ;;
    nebius)    probe_nebius ;;
    akamai)    probe_akamai ;;
    *) log "Unknown provider: $p"; exit 2 ;;
  esac
done

log "Probe run complete. Outputs under ${OUT_DIR} (run log: ${RUN_LOG})"

if [ "${DEBUG}" -eq 1 ]; then
  BUNDLE_DIR="/var/tmp/akamai-validation/${TOOL_NAME}-${STAMP}"
  mkdir -p "${BUNDLE_DIR}"
  cp -R "${OUT_DIR}" "${BUNDLE_DIR}/probes"
  {
    echo "host_os: $(uname -a)"
    echo "tool: ${TOOL_NAME}.sh"
    echo "invocation: $0 ${*:-}"
    echo "providers: ${PROVIDERS}"
    echo "curl: $(curl --version | head -1)"
    echo "dig: $(dig -v 2>&1 | head -1)"
    echo "vantage: ${VANTAGE}"
    echo "bash: ${BASH_VERSION}"
    echo "utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo
    echo "environment (redacted):"
    env | sort | sed -E 's/^([^=]*(TOKEN|SECRET|PASSWORD|KEY)[^=]*)=.*/\1=[REDACTED]/I'
  } > "${BUNDLE_DIR}/environment.txt"
  cat > "${BUNDLE_DIR}/manifest.txt" <<MANIFEST
manifest.txt       This file.
environment.txt    Host, tool versions, invocation, redacted environment.
probes/            Copy of every capture (.headers, .body, .meta, dns.txt, asn.txt,
                   timing.txt) and run log.
MANIFEST
  TGZ="/var/tmp/akamai-validation/${TOOL_NAME}-${STAMP}.tgz"
  tar -czf "${TGZ}" -C "/var/tmp/akamai-validation" "${TOOL_NAME}-${STAMP}"
  echo "DEBUG BUNDLE: ${BUNDLE_DIR}"
  echo "DEBUG BUNDLE TAR: ${TGZ}"
fi
