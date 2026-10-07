#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter 构建脚本（仅依赖 Python 标准库）

解析 book/ 下的章节 Markdown，生成：
  1. data.js        —— 供 index.html 在线/离线加载（<script src> 在 file:// 下可用）
  2. offline.html   —— 内联数据的单文件离线版（双击即开）

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
ENTRY_RE = re.compile(
    r"^##\s+(\d+)\s+(.+?)\s*"
    r"〔([ABC])〕〔影响：([^〕]+)〕〔花费：([^〕]+)〕〔时间：([^〕]+)〕〔毅力：([^〕]+)〕\s*$"
)
FIELD_RE = re.compile(r"^\*\*(花掉|换回|出处|说人话)\*\*[：:]\s*(.*)$")
NOTE_RE = re.compile(r"^>\s*〔([^〕]+)〕\s*(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$")


def parse_chapter(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    fname = os.path.basename(path)
    num = int(fname.split("-", 1)[0])
    label = fname.split("-", 1)[1].rsplit(".md", 1)[0]

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
                "spend": "",
                "gain": "",
                "source": "",
                "plain": "",
                "notes": [],
            }
            continue
        if cur is not None:
            fm = FIELD_RE.match(line)
            if fm:
                cur[{"花掉": "spend", "换回": "gain", "出处": "source", "说人话": "plain"}[fm.group(1)]] = fm.group(2).strip()
                continue
            nm = NOTE_RE.match(line)
            if nm:
                cur["notes"].append({"type": nm.group(1).strip(), "text": nm.group(2).strip()})
                continue
            if BULLET_RE.match(line):
                # stray bullet inside an entry block -> ignore
                continue
            if line.strip() == "":
                continue
        else:
            # before first entry: capture bullet list items (list-type chapter)
            bm = BULLET_RE.match(line)
            if bm and title is not None:
                items.append(bm.group(1).strip())

    if cur:
        entries.append(cur)

    return num, label, title, entries, items


def main():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    chapters = []
    entries = []
    lists = []
    problems = []

    for path in files:
        num, label, title, ch_entries, items = parse_chapter(path)
        if ch_entries:
            missing = [
                e["title"]
                for e in ch_entries
                if not (e["spend"] and e["gain"] and e["source"] and e["plain"])
            ]
            if missing:
                problems.append(f"[{label}] 缺少字段: {missing}")
            for e in ch_entries:
                three = (
                    e["cost_money"] == "无"
                    and e["cost_time"] == "无"
                    and e["cost_will"] == "无"
                )
                entries.append(
                    {
                        "chapter": num,
                        "num": e["num"],
                        "id": f"{num}-{e['num']}",
                        "title": e["title"],
                        "grade": e["grade"],
                        "impact": e["impact"],
                        "cost_money": e["cost_money"],
                        "cost_time": e["cost_time"],
                        "cost_will": e["cost_will"],
                        "three_zero": three,
                        "spend": e["spend"],
                        "gain": e["gain"],
                        "source": e["source"],
                        "plain": e["plain"],
                        "notes": e["notes"],
                    }
                )
            chapters.append(
                {
                    "num": num,
                    "label": label,
                    "title": title,
                    "file": "book/" + os.path.basename(path),
                    "count": len(ch_entries),
                    "type": "entries",
                }
            )
        else:
            lists.append({"chapter": num, "title": title, "items": items})
            chapters.append(
                {
                    "num": num,
                    "label": label,
                    "title": title,
                    "file": "book/" + os.path.basename(path),
                    "count": len(items),
                    "type": "list",
                }
            )

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

    # 1) data.js
    js = "window.BOOK_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
    with open(os.path.join(ROOT, "data.js"), "w", encoding="utf-8") as f:
        f.write(js)

    # 2) offline.html (inline data into index.html template)
    idx_path = os.path.join(ROOT, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            html = f.read()
        inline = '<script>window.BOOK_DATA = ' + json.dumps(data, ensure_ascii=False) + ';</script>'
        html = re.sub(r'<script src="data\.js"></script>', inline, html)
        with open(os.path.join(ROOT, "offline.html"), "w", encoding="utf-8") as f:
            f.write(html)

    # stats
    grade_count = {}
    three_count = 0
    for e in entries:
        grade_count[e["grade"]] = grade_count.get(e["grade"], 0) + 1
        if e["three_zero"]:
            three_count += 1
    print(f"✅ 解析完成：{len(chapters)} 章 / {len(entries)} 条条目 / {len(lists)} 个清单")
    print(f"   证据等级 A={grade_count.get('A',0)} B={grade_count.get('B',0)} C={grade_count.get('C',0)}")
    print(f"   三零（极高性价比）条目：{three_count}")
    print(f"   已生成 data.js 与 offline.html")


if __name__ == "__main__":
    main()
