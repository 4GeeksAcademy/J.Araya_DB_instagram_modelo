from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Initialize SQLAlchemy
db = SQLAlchemy()

# Association table to represent followers relationship
class Follower(db.Model):
    __tablename__ = 'follower'

    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

    def serialize(self):
        return {
            'user_from_id': self.user_from_id,
            'user_to_id': self.user_to_id
        }

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    # Relationships
    posts = relationship('Post', back_populates='author', cascade='all, delete')
    comments = relationship('Comment', back_populates='author', cascade='all, delete')
    following = relationship(
        'User', secondary='follower',
        primaryjoin=id == Follower.user_from_id,
        secondaryjoin=id == Follower.user_to_id,
        backref='followers'
    )

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email
        }

class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    # Relationships
    author = relationship('User', back_populates='posts')
    media_items = relationship('Media', back_populates='post', cascade='all, delete')
    comments = relationship('Comment', back_populates='post', cascade='all, delete')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id
        }

class Media(db.Model):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    # Relationships
    post = relationship('Post', back_populates='media_items')

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'url': self.url,
            'post_id': self.post_id
        }

class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    # Relationships
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            'id': self.id,
            'comment_text': self.comment_text,
            'author_id': self.author_id,
            'post_id': self.post_id
        }