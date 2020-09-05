
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import nltk.classify.util
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
from nltk.classify import NaiveBayesClassifier
import numpy as np
import re
import string
import nltk

# data = pd.read_csv('Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv', low_memory=False)
data = pd.read_json('Cell_Phones_and_Accessories_5.json', lines=True)
data = data[["overall", "reviewText", "summary", "reviewerName"]]
data.columns = ['reviews.rating' , 'reviews.text' , 'reviews.title' , 'reviews.username']

# Drop NAN Values
data = data.dropna()


data['reviews'] = data['reviews.rating'] >= 3
data['reviews'] = data['reviews'].replace([True, False],["POS", "NEG"])


negative_review_count = len(data[data["reviews"] == "NEG"])
positive_review_count = len(data[data["reviews"] == "POS"])


positive_data = data[data["reviews"] == "POS"]
positive_data = positive_data.sample(negative_review_count)
negative_data = data[data["reviews"] == "NEG"]
balanced_data = pd.concat([positive_data, negative_data]).sample(frac=1)
balanced_data["reviews"] = balanced_data["reviews"].replace(["POS", "NEG"], [1, 0])


import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
import numpy as np
import re
import string
import nltk

cleanup_re = re.compile('[^a-z]+')
def cleanup(sentence):
    sentence = str(sentence)
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    #sentence = " ".join(nltk.word_tokenize(sentence))
    return sentence

balanced_data["Summary_Clean"] = balanced_data["reviews.text"].apply(cleanup)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(balanced_data["Summary_Clean"], balanced_data["reviews"])

from wordcloud import STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
stopwords = set(STOPWORDS)
stopwords.remove("not") # "not" is an important word in making a negation of an quality.

vect = TfidfVectorizer(min_df=2, stop_words=stopwords, ngram_range=(1,2))

X_train_vector = vect.fit_transform(X_train)

X_test_vector = vect.transform(X_test)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score

scores = {} # To store the scores of all models

model1 = MultinomialNB().fit(X_train_vector , y_train)
predictions = model1.predict(X_test_vector)

auc_score = roc_auc_score(y_test, predictions)
scores["Multinomial Naive Bayes"] = auc_score

from sklearn.naive_bayes import BernoulliNB

model2 = BernoulliNB().fit(X_train_vector, y_train)
predictions = model2.predict(X_test_vector)

auc_score = roc_auc_score(y_test, predictions)
scores["Bernouli Naive Bayes"] = auc_score

from sklearn.linear_model import LogisticRegression

model3 = LogisticRegression(C=1000)
model3.fit(X_train_vector, y_train)
predictions = model3.predict(X_test_vector)

auc_score = roc_auc_score(y_test, predictions)

scores["Logistic Regression"] = auc_score

words = vect.get_feature_names()
feature_coefs = pd.DataFrame(
    data = list(zip(words, model3.coef_[0])),
    columns = ['feature', 'coef'])
feature_coefs = feature_coefs.sort_values(by="coef")

negative_words = "".join([str("\t\t\t\t\t\t\t" + str(pos + 1) + ": " + str(word) + "\n") for pos, word in enumerate(feature_coefs["feature"][:10])])
positive_words = "".join([str("\t\t\t\t\t\t\t" + str(pos + 1) + ": " + str(word) + "\n") for pos, word in enumerate(feature_coefs["feature"][:-11:-1])])

# def test_sample(model, sample):
#     sample_tfidf = vect.transform(sample)
#     result = model.predict(sample_tfidf)
#     prediction = model.predict(sample_tfidf)
#     probability = model.predict_proba(sample_tfidf)
#     print("Sample estimated as {} \nwith probability of being Negative: {}    and with probability of being Positive: {}".format("Positive" if prediction else "Negative", probability[0][0], probability[0][1]))

# test_sample(model3, ['The product was good and easy to  use'])


# SAVE THE LOGISTIC REGRESSION MODEL
import pickle
filename = 'finalized_model.sav'
pickle.dump(model3, open(filename, 'wb'))

# SAVE THE VECTORIZER
filename = "vectorizer.sav"
pickle.dump(vect, open(filename, 'wb'))
