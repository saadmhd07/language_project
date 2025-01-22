import streamlit as st
from pages.audio_conversation import audio_conversation
from pages.chat_page import chat_conversation

# Configuration de la page principale
st.set_page_config(page_title="Langue Project", layout="wide")

# Menu latéral pour naviguer entre les pages
st.sidebar.title("Menu")
page = st.sidebar.radio("Sélectionnez une page:", ("Chat Conversation", "Conversation Naturelle"))

if page == "Chat Conversation":
    chat_conversation()
elif page == "Conversation Naturelle":
    audio_conversation()