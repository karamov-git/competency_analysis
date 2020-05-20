import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from normalizer import DocumentsPreprocessing


class DocumentMatrixBuilder:
    def __init__(self):
        self.prepocessor = DocumentsPreprocessing()

    def get_prepocessing_text_and_vocabulary(self, documents, min_df=0.005,max_df=0.99, sub_text_extractor=None):
        if sub_text_extractor is None:
            sub_text_extractor = self.__stub
        cleaned_documents = self.prepocessor.clean_docs(documents)
        needed_sub_documents = cleaned_documents.apply(sub_text_extractor)
        corpus = self.prepocessor.normalize_docs(needed_sub_documents[needed_sub_documents != ''])
        vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, dtype=np.float64)
        vectorizer.fit(corpus)
        return corpus, vectorizer.vocabulary_

    def transform_and_get_vectorizer(self, documents, min_df=0.005,max_df=0.99, sub_text_extractor=None):
        if sub_text_extractor is None:
            sub_text_extractor = self.__stub
        cleaned_documents = self.prepocessor.clean_docs(documents)
        needed_sub_documents = cleaned_documents.apply(sub_text_extractor)
        corpus = self.prepocessor.normalize_docs(needed_sub_documents[needed_sub_documents != ''])
        vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, dtype=np.float64)
        res = vectorizer.fit_transform(corpus)
        return res, vectorizer


    def build_matrix_from_corpus_and_vocabulary(self, corpus, addition_vocabulary):
        vectorizer = TfidfVectorizer(vocabulary=addition_vocabulary, dtype=np.float64)
        matrix = vectorizer.fit_transform(corpus)
        return matrix, vectorizer.get_feature_names()

    def build_matrix(self, documents, sub_text_extractor, min_df=0.05, max_df=0.99):
        cleaned_documents = self.prepocessor.clean_docs(documents, )
        needed_sub_documents = cleaned_documents.apply(sub_text_extractor)
        corpus = self.prepocessor.normalize_docs(needed_sub_documents[needed_sub_documents != ''])
        vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, dtype=np.float64)
        matrix = vectorizer.fit_transform(corpus)
        return vectorizer.get_feature_names(), matrix

    def __stub(self, x):
        return x


def save_matrix_and_terms(terms, matrix, file_name='./matrix'):
    sparse.save_npz(file_name, matrix)
    with open('{}_terms'.format(file_name), 'w', encoding='utf-8') as f:
        f.write('\n'.join(terms))


def print_topics(count_related_words, components, terms):
    for i, comp in enumerate(components):
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:count_related_words]
        topic = "Topic " + str(i) + ": "
        for sorted_term in sorted_terms:
            topic = topic + sorted_term[0] + ' '
        print(topic)


def read_matrix(file_name='./matrix'):
    frequency_table = sparse.load_npz('{}.npz'.format(file_name))
    terms = []
    with open('{}_terms'.format(file_name), 'r', encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            terms.append(i.strip())
    return frequency_table, terms
