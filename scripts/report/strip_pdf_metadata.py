#!/usr/bin/env python3
"""strip_pdf_metadata.py

Rewrite a PDF with no document information dictionary entries other than an
optional Title and Author, no XMP metadata stream, and a deterministic file identifier.
The file is fully re-serialized, so no earlier revision of the metadata
survives in an incremental update section.

With --headings, also repair the bookmark titles. Chrome builds the PDF
outline from rendered line boxes and joins them without a separator, so a
heading that wraps in the layout reaches the bookmark panel with the space at
the wrap point missing ("Part A: ProductManagement Brief"). Each outline title
is matched to the true heading text by comparing both with all whitespace
removed, which is an exact comparison rather than a guess at where a space
belongs.

Usage: strip_pdf_metadata.py [-h] [--title TEXT] [--author TEXT] [--headings FILE] INPUT OUTPUT
Requires: pikepdf (run through uv with a pinned version by build_report.sh).
"""

import argparse
import sys

try:
    import pikepdf
except ImportError:  # keep -h usable without pikepdf installed
    pikepdf = None


def squash(text):
    """Return the text with every run of whitespace removed."""
    return "".join(text.split())


def load_headings(path):
    """Map whitespace-free heading text to the heading as written."""
    table = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            heading = line.strip()
            if heading:
                table.setdefault(squash(heading), heading)
    return table


def walk_outline(node, visit):
    """Call visit on every outline item reachable from node, once each."""
    seen = set()
    stack = [node.get("/First")]
    while stack:
        item = stack.pop()
        while item is not None:
            key = item.objgen
            if key in seen:
                break
            seen.add(key)
            visit(item)
            if "/First" in item:
                stack.append(item.get("/First"))
            item = item.get("/Next")


def match_heading(table, current):
    """Return the true heading for a bookmark title, or None.

    Chrome can also repeat a heading's first line box in the title: a one-line
    heading comes out doubled ("0. Executive Brief0. Executive Brief") and a
    wrapped one as first line, first line, rest. A title whose leading segment
    repeats immediately matches the heading that remains once the repeat is
    dropped; the comparison is still exact.
    """
    key = squash(current)
    if key in table:
        return table[key]
    for size in range(1, len(key) // 2 + 1):
        if key[:size] == key[size:2 * size] and key[size:] in table:
            return table[key[size:]]
    return None


def repair_outline(pdf, table):
    """Restore bookmark titles to the heading text. Returns (repaired, unmatched titles)."""
    if "/Outlines" not in pdf.Root:
        return 0, []
    repaired, unmatched = [0], []

    def visit(item):
        if "/Title" not in item:
            return
        current = str(item["/Title"])
        correct = match_heading(table, current)
        if correct is None:
            unmatched.append(current)
        elif correct != current:
            item["/Title"] = pikepdf.String(correct)
            repaired[0] += 1

    walk_outline(pdf.Root.Outlines, visit)
    return repaired[0], unmatched


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--title", help="document title to keep in the info dictionary")
    ap.add_argument("--author", help="document author to keep in the info dictionary")
    ap.add_argument("--headings", help="file of true heading texts, one per line, used to repair bookmark titles")
    args = ap.parse_args()
    if pikepdf is None:
        sys.exit("[ERROR] pikepdf not installed; run through uv as build_report.sh does")

    repaired, unmatched = 0, []
    with pikepdf.open(args.input) as pdf:
        if "/Metadata" in pdf.Root:
            del pdf.Root.Metadata
        for key in list(pdf.docinfo.keys()):
            del pdf.docinfo[key]
        if args.title:
            pdf.docinfo["/Title"] = args.title
        if args.author:
            pdf.docinfo["/Author"] = args.author
        if args.headings:
            repaired, unmatched = repair_outline(pdf, load_headings(args.headings))
        pdf.save(args.output, static_id=True, fix_metadata_version=False)

    with pikepdf.open(args.output) as check:
        keys = sorted(str(k) for k in check.docinfo.keys())
        has_xmp = "/Metadata" in check.Root
    allowed = sorted(k for k, v in (("/Title", args.title), ("/Author", args.author)) if v)
    if keys != allowed or has_xmp:
        sys.exit(f"[ERROR] metadata remains: info={keys} xmp={has_xmp}")
    print(f"[OK] metadata stripped: info={keys} xmp={has_xmp}")
    if args.headings:
        print(f"[OK] bookmark titles repaired: {repaired}, unmatched: {len(unmatched)}")
        for title in unmatched:
            print(f"[WARNING] unmatched bookmark title: {title}")


if __name__ == "__main__":
    main()
