import datetime
import string

import nltk
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from pymorphy2.tagset import OpencorporaTag
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords

from logger import log
import pymorphy2


class DocumentsNormalizer:
    def __init__(self, token_len_min=0, should_log=False, sub_text_extractor=None):
        self._stop_words = []
        self.__read_stop_words()
        self._token_len_min = token_len_min
        self.should_log = should_log
        self.analyzer = pymorphy2.MorphAnalyzer()
        self.ignore = ['COMP', 'INFN', 'NUMR', 'PRED', 'PRCL', 'PRTF', 'PRTS', 'GRND']
        self.sub_text_extractor = sub_text_extractor

    def normalize_documents(self, docs):
        log('start normalization')
        html_free_docs = docs.apply(self.__extract_row_text_from_html)
        log('end extract tow text from html')
        punctuation_free_docs = html_free_docs.apply(self.__remove_punctuation)
        if self.sub_text_extractor is not None:
            extracted_sub_text = punctuation_free_docs.apply(self.sub_text_extractor)[punctuation_free_docs != '']
            punctuation_free_docs = extracted_sub_text[extracted_sub_text != '']
        log('end of removing  punctuation ')
        tokens_collections = punctuation_free_docs.apply(lambda x: word_tokenize(x.lower()))
        log('end tokenize')
        a = self.__remove_noise(tokens_collections.apply(self.__lemmatize))
        log('end of removing noise')
        return a.apply(lambda _tokens: " ".join(_tokens))

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


def create_frequency_table(documents, min_df=0.05, max_df=0.99, sub_text_extractor=None):
    normalizer = DocumentsNormalizer(should_log=True, sub_text_extractor=sub_text_extractor)
    corpus = normalizer.normalize_documents(documents)

    vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, dtype=np.float64)
    frequency_table = vectorizer.fit_transform(corpus)
    return vectorizer.get_feature_names(), frequency_table


def save_frequency_table(terms, frequency_table, file_name='./frequency_table'):
    sparse.save_npz(file_name, frequency_table)
    with open('./terms', 'w', encoding='utf-8') as f:
        f.write('\n'.join(terms))


def print_topics(count_related_words, components, terms):
    for i, comp in enumerate(components):
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:count_related_words]
        topic = "Topic " + str(i) + ": "
        for sorted_term in sorted_terms:
            topic = topic + sorted_term[0] + ' '
        print(topic)


def read_frequency_table(file_name='./frequency_table.npz'):
    frequency_table = sparse.load_npz(file_name)
    terms = []
    with open('./terms', 'r', encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            terms.append(i.strip())
    return frequency_table, terms
