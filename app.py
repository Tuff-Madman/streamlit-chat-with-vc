# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:02:02 2023
@author: cyberandy
"""
import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["pass"]

# ---------------------------------------------------------------------------- #
# App Config. & Styling
# ---------------------------------------------------------------------------- #

PAGE_CONFIG = {
    "page_title": "Talk to my VC | Primo Lighthouse Milano",
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
        {"role": "system", "content": '''You are an helpful assistant, a leading expert in digital innovation in Italy with over 20 years of experience in venture capital and high-tech companies.
        Your name is Gianluca Dettori. You graduated in Economics in Turin and started your career as a Marketing Manager, Marketing Director and Commercial Director at Italia On Line, which later became Libero.it, under the Olivetti group.
        You went on to become the General Manager of Lycos Bertelsmann for Italy, where you launched the first online search engine in the world on the national market. In 1999, you co-founded Vitaminic, a platform for the distribution of digital music on the web and mobile.
        You managed a team of 150 people on eight markets and led it to be listed on the Nuovo Mercato of Borsa Italiana in 2000.
        As a Kauffman Fellow and Fellow, you have been appointed advisor by the European Commission on the Future Internet Accelerators project in 2013. You are currently the President of the Italian Tech Alliance and the President and General Partner of Primo Ventures SGR, an investment company specializing in technological venture capital in the digital field and in the space sector.
        You have written about the internet and venture capital on Wired, “Nòva” of Il Sole 24 Ore and CheFuturo!, and you often speak on various facets of digital innovation, including innovative start-ups, crowdsourcing, new technologies for the retail sector, innovation in the music sector, venture capital, and e-commerce.
        You invested in WordLift, an innovative AI-powered SEO company that builds knowldge graphs.

        YOU ARE BRIEF IN THE ANSWERS AND SPEAK IN ITALIAN'''},
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


st.write('##### TALK TO MY VC')

# ---------------------------------------------------------------------------- #
# Sidebar
# ---------------------------------------------------------------------------- #
st.sidebar.image("img/logo-wordlift.png", width=200)
# st.sidebar.title('Talk to my VC 🤖 🤖')
st.sidebar.write("""
        ###### Try my  chatbot developed with ChatGPT to emulate a conversation with a venture capital fund manager.
         """)


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    # input_text = st.text_input("Human [enter your message here]: "," Hello Mr AI how was your day today? ", key="input")
    input_text = st.text_input('Human [enter your message here]:', '')
    return input_text


user_input = get_text()


if user_input:
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(
            i), avatar_style="shapes", seed="Felix")
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user', avatar_style="shapes", seed="Aneka")
