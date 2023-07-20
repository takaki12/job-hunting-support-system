import os
import random
import string
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_login import login_user, LoginManager, login_manager, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# from generate import generate
from generate_text.generate_text import generate_text

app = Flask(__name__)

# データベースの設定
db_path = ""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ db_path + "wraites.db"
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)

# ログインマネージャーの設定
login_manager = LoginManager()
login_manager.init_app(app)

# ランダム文字列idの生成
def randomid(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for _ in range(n)]
   return "".join(randlst)

# ユーザクラス
class UserInformation(UserMixin, db.Model):
    id = db.Column(db.String(10), primary_key=True, autoincrement=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(500), nullable=False)
    weakness = db.Column(db.String(500), nullable=False)
    
class CompanyInformation(db.Model):
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(1000), nullable=True)
    occupation = db.Column(db.String(1000), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(1000), nullable=True)
    recruitment_type = db.Column(db.String(1000), nullable=True)
    business_content = db.Column(db.String(1000), nullable=True)
    company_info = db.Column(db.String(1000), nullable=True)
    recruitment_info = db.Column(db.String(1000), nullable=True)

# トップページ
@app.route("/")
def top():
    # データベース初期化
    with app.app_context():
        db.session.query(CompanyInformation).delete()
        db.session.commit()
    
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    json = "/Users/ttt/Documents/Master2023/デジタルコンテンツ特論/celest-393403-927fcb61c0da.json"
    creadentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
    gc = gspread.authorize(creadentials)

    SPREADSHEET_KEY = "1UhdIVYfoCCLvPp33thoKXrfRcy-6k3OkwKK0YY7cZHU"

    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    company_df = pd.DataFrame(worksheet.get_all_records())
    # num_id = 1
    for i in range(len(company_df)):
        if company_df["企業名"][i] != "":
            # DBに企業情報登録
            company = CompanyInformation(company_name=company_df["企業名"][i], purpose=company_df["企業理念・MVV"][i], occupation=company_df["職種"][i], industry=company_df["業種"][i], condition=company_df["条件"][i], recruitment_type=company_df["インターン/採用"][i], business_content=company_df["業務内容"][i], company_info=company_df["参考リンク(企業情報)"][i], recruitment_info=company_df["参考リンク(就職情報)"][i])
            db.session.add(company)
            db.session.commit()
            # num_id += 1

    return render_template("top.html")

# メインページ
@app.route("/main/<string:id>", methods=["GET", "POST"])
@login_required
def main(id):
    user = load_user(id)
    if request.method == "POST":
        # テキスト生成
        occupation = "データサイエンティスト"
        condition = "プログラミング経験あり"
        experience = user.experience
        business_content = "私たちが便利で快適な生活を営む上でかかせない社会インフラ。交通・情報・セキュリティなど安全・安心・快適な社会を支えるためのシステムづくりが住友電工システムソリューションの仕事です。"
        lower = int(request.form.get("lower"))
        upper = int(request.form.get("upper"))
        # print(lower, upper)
        # output = generate(lower, upper)
        output = generate_text(occupation, condition, experience, business_content, lower, upper)
        return render_template("main.html", output=output, id=id)
    else:
        return render_template("main.html", id=id)

# マイページ
@app.route("/mypage/<string:id>")
@login_required
def mypage(id):
    user = load_user(id)
    return render_template("mypage.html", user=user)

# ユーザによるユーザ情報更新
@app.route("/own_update/<string:id>", methods=["GET", "POST"])
@login_required
def own_update(id):
    user = load_user(id)
    if request.method == "POST":
        user.id = request.form.get("id")
        user.name = request.form.get("name")
        user.experience = request.form.get("experience")
        user.weakness = request.form.get("weakness")
        db.session.commit()
        id = user.id
        # logout_user()
        login_user(user)
        return redirect("/mypage/" + id)
    else:
        return render_template("own_update.html", user=user)

# 管理者ページ
@app.route("/admin")
def admin():
    # DBに登録されたデータを全て取得
    users = UserInformation.query.all()
    return  render_template("admin.html", users=users)

# 管理者によるユーザ情報更新
@app.route("/admin_update/<string:id>", methods=["GET", "POST"])
def admin_update(id):
    user = load_user(id)
    if request.method == "POST":
        user.id = request.form.get("id")
        user.name = request.form.get("name")
        user.experience = request.form.get("experience")
        user.weakness = request.form.get("weakness")
        db.session.commit()
        return redirect("/admin")
    else:
        return render_template("admin_update.html", user=user)

# 管理者によるユーザ情報削除
@app.route("/admin_delete/<string:id>", methods=["GET"])
def delete(id):
    user = load_user(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/admin")

# サインアップ
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        id = randomid(10)
        name = request.form.get("name")
        password = request.form.get("password")
        experience = request.form.get("experience")
        weakness = request.form.get("weakness")
        # DBに登録
        user = UserInformation(id=id, name=name, password=generate_password_hash(password, method="sha256"), experience=experience, weakness=weakness)
        db.session.add(user)
        db.session.commit()
        return render_template("signup_confirm.html", id=id, name=name, password=password, experience=experience, weakness=weakness)
    else:
        return render_template("signup.html")
    
# サインアップ確認
@app.route("/signup_confirm")
def signup_confirm():
    return redirect("/signup_confirm")

# サインイン
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        id = request.form.get("id")
        password = request.form.get("password")
        # 入力からDB内のユーザ情報を取得
        user = UserInformation.query.filter_by(id=id).first()
        # パスワードチェック
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main", id=id))
    else:
        return render_template("signin.html")

# サインアウト
@app.route("/signout")
def signout():
    logout_user()
    return redirect("/")

# ログイン済みユーザの情報を取得
@login_manager.user_loader
def load_user(user_id):
    return UserInformation.query.get(user_id)


if __name__ == "__main__":
    # データベース作成
    if not os.path.exists("instance/wraites.db"):
        with app.app_context():
            db.create_all()
    
    app.run(debug=True)
