#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter —— English EPUB generator (Python standard library only)

Parses en/book/*.md (the English six-field edition) and produces a clean EPUB:
  HowToInvestBetter-en.epub

Usage:
  python3 tools/build_en_epub.py
"""
import os
import re
import glob
import zipfile
import datetime
import html as _html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "en", "book")
OUT = os.path.join(ROOT, "HowToInvestBetter-en.epub")

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
TAG_RE = re.compile(r"^<!--\s*tags:\s*(.+?)\s*-->$")
FIELD_RE = re.compile(r"^-\s*(Cost|In plain terms|Payoff|Evidence grade|Sources|Note)[：:]\s*(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$")
FIELDS = ["Cost", "In plain terms", "Payoff", "Evidence grade", "Sources", "Note"]
TAG_LABEL = {
    "money": "Money", "time": "Time", "will": "Willpower",
    "payoff": "Payoff", "scope": "Scope", "impact": "Impact",
}
TAG_VAL_MAP = {
    "money": {"0": "none", "little": "little", "mid": "mid", "high": "high"},
    "time": {"0": "none", "little": "little", "some": "some"},
    "will": {"no": "no", "some": "some", "much": "much"},
    "payoff": {"low": "low", "mid": "mid", "high": "high"},
    "scope": {"money": "money", "time": "time", "health": "health",
              "relationship": "relationship", "energy": "energy"},
    "impact": {"self": "self", "family": "family", "self+family": "self+family"},
}

TITLE = "A High-Value Investment Guidebook"
SUB = "What it costs, what it returns, how strong the evidence is"
AUTHOR = "leo-bone"
UID = "howtoinvestbetter-en-2026"


def parse_book():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    chapters = []
    for path in files:
        num = int(os.path.basename(path).split("-", 1)[0])
        lines = open(path, encoding="utf-8").read().split("\n")
        title = None
        intro = []
        entries = []
        items = []
        cur = None
        for line in lines:
            m = HEAD_RE.match(line)
            if m and title is None and not line.startswith("##"):
                title = m.group(1).strip()
                continue
            m = ENTRY_RE.match(line)
            if m:
                if cur:
                    entries.append(cur)
                cur = {"num": int(m.group(1)), "title": m.group(2).strip(),
                       "tags": {}, "fields": {}}
                continue
            tm = TAG_RE.match(line)
            if tm and cur is not None:
                for part in re.split(r"\s+", tm.group(1).strip()):
                    if "=" in part:
                        k, v = part.split("=", 1)
                        cur["tags"][k.strip()] = v.strip()
                continue
            if cur is not None:
                fm = FIELD_RE.match(line)
                if fm:
                    cur["fields"][fm.group(1)] = fm.group(2).strip()
                    continue
                if line.strip() == "":
                    continue
            else:
                if line.strip() == "":
                    continue
                bm = BULLET_RE.match(line)
                if bm:
                    items.append(bm.group(1).strip())
                elif title is not None:
                    intro.append(line.strip())
        if cur:
            entries.append(cur)
        chapters.append((num, title or "Untitled", intro, entries, items))
    return chapters


def esc(s):
    return _html.escape(s or "", quote=True)


def tagline(tags):
    parts = []
    for key in ["money", "time", "will", "payoff", "scope", "impact"]:
        v = tags.get(key)
        if v:
            parts.append("%s: %s" % (TAG_LABEL[key], TAG_VAL_MAP.get(key, {}).get(v, v)))
    return " ｜ ".join(parts)


def chapter_xhtml(num, title, intro, entries, items):
    parts = ['<?xml version="1.0" encoding="utf-8"?>']
    parts.append('<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">')
    parts.append("<head><title>%s</title></head><body>" % esc(title))
    parts.append('<h1 class="ch">%s</h1>' % esc(title))
    for para in intro:
        parts.append('<p class="intro">%s</p>' % esc(para))
    if entries:
        for e in entries:
            parts.append('<div class="entry">')
            parts.append('<h3>%d. %s</h3>' % (e["num"], esc(e["title"])))
            tl = tagline(e["tags"])
            if tl:
                parts.append('<p class="meta">%s</p>' % esc(tl))
            for k in FIELDS:
                v = e["fields"].get(k)
                if v:
                    parts.append('<p><b>%s:</b> %s</p>' % (esc(k), esc(v)))
            parts.append('</div>')
    else:
        parts.append('<ul class="revlist">')
        for it in items:
            parts.append('<li>%s</li>' % esc(it))
        parts.append('</ul>')
    parts.append("</body></html>")
    return "\n".join(parts)


CSS = """
body{font-family:Georgia,"Times New Roman","Noto Serif CJK SC",serif;line-height:1.8;margin:1.2em;color:#1a1a1a;}
h1.ch{font-size:1.5em;border-bottom:2px solid #c0392b;padding-bottom:.3em;margin-bottom:.6em;}
h2.ch2{font-size:1.15em;color:#111;margin:.9em 0 .3em;}
.cp{color:#444;font-size:.92em;}
.intro{color:#444;font-size:.95em;}
.entry{border-left:3px solid #e0e0e0;padding-left:.9em;margin:1.1em 0;}
.entry h3{font-size:1.12em;margin:.5em 0 .2em;color:#111;}
.meta{font-size:.78em;color:#888;margin:.1em 0 .5em;}
.note{color:#b8860b;}
b{color:#c0392b;}
.revlist li{margin:.4em 0;}
"""

COVER = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>%s</title></head>
<body style="text-align:center;padding-top:4em;">
<h1 style="font-size:2em;color:#c0392b;">%s</h1>
<p style="font-size:1.1em;">%s</p>
<p style="color:#777;">Open source · CC BY 4.0</p>
</body></html>""" % (esc(TITLE), esc(TITLE), esc(SUB))


def preface_xhtml():
    return """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Introduction</title></head>
<body>
<h1 class="ch">Introduction · How to Read This Guidebook</h1>
<p class="intro">This is an evidence-based investment handbook. It recommends no specific product; it simply lists "high-value moves" that have been validated by statistics, research, and regulatory documents, arranged as a checklist you can follow entry by entry. Every entry uses the same ledger: what it costs, what it returns, how strong the evidence is, and where the sources come from.</p>
<h3>Four questions</h3>
<p class="intro">1. What does it cost? Money, time, willpower, or a permanent loss of principal?</p>
<p class="intro">2. What does it return? Long-term real return, lower volatility, tax &amp; fee savings, or avoidance of total loss?</p>
<p class="intro">3. How strong is the evidence? See the evidence grades below.</p>
<p class="intro">4. Where do the sources come from? Only academic journal papers and official documents are cited — never self-media or marketing accounts.</p>
<h3>Evidence grades</h3>
<p class="intro">[A] Authoritative long-term statistics (S&amp;P SPIVA, exchange yearbooks), randomized/longitudinal studies in top journals, official regulatory documents.</p>
<p class="intro">[B] Individual high-quality studies, backtest reports from authoritative institutions (Vanguard / Dalbar / Ibbotson), classic papers.</p>
<p class="intro">[C] Reasonable inference or broad consensus — logically sound but not forced to a precise citation.</p>
<h3>The Three-Zeros principle (the highest-value hard standard)</h3>
<p class="intro">An action is "Three Zeros" if cost = none, time = none, and willpower = none — all three costs are zero. Exactly 16 entries meet this strictly; do them first without overthinking. Many more fall in the high-value tier of "two zeros and one very low cost," which you can dig out on the search page by filtering each of cost / time / willpower to "none."</p>
<h3>Reading advice</h3>
<p class="intro">You don't have to do it all — this is a menu, not a to-do list. Take even one or two items and it counts. To save time, filter by "Three Zeros only" first; within each chapter entries are ranked from highest to lowest value, so start with the first few; if you can't follow the numbers, just read the "In plain terms" line of each entry.</p>
</body></html>"""


def license_xhtml():
    return """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>License</title></head>
<body>
<h1 class="ch">License &amp; Disclaimer</h1>
<p class="intro">The main content of this guidebook is licensed under <b>CC BY 4.0</b> (Creative Commons Attribution 4.0 International). You are free to share, adapt, and use it commercially, provided you give appropriate credit to the author, <b>%s</b>, and indicate if changes were made. The code (search page, build scripts) is licensed under MIT.</p>
<p class="intro">This guidebook is an independently authored, evidence-based methodology handbook and is <b>not</b> investment advice from any institution or individual. All citations follow each organization's latest official releases. Markets carry risk; decisions require independent judgment and consultation with a licensed professional.</p>
<p class="intro">This is an open-source edition. The latest version and the Chinese original are maintained at <b>github.com/leo-bone/HowToInvestBetter</b>.</p>
</body></html>""" % esc(AUTHOR)


def build():
    chapters = parse_book()
    chapters = [c for c in chapters if c[3] or c[4]]
    today = datetime.date.today().isoformat()

    opf_items, ncx_points, xhtml_files = [], [], []
    xhtml_files.append(("cover.xhtml", COVER))
    opf_items.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
    ncx_points.append('<navPoint id="np-cover" playOrder="1"><navLabel><text>Cover</text></navLabel><content src="cover.xhtml"/></navPoint>')

    xhtml_files.append(("license.xhtml", license_xhtml()))
    opf_items.append('<item id="license" href="license.xhtml" media-type="application/xhtml+xml"/>')
    ncx_points.append('<navPoint id="np-license" playOrder="2"><navLabel><text>License</text></navLabel><content src="license.xhtml"/></navPoint>')

    xhtml_files.append(("preface.xhtml", preface_xhtml()))
    opf_items.append('<item id="preface" href="preface.xhtml" media-type="application/xhtml+xml"/>')
    ncx_points.append('<navPoint id="np-preface" playOrder="3"><navLabel><text>Introduction</text></navLabel><content src="preface.xhtml"/></navPoint>')

    play = 4
    titles = {"cover.xhtml": "Cover", "license.xhtml": "License", "preface.xhtml": "Introduction"}
    for num, title, intro, entries, items in chapters:
        fn = "ch%02d.xhtml" % num
        titles[fn] = title
        xhtml_files.append((fn, chapter_xhtml(num, title, intro, entries, items)))
        opf_items.append('<item id="ch%d" href="%s" media-type="application/xhtml+xml"/>' % (num, fn))
        ncx_points.append('<navPoint id="np-%d" playOrder="%d"><navLabel><text>%s</text></navLabel><content src="%s"/></navPoint>' % (num, play, esc(title), fn))
        play += 1

    manifest = "\n    ".join(opf_items)
    spine = "\n    ".join('<itemref idref="%s"/>' % (fn.replace(".xhtml", "")) for fn, _ in xhtml_files)
    opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:uuid:%s</dc:identifier>
    <dc:title>%s</dc:title>
    <dc:creator>%s</dc:creator>
    <dc:language>en</dc:language>
    <dc:date>%s</dc:date>
    <meta property="dcterms:modified">%sT00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="styles.css" media-type="text/css"/>
        %s
  </manifest>
  <spine>
    %s
  </spine>
</package>""" % (UID, esc(TITLE), esc(AUTHOR), today, today, manifest, spine)

    nav_li = "\n".join('<li><a href="%s">%s</a></li>' % (fn, esc(titles.get(fn, fn))) for fn, _ in xhtml_files)
    nav = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.w3.org/2009/opf">
<head><title>Contents</title></head>
<body>
<nav epub:type="toc" id="toc">
<h1>Contents</h1>
<ol>%s</ol>
</nav>
</body></html>""" % nav_li

    ncx = """<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="dtb:uid" content="urn:uuid:%s"/>
<meta name="dtb:depth" content="1"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle><text>%s</text></docTitle>
<navMap>
%s
</navMap>
</ncx>""" % (UID, esc(TITLE), "\n".join(ncx_points))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/nav.xhtml", nav)
        z.writestr("OEBPS/toc.ncx", ncx)
        z.writestr("OEBPS/styles.css", CSS)
        for fn, content in xhtml_files:
            z.writestr("OEBPS/" + fn, content)

    total_entries = sum(len(c[3]) for c in chapters)
    print("✅ Generated %s" % OUT)
    print("   Chapters: %d | Entries: %d" % (len(chapters), total_entries))


if __name__ == "__main__":
    build()
