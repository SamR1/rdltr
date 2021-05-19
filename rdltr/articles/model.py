import datetime
from typing import Dict

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import DeclarativeMeta

from .. import db
from ..users.model import User

BaseModel: DeclarativeMeta = db.Model

tags_to_articles = db.Table(
    'articles_tags',
    db.Column(
        'tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True
    ),
    db.Column(
        'page_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True
    ),
)


class Category(BaseModel):
    __tablename__ = 'categories'
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='category_unique_name'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_user_category'),
        nullable=True,
    )
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    is_default = db.Column(db.Boolean, default=False)
    user = db.relationship(User, back_populates='categories')
    articles = db.relationship('Article', back_populates='category')

    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name

    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'is_default': self.is_default,
            'nb_articles': len(self.articles),
        }


class Tag(BaseModel):
    __tablename__ = 'tags'
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='tag_unique_name'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_user_tags'),
        nullable=True,
    )
    name = db.Column(db.String(50), nullable=False)
    user = db.relationship(User, back_populates='tags')

    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name

    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'nb_articles': len(self.articles),
        }


class Article(BaseModel):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', name='fk_category_articles'),
        nullable=True,
    )
    url = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    html_content = db.Column(db.String(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.Column(db.String())
    read_status = db.Column(db.Boolean(), default=False, nullable=False)
    favorite = db.Column(db.Boolean(), default=False, nullable=False)
    category = db.relationship(Category, back_populates='articles')
    tags = db.relationship(
        Tag,
        secondary=tags_to_articles,
        lazy='subquery',
        backref=db.backref('articles', lazy=True),
    )

    def __init__(
        self,
        category_id: int,
        url: str,
        title: str,
        content: str,
        html_content: str,
    ) -> None:
        self.category_id = category_id
        self.url = url
        self.title = title
        self.content = content
        self.html_content = html_content

    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'html_content': self.html_content,
            'category': self.category.serialize(),
            'tags': [tag.serialize() for tag in self.tags],
            'comments': self.comments,
            'date_added': self.date_added,
            'read': self.read_status,
            'favorite': self.favorite,
        }
