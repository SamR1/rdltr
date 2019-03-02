import datetime

from sqlalchemy import UniqueConstraint

from .. import db
from ..users.model import User

tags_to_articles = db.Table(
    'articles_tags',
    db.Column(
        'tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True
    ),
    db.Column(
        'page_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True
    ),
)


class Category(db.Model):
    __tablename__ = "categories"
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
    user = db.relationship(User, backref='category_user')
    articles = db.relationship('Article', backref='category_articles')

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'is_default': self.is_default,
        }


class Tag(db.Model):
    __tablename__ = "tags"
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
    user = db.relationship(User, backref='tag_user')

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def serialize(self):
        return {'id': self.id, 'user_id': self.user_id, 'name': self.name}


class Article(db.Model):
    __tablename__ = "articles"
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
    category = db.relationship(Category, backref='category')
    tags = db.relationship(
        Tag,
        secondary=tags_to_articles,
        lazy='subquery',
        backref=db.backref('articles', lazy=True),
    )

    def __init__(self, category_id, url, title, content, html_content):
        self.category_id = category_id
        self.url = url
        self.title = title
        self.content = content
        self.html_content = html_content

    def serialize(self):
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
        }
