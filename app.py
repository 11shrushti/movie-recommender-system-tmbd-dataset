import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json


def fetch_poster(movie_id):
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # Number of retries
        backoff_factor=1,  # Time to wait between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        # Make the request
        response = session.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2eec3c9334dbb9ab95c84ca6e5da9251",
            timeout=10  # Timeout in seconds
        )
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse JSON data
        data = response.json()
        
        # Return the poster URL if available
        if "poster_path" in data:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            print("Poster path not found in the response.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    
    return None

    # response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=2eec3c9334dbb9ab95c84ca6e5da9251".format(movie_id) ,timeout=10 )
    # data = response.json()
    
    # return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
   
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
  # need to find the distances
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse = True, key = lambda x : x[1])[1:6]
    

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from the api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open("movie_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl","rb"))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a Movie of your choice." ,
    movies["title"].values 
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    
    col1 , col2 ,col3 ,col4 ,col5= st.columns(5)
    
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])                