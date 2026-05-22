import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return "https://via.placeholder.com/500x750?text=API+Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters =[]

    for i in movies_list:
        movie_id =  movies.iloc[i[0]].movie_id
        #fetch posters from API
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch posters from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('MOVIE RECOMMENDER SYSTEM')

Selected_Movie_name= st.selectbox('Please select a movie to recommend', movies['title'].values)

if st.button('Recommend'):
    names,poster = recommend(Selected_Movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
         st.text(names[0])
         st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
            st.text(names[2])
            st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])

