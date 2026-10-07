#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HowToInvestBetter —— 内容质量校验（产品化收口）

检查项：
  1. 字段完整性：每条必须有 成本/说人话/收益/证据等级/来源（备注可选）
  2. 标签完整性：每条必须有 <!-- 标签: 钱/时间/毅力/收益/口径/影响 -->
  3. 残留未核实：全书不得出现「待核实」
  4. ID 唯一性（第X章第Y条 不得重复）
  5. 交叉引用（「第X章第Y条」）是否都能解析到
  6. 争议标注统计、三零条目、证据等级分布

用法：
  python3 tools/lint.py
返回非 0 表示存在问题（可用于 CI / 提交前检查）。
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")

HEAD_RE = re.compile(r"^#\s+(.+?)\s*$")
ENTRY_RE = re.compile(r"^###\s+(\d+)\.\s+(.+?)\s*$")
TAG_RE = re.compile(r"^<!--\s*标签:\s*(.+?)\s*-->$")
FIELD_RE = re.compile(r"^-\s*(成本|说人话|收益|证据等级|来源|备注)[：:]\s*(.*)$")
TAG_KEYS = ["钱", "时间", "毅力", "收益", "口径", "影响"]
XREF_RE = re.compile(r"第\s*(\d+)\s*[章节]\s*第\s*(\d+)\s*条")


def collect():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    chapters = []
    entries = []
    list_items = []
    for path in files:
        num = int(os.path.basename(path).split("-", 1)[0])
        raw = open(path, encoding="utf-8").read()
        title = None
        cur = None
        in_entries = False
        for line in raw.split("\n"):
            m = HEAD_RE.match(line)
            if m and title is None and not line.startswith("##"):
                title = m.group(1).strip()
                continue
            m = ENTRY_RE.match(line)
            if m:
                in_entries = True
                if cur:
                    entries.append(cur)
                cur = {
                    "chapter": num, "num": int(m.group(1)), "title": m.group(2).strip(),
                    "grade": "", "tags": {}, "fields": {}, "raw": raw,
                    "src": os.path.basename(path),
                }
                continue
            tm = TAG_RE.match(line)
            if tm and cur is not None:
                tags = {}
                for part in re.split(r"\s+", tm.group(1).strip()):
                    if "=" in part:
                        k, v = part.split("=", 1)
                        tags[k.strip()] = v.strip()
                cur["tags"] = tags
                continue
            if cur is not None:
                fm = FIELD_RE.match(line)
                if fm:
                    k = fm.group(1)
                    cur["fields"][k] = fm.group(2).strip()
                    if k == "证据等级" and fm.group(2).strip():
                        cur["grade"] = fm.group(2).strip()[0]
                    continue
                if line.strip() == "":
                    continue
            if not in_entries:
                bm = re.match(r"^[-*]\s+(.+?)\s*$", line)
                if bm:
                    list_items.append(bm.group(1).strip())
        if cur:
            entries.append(cur)
        chapters.append((num, title or "未命名", len([e for e in entries if e["chapter"] == num])))
    return chapters, entries, list_items


def main():
    chapters, entries, list_items = collect()
    problems = []

    # 1. 字段完整性
    for e in entries:
        miss = [k for k in ("成本", "说人话", "收益", "证据等级", "来源") if not e["fields"].get(k)]
        if miss:
            problems.append("字段缺失 [%s] 第%d章第%d条《%s》缺：%s" % (
                e["src"], e["chapter"], e["num"], e["title"], "、".join(miss)))

    # 2. 标签完整性
    for e in entries:
        miss = [k for k in TAG_KEYS if not e["tags"].get(k)]
        if miss:
            problems.append("标签缺失 [%s] 第%d章第%d条《%s》缺：%s" % (
                e["src"], e["chapter"], e["num"], e["title"], "、".join(miss)))

    # 3. 待核实残留
    for e in entries:
        blob = " ".join(e["fields"].values())
        if "待核实" in blob:
            problems.append("未核实残留 [%s] 第%d章第%d条《%s》仍含「待核实」" % (
                e["src"], e["chapter"], e["num"], e["title"]))

    # 4. ID 唯一性
    ids = {}
    for e in entries:
        key = (e["chapter"], e["num"])
        ids[key] = ids.get(key, 0) + 1
    for k, v in ids.items():
        if v > 1:
            problems.append("ID 重复：第%d章第%d条 出现 %d 次" % (k[0], k[1], v))

    # 5. 交叉引用校验
    valid_refs = set((e["chapter"], e["num"]) for e in entries)
    xref_missing = []
    seen = set()
    for e in entries:
        for cm, em in XREF_RE.findall(e["raw"]):
            ref = (int(cm), int(em))
            if ref in seen:
                continue
            seen.add(ref)
            if ref not in valid_refs:
                xref_missing.append("引用失效 [%s] 第%d章第%d条 指向 第%d章第%d条（不存在）" % (
                    e["src"], e["chapter"], e["num"], ref[0], ref[1]))

    # 统计
    grade = {"A": 0, "B": 0, "C": 0}
    for e in entries:
        grade[e["grade"]] = grade.get(e["grade"], 0) + 1
    three = [e for e in entries
             if e["tags"].get("钱") == "0" and e["tags"].get("时间") == "0" and e["tags"].get("毅力") == "否"]
    dispute = sum(1 for e in entries if "争议" in (e["fields"].get("备注") or e["fields"].get("证据等级", "")))

    print("=== HowToInvestBetter 内容质量校验 ===")
    print("章节数：%d ｜ 条目数：%d ｜ 清单条目：%d" % (len(chapters), len(entries), len(list_items)))
    print("证据等级 A=%d B=%d C=%d" % (grade["A"], grade["B"], grade["C"]))
    print("三零条目：%d ｜ 含争议标注：%d" % (len(three), dispute))
    print("交叉引用检查：%d 处，失效 %d 处" % (len(seen), len(xref_missing)))
    print("问题总数：%d" % (len(problems) + len(xref_missing)))

    if problems or xref_missing:
        print("\n--- 待修复 ---")
        for p in problems:
            print("  ✗", p)
        for p in xref_missing:
            print("  ✗", p)
        return 1
    print("\n✅ 全部通过：字段完整、标签齐全、无未核实残留、ID 唯一、交叉引用有效。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
