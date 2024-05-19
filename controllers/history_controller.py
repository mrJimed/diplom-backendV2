from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from database import db
from db_models.annotation import Annotation

history_controller = Blueprint('history_controller', __name__, url_prefix='/history')


@history_controller.post('')
@login_required
def add_annotation():
    data = request.get_json()
    new_summarized_text = Annotation(
        title=data['title'],
        text=data['text'],
        user_id=current_user.id
    )
    db.session.add(new_summarized_text)
    db.session.commit()
    return '', 200


@history_controller.get('')
@login_required
def get_annotation_history():
    annotations = Annotation.query.filter(Annotation.user_id == current_user.id).all()
    annotations = sorted(annotations, key=lambda annotation: annotation.create_ts, reverse=True)
    return jsonify([annotation.serialize() for annotation in annotations]), 200
