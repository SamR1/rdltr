from datetime import datetime, timedelta
from typing import Dict, Optional, Union

import jwt
from flask import current_app
from sqlalchemy.ext.declarative import DeclarativeMeta

from .. import bcrypt, db

BaseModel: DeclarativeMeta = db.Model


class User(BaseModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    categories = db.relationship("Category", back_populates="user")
    tags = db.relationship("Tag", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username!r}>"

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        created_at: Optional[datetime] = None,
    ):
        self.username = username
        self.email = email
        self.created_at = created_at if created_at else datetime.utcnow()
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()

    @staticmethod
    def encode_auth_token(user_id: int) -> str:
        """
        Generates the auth token
        :param user_id: -
        :return: JWToken
        """
        payload = {
            "exp": datetime.utcnow()
            + timedelta(
                days=current_app.config["TOKEN_EXPIRATION_DAYS"],
                seconds=current_app.config["TOKEN_EXPIRATION_SECONDS"],
            ),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(
            payload, current_app.config["SECRET_KEY"], algorithm="HS256"
        )

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[int, str]:
        """
        Decodes the auth token
        :param auth_token: -
        :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def serialize(self) -> Dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "categories": [
                category.serialize() for category in self.categories
            ],
            "tags": [tag.serialize() for tag in self.tags],
        }
