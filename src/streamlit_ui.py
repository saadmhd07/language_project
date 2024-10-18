import streamlit as st
from bot import ChatBot

# Initialisation du chatbot
bot = ChatBot()

# Interface utilisateur Streamlit
st.title("Chatbot avec Together.ai")
st.write("Posez votre question ci-dessous :")

# Champ de saisie pour l'utilisateur
user_input = st.text_input("Votre question :")

# Initialiser l'historique dans la session Streamlit
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

# Lorsque l'utilisateur envoie une question
if st.button("Envoyer"):
    if user_input:
        # Appel au chatbot pour obtenir la réponse
        bot_response = bot.get_response(user_input)
        
        # Ajouter la question et la réponse à l'historique
        st.session_state["conversation"].append({"role": "user", "content": user_input})
        st.session_state["conversation"].append({"role": "assistant", "content": bot_response})

# Afficher l'historique des conversations
if st.session_state["conversation"]:
    st.write("**Historique de la conversation :**")
    for message in st.session_state["conversation"]:
        if message["role"] == "user":
            st.write(f"**Vous**: {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**Bot**: {message['content']}")