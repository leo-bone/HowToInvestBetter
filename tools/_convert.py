#!/usr/bin/env python3
# 一次性格式转换：把旧格式条目转成原书格式。幂等（已是新格式则跳过）。
import re, glob, os

BOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "book")

OLD = re.compile(
    r"^##\s+(\d+)\s+(.+?)\s*〔([ABC])〕〔影响：([^〕]+)〕〔花费：([^〕]+)〕〔时间：([^〕]+)〕〔毅力：([^〕]+)〕\s*$"
)

COST = {"无": "0", "低": "少", "高": "多", "0": "0"}
TIME = {"无": "0", "低": "少", "高": "多", "0": "0"}
WILL = {"无": "否", "低": "些", "高": "多", "否": "否"}


def convert(text):
    lines = text.split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        m = OLD.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        num, title, grade, impact, spend, tm, will = m.groups()
        j = i + 1
        block = []
        while j < n and not lines[j].startswith("## ") and not lines[j].startswith("# "):
            block.append(lines[j]); j += 1

        cost = plain = gain = src = None
        notes = []
        for ln in block:
            if ln.startswith("**花掉**："):
                cost = ln[len("**花掉**："):].strip()
            elif ln.startswith("**换回**："):
                gain = ln[len("**换回**："):].strip()
            elif ln.startswith("**出处**："):
                src = ln[len("**出处**："):].strip()
            elif ln.startswith("**说人话**："):
                plain = ln[len("**说人话**："):].strip()
            elif ln.lstrip().startswith(">"):
                notes.append(ln.lstrip().lstrip(">").strip())
            elif ln.strip():
                notes.append(ln.strip())

        out.append("### %d. %s" % (int(num), title))
        out.append("<!-- 标签: 钱=%s 时间=%s 毅力=%s 收益=中 口径=金钱 影响=%s -->" % (
            COST.get(spend, spend), TIME.get(tm, tm), WILL.get(will, will), impact.strip()))
        if cost:
            out.append("- 成本：%s" % cost)
        if plain:
            out.append("- 说人话：%s" % plain)
        if gain:
            out.append("- 收益：%s" % gain)
        out.append("- 证据等级：%s" % grade)
        if src:
            out.append("- 来源：%s" % src)
        note = " ".join(x for x in notes if x.strip())
        if note:
            out.append("- 备注：%s" % note)
        out.append("")
        i = j
    return "\n".join(out)


def main():
    total = 0
    for path in sorted(glob.glob(os.path.join(BOOK, "*.md"))):
        txt = open(path, encoding="utf-8").read()
        if "### " in txt and "<!-- 标签:" in txt and not OLD.search(txt):
            print("[skip] 已是新格式:", os.path.basename(path)); continue
        new = convert(txt)
        if new != txt:
            open(path, "w", encoding="utf-8").write(new)
            cnt = len(re.findall(r"^### \d+\.", new, re.M))
            print("[ok] %s -> %d 条" % (os.path.basename(path), cnt))
            total += cnt
    print("转换条目合计:", total)


if __name__ == "__main__":
    main()
