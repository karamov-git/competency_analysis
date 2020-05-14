import urllib.request

import pandas as pd
import slate3k as slate
import logger


class EducationDocumentsProvider:

    def __init__(self):
        self._education_program_urls = {
            'Безопасность сетевых технологий': 'https://programs.edu.urfu.ru/media/rpm/00031837.pdf',
            'Безопасные автоматизированные системы': 'https://programs.edu.urfu.ru/media/rpm/00031826.pdf',
            'Инженерно-техническая защита информации': 'https://programs.edu.urfu.ru/media/rpm/00031824.pdf',
            'Информационное кодирование': 'https://programs.edu.urfu.ru/media/rpm/00031825.pdf',
            'Математические основы обеспечения информационной безопасности': 'https://programs.edu.urfu.ru/media/rpm/00032487.pdf',
            'Методы и средства борьбы с компьютерной преступностью': 'https://programs.edu.urfu.ru/media/rpm/00031843.pdf',
            'Методы и средства защиты документооборота': 'https://programs.edu.urfu.ru/media/rpm/00031842.pdf',
            'Программно-алгоритмическое обеспечение информационной безопасности': 'https://programs.edu.urfu.ru/media/rpm/00031827.pdf',
            'Программно-аппаратные средства защиты информации': 'https://programs.edu.urfu.ru/media/rpm/00031835.pdf',
            'Метрология, стандартизация и сертификация': 'https://programs.edu.urfu.ru/media/rpm/00032305.pdf',
            'Программные средства проектирования систем связи': 'https://programs.edu.urfu.ru/media/rpm/00032276.pdf',
            'Проектирование средств связи': 'https://programs.edu.urfu.ru/media/rpm/00029187.pdf',
            'Системы связи': 'https://programs.edu.urfu.ru/media/rpm/00029152.pdf',
            'Теоретические основы передачи информации': 'https://programs.edu.urfu.ru/media/rpm/00032106.pdf',
            'Теория связи': 'https://programs.edu.urfu.ru/media/rpm/00029144.pdf',
            'Анализ предметной области': 'https://programs.edu.urfu.ru/media/rpm/00028624.pdf',
            'Базы данных и знаний': 'https://programs.edu.urfu.ru/media/rpm/00028561.pdf',
            'Графические приложения': 'https://programs.edu.urfu.ru/media/rpm/00028583.pdf',
            'Измерительные информационные системы': 'https://programs.edu.urfu.ru/media/rpm/00028667.pdf',
            'Информационная безопасность': 'https://programs.edu.urfu.ru/media/rpm/00032258.pdf',
            'Концепции современного программирования': 'https://programs.edu.urfu.ru/media/rpm/00028557.pdf',
            'Корпоративные информационные системы': 'https://programs.edu.urfu.ru/media/rpm/00028666.pdf',
            'Многоуровневые и мобильные приложения': 'https://programs.edu.urfu.ru/media/rpm/00028580.pdf',
            'Основы информационных процессов': 'https://programs.edu.urfu.ru/media/rpm/00028562.pdf',
            'Проектирование микропроцессорных систем': 'https://programs.edu.urfu.ru/media/rpm/00031158.pdf',
            'Промышленные базы данных': 'https://programs.edu.urfu.ru/media/rpm/00028663.pdf',
            'Современные сетевые технологии': 'https://programs.edu.urfu.ru/media/rpm/00028553.pdf',
            'Средства и технологии разработки программного обеспечения': 'https://programs.edu.urfu.ru/media/rpm/00025161.pdf',
            'Средства разработки корпоративных информационных систем': 'https://programs.edu.urfu.ru/media/rpm/00028634.pdf',
            'Администрирование и безопасность операционных систем': 'https://programs.edu.urfu.ru/media/rpm/00032062.pdf',
            'Безопасность документооборота': 'https://programs.edu.urfu.ru/media/rpm/00032069.pdf',
            'Безопасность систем связи': 'https://programs.edu.urfu.ru/media/rpm/00032071.pdf',
            'Криминалистические методы информационной безопасности': 'https://programs.edu.urfu.ru/media/rpm/00032076.pdf',
            'Моделирование сетей и систем': 'https://programs.edu.urfu.ru/media/rpm/00032068.pdf',
            'Организация защиты информации': 'https://programs.edu.urfu.ru/media/rpm/00032067.pdf',
            'Базы данных и интеллектуальные системы': 'https://programs.edu.urfu.ru/media/rpm/00029974.pdf',
            'Интеллектуальные методы анализа информации': 'https://programs.edu.urfu.ru/media/rpm/00029983.pdf',
            'Интернет-технологии': 'https://programs.edu.urfu.ru/media/rpm/00029978.pdf',
            'Методы анализа Big Data': 'https://programs.edu.urfu.ru/media/rpm/00029984.pdf',
            'Управление в технических системах': 'https://programs.edu.urfu.ru/media/rpm/00029988.pdf',
            'Управление проектами информационных систем': 'https://programs.edu.urfu.ru/media/rpm/00029991.pdf',
            'Администрирование информационных систем': 'https://programs.edu.urfu.ru/media/rpm/00030238.pdf',
            'Реальное программирование': 'https://programs.edu.urfu.ru/media/rpm/00029418.pdf',
            'Эффективное программирование': 'https://programs.edu.urfu.ru/media/rpm/00029427.pdf',
            'Менеджмент в информационных технологиях': 'https://programs.edu.urfu.ru/media/rpm/00032287.pdf',
            'Основания информатики и программирования': 'https://programs.edu.urfu.ru/media/rpm/00032278.pdf',
            'Основы программной инженерии': 'https://programs.edu.urfu.ru/media/rpm/00032283.pdf',
            'Проектирование информационных систем': 'https://programs.edu.urfu.ru/media/rpm/00032288.pdf',
            'Проектирование программного обеспечения': 'https://programs.edu.urfu.ru/media/rpm/00032291.pdf',
            'Технологии разработки Web-приложений': 'https://programs.edu.urfu.ru/media/rpm/00032284.pdf',
            'Языки логического программирования': 'https://programs.edu.urfu.ru/media/rpm/00031689.pdf',
            'Автоматизированные управляющие и информационные системы': 'https://programs.edu.urfu.ru/media/rpm/00030875.pdf',
            'Микропроцессорные системы': 'https://programs.edu.urfu.ru/media/rpm/00030870.pdf'}

    def __download_education_docs(self, name, pdf_url):
        response = urllib.request.urlopen(pdf_url)
        with open('./educations/{}.pdf'.format(name), 'wb') as file_descriptor:
            file_descriptor.write(response.read())

    def get_education_program(self):
        for pdf_name in self._education_program_urls.keys():
            self.__download_education_docs(pdf_name, self._education_program_urls[pdf_name])
        logger.log('end download')
        docs = self.__extract_educations(self._education_program_urls.keys())
        return pd.DataFrame(docs, columns=['documents'])

    def __extract_educations(self, education_docs_name):
        docs = []
        for doc in education_docs_name:
            with open('./educations/{}.pdf'.format(doc), 'rb') as doc_stream:
                doc_as_page_string = slate.PDF(doc_stream)
                logger.log('end extract {}'.format(doc))
            doc_as_string = ' '.join(doc_as_page_string)
            docs.append(doc_as_string)
        return docs
