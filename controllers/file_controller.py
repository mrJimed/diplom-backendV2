import uuid

from flask import Blueprint, send_file
from services.file_service import get_file_path

from db_models.models import File

file_controller = Blueprint('file_controller', __name__, url_prefix='/file')


@file_controller.get('/<id>')
def download_file(id):
    file = File.query.filter(File.id == uuid.UUID(id)).first()
    return send_file(path_or_file=get_file_path(f'{file.id}{file.extension}'),
                     as_attachment=True,
                     download_name=file.filename)
