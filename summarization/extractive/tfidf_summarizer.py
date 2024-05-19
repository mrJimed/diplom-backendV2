import re
from collections import defaultdict
from typing import Any

import nltk
import pymorphy3
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfSummarizer:
    @staticmethod  # Суммаризация текста
    def summarize_text(text: str, top_n: int, lemmatize: bool = True) -> str:
        orig_text = re.sub(r'\s+', ' ', text)
        orig_sentences = nltk.sent_tokenize(orig_text)
        preprocessed_sentences = []
        for sentence in orig_sentences:
            preprocessed_sentences.append(TfidfSummarizer._text_preprocessing(sentence, lemmatize))
        weighted_word_frequency = TfidfSummarizer._get_weighted_word_frequency(preprocessed_sentences)
        sentences_scores = defaultdict(float)
        for preprocessed_sentence, orig_sentence in zip(preprocessed_sentences, orig_sentences):
            for word in nltk.word_tokenize(preprocessed_sentence):
                if word in weighted_word_frequency.keys():
                    sentences_scores[orig_sentence] += weighted_word_frequency[word]
        selected_sentences = sorted(sentences_scores.keys(), key=lambda x: sentences_scores[x], reverse=True)[
                             :top_n]
        return ' '.join(selected_sentences)

    @staticmethod  # Лемматизация текста
    def _lemmatized_text(sentence: str) -> str:
        morph = pymorphy3.MorphAnalyzer()
        lemmatized_words = []
        for word in nltk.word_tokenize(sentence):
            normal_form = morph.parse(word.lower())[0].normal_form
            lemmatized_words.append(normal_form)
        return ' '.join(lemmatized_words)

    @staticmethod  # Предобработка текста
    def _text_preprocessing(sentence: str, lemmatize: bool) -> str:
        stop_words = set(stopwords.words('russian'))
        clear_sentence = re.sub(r'[^\w\s]', '', sentence.lower())
        clear_sentence = ' '.join([word for word in nltk.word_tokenize(clear_sentence) if word not in stop_words])
        if lemmatize:
            return TfidfSummarizer._lemmatized_text(clear_sentence)
        return clear_sentence

    @staticmethod  # Подсчёт частоты употребления для каждого слова
    def _get_weighted_word_frequency(sentences: list[str]) -> defaultdict[Any, float]:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()
        word_scores = defaultdict(float)
        for i, sentence in enumerate(sentences):
            feature_index = tfidf_matrix[i, :].nonzero()[1]
            for idx in feature_index:
                word = feature_names[idx]
                word_scores[word] += tfidf_matrix[i, idx]
        return word_scores
