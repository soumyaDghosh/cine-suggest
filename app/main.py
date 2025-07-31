import sys
import os
sys.path.insert(0, os.path.curdir)

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from model.recommender import load_processed, compute_similarity, recommend
from utilities.utils import fetch_image

df = load_processed()
similarity = compute_similarity(df)

st.title("🎥Cine Suggest")
search = st.text_input("Type to search a movie")
filtered = [title for title in df["title"] if search.lower() in title.lower()]

if search:
    movie_name = st.selectbox("Pick from results", filtered if filtered else ["No match"])


    if st.button("Recommend"):
        with st.spinner("Generating recommendations..."):
            recommendations: dict = recommend(movie_name, df, similarity)
            cols: list[DeltaGenerator] = st.columns(len(recommendations))
            for col, (name, movie_id) in zip(cols, recommendations.items()):
                with col:
                    st.image(fetch_image(movie_id))
                    st.text(name)
