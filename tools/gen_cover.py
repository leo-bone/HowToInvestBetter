#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成分享封面图 cover.png（1200x630，GitHub Pages / 社交分享卡片 / EPUB·PDF 封面用）。
依赖：Pillow（构建时安装，读者无需）。
用法：python3 tools/gen_cover.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cover.png")

# 中文字体：优先黑体（标题粗），正文用宋体
HEITI = "/System/Library/Fonts/STHeiti Medium.ttc"
SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"


def font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def main():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (15, 27, 45))
    d = ImageDraw.Draw(img)

    # 背景竖向渐变（深海军蓝 -> 略亮）
    top = (15, 27, 45)
    bot = (23, 42, 71)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    # 顶部强调色条
    d.rectangle([80, 118, 170, 126], fill=(47, 158, 68))

    # 主标题
    f_title = font(HEITI, 92)
    d.text((80, 150), "高性价比投资指南", font=f_title, fill=(255, 255, 255))

    # 副标题
    f_sub = font(SONG, 40)
    d.text((82, 268), "循证投资手册", font=f_sub, fill=(203, 213, 225))

    # 标语
    f_tag = font(SONG, 33)
    d.text((82, 340), "花掉什么 · 换回什么 · 证据有多硬", font=f_tag, fill=(147, 197, 253))

    # 数据 chips
    chips = ["302 条", "24 章", "证据 A/B/C"]
    x = 82
    y = 470
    f_chip = font(SONG, 26)
    for ch in chips:
        w = int(d.textlength(ch, font=f_chip)) + 34
        d.rounded_rectangle([x, y, x + w, y + 50], radius=25,
                            outline=(86, 104, 129), width=2)
        d.text((x + 17, y + 11), ch, font=f_chip, fill=(226, 232, 240))
        x += w + 18

    # 页脚
    f_foot = font(SONG, 22)
    d.text((82, y + 78), "循证投资手册 · 只引期刊论文与官方文件",
           font=f_foot, fill=(100, 116, 139))

    img.save(OUT, "PNG", optimize=True)
    print("[ok] 已生成", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
