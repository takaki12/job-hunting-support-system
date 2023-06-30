import os
from flask import Flask
from flask import render_template, request, redirect
from flask_login import login_user, LoginManager, login_manager, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from generate_text import generate


app = Flask(__name__)
# データベースの設定
db_path = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_path + 'users.db'
app.config['SECRET_KEY'] = os.urandom(24)
users_db = SQLAlchemy(app)

# ログインマネージャーの設定
login_manager = LoginManager()
login_manager.init_app(app)

# ユーザクラス
class UserInformation(UserMixin, users_db.Model):
    id = users_db.Column(users_db.Integer, primary_key=True)
    name = users_db.Column(users_db.String(20), nullable=False)
    password = users_db.Column(users_db.String(100), nullable=False)
    strong = users_db.Column(users_db.String(200), nullable=False)

# トップページ
@app.route('/')
def top():
    return render_template('top.html')

# メインページ
@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        # テキスト生成
        data1 = request.form.get('data1')
        data2 = request.form.get('data2')
        data3 = request.form.get('data3')
        output = generate(data1, data2, data3)
        return render_template('main.html', output=output)
    else:
        return render_template('main.html')

# マイページ
@app.route('/mypage')
@login_required
def mypage():
    return render_template('mypage.html')

# 管理者ページ
@app.route('/admin')
def admin():
    # DBに登録されたデータを全て取得
    users = UserInformation.query.all()
    return  render_template('admin.html', users=users)

# 管理者によるユーザ情報更新
@app.route('/admin_update/<int:id>', methods=['GET', 'POST'])
def admin_update(id):
    user = UserInformation.query.get(id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.strong = request.form.get('strong')
        users_db.session.commit()
        return redirect('/admin')
    else:
        return render_template('admin_update.html', user=user)

# 管理者によるユーザ情報削除
@app.route('/admin_delete/<int:id>', methods=['GET'])
def delete(id):
    user = UserInformation.query.get(id)
    users_db.session.delete(user)
    users_db.session.commit()
    return redirect('/admin')

# サインアップ
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        strong = request.form.get('strong')
        # DBに登録
        user = UserInformation(name=name, password=generate_password_hash(password, method='sha256'), strong=strong)
        users_db.session.add(user)
        users_db.session.commit()
        return redirect('/signin')
    else:
        return render_template('signup.html')

# サインイン
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        # 入力からDB内のユーザ情報を取得
        user = UserInformation.query.filter_by(name=name).first()
        # パスワードチェック
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/main')
    else:
        return render_template('signin.html')

# サインアウト
@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect('/signin')

# ログイン済みユーザの情報を取得
@login_manager.user_loader
def load_user(user_id):
    return UserInformation.query.get(int(user_id))


if __name__ == "__main__":
    # データベース作成
    if not os.path.exists("instance/users.db"):
        with app.app_context():
            users_db.create_all()
    app.run(debug=True)