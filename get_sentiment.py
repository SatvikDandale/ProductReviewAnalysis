from reviews import get_reviews
import pandas as pd

def get_sentiment(text=[], modelName="finalized_model.sav", vectorName="vectorizer.sav"):
    if len(text) == 0:
        return -1

    # Load the model and vectorizer from pickle file
    import pickle
    # from sklearn.feature_extraction.text import TfidfVectorizer

    vect = pickle.load(open(vectorName, 'rb'))
    sample = vect.transform(text)
    
    model = pickle.load(open(modelName, 'rb'))
    results = model.predict(sample)
    results= ["POS" if result == 1 else "NEG" for result in results]
    return pd.Series(results)

def reviews_analysis(url):
    """
    This module will obtain the dataframe containing the reviews:
        1. Calculate the sentiments using the reviews
        2. Calculate the count of positive and negative reviews
        3. Calculate the average rating
    Returns
        total_ratings, avg_rating, negative_reviews
    """

    import numpy as np
    product_name, dataframe = get_reviews(url)
    
    # Just get the title as reviews
    reviews = dataframe["title"]
    dataframe["rating"] = dataframe["rating"].astype('float')
    ratings = dataframe["rating"]
    avg_rating = np.mean(ratings)
    sentiments = get_sentiment(reviews)
    # sentiments = pd.Series([1 if sentiment == "POS" else 0 for sentiment in sentiments])
    
    print(sentiments)
    print(ratings)
    dataframe["rating"] = dataframe["rating"].astype('int')
    # negative_reviews = dataframe[dataframe["rating"] < 3]
    negative_reviews = dataframe[sentiments == "NEG"]
    # print(negative_reviews)


    return product_name, ratings, avg_rating, negative_reviews, sentiments

if __name__ == "__main__":
    url = "https://www.amazon.com/Xiaomi-Redmi-Note-Internationa-Version/dp/B07YZLRBFP/ref=sr_1_5?dchild=1&keywords=smartphones&qid=1587811250&sr=8-5"
    product_name, ratings, avg_rating, negative_reviews, sentiments = reviews_analysis(url)
    if len(negative_reviews) == 0:
        print("No negative reviews!")