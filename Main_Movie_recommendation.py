import streamlit as st
import pickle
import pandas as pd
import requests
OMDB_API_KEY='27e41d49'
def fetch_poster(movie_title):
    url=f'http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}'
    response=requests.get(url)
    data=response.json()
    if 'Poster' in data and data['Poster']!='N/A':
        return data['Poster']
    else:
        return "https://via.placeholder.com/150"

def recommend(movie):
    # Find the index of the selected movie
    movie_index=movies[movies['title'] == movie].index[0]
    # Get the similarity scores for the selected movie
    distance=similarity[movie_index]
    # Sort movies based on similarity scores
    movie_list=sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    # Prepare lists for recommended movie titles and posters
    recommend_movies=[movie]
    recommended_movies_poster=[fetch_poster(movie)]

    # Add most similar movies to the recommendation list
    for i in movie_list:
        movie_title=movies.iloc[i[0]].title
        recommend_movies.append(movie_title)
        recommended_movies_poster.append(fetch_poster(movie_title))

    return recommend_movies,recommended_movies_poster

# Load movie data and similarity matrix from pickle files
movies_dict=pickle.loads(open(r'C:\Users\hasan\Desktop\classify\movies_dict.pkl', 'rb').read())
movies=pd.DataFrame(movies_dict)
similarity=pickle.loads(open(r'C:\Users\hasan\Desktop\classify\similarity.pkl', 'rb').read())

st.title('Movie Recommendation System')
selected_movie = st.selectbox('Which Movie Do You Prefer?', movies['title'].values)
if st.button('Recommend'):
    names, poster = recommend(selected_movie)
    col1, col2, col3 = st.columns(3)
    for i in range(len(names)):
        if i==0:
            with col1:
                st.text(names[i])
                st.image(poster[i])
        elif i==1:
            with col2:
                st.text(names[i])
                st.image(poster[i])
        elif i==2:
            with col3:
                st.text(names[i])
                st.image(poster[i])