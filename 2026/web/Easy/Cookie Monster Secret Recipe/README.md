# picoCTF 2025 – Cookie Monster Secret Recipe

## Category
Web Exploitation

---

## 📝 Problem Overview

ログインフォーム付きの Web ポータルが与えられる。

- ユーザー名：不明
- パスワード：不明
- 通常ログインは失敗する

しかし、開発者が何かを隠している可能性がある。

目的は **flag を取得すること**。

---

## 🔍 Initial Analysis

ページにアクセスするとログインフォームが表示される。

ログイン情報は分からないため、適当に入力してログインを試みる。

例：

```
username: aaa  
password: aaa
```

ログイン自体は成功しないが、ページは動作する。

ここで重要なのは：

> ログイン突破ではなく、クライアント側の情報を調査すること。

Web問題ではまず **開発者ツールを確認する** のが基本である。

---

## 🛠 Investigation

### 1. 開発者ツールを開く

Mac:

```
⌘ + Option + I
```

Console タブを開く。

---

### 2. Cookie を確認

Console で以下を実行：

```javascript
document.cookie
```

出力：

```
secret_recipe=cGljb0NURntjMDBrMWVfbTBuc3Rlcl9sMHZlc19jMDBraWVzX0M0MzBBRTIwfQ%3D%3D
```

`secret_recipe` という Cookie が存在している。

値は Base64 エンコードされているように見える。

---

### 3. Base64 をデコード

以下を実行：

```javascript
atob(document.cookie.split("=")[1].split("%")[0])
```

出力：

```
picoCTF{c00k1e_m0nster_l0ves_c00kies_C430AE20}
```

---

## 🚩 Flag

```
picoCTF{c00k1e_m0nster_l0ves_c00kies_C430AE20}
```

---

## 📚 Key Learning Points

- Web問題ではまず開発者ツールを確認する
- `document.cookie` で Cookie を確認できる
- Base64 は `atob()` でデコード可能
- ログインフォームがあっても、突破が目的とは限らない

---

## 🧠 Concept

この問題は：

> クライアント側に flag を保存してしまっている典型的なミス

Cookie はユーザー側から閲覧可能であるため、
機密情報を保存するべきではない。

---

## 🏁 Conclusion

ログインを突破するのではなく、
ブラウザの Cookie を確認し、Base64 をデコードすることで flag を取得できた。

Web問題ではまず：

- ソースコード確認
- Cookie確認
- Networkタブ確認

が基本戦略となる。





