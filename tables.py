from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    pw_hash = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, name, email, pw_hash, role):
        self.name = name
        self.email = email
        self.pw_hash = pw_hash
        self.role = role
