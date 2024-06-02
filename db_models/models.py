import uuid
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from database import db


class File(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    filename = db.Column(db.Text, nullable=False)
    extension = db.Column(db.String, nullable=False)
    annotation = db.relationship('Annotation', backref='file', uselist=False)


class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    annotations = db.relationship('Annotation', backref='user', lazy=True)


class Transcribation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    transcribation = db.Column(db.Text, nullable=False)
    annotation = db.relationship('Annotation', backref='transcribation', uselist=False)


class Annotation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    create_ts = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    title = db.Column(db.String, nullable=False)
    annotation = db.Column(db.Text, nullable=False)
    annotation_type = db.Column(db.String, nullable=False)
    file_id = db.Column(UUID(as_uuid=True), db.ForeignKey('file.id'), nullable=False)
    transcribation_id = db.Column(UUID(as_uuid=True), db.ForeignKey('transcribation.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
