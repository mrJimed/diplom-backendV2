import re
from collections import Counter, defaultdict

import nltk
import pymorphy3
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize


class TextRankSummarizer:
    @staticmethod  # Суммаризация текста
    def summarize_text(text: str, top_n: int, lemmatize: bool = True) -> str:
        orig_text = re.sub(r'\s+', ' ', text)
        orig_sentences = sent_tokenize(orig_text)
        preprocessed_sentences = TextRankSummarizer._preprocess_text(orig_text, lemmatize)
        graph = TextRankSummarizer._build_graph(preprocessed_sentences)
        tr = TextRankSummarizer._textrank(graph)
        top_n_sentences = sorted(tr.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return ' '.join([orig_sentences[i] for i, _ in top_n_sentences])

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
            return TextRankSummarizer._lemmatized_text(clean_sentences)
        return clean_sentences

    @staticmethod  # Построение графа предложений
    def _build_graph(sentences: list[str]) -> defaultdict:
        graph = defaultdict(list)
        for i, sentence1 in enumerate(sentences):
            for j, sentence2 in enumerate(sentences):
                if i != j:
                    common_words = set(sentence1.split()) & set(sentence2.split())
                    if common_words:
                        graph[i].append((j, len(common_words)))
        return graph

    @staticmethod  # Вычисление весов вершин графа
    def _calculate_weights(graph: defaultdict) -> Counter:
        weights = Counter()
        for word, edges in graph.items():
            for _, weight in edges:
                weights[word] += weight
        return weights

    @staticmethod  # Алгоритм TextRank
    def _textrank(graph: defaultdict, iterations: int = 10) -> dict:
        n = len(graph)
        tr = {node: 1.0 / n for node in graph}
        damping_factor = 0.85

        for _ in range(iterations):
            new_tr = defaultdict(float)
            for node in graph:
                for neighbor, weight in graph[node]:
                    new_tr[neighbor] += damping_factor * tr[node] / len(graph[node])
            tr = new_tr

        return tr
