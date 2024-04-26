import streamlit as st
import pickle
import requests
from PIL import Image
from io import BytesIO


anime = pickle.load(open("anime.pkl", 'rb'))
cosine_sim = pickle.load(open("similarity.pkl", 'rb'))
anime_list=anime['title'].values

st.header("Anime Recommender System")

import streamlit.components.v1 as components

selectvalue=st.selectbox("Select anime from dropdown", anime_list)


def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = anime[anime['title']==title].index[0]
    

    distance = sorted(list(enumerate(cosine_sim[idx])), reverse=True, key=lambda vector:vector[1])
    recommend_anime=[]
    recommend_poster=[]
    for i in distance[1:6]:
        
        recommend_anime.append(anime.iloc[i[0]].title)
        url=anime.iloc[i[0]]['Poster']
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        nouvelle_taille = (250, 300)
        image_agrandie = image.resize(nouvelle_taille, Image.ANTIALIAS)

        recommend_poster.append(image_agrandie)

    return recommend_anime,recommend_poster


if st.button("Show Recommend"):
    anime_name,anime_poster = get_recommendations(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(anime_name[0])
        st.image(anime_poster[0])
    with col2:
        st.text(anime_name[1])
        st.image(anime_poster[1])
    with col3:
        st.text(anime_name[2])
        st.image(anime_poster[2])
    with col4:
        st.text(anime_name[3])
        st.image(anime_poster[3])
    with col5:
        st.text(anime_name[4])
        st.image(anime_poster[4])

   