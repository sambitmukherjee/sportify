import streamlit as st
import openai
import pandas as pd

openai_client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

@st.cache_data
def get_llm_response_body(messages, max_tokens=500, temperature=0.8): # You can change these default argument values later on...
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content

@st.cache_data
def get_body_response(user_input):
    if len(user_input) == 0:
        return ""
    elif len(user_input) > 0 and len(user_input) < 20:
        return "Sorry! Your input wasn't long enough. Can you please describe it in a bit more detail?"
    else:    
        messages = [
            {
                'role': "system",
                'content': "Follow a professional tone. Make the response as medically accurate as possible." # Context for the LLM.
            },
            {
                'role': "user",
                'content': user_input
            }
        ]
        response = get_llm_response_body(messages)
        return response

st.image("body.png", width=220)
st.logo("light_orange_logo.png", size="large")
st.html('<br>')
st.text_input(label="Describe the physical issue:", key="body_issue")
st.html('<br>')
try:
    advise = get_body_response(st.session_state.body_issue)
    if len(advise) == 0 or advise == "Sorry! Your input wasn't long enough. Can you please describe it in a bit more detail?":
        st.write(advise)
    else:
        st.html('<span style="font-size: 15px; font-weight: bold;">Here\'s my advise:</span>')
        st.write(advise)
        st.html('<br>')
        st.html('<span style="font-size: 12px; font-style: italic;">Sportify is still an app in progress and while it aims to deliver the most medically accurate response, it may have some flaws.</span>')
        # For persistence:
        body_current = pd.DataFrame({'id': [1], 'user_id': [1], 'current_issue': [st.session_state.body_issue], 'current_advise': [advise]})
        body_current.to_csv("body_current.csv", index=False)
except:
    st.write("Oops! Something went wrong. Please try after a couple of minutes.")
