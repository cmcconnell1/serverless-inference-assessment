#!/usr/bin/env bash
# build_report.sh
#
# Render the assessment into one PDF. Two variants share the pipeline and styling:
#   full   docs/*.md plus selected evidence tables (the full report)
#   brief  brief/*.md, no appendix; cites full-report sections as plain text
# Pipeline: assemble Markdown -> pandoc (Mermaid to SVG, link rewrite) ->
# standalone HTML with print CSS -> headless Chrome PDF -> metadata rewrite ->
# hidden-character audit of the HTML intermediate.
#
# Usage: build_report.sh [-h|--help] [-v|--verbose] [--debug] [--variant full|brief] [-o FILE] [--keep-html]

set -euo pipefail

TOOL_NAME="build_report"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPORT_DIR="${SCRIPT_DIR}/report"
PDF_BASE="${REPO_ROOT}/dist/serverless-inference-assessment"
OUT_PDF=""
VARIANT="full"
TITLE="Serverless Inference Assessment"
SUBTITLE="Baseten, DeepInfra, and Nebius Token Factory, with implications for Akamai Cloud"
AUTHOR="Chris McConnell"
PIKEPDF_VERSION="10.15.0"
VERBOSE=0
DEBUG=0
KEEP_HTML=0
ARGS=("$@")

usage() {
  cat <<USAGE
${TOOL_NAME}.sh: build the brief or the full PDF report from the Markdown sources.

Usage:
  ${TOOL_NAME}.sh [options]

Options:
  -h, --help        Show this help and exit.
  -v, --verbose     Print each build step to the screen.
  --variant NAME    full (default): docs/ plus the evidence appendix, written to
                    dist/serverless-inference-assessment-full-report-chris-mcconnell.pdf.
                    brief: brief/ only, written to
                    dist/serverless-inference-assessment-brief-chris-mcconnell.pdf.
  -o, --out FILE    Output PDF path (default: set by --variant).
  --keep-html       Also write the HTML intermediate next to the PDF.
  --debug           Write a self-contained support bundle (assembled Markdown, HTML,
                    diagrams, logs, tool versions) to
                    /var/tmp/akamai-validation/${TOOL_NAME}-<variant>-<UTC>/ plus a .tgz, and print
                    DEBUG BUNDLE lines last. Implies --verbose.

Inputs:
  docs/[0-9][0-9]*.md            Full report chapters, in file-name order.
  brief/[0-9][0-9]*.md           Brief chapters, in file-name order.
  evidence/derived/*.md          Latency, DNS, status, catalog, and region tables (full only).
  evidence/manual/browser-checked-urls.tsv, evidence/derived/source-check.md
                                 With probe .meta files, set the cover evidence date range.
  CHANGELOG.md                   First release heading becomes the report version.

Requirements:
  pandoc 3.x, mmdc (mermaid-cli), Google Chrome or Chromium, uv, python3.
  Set CHROME=/path/to/chrome to override browser discovery.
  Set SOURCE_DATE_EPOCH to pin the build date for a reproducible cover page.

Exit codes: 0 success, 2 usage error, 3 missing dependency, 4 audit failure.
USAGE
}

log() { printf '%s\n' "$*" >&2; }
vlog() { [ "${VERBOSE}" -eq 1 ] && log "$@"; return 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    -v|--verbose) VERBOSE=1 ;;
    --debug) DEBUG=1; VERBOSE=1 ;;
    --keep-html) KEEP_HTML=1 ;;
    --variant) VARIANT="${2:-}"; shift ;;
    -o|--out) OUT_PDF="$2"; shift ;;
    *) log "Unknown option: $1"; usage; exit 2 ;;
  esac
  shift
done

case "${VARIANT}" in
  full)
    CHAPTERS="docs/[0-9][0-9]*.md"; ASSEMBLE_FLAGS=(); EXTERNAL_CHAPTERS="false"
    DOC_TITLE="${TITLE}: Full Report"; COVER_LABEL="Competitive assessment: full report"
    DEFAULT_PDF="${PDF_BASE}-full-report-chris-mcconnell.pdf" ;;
  brief)
    CHAPTERS="brief/[0-9][0-9]*.md"; ASSEMBLE_FLAGS=(--no-appendix); EXTERNAL_CHAPTERS="true"
    DOC_TITLE="${TITLE}: Brief"; COVER_LABEL="Competitive assessment: brief"
    DEFAULT_PDF="${PDF_BASE}-brief-chris-mcconnell.pdf" ;;
  *) log "Unknown variant: ${VARIANT} (expected full or brief)"; usage; exit 2 ;;
esac
OUT_PDF="${OUT_PDF:-${DEFAULT_PDF}}"

find_chrome() {
  if [ -n "${CHROME:-}" ]; then echo "${CHROME}"; return; fi
  local c
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
  for c in google-chrome google-chrome-stable chromium chromium-browser; do
    command -v "$c" >/dev/null 2>&1 && { command -v "$c"; return; }
  done
}

CHROME_BIN="$(find_chrome || true)"
for bin in pandoc mmdc uv python3; do
  command -v "$bin" >/dev/null 2>&1 || { log "Missing dependency: $bin"; exit 3; }
done
[ -n "${CHROME_BIN}" ] || { log "Missing dependency: Chrome or Chromium (set CHROME=)"; exit 3; }

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/${TOOL_NAME}.XXXXXX")"
LOGS="${WORK}/logs"
mkdir -p "${LOGS}" "${WORK}/diagrams" "$(dirname "${OUT_PDF}")"
cleanup() { [ "${DEBUG}" -eq 1 ] || rm -rf "${WORK:?}"; }
trap cleanup EXIT

if [ -n "${SOURCE_DATE_EPOCH:-}" ]; then
  BUILD_DATE="$(date -u -r "${SOURCE_DATE_EPOCH}" +%Y-%m-%d 2>/dev/null || date -u -d "@${SOURCE_DATE_EPOCH}" +%Y-%m-%d)"
else
  BUILD_DATE="$(date -u +%Y-%m-%d)"
fi
VERSION="$(sed -nE 's/^## \[([^]]+)\].*/\1/p' "${REPO_ROOT}/CHANGELOG.md" | head -n 1)"
VERSION="${VERSION:-unversioned}"
if git -C "${REPO_ROOT}" rev-parse --short HEAD >/dev/null 2>&1; then
  VERSION="${VERSION} ($(git -C "${REPO_ROOT}" rev-parse --short HEAD)$(git -C "${REPO_ROOT}" diff --quiet || echo ', modified'))"
fi

vlog "[1/6] assemble Markdown"
SUMMARY="$(python3 "${REPORT_DIR}/assemble.py" --root "${REPO_ROOT}" --out "${WORK}/report.md" \
  --meta "${WORK}/assembly.json" --chapters "${CHAPTERS}" ${ASSEMBLE_FLAGS[@]+"${ASSEMBLE_FLAGS[@]}"})"
EVIDENCE_FIRST="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["evidence_first_date_utc"])' <<<"${SUMMARY}")"
EVIDENCE_LAST="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["evidence_last_date_utc"])' <<<"${SUMMARY}")"
# Probes, browser checks, and the source check can fall on different UTC dates.
if [ "${EVIDENCE_LAST}" = "${EVIDENCE_FIRST}" ] || [ "${EVIDENCE_LAST}" = "unknown" ]; then
  EVIDENCE_RANGE="${EVIDENCE_FIRST}"
else
  EVIDENCE_RANGE="${EVIDENCE_FIRST} to ${EVIDENCE_LAST}"
fi
# The cover date field carries four label/value pairs as inline HTML; print.css
# lays them out as the cover metadata block.
meta_item() { printf '<span class="meta"><span class="k">%s</span> <span class="v">%s</span></span>' "$1" "$2"; }
COVER_META="$(meta_item "Prepared by" "${AUTHOR}")$(meta_item "Evidence window" "${EVIDENCE_RANGE} (UTC)")$(meta_item "Built" "${BUILD_DATE} (UTC)")$(meta_item "Version" "${VERSION}")"
python3 - "${WORK}/assembly.json" "${WORK}/meta.yaml" "${TITLE}" "${SUBTITLE}" \
  "${COVER_META}" "${DOC_TITLE}" "${EXTERNAL_CHAPTERS}" <<'PY'
import json, sys
src, dst, title, subtitle, date, doc_title, external = sys.argv[1:8]
a = json.load(open(src))
q = lambda s: '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
lines = [f"title: {q(title)}", f"subtitle: {q(subtitle)}", f"date: {q(date)}",
         f"pagetitle: {q(doc_title)}", "document-css: false", "lang: en",
         f"external-chapters: {external}", "evidence-included:"]
lines += [f"  - {q(n)}" for n in a["evidence_included"]]
open(dst, "w").write("\n".join(lines) + "\n")
PY

# Per-variant running header and cover label, layered over print.css.
cat > "${WORK}/variant.css" <<CSS
@page { @top-left { content: "${DOC_TITLE}"; } }
header#title-block-header::before { content: "${COVER_LABEL}"; }
CSS

vlog "[2/6] pandoc to HTML (Mermaid via mmdc)"
# --wrap=none keeps each heading on one source line. Chrome builds the PDF
# outline by joining an element's source lines without inserting a space, so a
# wrapped heading reaches the bookmark panel as "Part A: ProductManagement".
# autolink_bare_uris makes the bare-URL citations ("[B1] https://...") clickable.
MERMAID_OUT_DIR="${WORK}/diagrams" pandoc "${WORK}/report.md" \
  --from markdown-smart+autolink_bare_uris --to html5 --standalone \
  --wrap=none \
  --metadata-file "${WORK}/meta.yaml" \
  --toc --toc-depth=2 \
  --lua-filter "${REPORT_DIR}/mermaid.lua" \
  --lua-filter "${REPORT_DIR}/links.lua" \
  --css "${REPORT_DIR}/print.css" --css "${WORK}/variant.css" --embed-resources \
  --output "${WORK}/report.html" 2>"${LOGS}/pandoc.log"

vlog "[3/6] audit HTML for hidden and typographic characters"
if ! python3 - "${WORK}/report.html" >"${LOGS}/audit.log" 2>&1 <<'PY'
import sys, unicodedata
text = open(sys.argv[1], encoding="utf-8").read()
banned = set("\u2018\u2019\u201c\u201d\u2013\u2014\u2026\u00a0\u00a7\u2192\u2190\u2028\u2029")
bad = []
for i, ch in enumerate(text):
    cat = unicodedata.category(ch)
    if ch in banned or cat in ("Cf", "Co", "Cn", "Cs") or (cat == "So" and ch not in "\u00a9\u00ae\u2122"):
        bad.append((i, "U+%04X" % ord(ch), unicodedata.name(ch, "?")))
for b in bad[:50]:
    print("[FINDING] offset %d %s %s" % b)
print("[OK] no findings" if not bad else "[ERROR] %d findings" % len(bad))
sys.exit(1 if bad else 0)
PY
then
  cat "${LOGS}/audit.log" >&2
  exit 4
fi

vlog "[4/6] headless Chrome to PDF, numbering the table of contents"
render_pdf() {
  "${CHROME_BIN}" --headless=new --disable-gpu --no-pdf-header-footer \
    --generate-pdf-document-outline --run-all-compositor-stages-before-draw \
    --virtual-time-budget=20000 \
    --print-to-pdf="$2" "file://$1" >>"${LOGS}/chrome.log" 2>&1
}
toc_pages() {
  uv run --quiet --no-project --with "pikepdf==${PIKEPDF_VERSION}" \
    python "${REPORT_DIR}/toc_pages.py" "$@" >>"${LOGS}/toc.log" 2>&1 || { cat "${LOGS}/toc.log" >&2; exit 4; }
}
# Render with "00" placeholders so the first layout reserves page-number width,
# then inject the pages read back from the PDF and re-render until they agree.
toc_pages --placeholder --save "${WORK}/toc-0.json" "${WORK}/report.html" "${WORK}/report-toc.html"
PASS=0
while :; do
  PASS=$((PASS + 1))
  render_pdf "${WORK}/report-toc.html" "${WORK}/report-raw.pdf"
  toc_pages --pdf "${WORK}/report-raw.pdf" --save "${WORK}/toc-${PASS}.json" "${WORK}/report.html" "${WORK}/report-toc.next.html"
  if [ "${PASS}" -gt 1 ] && cmp -s "${WORK}/toc-$((PASS - 1)).json" "${WORK}/toc-${PASS}.json"; then
    vlog "      TOC page numbers stable after ${PASS} renders"
    break
  fi
  if [ "${PASS}" -ge 4 ]; then
    log "[ERROR] TOC page numbers did not stabilize after ${PASS} renders; see ${LOGS}/toc.log"
    exit 4
  fi
  mv "${WORK}/report-toc.next.html" "${WORK}/report-toc.html"
done

vlog "[5/6] rewrite PDF with title and author only: no producer, creator, dates, or XMP"
# Heading text as written, used to restore spaces Chrome drops from bookmarks.
python3 - "${WORK}/report.html" "${WORK}/headings.txt" <<'PY'
import html, re, sys
source = open(sys.argv[1], encoding="utf-8").read()
with open(sys.argv[2], "w", encoding="utf-8") as out:
    for match in re.finditer(r"<h[1-6][^>]*>(.*?)</h[1-6]>", source, re.S):
        text = html.unescape(re.sub(r"<[^>]+>", "", match.group(1)))
        text = " ".join(text.split())
        if text:
            out.write(text + "\n")
PY
uv run --quiet --no-project --with "pikepdf==${PIKEPDF_VERSION}" \
  python "${REPORT_DIR}/strip_pdf_metadata.py" --title "${DOC_TITLE}" --author "${AUTHOR}" \
  --headings "${WORK}/headings.txt" \
  "${WORK}/report-raw.pdf" "${OUT_PDF}" >"${LOGS}/strip.log" 2>&1 || { cat "${LOGS}/strip.log" >&2; exit 4; }
grep '^\[WARNING\]' "${LOGS}/strip.log" >&2 || true

vlog "[6/6] done"
[ "${KEEP_HTML}" -eq 1 ] && cp "${WORK}/report-toc.html" "${OUT_PDF%.pdf}.html"
if command -v pdfinfo >/dev/null 2>&1; then
  pdfinfo "${OUT_PDF}" > "${LOGS}/pdfinfo.txt" 2>&1 || true
  vlog "$(grep -E '^(Pages|Title|Author|Producer|Creator)' "${LOGS}/pdfinfo.txt" || true)"
fi
log "Report written: ${OUT_PDF}"

if [ "${DEBUG}" -eq 1 ]; then
  BUNDLE_DIR="/var/tmp/akamai-validation/${TOOL_NAME}-${VARIANT}-${STAMP}"
  mkdir -p "${BUNDLE_DIR}"
  cp -R "${WORK}/." "${BUNDLE_DIR}/work"
  cp "${OUT_PDF}" "${BUNDLE_DIR}/"
  {
    echo "host_os: $(uname -a)"
    echo "tool: ${TOOL_NAME}.sh"
    echo "invocation: $0 ${ARGS[*]:-}"
    echo "pandoc: $(pandoc --version | head -1)"
    echo "mmdc: $(mmdc --version 2>/dev/null)"
    echo "chrome: $("${CHROME_BIN}" --version 2>/dev/null)"
    echo "python3: $(python3 --version 2>&1)"
    echo "uv: $(uv --version)"
    echo "pikepdf: ${PIKEPDF_VERSION}"
    echo "variant: ${VARIANT}"
    echo "version: ${VERSION}"
    echo "build_date: ${BUILD_DATE}"
    echo "utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo
    echo "environment (redacted):"
    env | sort | sed -E 's/^([^=]*(TOKEN|SECRET|PASSWORD|KEY)[^=]*)=.*/\1=[REDACTED]/I'
  } > "${BUNDLE_DIR}/environment.txt"
  cat > "${BUNDLE_DIR}/manifest.txt" <<MANIFEST
manifest.txt              This file.
environment.txt           Host, tool versions, invocation, redacted environment.
$(basename "${OUT_PDF}")  Final PDF.
work/report.md            Assembled Markdown source.
work/meta.yaml            Title, date, version, evidence list passed to pandoc.
work/variant.css          Running header and cover label for this variant.
work/assembly.json        Chapters and evidence tables included, capture window.
work/report.html          Standalone HTML intermediate, audited for hidden characters.
work/report-toc.html      The same HTML with TOC page numbers; printed by Chrome.
work/toc-N.json           TOC page numbers read back after render N.
work/diagrams/            Mermaid sources (.mmd) and rendered SVGs.
work/report-raw.pdf       Chrome output before metadata rewrite.
work/logs/                pandoc, audit, chrome, strip, and pdfinfo logs.
MANIFEST
  TGZ="/var/tmp/akamai-validation/${TOOL_NAME}-${VARIANT}-${STAMP}.tgz"
  tar -czf "${TGZ}" -C "/var/tmp/akamai-validation" "${TOOL_NAME}-${VARIANT}-${STAMP}"
  echo "DEBUG BUNDLE: ${BUNDLE_DIR}"
  echo "DEBUG BUNDLE TAR: ${TGZ}"
fi
