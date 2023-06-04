# job-hunting-support-system
企業データを用いた就活支援システムの構築

## フォルダ構造
<pre>
.  
├── instance  
│   └── users.db  
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
### 詳細
- instance : データベースが保存されている
- src : 本システムで使用しているコード置き場  
  - templates : htmlなど  
    - admin_update : ユーザ情報の編集  
    - admin : 管理者用ページ(ユーザ一覧とそれらの編集、削除)  
    - main : メインページ  
    - mypage : ユーザの情報の参照・変更ページ  
    - signin : サインイン
    - signup : サインアップ  
    - top : ログインとサインインにつなぐトップページ  
  - app.py : webシステムと各ページの定義  
  - generate_text.py : 志望動機を生成する  
- requirements.txt : 必要ライブラリ  
- run.sh : システム起動  

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