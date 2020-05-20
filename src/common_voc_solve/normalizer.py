import string

import pymorphy2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymorphy2.tagset import OpencorporaTag


class DocumentsPreprocessing:
    def __init__(self, token_len_min=0):
        self._stop_words = []
        self.__read_stop_words()
        self._token_len_min = token_len_min
        self.analyzer = pymorphy2.MorphAnalyzer()
        self.ignore = ['COMP', 'INFN', 'NUMR', 'PRED', 'PRCL', 'PRTF', 'PRTS', 'GRND']

    def clean_docs(self, docs):
        html_free_docs = docs.apply(self.__extract_row_text_from_html)
        return html_free_docs.apply(self.__remove_punctuation).apply(lambda x: " ".join(x.lower().split()))

    def normalize_docs(self, docs):
        tokens_collections = docs.apply(word_tokenize)
        removed_noise_docs = self.__remove_noise(tokens_collections.apply(self.__lemmatize))
        return removed_noise_docs.apply(lambda _tokens: " ".join(_tokens))

    def __remove_noise(self, token_collections):
        return token_collections.apply(
            lambda collection: list(filter(
                lambda token: token not in self._stop_words and not token.isdigit() and len(
                    token) >= self._token_len_min,
                collection)))

    @staticmethod
    def __to_dict(tokens):
        unique_tokens = {}
        for token in tokens:
            if token in unique_tokens:
                unique_tokens[token] += 1
            else:
                unique_tokens[token] = 1
        return unique_tokens

    @staticmethod
    def __extract_row_text_from_html(text):
        soup = BeautifulSoup(text, 'html.parser')
        html_free = soup.get_text(strip=True, separator=' ')
        return html_free

    @staticmethod
    def __remove_punctuation(text):
        chars = []
        for char in text:
            if char in string.punctuation:
                chars.append(' ')
            else:
                chars.append(char)
        return "".join(chars)

    def __read_stop_words(self):
        english_stop_words = stopwords.words("english")
        with open('./ru_stop_words.txt', mode='r', encoding='utf-8') as f:
            raw_stop_words = f.readlines()
            for stop_word in raw_stop_words:
                self._stop_words.append(stop_word.strip())
        self._stop_words = self._stop_words + english_stop_words

    def __lemmatize(self, words):
        row = []
        for word in words:
            p = max(self.analyzer.parse(word), key=lambda x: x.score)
            if p.tag == OpencorporaTag('LATN'):
                row.append(word)
                continue
            if p.tag.POS in self.ignore:
                continue
            row.append(p.normal_form)
        return row
