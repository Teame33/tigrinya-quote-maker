from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(200))
    bio = db.Column(db.Text)
    website = db.Column(db.String(200))
    language_preference = db.Column(db.String(10), default='en')
    theme_preference = db.Column(db.String(20), default='light')
    
    # Relationships
    quotes = db.relationship('Quote', backref='author', lazy='dynamic')
    collections = db.relationship('Collection', backref='owner', lazy='dynamic')
    followers = db.relationship('Follow',
                              foreign_keys='Follow.followed_id',
                              backref=db.backref('followed', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    following = db.relationship('Follow',
                              foreign_keys='Follow.follower_id',
                              backref=db.backref('follower', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def followers_count(self):
        return self.followers.count()

    @hybrid_property
    def following_count(self):
        return self.following.count()

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    content_tigrinya = db.Column(db.Text)
    translation = db.Column(db.Text)
    category = db.Column(db.String(50))
    background = db.Column(db.String(200))
    font = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    scheduled_post = db.Column(db.DateTime)
    image_path = db.Column(db.String(200))
    
    # Relationships
    likes = db.relationship('Like', backref='quote', lazy='dynamic')
    comments = db.relationship('Comment', backref='quote', lazy='dynamic')
    collections = db.relationship('Collection', secondary='quote_collections')

    @hybrid_property
    def likes_count(self):
        return self.likes.count()

    @hybrid_property
    def comments_count(self):
        return self.comments.count()

class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    
    quotes = db.relationship('Quote', secondary='quote_collections')

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), nullable=False)

# Association table for quotes and collections
quote_collections = db.Table('quote_collections',
    db.Column('quote_id', db.Integer, db.ForeignKey('quotes.id'), primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id'), primary_key=True)
)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    related_id = db.Column(db.Integer)  # ID of related object (quote, comment, etc.)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    quotes = db.relationship('Quote', secondary='quote_tags')

# Association table for quotes and tags
quote_tags = db.Table('quote_tags',
    db.Column('quote_id', db.Integer, db.ForeignKey('quotes.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)
