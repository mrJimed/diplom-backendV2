import re
from collections import Counter

import nltk
import numpy as np
import pymorphy3
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize


class LexRankSummarizer:
    @staticmethod  # Суммаризация текста
    def summarize_text(text: str, top_n: int, lemmatize: bool = True) -> str:
        orig_text = re.sub(r'\s+', ' ', text)
        orig_sentences = sent_tokenize(orig_text)
        preprocessed_sentences = LexRankSummarizer._preprocess_text(orig_text, lemmatize)
        similarity_matrix = LexRankSummarizer._build_similarity_matrix(preprocessed_sentences)
        scores = LexRankSummarizer._lexrank(similarity_matrix)
        ranked_sentences = [(score, sentence) for score, sentence in zip(scores, orig_sentences)]
        ranked_sentences.sort(reverse=True)
        top_sentences = ranked_sentences[:top_n]
        summarized_sentences = [sentence for _, sentence in top_sentences]
        return ' '.join(summarized_sentences)

    @staticmethod  # Лемматизация текста
    def _lemmatized_text(sentences: list[str]) -> list[str]:
        morph = pymorphy3.MorphAnalyzer()
        lemmatized_sentences = []
        for sentence in sentences:
            lemmatized_words = []
            for word in nltk.word_tokenize(sentence):
                normal_form = morph.parse(word.lower())[0].normal_form
                lemmatized_words.append(normal_form)
            lemmatized_sentence = ' '.join(lemmatized_words)
            lemmatized_sentences.append(lemmatized_sentence)
        return lemmatized_sentences

    @staticmethod  # Предобработка текста
    def _preprocess_text(text: str, lemmatize: bool) -> list[str]:
        sentences = sent_tokenize(text)
        stop_words = set(stopwords.words('russian'))
        clean_sentences = [re.sub(r'[^\w\s]', '', sentence) for sentence in sentences]
        clean_sentences = [sentence.lower() for sentence in clean_sentences if sentence.lower() not in stop_words]
        if lemmatize:
            return LexRankSummarizer._lemmatized_text(clean_sentences)
        return clean_sentences

    @staticmethod  # Создание матрицы сходства между предложениями на основе косинусного сходства слов
    def _build_similarity_matrix(sentences: list[str]) -> np.ndarray:
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        for i, sentence1 in enumerate(sentences):
            for j, sentence2 in enumerate(sentences):
                if i != j:
                    similarity_matrix[i][j] = LexRankSummarizer._compute_cosine_similarity(sentence1, sentence2)
        return similarity_matrix

    @staticmethod  # Вычисление косинусного сходства между двумя предложениями.
    def _compute_cosine_similarity(sentence1: str, sentence2: str) -> float:
        vector1 = Counter(sentence1.split())
        vector2 = Counter(sentence2.split())
        intersection = set(vector1.keys()) & set(vector2.keys())
        numerator = sum([vector1[word] * vector2[word] for word in intersection])
        sum1 = sum([vector1[word] ** 2 for word in vector1.keys()])
        sum2 = sum([vector2[word] ** 2 for word in vector2.keys()])
        denominator = np.sqrt(sum1) * np.sqrt(sum2)
        if not denominator:
            return 0.0
        return float(numerator) / denominator

    @staticmethod  # Алгоритм LexRank
    def _lexrank(similarity_matrix: np.ndarray, damping_factor: float = 0.85, max_iter: int = 100,
                 tol: float = 0.001) -> np.ndarray:
        n = similarity_matrix.shape[0]
        matrix = np.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1.0
            for j in range(n):
                if np.sum(similarity_matrix[j]) != 0:
                    matrix[i, j] = damping_factor * similarity_matrix[i, j] / np.sum(similarity_matrix[j])
                else:
                    matrix[i, j] = 0.0

        lr = np.ones(n) / n
        for _ in range(max_iter):
            old_lr = np.copy(lr)
            lr = (1 - damping_factor) + damping_factor * np.dot(matrix, lr)
            if np.linalg.norm(lr - old_lr) < tol:
                break
        return lr
