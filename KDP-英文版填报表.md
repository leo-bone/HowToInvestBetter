# KDP 英文版上架填报表（English Edition · copy-paste ready）

> 目标市场：**Amazon.com（美国站，最大英文市场）**。账户、税务（W-8BEN）、收款（Payoneer/WorldFirst）三步与中文版完全相同，
> 见 [`KDP-上传操作指南.md`](KDP-上传操作指南.md) §1；本表只备英文版**要填的字段**与**上传资产**，复制即可。
> 战略与竞品见 [`AMAZON-上架方案.md`](AMAZON-上架方案.md)。

---

## 1. 基本信息（Basic Book Details）

| Field | Value（直接复制） |
|---|---|
| **Language** | English |
| **Book title** | A High-Value Investment Guidebook |
| **Subtitle** | What it costs, what it returns, how strong the evidence is |
| **Series** | 留空 |
| **Edition number** | 留空（首版） |
| **Author** | leo-bone |
| **Contributors** | 留空 |
| **Publisher** | leo-bone (self-published) |
| **Publishing rights** | 勾选「I own the copyright and I hold the necessary publishing rights.」（原创 + CC BY 4.0 授权，合规） |
| **Primary audience** | 留空（成人向） |

---

## 2. Description（简介 · 整段复制）

```
A no-hype, evidence-based investing manual.

Across 24 chapters and 302 entries, every action states three things plainly:

WHAT IT COSTS - fees, taxes, time, effort, and permanent loss of capital.
WHAT IT RETURNS - long-term real returns, lower volatility, tax savings, and avoiding wipeouts.
HOW STRONG THE EVIDENCE IS - A (authoritative statistics, top journals, official documents), B (single studies, institutional reports), C (reasonable inference, regulation).

Every entry cites its original sources. Only peer-reviewed papers and official documents - never self-media or marketing accounts.

It also introduces the "Three-Zero Principle": do first the moves that cost zero money, zero time, and zero willpower.

For ordinary investors who want to pay less tuition and stop being harvested.
```

> KDP 描述支持有限 HTML：可加 `<b>bold</b>`、`<br>`、`<h2>`、`<ul><li>`。上面纯文本可直接用；想更好看可用 `<b>` 包住每行标题。

---

## 3. Keywords & Categories

**Keywords（最多 7 个，建议如下）**

1. index fund investing
2. dollar cost averaging
3. personal finance for beginners
4. asset allocation
5. passive investing
6. long term investing
7. evidence based investing

**Categories（选 2 个）**

- Primary：`Kindle Store › Business & Money › Investing › Personal Finance`
- Secondary：`Kindle Store › Business & Money › Investing › Introduction`

*(纸书版分类同此；若后台为下拉树，按同义项就近选择即可。)*

| Field | Fill |
|---|---|
| **Age range** | 留空 |
| **Pre-order** | No（直接发布） |
| **Publication date** | 留默认 |

---

## 4. 上传资产清单（仓库内已生成）

| 用途 | 文件 | 规格 |
|---|---|---|
| Kindle 电子书正文 | `HowToInvestBetter-en.epub` | 24 章 / 302 条，含封面、版权页、导读、导航目录 |
| 电子书封面 | `cover-book-en.png` | **1600 × 2560** 竖版（KDP 最低 1000×1600） |
| 纸书内文 | `HowToInvestBetter-en-print.pdf` | **6" × 9"**，**366 页**，已含页码／版权页 |
| 纸书完整书封 | `cover-paperback-en.pdf` | 300 DPI，**13.0742" × 9.2500"**，含出血；KDP 首选 PDF |
| （备用）书封位图 | `cover-paperback-en.png` | 3922 × 2775，300 DPI |
| （导流）社交卡 | `en-cover.png` | 1200 × 630，GitHub Pages / 社交分享 |

---

## 5. 定价（Pricing）

| 版本 | 建议价 | 版税 | 说明 |
|---|---|---|---|
| Kindle 电子书 | **$4.99** | 70% | 必须落在 **$2.99–$9.99** 才可选 70% 档；$4.99 到手约 $3.49 |
| 平装纸书 | **$16.99** | 60% | 366 页黑白白纸，KDP 会自动给出最低价（约 $7.5 起），$16.99 到手约 $6–$7 |

- **Territories**：Worldwide rights（全球）
- **KDP Select**：**不勾**（勾了 90 天 Kindle 独家，与 GitHub 免费全文冲突；保持双渠道）
- **Matchbook / 低价匹配**：可选开，促销时纸书自动跟价

> 电子书定价想更低冲量可设 $3.99（仍 70%）；想更贴合英文市场专业手册定位可设 $5.99–$6.99。$4.99 是平衡默认。

---

## 6. 纸书印刷参数（Paperback Content · 必须与书封一致）

| 字段 | 填什么 | 为什么 |
|---|---|---|
| **Manuscript** | `HowToInvestBetter-en-print.pdf` | 6×9 内文 |
| **Cover** | `cover-paperback-en.pdf` | 首选 PDF；含出血、书脊、条码区 |
| **Paper type** | **White** | 书脊 0.8242″ 按白纸算出；换米色须重算 |
| **Ink** | Black & White | 最省，与内文一致 |
| **Trim size** | **6" x 9"** | 与内文 PDF 一致 |
| **Bleed** | **Bleed** | 书封四周 0.125″ 出血，不选会裁错 |
| **ISBN** | Get a free ISBN from Amazon | 省自购 |
| **Barcode** | 不用管 | KDP 自动加在封底右下角（已预留 2″×1.2″ 空白） |

> ⚠️ 白纸 / 6×9 / Bleed 三项必须与书封参数对齐，否则封面套不准。
> 书脊 = 页数 × 0.002252″ = **366 × 0.002252 = 0.8242″**。若内文页数变化，必须重跑：
> ```bash
> python3 tools/build_en_pdf.py --print          # 重出内文（页数可能变）
> python3 tools/gen_cover_en.py                  # 按新页数重算书脊，重出书封
> ```

---

## 7. 上架步骤（English Edition）

```
[ ] 1. 开国际 KDP 账户 + 绑 Payoneer/WorldFirst（7–10 天审核，见操作指南 §1）
[ ] 2. 填 W-8BEN（国籍=China，Non-U.S. person，把预扣从 30% 降到 0–10%）
[ ] 3. + Create → Kindle eBook，照抄 §1/§2/§3 字段
[ ] 4. 传 HowToInvestBetter-en.epub（正文）+ cover-book-en.png（封面）
[ ] 5. Preview book 翻一遍：封面→版权页→Introduction→第 1 章导航正常
[ ] 6. 定价 $4.99 / 70% / Worldwide → Publish（24–72h 上线，记下 ASIN）
[ ] 7. + Create → Paperback，字段同上，传 en-print.pdf + cover-paperback-en.pdf
[ ] 8. 纸张=White / 裁切=6×9 / 出血=Bleed / 免费 ISBN → Publish
[ ] 9. 买一本 Author Copy 实体样书核对印刷
[ ] 10. 描述末尾互链免费全文：github.com/leo-bone/HowToInvestBetter
```

---

## 8. 与中文版的关系（上架顺序建议）

- **英文版是打开 Amazon.com 最大市场的主力**，建议**先上英文版**（受众大、定价空间更大、无中文乱码风险）。
- 中文版随后走同一账户上架（Language=Chinese (Simplified)），字段见 [`KDP-中文版填报表.md`](KDP-中文版填报表.md)。
- 两版共用同一作者名与 GitHub 仓库导流；不要勾 KDP Select，保持 GitHub 免费全文同步引流。

---

## 9. 常见坑（英文版特有）

| 坑 | 后果 | 怎么避 |
|---|---|---|
| 电子书封面比例不对 | 上传被拒 / 显示变形 | 用 `cover-book-en.png`（1600×2560，已是标准竖版） |
| 纸书页数变了没重出书封 | 书脊错位、裁切切字 | 改内文后必跑 `tools/gen_cover_en.py` |
| 纸书纸张选米色 | 0.8242″ 书脊失效 | 选 White；要米色先重算书脊（`--cream`） |
| 定价低于 $2.99 | 只能拿 35% | 维持 $2.99–$9.99 |
| 勾了 KDP Select | 违反独家、与 GitHub 冲突 | 不勾 |
| 描述里放外部购买链接 | 可能被拒 | 只放"免费在线试读"式引导，不放竞品链接 |
