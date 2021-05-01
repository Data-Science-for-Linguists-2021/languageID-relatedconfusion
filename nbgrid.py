import pickle
import pandas as pd
import numpy as np
from numpy import linalg
import sklearn
from sklearn.model_selection import cross_val_score, cross_val_predict, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import wikipedia
from sklearn.cluster import KMeans

f = open('data/chunks_shufanon.pkl', 'rb')
data = pickle.load(f)
f.close()

data['tokens'] = data['text'].map(lambda x: [bytes([elem]) for elem in list(x)])

X = data['tokens']
y = data['lang']

def dummy_fun(doc):
    return doc

def analyzer(chunk):
    n = 2 #gram size
    grams = []
    for i in range(len(chunk)-n+1):
        grams.append(b''.join(chunk[i:i+n]))
    return grams

# set up model, vectorizer
# FEATURES ARE CHARACTER BIGRAMS
cnt = CountVectorizer(analyzer=analyzer, tokenizer=dummy_fun, preprocessor=dummy_fun,
                      token_pattern=None,  )# bigrams
pipeline = Pipeline([
   ('vectorizer',cnt),
   ('model',MultinomialNB())
])

params = {'vectorizer__max_features': #[50, 100, 150, 200, 250, ]}
                                        [300, 350, 400, 450]}

# do cross validation
skf = StratifiedKFold(n_splits=5, random_state=0, shuffle=True)
# clf = cross_val_score(pipeline, X, y, cv=skf, scoring='accuracy', n_jobs=1)
grid_search = GridSearchCV(pipeline, params, cv=skf, n_jobs=1, verbose=1, )
grid_search.fit(X, y)

for e,s in zip(grid_search.cv_results_['params'], grid_search.cv_results_['mean_test_score']):
    print(e,s)
