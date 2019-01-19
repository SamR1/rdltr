import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from rdltr import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<User {self.username!r}>'

    def __init__(
        self, username, email, password, created_at=datetime.datetime.utcnow()
    ):
        self.username = username
        self.email = email
        self.created_at = created_at
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
