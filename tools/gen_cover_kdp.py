#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成书籍竖版封面 cover-book.png（1600x2560，KDP 电子书/纸书封面、EPUB·PDF 封面用）。
比例 1:1.6，符合 Amazon KDP 封面建议（最小 1000x1600，理想 1600x2560）。
依赖：Pillow。用法：python3 tools/gen_cover_kdp.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cover-book.png")
AUTHOR = "leo-bone"

HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def draw_center(d, text, x_center, y, fnt, fill):
    w = int(d.textlength(text, font=fnt))
    d.text((x_center - w / 2, y), text, font=fnt, fill=fill)


def main():
    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), (15, 27, 45))
    d = ImageDraw.Draw(img)

    # 竖向渐变
    top, bot = (15, 27, 45), (23, 42, 71)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    # 外边框（浅色细线）
    d.rectangle([40, 40, W - 40, H - 40], outline=(86, 104, 129), width=4)

    cx = W / 2

    # 顶部红色强调条（居中短条）
    d.rectangle([cx - 90, 220, cx + 90, 236], fill=(192, 57, 43))

    # 主标题（两行更稳：主名 + 指南）
    f_title = font(HEITI, 150)
    draw_center(d, "高性价比", cx, 320, f_title, (255, 255, 255))
    draw_center(d, "投资指南", cx, 500, f_title, (255, 255, 255))

    # 副标题
    f_sub = font(SONG, 64)
    draw_center(d, "循证投资手册", cx, 720, f_sub, (203, 213, 225))

    # 标语
    f_tag = font(SONG, 50)
    draw_center(d, "花掉什么 · 换回什么 · 证据有多硬", cx, 830, f_tag, (147, 197, 253))

    # 分隔细线
    d.line([(cx - 360, 960), (cx + 360, 960)], fill=(86, 104, 129), width=3)

    # 数据 chips（居中排成一行）
    chips = ["302 条", "24 章", "证据 A/B/C", "CC BY 4.0"]
    f_chip = font(SONG, 44)
    # 先量总宽
    gaps = 40
    widths = [int(d.textlength(ch, font=f_chip)) + 56 for ch in chips]
    total = sum(widths) + gaps * (len(chips) - 1)
    x = cx - total / 2
    y = 1100
    for ch, w in zip(chips, widths):
        d.rounded_rectangle([x, y, x + w, y + 96], radius=48,
                            outline=(86, 104, 129), width=3)
        draw_center(d, ch, x + w / 2, y + 24, f_chip, (226, 232, 240))
        x += w + gaps

    # 中部一句话定位（居中两行）
    f_pos = font(SONG, 46)
    draw_center(d, "不荐股 · 不卖课", cx, 1380, f_pos, (226, 232, 240))
    draw_center(d, "只把经过统计与监管文件验证的高性价比动作", cx, 1450, f_pos, (226, 232, 240))
    draw_center(d, "列成一张能按图索骥的清单", cx, 1520, f_pos, (226, 232, 240))

    # 底部作者 + 开源声明
    f_foot = font(SONG, 44)
    d.line([(cx - 360, H - 360), (cx + 360, H - 360)], fill=(86, 104, 129), width=3)
    draw_center(d, "作者  %s" % AUTHOR, cx, H - 300, f_foot, (203, 213, 225))
    draw_center(d, "开源 CC BY 4.0 · 只引期刊论文与官方文件", cx, H - 230, f_foot, (100, 116, 139))

    img.save(OUT, "PNG", optimize=True)
    print("[ok] 已生成", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
