import streamlit as st
from app_pages.audio_conversation import audio_conversation
from app_pages.chat_page import chat_conversation

# Configure la page une seule fois ici
st.set_page_config(page_title="Langue Project", layout="wide")

st.sidebar.title("Menu")
page = st.sidebar.radio("Sélectionnez une page:", ("Chat Conversation", "Conversation Naturelle"))

if page == "Chat Conversation":
    chat_conversation()
elif page == "Conversation Naturelle":
    audio_conversation()