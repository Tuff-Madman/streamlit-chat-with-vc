# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 16:02:02 2023
@author: cyberandy
"""

# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #

import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["pass"]

# ---------------------------------------------------------------------------- #
# App Config. & Styling
# ---------------------------------------------------------------------------- #

PAGE_CONFIG = {
    "page_title": "Ask an SEO Expert",
    "page_icon": "img/fav-ico.png",
    "layout": "centered"
}


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.set_page_config(**PAGE_CONFIG)

local_css("style.css")


# ---------------------------------------------------------------------------- #
# Functions
# ---------------------------------------------------------------------------- #


def generate_response(prompt):
    messages = [
        {"role": "system", "content": st.secrets["system_prompt"]},
        {"role": "user", "content": prompt}
    ]

    completion = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages)

    content = completion["choices"][0]["message"]["content"]

    return content


# ---------------------------------------------------------------------------- #
# Web Application
# ---------------------------------------------------------------------------- #


st.write('##### ASK AN SEO EXPERT')

# ---------------------------------------------------------------------------- #
# Sidebar
# ---------------------------------------------------------------------------- #
st.sidebar.image("img/logo-wordlift.png", width=200)
st.sidebar.title('Ask an SEO Expert 💬')
st.sidebar.write("""
Try our latest chatbot to answer your top questions about search engine optimization.
\n\n
Have a question? [Let's talk](https://wordlift.io/contact-us) about it!.
\n\n
The chatbot is an experiment by [WordLift](https://wordlift.io/).""")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    # input_text = st.text_input("Human [enter your message here]: "," Hello Mr AI how was your day today? ", key="input")
    input_text = st.text_input('Human [enter your SEO question here]:', '')
    return input_text


user_input = get_text()


if user_input:
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(
            i), avatar_style="thumbs", seed="Aneka")
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user', avatar_style="thumbs", seed="Sambal")
