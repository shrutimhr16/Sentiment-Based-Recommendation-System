import pickle as pk
import pickle
import pandas as pd
import os
print(os.getcwd())

# Load pre trained sentiment model and vectorizer
with open('pickle/model.pkl', 'rb') as f:
    sentiment_model = pickle.load(f)
#print(sentiment_model,type(sentiment_model))
with open('pickle/tfidf-vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('pickle/cleaned-data.pkl', 'rb') as f:
    df = pickle.load(f)

review_df=pd.read_csv('sample30.csv')
print(review_df.loc[review_df.reviews_username=='mike'])

def check_valid_user(username):
    user_reviews = review_df[review_df['reviews_username'].str.lower() == username.lower()]
    if user_reviews.empty:
        return False
    else:
        return True
    

def model_predict(text):
    """Predict sentiment label for given text using trained model."""
    tfidf_vector = vectorizer.transform(text)
    return sentiment_model.predict(tfidf_vector)

def recommend_products(user_name):
    """Generate top 20 product recommendations with sentiment predictions for a user."""
    recommend_matrix = pk.load(open('pickle/recommendation_model.pkl', 'rb'))
    product_list = pd.DataFrame(recommend_matrix.loc[user_name].sort_values(ascending=False)[:20])
    print("product_list",product_list)
    product_frame = df[df.id.isin(product_list.index.tolist())]
    #product_reviews = df[df['id'] == product_id]['reviews_text']
    print("product_frame",product_frame.head())
    output_df = product_frame[['name', 'reviews_text']]
    print("output_df",output_df.head())
    output_df['predicted_sentiment'] = model_predict(output_df['reviews_text'])
    print(output_df.head())
    return output_df

def top5_products(df):
    """Return top 5 products with highest positive sentiment percentage."""
    total_product = df.groupby(['name']).agg('count')
    rec_df = df.groupby(['name', 'predicted_sentiment']).agg('count').reset_index()
    merge_df = pd.merge(rec_df, total_product['reviews_text'], on='name')
    merge_df['%percentage'] = (merge_df['reviews_text_x'] / merge_df['reviews_text_y']) * 100
    merge_df = merge_df.sort_values(ascending=False, by='%percentage')
    print(merge_df[:5])
    return pd.DataFrame(merge_df['name'][merge_df['predicted_sentiment'] == 1][:5])


