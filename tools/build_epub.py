#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter —— EPUB 生成器（仅依赖 Python 标准库）

解析 book/ 下的章节 Markdown（原书格式），生成一份排版干净的 EPUB 电子书：
  HowToInvestBetter.epub

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
ENTRY_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
TAG_RE = re.compile(r"^<!--\s*标签:\s*(.+?)\s*-->$")
FIELD_RE = re.compile(r"^-\s*(成本|说人话|收益|证据等级|来源|备注)[：:]\s*(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$")
FIELDS = ["成本", "说人话", "收益", "证据等级", "来源", "备注"]

TITLE = "高性价比投资指南"
AUTHOR = "leo"
UID = "7b2d5a91-3c8e-4f17-a5b6-0d9e2c7f4a58"
COPYRIGHT_FILE = os.path.join(ROOT, "版权声明.md")


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
        chapters.append((num, title or "未命名", intro, entries, items))
    return chapters


def esc(s):
    return _html.escape(s or "", quote=True)

def inline(s):
    """先转义，再把正文里轻量 Markdown 的 **粗体** 还原成 HTML。
    中文正文里的单星号（*ST 退市风险警示、204* 债券代码、收益* 等）都是字面符号，
    不做斜体转换，原样保留。"""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s


def _opf_gate(opf_text, written):
    """引用完整性门禁：每个 <itemref> 必须能解析到 manifest 里的 id，
    且 manifest 的每个 href 都必须在包内真实存在。专门拦下
    『manifest id 写成 ch1、spine 却写 ch01』这一类会让 KDP 直接拒收
    （"file is not properly structured / cannot convert"）的错误。"""
    import xml.etree.ElementTree as _ET
    NS = "{http://www.idpf.org/2007/opf}"
    root = _ET.fromstring(opf_text.encode("utf-8"))
    man = root.find(NS + "manifest")
    spine = root.find(NS + "spine")
    ids = {it.get("id") for it in man}
    hrefs = [it.get("href") for it in man if it.get("href")]
    bad = [it.get("idref") for it in spine if it.get("idref") not in ids]
    if bad:
        raise SystemExit("\u274c OPF gate: dangling spine idrefs -> %s" % bad)
    miss = [h for h in hrefs if h not in written]
    if miss:
        raise SystemExit("\u274c OPF gate: manifest hrefs missing from package -> %s" % miss)
    print("\u2705 OPF gate: %d manifest ids / %d spine refs \u5168\u90e8\u80fd\u89e3\u6790" % (len(ids), len(spine)))




def tagline(tags):
    return "钱：%s ｜ 时间：%s ｜ 毅力：%s ｜ 收益：%s ｜ 口径：%s" % (
        esc(tags.get("钱", "")), esc(tags.get("时间", "")), esc(tags.get("毅力", "")),
        esc(tags.get("收益", "")), esc(tags.get("口径", "")))


def chapter_xhtml(num, title, intro, entries, items):
    parts = ['<?xml version="1.0" encoding="utf-8"?>']
    parts.append('<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">')
    parts.append("<head><title>%s</title></head><body>" % esc(title))
    parts.append('<h1 class="ch">%s</h1>' % esc(title))
    for para in intro:
        parts.append('<p class="intro">%s</p>' % inline(para))
    if entries:
        for e in entries:
            parts.append('<div class="entry">')
            parts.append('<h3>%d. %s</h3>' % (e["num"], esc(e["title"])))
            parts.append('<p class="meta">%s</p>' % tagline(e["tags"]))
            for k in FIELDS:
                v = e["fields"].get(k)
                if v:
                    parts.append('<p><b>%s：</b>%s</p>' % (k, inline(v)))
            parts.append('</div>')
    else:
        parts.append('<ul class="revlist">')
        for it in items:
            parts.append('<li>%s</li>' % esc(it))
        parts.append('</ul>')
    parts.append("</body></html>")
    return "\n".join(parts)


CSS = """
body{font-family:"Noto Serif CJK SC","Songti SC",serif;line-height:1.85;margin:1.2em;color:#1a1a1a;}
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

COVER_IMG = os.path.join(ROOT, "cover-book.png")
if not os.path.exists(COVER_IMG):
    COVER_IMG = os.path.join(ROOT, "cover.png")
HAVE_COVER_IMG = os.path.exists(COVER_IMG)

if HAVE_COVER_IMG:
    COVER = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>%s</title></head>
<body style="text-align:center;padding-top:2em;">
<img src="cover.png" style="width:86%%;max-width:520px;" alt="%s"/>
</body></html>""" % (esc(TITLE), esc(TITLE))
else:
    COVER = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>%s</title></head>
<body style="text-align:center;padding-top:4em;">
<h1 style="font-size:2em;color:#c0392b;">%s</h1>
<p style="font-size:1.1em;">花掉什么，换回什么，证据有多硬</p>
<p style="color:#777;">循证投资手册</p>
</body></html>""" % (esc(TITLE), esc(TITLE))


def preface_xhtml():
    return """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>导读</title></head>
<body>
<h1 class="ch">导读 · 怎么读这本指南</h1>
<p class="intro">这是一份循证投资手册。它不推荐任何具体产品，只把经过统计、研究与监管文件验证的“高性价比动作”列成一张可按图索骥的清单。每条都用同一套账本：花掉什么、换回什么、证据多硬、出处哪来。</p>
<h3>四个问题</h3>
<p class="intro">1. 花掉什么？钱、时间、毅力，还是本金的永久性损失？</p>
<p class="intro">2. 换回什么？长期真实回报、更低波动、税费节省，还是避开归零？</p>
<p class="intro">3. 证据多硬？见下方证据等级。</p>
<p class="intro">4. 出处哪来？只引期刊论文与官方文件，不引自媒体与营销号。</p>
<h3>证据等级</h3>
<p class="intro">〔A〕权威长期统计（标普 SPIVA、交易所年鉴）、顶刊随机或追踪研究、官方监管文件。</p>
<p class="intro">〔B〕单项高质量研究、权威机构（Vanguard／Dalbar／Ibbotson）回测报告、经典论文。</p>
<p class="intro">〔C〕合理推论或广泛共识，逻辑硬但未必挂精确出处。</p>
<h3>三零原则（极高性价比死标准）</h3>
<p class="intro">一条动作若“花费等于无、时间等于无、毅力等于否”三项成本全为零，就是“三零”。严格符合的共 16 条，闭眼先做；更多动作是“两项为零、一项极低”的高性价比档，可用检索页按“花费／时间／毅力”分别筛“无”来挖掘。</p>
<h3>阅读建议</h3>
<p class="intro">不用全做，这是备选单不是任务清单。挑走一两条就算数。想省时间先按“仅三零”筛；每章内条目按性价比从高到低排，从每章前几条看起；看不懂就只读每一条的“说人话”一行。</p>
</body></html>"""


def copyright_xhtml():
    if not os.path.exists(COPYRIGHT_FILE):
        return preface_xhtml()
    parts = ['<?xml version="1.0" encoding="utf-8"?>',
             '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">',
             '<head><title>版权声明</title></head><body>']
    in_list = False
    for line in open(COPYRIGHT_FILE, encoding="utf-8").read().split("\n"):
        s = line.rstrip()
        if not s.strip():
            if in_list:
                parts.append("</ul>"); in_list = False
            continue
        s = s.replace("__AUTHOR__", AUTHOR)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(s))
        if s.startswith("## "):
            if in_list:
                parts.append("</ul>"); in_list = False
            parts.append('<h2 class="ch2">%s</h2>' % s[3:])
        elif s.startswith("# "):
            if in_list:
                parts.append("</ul>"); in_list = False
            parts.append('<h1 class="ch">%s</h1>' % s[2:])
        elif s.startswith("- "):
            if not in_list:
                parts.append('<ul class="revlist">'); in_list = True
            parts.append('<li>%s</li>' % s[2:])
        else:
            if in_list:
                parts.append("</ul>"); in_list = False
            parts.append('<p class="cp">%s</p>' % s)
    if in_list:
        parts.append("</ul>")
    parts.append("</body></html>")
    return "\n".join(parts)


def build():
    chapters = parse_book()
    chapters = [c for c in chapters if c[3] or c[4]]
    today = datetime.date.today().isoformat()

    opf_items, ncx_points, xhtml_files = [], [], []
    xhtml_files.append(("cover.xhtml", COVER))
    opf_items.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
    ncx_points.append('<navPoint id="np-cover" playOrder="1"><navLabel><text>封面</text></navLabel><content src="cover.xhtml"/></navPoint>')

    xhtml_files.append(("copyright.xhtml", copyright_xhtml()))
    opf_items.append('<item id="copyright" href="copyright.xhtml" media-type="application/xhtml+xml"/>')
    ncx_points.append('<navPoint id="np-copyright" playOrder="2"><navLabel><text>版权声明</text></navLabel><content src="copyright.xhtml"/></navPoint>')

    xhtml_files.append(("preface.xhtml", preface_xhtml()))
    opf_items.append('<item id="preface" href="preface.xhtml" media-type="application/xhtml+xml"/>')
    ncx_points.append('<navPoint id="np-preface" playOrder="3"><navLabel><text>导读</text></navLabel><content src="preface.xhtml"/></navPoint>')

    if HAVE_COVER_IMG:
        opf_items.append('<item id="coverimg" href="cover.png" media-type="image/png"/>')

    play = 4
    titles = {"cover.xhtml": "封面", "copyright.xhtml": "版权声明", "preface.xhtml": "导读"}
    for num, title, intro, entries, items in chapters:
        fn = "ch%02d.xhtml" % num
        titles[fn] = title
        xhtml_files.append((fn, chapter_xhtml(num, title, intro, entries, items)))
        opf_items.append('<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (fn.replace(".xhtml", ""), fn))
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
    <dc:language>zh-CN</dc:language>
    <dc:date>%s</dc:date>
    <meta property="dcterms:modified">%sT00:00:00Z</meta>
    %s
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="styles.css" media-type="text/css"/>
        %s
  </manifest>
  <spine>
    %s
  </spine>
</package>""" % (UID, esc(TITLE), esc(AUTHOR), today, today,
                ('<meta name="cover" content="coverimg"/>' if HAVE_COVER_IMG else ''),
                manifest, spine)

    nav_li = "\n".join('<li><a href="%s">%s</a></li>' % (fn, esc(titles.get(fn, fn))) for fn, _ in xhtml_files)
    nav = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>目录</title></head>
<body>
<nav epub:type="toc" id="toc">
<h1>目录</h1>
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

    # --- XML well-formedness gate -------------------------------------------
    # EPUB/Kindle readers parse every content document as STRICT XML. One bad
    # document (e.g. an undeclared HTML entity such as &copy;) makes KDP reject
    # the whole upload with "cannot convert your file". Fail the build here so a
    # broken EPUB can never be shipped again.
    import xml.etree.ElementTree as _ET
    _docs = list(xhtml_files) + [("content.opf", opf), ("nav.xhtml", nav), ("toc.ncx", ncx)]
    for _name, _text in _docs:
        try:
            _ET.fromstring(_text.encode("utf-8"))
        except Exception as _e:
            raise SystemExit("\u274c XML invalid in %s: %s" % (_name, _e))
    print("\u2705 XML gate: %d content documents are well-formed" % len(_docs))
    _written = {fn for fn, _ in xhtml_files} | {"nav.xhtml", "toc.ncx", "styles.css", "cover.png"}
    _opf_gate(opf, _written)

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
        if HAVE_COVER_IMG:
            with open(COVER_IMG, "rb") as fh:
                z.writestr("OEBPS/cover.png", fh.read())

    total_entries = sum(len(c[3]) for c in chapters)
    print("✅ 已生成 %s" % OUT)
    print("   章节：%d ｜ 条目：%d" % (len(chapters), total_entries))


if __name__ == "__main__":
    build()
