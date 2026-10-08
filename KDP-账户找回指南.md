# KDP 账户找回指南（密码 + 手机号都忘了）

> 你之前在 KDP 自己出过一本书，现在密码和当时绑的手机号都忘了。
> 好消息：**KDP 登录用的是亚马逊账户，而账户的"主钥匙"是邮箱，不是手机号**。手机号只用于两步验证（2FA）。只要还记得邮箱，就有路走。

---

## 0. 先判断：你还记得什么

| 你还记得 | 难度 | 走哪条路 |
|---|---|---|
| ✅ 注册邮箱 | 低 | 路径一 + 路径二（大概率自己搞定） |
| ❌ 密码 | — | 路径一重置 |
| ❌ 手机号 | 中 | 路径二绕开 2FA，或路径三找支持 |
| ✅ 旧书书名 / ASIN / ISBN | 关键 | 用作身份证据（路径三） |
| ✅ 收款银行账户 / 税表信息 | 关键 | 用作身份证据（路径三） |

> 最理想你至少记得**邮箱**和**旧书信息**。邮箱能重置密码；旧书信息能在 2FA 卡死时向支持证明"这账户确实是我的"。

---

## 路径一：重置密码（走邮箱，自己搞定）

1. 打开 KDP 登录页 **https://kdp.amazon.com** → 点 **「Forgot your password?」（忘记密码）**。
2. 输入**注册邮箱**（不是手机号）→ 亚马逊会给该邮箱发**验证码 / 重置链接**。
3. 收邮件 → 点链接设新密码。
4. 用新密码登录。下一步就会进入**两步验证（2FA）**——这里才是手机号忘掉的麻烦点，看路径二。

> 如果"忘记密码"页面只让你输手机号、且邮箱也想不起来：直接跳到**路径三**找支持，凭旧书信息和身份证件找回。

---

## 路径二：2FA / 手机号卡住了怎么办

登录输完新密码后，亚马逊要求输入短信验证码（发到那个忘了的手机号）。你收不到。这时看屏幕上有没有这些选项：

- **「Didn't receive a code? / 没收到验证码？」** → 点开后可能提供：
  - 改用**邮箱收验证码**（如果当时绑了邮箱验证）；
  - 改用**身份验证器 App**（如果你之前绑过 Google Authenticator / Microsoft Authenticator，用那个 App 里的 6 位码）；
  - **「Use a backup code / 使用备用码」**（注册 2FA 时亚马逊给过一组一次性备用码，找找当时存没存）；
- **「I don't have access to this phone number / 我无法使用这个手机号」** → 点它，系统会引导你走**身份验证**或转**人工支持**（路径三）。

> 三选一能进就能改：进账户后立刻去 **「Login & Security」→ 改手机号、重新绑认证器、生成新的备用码**，把 2FA 换成"认证器 App + 备用码"，别再只靠短信。

---

## 路径三：都卡死 → 联系 KDP / 亚马逊支持（带身份证据）

如果邮箱也收不到、手机号也换不了、备用码也没有，只能走人工身份核验。KDP 对"证明你是你"很较真，但你有**天然王牌：你就是那本书的作者**。

### 3.1 怎么联系

- 能进登录页但被 2FA 挡：在 2FA 页面点 **「Need help? / 需要帮助」→「Contact us」**，走"无法登录"流程。
- 完全进不去：用亚马逊通用账户恢复页 **https://www.amazon.com/ap/forgotpassword** 底部的 **「Need more help? Contact us」**；或直接搜 **"Amazon account recovery"** 走身份验证（有时需上传证件 + 自拍/视频核验）。
- KDP 支持中心：**https://kdp.amazon.com/en_US/contact-us**（登录后可用；登录不了就走上面通用通道，话术一致）。

### 3.2 向支持证明"账户是我的"——准备这些证据（越多越好）

| 证据 | 说明 |
|---|---|
| **旧书书名 + ASIN + ISBN** | 最强证据。ASIN 在 Amazon 商品页链接里（B0xxxxxx）；ISBN 在书版权页。告诉支持"我在贵平台出版过《XXX》，ASIN 是 XXX"。 |
| **收款银行账户** | 当时绑的 Payoneer/WorldFirst 或银行卡的尾号/开户名。支持能核对"版税该打去哪"。 |
| **税务信息** | 当时填的 W-8BEN / W-9 上的姓名、国籍、税号（如有）。 |
| **历史版税** | 大致记得哪年卖过、大约金额，也能佐证。 |
| **政府证件** | 护照 / 身份证（支持核验身份用，按页面要求上传）。 |

### 3.3 支持邮件 / 工单模板（中英对照，填空即可发）

**中文版（发 KDP 支持 / 账户恢复）：**

```
主题：无法登录 KDP 账户——忘记密码且原绑定手机号已停用，请求身份验证找回

您好，

我是 KDP 账户持有人，此前曾在贵平台自助出版过一本书。现因以下原因无法登录：
1. 密码已遗忘；
2. 当时绑定的手机号码已停用，无法接收两步验证短信。

我仍能接收注册邮箱的邮件（邮箱：__________）。

为证明我是该账户所有者，提供以下信息：
- 已出版书名：__________
- 该书 ASIN：__________
- 该书 ISBN：__________
- 当时绑定的收款账户开户名/尾号：__________
- 当时税务表（W-8BEN）填写的姓名/国籍：__________

恳请协助通过身份验证重置密码，并指导我更新两步验证方式（改为认证器 App + 备用码）。
谢谢。
```

**English version (for KDP Support):**

```
Subject: Cannot sign in to KDP — forgot password and old 2FA phone number discontinued

Hello,

I am the holder of a KDP account and have self-published a book on your platform before.
I cannot sign in because:
1. I forgot the password;
2. The phone number originally bound for two-step verification is no longer active, so I cannot receive the SMS code.

I can still receive email at the registered address: __________.

To prove ownership of the account, I provide:
- Published book title: __________
- Book ASIN: __________
- Book ISBN: __________
- Payout account holder name / last 4 digits: __________
- Name / nationality on the W-8BEN tax form: __________

Please help me verify my identity and reset the password, and advise how to update the 2FA method (switch to authenticator app + backup codes).
Thank you.
```

---

## 战略建议：找回旧账户，不要开新账户

- **找回旧账户**：保留你那本旧书的销售记录、评论、待结算版税；新书的《高性价比投资指南》也能直接加进同一个账户，管理方便。
- **开新账户是下策**：亚马逊 KDP 原则上**一个人/一个实体一个账户**。旧账户没关闭就开新的，可能触发关联风控、两头受限。只有在"旧账户彻底找不回、且支持明确建议新建"时才走新账户（用另一个邮箱）。
- 所以：**先穷尽路径一二三把旧账户找回来**。

---

## 找回后立即做 4 件防再丢

1. **改强密码** + 写进密码管理器（别再用记不住的）。
2. **两步验证改"认证器 App + 备用码"**，别只靠短信；把备用码打印/存云端。
3. **更新手机号**为现在在用的；绑一个**备用邮箱**。
4. 记录下旧书的 **ASIN / ISBN**，存一份到本地（下次找回就用得上）。

---

## 好消息：账户回来后，上传新书只要半天

《高性价比投资指南》的所有上架资产（EPUB、印刷 PDF、电子书封面、纸书全封面、填报表、逐屏上传指南）**已经全部就绪并推送**。账户一恢复，照着 `KDP-上传操作指南.md` 点一遍就能上架，不用再等任何东西。
