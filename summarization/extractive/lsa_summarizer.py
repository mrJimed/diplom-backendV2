import math
import re

import numpy as np
import pymorphy3
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from numpy.linalg import svd


class LsaSummarizer:
    @staticmethod  # Суммаризация текста
    def summarize_text(text: str, top_n: int, lemmatize: bool = True) -> str:
        orig_text = re.sub(r'\s+', ' ', text)
        orig_sentences = [sentence for sentence in sent_tokenize(orig_text)]
        preprocessed_sentences = [LsaSummarizer._text_preprocessing(sentence, lemmatize) for sentence in orig_sentences]
        unique_words = set()
        for sentence_words in preprocessed_sentences:
            unique_words.update(sentence_words)
        word_index = {word: idx for idx, word in enumerate(unique_words)}
        matrix = LsaSummarizer._create_matrix(preprocessed_sentences, word_index)
        matrix = LsaSummarizer._normalization_matrix(matrix)
        _, sigma, v_matrix = svd(matrix, full_matrices=False)
        min_length = max(3, top_n)
        weight_topics = [s ** 2 for s in sigma[:min_length]]
        scores = []
        for sentence_column in v_matrix.T:
            sentence_column = sentence_column[:min_length]
            score = math.sqrt(sum(wt * sc ** 2 for wt, sc in zip(weight_topics, sentence_column)))
            scores.append(score)
        ordered_indices_score = [idx for idx in range(len(orig_sentences))]
        ordered_indices_score = [idx for _, idx in sorted(zip(scores, ordered_indices_score), reverse=True)]
        ordered_indices_score = ordered_indices_score[:top_n]
        return " ".join([orig_sentences[idx] for idx in ordered_indices_score])

    @staticmethod  # Нормализация матрицы
    def _normalization_matrix(matrix: np.ndarray) -> np.ndarray:
        max_word_frequencies = np.max(matrix, axis=0)
        rows, columns = matrix.shape
        for row in range(rows):
            for column in range(columns):
                max_word_frequency = max_word_frequencies[column]
                if max_word_frequency != 0:
                    matrix[row, column] /= max_word_frequency
        return matrix

    @staticmethod  # Создание матрицы слов и предложений
    def _create_matrix(sentences: list[list[str]], words: dict[str:int]) -> np.ndarray:
        words_count = len(words)
        sentences_count = len(sentences)
        matrix = np.zeros((words_count, sentences_count))
        for column, sentence in enumerate(sentences):
            for word in sentence:
                row = words[word]
                matrix[row, column] += 1
        return matrix

    @staticmethod  # Лемматизация текста
    def _lemmatized_text(sentence: list[str]) -> list[str]:
        morph = pymorphy3.MorphAnalyzer()
        lemmatized_words = []
        for word in sentence:
            normal_form = morph.parse(word.lower())[0].normal_form
            lemmatized_words.append(normal_form)
        return lemmatized_words

    @staticmethod  # Предобработка текста
    def _text_preprocessing(sentence: str, lemmatize: bool) -> list[str]:
        stop_words = set(stopwords.words('russian'))
        clear_sentence = re.sub(r'[^\w\s]', '', sentence.lower())
        clear_sentence = [word for word in word_tokenize(clear_sentence) if word not in stop_words]
        if lemmatize:
            return LsaSummarizer._lemmatized_text(clear_sentence)
        return clear_sentence
