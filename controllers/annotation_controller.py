import os
import re
import uuid
from flask import Blueprint, request
from werkzeug.datastructures.file_storage import FileStorage

from services import email_service
from summarization.abstractive.bart_summarizer import BartSummarizer as bart
from summarization.extractive.lex_rank_summarizer import LexRankSummarizer as lexrank
from transcribation.demo import transcribation

annotation_controller = Blueprint('annotation_controller', __name__, url_prefix='/annotation')


def get_file_content(file: FileStorage):
    return file.stream.read().decode("utf-8")


def get_path(filename: str):
    return os.path.join('upload', filename)


def save_file(file: FileStorage):
    extension = re.search(r'\.[\w\d]+$', file.filename).group()
    new_filename = f'{uuid.uuid4()}{extension}'
    path = get_path(new_filename)
    file.save(path)
    return new_filename


def remove_file(filename: str):
    os.remove(get_path(filename))


@annotation_controller.post('/extractive')
def extractive():
    file = request.files['file']
    top_n = int(request.form['topN'])

    filename = save_file(file)
    text = transcribation(get_path(filename))
    annotation = lexrank.summarize_text(text, top_n, False)
    remove_file(filename)

    if request.form['isSendEmail'].lower() == 'true':
        to_email = request.form['toEmail']
        email_service.send_email(
            to_email=to_email,
            subject=f'Результат аннотирования для файла \"{file.filename}\"',
            text=annotation
        )
    return annotation


@annotation_controller.post('/abstractive')
def abstractive():
    file = request.files['file']
    max_length = int(request.form['maxLength']) / 100
    min_length = int(request.form['minLength']) / 100
    print(f'Abstractive summarization started (min_length={min_length}, max_length={max_length})')

    filename = save_file(file)
    text = transcribation(get_path(filename))
    print(text)
    annotation = bart().summarize_text(text, max_length=max_length, min_length=min_length)
    remove_file(filename)

    if request.form['isSendEmail'].lower() == 'true':
        to_email = request.form['toEmail']
        email_service.send_email(
            to_email=to_email,
            subject=f'Результат аннотирования для файла \"{file.filename}\"',
            text=annotation
        )
    return annotation
