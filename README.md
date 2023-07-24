# job-hunting-support-system
企業データを用いた就活支援システムの構築

## フォルダ構造
<pre>
.  
├── instance  
│   └── users.db  
├── src  
│   ├── generate_text  
│   │   ├── character_limit.py  
│   │   ├── generate_text.py  
│   │   └── match_experience.py  
│   ├── static  
│   │   ├── css  
│   │   │   └── style1.css    
│   │   └── js  
│   │       └── function.js  
│   ├── templates  
│   │   ├── admin_update.html  
│   │   ├── admin.html  
│   │   ├── main.html  
│   │   ├── mypage.html  
│   │   ├── own_update.html  
│   │   ├── signin.html  
│   │   ├── signup.html  
│   │   └── top.html  
│   └── app.py  
├── requirements.txt  
└── run.sh
</pre>
### 詳細
- instance : データベースが保存されている
- src : 本システムで使用しているコード置き場  
  - generate_text : 文章生成プログラム
  - static : cssやJavaScriptなど
  - templates : htmlなど  
    - admin_update : ユーザ情報の編集(管理者)  
    - admin : 管理者用ページ(ユーザ一覧とそれらの編集、削除)  
    - main : メインページ  
    - mypage : ユーザの情報の参照・変更ページ  
    - own_update : ユーザ情報の編集(ユーザ自身)
    - signin : サインイン
    - signup : サインアップ  
    - top : ログインとサインインにつなぐトップページ  
  - app.py : webシステムと各ページの定義  
- requirements.txt : 必要ライブラリ  
- run.sh : システム起動  

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
このとき、プロジェクトディレクトリ直下にスプレッドシートAPIのキー情報jsonファイルを置く。  
また、所定の場所にOpenAIのAPIキーを入れる。  
システム立ち上げ(バックグラウンド推奨)  
```
./run.sh
```
以下のURLをブラウザで開く  
```
http://127.0.0.1:5000
```