# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:02:02 2023
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
    "page_title": "Parla con il mio VC | Primo Lighthouse Milano",
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

# This function utilizes the OpenAI Completion API to generate a response based on the given prompt.
# The temperature setting of the API affects how random the response is.
# A higher temperature will generate more unpredictable responses while a
# lower temperature will lead to more predictable ones.

# def generate_response(prompt):
#    completions = openai.Completion.create(
#        engine="text-davinci-003",
#        prompt=prompt,
#        temperature=0.9,
#        max_tokens=150,
#        top_p=1,
#        frequency_penalty=0.0,
#        presence_penalty=0.6,
#        stop=[" Human:", " AI:"]
#   )

#    message = completions.choices[0].text
#   return message


def generate_response(prompt):
    messages = [
        {"role": "system", "content": st.secrets["system_prompt"]},
        {"role": "user", "content": prompt}
    ]

    completion = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages)

    return completion["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------- #
# Web Application
# ---------------------------------------------------------------------------- #


st.write('##### TALK TO MY VC')

#
# ---------------------------------------------------------------------------- #
# Sidebar
# ---------------------------------------------------------------------------- #
# st.sidebar.image("img/logo-wordlift.png", width=200)
# st.sidebar.title('Talk to my VC 🤖 🤖')
# st.sidebar.write("""
# Try my  chatbot developed with GPT-4 to emulate a conversation with a famous Italian Venture Capital Fund Manager 🇮🇹.
# You can ask him about his experience in the Venture Capital industry, his investment strategy, his portfolio companies, his opinion on the Italian startup ecosystem and much more.
# The chatbot is an experiment by [WordLift](https://wordlift.io/) and will speak in Italian (even if you write in English).
#         """)


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    return st.text_input('Human [enter your message here]:', '')


if user_input := get_text():
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(
            i), avatar_style="shapes", seed="Felix")
        message(
            st.session_state['past'][i],
            is_user=True,
            key=f'{str(i)}_user',
            avatar_style="shapes",
            seed="Aneka",
        )
