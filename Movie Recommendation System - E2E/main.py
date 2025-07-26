import streamlit as st
import requests
import random


def get_movies_list():
    api_url = 'http://127.0.0.1:8000/movies-list'
    response = requests.get(api_url)
    data = response.json()
    return data['movies']

def get_recommendations(movie_name):
    api_url = f'http://127.0.0.1:8000/recommendations/{movie_name}'
    response = requests.get(api_url)
    recommendations_data = response.json()
    return recommendations_data['recommendations']

def get_movie_details(movie_name):
    url = f'http://127.0.0.1:8000/movie-details/{movie_name}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        movie_poster = data['image_url']
        return movie_poster
    return None

@st.dialog("You Might Also Like", width="large")
def recommendations_dialog(watched_movie):
    movies = get_recommendations(watched_movie)
    image_not_found = 'https://png.pngtree.com/png-vector/20221125/ourmid/pngtree-no-image-available-icon-flatvector-illustration-thumbnail-graphic-illustration-vector-png-image_40966590.jpg'

    cols = st.columns(5)

    for i in range(len(movies)):
        image_url = get_movie_details(movies[i]['title'])
        with cols[i % 5]:
            if image_url:
                st.image(image_url)
            else:
                st.image(image_not_found, width=70)

            movie_title = movies[i]['title']
            st.write(movie_title)


if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False

if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'random_movies' not in st.session_state:

    st.session_state.random_movies = random.sample(range(0, 5001), 5)
if 'trending_images' not in st.session_state:
    st.session_state.trending_images = {}

st.header("Movie Recommendation System :sunglasses:", divider=True)

st.write("Top Trending Movies In Your Country")
cols = st.columns(5)

latest_movies = get_movies_list()

for i in range(len(st.session_state.random_movies)):
    with cols[i % 5]:
        movie = latest_movies[st.session_state.random_movies[i]]
        
        
        if movie not in st.session_state.trending_images:
            st.session_state.trending_images[movie] = get_movie_details(movie)
        
        image_url = st.session_state.trending_images[movie]
        if image_url:
            st.image(image_url)
        st.write(movie)
        
        
        button_key = f"watch_trending_{i}"
        if st.button(label='Watch', key=button_key):
            st.session_state.selected_movie = movie
            st.session_state.show_recommendations = True
            st.rerun()

st.write('-----')


option = st.selectbox(
    "Search A Movie",
    get_movies_list(),
)

if st.button(label='Watch', key="watch_search"):
    st.session_state.selected_movie = option
    st.session_state.show_recommendations = True
    st.rerun()


if st.session_state.show_recommendations and st.session_state.selected_movie:
    st.write('You have watched', st.session_state.selected_movie)
    recommendations_dialog(st.session_state.selected_movie)
    st.session_state.show_recommendations = False
    st.session_state.selected_movie = None

# Footer
footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
padding-top:10px
}
</style>
<div class="footer">
<p>Project By Ashutosh Karemore </p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)