import urllib.request

import pandas as pd
import slate3k as slate
import logger


class EducationDocumentsProvider:

    def __init__(self):
        self._education_program_urls = {
            'Безопасность сетевых технологий' : 'https://programs.edu.urfu.ru/media/rpm/00031837.pdf',
            'Безопасные автоматизированные системы':'https://programs.edu.urfu.ru/media/rpm/00031826.pdf',
            'Информационное кодирование':'https://programs.edu.urfu.ru/media/rpm/00031825.pdf',
            'Информационные технологии':'https://programs.edu.urfu.ru/media/rpm/00032488.pdf',
            'Методы и средства защиты документооборота' : 'https://programs.edu.urfu.ru/media/rpm/00031842.pdf',
            'Программно-алгоритмическое обеспечение информационной безопасности':'https://programs.edu.urfu.ru/media/rpm/00031827.pdf',
            'Анализ предметной области':'https://programs.edu.urfu.ru/media/rpm/00028624.pdf',
            'Базы данных и знаний':'https://programs.edu.urfu.ru/media/rpm/00028561.pdf',
            'Графические приложения':'https://programs.edu.urfu.ru/media/rpm/00028583.pdf',
            'Информационно-управляющие системы':'https://programs.edu.urfu.ru/media/rpm/00030707.pdf',
            'Концепции современного программирования':'https://programs.edu.urfu.ru/media/rpm/00028557.pdf',
            'Корпоративные информационные системы':'https://programs.edu.urfu.ru/media/rpm/00028666.pdf',
            'Многоуровневые и мобильные приложения':'https://programs.edu.urfu.ru/media/rpm/00028580.pdf',
            'Основы информационных процессов':'https://programs.edu.urfu.ru/media/rpm/00028562.pdf',
            'Проектирование микропроцессорных систем':'https://programs.edu.urfu.ru/media/rpm/00031158.pdf',
            'Промышленные базы данных':'https://programs.edu.urfu.ru/media/rpm/00028663.pdf',
            'Современные сетевые технологии':'https://programs.edu.urfu.ru/media/rpm/00028553.pdf',
            'Средства и технологии разработки программного обеспечения':'https://programs.edu.urfu.ru/media/rpm/00025161.pdf',
            'Базы данных и интеллектуальные системы':'https://programs.edu.urfu.ru/media/rpm/00029974.pdf',
            'Интеллектуальные методы анализа информации':'https://programs.edu.urfu.ru/media/rpm/00029983.pdf',
            'Интернет-технологии':'https://programs.edu.urfu.ru/media/rpm/00029978.pdf',
            'Методы анализа Big Data':'https://programs.edu.urfu.ru/media/rpm/00029984.pdf',
            'Управление проектами информационных систем':'https://programs.edu.urfu.ru/media/rpm/00029991.pdf',
            'Администрирование информационных систем':'https://programs.edu.urfu.ru/media/rpm/00030238.pdf',
            'Реальное программирование':'https://programs.edu.urfu.ru/media/rpm/00029418.pdf',
            'Эффективное программирование':'https://programs.edu.urfu.ru/media/rpm/00029427.pdf',
            'Программирование':'https://programs.edu.urfu.ru/media/rpm/00024682.pdf',
            'Теория программирования':'https://programs.edu.urfu.ru/media/rpm/00024644.pdf',
            'Машинная графика':'https://programs.edu.urfu.ru/media/rpm/00032292.pdf',
            'Менеджмент в информационных технологиях' : 'https://programs.edu.urfu.ru/media/rpm/00032287.pdf',
            'Основания информатики и программирования':'https://programs.edu.urfu.ru/media/rpm/00032278.pdf',
            'Программное обеспечение информационных систем':'https://programs.edu.urfu.ru/media/rpm/00032279.pdf',
            'Технологии разработки Web-приложений':'https://programs.edu.urfu.ru/media/rpm/00032284.pdf',
            'Языки логического программирования':'https://programs.edu.urfu.ru/media/rpm/00031689.pdf',
            'Моделирование бизнес-процессов' : 'https://programs.edu.urfu.ru/media/rpm/00027742.pdf',
            'Обеспечение качества и тестирование программного обеспечения':'https://programs.edu.urfu.ru/media/rpm/00027745.pdf',
            'Проектирование интерфейсов':'https://programs.edu.urfu.ru/media/rpm/00027749.pdf',
            'Разработка программного обеспечения':'https://programs.edu.urfu.ru/media/rpm/00027747.pdf',
        }
        print(len(self._education_program_urls))

    def __download_education_docs(self, name, pdf_url):
        response = urllib.request.urlopen(pdf_url)
        with open('./educations/{}.pdf'.format(name), 'wb') as file_descriptor:
            file_descriptor.write(response.read())

    def get_education_program(self, extract_by='module'):
        for pdf_name in self._education_program_urls.keys():
            self.__download_education_docs(pdf_name, self._education_program_urls[pdf_name])
        logger.log('end download')
        docs = self.__extract_educations(self._education_program_urls.keys(), extract_by)
        return pd.DataFrame.from_records(docs, columns=['name', 'documents'])

    def __extract_educations(self, education_docs_name, extract_by='module'):
        docs = []
        for doc in education_docs_name:
            with open('./educations/{}.pdf'.format(doc), 'rb') as doc_stream:
                doc_as_page_string = slate.PDF(doc_stream)
                logger.log('end extract {}'.format(doc))
            doc_as_string = ' '.join(doc_as_page_string)
            if extract_by == 'module':
                docs.append([doc, doc_as_string])
            else:
                for discipline in self.__split_module_by_discipline(doc_as_string):
                    docs.append([discipline[0], discipline[1]])
        return docs

    def __get_name(self, discipline):
        end_words = ['1.1', 'рабочая', 'аннотация', '1.2', '1.3']
        end_positions = [discipline.lower().find(end) for end in end_words]
        min_end = len(discipline)
        for pos in end_positions:
            if pos < min_end and pos != -1:
                min_end = pos
        name = discipline[:min_end].strip().lower().replace('\n', '').replace('«','').replace('-', '').replace('»', '')
        if name == '':
            name = 'not contain name'
        return name

    def __split_module_by_discipline(self, module):
        disciplines = module.split('ОБЩАЯ ХАРАКТЕРИСТИКА ДИСЦИПЛИНЫ')
        result = []
        for discipline in disciplines[1:]:
            name = self.__get_name(discipline)
            result.append([name, discipline])
        return result
