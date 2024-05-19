import uuid

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from database import db


class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    annotations = db.relationship('Annotation', backref='user', lazy=True)
