import urllib.request
import pandas as pd
from normalizer import DocumentsPreprocessing
import matrix

education_links = ['https://programs.edu.urfu.ru/ru/8516/', 'https://programs.edu.urfu.ru/ru/10216/',
                   'https://programs.edu.urfu.ru/ru/8510/',
                   'https://programs.edu.urfu.ru/ru/9813/', 'https://programs.edu.urfu.ru/ru/8512/',
                   'https://programs.edu.urfu.ru/ru/9795/', 'https://programs.edu.urfu.ru/ru/8986/',
                   'https://programs.edu.urfu.ru/ru/9021/', 'https://programs.edu.urfu.ru/ru/8522/',
                   'https://programs.edu.urfu.ru/ru/8541/',
                   'https://programs.edu.urfu.ru/ru/8562/', 'https://programs.edu.urfu.ru/ru/8655/',
                   'https://programs.edu.urfu.ru/ru/9082/', 'https://programs.edu.urfu.ru/ru/9797/',
                   'https://programs.edu.urfu.ru/ru/9812/', 'https://programs.edu.urfu.ru/ru/9936/',
                   'https://programs.edu.urfu.ru/ru/9846/']


def extract_education(links):
    educations = []
    for link in links:
        req = urllib.request.Request(link, method="GET")
        educations.append(urllib.request.urlopen(req).read().decode())
    return educations


ed_descriptions = pd.read_csv('ed.csv')['ed_description']
term, documents_matrix = matrix.DocumentMatrixBuilder(min_df=0.001, max_df=0.999).build_matrix(
    ed_descriptions)
matrix.save_matrix_and_terms(term, documents_matrix, file_name='./ed_matrix')
