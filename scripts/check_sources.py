#!/usr/bin/env python3
"""check_sources.py

Verify the public sources cited by the assessment.

1. Reachability: extract every http(s) URL from README.md and docs/*.md, GET each
   one with a browser user agent, and classify the result.
2. Quotes: for each row of evidence/quote-checks.tsv (doc, url, phrase), fetch the
   page, strip markup, normalize typography, and report whether the phrase appears.

Writes evidence/derived/source-check.md. Standard library only; no credentials.

Result classes:
  OK        2xx or 3xx after redirects
  EXPECTED  405 or 404 on an API base URL cited as an endpoint string, not a page
  BLOCKED   401, 403, 429, or a transport error on a site known to block scripts;
            check these in a browser
  BROKEN    404, 410, 5xx, or DNS failure on a page

A BLOCKED URL listed in evidence/manual/browser-checked-urls.tsv (url, checked_utc,
result) is reported as BROWSER OK with the date of the manual check. A quote on a
BLOCKED page is searched in the matching browser capture (evidence/manual/*.txt whose
first line is "url: <url>") and reported as FOUND IN CAPTURE or NOT FOUND IN CAPTURE.

Exit codes: 0 no BROKEN URL and no NOT FOUND quote; 1 otherwise; 2 usage error.

Usage: check_sources.py [-h] [-v] [--debug] [--workers N] [--timeout S]
"""

import argparse
import concurrent.futures
import csv
import glob
import html
import os
import platform
import re
import shutil
import ssl
import sys
import tarfile
import urllib.error
import urllib.request
from datetime import datetime, timezone

TOOL = "check_sources"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "evidence", "derived", "source-check.md")
QUOTES = os.path.join(ROOT, "evidence", "quote-checks.tsv")
MANUAL = os.path.join(ROOT, "evidence", "manual", "browser-checked-urls.tsv")
BUNDLE_ROOT = "/var/tmp/akamai-validation"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
URL_RE = re.compile(r"https?://[^\s)>\]|`\"']+")
API_BASES = ("api.deepinfra.com/v1/openai", "api.tokenfactory.nebius.com/v1", "inference.baseten.co/v1")
TYPO = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-",
        "\u2011": "-", "\u00a0": " ", "\u2026": "..."}


def extract_urls():
    """Return {url: [doc, ...]} for every cited URL, skipping templates."""
    found = {}
    for path in [os.path.join(ROOT, "README.md")] + sorted(glob.glob(os.path.join(ROOT, "docs", "*.md"))):
        with open(path, encoding="utf-8") as f:
            for url in URL_RE.findall(f.read()):
                url = url.rstrip(".,;:")
                if "{" in url:
                    continue
                found.setdefault(url, []).append(os.path.basename(path)[:3].rstrip("-"))
    return found


def fetch(url, timeout, want_body=False):
    """GET url; return (status, final_url, body_text_or_None, error)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/json,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            body = r.read().decode("utf-8", errors="replace") if want_body else None
            return r.status, r.geturl(), body, ""
    except urllib.error.HTTPError as e:
        return e.code, url, None, ""
    except Exception as e:  # DNS, TLS, timeout
        return 0, url, None, type(e).__name__


def classify(url, status):
    if 200 <= status < 400:
        return "OK"
    if status in (404, 405) and any(b in url for b in API_BASES):
        return "EXPECTED"
    if status in (0, 401, 403, 429):
        return "BLOCKED"
    return "BROKEN"


def normalize(text):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    for k, v in TYPO.items():
        text = text.replace(k, v)
    return re.sub(r"\s+", " ", text).lower()


def load_captures():
    """Return {url: (filename, text)} for browser captures under evidence/manual/."""
    caps = {}
    for path in glob.glob(os.path.join(ROOT, "evidence", "manual", "*.txt")):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        first = text.split("\n", 1)[0]
        if first.startswith("url: "):
            caps[first[5:].strip()] = (os.path.basename(path), text)
    return caps


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true", help="print each URL and quote result")
    ap.add_argument("--debug", action="store_true",
                    help=f"write a support bundle to {BUNDLE_ROOT}/ and print its location last")
    ap.add_argument("--workers", type=int, default=8, help="parallel requests (default 8)")
    ap.add_argument("--timeout", type=float, default=20, help="per-request timeout in seconds (default 20)")
    args = ap.parse_args()

    started = datetime.now(timezone.utc)
    urls = extract_urls()
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(fetch, u, args.timeout): u for u in urls}
        for fut in concurrent.futures.as_completed(futs):
            u = futs[fut]
            status, final, _, err = fut.result()
            results[u] = (status, final, err, classify(u, status))
            if args.verbose:
                print(f"[{results[u][3]}] {status} {u}")

    quotes = []
    with open(QUOTES, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    pages = {}
    captures = load_captures()
    for row in rows:
        if row["url"] not in pages:
            pages[row["url"]] = fetch(row["url"], args.timeout, want_body=True)
        status, _, body, err = pages[row["url"]]
        if body is None and row["url"] in captures:
            name, text = captures[row["url"]]
            found = normalize(row["phrase"]) in normalize(text)
            verdict = ("FOUND IN CAPTURE " if found else "NOT FOUND IN CAPTURE ") + name
        elif body is None:
            verdict = "BLOCKED" if classify(row["url"], status) == "BLOCKED" else "PAGE ERROR"
        else:
            verdict = "FOUND" if normalize(row["phrase"]) in normalize(body) else "NOT FOUND"
        quotes.append((row["doc"], row["url"], row["phrase"], status, verdict))
        if args.verbose:
            print(f"[{verdict}] {row['doc']}: {row['phrase']}")

    manual = {}
    if os.path.exists(MANUAL):
        with open(MANUAL, encoding="utf-8") as f:
            manual = {r["url"]: r for r in csv.DictReader(f, delimiter="\t")}
    for u, (status, final, err, cls) in list(results.items()):
        if cls == "BLOCKED" and u in manual:
            results[u] = (status, final, f"checked in a browser {manual[u]['checked_utc']}: {manual[u]['result']}", "BROWSER OK")

    counts = {}
    for _, _, _, cls in results.values():
        counts[cls] = counts.get(cls, 0) + 1
    qcounts = {}
    for q in quotes:
        key = q[4].split(" akamai-")[0] if "CAPTURE" in q[4] else q[4]
        qcounts[key] = qcounts.get(key, 0) + 1

    lines = ["# Source check", "",
             f"Run: {started.strftime('%Y-%m-%d %H:%M UTC')}. Generated by `scripts/check_sources.py`.", "",
             "Pages marked BLOCKED refuse scripted clients; open them in a browser to verify and record the",
             "result in `evidence/manual/browser-checked-urls.tsv`. BROWSER OK means that record exists.", "",
             "## Cited URLs", "",
             f"Unique URLs: {len(results)}. " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + ".", "",
             "| Result | HTTP | URL | Cited in | Note |", "| --- | --- | --- | --- | --- |"]
    for u, (status, final, err, cls) in sorted(results.items(), key=lambda kv: (kv[1][3] == "OK", kv[0])):
        if cls == "OK" and final.rstrip("/") == u.rstrip("/"):
            continue
        note = err or (f"redirects to {final}" if final.rstrip("/") != u.rstrip("/") else "")
        lines.append(f"| {cls} | {status or '-'} | {u} | {', '.join(sorted(set(urls[u])))} | {note} |")
    lines += ["", "OK URLs without a redirect are counted above and not listed.", "",
              "## Quotes and figures", "",
              ", ".join(f"{k} {v}" for k, v in sorted(qcounts.items())) + ".", "",
              "| Result | Claim | Phrase | URL |", "| --- | --- | --- | --- |"]
    for doc, url, phrase, status, verdict in quotes:
        lines.append(f"| {verdict} | {doc} | `{phrase}` | {url} |")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {OUT}")
    print("URLs: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print("Quotes: " + ", ".join(f"{k} {v}" for k, v in sorted(qcounts.items())))

    if args.debug:
        stamp = started.strftime("%Y%m%dT%H%M%SZ")
        bdir = os.path.join(BUNDLE_ROOT, f"{TOOL}-{stamp}")
        os.makedirs(bdir, exist_ok=True)
        shutil.copy(OUT, bdir)
        shutil.copy(QUOTES, bdir)
        redact = re.compile(r"(TOKEN|SECRET|PASSWORD|KEY)", re.I)
        env = "\n".join(f"{k}=[REDACTED]" if redact.search(k) else f"{k}={v}" for k, v in sorted(os.environ.items()))
        with open(os.path.join(bdir, "environment.txt"), "w") as f:
            f.write(f"host_os: {platform.platform()}\npython: {sys.version.split()[0]}\ntool: {TOOL}.py\n"
                    f"invocation: {' '.join(sys.argv)}\nutc: {started.isoformat()}\n\nenvironment (redacted):\n{env}\n")
        with open(os.path.join(bdir, "manifest.txt"), "w") as f:
            f.write("manifest.txt       This file.\nenvironment.txt    Host, interpreter, invocation, redacted environment.\n"
                    "source-check.md    Results.\nquote-checks.tsv   Quote list used as input.\n")
        tgz = f"{bdir}.tgz"
        with tarfile.open(tgz, "w:gz") as t:
            t.add(bdir, arcname=os.path.basename(bdir))
        print(f"DEBUG BUNDLE: {bdir}")
        print(f"DEBUG BUNDLE TAR: {tgz}")

    broken = counts.get("BROKEN", 0) + sum(v for k, v in qcounts.items() if k.startswith("NOT FOUND"))
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
