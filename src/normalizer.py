import datetime
import string

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize


class DocumentsNormalizer:
    def __init__(self, normalization_algorithm=None, token_len_min=0, should_log=False):
        self._stop_words = []
        self.__read_stop_words()
        self._token_len_min = token_len_min
        self.should_log = should_log

    def normalize_documents(self, docs):
        self.log('start normalization ')
        html_free_docs = docs.apply(self.__extract_row_text_from_html)
        self.log('end extract tow text from html')
        punctuation_free_docs = html_free_docs.apply(self.__remove_punctuation)
        self.log('end of removing  punctuation ')
        tokens_collections = punctuation_free_docs.apply(lambda x: word_tokenize(x.lower()))
        self.log('end tokenize')
        a = self.__remove_noise(tokens_collections)
        self.log('end of removing noise')
        return a.apply(lambda _tokens: " ".join(_tokens))

    def __remove_noise(self, token_collections):
        return token_collections.apply(
            lambda collection: list(filter(
                lambda token: token not in self._stop_words and not token.isdigit() and len(
                    token) >= self._token_len_min,
                collection)))

    def log(self, message):
        if not self.should_log:
            return
        now = datetime.datetime.now()
        print("{0} - {1}".format(now.strftime("%Y-%m-%d %H:%M:%S"), message))
        return

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
        with open('./ru_stop_words.txt', mode='r', encoding='utf-8') as f:
            raw_stop_words = f.readlines()
            for stop_word in raw_stop_words:
                self._stop_words.append(stop_word.strip())
