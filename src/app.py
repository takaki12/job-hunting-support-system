import os
from flask import Flask
from flask import render_template, request, redirect
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# データベースの設定
db_path = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_path + 'users.db'
users_db = SQLAlchemy(app)

# ユーザクラス
class UserInformation(users_db.Model):
    id = users_db.Column(users_db.Integer, primary_key=True)
    name = users_db.Column(users_db.String(20), nullable=False)
    password = users_db.Column(users_db.String(100), nullable=False)
    strong = users_db.Column(users_db.String(200), nullable=False)

@app.route('/')
def top():
    return render_template('top.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

@app.route('/admin')
def admin():
    # DBに登録されたデータを全て取得
    users = UserInformation.query.all()
    return  render_template('admin.html', users=users)

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
        return redirect('/')
    else:
        return render_template('signup.html')
    
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

@app.route('/admin_delete/<int:id>', methods=['GET'])
def delete(id):
    user = UserInformation.query.get(id)
    users_db.session.delete(user)
    users_db.session.commit()
    return redirect('/admin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        # 入力からDB内のユーザ情報を取得
        user = UserInformation.query.filter_by(name=name).first()
        # パスワードチェック
        if check_password_hash(user.password, password):
            return redirect('/main')
    else:
        return render_template('login.html')
    
@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == "__main__":
    # データベース作成
    if not os.path.exists("instance/users.db"):
        with app.app_context():
            users_db.create_all()
    app.run(debug=True)