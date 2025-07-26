import os
from fastapi import FastAPI
import pickle
import pandas as pd
import numpy as np
import requests


app = FastAPI()


# models folder path
def models_path(model_name):
    base_path = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(base_path, '..', 'models',model_name)
    models_path = os.path.abspath(models_path)
    return models_path

def load_movies():
    with open(models_path('movies.pkl'), 'rb') as f:
        movies = pickle.load(f)
    movies_df = pd.DataFrame(data = movies)
    return movies_df

def load_similarity_model():
    with open(models_path('similarity.pkl'), 'rb') as f:
        similarity_model = pickle.load(f)
    return similarity_model

# @app.get('/movie-details/{movie_id}')
# def movie_details(movie_id : int):

#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"

#     headers = {
#         "accept": "application/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMWUzNzcxMmI1YzdhYTBlODliMWMzYmVkMDQ1NjNmOSIsIm5iZiI6MTc1MzUzNDQyMC4yNzYsInN1YiI6IjY4ODRjZmQ0NTg1NTk3YzEwMGY3OGE2MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YAqA_sVG_k2GV7aUwnFB1gCwe1WfTgZ-T8f-KMWYzW8"
#     }

#     response = requests.get(url, headers=headers)
#     data = response.json()
#     backdrops = data.get('backdrops',[])
#     first_backdrop = backdrops[0]
#     image = first_backdrop['file_path']


#     return { 'image_url': image }

@app.get('/movie-details/{movie_id}')
def movie_details(movie_id : str):

    url = f"https://www.omdbapi.com/?t={movie_id}&apikey=3720d1a2"

    response = requests.get(url)
    data = response.json()
    image = data['Poster']
    return { 'image_url': image }


# @app.get('/trending-movies')
# def trending_movies():
#     movies_df = load_movies()
#     trending_movies = movies_df['year'] == 2025
#     return {'trending-movies': trending_movies}

@app.get('/')
def home():
    return f'Movie Recommendation System'

# Show list of Available movies
@app.get('/movies-list')
def get_movies_list():
    movies_df = load_movies()
    titles = movies_df['title'].tolist()
    id=  movies_df['id'].tolist()
    return {'movies': titles,'id':id}

@app.get('/recommendations/{movie_name}')
async def recommendations(movie_name : str):
    name = movie_name.lower()
    recommended_movies_list = []
    movies_df = load_movies()
    similarity = load_similarity_model()

    if name in movies_df['movie_title'].values:
        movie_index = movies_df[movies_df['movie_title'] == name].index[0]
        recomendation = sorted(list(enumerate(similarity[movie_index])), reverse = True, key = lambda x:x[1])[1:6]
        
        for i in recomendation:
            
            title = movies_df.iloc[i[0]].title
            id = int(movies_df.iloc[i[0]].id)

            recommended_movies_list.append ({
                
                'id' :  id,
                'title' : title

                })
       
        return { 'recommendations' : recommended_movies_list}
    else:
        return f'Movie - {movie_name} Not Found'