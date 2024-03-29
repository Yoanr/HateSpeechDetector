import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve, GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
import string
import re
from nltk.corpus import stopwords
from sklearn import preprocessing
import pickle
import numpy as np
import pandas as pd
import warnings
import os
import pickle
import argparse
import dill

from mlxtend.evaluate import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix


def convert(old_pkl):
    """
    Convert a Python 2 pickle to Python 3
    """
    # Make a name for the new pickle
    new_pkl = os.path.splitext(os.path.basename(old_pkl))[0]+"_p3.pkl"

    # Convert Python 2 "ObjectType" to Python 3 object
    dill._dill._reverse_typemap["ObjectType"] = object

    # Open the pickle using latin1 encoding
    with open(old_pkl, "rb") as f:
        loaded = pickle.load(f, encoding="latin1")

    # Re-save as Python 3 pickle
    with open(new_pkl, "wb") as outfile:
        pickle.dump(loaded, outfile)


def processTweet(tweet):

    tweet = tweet.lower()
    #Remove urls
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', tweet)
    #Remove usernames
    tweet = re.sub('@[^\s]+', '', tweet)
    #Remove white space
    tweet = tweet.strip()
    #Remove hashtags
    tweet = re.sub(r'#([^\s]+)', '', tweet)
    #Remove stopwords
    tweet = " ".join([word for word in tweet.split(
        ' ') if word not in stopwords.words('english')])
    #Remove punctuation
    tweet = "".join(l for l in tweet if l not in string.punctuation)

    return tweet


def dump():
    hate_speech = pd.read_csv('./twitter-hate-speech-classifier-DFE-a845520.csv',
                            encoding='iso-8859-1')
    print('There are', len(hate_speech), 'data points.')
    hate_speech_subset = hate_speech.iloc[:, [19, 5, 6]]
    hate_speech_subset.columns = ['Tweets', 'Verdict', 'Confidence']

    le = preprocessing.LabelEncoder()
    le.fit(list(hate_speech_subset.Verdict.unique()))
    hate_speech_subset['Numeric_Verdict'] = le.transform(
        list(hate_speech_subset.Verdict.values))
    hate_speech_subset['Tweets'] = hate_speech_subset['Tweets'].map(
        lambda x: processTweet(x))

    text = hate_speech_subset['Tweets'].values
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    vectorizer.fit(text)


    X = vectorizer.transform(text)
    y = hate_speech_subset['Numeric_Verdict'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y)


    cm = confusion_matrix(y_train,
                      SVC(kernel='linear', probability=True).fit(X_train, y_train).predict(X_train))
    fig, ax = plot_confusion_matrix(conf_mat=cm)
    plt.show()

    #0 : The tweet contains hate speech
    #1 : The tweet is not offensive
    #2 : The tweet uses offensive language but not hate speech

    print(X.shape)

    """
    param_grid = {"max_depth": [3, None],
                "n_estimators": [10, 50, 100],
                "max_features": [1, 3, 10],
                "min_samples_split": [2, 3, 10],
                "min_samples_leaf": [1, 3, 10],
                "bootstrap": [True, False],
                "criterion": ["gini", "entropy"]}

    grid_rf = GridSearchCV(RandomForestClassifier(),
                            param_grid=param_grid,
                            cv=10,
                            scoring='accuracy')
    grid_rf.fit(X_train, y_train)
    grid_rf.score(X_train, y_train)
    """
    clf_rfc = RandomForestClassifier()
    clf_rfc.fit(X_train, y_train)
    score = clf_rfc.score(X_test, y_test)
    print(score)

    pickle.dump(clf_rfc, open('pkl_objects/classifier.pkl', 'wb'), protocol= 4)
    convert('pkl_objects/classifier.pkl')


def performFast(inputText):

    hate_speech = pd.read_csv('./twitter-hate-speech-classifier-DFE-a845520.csv',
                              encoding='iso-8859-1')
    #print('There are', len(hate_speech), 'data points.')
    hate_speech_subset = hate_speech.iloc[:, [19, 5, 6]]
    hate_speech_subset.columns = ['Tweets', 'Verdict', 'Confidence']

    le = preprocessing.LabelEncoder()
    le.fit(list(hate_speech_subset.Verdict.unique()))
    hate_speech_subset['Numeric_Verdict'] = le.transform(
        list(hate_speech_subset.Verdict.values))
    hate_speech_subset['Tweets'] = hate_speech_subset['Tweets'].map(
        lambda x: processTweet(x))

    text = hate_speech_subset['Tweets'].values
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    vectorizer.fit(text)
    CUR_DIR = os.path.dirname(__file__)
    CLF = pickle.load(open(
        os.path.join(CUR_DIR,
                     'pkl_objects',
                     'classifier_p3.pkl'), 'rb'))

                     
    lab = ["contains hate speech", "is not offensive",
           "uses offensive language but not hate speech"]
    tweet_to_clf = processTweet(inputText)
    tweet_to_clf = vectorizer.transform([tweet_to_clf])
    label = CLF.predict(tweet_to_clf)[0]
    confidence = max(CLF.predict_proba(tweet_to_clf)[0])*100

    print("The Msg : ", inputText,lab[label], " with ", str(round(confidence, 2)) + "% confidence.")
    return label



