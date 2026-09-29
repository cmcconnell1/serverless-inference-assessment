#!/usr/bin/env python3
"""toc_pages.py

Write page numbers into the HTML table of contents. Chrome cannot compute
target-counter() when printing, so the build renders the PDF, reads the page
of each named destination (Chrome emits one per link target, named by the
element id), and injects those numbers into the TOC entries of the HTML. The
build repeats until the numbers read back from the PDF match the numbers that
were injected, so a TOC entry that wraps and shifts pagination is corrected.

With --placeholder, no PDF is read: every entry gets "00", which reserves the
width of a two-digit page number for the first render.

Usage: toc_pages.py [-h] [--pdf FILE] [--placeholder] --save JSON HTML_IN HTML_OUT
Requires: pikepdf unless --placeholder (run through uv by build_report.sh).
"""

import argparse
import html
import json
import re
import sys

TOC_LINK = re.compile(r'<a href="#([^"]+)" id="toc-\1">(.*?)</a>', re.S)


def read_pages(pdf_path):
    """Map element id to 1-based page number from the PDF's named destinations."""
    import pikepdf

    pages = {}
    with pikepdf.open(pdf_path) as pdf:
        index = {page.objgen: n for n, page in enumerate(pdf.pages, 1)}
        dests = pdf.Root.get("/Dests")
        if dests is None:
            return pages
        for name, dest in dests.items():
            target = dest[0] if isinstance(dest, pikepdf.Array) else dest.get("/D")[0]
            if target.objgen in index:
                pages[html.unescape(str(name).lstrip("/"))] = index[target.objgen]
    return pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html_in")
    ap.add_argument("html_out")
    ap.add_argument("--pdf", help="rendered PDF to read destination pages from")
    ap.add_argument("--placeholder", action="store_true", help='inject "00" instead of reading a PDF')
    ap.add_argument("--save", required=True, help="write the injected id-to-page map as JSON")
    args = ap.parse_args()
    if not args.placeholder and not args.pdf:
        ap.error("--pdf is required unless --placeholder is given")

    pages = {} if args.placeholder else read_pages(args.pdf)
    source = open(args.html_in, encoding="utf-8").read()
    start = source.find('<nav id="TOC"')
    end = source.find("</nav>", start)
    if start < 0 or end < 0:
        sys.exit("[ERROR] no TOC nav element in the HTML")

    injected, missing = {}, []

    def number(match):
        anchor, text = match.group(1), match.group(2)
        page = "00" if args.placeholder else pages.get(html.unescape(anchor))
        if page is None:
            missing.append(anchor)
            return match.group(0)
        injected[anchor] = page
        return (f'<a href="#{anchor}" id="toc-{anchor}"><span class="toc-text">{text}</span>'
                f'<span class="toc-page">{page}</span></a>')

    toc = TOC_LINK.sub(number, source[start:end])
    with open(args.html_out, "w", encoding="utf-8") as f:
        f.write(source[:start] + toc + source[end:])
    with open(args.save, "w", encoding="utf-8") as f:
        json.dump(injected, f, indent=1, sort_keys=True)
    print(f"[OK] TOC entries numbered: {len(injected)}, without a destination: {len(missing)}")
    if missing:
        print("[WARNING] no destination for: " + ", ".join(missing[:10]))


if __name__ == "__main__":
    main()
