#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English edition cover generator (KDP-ready).

Outputs:
  1. en-cover.png         1200x630  social / GitHub Pages share card
  2. cover-book-en.png    1600x2560 Kindle eBook cover (KDP min 1000x1600)
  3. cover-paperback-en.png  300 DPI full wrap (back | spine | front)
  4. cover-paperback-en.pdf  300 DPI full wrap (KDP preferred upload format)

KDP wrap rule (verified vs official help):
  left = back cover | middle = spine | right = front cover
  bleed 0.125" on all sides; barcode auto-added by KDP at back-bottom-right
  (we reserve a 2"x1.2" blank there).
  spine = pages * paper thickness (white 0.002252"/pg)
Usage: python3 tools/gen_cover_en.py [--cream] [--pages N]
"""
import os
import argparse
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINT_PDF = os.path.join(ROOT, "HowToInvestBetter-en-print.pdf")
SOCIAL = os.path.join(ROOT, "en-cover.png")
EBOOK = os.path.join(ROOT, "cover-book-en.png")
WRAP_PNG = os.path.join(ROOT, "cover-paperback-en.png")
WRAP_PDF = os.path.join(ROOT, "cover-paperback-en.pdf")

TITLE = "A High-Value Investment Guidebook"
SUB = "What it costs, what it returns, how strong the evidence is"
AUTHOR = "leo-bone"

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

NAVY_TOP, NAVY_BOT = (15, 27, 45), (23, 42, 71)
STEEL = (86, 104, 129)
LIGHT = (226, 232, 240)
BLUE = (147, 197, 253)
RED = (192, 57, 43)
MUTE = (100, 116, 139)
WHITE = (255, 255, 255)

DPI = 300.0
BLEED_IN = 0.125
TRIM_W, TRIM_H = 6.0, 9.0
PAPER_WHITE = 0.002252
PAPER_CREAM = 0.002500


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def tw(d, text, fnt):
    return int(d.textlength(text, font=fnt))


def center(d, text, cx, y, fnt, fill):
    d.text((cx - tw(d, text, fnt) / 2, y), text, font=fnt, fill=fill)


def gradient(d, W, H):
    for y in range(H):
        t = y / H
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)


# ---------------- front cover content (designed on 1800x2700 panel) ----------
def draw_front(d, ox, oy):
    pw, ph = 1800, 2700
    cx = ox + pw / 2
    safe = 90
    d.rectangle([ox + safe, oy + safe, ox + pw - safe, oy + ph - safe],
                outline=STEEL, width=4)
    # accent bar
    d.rectangle([cx - 90, oy + 220, cx + 90, oy + 238], fill=RED)
    ft = font(BOLD, 150)
    center(d, "A High-Value", cx, oy + 320, ft, WHITE)
    center(d, "Investment", cx, oy + 500, ft, WHITE)
    center(d, "Guidebook", cx, oy + 680, ft, WHITE)
    fs = font(REG, 52)
    center(d, "What it costs, what it returns,", cx, oy + 860, fs, BLUE)
    center(d, "how strong the evidence is", cx, oy + 928, fs, BLUE)
    d.line([(cx - 360, oy + 1010), (cx + 360, oy + 1010)], fill=STEEL, width=3)
    chips = ["302 entries", "24 chapters", "Evidence A/B/C", "CC BY 4.0"]
    fch = font(REG, 42)
    gaps = 36
    cw = [tw(d, ch, fch) + 52 for ch in chips]
    xx = cx - (sum(cw) + gaps * (len(chips) - 1)) / 2
    yy = oy + 1130
    for ch, ww in zip(chips, cw):
        d.rounded_rectangle([xx, yy, xx + ww, yy + 90], radius=45,
                            outline=STEEL, width=3)
        center(d, ch, xx + ww / 2, yy + 22, fch, LIGHT)
        xx += ww + gaps
    fp = font(REG, 50)
    center(d, "No stock tips. No courses to sell.", cx, oy + 1420, fp, LIGHT)
    center(d, "Just evidence you can verify yourself.", cx, oy + 1490, fp, LIGHT)
    d.line([(cx - 360, oy + 2160), (cx + 360, oy + 2160)], fill=STEEL, width=3)
    center(d, "by %s" % AUTHOR, cx, oy + 2230, font(REG, 56), (203, 213, 225))
    center(d, "Open source CC BY 4.0", cx, oy + 2310, font(REG, 36), MUTE)


# ---------------- back cover content (1800x2700 panel) -----------------------
def draw_back(d, ox, oy):
    pw, ph = 1800, 2700
    bcx = ox + pw / 2
    safe = 90
    d.rectangle([ox + safe, oy + safe, ox + pw - safe, oy + ph - safe],
                outline=STEEL, width=4)
    center(d, "About This Book", bcx, oy + 150, font(BOLD, 54), WHITE)
    d.line([(bcx - 200, oy + 232), (bcx + 200, oy + 232)], fill=RED, width=4)
    body = font(REG, 38)
    para = [
        "A no-hype, evidence-based investing manual.",
        "Across 24 chapters and 302 entries, every action",
        "states three things clearly:",
        "  - What it costs (fees, taxes, time, effort,",
        "    permanent loss of capital)",
        "  - What it returns (long-term real returns,",
        "    lower volatility, tax savings, avoiding wipeouts)",
        "  - How strong the evidence is (A = authoritative",
        "    statistics & official documents; B = single",
        "    studies & institutional reports; C = reasonable",
        "    inference & regulation).",
        "Sources cite only peer-reviewed papers and official",
        "filings - never self-media or marketing accounts.",
    ]
    yy = oy + 300
    for line in para:
        d.text((ox + 150, yy), line, font=body, fill=LIGHT)
        yy += 56
    fbul = font(REG, 36)
    bullets = [
        "The 'Three-Zero Principle': do first the moves that",
        "   cost zero money, zero time, and zero willpower.",
        "Every entry shows its original source; check the",
        "   A/B/C evidence yourself.",
        "Taxes, ETFs, IPOs, and fund screening tuned for",
        "   practical investors.",
        "Open source CC BY 4.0 - read the full text free online.",
    ]
    yy = oy + 1080
    for b in bullets:
        d.text((ox + 150, yy), ("- " if not b.startswith("   ") else "   ") + b.strip(),
               font=fbul, fill=BLUE)
        yy += 52
    # barcode zone (back-bottom-right): 2"x1.2", 0.25" from spine & bottom
    bar_w, bar_h = int(round(2.0 * DPI)), int(round(1.2 * DPI))
    bar_right = ox + pw - int(round(0.25 * DPI))
    bar_bottom = oy + ph - int(round(0.25 * DPI))
    bar_x, bar_y = bar_right - bar_w, bar_bottom - bar_h
    d.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h],
                fill=WHITE, outline=STEEL, width=2)
    center(d, "Barcode added by KDP", bar_x + bar_w / 2, bar_y + bar_h / 2 - 14,
           font(REG, 28), (130, 130, 130))
    center(d, "ISBN assigned free by KDP", bar_x + bar_w / 2, bar_y - 34,
           font(REG, 30), LIGHT)
    center(d, "github.com/leo-bone/HowToInvestBetter", bcx,
           oy + ph - 560, font(REG, 30), MUTE)


# ---------------- spine (rotated) --------------------------------------------
def draw_spine(d, x0, y0, spine):
    d.rectangle([x0, y0, x0 + spine, y0 + 2700], fill=(12, 22, 38))
    spine_text = "%s   %s" % (TITLE, AUTHOR)
    fsz = min(int(46 * (spine / 247.0)), 52)
    fsp = font(BOLD, fsz)
    t = tw(d, spine_text, fsp)
    pad = 24
    tmp = Image.new("RGBA", (t + 2 * pad, spine), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((pad, (spine - fsz) / 2 - 4), spine_text,
                             font=fsp, fill=(235, 240, 248))
    tmp = tmp.rotate(90, expand=True)
    d.line([(x0, y0 + 10), (x0 + spine, y0 + 10)], fill=STEEL, width=2)
    d.line([(x0, y0 + 2690), (x0 + spine, y0 + 2690)], fill=STEEL, width=2)
    d.text((x0 + (spine - tmp.width) / 2, y0 + (2700 - tmp.height) / 2),
           "", font=fsp, fill=(0, 0, 0))
    # paste rotated text centered on spine
    base = Image.new("RGBA", (spine, 2700), (0, 0, 0, 0))
    base.paste(tmp, ((spine - tmp.width) // 2, (2700 - tmp.height) // 2))
    img_mask = base.convert("RGB")
    d.image = None
    return base, x0, y0, spine


def page_count():
    for mod in ("pypdf", "PyPDF2"):
        try:
            m = __import__(mod)
            return len(m.PdfReader(PRINT_PDF).pages)
        except Exception:
            pass
    return 366


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cream", action="store_true")
    ap.add_argument("--pages", type=int, default=None)
    args = ap.parse_args()

    pages = args.pages or page_count()
    per = PAPER_CREAM if args.cream else PAPER_WHITE
    spine_in = pages * per
    cover_w_in = 2 * BLEED_IN + 2 * TRIM_W + spine_in
    cover_h_in = TRIM_H + 2 * BLEED_IN

    W = int(round(cover_w_in * DPI))
    H = int(round(cover_h_in * DPI))
    bleed = int(round(BLEED_IN * DPI))
    spine = int(round(spine_in * DPI))
    trim_w = int(round(TRIM_W * DPI))
    trim_h = int(round(TRIM_H * DPI))

    # ============ full wrap ============
    img = Image.new("RGB", (W, H), NAVY_TOP)
    d = ImageDraw.Draw(img)
    gradient(d, W, H)
    back_x0 = bleed
    spine_x0 = back_x0 + trim_w
    front_x0 = spine_x0 + spine
    draw_back(d, back_x0, bleed)
    draw_front(d, front_x0, bleed)
    # spine
    base, sx, sy, sp = draw_spine(d, spine_x0, bleed, spine)
    img.paste(base, (sx, sy), base)
    img.save(WRAP_PNG, "PNG", optimize=True)

    # 300 DPI PDF wrap
    made_pdf = False
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        c = rl_canvas.Canvas(WRAP_PDF, pagesize=(cover_w_in * 72, cover_h_in * 72))
        c.drawImage(WRAP_PNG, 0, 0, width=cover_w_in * 72, height=cover_h_in * 72)
        c.showPage()
        c.save()
        made_pdf = True
    except Exception as e:
        print("[warn] no PDF (reportlab missing):", e)

    print("[ok] %s (%d x %d, 300DPI)" % (WRAP_PNG, W, H))
    if made_pdf:
        print("[ok] %s (%.4f\" x %.4f\")" % (WRAP_PDF, cover_w_in, cover_h_in))
    print("     paper=%s pages=%d spine=%.4f\"(%dpx) wrap=%.4f\"x%.4f\"" % (
        "cream" if args.cream else "white", pages, spine_in, spine, cover_w_in, cover_h_in))

    # ============ eBook cover 1600x2560 ============
    eb = Image.new("RGB", (1600, 2560), NAVY_TOP)
    de = ImageDraw.Draw(eb)
    gradient(de, 1600, 2560)
    # scale front design (1800x2700) into 1600x2560 uniformly-ish
    sx, sy = 1600 / 1800.0, 2560 / 2700.0
    # redraw front at the ebook scale by translating coordinates
    cx = 800
    safe = int(90 * sx)
    de.rectangle([safe, safe, 1600 - safe, 2560 - safe], outline=STEEL, width=4)
    de.rectangle([cx - 80, int(220 * sy), cx + 80, int(238 * sy)], fill=RED)
    ft = font(BOLD, int(150 * sy))
    center(de, "A High-Value", cx, int(320 * sy), ft, WHITE)
    center(de, "Investment", cx, int(500 * sy), ft, WHITE)
    center(de, "Guidebook", cx, int(680 * sy), ft, WHITE)
    fs = font(REG, int(52 * sy))
    center(de, "What it costs, what it returns,", cx, int(860 * sy), fs, BLUE)
    center(de, "how strong the evidence is", cx, int(928 * sy), fs, BLUE)
    de.line([(cx - 320, int(1010 * sy)), (cx + 320, int(1010 * sy))], fill=STEEL, width=3)
    chips = ["302 entries", "24 chapters", "Evidence A/B/C", "CC BY 4.0"]
    fch = font(REG, int(42 * sy))
    gaps = 32
    cw = [tw(de, ch, fch) + 48 for ch in chips]
    xx = cx - (sum(cw) + gaps * (len(chips) - 1)) / 2
    yy = int(1130 * sy)
    for ch, ww in zip(chips, cw):
        de.rounded_rectangle([xx, yy, xx + ww, yy + int(84 * sy)], radius=int(42 * sy),
                             outline=STEEL, width=3)
        center(de, ch, xx + ww / 2, yy + int(20 * sy), fch, LIGHT)
        xx += ww + gaps
    fp = font(REG, int(48 * sy))
    center(de, "No stock tips. No courses to sell.", cx, int(1420 * sy), fp, LIGHT)
    center(de, "Just evidence you can verify yourself.", cx, int(1490 * sy), fp, LIGHT)
    de.line([(cx - 320, int(2160 * sy)), (cx + 320, int(2160 * sy))], fill=STEEL, width=3)
    center(de, "by %s" % AUTHOR, cx, int(2230 * sy), font(REG, int(54 * sy)), (203, 213, 225))
    center(de, "Open source CC BY 4.0", cx, int(2310 * sy), font(REG, int(34 * sy)), MUTE)
    eb.save(EBOOK, "PNG", optimize=True)
    print("[ok] %s (1600 x 2560)" % EBOOK)

    # ============ social card 1200x630 ============
    sc = Image.new("RGB", (1200, 630), NAVY_TOP)
    ds = ImageDraw.Draw(sc)
    gradient(ds, 1200, 630)
    ds.rectangle([80, 118, 170, 126], fill=RED)
    ft = font(BOLD, 78)
    center(ds, "A High-Value", 600, 150, ft, WHITE)
    center(ds, "Investment Guidebook", 600, 240, ft, WHITE)
    fs = font(REG, 34)
    center(ds, "What it costs, what it returns, how strong the evidence is", 600, 350, fs, BLUE)
    fp = font(REG, 30)
    center(ds, "No stock tips. No courses to sell. Just evidence.", 600, 408, fp, LIGHT)
    chips = ["302 entries", "24 chapters", "Evidence A/B/C", "CC BY 4.0"]
    fch = font(REG, 26)
    gaps = 18
    cw = [tw(ds, ch, fch) + 34 for ch in chips]
    xx = 600 - (sum(cw) + gaps * (len(chips) - 1)) / 2
    yy = 478
    for ch, ww in zip(chips, cw):
        ds.rounded_rectangle([xx, yy, xx + ww, yy + 50], radius=25, outline=STEEL, width=2)
        center(ds, ch, xx + ww / 2, yy + 11, fch, LIGHT)
        xx += ww + gaps
    ff = font(REG, 22)
    center(ds, "Open-source evidence-based investing manual - cites only journals & official docs",
           600, yy + 86, ff, MUTE)
    sc.save(SOCIAL, "PNG", optimize=True)
    print("[ok] %s (1200 x 630)" % SOCIAL)


if __name__ == "__main__":
    main()
