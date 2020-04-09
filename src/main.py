import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from normalizer import DocumentsNormalizer

data_set = pd.read_csv('./merged.csv')
normalizer = DocumentsNormalizer(should_log=True)
corpus = normalizer.normalize_documents(data_set['description'])
vectorizer = CountVectorizer()
frequency_table = vectorizer.fit_transform(corpus)
features = vectorizer.get_feature_names()

count_vect_df = pd.DataFrame(frequency_table.todense(), columns=vectorizer.get_feature_names())
count_vect_df.to_csv('./frequency_table.csv')

print("end of main.py")
