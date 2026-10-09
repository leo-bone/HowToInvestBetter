# KDP 上传操作指南（中文版 · 照着点）

> 配合 `KDP-中文版填报表.md`（字段数值）与 `AMAZON-上架方案.md`（战略与竞品）使用。
> 本指南按 KDP 后台真实流程逐屏拆解，所有"填什么"都来自填报表，可直接复制。
> 目标：把《高性价比投资指南》上架到 Amazon.com（国际站）卖 **Kindle 电子书**（⚠️ 中文纸书 KDP 不支持，见 §3）。
>
> **英文版优先**：英文版（*A High-Value Investment Guidebook*）字段与上传资产见 [`KDP-英文版填报表.md`](KDP-英文版填报表.md)。
> 建议**先上英文版**（受众最大、定价空间更大），再上中文版；下方 §1 的账户／W-8BEN 税务／收款三步**两版通用**。

---

## 0. 动手前必须准备好的 4 样东西

| 序号 | 你要准备的 | 说明 | 我能替你做的 |
|---|---|---|---|
| 1 | 国际 KDP 账户 | 在 kdp.amazon.com 注册（中国 Kindle 商店已关，只能上国际站卖给海外读者） | ❌ 需你的邮箱 + 身份验证 |
| 2 | 收款方式 | 中国银行卡 Amazon 不能直接打款，用 **Payoneer / WorldFirst** 开一个"美国虚拟银行账户"作为收款账户 | ❌ 需你的身份 + 开户 |
| 3 | 税务表 W-8BEN | 非美国作者必须填，否则版税被预扣 30%；填了按中美协定降到 ~0–10% | ❌ 需你的税务信息 |
| 4 | 上传文件 | `HowToInvestBetter.epub` + `cover-book.jpg`（中文电子书，传 KDP）；`HowToInvestBetter-print.pdf` + `cover-paperback.pdf`（中文纸书，**IngramSpark 用**，KDP 用不了） | ✅ 已生成在仓库 |

> ⚠️ 1–3 是平台账户操作，带你的身份与资金，**必须你自己完成**。我只能把第 4 项的文件和上架字段备好。

---

## 1. 开 KDP 账户（约 7–10 天审核，先开不亏）

1. 浏览器打开 **https://kdp.amazon.com** → 点「Sign up」。
2. 用你常用邮箱注册（建议 Gmail / Outlook，别用国内邮箱避免收不到验证信）。
3. 填「Your Account Information」：姓名、地址（填真实，税务要核对）、电话。
4. 进入「**Tax Interview（税务访谈）**」：
   - 选「Individual」→ 国籍/居民选 **China** → 勾选「Non-U.S. person」。
   - 系统生成 **W-8BEN** 电子表，确认姓名/地址/国籍无误，提交。
   - 这一步决定版税预扣率，务必认真填，别跳。
5. 进入「**Getting Paid（收款）**」：
   - 选「Electronic Funds Transfer (EFT)」→ 银行国选 **United States**。
   - 银行名/路由号/账户号填 **Payoneer 或 WorldFirst 给你的美国虚拟账户**（它们会提供 Routing Number + Account Number）。
   - 没有这步，书卖了钱也打不回来——这是中文作者最容易卡住的地方。
6. 提交后等 Amazon 审核（通常 7–10 天，期间能先建书、不能收款）。

---

## 2. 新建 Kindle 电子书（核心：照抄下面字段）

进入 KDP 后台 → 左上角 **「+ Create」→「Kindle eBook」**。

### 2.1 Kindle eBook Details（详情）

| 字段 | 填什么（直接复制） |
|---|---|
| **Language（语言）** | **Chinese (Traditional)** ← 中文在 KDP 语言表里只有这一项（仅电子书）。若下拉另有 Chinese (Simplified)，选它更贴合内容，但**两者都不解锁纸书** |
| **Book title（书名）** | 高性价比投资指南 |
| **Subtitle（副标题）** | 花掉什么，换回什么，证据有多硬（循证投资手册） |
| **Author（作者）** | leo |
| **Contributors（贡献者）** | 留空 |
| **Description（描述）** | ↓ 见下方整段复制 |
| **Publishing rights（出版权）** | 勾选 **「I own the copyright and I hold the necessary publishing rights.」**（原创作品，作者持有版权与出版权） |

**Description 整段（复制下面全部）：**

```
一本不荐股、不卖课的循证投资手册。24 章 302 条，每条都写清：花掉什么（费用／税／时间／精力／本金永久损失）、换回什么（长期真实回报／降波动／税费节省／避开归零）、证据多硬（A 权威统计·顶刊·官方文件｜B 单项研究·机构报告｜C 合理推论·法规）、原始出处（只引期刊论文与官方文件，不引自媒体与营销号）。首创「三零原则」——花费、时间、毅力三项成本全为零的动作闭眼先做。适合想少交学费、不被割韭菜的普通投资者。
```

> 💡 KDP 描述支持有限 HTML：可加 `<b>加粗</b>`、`<br>` 换行、`<h2>小标题</h2>`、`<ul><li>列表</li></ul>`。想排版更好看，可把上面纯文本换成带 `<b>` 的版本（不影响审核）。

### 2.2 Keywords & Categories（关键词与分类）

| 字段 | 填什么 |
|---|---|
| **Keywords（关键词，最多 7 个）** | 指数基金、定投、个人理财、资产配置、小白理财、被动投资、投资入门 |
| **Categories（分类，可选 2 个）** | 主要：Kindle Store › Business & Money › Investing › Personal Finance；备选：Kindle Store › Business & Money › Investing › Stocks |
| **Age range（年龄段）** | 留空（成人向，不选也能过） |
| **Pre-order（预售）** | 选「No」（直接发布） |
| **Publication date（出版日）** | 留默认（今天或稍后） |

### 2.3 Kindle eBook Content（上传正文与封面）

1. **Manuscript（正文）**：上传 `HowToInvestBetter.epub`。（⚠️ 官方对「Chinese (Traditional)」电子书只列 **DOC/DOCX**，EPUB 有被审核打回的风险；**若被打回，告诉我，我立刻生成 DOCX 版本**。）
   - 上传后点 **「Preview book（预览）」** 用在线阅读器翻一遍，重点看：封面→版权页→导读→第 1 章导航是否正常、中文是否乱码。
   - 若乱码：EPUB 已内嵌思源宋体回退，正常不会；万一出问题，先用 **Kindle Previewer**（Amazon 免费工具）本地校验一次再传。
2. **Book cover（封面）**：选 **「Upload a cover image」** → 上传 `cover-book.png`（1600×2560 竖版）。
   - 不要选「Launch Cover Creator」自己画，直接用我们做好的。
3. 纸书暂不选，本步只管电子书。

### 2.4 Kindle eBook Pricing（定价与版税）

| 字段 | 填什么 |
|---|---|
| **Territories（销售区域）** | 选「Worldwide rights（全球）」 |
| **Royalty（版税）** | 选 **70%**（必须价格落在 $2.99–$9.99 才可选） |
| **List price（定价）** | **$3.99**（落在 70% 区间；美国/英国/欧洲/日本等站点可一起设，统一 $3.99 即可） |
| **KDP Select（可选）** | 不勾（勾了要 90 天 Kindle 独家；想进 Kindle Unlimited 再考虑） |

> 70% 版税下，$3.99 你实际到手约 **$2.79/本**（扣约 30% 渠道+增值税）。35% 档到手更少且无需价格限制，所以 $3.99 + 70% 是最优默认。

### 2.5 发布

- 拉到最下点 **「Publish your Kindle eBook」**。
- 状态变 **「In review」** → 通常 24–72 小时变 **「Live」**，之后在 Amazon.com 搜书名即可买到。
- 保存一份 **ASIN**（上线后 KDP 后台生成，形如 B0xxxxxx），后面纸书和推广要用。

---

## 3. 中文纸书：KDP 建不了，改走 IngramSpark

> ⚠️ **这不是设置错误，是平台硬限制。**
> KDP 官方《Book Supported Languages》表中中文只有「**Chinese (Traditional)（eBook only，仅电子书）**」一项；官方《Chinese (Traditional) (Beta)》帮助页明确写「KDP doesn't support: **Paperbacks in Chinese (Traditional or Simplified)**」。
> 所以后台点「Paperback」只会出现一行灰字 `KDP does not support creating paperbacks in Chinese (Traditional)`，**上传槽根本不会出现**。换语言、转繁体都无效。

| 想知道 | 答案 |
|---|---|
| 中文 Kindle 电子书 | ✅ 可以（照 §2 走） |
| 中文平装 / 精装纸书 | ❌ KDP 一律不支持 |
| 那中文纸书去哪做 | **IngramSpark**（POD，支持简体中文实体书） |

### 3.1 IngramSpark 关键参数

- **渠道**：全球 4 万+ 书店 / 图书馆 / 学校 / 线上零售商（Ingram 分销网络），也可经其进入 Amazon 销售。
- **费用**：每本书号约 **$49** 上架费（常有促销码免掉）；无库存、先卖后印。
- **ISBN**：建议**自购全球通用 ISBN**（用平台免费 ISBN 会把出版商登记成平台）。
- **分销设置**：批发折扣 **55%** + 退货政策「可退货」，否则书店不进货。
- **文件**：现有 `HowToInvestBetter-print.pdf`（6×9 / 337 页 / 字体全内嵌）可直接作为内文候选，但**页边距与出血需按其模板复核**；封面必须用其 **cover template 生成器**按 337 页重算（其书脊公式与 KDP 略有差异），不能直接上传 `cover-paperback.pdf`。
- **决策**：中文纸书非刚需 → 中文只出电子书，纸书精力放在**英文版**（English 在 KDP 上 paperback / hardcover 全支持）。


---

## 4. 上线后：导流（零成本流量）

书在 Amazon 卖，可同时维护一个免费的检索页（可被搜索引擎收录）作为入口：

1. 检索页部署在任意静态托管上并启用（可被搜索引擎收录）。
2. README 已有 6 语言版 + 下载入口，海外华人搜"投资指南"有机会被 Google 收进来。
3. 可在自有渠道（邮件 / 社媒）告知读者，把免费读者转成付费买家。
4. 可选：提交 sitemap 到 Google Search Console，加快收录。

---

## 5. 时间线 & 检查清单

```
[ ] 1. 开 KDP 账户 + 绑 Payoneer/WorldFirst（7–10 天审核）
[ ] 2. 填 W-8BEN 税务表
[ ] 3. 新建 Kindle eBook，照抄 §2 字段，传 .epub + cover-book.png
[ ] 4. 预览无误 → 定价 $3.99 / 70% → Publish（24–72h 上线）
[ ] 5. （中文纸书在 KDP 建不了 —— 见 §3；如需纸书改走 IngramSpark）
[ ] 6. 留意 KDP 是否因格式退回中文电子书 EPUB → 若退回改传 DOCX
[ ] 7. 买一本 Author Copy 实体样书核对印刷
[ ] 8. 在自有渠道 / 书描述互链导流
```

**预计总耗时**：账户审核 7–10 天是硬等待；纯上架操作半天能搞定。

---

## 6. 常见坑（提前避开）

| 坑 | 后果 | 怎么避 |
|---|---|---|
| 没开 Payoneer/WorldFirst 美国账户 | 版税打不回来 | 第 1 步就开，别等到卖出去才补 |
| W-8BEN 没填/填错 | 预扣 30% 税 | 认真填国籍=China、Non-U.S. person |
| 纸书纸张选了米色 | 书脊 0.7589″ 失效、封面套不准 | 选白纸；要换米色先重算书脊 |
| 纸书出血选 None | 封面四周被裁掉 | 选 Bleed |
| EPUB 中文乱码 | 审核退回 / 读者差评 | 上传前用 Kindle Previewer 校验 |
| **中文电子书传 EPUB 被打回（要求 DOC/DOCX）** | 审核不过，需重传 | KDP 官方对 Chinese (Traditional) 电子书只列 DOC/DOCX；被打回就改传 Word 版 |
| **后台点 Paperback 只有一行灰字「KDP does not support creating paperbacks in Chinese (Traditional)」** | 中文纸书**根本建不了**，与环境/设置无关 | KDP 官方不支持任何中文纸书（繁简皆不支持）。改走 IngramSpark，见 §3 |
| **纸书报「Fonts are missing…」** | 印前检查直接拒收，无法发布 | 内文 PDF 的字体必须**全部内嵌**。构建脚本已改用 Songti SC（TrueType，子集内嵌）；旧版 STSong-Light 是 Adobe CID 字体、只引用不嵌入，必被拒。重跑 `python3 tools/build_pdf.py --print` 即可 |
| 定价低于 $2.99 | 只能选 35% 版税 | 维持 $2.99–$9.99 拿 70% |
| 勾了 KDP Select | 90 天 Kindle 独家限制 | 按需评估 |

---

## 7. 以后正文改了怎么办（联动提醒）

书脊宽度 = 页数 × 纸张厚度。只要出现以下任一变动，**必须重跑书封生成**否则封面错位：

```bash
# 正文改完 → 重建产物
python3 tools/build.py            # 检索页数据
python3 tools/build_pdf.py --print   # 印刷版 PDF（页数可能变）
python3 tools/gen_cover_paperback.py # 按新页数重算书脊，重出 cover-paperback.pdf
python3 tools/build_epub.py          # 电子书
```

重算后：**英文纸书**把新的 PDF 重传到 KDP（后台「…」→「Edit paperback content」→ 替换文件，不用重建书记录）；**中文纸书**则传到 IngramSpark（KDP 用不上中文纸书）。
