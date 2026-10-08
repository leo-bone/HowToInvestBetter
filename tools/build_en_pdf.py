#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter —— English PDF generator (depends on reportlab + CJK-capable font)

Parses en/book/*.md (English six-field edition) into a clean PDF ebook:
  HowToInvestBetter-en.pdf        (A4, on-screen / e-reader)
  HowToInvestBetter-en-print.pdf  (6x9 inch, KDP Paperback standard; --print)

The CJK-capable font (STSong-Light, built into reportlab) is used throughout so
that the original Chinese document titles preserved in "Sources" render without
missing-glyph boxes.

Usage:
  pip install reportlab
  python3 tools/build_en_pdf.py            # A4
  python3 tools/build_en_pdf.py --print    # 6x9 KDP paperback
"""
import os
import re
import glob
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "en", "book")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# KDP Paperback standard: 6x9 inch trim, 0.75" margins
PRINT_MODE = "--print" in sys.argv
PAGESIZE = (6 * 72, 9 * 72) if PRINT_MODE else A4
MARGIN = (0.75 * 72) if PRINT_MODE else (20 * mm)
OUT = os.path.join(ROOT, "HowToInvestBetter-en-print.pdf") if PRINT_MODE else os.path.join(ROOT, "HowToInvestBetter-en.pdf")
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether, Image
)
try:
    from PIL import Image as _PILImage
except Exception:
    _PILImage = None

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
FONT = "STSong-Light"  # CJK-capable; also renders Latin glyphs

TITLE = "A High-Value Investment Guidebook"
SUB = "What it costs, what it returns, how strong the evidence is"
AUTHOR = "leo-bone"

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
TAG_RE = re.compile(r"^<!--\s*tags:\s*(.+?)\s*-->$")
FIELD_RE = re.compile(r"^-\s*(Cost|In plain terms|Payoff|Evidence grade|Sources|Note)[：:]\s*(.*)$")
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


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tagline(tags):
    parts = []
    for key in ["money", "time", "will", "payoff", "scope", "impact"]:
        v = tags.get(key)
        if v:
            parts.append("%s: %s" % (TAG_LABEL[key], TAG_VAL_MAP.get(key, {}).get(v, v)))
    return " ｜ ".join(parts)


def parse_chapters():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    out = []
    for path in files:
        num = int(os.path.basename(path).split("-", 1)[0])
        title = None
        intro = []
        entries = []
        items = []
        cur = None
        for line in open(path, encoding="utf-8").read().split("\n"):
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
                bm = re.match(r"^[-*]\s+(.+?)\s*$", line)
                if bm:
                    items.append(bm.group(1).strip())
                elif title is not None:
                    intro.append(line.strip())
        if cur:
            entries.append(cur)
        if entries or items:
            out.append((num, title or "Untitled", intro, entries, items))
    return out


H1 = ParagraphStyle("H1", fontName=FONT, fontSize=17, leading=22, spaceAfter=8,
                    textColor=HexColor("#c0392b"))
H2 = ParagraphStyle("H2", fontName=FONT, fontSize=11.5, leading=15, spaceBefore=8,
                    spaceAfter=3, textColor=HexColor("#1a1a1a"))
META = ParagraphStyle("META", fontName=FONT, fontSize=7.8, leading=11,
                      textColor=HexColor("#888888"), spaceAfter=4)
INTRO = ParagraphStyle("INTRO", fontName=FONT, fontSize=9.3, leading=14,
                       textColor=HexColor("#444444"), spaceAfter=4)
BODY = ParagraphStyle("BODY", fontName=FONT, fontSize=9.5, leading=14,
                      spaceAfter=2, alignment=TA_LEFT)
NOTE = ParagraphStyle("NOTE", fontName=FONT, fontSize=8.8, leading=12.5,
                      textColor=HexColor("#8a6d1b"), spaceAfter=2)
COVER_T = ParagraphStyle("COVER_T", fontName=FONT, fontSize=24, leading=30,
                         alignment=TA_CENTER, textColor=HexColor("#c0392b"))
COVER_S = ParagraphStyle("COVER_S", fontName=FONT, fontSize=13, leading=20,
                         alignment=TA_CENTER, textColor=HexColor("#444444"))
COVER_F = ParagraphStyle("COVER_F", fontName=FONT, fontSize=10, leading=16,
                         alignment=TA_CENTER, textColor=HexColor("#777777"))


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawString(MARGIN, 12 * mm, "A High-Value Investment Guidebook · Open source CC BY 4.0")
    canvas.drawRightString(doc.pagesize[0] - MARGIN, 12 * mm, "Page %d" % doc.page)
    canvas.restoreState()


def build():
    chapters = parse_chapters()
    total_entries = sum(len(c[3]) for c in chapters)
    today = datetime.date.today().isoformat()

    doc = SimpleDocTemplate(
        OUT, pagesize=PAGESIZE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title=TITLE, author=AUTHOR,
        subject="Evidence-based investment handbook", lang="en",
    )
    story = []

    # --- Cover (text only; the Chinese cover image is not used for the EN edition) ---
    story.append(Spacer(1, 40 * mm))
    story.append(Paragraph(esc(TITLE), COVER_T))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(esc(SUB), COVER_S))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("Open source · CC BY 4.0", COVER_F))
    story.append(Paragraph("Updated %s · %d chapters · %d entries" % (today, len(chapters), total_entries), COVER_F))
    story.append(PageBreak())

    # --- License page ---
    story.append(Paragraph("License &amp; Disclaimer", H1))
    story.append(HRFlowable(width="100%", color=HexColor("#c0392b"), thickness=1, spaceAfter=8))
    license_lines = [
        "The main content of this guidebook is licensed under CC BY 4.0 (Creative Commons Attribution 4.0 International). You are free to share, adapt, and use it commercially, provided you give appropriate credit to the author, leo-bone, and indicate if changes were made. The code (search page, build scripts) is licensed under MIT.",
        "This guidebook is an independently authored, evidence-based methodology handbook and is not investment advice from any institution or individual. All citations follow each organization's latest official releases. Markets carry risk; decisions require independent judgment and consultation with a licensed professional.",
        "This is an open-source edition. The latest version and the Chinese original are maintained at github.com/leo-bone/HowToInvestBetter.",
    ]
    for ln in license_lines:
        story.append(Paragraph(esc(ln), INTRO))
    if PRINT_MODE:
        story.append(Spacer(1, 8))
        story.append(Paragraph("ISBN: ______________ (apply for a free KDP ISBN, or fill in your own before submission)", META))
    story.append(PageBreak())

    # --- Introduction page ---
    story.append(Paragraph("Introduction · How to Read This Guidebook", H1))
    story.append(HRFlowable(width="100%", color=HexColor("#c0392b"), thickness=1, spaceAfter=8))
    intro_items = [
        "This is an evidence-based investment handbook. It recommends no specific product; it simply lists high-value moves validated by statistics, research, and regulatory documents, arranged as a checklist you can follow entry by entry. Every entry uses the same ledger: what it costs, what it returns, how strong the evidence is, and where the sources come from.",
        "Four questions: 1) What does it cost? Money, time, willpower, or a permanent loss of principal? 2) What does it return? Long-term real return, lower volatility, tax & fee savings, or avoidance of total loss? 3) How strong is the evidence? See the grades below. 4) Where do the sources come from? Only journal papers and official documents — never self-media or marketing.",
        "Evidence grades: [A] authoritative long-term statistics (S&P SPIVA, exchange yearbooks), randomized/longitudinal studies in top journals, official regulatory documents. [B] individual high-quality studies, backtest reports from authoritative institutions (Vanguard / Dalbar / Ibbotson), classic papers. [C] reasonable inference or broad consensus — logically sound but not forced to a precise citation.",
        "The Three-Zeros principle (highest-value hard standard): an action is Three Zeros if cost = none, time = none, and willpower = none. Exactly 16 entries meet this strictly — do them first without overthinking; many more are two-zeros-and-one-very-low.",
        "Reading advice: you don't have to do it all — this is a menu, not a to-do list. Take even one or two items and it counts. To save time, filter by Three Zeros only; within each chapter entries are ranked high to low by value, so start with the first few; if you can't follow the numbers, just read the In plain terms line of each entry.",
    ]
    for it in intro_items:
        story.append(Paragraph(esc(it), INTRO))
    story.append(PageBreak())

    # --- Table of contents ---
    story.append(Paragraph("Contents", H1))
    story.append(HRFlowable(width="100%", color=HexColor("#c0392b"), thickness=1, spaceAfter=8))
    for num, title, intro, entries, items in chapters:
        cnt = "%d entries" % len(entries) if entries else "%d-item list" % len(items)
        story.append(Paragraph("Chapter %d  %s  <font color='#999999'>(%s)</font>" % (num, esc(title), cnt), BODY))
    story.append(PageBreak())

    # --- Chapters ---
    for num, title, intro, entries, items in chapters:
        story.append(Paragraph("Chapter %d  %s" % (num, esc(title)), H1))
        story.append(HRFlowable(width="100%", color=HexColor("#e0e0e0"), thickness=0.6, spaceAfter=6))
        for para in intro:
            story.append(Paragraph(esc(para), INTRO))
        for e in entries:
            block = []
            block.append(Paragraph("%d. %s" % (e["num"], esc(e["title"])), H2))
            tl = tagline(e["tags"])
            if tl:
                block.append(Paragraph("<font color='#888888'>%s</font>" % esc(tl), META))
            for k in FIELDS:
                v = e["fields"].get(k)
                if v:
                    block.append(Paragraph("<font color='#c0392b'>%s:</font> %s" % (esc(k), esc(v)), BODY))
            story.append(KeepTogether(block))
            story.append(Spacer(1, 3))
        if items:
            story.append(Spacer(1, 4))
            story.append(Paragraph("<font color='#c0392b'>Negative-value moves — cross one off as it appears:</font>", BODY))
            for it in items:
                story.append(Paragraph("· %s" % esc(it), BODY))
        story.append(PageBreak())

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("✅ Generated %s" % OUT)
    print("   Chapters: %d | Entries: %d" % (len(chapters), total_entries))


if __name__ == "__main__":
    build()
