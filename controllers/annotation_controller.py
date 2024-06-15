from flask import Blueprint, request

from services import email_service
from services.file_service import save_file, get_path, remove_file, get_file_extension, is_correct_format, get_correct_formats
from summarization.abstractive.bart_summarizer import BartSummarizer as bart
from summarization.extractive.lex_rank_summarizer import LexRankSummarizer as lexrank
from transcribation.demo import transcribation

annotation_controller = Blueprint('annotation_controller', __name__, url_prefix='/annotation')


@annotation_controller.post('/extractive')
def extractive():
    file = request.files['file']
    top_n = int(request.form['topN'])

    if (not is_correct_format(get_file_extension(file.filename))):
        return f'Данный формат файла не поддерживается. Поддерживаемые форматы: {", ".join(get_correct_formats())}', 400

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

    if (not is_correct_format(get_file_extension(file.filename))):
        return f'Данный формат файла не поддерживается. Поддерживаемые форматы: {", ".join(get_correct_formats())}', 400
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
