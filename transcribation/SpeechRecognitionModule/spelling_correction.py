"""
Модуль содержит в себе класс для правки "сырого" текста, полученного путем первичной
транскрибации, и расставления в нем пунктуации.
"""
import time
import torch
from typing import List, Union
from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast

from .utils import correct_cur_sent

class SpellingCorrector:
    """
    Класс для правки текста и расставления пунктуации.
    """
    def __init__(self,
                 raw_sentences: List[str],
                 device: torch.device,
                 concat_sentences: bool = True,
                 max_input: int = 256):
        """
        Инициализация токенизатора и модели для правки текста и расставления пунктуации.
        Args:
            raw_sentences (List[str]): Ожидается список предложений raw_transcriptions из RawTranscriptionModel.
            device (torch.device): GPU или CPU.
            concat_sentences (bool): True, если требуется сконкатенировать предложения в одно, False иначе.
            max_input (int): Максимальная длина входной последовательности (256 - максимум в данном случае).
        """
        SPELLING_CORRECTION_MODEL = 'UrukHan/t5-russian-spell'

        self.tokenizer = T5TokenizerFast.from_pretrained(SPELLING_CORRECTION_MODEL)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(SPELLING_CORRECTION_MODEL)
        self.raw_sentences = raw_sentences
        self.spelling_corrected_sentences: List[str] = []
        self.spelling_correction_duration = None
        self.concat = concat_sentences
        self.max_input = max_input
        self.device = device

    def _concatenate_sentences(self) -> str:
        """
        Конкатенация исправленных предложений.
        """
        concat_sentence = self.spelling_corrected_sentences[0]
        prev_sent = self.spelling_corrected_sentences[0]
        for cur_sent in self.spelling_corrected_sentences[1:]:
            concat_sentence += " " + correct_cur_sent(prev_sent, cur_sent)
            prev_sent = cur_sent

        return concat_sentence

    def correct_spelling(self) -> Union[List, str]:
        """
        Функция правит текст и расставляет в нем пунктуацию.
        Returns: поправленный текст с расставленной пунктуацией.
        """
        correct_spelling_start_time = time.time()

        # Tokenizing
        task_prefix = "Spell correct: "
        encoded = self.tokenizer(
            [task_prefix + sequence for sequence in self.raw_sentences],
            padding="longest",
            max_length=self.max_input,
            truncation=True,
            return_tensors="pt",
        )

        # Predict and decode
        predicts = self.model.generate(**encoded.to(self.device))
        self.spelling_corrected_sentences = self.tokenizer.batch_decode(predicts, skip_special_tokens=True)

        if self.concat:
            output_sentence = self._concatenate_sentences()
            self.spelling_correction_duration = time.time() - correct_spelling_start_time
            return output_sentence
        else:
            self.spelling_correction_duration = time.time() - correct_spelling_start_time
            return self.spelling_corrected_sentences

