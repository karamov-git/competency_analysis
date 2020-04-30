import normalizer
import pandas as pd

requirements_start_words = ['Требования', 'Твой функционал', 'Что мы ожидаем от вас', 'Нам важно',
                            'Что хотим от тебя',
                            'Вы нам подходите если', 'От вас', 'От тебя', 'Необходимые знания и навыки',
                            'Что нужно знать/уметь'
    , 'Что ждем от кандидата', 'Профессиональные навыки', 'Ключевые умения', 'Что мы ожидаем от кандидата',
                            'Необходимы', 'Наши ожидания']
requirements_stop_words = ['Условия', 'Что мы предлагаем', 'Что мы за это предлагаем', 'Преимущества работы у нас'
    , 'Что у нас есть', 'Мы предлагаем', 'Что предлагаем', 'Мы гарантируем']

global c
from bs4 import BeautifulSoup

def count(documents):
    unique = {i: 0 for i in requirements_start_words + requirements_stop_words}
    c = 0

    def count_int_document(row):
        soup = BeautifulSoup(row, 'html.parser')
        html_free = soup.get_text(strip=True, separator=' ')
        for start_word in requirements_start_words:
            for stop_word in requirements_stop_words:
                start_position = html_free.find(start_word)
                stop_position = html_free.find(stop_word)
                if stop_position > start_position:
                    unique[start_word] += 1
                    unique[stop_word] += 1
                    return 1
        return 0

    for index, document in documents.items():
        c = c + count_int_document(document)
    print(c)
    print(len(documents))
    print(unique)


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
count(documents)

# terms, frequency_table = normalizer.create_frequency_table(documents, min_df=0.005, max_df=0.98)
# normalizer.save_frequency_table(terms, frequency_table)
