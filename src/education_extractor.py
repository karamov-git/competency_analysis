import pandas as pd
from normalizer import DocumentsPreprocessing
import matrix
from documents_provider import EducationDocumentsProvider

skills_mark_words = [('планируемые результаты обучения по дисциплине', '1 4 объем дисциплины'),
                     ('содержание дисциплины', '3 распределение учебного времени')]


def extract(doc, mark_sent):
    mark_start, mark_end = mark_sent
    start_position = doc.find(mark_start)
    end_position = doc.find(mark_end)
    if start_position == -1 or end_position == -1 or start_position > end_position:
        return ''
    return doc[start_position + len(mark_start): end_position] + extract(doc[end_position + len(mark_end):], mark_sent)


def education_skills_extractor(document):
    result = extract(document, skills_mark_words[0])
    content = extract(document, skills_mark_words[1])
    return ' '.join([result, content])


data_set = pd.read_csv('./ed.csv')
documents = data_set['documents']

term, documents_matrix = matrix.DocumentMatrixBuilder(min_df=0.001, max_df=0.999,
                                                      sub_text_extractor=education_skills_extractor).build_matrix(
    documents)
matrix.save_matrix_and_terms(term, documents_matrix, './ed_matrix')
