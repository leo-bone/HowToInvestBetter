#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成纸书完整书封（KDP Paperback 6x9 全 wrap）。

KDP 排版规则（已核对官方帮助）：从左到右 = 封底 | 书脊 | 封面；四周出血 0.125"；
条码由 KDP 自动加在「封底右下角」（预留 2"x1.2" 空白，距书脊/底边 0.25"）。
尺寸公式：
  书脊 = 页数 x 纸张厚度（白纸 0.002252"/页，米色 0.0025"/页；不四舍五入）
  封面总宽 = 出血 + 封底 + 书脊 + 封面 + 出血
  封面总高 = 出血 + 裁切高 9" + 出血
输出：cover-paperback.png（300 DPI）+ cover-paperback.pdf（300 DPI，KDP 首选）
用法：python3 tools/gen_cover_paperback.py [--cream] [--pages N]
"""
import os
import argparse
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINT_PDF = os.path.join(ROOT, "HowToInvestBetter-print.pdf")
OUT_PNG = os.path.join(ROOT, "cover-paperback.png")
OUT_PDF = os.path.join(ROOT, "cover-paperback.pdf")
AUTHOR = "leo-bone"
TITLE = "高性价比投资指南"

HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"
DPI = 300.0
BLEED_IN = 0.125
TRIM_W, TRIM_H = 6.0, 9.0
PAPER_WHITE = 0.002252
PAPER_CREAM = 0.002500

NAVY_TOP, NAVY_BOT = (15, 27, 45), (23, 42, 71)
STEEL = (86, 104, 129)
LIGHT = (226, 232, 240)
BLUE = (147, 197, 253)
RED = (192, 57, 43)
MUTE = (100, 116, 139)


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def text_w(d, text, fnt):
    return int(d.textlength(text, font=fnt))


def center(d, text, cx, y, fnt, fill):
    d.text((cx - text_w(d, text, fnt) / 2, y), text, font=fnt, fill=fill)


def page_count():
    for mod in ("pypdf", "PyPDF2"):
        try:
            m = __import__(mod)
            return len(m.PdfReader(PRINT_PDF).pages)
        except Exception:
            pass
    return 338


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cream", action="store_true", help="米色纸（书脊更宽）")
    ap.add_argument("--pages", type=int, default=None)
    args = ap.parse_args()

    pages = args.pages or page_count()
    per = PAPER_CREAM if args.cream else PAPER_WHITE
    spine_in = pages * per
    cover_w_in = 2 * BLEED_IN + 2 * TRIM_W + spine_in
    cover_h_in = TRIM_H + 2 * BLEED_IN

    W = int(round(cover_w_in * DPI))
    H = int(round(cover_h_in * DPI))
    bleed = int(round(BLEED_IN * DPI))          # 37.5
    spine = int(round(spine_in * DPI))
    trim_w = int(round(TRIM_W * DPI))           # 1800
    trim_h = int(round(TRIM_H * DPI))           # 2700
    safe = int(round(0.30 * DPI))               # 0.3" 安全区（>0.25" 要求）

    trim_left = bleed
    trim_top = bleed
    back_x0 = trim_left                         # 封底：左面板
    spine_x0 = back_x0 + trim_w                 # 书脊：中间
    front_x0 = spine_x0 + spine                 # 封面：右面板

    img = Image.new("RGB", (W, H), NAVY_TOP)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    ry = trim_h / 2560.0     # 纵向比例（沿用竖版电子书封面 2560 基准）
    rx = trim_w / 1600.0     # 横向比例（基准 1600）

    def Y(v):
        return trim_top + int(v * ry)

    # ================= 封面（右面板） =================
    fx0 = front_x0
    cx = fx0 + trim_w / 2
    d.rectangle([fx0 + safe, trim_top + safe, fx0 + trim_w - safe, trim_top + trim_h - safe],
                outline=STEEL, width=int(4 * ry))
    bw = 180 * rx
    d.rectangle([cx - bw / 2, Y(220), cx + bw / 2, Y(236)], fill=RED)
    ft = font(HEITI, int(150 * ry))
    center(d, "高性价比", cx, Y(320), ft, (255, 255, 255))
    center(d, "投资指南", cx, Y(500), ft, (255, 255, 255))
    center(d, "循证投资手册", cx, Y(720), font(SONG, int(64 * ry)), (203, 213, 225))
    center(d, "花掉什么 · 换回什么 · 证据有多硬", cx, Y(830), font(SONG, int(50 * ry)), BLUE)
    d.line([(cx - 360 * rx, Y(960)), (cx + 360 * rx, Y(960))], fill=STEEL, width=int(3 * ry))
    chips = ["302 条", "24 章", "证据 A/B/C", "CC BY 4.0"]
    fch = font(SONG, int(44 * ry))
    gaps = 40 * rx
    cw = [text_w(d, ch, fch) + 56 * rx for ch in chips]
    xx = cx - (sum(cw) + gaps * (len(chips) - 1)) / 2
    yy = Y(1100)
    for ch, ww in zip(chips, cw):
        d.rounded_rectangle([xx, yy, xx + ww, yy + 96 * ry], radius=int(48 * ry),
                            outline=STEEL, width=int(3 * ry))
        center(d, ch, xx + ww / 2, yy + 24 * ry, fch, LIGHT)
        xx += ww + gaps
    fp = font(SONG, int(46 * ry))
    center(d, "不荐股 · 不卖课", cx, Y(1380), fp, LIGHT)
    center(d, "只把经过统计与监管文件验证的高性价比动作", cx, Y(1450), fp, LIGHT)
    center(d, "列成一张能按图索骥的清单", cx, Y(1520), fp, LIGHT)
    ff = font(SONG, int(44 * ry))
    d.line([(cx - 360 * rx, Y(2200)), (cx + 360 * rx, Y(2200))], fill=STEEL, width=int(3 * ry))
    center(d, "作者  %s" % AUTHOR, cx, Y(2270), ff, (203, 213, 225))
    center(d, "开源 CC BY 4.0 · 只引期刊论文与官方文件", cx, Y(2340), font(SONG, int(36 * ry)), MUTE)

    # ================= 书脊（中间） =================
    d.rectangle([spine_x0, trim_top, spine_x0 + spine, trim_top + trim_h], fill=(12, 22, 38))
    spine_text = "%s   %s" % (TITLE, AUTHOR)
    fsz = min(int(46 * (spine / 227.0)), 52)
    fsp = font(HEITI, fsz)
    tw = text_w(d, spine_text, fsp)
    pad = 24
    tmp = Image.new("RGBA", (tw + 2 * pad, spine), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((pad, (spine - fsz) / 2 - 4), spine_text, font=fsp, fill=(235, 240, 248))
    tmp = tmp.rotate(90, expand=True)   # 旋转后宽=spine，高=tw+2pad
    img.paste(tmp, (spine_x0, trim_top + int((trim_h - tmp.height) / 2)), tmp)
    d.line([(spine_x0, trim_top + 10), (spine_x0 + spine, trim_top + 10)], fill=STEEL, width=2)
    d.line([(spine_x0, trim_top + trim_h - 10), (spine_x0 + spine, trim_top + trim_h - 10)], fill=STEEL, width=2)

    # ================= 封底（左面板） =================
    bx0 = back_x0
    bcx = bx0 + trim_w / 2
    d.rectangle([bx0 + safe, trim_top + safe, bx0 + trim_w - safe, trim_top + trim_h - safe],
                outline=STEEL, width=int(4 * ry))
    center(d, "内容简介", bcx, Y(150), font(HEITI, int(54 * ry)), (255, 255, 255))
    d.line([(bcx - 200 * rx, Y(230)), (bcx + 200 * rx, Y(230))], fill=RED, width=int(4 * ry))
    body = font(SONG, int(40 * ry))
    para = [
        "一本不荐股、不卖课的循证投资手册。",
        "24 章 302 条投资动作，逐条标注：",
        "  花掉什么（费用·税·时间·精力·本金永久损失）",
        "  换回什么（长期真实回报·降波动·税费节省·避开归零）",
        "  证据有多硬（A 权威统计｜B 单项研究｜C 合理推论），",
        "并只引用期刊论文与官方文件，不引自媒体。",
    ]
    yy = Y(300)
    for line in para:
        d.text((bx0 + 160 * rx, yy), line, font=body, fill=LIGHT)
        yy += int(60 * ry)
    bullets = [
        "首创「三零原则」：花费、时间、毅力成本全为零的动作闭眼先做",
        "每条给原始出处，A/B/C 三级证据自己能核查",
        "适配中国市场的税费、ETF、打新、基金筛选",
        "开源 CC BY 4.0，可免费在线全文阅读",
    ]
    fbul = font(SONG, int(38 * ry))
    yy = Y(760)
    for b in bullets:
        d.text((bx0 + 160 * rx, yy), "•  " + b, font=fbul, fill=BLUE)
        yy += int(58 * ry)

    # 条码区：封底右下角，2"x1.2"，距书脊与底边各 0.25"
    bar_w, bar_h = int(round(2.0 * DPI)), int(round(1.2 * DPI))
    bar_right = spine_x0 - int(round(0.25 * DPI))
    bar_bottom = trim_top + trim_h - int(round(0.25 * DPI))
    bar_x, bar_y = bar_right - bar_w, bar_bottom - bar_h
    d.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(255, 255, 255), outline=STEEL, width=2)
    center(d, "条码由 KDP 自动添加", bar_x + bar_w / 2, bar_y + bar_h / 2 - 16 * ry, font(SONG, int(30 * ry)), (130, 130, 130))
    # ISBN 占位（在条码区上方，避免被覆盖）
    d.text((bar_x, bar_y - int(70 * ry)), "ISBN：由 KDP 免费分配", font=font(SONG, int(32 * ry)), fill=LIGHT)
    # 署名与仓库（置于条码区上方，避免被条码覆盖或压框）
    center(d, "作者 %s" % AUTHOR, bcx, trim_top + trim_h - int(640 * ry), font(SONG, int(36 * ry)), (203, 213, 225))
    center(d, "github.com/leo-bone/HowToInvestBetter", bcx,
           trim_top + trim_h - int(578 * ry), font(SONG, int(31 * ry)), MUTE)

    img.save(OUT_PNG, "PNG", optimize=True)

    # 300 DPI PDF（KDP 首选上传格式）
    made_pdf = False
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        c = rl_canvas.Canvas(OUT_PDF, pagesize=(cover_w_in * 72, cover_h_in * 72))
        c.drawImage(OUT_PNG, 0, 0, width=cover_w_in * 72, height=cover_h_in * 72)
        c.showPage()
        c.save()
        made_pdf = True
    except Exception as e:
        print("[warn] 未生成 PDF（缺 reportlab）:", e)

    print("[ok] 已生成 %s (%d x %d px, 300DPI)" % (OUT_PNG, W, H))
    if made_pdf:
        print("[ok] 已生成 %s (%.3f\" x %.3f\")" % (OUT_PDF, cover_w_in, cover_h_in))
    print("     纸张=%s 页数=%d 书脊=%.4f\"(%dpx) 全封面=%.4f\"x%.4f\"" % (
        "米色" if args.cream else "白纸", pages, spine_in, spine, cover_w_in, cover_h_in))
    print("     KDP 顺序：封底(左) | 书脊(中) | 封面(右)；条码区=封底右下角")


if __name__ == "__main__":
    main()
