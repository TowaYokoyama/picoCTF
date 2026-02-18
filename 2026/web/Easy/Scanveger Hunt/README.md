# picoCTF – Scan / Discover / Hunt 系 Writeup

## Category
Web Exploitation / General Skills

---

## 📝 Problem Overview

Webサイトを調査し、隠された情報やフラグを発見する問題。

特別なエクスプロイトは不要で、  
「どこを見ればいいか」に気づけるかがポイント。

---

## 🔎 Step 1 – ページのソースを確認

まずは基本。

- 右クリック → ページのソースを表示
- `Ctrl + U`（Macなら `Cmd + Option + U`）

HTMLコメントや隠しヒントを探す。

確認ポイント：

- `<!-- comment -->`
- 隠しリンク
- 不自然なパス

---

## 🔎 Step 2 – robots.txt を確認

こちらを参照
https://devo.jp/seolaboratory/40191/

ブラウザで：

```
/robots.txt
```

にアクセス。

ここに：

- disallow されているパス
- 隠されたディレクトリ

が書かれていることがある。

---

apacheサーバーより(php)
http://mercury.picoctf.net:27393/.htaccess 


# Part 4: 3s_2_lO0k \# I love making websites on my Mac, I can Store a lot of information there.

今度のヒントはweb制作にマックを使っているというヒント。Storeが大文字なので関わりありそう。macはファイル作成時に.DS_Storeという隠しファイルを自動生成する。

----
Done!
謎解き系？知らないことが多く勉強になった