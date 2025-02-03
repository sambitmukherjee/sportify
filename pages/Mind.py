import streamlit as st
import openai
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

openai_client = openai.OpenAI(api_key=st.secrets["openai_api_key"])
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=st.secrets["spotify_client_id"], client_secret=st.secrets["spotify_client_secret"]))

@st.cache_data
def get_llm_response_mind(messages, max_tokens=500, temperature=0.8): # You can change these default argument values later on...
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature, 
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

@st.cache_data
def get_spotify_track_ids(response):
    all_track_ids = []
    parsed_json = json.loads(response)
    for song in parsed_json['songs']:
        query = f"{song['track_name']} {song['artist_name']}"
        results = sp.search(q=query, limit=1, type="track")
        track_id = results['tracks']['items'][0]['id']
        all_track_ids.append(track_id)
    return all_track_ids

@st.cache_data
def get_mind_response(mind_issue, genre):
    if len(mind_issue) == 0:
        return ""
    elif len(mind_issue) > 0 and len(mind_issue) < 20:
        return "Sorry! Your input wasn't long enough. Can you please describe it in a bit more detail?"
    else:
        user_input = f"The issue I'm currently facing is: {mind_issue}. My chosen music genre is: {genre}."    
        messages = [
            {
                'role': "system",
                'content': """The user will provide you a current psychological issue he/she is facing. The user will also provide you a music genre.
        
        Based on these two inputs from the user, return 10 songs (along with artist names) that may benefit the user as a form of music therapy.

        No songs suggested should be explicit or have references to inappropiate or controversial topics. Choose from a wide variety of songs.

        Return your response in a JSON format with the following keys: 'track_name' and 'artist_name'.
        """
            },
            {
                'role': "user",
                'content': user_input
            }
        ]
        response = get_llm_response_mind(messages)
        return response

st.image("mind.png", width=220)
st.logo("light_orange_logo.png", size="large")
st.html('<br>')
st.text_input(label="Describe the mind issue:", key="mind_issue")
st.selectbox("Select a music genre:", ['Pop', 'Rock', 'Metal', 'Jazz', 'UK Rap', 'Bollywood', 'Funk', 'R & B', 'Hip Hop'], key="genre")
st.html('<br>')

try:
    response = get_mind_response(st.session_state.mind_issue, st.session_state.genre)
    if len(response) == 0 or response == "Sorry! Your input wasn't long enough. Can you please describe it in a bit more detail?":
        st.write(response)
    else:
        spotify_track_ids = get_spotify_track_ids(response)
        if len(spotify_track_ids) > 0:
            st.html('<span style="font-size: 15px; font-weight: bold;">Here are some song recommendations:</span>')
            for track_id in spotify_track_ids:
                iframe_string = f'<iframe style="border-radius:12px; margin-bottom: -70px;" src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" width="100%" height="150" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
                st.markdown(iframe_string, unsafe_allow_html=True)
            # For persistence:
            mind_current = pd.DataFrame({'id': [i for i in range(1, 11)], 'user_id': [1] * 10, 'current_issue': [st.session_state.mind_issue] * 10, 'recommended_track_id': spotify_track_ids})
            mind_current.to_csv("mind_current.csv", index=False)            
except:
    st.write("Oops! Something went wrong. Please try after a couple of minutes.")
