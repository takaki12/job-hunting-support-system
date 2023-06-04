# job-hunting-support-system
企業データを用いた就活支援システムの構築

## フォルダ構造
<pre>
.  
├── instance  
├── src  
│   ├── static  
│   │   ├── css  
│   │   └── js  
│   │       └── function.js  
│   ├── templates  
│   │   ├── admin_update.html  
│   │   ├── admin.html  
│   │   ├── main.html  
│   │   ├── mypage.html  
│   │   ├── signin.html  
│   │   ├── signup.html  
│   │   └── top.html  
│   ├── app.py  
│   └── generate_text.py  
├── requirements.txt  
└── run.sh
</pre>
src : コード  
templates : htmlなど  
・admin : 管理者用ページ(ユーザ一覧とそれらの編集、削除)  
・admin_update : ユーザ情報の編集  
・login : ログインページ  
・main  : メインページ  
・mypage : ユーザの情報の参照・変更ページ  
・signup : サインアップ  
・top : ログインとサインインにつなぐトップページ  

## マイページ
ユーザ情報 : 名前(text), 強み(text)  

## 実行手順
クローン
```
$ git clone https://github.com/takaki12/job-hunting-support-system.git
```
python3.10以上のvenvを作成し、必要なライブラリをインポートする
```
$ python3 -m venv .venv
$ pip install -r requirements.txt
```
システム立ち上げ(バックグラウンド推奨)
```
./run.sh
```
以下のURLをブラウザで開く
```
http://127.0.0.1:5000
```