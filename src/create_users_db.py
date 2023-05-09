from app import app, users_db
with app.app_context():
    users_db.create_all()