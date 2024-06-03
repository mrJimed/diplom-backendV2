import uuid

from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from db_models.models import Annotation, Transcribation, File

history_controller = Blueprint('history_controller', __name__, url_prefix='/history')


@history_controller.get('')
@login_required
def get_annotation_history():
    annotations = Annotation.query.filter(Annotation.user_id == current_user.id).all()
    annotations = sorted(annotations, key=lambda annotation: annotation.create_ts, reverse=True)
    return jsonify([{
        'id': annotation.id,
        'annotation': annotation.annotation,
        'title': annotation.title,
        'create_ts': annotation.create_ts.strftime("%H:%M %d.%m.%Y ")
    } for annotation in annotations]), 200


@history_controller.get('/<id>')
@login_required
def get_annotation_history_info(id):
    annotation = Annotation.query.filter(Annotation.id == uuid.UUID(id)).first()
    transcribation = Transcribation.query.filter(Transcribation.id == annotation.transcribation_id).first()
    file = File.query.filter(File.id == annotation.file_id).first()

    return {
        'annotation': annotation.annotation,
        'title': annotation.title,
        'type':annotation.annotation_type,
        'create_ts': annotation.create_ts.strftime("%H:%M %d.%m.%Y "),
        'transcribation': transcribation.transcribation,
        'file_id': file.id,
        'filename': file.filename
    }, 200
