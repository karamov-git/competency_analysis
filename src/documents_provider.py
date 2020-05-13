import urllib.request

import pandas as pd
import slate3k as slate


class EducationDocumentsProvider:

    def __init__(self):
        self.education_program_urls = {
            'Безопасность сетевых технологий': 'https://programs.edu.urfu.ru/media/rpm/00031837.pdf'}

    def download_education_docs(self, name, pdf_url):
        response = urllib.request.urlopen(pdf_url)
        with open('./educations/{}.pdf'.format(name), 'wb') as file_descriptor:
            file_descriptor.write(response.read())

    def get_education_program(self):
        for pdf_name in self.education_program_urls.keys():
            self.download_education_docs(pdf_name, self.education_program_urls[pdf_name])
        docs = self.extract_educations(self.education_program_urls.keys())
        return pd.DataFrame(docs, columns=['documents'])

    def extract_educations(self, education_docs_name):
        docs = []
        for doc in education_docs_name:
            with open('./educations/{}.pdf'.format(doc), 'rb') as doc_stream:
                doc_as_page_string = slate.PDF(doc_stream)
            doc_as_string = ' '.join(doc_as_page_string)
            docs.append(doc_as_string)
        return docs
