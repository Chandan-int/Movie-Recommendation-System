import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=17b84c6365053d48596585faf6e22d9e&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        print(f"Failed to fetch poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"



def recomended(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recomended_movies=[]
    recomended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recomended_movies.append(movies.iloc[i[0]].title)
        # fetch_poster_url=fetch_poster(movies.iloc[i[0]].movie_id)
        recomended_movies_poster.append(fetch_poster(movie_id))
    return recomended_movies, recomended_movies_poster

Movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(Movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recomender System')



selected_movie_name=st.selectbox(
    'How woould you like to be contacted?',
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movies, recommended_movie_posters = recomended(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)  # <- changed line
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movie_posters[4])

