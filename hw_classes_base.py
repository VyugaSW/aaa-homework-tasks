# -*- coding: utf-8 -*-
import math


# Реализация класса взята с практики
class CountVectorizer:
    def __init__(self, lowercase=True, ngram_size=1):
        self._vocabulary = {}
        self.lowercase = lowercase
        if ngram_size < 1:
            raise ValueError('ERROR: ngram_size may not be less than 1.')

        self.ngram_size = ngram_size
        self.curr_i = 0

    @property
    def vocabulary(self):
        return self._vocabulary

    @vocabulary.setter
    def vocabulary(self, new_vocabulary):
        if not isinstance(new_vocabulary, dict):
            raise TypeError('ERROR: vocabulary must be a dict.')

        self._vocabulary = new_vocabulary
        self.curr_i = max(new_vocabulary.values()) + 1 if new_vocabulary else 0

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}
        self.curr_i = 0

    def to_dict(self):
        return {
            'lowercase': self.lowercase,
            'ngram_size': self.ngram_size,
            'vocabulary': self.vocabulary.copy(),
        }

    @classmethod
    def from_dict(cls, vectorizer_state):
        if not isinstance(vectorizer_state, dict):
            raise TypeError('ERROR: state must be a dictionary.')

        vectorizer = cls(
            lowercase=vectorizer_state['lowercase'],
            ngram_size=vectorizer_state['ngram_size']
        )
        vectorizer.vocabulary = vectorizer_state['vocabulary'].copy()

        return vectorizer

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        words = text.split()

        return [
            ' '.join(words[i:i + self.ngram_size])
            for i in range(len(words) - self.ngram_size + 1)
        ]

    def add_word(self, word):
        if word in self._vocabulary:
            return self._vocabulary[word]

        self._vocabulary[word] = self.curr_i
        self.curr_i += 1

        return self.curr_i - 1

    def get_feature_names(self):
        return list(self._vocabulary.keys())

    def fit(self, text):
        if not text or not any(self.tokenize(line) for line in text):
            raise ValueError('ERROR: text has no tokens.')

        self._vocabulary = {}
        self.curr_i = 0
        for line in text:
            for token in self.tokenize(line):
                self.add_word(token)

    def transform(self, text):
        if not self._vocabulary:
            raise RuntimeError("ERROR: fit isn't initialized.")

        counts_matrix = []
        for line in text:
            tokens = self.tokenize(line)
            line_counts = [0] * len(self._vocabulary)

            for token in tokens:
                if token in self._vocabulary:
                    line_counts[self._vocabulary[token]] += 1

            counts_matrix.append(line_counts)

        return counts_matrix

    def fit_transform(self, text):
        self.fit(text)
        return self.transform(text)


class TfidfVectorizer(CountVectorizer):
    def __init__(self, lowercase=True, ngram_size=1, use_idf=True):
        super().__init__(lowercase=lowercase, ngram_size=ngram_size)
        self.use_idf = use_idf
        self._idf = []
        self._n_docs = 0

    @classmethod
    def from_config(cls, config):
        if not isinstance(config, dict):
            raise TypeError('ERROR: config must be a dictionary.')

        lowercase = config.get('lowercase', True)
        use_idf = config.get('use_idf', True)

        return cls(lowercase=lowercase, use_idf=use_idf)

    @property
    def idf(self):
        return self._idf.copy()

    def fit(self, text):
        if not text or not any(self.tokenize(line) for line in text):
            raise ValueError('ERROR: text has no tokens.')

        self._vocabulary = {}
        self.curr_i = 0
        self._idf = []
        self._n_docs = len(text)

        doc_tokens = []
        for doc in text:
            tokens = self.tokenize(doc)
            doc_tokens.append(set(tokens))
            for token in tokens:
                self.add_word(token)

        if self.use_idf:
            self._idf = [0] * len(self._vocabulary)
            for word, idx in self._vocabulary.items():
                df = sum(1 for tokens in doc_tokens if word in tokens)
                self._idf[idx] = math.log((self._n_docs + 1) / (df + 1)) + 1

    def transform(self, text):
        if not self._vocabulary:
            raise RuntimeError("ERROR: fit isn't initialized.")

        tfidf_matrix = []
        for line in text:
            tokens = self.tokenize(line)
            line_counts = [0] * len(self._vocabulary)
            known_words_count = 0

            for token in tokens:
                if token in self._vocabulary:
                    line_counts[self._vocabulary[token]] += 1
                    known_words_count += 1

            if known_words_count > 0:
                for i in range(len(line_counts)):
                    tf = line_counts[i] / known_words_count
                    if self.use_idf:
                        line_counts[i] = tf * self._idf[i]
                    else:
                        line_counts[i] = tf
            else:
                line_counts = [0] * len(self._vocabulary)

            tfidf_matrix.append(line_counts)

        return tfidf_matrix


class KeywordExtractor:
    def __init__(self, vectorizer, top_n=3):
        self.vectorizer = vectorizer
        self.top_n = top_n

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, new_top_n):
        if not isinstance(new_top_n, int) or new_top_n <= 0:
            raise ValueError('ERROR: top_n must be a positive integer.')

        self._top_n = new_top_n

    def fit(self, text):
        self.vectorizer.fit(text)
        return self

    def extract(self, text):
        matrix = self.vectorizer.transform(text)
        feature_names = self.vectorizer.get_feature_names()
        extracted_keywords = []
        for row in matrix:
            word_weights = []
            for i, weight in enumerate(row):
                if weight > 0:
                    word_weights.append((feature_names[i], weight))

            word_weights.sort(key=lambda x: (-x[1], x[0]))
            extracted_keywords.append(word_weights[: self._top_n])

        return extracted_keywords


TRAIN_CORPUS = [
    'Марс сигнал сигнал',
    'Марс пыль',
    'Марс сигнал антенна',
]

CHECK_CORPUS = [
    'СИГНАЛ шум сигнал',
    'антенна пыль',
    'марс марс марс',
    'комета',
    ''
]


def demo():
    print('--Сценарий 1')
    tfidf = TfidfVectorizer.from_config({})
    matrix1 = tfidf.fit_transform(TRAIN_CORPUS)
    print(tfidf.get_feature_names())

    current_idf = tfidf.idf
    print(current_idf)
    print(matrix1)

    current_idf.clear()
    print(tfidf.idf)

    print('\n--Сценарий 2')
    tf = TfidfVectorizer.from_config({'lowercase': False, 'use_idf': False})
    scenario2_corpus = ['Марс марс', 'МАРС сигнал']

    matrix2 = tf.fit_transform(scenario2_corpus)
    print(tf.get_feature_names())
    print(tf.idf)
    print(matrix2)

    tfidf.fit(['Венера облака'])
    print(tfidf.get_feature_names())
    print(tfidf.idf)
    print(tfidf.transform(['Марс Венера облака']))

    print('\n--Сценарий 3')
    extractor = KeywordExtractor(tfidf, top_n=2)
    extractor.fit(TRAIN_CORPUS)

    print(extractor.extract(CHECK_CORPUS))

    extractor.top_n = 1
    print(extractor.extract(CHECK_CORPUS))

    try:
        extractor.top_n = 0
    except ValueError as e:
        print('ValueError:', e)


if __name__ == '__main__':
    demo()
