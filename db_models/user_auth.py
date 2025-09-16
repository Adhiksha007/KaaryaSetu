from db_models import db
from datetime import datetime

class UserAuth(db.Model):
    __tablename__ = 'user_auth'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('UserProfile', backref='auth', uselist=False, cascade="all, delete-orphan")
