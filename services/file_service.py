import os
import re
import uuid
import shutil
from werkzeug.datastructures.file_storage import FileStorage

from database import db
from db_models.models import File


def remove_dir(dir_name: str):
    shutil.rmtree(get_file_path(dir_name))


def get_file_path(filename: str) -> str:
    return os.path.join('upload', filename)


def save_file(file: FileStorage) -> str:
    extension = re.search(r'\.[\w\d]+$', file.filename).group()
    new_filename = f'{uuid.uuid4()}{extension}'
    path = get_file_path(new_filename)
    file.save(path)
    return new_filename


def save_file_after_database(file: FileStorage, new_filename: str):
    path = get_file_path(new_filename)
    file.save(path)


def save_file_db(file: FileStorage) -> File:
    extension = re.search(r'\.[\w\d]+$', file.filename).group()
    db_file = File(
        filename=file.filename,
        extension=extension
    )
    db.session.add(db_file)
    db.session.commit()
    return db_file


def remove_file(filename: str):
    os.remove(get_file_path(filename))
