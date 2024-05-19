import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from database import db


class Annotation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    create_ts = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'user_id': str(self.user_id),
            'create_ts': self.create_ts.strftime("%H:%M %d.%m.%Y ")
        }
