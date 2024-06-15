import os
import re
import uuid

from werkzeug.datastructures.file_storage import FileStorage


def get_path(filename: str):
    return os.path.join('upload', filename)


def get_file_content(file: FileStorage):
    return file.stream.read().decode("utf-8")


def remove_file(filename: str):
    os.remove(get_path(filename))


def get_correct_formats():
    return ['.wav', '.mp3', '.acc', '.mp4', '.mov', '.mvm', '.avi']


def is_correct_format(file_extension: str):
    return file_extension.lower() in get_correct_formats()


def get_file_extension(filename: str):
    return re.search(r'\.[\w\d]+$', filename).group()


def save_file(file: FileStorage):
    extension = get_file_extension(file.filename)
    new_filename = f'{uuid.uuid4()}{extension}'
    path = get_path(new_filename)
    file.save(path)
    return new_filename
