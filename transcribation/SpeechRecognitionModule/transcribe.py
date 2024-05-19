"""
Модуль содержит функцию осуществляющую перевод аудио в текст.
"""
import torch

from .split_audio import Audio2Chunks
from .raw_transcription import RawTranscriptionModel
from .spelling_correction import SpellingCorrector
from .utils import print_stats


def speech2text(path2audio: str,
                device: torch.device,
                batch_size: int = 16,
                verbose: int = 1,
                max_seq_len: int = 256,
                max_chunk_duration: int = 150) -> str:
    """
    Функция переводит аудио в текст.
    Args:
        path2audio (str): Путь до аудио.
        device (torch.device): CPU или GPU.
        batch_size (int): Размер batch-а.
        verbose (int): Уровень подробности.
                       Если =0, то только возвращение output-а.
                       Если =1, то предыдущее, а также вывод статистики по времени работы.
                       Если =2, то предыдущее, а также вывод промежуточных результатов после каждого подэтапа.
        max_seq_len (int): Максимальная длина входной последовательности для токенизатора.
        max_chunk_duration (int): Максимальная продолжительность чанка в секундах.

    Returns:
        Текст извлеченный из аудио.
    """
    if verbose == 2: print("Starting splitting audio on chunks.")
    audio_splitter = Audio2Chunks(path2audio=path2audio, verbose=verbose, max_chunk_duration=max_chunk_duration)
    audio_splitter.split_and_save_chunks()
    if verbose == 2: print("Finished splitting audio on chunks.")

    if verbose == 2: print("Started transcribing chunks splitting audio.")
    nemo_model = RawTranscriptionModel(paths2chunks=audio_splitter.paths2chunks)
    nemo_model.raw_transcription(batch_size=batch_size)
    if verbose == 2: print("Finished transcribing chunks splitting audio.")

    if verbose == 2: print("Started correcting spelling and merging chunks.")
    speller = SpellingCorrector(raw_sentences=nemo_model.raw_transcriptions,
                                device=device,
                                concat_sentences=True,
                                max_input=max_seq_len)
    output = speller.correct_spelling()
    if verbose == 2: print("Finished correcting spelling and merging chunks.")

    if verbose >= 1: print_stats(audio_duration=audio_splitter.audio_duration,
                                time_for_splitting_audio=audio_splitter.split_audio_duration,
                                time_for_transcribing=nemo_model.transcription_duration,
                                time_for_spelling_correction=speller.spelling_correction_duration)

    return output
