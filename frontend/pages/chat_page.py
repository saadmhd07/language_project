import streamlit as st
import requests

def chat_conversation():
    st.title("Chat avec le chatbot")

    # Sélection de la langue d'apprentissage (la langue dans laquelle le bot doit répondre)
    languages = {"🇫🇷 Français": "fr", "🇬🇧 English": "en", "🇪🇸 Español": "es"}
    selected_language = st.selectbox("Choisissez la langue d'apprentissage:", list(languages.keys()))
    learning_language = languages[selected_language]  # Obtenir le code de la langue sélectionnée

    # Champ de texte pour l'utilisateur
    user_input = st.text_input("Tapez votre message ici:")

    if st.button("Envoyer"):
        st.write("Envoi du message...")

        try:
            response = requests.post(
                "http://127.0.0.1:5000/chat",
                json={
                    "message": user_input,
                    "scenario": "Arrival at University",
                    "language": learning_language
                }
            )
            # Vérifier la réponse avant d'afficher
            st.write("Statut HTTP :", response.status_code)
            st.write("Réponse brute :", response.text)

            if response.status_code == 200:
                bot_response = response.json().get("response", "Aucune réponse reçue.")
                st.write(f"🤖 Bot ({selected_language}): {bot_response}")
            else:
                st.error("Erreur lors de la communication avec le bot.")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion : {e}")