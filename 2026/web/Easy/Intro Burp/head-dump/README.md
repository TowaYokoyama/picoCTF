# Head Dump

## Category
Web Exploitation

---

## 📝 Problem Overview

提供されたブログサイトを調査し、隠された flag を取得する問題。

記事内に「API Documentation」に関する記述があり、
開発用 API が公開されている可能性が示唆されている。

目的は、サーバのメモリダンプから flag を取得すること。

---

## 🔍 Initial Analysis

トップページは通常のブログサイトに見える。

記事の中に以下のようなヒントがある：

> API Documentation is available for developers.

これは開発用の Swagger UI が公開されたままになっている可能性を示している。

---

## そもそもhead-dumpとは？

サーバーのメモリ（heap）をそのままファイルに吐き出す機能。

JavaやNode.jsなどのアプリケーションで、バグ調査やパフォーマンス確認のために使われる。

このダンプには、実行中の変数や認証情報など、機密データが含まれていることが多い。

---
## ダンプする機能とは？
開発や運用のために、サーバーの現在の状態を一括で保存する機能。

正常なら認証付き・ローカル限定・開発環境のみで使う。
---

## 🔎 Step 1: API Documentation を探す

一般的な Swagger(APIの仕様書ツール) の公開パスは：

/api-docs

そのため、ブラウザで直接アクセスする：

http://<instance-url>/api-docs

Swagger UI が表示されることを確認。

---

## 🔎 Step 2: メモリダンプ用エンドポイントを特定

Swagger 内に以下のようなエンドポイントが存在する：

GET /api/heapdump

（名称は memory / snapshot / dump などの可能性あり）

これはサーバのメモリダンプを生成・取得するAPIである。

---

## 🔎 Step 3: ダンプを取得
tru it outがなぜかできなかったが、できた場合
```
content-disposition: attachment; filename="heapdump-xxx.heapsnapshot"
content-type: application/octet-stream
```

# ヘッダー名	意味
content-disposition: attachment	ブラウザに「これはファイルとして扱ってね」と指示
content-type: application/octet-stream	中身はバイナリ形式、つまり一般的なファイル

Swagger UI が操作できない場合は、直接URLを叩く：

http://<instance-url>/api/heapdump

レスポンスとしてメモリダンプファイルが取得できる。

---

## 🔎 Step 4: flag を検索

取得したファイルから picoCTF{} を検索する。

例（バイナリの場合）：

    strings dump.bin | grep picoCTF

テキスト形式の場合：

    grep picoCTF dump.txt

flag が発見できる。

---

## 🏁 Flag

picoCTF{...}

---

## 🧠 What We Learned

- 本番環境で Swagger を公開したままにすると危険
- デバッグ用APIの削除忘れは重大な情報漏洩につながる
- メモリダンプには機密情報が含まれる可能性がある

---

## 🔐 Root Cause

開発者が Swagger UI とメモリダンプ生成APIを
本番環境で無効化していなかったことによる情報漏洩。

---

## 🧩 Key Concept

- Swagger Exposure
- Information Disclosure
- Debug Endpoint Leakage
