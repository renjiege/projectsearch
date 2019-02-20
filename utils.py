##########auto similarity function#######################################################################

from sklearn.feature_extraction.text import TfidfVectorizer
import os.path
import pandas as pd
import numpy as np

pd.set_option('display.max_colwidth', -1)
project_path = os.path.abspath(os.path.dirname(__file__))
data = os.path.join(project_path, "data/Data_for_Similarity_New.xlsx")

def most_similarity_project(input_text):

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    datasource = pd.read_excel(data, encoding="ISO-8859-1")
    datasource.head()

    datasource['Simiscore'] = 0

    index_source = 0
    max_simi = 0

    for i in range(0, len(datasource)):
        documents = []
        documents.append(input_text)
        documents.append(datasource.loc[i, 'Text'])
        tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words='english').fit_transform(documents)
        # no need to normalize, since Vectorizer will return normalized tf-idf
        pairwise_similarity = tfidf * tfidf.T
        temp = pairwise_similarity.A[0][1]
        simiscore = "{0:.4f}".format(temp)
        datasource.loc[i, 'Simiscore'] = simiscore

    datasource['Rank'] = datasource['Simiscore'].rank(method='average', ascending=False)
    datasource = datasource.sort_values('Rank', ascending=True)
    datasource['Rank'] = datasource['Rank'].astype(np.int64)
    datasource['Simiscore'] = datasource['Simiscore'].astype(np.float)
    datasource = datasource[datasource['Simiscore'] != 0]

    if datasource.size == 0:
        return '<h3>No results found. Please try other keywords.</h3>'
    else:
        datasource = datasource.head(10)
        datasource = datasource.reset_index()
        # select some needed columns to display
        datadisplay = datasource[
            ["Rank", "ProjectName", "Organization", "Country", "Sector", "Year", "Practitioner", "ProjectID", "Text"]]
        return datadisplay.to_html()
