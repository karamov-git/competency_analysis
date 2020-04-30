import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

from normalizer import read_frequency_table, DocumentsNormalizer


def make_clustering(cluser_count, topic_count):
    def get_terms(topic_number, corpus, component):
        component_for_topic = component[topic_number, :][0]
        corpus_weight_for_topic = zip(corpus, component_for_topic)
        return np.array(sorted(corpus_weight_for_topic, key=lambda x: x[1], reverse=True)[:10])[:, 0]

    def get_top_terms_for_even_documents(svd, component, corpus):
        significant_topic_for_each_row = np.argmax(svd, axis=1).reshape((svd.shape[0], 1))
        return np.apply_along_axis(get_terms, 1, significant_topic_for_each_row, corpus, component)

    frequency_table, terms = read_frequency_table()
    origignal_table = frequency_table.toarray()

    svd_model = TruncatedSVD(n_components=topic_count)
    topics = svd_model.fit_transform(origignal_table)
    components = svd_model.components_
    top_terms = get_top_terms_for_even_documents(topics, components, terms)
    embedding = TSNE(n_components=2, metric='cosine', random_state=5).fit_transform(topics)

    kmeans = KMeans(n_clusters=cluser_count, random_state=3)
    return kmeans.fit_predict(topics), embedding, top_terms


def cluster_visualization(clusters, embedding, top_terms, file_name):
    df = pd.DataFrame(clusters, columns=['cluster_n'])
    df['Id'] = np.arange(len(df))
    df['x'] = embedding[:, 0]
    df['y'] = embedding[:, 1]

    plt.figure(figsize=(20, 15))
    group_by_cluster = df.groupby('cluster_n')
    for name, group in group_by_cluster:
        c = np.array([np.random.rand(3, )] * len(group['Id']))
        plt.scatter(group['x'], group['y'],
                    s=20,
                    c=c,
                    edgecolor='none',
                    label=name)

    plt.legend(fontsize=12)
    plt.savefig('./' + file_name + '.png')

    df2 = pd.DataFrame(top_terms)
    df2['cluster'] = clusters

    group_by_cluster = df2.groupby('cluster')
    top_words_by_cluster = []
    for name, group in group_by_cluster:
        top_terms_in_group = group.iloc[:, 0:10]
        unique_words_in_group = dict()
        for i, row in top_terms_in_group.iterrows():
            for j, word in row.items():
                if word in unique_words_in_group:
                    continue
                else:
                    unique_words_in_group[word] = 1
        top_words_by_cluster.append((name, " ".join(unique_words_in_group.keys())))

    cluster_top_terms = []
    for cluster_name, words in top_words_by_cluster:
        cluster_top_terms.append(str(cluster_name) + ': ' + words)

    with open('./' + file_name + '.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(cluster_top_terms))


start_n_components = 100
start_n_cluster = 4


def visualization_embedding(embedding, file_name):
    plt.figure(figsize=(20, 15))
    plt.scatter(embedding[:, 0], embedding[:, 1],
                edgecolor='none')
    plt.legend(fontsize=12)
    plt.savefig('./' + file_name + '.png')


def get_terms(topic_number, corpus, component):
    component_for_topic = component[topic_number, :][0]
    corpus_weight_for_topic = zip(corpus, component_for_topic)
    a = sorted(corpus_weight_for_topic, key=lambda x: x[1], reverse=True)
    return np.array(a)[:, 0]


def get_top_terms_for_each_documents(svd, component, corpus):
    significant_topic_for_each_row = np.argmax(svd, axis=1).reshape((svd.shape[0], 1))
    return np.apply_along_axis(get_terms, 1, significant_topic_for_each_row, corpus, component)



topic_count = 5

data_set = pd.read_csv('./merged.csv').head(1000)
documents = data_set['description']

normalizer = DocumentsNormalizer(should_log=True)
corpus = normalizer.normalize_documents(documents)

vectorizer = TfidfVectorizer(min_df=0.005, max_df=0.98, dtype=np.float64)
frequency_table = vectorizer.fit_transform(corpus)

origignal_table = frequency_table.toarray()

svd_model = TruncatedSVD(n_components=topic_count, algorithm='arpack')
topics = svd_model.fit_transform(origignal_table)
components = svd_model.components_
lda = LatentDirichletAllocation(n_components=topic_count, random_state=0)
topics = lda.fit_transform(origignal_table)
components = lda.components_
#top_terms = get_top_terms_for_each_documents(topics, components, terms)


embedding = TSNE(n_components=2, metric='cosine', random_state=5).fit_transform(topics)

clusters_by_topics = np.argmax(topics, axis=1).reshape((topics.shape[0], 1))
df2 = pd.DataFrame(np.arange(topics.shape[0]), columns=['Id'])
df2['cluster'] = clusters_by_topics
group_by_cluster = df2.groupby('cluster')


data = np.array(corpus)
for name, group in group_by_cluster:
    unique_words = {}
    for i, row in group.iterrows():
        d_id = row['Id']
        document  = data[d_id]
        for word in document.split():
            word = word.strip()
            if word in unique_words:
                continue
            else:
                unique_words[word] = 1
    print(" ".join(unique_words.keys()))



"""for n_components in range(start_n_components, 301, 50):
    for n_cluster in range(start_n_cluster, 10):
        cluster, embedding, top_terms = make_clustering(n_cluster, n_components)
        file_name = 'clustering_without_lem/{0}-{1}'.format(n_components, n_cluster)
        cluster_visualization(cluster, embedding, top_terms, file_name)


frequency_table, terms = read_frequency_table()
origignal_table = frequency_table.toarray()

for n_components in range(start_n_components, 301, 50):
    svd_model = TruncatedSVD(n_components=n_components)
    topics = svd_model.fit_transform(origignal_table)
    embedding = TSNE(n_components=2, metric='cosine', random_state=5).fit_transform(topics)
    visualization_embedding(embedding, 'n_components2/{0}'.format(n_components))
"""