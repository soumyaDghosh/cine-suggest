import sys
import os
sys.path.insert(0, os.path.curdir)

import streamlit as st
from model.recommender import load_processed, compute_similarity, recommend
from utilities.utils import fetch_image

df = load_processed()
similarity = compute_similarity(df)

st.title("🎥Cine Suggest")
movie_name = st.selectbox("Select a movie:", df["title"].values)


if st.button("Recommend"):
    with st.spinner("Generating recommendations..."):
        recommendations = recommend(movie_name, df, similarity)
        cols = st.columns(len(recommendations))
        for col, (name, movie_id) in zip(cols, recommendations.items()):
            with col:
                st.image(fetch_image(movie_id))
                st.text(name)
