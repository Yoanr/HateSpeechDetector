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

def classify_tweet(le, vectorizer, tweet, clf):
    lab = ["The tweet contains hate speech","The tweet is not offensive","The tweet uses offensive language but not hate speech"]
    tweet_to_clf = processTweet(tweet)
    tweet_to_clf = vectorizer.transform([tweet_to_clf])
    label = clf.predict(tweet_to_clf)[0]
    confidence = max(clf.predict_proba(tweet_to_clf)[0])*100
    return 'hateSpeech says: ' + lab[label] + ' with ' + str(round(confidence, 2)) + '% confidence.'

def perform(inputText):
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


    X = vectorizer.transform(text)
    y = hate_speech_subset['Numeric_Verdict'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    #print(X.shape)

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
    clf_rfc.score(X_test, y_test)


    #pickle.dump(clf_rfc, open('classifiernew.pkl', 'wb'),protocol = 4)

    print(classify_tweet(le, vectorizer, inputText, clf_rfc))
