# KDP 英文版「上线 + 导流」推广包（Launch & Derivation Kit）

> 配套 [`KDP-英文版填报表.md`](KDP-英文版填报表.md)（字段填报）与 [`KDP-上传操作指南.md`](KDP-上传操作指南.md)（账户/税务/收款）。
> 本包解决两件事：**① 实体样书（Proof）到手后怎么验收**；**② 上线后怎么发文导流**（Amazon 描述 + 社媒 + 30 天节奏）。
> 文案主体为英文（面向 Amazon.com 受众）；给用户的检查说明为中文。

---

## A. 作者样书（Author Copy / Proof）验收清单

KDP 纸书上线前**务必先买一本 Author Copy**（比读者价便宜、不公开销售），到手后逐项核对，再点 Approve。电子版无样书，靠后台 Preview 翻一遍即可。

```
[ ] 1. 书脊：标题 / 作者文字方向正确（竖排旋转）、居中、不被裁切、不被胶口压住
[ ] 2. 封面 / 封底：四周 0.125″ 出血无白边；图案 / 文字不切边；封底右下角条码区留白正确
[ ] 3. 内文：页码连续、无空白页 / 重复页；第 1 章从奇数页（右页）起
[ ] 4. 图表 / 表格：无跨页断裂、无溢出文本框、无图片模糊（本版纯文字，重点查表格换行）
[ ] 5. 字体：英文无乱码；引号 " " 、破折号 — 、连字符 - 渲染正确（最容易出问题）
[ ] 6. 版权页：书名 / 副标题 / 作者 / 版权声明 / 年份 齐全
[ ] 7. 手感：纸张厚度（White 标准）、装订是否开胶、翻页是否掉页
[ ] 8. 比对：样书与上传的 HowToInvestBetter-en-print.pdf 视觉一致（尤其书脊宽度）
```

> ⚠️ 书脊 = 383 × 0.002252″ = 0.8625″，是按 **White 纸 + 当前页数** 算的。若样书书脊与封面不符，说明内文页数变了 → 重跑 `build_en_pdf.py --print` + `gen_cover_en.py` 再投稿。

---

## B. Amazon 图书描述（HTML · 整段复制）

> KDP 描述支持有限 HTML：`<b> <i> <u> <h2> <p> <br> <ul><li> <a>`。下面整段复制粘贴即可。
> 这一段是**最终版**，已取代填报表 §2 的纯文本占位。

```html
<h2>Most investing books tell you what to do. This one shows you the evidence — and the price tag.</h2>

<p><b>A High-Value Investment Guidebook</b> is a field manual of <b>302 independent, debatable moves</b>, each one rated for what it costs you, what it returns, and how strong the evidence behind it really is.</p>

<p>Every entry carries a transparent <b>Evidence Grade</b>:</p>
<ul>
<li><b>A</b> — hard regulation or settled research</li>
<li><b>B</b> — strong statistical regularity</li>
<li><b>C</b> — plausible but unproven</li>
</ul>
<p>…and cites only primary sources: peer-reviewed journals, securities regulators, and official tax codes. No gurus. No "trust me." No affiliate links.</p>

<p>Inside you'll find:</p>
<ul>
<li><b>24 chapters</b> covering fees &amp; taxes, index investing, investor behavior, asset allocation, retirement, real estate, insurance, crypto, and the moves that quietly destroy returns.</li>
<li>The <b>"Three-Zero" shortlist</b>: 16 entries that cost almost nothing, take little time, and need no willpower — yet reliably improve outcomes.</li>
<li>Plain-language translations of the academic findings that actually move the needle, with the original citations so you can verify them yourself.</li>
</ul>

<p><b>Who it's for:</b> the self-directed investor who is tired of conflicting advice and wants a calm, evidence-first map of what's worth doing — and what's not.</p>

<p>This Kindle / paperback edition is the carefully formatted, citation-linked, portable version — built for the reader who wants the whole map in one place.</p>

<p><i>Copyright © 2026 leo. All rights reserved.</i></p>
```

> 文案逻辑：强调「循证、可核查出处、排版精修、方便携带」；不在描述里放竞品或外部链接（会被拒）。

---

## C. 首发社媒文案（英文 · 复制即用）

### C1. X / Twitter  Thread（7 条，顺序发）

**1/** I spent two years grading 302 investing "tips" by their actual evidence — what they cost, what they return, and how strong the proof really is. The findings that surprised me most 🧵

**2/** Finding #1: the highest-grade move in the whole book costs $0 and ~10 minutes. Switching from an actively managed fund to a low-cost index fund cuts ~1% off your annual cost — the single most reliable boost to long-term returns. Grade A.

**3/** Finding #2: most "beat the market" newsletters and stock-picking services grade C. Not because they're scams — because outperformance is statistically hard to repeat and almost never survives fees. Paying for it is usually Grade C at best.

**4/** Finding #3: the "Three-Zero" shortlist — 16 moves that cost zero money, zero time, and zero willpower. Doing just these beats 90% of the "active" things people stress about. The book is basically a ranked list of what deserves your attention.

**5/** Finding #4: taxes are the only certainty. Account ordering, holding periods, and tax-loss harvesting are all Grade A — boring, but they move real after-tax returns more than clever stock picks.

**6/** I wrote an evidence-graded, 302-entry investing guide because the evidence shouldn't be behind jargon. If you want the formatted, citation-linked edition, it's on Amazon. Link in replies.

**7/** Formatted Kindle/paperback edition: [AMAZON_LINK_ONCE_LIVE]. RT the first tweet if this belongs in more people's hands.

### C2. Reddit 发帖（r/Bogleheads 或 r/personalfinance · 价值先行，不硬广）

**Title:** A 302-entry, evidence-graded investing guide (free sample inside)

**Body:**
I got tired of investment advice that can't show its work, so I built a field manual: 302 independent moves, each one stating (1) what it costs, (2) what it returns, and (3) an Evidence Grade A/B/C with the original citation — only peer-reviewed papers and official docs, no gurus.

It covers fees, index investing, behavior, allocation, retirement, real estate, insurance, crypto, and the moves that quietly destroy returns. The "Three-Zero" shortlist (16 free, low-effort, high-grade moves) is the part I'd start with.

The formatted Kindle/paperback edition is on Amazon: [AMAZON_LINK_ONCE_LIVE]
I also put out a formatted Kindle/paperback version for people who want it portable.

Genuinely curious: which "common sense" investing tip do you think would grade lowest if held to this standard?

### C3. Newsletter / 邮件（短版）

**Subject:** 302 investing moves, graded by evidence

Most advice tells you what to do. I wanted to know what it's worth — and how strong the proof is. So I graded 302 moves on cost, payoff, and evidence (A/B/C), citing only journals and official documents.

Formatted edition on Amazon: [AMAZON_LINK_ONCE_LIVE]
Formatted edition: [AMAZON_LINK_ONCE_LIVE]

Start with the "Three-Zero" shortlist — 16 moves that cost nothing and need no willpower, yet reliably help.

---

## D. 上线后 30 天节奏

```
[ ] Day 0   双版本上线（ebook $4.99 / pb $16.99）；记下 ASIN / ISBN
[ ] Day 1   发 X thread 并置顶；Reddit 发帖；把 Amazon 链接补进 C1/C3 占位
[ ] Day 1-7 邀 10–15 位早期读者留评（Author Central 的 "Share with friends" / 直接发链接）
           —— 没有 review 转化率极低，这是最关键的一步
[ ] Week 2  纸书可报 Amazon Vine（需 FBA 库存；免费换真实评测；电子书无 Vine）
[ ] Week 2-4 定价 A/B：ebook 试 $3.99 冲量 vs 维持 $4.99，看销量/排名
[ ] 持续    在 en/index.html 与社媒保持 Amazon 入口与购买链接。
[ ] 闭环    免费全文版权页 / 每章末放 "Prefer a formatted copy? → Amazon" 引流句
```

> 注意：本项目**不勾 KDP Select**，故无 KU / KENP 读后付费；导流核心靠「免费全文 → 付费便携版」的转化，而非 KU 内阅。

---

## E. 上线物料自检（仓库内已就绪）

| 物料 | 文件 | 用途 |
|---|---|---|
| 电子书正文 | `HowToInvestBetter-en.epub` | KDP 上传（含内嵌封面） |
| 电子书封面 | `cover-book-en.png` | 1600×2560 |
| 纸书内文 | `HowToInvestBetter-en-print.pdf` | 383 页 / 6×9 / Bleed |
| 纸书书封 | `cover-paperback-en.pdf` | 13.1125″×9.2500″ / 300 DPI |
| 社交卡 | `en-cover.png` | 1200×630，社媒配图 |
