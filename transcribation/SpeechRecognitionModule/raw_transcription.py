"""
Модуль содержит в себе класс, для работы с этапом распознавания аудио в чанках.
"""
import time
from typing import List

import nemo.collections.asr as nemo_asr
from tqdm import tqdm


class RawTranscriptionModel:
    """
    Класс для первичного распознавания речи.
    """

    def __init__(self, paths2chunks: List[str]):
        """
        Инициализация модели Nemo, для распознавания речи.
        Args:
            paths2chunks (List[str]): Список путей до чанков к распознаваемому аудио (аудио и его чанки
                                                                                    должны быть 16K mono wav!).
        """
        self.model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained("nvidia/stt_ru_conformer_transducer_large")
        self.paths2chunks = paths2chunks
        self.num_chunks = len(paths2chunks)
        self.raw_transcriptions: List[str] = []
        self.transcription_duration = None

    def _transcribe_chunk(self, idx: int, batch_size: int = 16) -> None:
        """
        Транскрибация отдельного чанка.
        Args:
            idx: Индекс чанка.
            batch_size: Размер batch-а.
        """
        transcribed_text = self.model.transcribe([self.paths2chunks[idx]], batch_size=batch_size)[0][0]
        if len(transcribed_text) != 0:
            self.raw_transcriptions.append(transcribed_text)

    def raw_transcription(self, batch_size: int = 16) -> None:
        """
        Транскрибация всех чанков. Результат транскрибации находится в self.raw_transcriptions
        Args:
            batch_size: Размер batch-а.
        """
        transcribing_start_time = time.time()
        for i in tqdm(range(self.num_chunks)):
            self._transcribe_chunk(i, batch_size=batch_size)
        self.transcription_duration = time.time() - transcribing_start_time





