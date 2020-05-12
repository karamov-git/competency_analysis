import pandas as pd

requirements_stop_words = ['условия', 'преимущества работы', 'у нас есть', 'предлагаем', 'гарантируем', 'нужно будет']
requirements_start_words = ['Требования', 'Твой функционал', 'мы ожидаем', 'хотим от', 'вас', 'тебя', 'нужно знать',
                            'нужно уметь', 'Ключевые умения', 'ожидания']
from normalizer import DocumentsPreprocessing
import matrix


def count_documents_with_requirement(documents):
    requirements = {i: 0 for i in requirements_start_words + requirements_stop_words}
    count = 0
    cleaned_documents = DocumentsPreprocessing().clean_docs(documents)

    def count_requirements_in(document):
        for start_word in requirements_start_words:
            for stop_word in requirements_stop_words:
                start_position = document.find(start_word.lower())
                stop_position = document.find(stop_word.lower())
                if stop_position > start_position:
                    requirements[start_word] += 1
                    requirements[stop_word] += 1
                    return 1
        return 0

    for index, document in cleaned_documents.items():
        count = count + count_requirements_in(document)
    return count, requirements


def hh_vacancy_requirements_extractor(row):
    for start_word in requirements_start_words:
        for stop_word in requirements_stop_words:
            start_position = row.find(start_word)
            stop_position = row.find(stop_word)
            if stop_position > start_position:
                return row[start_position + len(start_word): stop_position]
    return ''


data_set = pd.read_csv('./merged.csv')
documents = data_set['description']

term, documents_matrix = matrix.DocumentMatrixBuilder(min_df=0.001, max_df=0.999,
                                                      sub_text_extractor=hh_vacancy_requirements_extractor).build_matrix(
    documents)
matrix.save_matrix_and_terms(term, documents_matrix)
