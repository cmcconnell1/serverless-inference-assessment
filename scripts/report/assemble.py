#!/usr/bin/env python3
"""assemble.py

Concatenate the assessment chapters and selected evidence tables into one
Markdown source for the PDF build. The full report reads docs/ and appends the
evidence tables; the brief reads brief/ with --chapters and --no-appendix. Each chapter is wrapped in a fenced div
with a stable id (ch-00, ch-01, ..., ch-04b) so cross-document links can be
rewritten to in-document anchors. Evidence tables are demoted one heading
level, wrapped as ev-<name>, and trimmed of bulk lists that belong in the
repository rather than the report.

Usage: assemble.py [-h] --root DIR --out FILE [--meta FILE] [--chapters GLOB] [--no-appendix]
"""

import argparse
import glob
import json
import os
import re
import sys

CHAPTER_GLOB = "docs/[0-9][0-9]*.md"
EVIDENCE = [
    ("latency", "Connection-phase latency"),
    ("dns-cdn", "DNS, ASN, and hosting fingerprints"),
    ("status-incidents", "Status page incidents"),
    ("deepinfra-catalog", "DeepInfra catalog analysis"),
    ("akamai-regions", "Akamai Cloud regions"),
]
EXCLUDED_EVIDENCE = ["api-surface", "openapi-surface"]
DROP_LINE = re.compile(r"^(Leaf component names:|Groups:)")
DETAILS_OPEN = re.compile(r"^<details>")
DETAILS_CLOSE = re.compile(r"^</details>")


def chapter_id(path):
    """Return ch-<prefix> for docs/NN[a-z]-title.md."""
    m = re.match(r"(\d\d[a-z]?)-", os.path.basename(path))
    return f"ch-{m.group(1)}" if m else None


def shift_headings(text, by):
    """Demote ATX headings outside fenced code blocks by the given number of levels."""
    out, fence = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,5} ", line):
            line = "#" * by + line
        out.append(line)
    return "\n".join(out)


def trim_evidence(text):
    """Remove collapsible path lists and bulk component-name lines."""
    out, skip = [], False
    for line in text.splitlines():
        if DETAILS_OPEN.match(line):
            skip = True
            continue
        if DETAILS_CLOSE.match(line):
            skip = False
            continue
        if skip or DROP_LINE.match(line):
            continue
        out.append(line)
    return "\n".join(out)


def capture_window(root):
    """Earliest and latest captured_utc across all probe .meta files."""
    stamps = []
    for meta in glob.glob(os.path.join(root, "evidence", "probes", "*", "*.meta")):
        with open(meta, encoding="utf-8") as f:
            for line in f:
                if line.startswith("captured_utc:"):
                    stamps.append(line.split(":", 1)[1].strip())
    return (min(stamps), max(stamps)) if stamps else ("unknown", "unknown")


def evidence_dates(root, probe_first, probe_last):
    """UTC dates of every evidence source: probes, browser checks, and the source-check run.

    Probes are not the only evidence: pages that block scripted clients are
    read in a browser (evidence/manual/browser-checked-urls.tsv), and the
    source check runs after both. The cover date range must cover all three,
    so the caller takes min() and max() of this list.
    """
    dates = [d[:10] for d in (probe_first, probe_last) if d != "unknown"]
    tsv = os.path.join(root, "evidence", "manual", "browser-checked-urls.tsv")
    if os.path.exists(tsv):
        with open(tsv, encoding="utf-8") as f:
            next(f, None)
            for line in f:
                cols = line.rstrip("\n").split("\t")
                if len(cols) > 1 and re.match(r"^\d{4}-\d{2}-\d{2}$", cols[1]):
                    dates.append(cols[1])
    check = os.path.join(root, "evidence", "derived", "source-check.md")
    if os.path.exists(check):
        with open(check, encoding="utf-8") as f:
            m = re.search(r"^Run: (\d{4}-\d{2}-\d{2}) ", f.read(), re.M)
            if m:
                dates.append(m.group(1))
    return dates


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="repository root")
    ap.add_argument("--out", required=True, help="combined Markdown output path")
    ap.add_argument("--meta", help="write a JSON summary of what was assembled")
    ap.add_argument("--chapters", default=CHAPTER_GLOB,
                    help=f"chapter glob relative to --root (default: {CHAPTER_GLOB})")
    ap.add_argument("--no-appendix", action="store_true", help="omit the evidence table appendix")
    args = ap.parse_args()

    chapters = sorted(glob.glob(os.path.join(args.root, args.chapters)))
    if not chapters:
        sys.exit(f"[ERROR] no chapters match {args.root}/{args.chapters}")
    parts = []
    for path in chapters:
        cid = chapter_id(path)
        with open(path, encoding="utf-8") as f:
            body = f.read().rstrip()
        parts.append(f"::: {{#{cid} .chapter .{cid}}}\n\n{body}\n\n:::\n")

    included = []
    if args.no_appendix:
        return finish(args, chapters, parts, included)
    parts.append("::: {#appendix-evidence .chapter .appendix}\n\n# Appendix: Evidence Tables\n\n"
                 "Generated by `scripts/summarize_probes.py` from the raw captures in `evidence/probes/`. "
                 "The full API surface and OpenAPI path lists are omitted here and remain in the repository: "
                 + ", ".join(f"`evidence/derived/{n}.md`" for n in EXCLUDED_EVIDENCE) + ".\n\n:::\n")
    for name, _title in EVIDENCE:
        path = os.path.join(args.root, "evidence", "derived", f"{name}.md")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            body = shift_headings(trim_evidence(f.read().rstrip()), 1)
        parts.append(f"::: {{#ev-{name} .evidence}}\n\n{body}\n\n:::\n")
        included.append(name)
    return finish(args, chapters, parts, included)


def finish(args, chapters, parts, included):
    """Write the combined Markdown and the JSON summary."""
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    first, last = capture_window(args.root)
    dates = evidence_dates(args.root, first, last)
    summary = {
        "chapters": [os.path.relpath(p, args.root) for p in chapters],
        "evidence_included": included,
        "evidence_excluded": EXCLUDED_EVIDENCE,
        "capture_first_utc": first,
        "capture_last_utc": last,
        "evidence_first_date_utc": min(dates) if dates else "unknown",
        "evidence_last_date_utc": max(dates) if dates else "unknown",
    }
    if args.meta:
        with open(args.meta, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
