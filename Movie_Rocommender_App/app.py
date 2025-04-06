import streamlit as st
import pandas as pd
import pickle
import requests

# Loading the movie dataset and similarity matrix
file = open('../movie_dict.pkl', 'rb')
movieList = pickle.load(file)
file.close()
movieList = pd.DataFrame(movieList)

file = open('../similarity.pkl', 'rb')
similarity = pickle.load(file)
file.close()

# Function to fetch movie poster
def fetch_poster(movie_id):
    not_found = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNNLEL-qmmLeFR1nxJuepFOgPYfnwHR56vcw&s'
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']

    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = not_found

    return full_path

# Function to recommend movies
def recommend_movie(movie_name):
    index = movieList[movieList['title'] == movie_name].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movieList.iloc[i[0]].title)
    return recommended_movies

# Streamlit App
st.set_page_config(page_title="Movie Recommender App", page_icon=":movie_camera:", layout="wide")
st.write('# Movie Recommender App')
st.write('This is a simple movie recommender app built with Streamlit.')
length = len(movieList['title'].values)
st.write(length, 'Movies are Available')

seleted_movie = st.selectbox('Select a Movie Name', movieList['title'].values)

if st.button('Recommendation'):
    recommendations = recommend_movie(seleted_movie)

    st.write('### Recommendations:')
    cols = st.columns(5)
    
    for idx, i in enumerate(recommendations):
        movie_id = movieList[movieList['title'] == i].movie_id.values[0]
        poster = fetch_poster(movie_id)

        with cols[idx]:
            st.image(poster, width=200)
            st.write(i)
            st.write('Movie ID:', movie_id)
            st.write('More Details:', f'[Click Me](https://www.themoviedb.org/movie/{movie_id})')