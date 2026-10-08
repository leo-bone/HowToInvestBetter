#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英文版构建脚本（仅依赖 Python 标准库）
解析 en/book/ 下的章节 Markdown（英文六字段格式），生成：
  1. en/data.js        —— 供 en/index.html 加载
  2. en/offline.html   —— 内联数据的单文件离线版

条目格式：
  ### N. Title
  <!-- tags: money=0 time=little will=no payoff=mid scope=money impact=self -->
  - Cost: ...
  - In plain terms: ...
  - Payoff: ...
  - Evidence grade: A
  - Sources: ...
  - Note: ...

同时做一致性 lint（字段缺失 / 标签键缺失 / 标签值非法 / 证据等级非法 / 残留中文"第X条"）。
用法：python3 tools/build_en.py
"""
import os
import re
import json
import glob
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "en", "book")
OUT_DIR = os.path.join(ROOT, "en")

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
TAG_RE = re.compile(r"^<!--\s*tags:\s*(.+?)\s*-->$")
FIELD_RE = re.compile(r"^-\s*(Cost|In plain terms|Payoff|Evidence grade|Sources|Note)[：:]\s*(.*)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$")

TAG_KEYS = ["money", "time", "will", "payoff", "scope", "impact"]
VALID_VALUES = {
    "money": {"0", "little", "mid", "high"},
    "time": {"0", "little", "some"},
    "will": {"no", "some", "much"},
    "payoff": {"low", "mid", "high"},
    "scope": {"money", "time", "health", "relationship", "energy"},
    "impact": {"self", "family", "self+family"},
}
FIELD_MAP = {"Cost": "cost", "In plain terms": "plain", "Payoff": "gain",
             "Evidence grade": "grade", "Sources": "source", "Note": "note"}
# 残留中文"第X条 / 第X章第Y条"检测（英文文件不应出现）
CN_XREF_RE = re.compile(r"第\s*\d+\s*(?:章)?\s*条")


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
    intro = []
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
                key = FIELD_MAP[fm.group(1)]
                cur[key] = (cur[key] + " " + fm.group(2).strip()).strip() if cur[key] else fm.group(2).strip()
                continue
            if line.strip() == "":
                continue
            if not line.startswith("###") and not line.startswith("#"):
                cur["note"] = (cur["note"] + " " + line.strip()).strip()
            continue
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
            missing = [e["title"] for e in ch_entries
                       if not (e["cost"] and e["gain"] and e["source"] and e["plain"] and e["grade"])]
            if missing:
                problems.append("[%s] missing fields: %s" % (label, missing))
            for e in ch_entries:
                t = e["tags"]
                for k in TAG_KEYS:
                    if not t.get(k):
                        problems.append("[%s] Entry %d: tag %s empty" % (label, e["num"], k))
                    elif t.get(k) not in VALID_VALUES[k]:
                        problems.append("[%s] Entry %d: tag %s=%s invalid" % (label, e["num"], k, t.get(k)))
                if e["grade"] not in ("A", "B", "C"):
                    problems.append("[%s] Entry %d: grade '%s' invalid" % (label, e["num"], e["grade"]))
                three = (t.get("money") == "0" and t.get("time") == "0" and t.get("will") == "no")
                entries.append({
                    "chapter": num, "num": e["num"], "id": "%d-%d" % (num, e["num"]),
                    "title": e["title"], "grade": e["grade"], "tags": t,
                    "impact": t.get("impact", ""), "cost_money": t.get("money", ""),
                    "cost_time": t.get("time", ""), "cost_will": t.get("will", ""),
                    "benefit": t.get("payoff", ""), "scope": t.get("scope", ""),
                    "three_zero": three,
                    "cost": e["cost"], "plain": e["plain"], "gain": e["gain"],
                    "source": e["source"], "note": e["note"],
                })
            chapters.append({
                "num": num, "label": label, "title": title, "intro": intro,
                "file": "en/book/" + os.path.basename(path),
                "count": len(ch_entries), "type": "entries",
            })
        else:
            lists.append({"chapter": num, "title": title, "items": items})
            chapters.append({
                "num": num, "label": label, "title": title, "intro": intro,
                "file": "en/book/" + os.path.basename(path),
                "count": len(items), "type": "list",
            })

    # 残留中文"第X条"检测（英文文件不应出现；导语/正文中）
    for path in files:
        for i, line in enumerate(open(path, encoding="utf-8"), 1):
            if CN_XREF_RE.search(line):
                problems.append("[%s] line %d: residual Chinese cross-ref '第X条' found" % (os.path.basename(path), i))

    if problems:
        print("⚠️ Lint problems (%d):" % len(problems))
        for p in problems[:60]:
            print("  -", p)
        if len(problems) > 60:
            print("  ... and %d more" % (len(problems) - 60))

    data = {
        "updated": datetime.date.today().isoformat(),
        "chapters": chapters, "entries": entries, "lists": lists,
    }
    js = "window.BOOK_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
    with open(os.path.join(OUT_DIR, "data.js"), "w", encoding="utf-8") as f:
        f.write(js)

    idx_path = os.path.join(OUT_DIR, "index.html")
    if os.path.exists(idx_path):
        html = open(idx_path, encoding="utf-8").read()
        inline = '<script>window.BOOK_DATA = ' + json.dumps(data, ensure_ascii=False) + ';</script>'
        html = re.sub(r'<script src="data\.js"></script>', inline, html)
        with open(os.path.join(OUT_DIR, "offline.html"), "w", encoding="utf-8") as f:
            f.write(html)

    grade_count = {}
    three_count = 0
    for e in entries:
        grade_count[e["grade"]] = grade_count.get(e["grade"], 0) + 1
        if e["three_zero"]:
            three_count += 1
    chars = sum(len(open(p, encoding="utf-8").read()) for p in files)
    print("✅ EN parse done: %d chapters / %d entries / %d lists" % (len(chapters), len(entries), len(lists)))
    print("   Evidence grade A=%d B=%d C=%d" % (grade_count.get("A", 0), grade_count.get("B", 0), grade_count.get("C", 0)))
    print("   Three-Zero entries: %d" % three_count)
    print("   English chars (rough): ~%d" % chars)
    print("   Generated en/data.js" + (" and en/offline.html" if os.path.exists(idx_path) else ""))


if __name__ == "__main__":
    main()
