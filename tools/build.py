#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter 构建脚本（仅依赖 Python 标准库）

解析 book/ 下的章节 Markdown（原书格式），生成：
  1. data.js        —— 供 index.html 在线/离线加载（<script src> 在 file:// 下可用）
  2. offline.html   —— 内联数据的单文件离线版（双击即开）

条目格式：
  ### N. 标题
  <!-- 标签: 钱=0 时间=少 毅力=否 收益=中 口径=金钱 影响=自己 -->
  - 成本：...
  - 说人话：...
  - 收益：...
  - 证据等级：A
  - 来源：...
  - 备注：...

用法：
  python3 tools/build.py
"""
import os
import re
import json
import glob
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
TAG_RE = re.compile(r"^<!--\s*标签:\s*(.+?)\s*-->$")
FIELD_RE = re.compile(r"^-\s*(成本|说人话|收益|证据等级|来源|备注)[：:]\s*(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$")

TAG_KEYS = ["钱", "时间", "毅力", "收益", "口径", "影响"]


def parse_tags(comment):
    tags = {}
    for part in re.split(r"\s+", comment.strip()):
        if "=" in part:
            k, v = part.split("=", 1)
            tags[k.strip()] = v.strip()
    return {k: tags.get(k, "") for k in TAG_KEYS}


def parse_chapter(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    fname = os.path.basename(path)
    num = int(fname.split("-", 1)[0])
    label = fname.split("-", 1)[1].rsplit(".md", 1)[0]

    title = None
    intro = []          # 章前导语/索引（title 与第一条之间的文本）
    entries = []
    items = []
    cur = None
    pending_tag = None

    for line in lines:
        m = HEAD_RE.match(line)
        if m and title is None and not line.startswith("##"):
            title = m.group(1).strip()
            continue

        m = TAG_RE.match(line)
        if m:
            parsed = parse_tags(m.group(1))
            # 标签注释通常紧跟在标题之后，归属当前条目；零星前置则暂存
            if cur is not None and not any(cur["tags"].values()):
                cur["tags"] = parsed
            else:
                pending_tag = parsed
            continue

        m = ENTRY_RE.match(line)
        if m:
            if cur:
                entries.append(cur)
            cur = {
                "num": int(m.group(1)),
                "title": m.group(2).strip(),
                "tags": pending_tag or {k: "" for k in TAG_KEYS},
                "cost": "", "plain": "", "gain": "", "grade": "", "source": "", "note": "",
            }
            pending_tag = None
            continue

        if cur is not None:
            fm = FIELD_RE.match(line)
            if fm:
                key = {"成本": "cost", "说人话": "plain", "收益": "gain",
                       "证据等级": "grade", "来源": "source", "备注": "note"}[fm.group(1)]
                cur[key] = (cur[key] + " " + fm.group(2).strip()).strip() if cur[key] else fm.group(2).strip()
                continue
            if line.strip() == "":
                continue
            # 条目内非字段行：并入备注
            if not line.startswith("###") and not line.startswith("#"):
                cur["note"] = (cur["note"] + " " + line.strip()).strip()
            continue

        # before first entry
        if title is not None:
            if line.strip() == "":
                continue
            bm = BULLET_RE.match(line)
            if bm:
                items.append(bm.group(1).strip())
            else:
                intro.append(line.strip())

    if cur:
        entries.append(cur)

    return num, label, title, intro, entries, items


def main():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    chapters = []
    entries = []
    lists = []
    problems = []

    for path in files:
        num, label, title, intro, ch_entries, items = parse_chapter(path)
        if ch_entries:
            missing = [
                e["title"]
                for e in ch_entries
                if not (e["cost"] and e["gain"] and e["source"] and e["plain"] and e["grade"])
            ]
            if missing:
                problems.append(f"[{label}] 缺少字段: {missing}")
            for e in ch_entries:
                t = e["tags"]
                three = (t.get("钱") == "0" and t.get("时间") in ("0",) and t.get("毅力") == "否")
                entries.append({
                    "chapter": num,
                    "num": e["num"],
                    "id": f"{num}-{e['num']}",
                    "title": e["title"],
                    "grade": e["grade"],
                    "tags": t,
                    "impact": t.get("影响", ""),
                    "cost_money": t.get("钱", ""),
                    "cost_time": t.get("时间", ""),
                    "cost_will": t.get("毅力", ""),
                    "benefit": t.get("收益", ""),
                    "scope": t.get("口径", ""),
                    "three_zero": three,
                    "cost": e["cost"],
                    "plain": e["plain"],
                    "gain": e["gain"],
                    "source": e["source"],
                    "note": e["note"],
                })
            chapters.append({
                "num": num, "label": label, "title": title,
                "intro": intro,
                "file": "book/" + os.path.basename(path),
                "count": len(ch_entries), "type": "entries",
            })
        else:
            lists.append({"chapter": num, "title": title, "items": items})
            chapters.append({
                "num": num, "label": label, "title": title,
                "intro": intro,
                "file": "book/" + os.path.basename(path),
                "count": len(items), "type": "list",
            })

    if problems:
        print("⚠️ 解析问题：")
        for p in problems:
            print("  -", p)

    data = {
        "updated": datetime.date.today().isoformat(),
        "chapters": chapters,
        "entries": entries,
        "lists": lists,
    }

    js = "window.BOOK_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
    with open(os.path.join(ROOT, "data.js"), "w", encoding="utf-8") as f:
        f.write(js)

    idx_path = os.path.join(ROOT, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            html = f.read()
        inline = '<script>window.BOOK_DATA = ' + json.dumps(data, ensure_ascii=False) + ';</script>'
        html = re.sub(r'<script src="data\.js"></script>', inline, html)
        with open(os.path.join(ROOT, "offline.html"), "w", encoding="utf-8") as f:
            f.write(html)

    grade_count = {}
    three_count = 0
    for e in entries:
        grade_count[e["grade"]] = grade_count.get(e["grade"], 0) + 1
        if e["three_zero"]:
            three_count += 1
    chars = sum(len(open(p, encoding="utf-8").read()) for p in files)
    print(f"✅ 解析完成：{len(chapters)} 章 / {len(entries)} 条条目 / {len(lists)} 个清单")
    print(f"   证据等级 A={grade_count.get('A',0)} B={grade_count.get('B',0)} C={grade_count.get('C',0)}")
    print(f"   三零（极高性价比）条目：{three_count}")
    print(f"   正文字数：约 {chars:,} 字")
    print(f"   已生成 data.js 与 offline.html")


if __name__ == "__main__":
    main()
