#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter —— EPUB 生成器（仅依赖 Python 标准库）

解析 book/ 下的章节 Markdown，生成一份排版干净的 EPUB 电子书：
  HowToInvestBetter.epub

EPUB = zip(mimetype + META-INF/container.xml + OEBPS/*.xhtml + content.opf + toc.ncx)

用法：
  python3 tools/build_epub.py
"""
import os
import re
import glob
import zipfile
import datetime
import html as _html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
OUT = os.path.join(ROOT, "HowToInvestBetter.epub")

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(
    r"^##\s+(\d+)\s+(.+?)\s*"
    r"〔([ABC])〕〔影响：([^〕]+)〕〔花费：([^〕]+)〕〔时间：([^〕]+)〕〔毅力：([^〕]+)〕\s*$"
)
FIELD_RE = re.compile(r"^\*\*(花掉|换回|出处|说人话)\*\*[：:]\s*(.*)$")
NOTE_RE = re.compile(r"^>\s*〔([^〕]+)〕\s*(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$")

TITLE = "高性价比投资指南"
AUTHOR = "HowToInvestBetter 项目（仿《高性价比人生指南》体例）"
UID = "howtoinvestbetter-2026"


def parse_book():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    chapters = []
    for path in files:
        num = int(os.path.basename(path).split("-", 1)[0])
        lines = open(path, encoding="utf-8").read().split("\n")
        title = None
        entries = []
        items = []
        cur = None
        for line in lines:
            m = HEAD_RE.match(line)
            if m and title is None:
                title = m.group(1).strip()
                continue
            m = ENTRY_RE.match(line)
            if m:
                if cur:
                    entries.append(cur)
                cur = {
                    "num": int(m.group(1)),
                    "title": m.group(2).strip(),
                    "grade": m.group(3),
                    "impact": m.group(4).strip(),
                    "cost_money": m.group(5).strip(),
                    "cost_time": m.group(6).strip(),
                    "cost_will": m.group(7).strip(),
                    "fields": {},
                    "notes": [],
                }
                continue
            if cur is not None:
                fm = FIELD_RE.match(line)
                if fm:
                    cur["fields"][fm.group(1)] = fm.group(2).strip()
                    continue
                nm = NOTE_RE.match(line)
                if nm:
                    cur["notes"].append((nm.group(1).strip(), nm.group(2).strip()))
                    continue
                if BULLET_RE.match(line):
                    continue
                if line.strip() == "":
                    continue
            else:
                bm = BULLET_RE.match(line)
                if bm and title is not None:
                    items.append(bm.group(1).strip())
        if cur:
            entries.append(cur)
        chapters.append((num, title or "未命名", entries, items))
    return chapters


def esc(s):
    return _html.escape(s or "", quote=True)


GRADE_LABEL = {"A": "证据 A · 权威统计/顶刊/官方文件", "B": "证据 B · 单项研究/机构报告", "C": "证据 C · 合理推论/广泛共识"}


def chapter_xhtml(num, title, entries, items):
    parts = ['<?xml version="1.0" encoding="utf-8"?>']
    parts.append('<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">')
    parts.append("<head><title>%s</title></head><body>" % esc(title))
    parts.append('<h1 class="ch">%s</h1>' % esc(title))
    if entries:
        for e in entries:
            parts.append('<div class="entry">')
            parts.append('<h2>%d. %s</h2>' % (e["num"], esc(e["title"])))
            parts.append('<p class="meta">%s ｜ 影响：%s ｜ 花费：%s 时间：%s 毅力：%s</p>' % (
                esc(GRADE_LABEL[e["grade"]]), esc(e["impact"]),
                esc(e["cost_money"]), esc(e["cost_time"]), esc(e["cost_will"])))
            for k in ("花掉", "换回", "出处", "说人话"):
                if e["fields"].get(k):
                    parts.append('<p><b>%s：</b>%s</p>' % (k, esc(e["fields"][k])))
            for typ, txt in e["notes"]:
                parts.append('<p class="note">〔%s〕 %s</p>' % (esc(typ), esc(txt)))
            parts.append('</div>')
    else:
        parts.append('<ul class="revlist">')
        for it in items:
            parts.append('<li>%s</li>' % esc(it))
        parts.append('</ul>')
    parts.append("</body></html>")
    return "\n".join(parts)


CSS = """
body{font-family:"Noto Serif CJK SC","Songti SC",serif;line-height:1.8;margin:1.2em;color:#1a1a1a;}
h1.ch{font-size:1.5em;border-bottom:2px solid #c0392b;padding-bottom:.3em;margin-bottom:.6em;}
.entry{border-left:3px solid #e0e0e0;padding-left:.8em;margin:1em 0;}
.entry h2{font-size:1.15em;margin:.4em 0;color:#222;}
.meta{font-size:.8em;color:#777;margin:.2em 0 .6em;}
.meta,.note{font-size:.82em;}
.note{color:#b8860b;font-style:italic;}
b{color:#c0392b;}
.revlist li{margin:.4em 0;}
"""

COVER = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>%s</title></head>
<body style="text-align:center;padding-top:4em;">
<h1 style="font-size:2em;color:#c0392b;">%s</h1>
<p style="font-size:1.1em;">花掉什么，换回什么，证据有多硬</p>
<p style="color:#777;">仿《高性价比人生指南》体例 · 开源 · CC BY 4.0</p>
</body></html>""" % (esc(TITLE), esc(TITLE))


def build():
    chapters = parse_book()
    # 只保留有正文（条目或清单）的章
    chapters = [c for c in chapters if c[2] or c[3]]
    today = datetime.date.today().isoformat()

    opf_items = []
    ncx_points = []
    xhtml_files = []

    # cover
    xhtml_files.append(("cover.xhtml", COVER))
    opf_items.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
    ncx_points.append('<navPoint id="np-cover" playOrder="1"><navLabel><text>封面</text></navLabel><content src="cover.xhtml"/></navPoint>')

    play = 2
    for i, (num, title, entries, items) in enumerate(chapters):
        fn = "ch%02d.xhtml" % num
        xhtml_files.append((fn, chapter_xhtml(num, title, entries, items)))
        opf_items.append('<item id="ch%d" href="%s" media-type="application/xhtml+xml"/>' % (num, fn))
        ncx_points.append('<navPoint id="np-%d" playOrder="%d"><navLabel><text>%s</text></navLabel><content src="%s"/></navPoint>' % (num, play, esc(title), fn))
        play += 1

    # content.opf
    manifest = "\n    ".join(opf_items)
    spine = "\n    ".join('<itemref idref="%s"/>' % (
        "cover" if fn == "cover.xhtml" else fn.replace(".xhtml", "")) for fn, _ in xhtml_files)
    opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:uuid:%s</dc:identifier>
    <dc:title>%s</dc:title>
    <dc:creator>%s</dc:creator>
    <dc:language>zh-CN</dc:language>
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

    # nav.xhtml (EPUB3 TOC)
    nav_li = "\n".join('<li><a href="%s">%s</a></li>' % (
        fn if fn == "cover.xhtml" else fn, esc(title) if fn == "cover.xhtml" else esc(title)) for fn, _ in xhtml_files)
    nav = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/epub">
<head><title>目录</title></head>
<body>
<nav epub:type="toc" id="toc">
<h1>目录</h1>
<ol>%s</ol>
</nav>
</body></html>""" % nav_li

    # toc.ncx (EPUB2 fallback)
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

    # 打包
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

    total_entries = sum(len(c[2]) for c in chapters)
    print("✅ 已生成 %s" % OUT)
    print("   章节：%d ｜ 条目：%d" % (len(chapters), total_entries))


if __name__ == "__main__":
    build()
