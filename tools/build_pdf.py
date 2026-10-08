#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter —— PDF 生成器（依赖 reportlab + 内置 CJK 字体）

解析 book/ 生成排版干净的 PDF 电子书：HowToInvestBetter.pdf
  - 封面
  - 目录（按章）
  - 每章：章标题 + 章前导语 + 条目（标题/标签/成本·说人话·收益·证据等级·来源·备注）
  - 页脚页码

中文字体使用 reportlab 内置的 Adobe CID 字体 STSong-Light（无需额外字体文件）。

用法：
  python3 tools/build_pdf.py
"""
import os
import re
import glob
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# 纸书印刷级：6×9 英寸开本（KDP Paperback 标准），页边距 0.75″
PRINT_MODE = "--print" in sys.argv
PAGESIZE = (6 * 72, 9 * 72) if PRINT_MODE else A4
MARGIN = (0.75 * 72) if PRINT_MODE else (20 * mm)
OUT = os.path.join(ROOT, "HowToInvestBetter-print.pdf") if PRINT_MODE else os.path.join(ROOT, "HowToInvestBetter.pdf")
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
FONT = "STSong-Light"

TITLE = "高性价比投资指南"
SUB = "花掉什么，换回什么，证据有多硬"
AUTHOR = "HowToInvestBetter 项目组"
COPYRIGHT_FILE = os.path.join(ROOT, "版权声明.md")

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
TAG_RE = re.compile(r"^<!--\s*标签:\s*(.+?)\s*-->$")
FIELD_RE = re.compile(r"^-\s*(成本|说人话|收益|证据等级|来源|备注)[：:]\s*(.*)$")
FIELDS = ["成本", "说人话", "收益", "证据等级", "来源", "备注"]


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tagline(tags):
    return "钱：%s ｜ 时间：%s ｜ 毅力：%s ｜ 收益：%s ｜ 口径：%s" % (
        esc(tags.get("钱", "")), esc(tags.get("时间", "")), esc(tags.get("毅力", "")),
        esc(tags.get("收益", "")), esc(tags.get("口径", "")))


def read_copyright_flowables():
    """读取 版权声明.md 渲染为 PDF 流（单一信源，避免与仓库文件漂移）。"""
    if not os.path.exists(COPYRIGHT_FILE):
        return []
    flows = []
    for line in open(COPYRIGHT_FILE, encoding="utf-8").read().split("\n"):
        s = line.rstrip()
        if not s.strip():
            continue
        s = s.replace("__AUTHOR__", AUTHOR)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(s))
        if s.startswith("## "):
            flows.append(Paragraph(s[3:], H2))
        elif s.startswith("# "):
            flows.append(Paragraph(s[2:], H1))
        elif s.startswith("- "):
            flows.append(Paragraph("· " + s[2:], BODY))
        else:
            flows.append(Paragraph(s, INTRO))
    return flows


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
            out.append((num, title or "未命名", intro, entries, items))
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
    canvas.drawRightString(doc.pagesize[0] - 18 * mm, 12 * mm, "第 %d 页" % doc.page)
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
        subject="循证投资手册", lang="zh-CN",
    )
    story = []

    story.append(Spacer(1, 40 * mm))
    cover_png = os.path.join(ROOT, "cover.png")
    if os.path.exists(cover_png) and _PILImage is not None:
        w, h = _PILImage.open(cover_png).size
        tw = (110 * mm) if PRINT_MODE else (150 * mm)
        im = Image(cover_png, width=tw, height=tw * h / w)
        story.append(im)
        story.append(Spacer(1, 8 * mm))
        story.append(Paragraph("开源 · CC BY 4.0", COVER_F))
        story.append(Paragraph("更新于 %s · 共 %d 章 %d 条" % (today, len(chapters), total_entries), COVER_F))
    else:
        story.append(Paragraph(esc(TITLE), COVER_T))
        story.append(Spacer(1, 6 * mm))
        story.append(Paragraph(esc(SUB), COVER_S))
        story.append(Spacer(1, 10 * mm))
        story.append(Paragraph("开源 · CC BY 4.0", COVER_F))
        story.append(Paragraph("更新于 %s · 共 %d 章 %d 条" % (today, len(chapters), total_entries), COVER_F))
    story.append(PageBreak())

    # 版权声明页
    story.append(Paragraph("版权声明", H1))
    story.append(HRFlowable(width="100%", color=HexColor("#c0392b"), thickness=1, spaceAfter=8))
    for fl in read_copyright_flowables():
        story.append(fl)
    if PRINT_MODE:
        story.append(Spacer(1, 8))
        story.append(Paragraph("ISBN：______________（纸书投稿前向 KDP 免费申请，或填写自有 ISBN）", META))
    story.append(PageBreak())

    # 导读页
    story.append(Paragraph("导读 · 怎么读这本指南", H1))
    story.append(HRFlowable(width="100%", color=HexColor("#c0392b"), thickness=1, spaceAfter=8))
    intro_items = [
        "这是一份循证投资手册。它不推荐任何具体产品，只把经过统计、研究与监管文件验证的「高性价比动作」列成一张可按图索骥的清单。每条都用同一套账本：花掉什么、换回什么、证据多硬、出处哪来。",
        "四个问题：① 花掉什么？钱、时间、毅力，还是本金的永久性损失？② 换回什么？长期真实回报、更低波动、税费节省，还是避开归零？③ 证据多硬？见下方证据等级。④ 出处哪来？只引期刊论文与官方文件，不引自媒体与营销号。",
        "证据等级：〔A〕权威长期统计（标普 SPIVA、交易所年鉴）、顶刊随机或追踪研究、官方监管文件。〔B〕单项高质量研究、权威机构（Vanguard／Dalbar／Ibbotson）回测报告、经典论文。〔C〕合理推论或广泛共识，逻辑硬但未必挂精确出处。",
        "三零原则（极高性价比死标准）：一条动作若「花费等于无、时间等于无、毅力等于否」三项成本全为零，就是「三零」。严格符合的共 16 条，闭眼先做；更多动作是「两项为零、一项极低」的高性价比档。",
        "阅读建议：不用全做，这是备选单不是任务清单。挑走一两条就算数。想省时间先按「仅三零」筛；每章内条目按性价比从高到低排，从每章前几条看起；看不懂就只读每一条的「说人话」一行。",
    ]
    for it in intro_items:
        story.append(Paragraph(esc(it), INTRO))
    story.append(PageBreak())

    story.append(Paragraph("目录", H1))
    story.append(HRFlowable(width="100%", color=HexColor("#c0392b"), thickness=1, spaceAfter=8))
    for num, title, intro, entries, items in chapters:
        cnt = "%d 条" % len(entries) if entries else "%d 项清单" % len(items)
        story.append(Paragraph("第%d章　%s　<span color='#999999'>（%s）</span>" % (num, esc(title), cnt), BODY))
    story.append(PageBreak())

    for num, title, intro, entries, items in chapters:
        story.append(Paragraph("第%d章　%s" % (num, esc(title)), H1))
        story.append(HRFlowable(width="100%", color=HexColor("#e0e0e0"), thickness=0.6, spaceAfter=6))
        for para in intro:
            story.append(Paragraph(esc(para), INTRO))
        for e in entries:
            block = []
            block.append(Paragraph("%d. %s" % (e["num"], esc(e["title"])), H2))
            block.append(Paragraph("<font color='#888888'>%s</font>" % tagline(e["tags"]), META))
            for k in FIELDS:
                v = e["fields"].get(k)
                if v:
                    block.append(Paragraph("<font color='#c0392b'>%s：</font>%s" % (k, esc(v)), BODY))
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
