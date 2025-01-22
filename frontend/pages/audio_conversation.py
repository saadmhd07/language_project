import streamlit as st
import requests
from st_audiorec import st_audiorec

def audio_conversation():
    st.title("Conversation Naturelle Audio")
    st.write("Commencez à parler, et le chatbot vous répondra directement par audio.")

    # Sélection de la langue
    languages = {"🇫🇷 Français": "fr", "🇬🇧 English": "en", "🇪🇸 Español": "es"}
    selected_language = st.selectbox("Choisissez la langue d'apprentissage:", list(languages.keys()))

    # Enregistrement audio avec le composant st_audiorec
    audio_bytes = st_audiorec()

    if audio_bytes:
        st.write("Traitement de l'audio en cours...")

        # Envoyer l'audio au back-end Flask pour transcription
        files = {"audio": ("input.wav", audio_bytes, "audio/wav")}
        try:
            response = requests.post("http://127.0.0.1:5000/transcribe", files=files, data={"language": languages[selected_language]})
            st.write("Statut HTTP :", response.status_code)
            st.write("Réponse brute :", response.text)

            if response.status_code == 200:
                transcript = response.json().get("text", "Erreur de transcription")
                st.write(f"**Texte transcrit :** {transcript}")

                # Envoi du texte au chatbot pour obtenir une réponse
                chat_response = requests.post("http://127.0.0.1:5000/chat", json={"message": transcript, "scenario": "Arrival at University", "language": languages[selected_language]})
                
                if chat_response.status_code == 200:
                    bot_reply = chat_response.json().get("response", "Erreur de réponse")
                    st.write(f"**Réponse du bot :** {bot_reply}")

                    # Générer un fichier audio de la réponse
                    audio_response = requests.post("http://127.0.0.1:5000/synthesize", json={"text": bot_reply, "language": languages[selected_language]})
                    audio_path = audio_response.json().get("audio_path", "")

                    if audio_path:
                        st.audio(audio_path)
                    else:
                        st.error("Erreur lors de la synthèse audio.")
                else:
                    st.error("Erreur lors de la communication avec le bot.")
            else:
                st.error(f"Erreur lors de la transcription audio. Statut HTTP: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion au serveur Flask : {e}")