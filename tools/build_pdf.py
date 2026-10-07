#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter —— PDF 生成器（依赖 reportlab + 内置 CJK 字体）

解析 book/ 生成排版干净的 PDF 电子书：HowToInvestBetter.pdf
  - 封面
  - 目录（按章）
  - 每章：章标题 + 条目（标题/标签/花掉·换回·出处·说人话）
  - 页脚页码

中文字体使用 reportlab 内置的 Adobe CID 字体 STSong-Light（无需额外字体文件）。

用法：
  python3 tools/build_pdf.py
依赖安装（仅构建时用，不影响读者）：
  pip install reportlab
"""
import os
import re
import glob
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
OUT = os.path.join(ROOT, "HowToInvestBetter.pdf")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether
)

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
FONT = "STSong-Light"

TITLE = "高性价比投资指南"
SUB = "花掉什么，换回什么，证据有多硬"

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(
    r"^##\s+(\d+)\s+(.+?)\s*"
    r"〔([ABC])〕〔影响：([^〕]+)〕〔花费：([^〕]+)〕〔时间：([^〕]+)〕〔毅力：([^〕]+)〕\s*$"
)
FIELD_RE = re.compile(r"^\*\*(花掉|换回|出处|说人话)\*\*[：:]\s*(.*)$")
NOTE_RE = re.compile(r"^>\s*〔([^〕]+)〕\s*(.*)$")

GRADE_LABEL = {"A": "A·权威统计/顶刊/官方", "B": "B·单项研究/机构报告", "C": "C·合理推论/广泛共识"}


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def parse_chapters():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    out = []
    for path in files:
        num = int(os.path.basename(path).split("-", 1)[0])
        title = None
        entries = []
        items = []
        cur = None
        for line in open(path, encoding="utf-8").read().split("\n"):
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
                    "cm": m.group(5).strip(),
                    "ct": m.group(6).strip(),
                    "cw": m.group(7).strip(),
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
                if line.strip() == "":
                    continue
            else:
                # 清单型章节：条目之前的纯列表项
                bm = re.match(r"^[-*]\s+(.+?)\s*$", line)
                if bm and title is not None:
                    items.append(bm.group(1).strip())
        if cur:
            entries.append(cur)
        if entries or items:
            out.append((num, title or "未命名", entries, items))
    return out


# 样式
H1 = ParagraphStyle("H1", fontName=FONT, fontSize=17, leading=22, spaceAfter=8,
                    textColor=HexColor("#c0392b"))
H2 = ParagraphStyle("H2", fontName=FONT, fontSize=11.5, leading=15, spaceBefore=8,
                    spaceAfter=3, textColor=HexColor("#1a1a1a"))
META = ParagraphStyle("META", fontName=FONT, fontSize=8, leading=11,
                      textColor=HexColor("#777777"), spaceAfter=4)
BODY = ParagraphStyle("BODY", fontName=FONT, fontSize=9.5, leading=14,
                      spaceAfter=2, alignment=TA_LEFT)
NOTE = ParagraphStyle("NOTE", fontName=FONT, fontSize=8.5, leading=12,
                      textColor=HexColor("#b8860b"), spaceAfter=2)
LABEL_RED = HexColor("#c0392b")
COVER_T = ParagraphStyle("COVER_T", fontName=FONT, fontSize=26, leading=32,
                         alignment=TA_CENTER, textColor=HexColor("#c0392b"))
COVER_S = ParagraphStyle("COVER_S", fontName=FONT, fontSize=13, leading=20,
                         alignment=TA_CENTER, textColor=HexColor("#444444"))
COVER_F = ParagraphStyle("COVER_F", fontName=FONT, fontSize=10, leading=16,
                         alignment=TA_CENTER, textColor=HexColor("#777777"))


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawString(18 * mm, 12 * mm, "高性价比投资指南 · 开源 CC BY 4.0")
    canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, "第 %d 页" % doc.page)
    canvas.restoreState()


def build():
    chapters = parse_chapters()
    total_entries = sum(len(c[2]) for c in chapters)
    today = datetime.date.today().isoformat()

    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=TITLE, author="HowToInvestBetter 项目",
        subject="循证投资手册", lang="zh-CN",
    )
    story = []

    # 封面
    story.append(Spacer(1, 55 * mm))
    story.append(Paragraph(esc(TITLE), COVER_T))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(esc(SUB), COVER_S))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("仿《高性价比人生指南》体例 · 开源 · CC BY 4.0", COVER_F))
    story.append(Paragraph("更新于 %s · 共 %d 章 %d 条" % (today, len(chapters), total_entries), COVER_F))
    story.append(PageBreak())

    # 目录
    story.append(Paragraph("目录", H1))
    story.append(HRFlowable(width="100%", color=HexColor("#c0392b"), thickness=1, spaceAfter=8))
    for num, title, entries, items in chapters:
        cnt = "%d 条" % len(entries) if entries else "%d 项清单" % len(items)
        story.append(Paragraph("第%d章　%s　<span color='#999999'>（%s）</span>" % (num, esc(title), cnt), BODY))
    story.append(PageBreak())

    # 正文
    for num, title, entries, items in chapters:
        story.append(Paragraph("第%d章　%s" % (num, esc(title)), H1))
        story.append(HRFlowable(width="100%", color=HexColor("#e0e0e0"), thickness=0.6, spaceAfter=6))
        for e in entries:
            block = []
            block.append(Paragraph("%d. %s" % (e["num"], esc(e["title"])), H2))
            block.append(Paragraph(
                "<font color='#888888'>[%s] 影响：%s ｜ 花费：%s 时间：%s 毅力：%s</font>" % (
                    GRADE_LABEL[e["grade"]], esc(e["impact"]), esc(e["cm"]), esc(e["ct"]), esc(e["cw"])), META))
            for k in ("花掉", "换回", "出处", "说人话"):
                if e["fields"].get(k):
                    block.append(Paragraph("<font color='#c0392b'>%s：</font>%s" % (k, esc(e["fields"][k])), BODY))
            for typ, txt in e["notes"]:
                block.append(Paragraph("<font color='#b8860b'>〔%s〕 %s</font>" % (esc(typ), esc(txt)), NOTE))
            story.append(KeepTogether(block))
            story.append(Spacer(1, 3))
        if items:
            story.append(Spacer(1, 4))
            story.append(Paragraph("<font color='#c0392b'>以下动作性价比为负，出现一个划掉一个：</font>", BODY))
            for it in items:
                story.append(Paragraph("· %s" % esc(it), BODY))
        story.append(PageBreak())

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("✅ 已生成 %s" % OUT)
    print("   章节：%d ｜ 条目：%d" % (len(chapters), total_entries))


if __name__ == "__main__":
    build()
