from datetime import datetime
from extensions import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )
    is_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    failed_login_attempts = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )
    locked_until = db.Column(
        db.DateTime,
        nullable=True
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    last_login = db.Column(
        db.DateTime,
        nullable=True
    )
    def __repr__(self):
        return f"<User {self.username}>"
class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    jti = db.Column(
        db.String(255),
        nullable=False,
        unique=True,
        index=True
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    def __repr__(self):
        return f"<RevokedToken {self.jti}>"