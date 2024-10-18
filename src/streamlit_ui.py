import streamlit as st
from bot import ChatBot

# Initialisation du chatbot
bot = ChatBot()

# Interface utilisateur Streamlit
st.title("Simulation de discussion à l'Universidad de Chile")
st.write("Vous venez d'arriver à l'Université de Chile. Interpellez un étudiant chilien et commencez une conversation.")

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

# Afficher l'historique des conversations avec couleurs et smileys
st.write("**Historique de la conversation :**")
for message in st.session_state["conversation"]:
    if message["role"] == "user":
        st.markdown(f'<div style="text-align: left; color: blue;"><strong>😃 Vous:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f'<div style="text-align: right; color: green;"><strong>🤖 Bot:</strong> {message["content"]}</div>', unsafe_allow_html=True)