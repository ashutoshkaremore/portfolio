import os
from fastapi import FastAPI
import pickle
import pandas as pd


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

@app.get('/')
def home():
    return f'Movie Recommendation System'

# Show list of Available movies
@app.get('/movies-list')
def get_movies_list():
    movies_list = load_movies()
    movies_list['title'].to_dict() 
    return movies_list

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
            recommended_movies_list.append(movies_df.iloc[i[0]].title)
        return recommended_movies_list
    else:
        return f'Movie - {movie_name} Not Found'