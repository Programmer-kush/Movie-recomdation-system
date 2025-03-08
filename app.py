'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date: 2021-Nov-15
'''

import pickle 
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


import streamlit as st
import pickle
import requests

# Streamlit Title
st.header('Movie Recommender System Using Machine Learning')

# GitHub Releases URLs
movie_list_url = "https://github.com/Programmer-kush/Movie-recomdation-system/releases/download/v1.0/movie_list.pkl"
similarity_url = "https://github.com/Programmer-kush/Movie-recomdation-system/releases/download/v1.0/similarity.pkl"

# Local filenames
movie_list_file = "movie_list.pkl"
similarity_file = "similarity.pkl"

# Function to download files
def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
    else:
        st.error(f"Failed to download {filename}. Check the URL or network connection.")

# Download and save the files
download_file(movie_list_url, movie_list_file)
download_file(similarity_url, similarity_file)

# Load Pickle Files
try:
    movies = pickle.load(open(movie_list_file, 'rb'))
    similarity = pickle.load(open(similarity_file, 'rb'))
    st.write("Files loaded successfully!")
except Exception as e:
    st.error(f"Error loading pickle files: {e}")
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
