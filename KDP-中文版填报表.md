# KDP 中文版上架填报表（可直接复制粘贴）

> 配合 `AMAZON-上架方案.md` 使用。本表把中文版上架 KDP 要填的字段都备好，复制即可。

## 基本信息

- **书名**：高性价比投资指南
- **副标题**：花掉什么，换回什么，证据有多硬（循证投资手册）
- **作者**：leo
- **语言**：**Chinese (Traditional)** ← KDP 语言下拉里中文只有这一项（官方支持语言表中为「Chinese (Traditional)（仅电子书）」）。简体中文根本不在 KDP 支持列表内。**该字段只影响电子书；中文纸书 KDP 一律不做，见下方 ⚠️。**
- **出版商**：leo（自出版）
- **书籍类型**：非虚构 · 商业与理财

---

## ⚠️ 平台硬限制：中文纸书在 KDP 上做不了（2026-10-09 实测确认）

KDP 官方《Book Supported Languages》表中，中文只有一条：**Chinese (Traditional)（eBook only，仅电子书）**；官方《Chinese (Traditional) (Beta)》帮助页明确列出「KDP doesn't support: **Paperbacks in Chinese (Traditional or Simplified)**」。

因此：**KDP 不能出任何中文纸书（简体、繁体都不行）**。在后台点「Paperback / 平装书」只会看到一行灰字 `KDP does not support creating paperbacks in Chinese (Traditional)`，纸书的上传槽根本不会出现。换语言选项、把内容转成繁体，**都无法解锁**。

| 产品线 | 中文版在 KDP 的可行性 |
|---|---|
| Kindle 电子书 | ✅ 可以做（本表下方照用） |
| 平装纸书 Paperback | ❌ 平台不支持 |
| 精装 Hardcover | ❌ 平台不支持 |
| 中文纸书替代平台 | **IngramSpark**（支持简体中文实体书，见文末） |

---


## 书籍简介（KDP 描述，约 180 字）

一本不荐股、不卖课的循证投资手册。24 章 302 条，每条都写清：花掉什么（费用／税／时间／精力／本金永久损失）、换回什么（长期真实回报／降波动／税费节省／避开归零）、证据多硬（A 权威统计·顶刊·官方文件｜B 单项研究·机构报告｜C 合理推论·法规）、原始出处（只引期刊论文与官方文件，不引自媒体与营销号）。首创「三零原则」——花费、时间、毅力三项成本全为零的动作闭眼先做。适合想少交学费、不被割韭菜的普通投资者。

## 关键词（7 个，用于 KDP 搜索）

指数基金、定投、个人理财、资产配置、小白理财、被动投资、投资入门

## 分类（KDP 两阶分类）

- 主要：Kindle 商店 › 商业与理财 › 投资 › 个人理财
- 备选：Kindle 商店 › 商业与理财 › 投资 › 证券（股票）

## 定价建议

- **电子书**：$3.99（落在 70% 版税区间 $2.99–$9.99）
- **纸书（6×9）**：**KDP 不适用**（中文纸书 KDP 不支持，见上方 ⚠️）。337 页黑白白纸按 KDP 美站口径的印刷成本 = $1.00 + 337 × $0.012 = **$5.04**，此数字仅作成本参照；若走 IngramSpark，其定价体系不同（标价 × 批发折扣 − 印刷成本），需单独重算。

## 上传资产清单（仓库内已生成）

| 资产 | 用途 |
|---|---|
| `HowToInvestBetter.epub`（含封面 + 版权页 + 导读 + 导航目录） | 中文 **Kindle 电子书** 正文 → 传 KDP |
| `cover-book.jpg`（1600×2560，桌面版为 JPG） | 电子书封面 → 传 KDP（KDP 只收 JPG/TIFF，**别选同名 .png**） |
| `HowToInvestBetter-print.pdf`（6×9，337 页，字体全部内嵌） | 中文纸书内文 → **KDP 用不了**，留给 IngramSpark |
| `cover-paperback.pdf` / `.png`（300 DPI，含四边 0.125″ 出血） | 中文纸书全封面 → **KDP 用不了**，留给 IngramSpark（其封面模板不同，需换算） |

> ⚠️ **中文电子书格式风险**：KDP 官方对「Chinese (Traditional)」电子书要求用 **Microsoft Word（DOC/DOCX）**，并注明「We don't support other file types for Chinese (Traditional)」。上传 EPUB 若被审核打回，需改传 DOCX 版本。

## 纸书书封参数（KDP 中文纸书不适用；以下参数供 IngramSpark 换算时参考）

下单用 **白纸（White，黑白印刷）**，与下面参数一致；若改用米色纸须重算书脊。

- 开本 6×9 英寸 · 页数 337 · **书脊 0.7589″**（= 337 × 0.002252″）
- 全封面尺寸 **13.0089″ × 9.2500″**（300 DPI，含四边 0.125″ 出血）
- 版式符合 KDP 规范：**封底（左）｜书脊（中）｜封面（右）**
- **条码区**已按 KDP 要求在**封底右下角**预留 2″×1.2″ 空白（条码由 KDP 自动添加）
- 边框 / 文字均在裁切线内 0.3″ 安全区，避免裁切与折页偏移时被切
- 重新生成：`python3 tools/gen_cover_paperback.py`（换纸张加 `--cream`，换页数加 `--pages N`）

## 上架步骤（中文版）

1. 注册**国际 KDP 账户（美站）** amazon.com/kdp：绑定 Payoneer / WorldFirst 境外银行卡，填 **W-8BEN**（避免 30% 预扣税），绑国际信用卡。审核约 7–10 天。
2. 新建「**Kindle 电子书**」：填上方书名／作者／描述／关键词／分类，上传 `HowToInvestBetter.epub` + `cover-book.jpg`（KDP 封面只收 JPG/TIFF），预览无误后发布（约 48 小时上线 Amazon.com）。
3. ~~新建「平装书（Paperback）」~~ **KDP 建不了中文纸书**（点 Paperback 只会显示 `KDP does not support creating paperbacks in Chinese (Traditional)`）。中文纸书改走 **IngramSpark**，见文末「中文纸书替代方案」。
4. 定价 $3.99，确认处于 70% 版税区间。
5. 上线后通过自有渠道（邮件列表 / 社媒）告知读者并收集评价。

---

## 中文纸书替代方案（IngramSpark）

IngramSpark 是全球最大图书批发商 Ingram 的自出版 POD 平台，**支持简体中文实体书与电子书**：

- **渠道**：可触达全球 4 万+ 书店 / 图书馆 / 学校 / 线上零售商（Ingram 分销网络），也能经其分销进入 Amazon 销售；KDP 的纸书只在 Amazon 各站。
- **成本**：每本书号（title）约 $49 上架费（常有促销码可免）；无库存、先卖后印。
- **ISBN**：建议**自购全球通用 ISBN**，让出版商登记为你自己（用免费 ISBN 会把出版商登记成平台）。
- **分销设置**：批发折扣设 **55%**（行业标准）+ 退货政策设「可退货」，否则书店不会进货。
- **注意**：IngramSpark 的内文页边距/出血与封面模板规格**与 KDP 不同**，现有 `HowToInvestBetter-print.pdf` + `cover-paperback.pdf` 需按其模板复核/重做后才能上传。
- **决策建议**：若中文纸书非刚需 → 中文只出电子书，把纸书精力放在**英文版**（English 在 KDP 上 paperback / hardcover 全支持，路是通的）。
