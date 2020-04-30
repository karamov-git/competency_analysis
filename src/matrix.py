import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from normalizer import DocumentsPreprocessing


class DocumentMatrixBuilder:

    def __init__(self, min_df=0.05, max_df=0.99, sub_text_extractor=None):
        self.prepocessor = DocumentsPreprocessing()
        self.min_df = min_df
        self.max_df = max_df
        self.sub_text_extractor = sub_text_extractor

    def build_matrix(self, documents):
        cleaned_documents = self.prepocessor.clean_docs(documents)
        needed_sub_documents = cleaned_documents.apply(self.sub_text_extractor)
        corpus = self.prepocessor.normalize_docs(needed_sub_documents[needed_sub_documents != ''])
        vectorizer = TfidfVectorizer(min_df=self.min_df, max_df=self.max_df, dtype=np.float64)
        matrix = vectorizer.fit_transform(corpus)
        return vectorizer.get_feature_names(), matrix


def save_matrix_and_terms(terms, matrix, file_name='./matrix'):
    sparse.save_npz(file_name, matrix)
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


def read_matrix(file_name='./matrix.npz'):
    frequency_table = sparse.load_npz(file_name)
    terms = []
    with open('./terms', 'r', encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            terms.append(i.strip())
    return frequency_table, terms
