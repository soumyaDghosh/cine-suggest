import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_processed(path="data/processed_tmdb.pkl"):
    return pd.read_pickle(path)

def compute_similarity(df):
    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(df["tags"]).toarray()
    similarity = cosine_similarity(vectors)
    return similarity

def recommend(movie_name, df, similarity, n: int=5) -> dict:
    index = df[df["title"] == movie_name].index[0]
    distances = list(enumerate(similarity[index]))
    movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:n+1]
    return { df.iloc[movie[0]].title: df.iloc[movie[0]].movie_id for movie in movies }

