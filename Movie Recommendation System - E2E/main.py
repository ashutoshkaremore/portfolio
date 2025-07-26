import streamlit as st
import requests


def get_movies_list():
    api_url = 'http://127.0.0.1:8000/movies-list'
    response = requests.get(api_url)
    data = response.json()
    #st.success("Movies List fetched successfully!")
    return data['movies']

def get_recommendations(movie_name):
    api_url = f'http://127.0.0.1:8000/recommendations/{movie_name}'
    response = requests.get(api_url)
    recommendations_data = response.json()
    #st.success("Recommendations fetched successfully!")
    return recommendations_data['recommendations']

@st.dialog("You Might Also Like")
def recommendations_dialog(watched_movie):
    movies = get_recommendations(watched_movie)
    for x in range(len(movies)):
        st.write(movies[x])

st.header("Movie Recommendation System :sunglasses:",divider=True)
option = st.selectbox(
    "Which Movie You Want To Watch",
    (get_movies_list()),
)

st.write("You Have Watched:", option)
#st.header("You Might Also Like",divider=True)
#st.write(get_recommendations(option))
recommendations_dialog(option)


#Footer
footer="""<style>
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
st.markdown(footer,unsafe_allow_html=True)