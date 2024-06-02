from database import db
import uuid
from flask_login import current_user
from db_models.models import Transcribation, Annotation


def save_transcribation_db(transcribation_result: str) -> Transcribation:
    tran = Transcribation(
        transcribation=transcribation_result
    )
    db.session.add(tran)
    db.session.commit()
    return tran


def save_annotation(title: str, annotation_result: str, annotation_type: str, file_id: uuid,
                    transcribation_id: uuid) -> Annotation:
    annotation = Annotation(
        title=title,
        annotation=annotation_result,
        file_id=file_id,
        annotation_type=annotation_type,
        transcribation_id=transcribation_id,
        user_id=current_user.id
    )
    db.session.add(annotation)
    db.session.commit()
    return annotation
