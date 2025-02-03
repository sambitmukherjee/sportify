import streamlit as st
import pandas as pd

st.image("orange_bg_logo.png", width=260)
st.logo("light_orange_logo.png", size="large")
st.title("Home")
st.divider()
users = pd.read_csv("users.csv")
full_name = users['first_name'][0] + " " + users['last_name'][0]
hello_message = f"Hello, {full_name}!"
st.html('<p style="font-size: 20px;">' + hello_message + '</p>')
dob = users['dob'][0]
st.html('<p style="font-size: 15px;">Date of Birth: ' + dob + '</p>')
st.divider()
"""
#### My Body
"""
body = pd.read_csv("body_current.csv")
current_body_issue = body['current_issue'][0]
st.html('<span style="font-size: 15px; font-weight: bold; color: #E4E2DC;">Current Issue:</span>')
st.html('<span style="font-size: 15px;">' + current_body_issue + '</span>')
st.html('<span style="font-size: 15px; font-weight: bold;">Current Training Advise:</span>')
advise = body['current_advise'][0]
st.write('<div style="color: #E4E2DC;">' + advise + '</div>', unsafe_allow_html=True) # Try either <div> or <span> for each element.
st.divider()
"""
#### My Mind
"""
mind = pd.read_csv("mind_current.csv")
current_mind_issue = mind['current_issue'][0]
st.html('<span style="font-size: 15px; font-weight: bold;">Current Issue:</span>')
st.html('<span style="font-size: 15px;">' + current_mind_issue + '</span>')
st.html('<span style="font-size: 15px; font-weight: bold;">Recommended Songs:</span>')
track_ids = mind['recommended_track_id'].tolist()
for i in range(10):
    iframe_string = f'<iframe style="border-radius: 12px; margin-bottom: -70px; padding-bottom: 0px;" src="https://open.spotify.com/embed/track/{track_ids[i]}?utm_source=generator" width="100%" height="150" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'        
    st.markdown(iframe_string, unsafe_allow_html=True)   
