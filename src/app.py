import os
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_path=None)
# データベースの設定
db_path = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ db_path + 'users.db'
users_db = SQLAlchemy(app)
# データベース作成
if not os.path.exists("instance/users.db"):
    with app.app_context():
        users_db.create_all()

# ユーザクラス
class UserInformation(users_db.Model):
    id = users_db.Column(users_db.Integer, primary_key=True)
    name = users_db.Column(users_db.String(20), nullable=False)
    strong = users_db.Column(users_db.String(200), nullable=False)

@app.route('/')
def top():
    return render_template('top.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

if __name__ == "__main__":
    app.run(debug=True)