from flask import Blueprint, request
from flask_login import current_user

from services import email_service
from services.annotation_service import save_transcribation_db, save_annotation
from services.file_service import save_file, save_file_after_database, save_file_db, remove_file, remove_dir
from summarization.extractive.lex_rank_summarizer import LexRankSummarizer as lexrank
from summarization.abstractive.bart_summarizer import BartSummarizer as bart

annotation_controller = Blueprint('annotation_controller', __name__, url_prefix='/annotation')


def send_email(to_email: str, annotation: str, filename: str):
    email_service.send_email(
        to_email=to_email,
        subject=f'Результат аннотирования для файла \"{filename}\"',
        text=annotation
    )


@annotation_controller.post('/abstractive')
def abstractive():
    file = request.files['file']
    max_length = int(request.form['maxLength']) / 100
    min_length = int(request.form['minLength']) / 100

    if current_user is not None:
        file_text = file.stream.read().decode("utf-8")
        db_file = save_file_db(file)
        save_file_after_database(file, f'{db_file.id}{db_file.extension}')
        tran_result = file_text
        annotation = bart().summarize_text(tran_result, max_length, min_length)
        save_annotation(
            title=file.filename,
            annotation_result=annotation,
            annotation_type='Абстрактивная',
            file_id=db_file.id,
            transcribation_id=save_transcribation_db(tran_result).id
        )
        remove_dir(f'{db_file.id}')
        if request.form['isSendEmail'].lower() == 'true':
            send_email(request.form['toEmail'], annotation, file.filename)
        return annotation
    else:
        filename = save_file(file)
        tran_result = file.stream.read().decode("utf-8")
        annotation = bart().summarize_text(tran_result, max_length, min_length)
        if request.form['isSendEmail'].lower() == 'true':
            send_email(request.form['toEmail'], annotation, file.filename)
        remove_file(filename)
        return annotation


@annotation_controller.post('/extractive')
def extractive():
    file = request.files['file']
    top_n = int(request.form['topN'])

    if current_user is not None:
        file_text = file.stream.read().decode("utf-8")
        db_file = save_file_db(file)
        save_file_after_database(file, f'{db_file.id}{db_file.extension}')
        tran_result = file_text
        annotation = lexrank.summarize_text(tran_result, top_n, False)
        save_annotation(
            title=file.filename,
            annotation_result=annotation,
            annotation_type='Экстрактивная',
            file_id=db_file.id,
            transcribation_id=save_transcribation_db(tran_result).id
        )
        remove_dir(f'{db_file.id}')
        if request.form['isSendEmail'].lower() == 'true':
            send_email(request.form['toEmail'], annotation, file.filename)
        return annotation
    else:
        filename = save_file(file)
        tran_result = file.stream.read().decode("utf-8")
        annotation = lexrank.summarize_text(tran_result, top_n, False)
        if request.form['isSendEmail'].lower() == 'true':
            send_email(request.form['toEmail'], annotation, file.filename)
        remove_file(filename)
        return annotation
