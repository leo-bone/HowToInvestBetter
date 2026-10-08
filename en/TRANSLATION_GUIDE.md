# 英文版翻译规范与术语锁 / English Translation Guide & Term Lock

本文件是《高性价比投资指南》英文版（`en/book/*.md`）的唯一权威规范。所有翻译（人工或子代理）必须严格遵循，以保证：① 六字段结构可被构建脚本解析；② 全书的术语、证据等级、标签、交叉引用格式一致；③ 数字、URL、法条、年份零失真。

---

## 0. 文件命名与章节标题

文件名格式：`NN-Slug.md`（编号用两位数字，slug 用英文短横线）。章节内一级标题用 `# I. English Title`（罗马数字 + 点 + 空格）。

| 编号 | 中文标题 | 文件名 slug | 英文标题（章节内 `#` 用罗马数字） |
|---|---|---|---|
| 01 | 不要亏在认知外 | 01-Dont-Lose-Outside-Your-Circle | I. Don't Lose Outside Your Circle of Competence |
| 02 | 费用税收 | 02-Fees-and-Taxes | II. Fees and Taxes |
| 03 | 行为偏差 | 03-Behavioral-Biases | III. Behavioral Biases |
| 04 | 被动省心 | 04-Passive-and-Hands-Off | IV. Passive and Hands-Off |
| 05 | 资产速查 | 05-Asset-Quick-Reference | V. Asset Quick Reference |
| 06 | 骗局红线 | 06-Scams-and-Red-Lines | VI. Scams and Red Lines |
| 07 | 划算动作 | 07-Cost-Effective-Moves | VII. Cost-Effective Moves |
| 08 | 税务账户 | 08-Tax-Advantaged-Accounts | VIII. Tax-Advantaged Accounts |
| 09 | 人生阶段 | 09-Life-Stages | IX. Life Stages |
| 10 | 反面清单 | 10-The-Dont-Do-List | X. The Don't-Do List（纯清单章节，无 `###` 条目，全为 bullet） |
| 11 | A股实操 | 11-A-Share-Practical-Playbook | XI. A-Share Practical Playbook |
| 12 | 冷计算器 | 12-The-Cold-Calculator | XII. The Cold Calculator |
| 13 | 养老退休 | 13-Retirement | XIII. Retirement |
| 14 | 保险配置 | 14-Insurance | XIV. Insurance |
| 15 | 房产负债 | 15-Housing-and-Debt | XV. Housing and Debt |
| 16 | 信息防忽悠 | 16-Spotting-Misinformation | XVI. Spotting Misinformation |
| 17 | 宏观周期 | 17-Macro-Cycles | XVII. Macro Cycles |
| 18 | 人力资本 | 18-Human-Capital | XVIII. Human Capital |
| 19 | 消费记账 | 19-Spending-and-Budgeting | XIX. Spending and Budgeting |
| 20 | 极端情形 | 20-Extreme-Scenarios | XX. Extreme Scenarios |
| 21 | 基金选择实操 | 21-Fund-Selection-in-Practice | XXI. Fund Selection in Practice |
| 22 | 固定收益细节 | 22-Fixed-Income-Details | XXII. Fixed Income Details |
| 23 | 全球与ETF配置 | 23-Global-and-ETF-Allocation | XXIII. Global and ETF Allocation |
| 24 | 衍生品杠杆风险 | 24-Derivatives-and-Leverage-Risks | XXIV. Derivatives and Leverage Risks |

---

## 1. 六字段英文映射（**必须严格使用以下英文标签名**，构建脚本靠它们解析）

| 中文 | 英文（字段标题，写在条目内） |
|---|---|
| 成本 | **Cost** |
| 说人话 | **In plain terms** |
| 收益 | **Payoff** |
| 证据等级 | **Evidence grade** |
| 来源 | **Sources** |
| 备注 | **Note** |

条目内字段行的写法（冒号后空格）：
```
- Cost: ...
- In plain terms: ...
- Payoff: ...
- Evidence grade: A
- Sources: ...
- Note: ...
```
顺序与中文版一致：Cost → In plain terms → Payoff → Evidence grade → Sources → Note。

---

## 2. 标签注释英文映射（**必须严格使用**）

中文原格式：`<!-- 标签: 钱=0 时间=少 毅力=否 收益=中 口径=金钱 影响=自己 -->`
英文格式：`<!-- tags: money=0 time=little will=no payoff=mid scope=money impact=self -->`

键名（6 个，顺序固定）：`money time will payoff scope impact`

| 维度 | 中文值 | 英文值 |
|---|---|---|
| 钱（money） | 0 / 少 / 中 / 多 | `0` / `little` / `mid` / `high` |
| 时间（time） | 0 / 少 / 些 | `0` / `little` / `some` |
| 毅力（will） | 否 / 些 / 多 | `no` / `some` / `much` |
| 收益（payoff） | 低 / 中 / 高 | `low` / `mid` / `high` |
| 口径（scope） | 金钱 / 时间 / 健康 / 关系 / 精力 | `money` / `time` / `health` / `relationship` / `energy` |
| 影响（impact） | 自己 / 家庭 / 自己／家庭 | `self` / `family` / `self+family` |

注意：`影响=自己／家庭` 翻译为 `impact=self+family`（用 `+` 连接，不用斜杠）。

---

## 3. 证据等级（Evidence grade）取值

仅允许 `A`、`B`、`C` 三个大写字母，与中文完全一致。**不得改写、不得翻译**（保持 A/B/C）。
- A = 权威长期统计、顶刊随机／追踪研究、官方监管文件
- B = 单项高质量研究、权威机构回测、经典论文
- C = 合理推论／广泛共识，逻辑硬但不勉强挂精确出处

---

## 4. 交叉引用英文格式

| 中文 | 英文（构建脚本识别此格式） |
|---|---|
| 见第 X 条 | **see Entry X** |
| 第 X 章第 Y 条 | **Chapter X, Entry Y** |
| 交叉参考：第 X、Y 条 | **Cross-reference: Entries X, Y** |
| 交叉参考：第 X、Y、Z 条 | **Cross-reference: Entries X, Y, Z** |

规则：
- 同章引用用 `Entry X`（不写章号）；跨章用 `Chapter X, Entry Y`。
- 多条用 `Entries X, Y, Z`（逗号+空格分隔）。
- 例句：
  - 中文：「交叉参考：第 5 条（非标）、第 9 条（可解释测试）」
  - 英文：`Cross-reference: Entry 5 (non-standard assets), Entry 9 (explainability test).`

---

## 5. 核心术语表（翻译时锁定，保持全书一致）

| 中文 | English | 备注 |
|---|---|---|
| 三零原则 | Three-Zero Principle | 花钱=0、花时间=0、需毅力=否 |
| 性价比 | cost-performance / value for money | 上下文取义 |
| 费率侵蚀 / 费用拖累 | fee drag | |
| 总成本拥有 / 总持有成本 | total cost of ownership | |
| 宽基指数 | broad-market index | |
| 指数基金 | index fund | |
| ETF | ETF (exchange-traded fund) | 首次出现写全称，后文用 ETF |
| QDII | QDII (Qualified Domestic Institutional Investor) | |
| 港股通 | Stock Connect | |
| REITs | REITs (Real Estate Investment Trusts) | |
| 可转债 | convertible bond | |
| 货币基金 | money market fund | |
| 国债逆回购 | reverse repurchase agreement / reverse repo | |
| 久期 | duration | |
| 信用利差 | credit spread | |
| 实际利率 | real interest rate | |
| 印花税 | stamp duty | |
| 资本利得税 | capital gains tax | |
| 个人所得税 | individual income tax | |
| 税收递延 | tax deferral | |
| 个人养老金 | private pension account | 中国 2022 推出的税优账户 |
| 处置效应 | disposition effect | |
| 过度自信 | overconfidence | |
| 损失厌恶 | loss aversion | |
| 锚定效应 | anchoring | |
| 羊群效应 | herding | |
| 确认偏误 | confirmation bias | |
| 心理账户 | mental accounting | |
| 涨跌停 | price limit | 主板 ±10%，创业板/科创板 ±20% |
| T+1 | T+1 settlement | |
| 注册制 | registration-based IPO system | |
| ST / *ST | special treatment (ST / *ST) | |
| 退市 | delisting | |
| 两融 | margin trading and securities lending | |
| 打新 | IPO subscription | |
| 期权时间价值 | option time value (theta) | |
| 隐含波动率 | implied volatility | |
| 强平 / 强制平仓 | forced liquidation / margin call | |
| 杠杆 ETF | leveraged ETF | |
| 波动率损耗 | volatility decay | |
| 雪球结构 | snowball structured product | |
| 卖出看跌期权 | selling a put | |
| 分散 | diversification | |
| 被动投资 | passive investing | |
| 主动基金 | actively managed fund | |
| 跟踪误差 | tracking error | |
| 换手率 | turnover rate | |
| 适当性 | suitability / appropriateness | 监管语境用 suitability |
| 内幕交易 | insider trading | |
| 13F | Form 13F | 美国机构持仓披露 |
| 回测 | backtest | |
| 再平衡 | rebalancing | |

机构与法规名（保留官方英文，首次出现给全称）：
- 中国证监会 → China Securities Regulatory Commission (CSRC)
- 美国 SEC → U.S. Securities and Exchange Commission (SEC)
- 美国 FINRA → U.S. Financial Industry Regulatory Authority (FINRA)
- 上海证券交易所 → Shanghai Stock Exchange (SSE)
- 中国证券业协会 → Securities Association of China (SAC)
- NYSE / Nasdaq / S&P 500 / Dow Jones
- 标普 500 → S&P 500
- 沪深 300 → CSI 300
- 科创板 → STAR Market
- 创业板 → ChiNext
- 《证券法》 → Securities Law of the People's Republic of China
- 《刑法》 → Criminal Law of the People's Republic of China
- 《证券期货投资者适当性管理办法》 → Measures for the Administration of Investor Suitability for Securities and Futures

---

## 6. 翻译铁律（任何情况不得违反）

1. **数字零失真**：所有百分比、年份、金额、回测数字（如 20.53%、2016–2019、2457 元、8.7% vs 9.7%）原样保留，不得改写或"本地化"为美元。涉及人民币金额保留「yuan / RMB」单位。
2. **URL 零改动**：所有 `<https://...>` 链接原样保留，不得翻译、不得省略、不得替换。
3. **法条/文件真实名保留**：法规、论文、报告的官方英文名称照写；无英文官方名的用准确学术译名（如 Journal of Finance、Journal of Financial and Quantitative Analysis）。
4. **六字段顺序与标签名固定**：Cost / In plain terms / Payoff / Evidence grade / Sources / Note，字段名不得自创。
5. **标签注释完整**：每条目顶部必须有 `<!-- tags: ... -->`，六个键齐全（缺的写空值如 `money=` 不可，必须给值；确实无对应填 `0`/`no`/`mid`/`money`/`self` 等最贴近值，保持六键齐全）。
6. **语气一致**：保持中文版"直白、不粉饰、说人话"的语气；英文用第二人称 you、祈使句、短句，避免学术腔。术语首次出现可加括号释义。
7. **证据等级只写 A/B/C**。
8. **交叉引用按第 4 节格式改写**（不要保留中文"第 X 条"或"第 X 章第 Y 条"写法，也不要写成"see Rule X"之类变体——必须用 Entry / Chapter X, Entry Y / Cross-reference: Entries X, Y）。
9. **章节导语中的条号引用**也按第 4 节英文格式（如 `(Entry 1)`、`(Chapter 2, Entry 5)`）。
10. **不要增删条目**：条目数量与中文逐条对应，标题（`### N.`）编号不变。第 10 章是纯 bullet 清单，无 `###` 条目，所有内容保持为 `-` bullet。
11. **保留 Markdown 结构**：加粗 `**x**`、链接 `<url>`、列表 `-` 与中文版一一对应。
12. **书名/项目名**：《高性价比投资指南》→ *HowToInvestBetter: A High Cost-Performance Guide to Investing*；《高性价比人生指南》→ *HowToLiveBetter*（作为致敬来源，保留原名并注明 CC BY 4.0 改编）。

---

## 7. 给翻译者的工作流

1. 读本章中文原文 `book/NN-*.md`。
2. 对照本规范与第 1 章样例 `en/book/01-Dont-Lose-Outside-Your-Circle.md`。
3. 逐条翻译，严格套用六字段 + 标签注释 + 交叉引用英文格式。
4. 写完通读一遍，确认：数字/URL/法条无误、六字段齐全、标签六键齐全、交叉引用格式正确。
5. 输出到 `en/book/NN-Slug.md`，文件名按第 0 节 slug。
